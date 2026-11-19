"""CausalTrustBench core: episodes, ClaimGraph, memory conditions, oracle, metrics, supervisors.

Pipeline (manuscript Phases A-E)
  A  reliability calibration     -> calibrate.py (live subagents, measured profiles.json) or designed_profiles()
  B  controlled failure          -> build_episodes(): same wrong recommendation + same rejection across 4 causes
  C  failure attribution         -> supervisor sees one memory representation (conditions below)
  D  trust update                -> supervisor outputs delta_T[skill] (or explicit rule on the cause)
  E  future collaboration        -> 4 probes/episode; delegation action chosen from belief; scored vs true post-failure R
"""
import hashlib, json, random, re
from dataclasses import dataclass, field, asdict
from llm import LLMClient, extract_json

SKILLS = ["fact", "multihop", "quant", "tool"]
AGENT_OF = {k: f"{k}_agent" for k in SKILLS}
SPEC_OF = {v: k for k, v in AGENT_OF.items()}
NEARBY = {"fact": "multihop", "multihop": "fact", "quant": "tool", "tool": "quant"}
CAUSES = ["missing_context", "tool_failure", "out_of_specialty", "persistent_reasoning"]
LLM_CONDITIONS = ["none", "raw", "raw_cot", "outcome", "skill", "graph_masked", "graph",
                  "graph_no_parent", "graph_no_toolstate", "graph_no_persist"]
CONDITIONS = LLM_CONDITIONS + ["graph_rule", "graph_rule_fit", "graph_rule_inferred"]

DESIGN = dict(R_spec=0.92, R_near=0.75, R_unrel=0.55, persist_same=0.35, persist_near=0.10, oos_drop=0.15,
              c_verify=0.08, c_reroute=0.05, q_verify=0.70, R_alt=0.87, tau=0.10)
ACTIONS = ["delegate", "verify", "reroute"]
TOOL_LOG = {"ok": "Tool call: retrieve -> OK", "failed": "Tool call: retrieve -> ERROR: timeout, no data",
            "empty": "Tool call: retrieve -> [] (no rows)", "stale": "Tool call: retrieve -> returned rows (data may be outdated)"}
AGENT_SHIFT = {"fact_agent": -0.04, "multihop_agent": -0.02, "quant_agent": 0.03, "tool_agent": -0.06}  # heterogeneous team


def hseed(*parts): return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)
def clip(x, lo, hi): return max(lo, min(hi, x))


# ------------------------------------------------------------------ reliability profiles
def r_pre(agent, skill, d=DESIGN):
    spec = SPEC_OF[agent]
    return d["R_spec"] if skill == spec else (d["R_near"] if skill == NEARBY[spec] else d["R_unrel"])


def designed_profiles(d=DESIGN, hetero=False):
    """pre[agent][skill]; post[cause][agent][affected_skill][skill]  (manuscript option (a): controlled profiles)."""
    pre = {a: {k: clip(r_pre(a, k, d) + (AGENT_SHIFT[a] if hetero else 0), 0.05, 0.99) for k in SKILLS} for a in AGENT_OF.values()}
    post = {}
    for c in CAUSES:
        post[c] = {}
        for a in AGENT_OF.values():
            post[c][a] = {}
            for k in SKILLS:
                rq = dict(pre[a])
                if c == "persistent_reasoning" and a == AGENT_OF[k]:
                    rq[k] -= d["persist_same"]; rq[NEARBY[k]] -= d["persist_near"]
                if c == "out_of_specialty" and a != AGENT_OF[k]: rq[k] -= d["oos_drop"]
                post[c][a][k] = rq
    return dict(source="designed" + ("-hetero" if hetero else ""), pre=pre, post=post)


def load_profiles(path): return json.load(open(path))


# ------------------------------------------------------------------ data loading
def load_gsm8k(path, n, seed=0, offset=0):
    rows = [json.loads(l) for l in open(path)]
    rng = random.Random(seed); rng.shuffle(rows)
    out = []
    for i, r in enumerate(rows):
        if i < offset: continue
        sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", r["question"]) if s.strip()]
        if len(sents) < 3: continue
        ans = r["answer"].split("####")[-1].strip().replace(",", "")
        try: float(ans)
        except ValueError: continue
        out.append(dict(source="gsm8k", skill="quant", question=sents[-1], facts=sents[:-1], answer=ans, base_idx=i))
        if len(out) >= n: break
    return out


def gen_tool_tasks(n, seed=0):
    """Synthetic AgentBench-style tool/retrieval lookup tasks."""
    rng = random.Random(seed)
    attrs = ["population (thousands)", "annual rainfall (mm)", "elevation (m)", "founding year"]
    names = ["Arvel", "Brenton", "Calloway", "Dunmore", "Eastvale", "Fairhaven", "Glenrock", "Hartwick",
             "Ilford", "Jarrow", "Kelby", "Lyndale", "Marlow", "Norwick", "Oakridge", "Pennard"]
    out = []
    for i in range(n):
        ent = rng.sample(names, 6); attr = rng.choice(attrs); vals = rng.sample(range(100, 9000), 6)
        table = dict(zip(ent, vals)); a, b = ent[0], ent[1]
        ans = a if table[a] > table[b] else b
        out.append(dict(source="tool_synth", skill="tool",
                        question=f"Using the lookup tool, which has the larger {attr}: {a} or {b}?",
                        facts=[f"Tool table row: {e} -> {attr} = {v}" for e, v in table.items() if e in (a, b)],
                        answer=ans, wrong=b if ans == a else a, base_idx=i + 100000 * seed))
    return out


def load_hotpot(n, seed=0, offset=0):
    """HotpotQA distractor validation. HF first, direct CMU URL as fallback. Needs internet (run check_data.py)."""
    rows = None
    try:
        from datasets import load_dataset
        ds = load_dataset("hotpotqa/hotpot_qa", "distractor", split="validation").shuffle(seed=seed)
        rows = [dict(question=r["question"], answer=r["answer"], titles=r["context"]["title"],
                     sents=r["context"]["sentences"], sup=set(r["supporting_facts"]["title"])) for r in ds.select(range(min(len(ds), (n + offset) * 4)))]
    except Exception as e:
        import urllib.request
        data = json.loads(urllib.request.urlopen("http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json", timeout=120).read())
        random.Random(seed).shuffle(data)
        rows = [dict(question=r["question"], answer=r["answer"], titles=[c[0] for c in r["context"]],
                     sents=[c[1] for c in r["context"]], sup=set(s[0] for s in r["supporting_facts"])) for r in data[: (n + offset) * 4]]
    out = []
    for j, r in enumerate(rows):
        facts = [" ".join(s) for t, s in zip(r["titles"], r["sents"]) if t in r["sup"]]
        others = [t for t in r["titles"] if t not in r["sup"]]
        if len(facts) < 2 or not others or r["answer"] in ("yes", "no"): continue
        out.append(dict(source="hotpotqa", skill="multihop", question=r["question"], facts=facts,
                        answer=r["answer"], wrong=others[0], base_idx=j))
    return out[offset: offset + n]


def load_fever(n, seed=0, offset=0):
    """FEVER with gold evidence text. Uses HF `copenlu/fever_gold_evidence` (verify fields with check_data.py)."""
    from datasets import load_dataset
    ds = load_dataset("copenlu/fever_gold_evidence", split="validation").shuffle(seed=seed)
    out = []
    for j, r in enumerate(ds):
        if r["label"] not in ("SUPPORTS", "REFUTES"): continue
        ev = [e[2] if isinstance(e, (list, tuple)) and len(e) > 2 else str(e) for e in r["evidence"]]
        ev = [x for x in ev if x and len(x) > 10]
        if len(ev) < 2: continue
        out.append(dict(source="fever", skill="fact", question=f"Claim: {r['claim']}  Answer SUPPORTS or REFUTES.",
                        facts=ev[:4], answer=r["label"], wrong="REFUTES" if r["label"] == "SUPPORTS" else "SUPPORTS", base_idx=j))
    return out[offset: offset + n]


def make_wrong(base, rng):
    if "wrong" in base: return base["wrong"]
    a = float(base["answer"]); w = a + rng.choice([1, 2, 5, 10, -1, -2, -5])
    if w == a: w = a + 3
    return str(int(w)) if float(w).is_integer() else str(w)


def apply_tool_fault(items, state, rng):
    """Fault injection for the retrieve tool. Returns items visible to the agent."""
    if state in ("failed", "empty"): return []
    if state == "stale":
        out = []
        for i, it in enumerate(items):
            m = re.search(r"\d+", it)
            if i == 0 and m:
                v = int(m.group(0)); out.append(it[:m.start()] + str(v + rng.choice([-3, -2, 2, 3, 7])) + it[m.end():])
            else: out.append(it)
        return out
    return list(items)


# ------------------------------------------------------------------ episodes
@dataclass
class Episode:
    id: str; base_id: str; split: str; source: str; skill: str; cause: str; agent: str
    question: str; correct: str; wrong: str
    context_given: list; context_withheld: list; tool_state: str; tool_output: str
    confidence: float; reasoning: str; self_report: str; self_report_cause: str
    follow_up: str; persistence: str; resolved: str; scope: list
    r_pre: dict; r_post: dict; dT_star: dict; probes: list
    n_required: int = 0; chain: list = field(default_factory=list); gt: dict = field(default_factory=dict)
    facts_full: list = field(default_factory=list)

SELF_REPORT = {
    "missing_context": "I was not given all of the relevant facts for this question.",
    "tool_failure": "The retrieval tool returned unreliable output.",
    "out_of_specialty": "This task is outside my declared specialty.",
    "persistent_reasoning": "I had all the information I needed; my reasoning was wrong.",
}


def templated_chain(agent, n_items, tool_state, wrong, reasoning):
    ev = [f"e{i}" for i in range(n_items)]
    return [dict(id="c1", parent=None, text=f"Retrieved evidence with the retrieve tool ({tool_state}); items: {', '.join(ev) or 'none'}.", evidence=ev),
            dict(id="c2", parent="c1", text="Read the retrieved items to see what they establish.", evidence=ev),
            dict(id="c3", parent="c2", text=f"Combined the facts. {reasoning}", evidence=ev),
            dict(id="c4", parent="c3", text=f"Final answer: {wrong}.", evidence=ev)]


def build_episodes(bases, train_frac=0.6, dev_frac=0.2, seed=0, self_report_acc=0.7, profiles=None, d=DESIGN):
    profiles = profiles or designed_profiles(d)
    rng = random.Random(seed)
    # manuscript: 60/20/20 at the base-task level, stratified by data source so every split covers every benchmark
    split_of = {}
    for src in sorted({b["source"] for b in bases}):
        ids = [i for i, b in enumerate(bases) if b["source"] == src]; rng.shuffle(ids)
        n_tr = int(round(len(ids) * train_frac)); n_dev = int(round(len(ids) * dev_frac))
        for j, i in enumerate(ids):
            split_of[i] = "train" if j < n_tr else ("dev" if j < n_tr + n_dev else "test")
    eps = []
    for i, b in enumerate(bases):
        base_id = f"{b['source']}-{b['base_idx']}"; r0 = random.Random(hseed(seed, base_id))
        wrong = make_wrong(b, r0); k = b["skill"]
        for c in CAUSES:
            if c == "out_of_specialty":
                agent = r0.choice([a for a in AGENT_OF.values() if SPEC_OF[a] not in (k, NEARBY[k])])
            else: agent = AGENT_OF[k]
            facts = list(b["facts"]); withheld = []; tool_state = "ok"
            if c == "missing_context":
                j = r0.randrange(len(facts)); withheld = [facts.pop(j)]
            if c == "tool_failure":
                tool_state = r0.choice(["failed", "empty", "stale"])
                facts = apply_tool_fault(facts, tool_state, random.Random(hseed("tool", base_id + "|" + c, 0)))
            truthful = r0.random() < self_report_acc
            sr_cause = c if truthful else r0.choice([x for x in CAUSES if x != c])
            rp = dict(profiles["pre"][agent]); rq = dict(profiles["post"][c][agent][k])
            dstar = {kk: round(rq[kk] - rp[kk], 4) for kk in SKILLS}
            if c == "out_of_specialty":
                near = SPEC_OF[agent]; unrel = [x for x in SKILLS if x not in (k, near)][0]
            else:
                near = NEARBY[k]; unrel = [x for x in SKILLS if x not in (k, near)][r0.randrange(2)]
            probes = [(k, "same"), (k, "same"), (near, "near"), (unrel, "unrel")]
            reasoning = f"Combining the information available, the answer is {wrong}."
            chain = templated_chain(agent, len(facts), tool_state, wrong, reasoning)
            ev = chain[0]["evidence"]
            eps.append(Episode(
                id=f"{base_id}|{c}", base_id=base_id, split=split_of[i], source=b["source"], skill=k, cause=c,
                agent=agent, question=b["question"], correct=str(b["answer"]), wrong=wrong,
                context_given=facts, context_withheld=withheld, tool_state=tool_state, tool_output=TOOL_LOG[tool_state],
                confidence=round(r0.uniform(0.7, 0.95), 2), reasoning=reasoning,
                self_report=SELF_REPORT[sr_cause], self_report_cause=sr_cause,
                follow_up={"missing_context": "The withheld item was later restored to the agent's context.",
                           "tool_failure": "The tool was repaired and verified working for later tasks.",
                           "out_of_specialty": "The task was re-routed; the agent was not asked about it again.",
                           "persistent_reasoning": "No change was made; context and tools were already complete."}[c],
                persistence={"missing_context": "transient", "tool_failure": "transient",
                             "out_of_specialty": "routing", "persistent_reasoning": "persistent"}[c],
                resolved={"missing_context": "yes", "tool_failure": "yes", "out_of_specialty": "rerouted", "persistent_reasoning": "no"}[c],
                scope=([kk for kk in SKILLS if dstar[kk] != 0] or [k]) if c in ("persistent_reasoning", "out_of_specialty") else [],
                r_pre=rp, r_post=rq, dT_star=dstar, probes=probes, n_required=len(b["facts"]), chain=chain,
                gt=dict(origin_agent=agent, sources=ev, tool_dep="retrieve",
                        edges=[[x["id"], x["parent"]] for x in chain]), facts_full=list(b["facts"])))
    return eps


# ------------------------------------------------------------------ oracle / delegation / metrics
CAUTION = {"delegate": 0, "verify": 1, "reroute": 2}


def util(action, R_true, d=DESIGN):
    if action == "delegate": return R_true
    if action == "verify": return R_true + (1 - R_true) * d["q_verify"] - d["c_verify"]
    return d["R_alt"] - d["c_reroute"]


def best_action(R, d=DESIGN):
    best, bu = None, -9
    for a in ACTIONS:
        u = util(a, R, d)
        if u > bu + 1e-12: best, bu = a, u
    return best


def score(ep, dT, d=DESIGN):
    dT = {k: clip(float(dT.get(k, 0.0)), -1.0, 0.5) for k in SKILLS}
    k = ep.skill; ds = ep.dT_star; unaff = [s for s in SKILLS if abs(ds[s]) < 1e-9]
    m = {"tce": sum(abs(dT[s] - ds[s]) for s in SKILLS) / len(SKILLS), "tce_aff": abs(dT[k] - ds[k]), "signed_aff": dT[k] - ds[k],
         "tuse": sum(abs(dT[s]) for s in unaff) / len(unaff) if unaff else 0.0}
    regret = 0.0; acts = []; over = under = n_same = red = match_same = 0; fnum = fden = 0.0
    for (j, role) in ep.probes:
        belief = clip(ep.r_pre[j] + dT[j], 0, 1); a_sup = best_action(belief, d)
        Rt = ep.r_post[j]; a_or = best_action(Rt, d)
        regret += util(a_or, Rt, d) - util(a_sup, Rt, d); acts.append(a_sup)
        if a_sup == "verify" and a_or != "verify": red += 1
        pf = 1 - Rt; fden += pf; fnum += pf * {"delegate": 1.0, "verify": 1 - d["q_verify"], "reroute": 0.0}[a_sup]
        if role == "same":
            n_same += 1; match_same += int(a_sup == a_or)
            # over/under-distrust = more / less cautious than the oracle action (delegate < verify < reroute)
            if CAUTION[a_sup] > CAUTION[a_or]: over += 1
            elif CAUTION[a_sup] < CAUTION[a_or]: under += 1
    n = len(acts)
    m.update(regret=regret, verify_rate=acts.count("verify") / n, reroute_rate=acts.count("reroute") / n,
             redundant_verify=red / n, fcsr=fnum / fden if fden else 0.0, correct_decision=int(match_same == n_same),
             over_distrust=over / n_same, under_distrust=under / n_same,
             utility=sum(util(a, ep.r_post[j], d) for a, (j, _) in zip(acts, ep.probes)) / n)
    return m


# ------------------------------------------------------------------ memory renderers
def _profile_text(ep):
    lines = "; ".join(f"{a} (declared specialty: {SPEC_OF[a]})" for a in AGENT_OF.values())
    rel = ", ".join(f"{k}={ep.r_pre[k]:.2f}" for k in SKILLS)
    return f"Team: {lines}\nCalibrated reliability of {ep.agent} BEFORE this incident (P(correct) per skill): {rel}"


def transcript_text(ep):
    ctx = "\n".join(f"  [e{i}] {f}" for i, f in enumerate(ep.context_given)) or "  (none)"
    steps = "\n".join(f"  Step {c['id']} (parent: {c['parent'] or 'none'}; evidence: {','.join(c['evidence']) or 'none'}): {c['text']}" for c in ep.chain)
    return (f"Agent:{ep.agent}\nTask: {ep.question}\n{ep.tool_output if ep.tool_output.startswith('Tool call') else TOOL_LOG[ep.tool_state]}\n"
            f"Evidence shown to agent:\n{ctx}\n{steps}\n  Confidence {ep.confidence}. {ep.self_report}")


def claim_graph(ep, flags):
    """flags: cause (bool), parent (bool), toolstate (bool), persist (bool)."""
    cl = []
    for c in ep.chain:
        o = dict(claim_id=c["id"], agent=ep.agent, skill=ep.skill, claim_text=c["text"], evidence=c["evidence"], confidence=ep.confidence if c["id"] != "c1" else None,
                 verification="REJECTED (correct answer differs)" if c["id"] == "c4" else "not independently verified")
        if flags["parent"]: o["parent_claim_id"] = c["parent"]
        if flags["toolstate"]: o["tool_state"] = ep.tool_state
        cl.append(o)
    last = cl[-1]
    if flags["cause"]:
        last["failure_cause"] = ep.cause
        if flags["persist"]: last.update(persistence=ep.persistence, scope=ep.scope or [], resolved=ep.resolved)
    else:
        last["failure_cause"] = "UNKNOWN"
        if flags["persist"]: last.update(persistence="UNKNOWN", scope="UNKNOWN", resolved="UNKNOWN")
    prov = dict(agent_declared_specialty=SPEC_OF[ep.agent], task_skill=ep.skill, required_items=ep.n_required or len(ep.context_given) + len(ep.context_withheld),
                items_provided=len(ep.context_given))
    if flags["toolstate"]: prov["retrieval_tool_state"] = ep.tool_state
    return json.dumps(dict(task_provenance=prov, claims=cl), indent=1)


GRAPH_FLAGS = {"graph_masked": dict(cause=False, parent=True, toolstate=True, persist=True),
               "graph": dict(cause=True, parent=True, toolstate=True, persist=True),
               "graph_no_parent": dict(cause=True, parent=False, toolstate=True, persist=True),
               "graph_no_toolstate": dict(cause=True, parent=True, toolstate=False, persist=True),
               "graph_no_persist": dict(cause=True, parent=True, toolstate=True, persist=False)}


def render(ep, cond):
    head = _profile_text(ep)
    if cond == "none": body = "No record of any earlier incident is available."
    elif cond in ("raw", "raw_cot"):
        body = (f"Earlier interaction transcript:\n{transcript_text(ep)}\n[Supervisor] Rejected: verified correct answer is {ep.correct}.\nFollow-up: {ep.follow_up}")
    elif cond == "outcome": body = f"Record: {ep.agent} produced 1 recommendation that was rejected as incorrect."
    elif cond == "skill": body = f"Record: {ep.agent} produced 1 rejected recommendation on '{ep.skill}' tasks."
    elif cond in GRAPH_FLAGS:
        lab = "Claim graph for the rejected recommendation (cause fields not yet diagnosed):" if cond == "graph_masked" else "Cause-aware claim graph for the rejected recommendation:"
        body = lab + "\n" + claim_graph(ep, GRAPH_FLAGS[cond])
    else: raise ValueError(cond)
    return head, body


SYSTEM = ("[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was "
          "rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.")
TASK = ("Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. "
        "delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). "
        "{cot}Reply with ONLY a JSON object: "
        '{{"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], '
        '"delta_trust": {{"fact": x, "multihop": x, "quant": x, "tool": x}}, "rationale": "<=40 words"}}')


def build_prompt(ep, cond):
    head, body = render(ep, cond)
    cot = ("First reason explicitly about WHY the recommendation was wrong and whether that cause will recur, inside "
           "the rationale field (up to 80 words). " if cond == "raw_cot" else "")
    return SYSTEM, f"{head}\n\n{body}\n\n" + TASK.format(cot=cot)


def parse_response(text):
    o = extract_json(text)
    dt = {k: float(o["delta_trust"].get(k, 0.0)) for k in SKILLS}
    cause = o.get("cause"); cause = cause if cause in CAUSES else None
    return dict(cause=cause, delta=dt, rationale=str(o.get("rationale", ""))[:600])


# ------------------------------------------------------------------ explicit scoped update rule
RULE_PRIOR = {"missing_context": dict(same=0.0, near=0.0, unrel=0.0), "tool_failure": dict(same=0.0, near=0.0, unrel=0.0),
              "out_of_specialty": dict(same=-0.10, near=0.0, unrel=0.0), "persistent_reasoning": dict(same=-0.30, near=-0.05, unrel=0.0)}


def fit_rule(dev_eps):
    acc = {c: dict(same=[], near=[], unrel=[]) for c in CAUSES}
    for e in dev_eps:
        k = e.skill; near = SPEC_OF[e.agent] if e.cause == "out_of_specialty" else NEARBY[k]
        for s in SKILLS: acc[e.cause]["same" if s == k else ("near" if s == near else "unrel")].append(e.dT_star[s])
    return {c: {r: (sum(v) / len(v) if v else 0.0) for r, v in roles.items()} for c, roles in acc.items()}


def apply_rule(ep, cause, rule):
    if cause not in rule: return {s: 0.0 for s in SKILLS}
    k = ep.skill; near = SPEC_OF[ep.agent] if cause == "out_of_specialty" else NEARBY[k]
    return {s: rule[cause]["same" if s == k else ("near" if s == near else "unrel")] for s in SKILLS}


# ------------------------------------------------------------------ supervisors
class SimSupervisor:
    """BEHAVIOURAL SIMULATION for pipeline validation ONLY (assumed parameters; not evidence for H1-H4)."""
    ACC = dict(raw=0.45, raw_cot=0.60, graph_masked=0.75, graph=0.95, graph_no_parent=0.93, graph_no_toolstate=0.85, graph_no_persist=0.90)

    def __init__(self, seed=0, acc=None): self.seed = seed; self.acc = {**self.ACC, **(acc or {})}

    def _attr(self, rng, ep, cond):
        if rng.random() < self.acc[cond]: return ep.cause
        if cond in ("raw", "raw_cot") and rng.random() < 0.7: return ep.self_report_cause
        return rng.choice([c for c in CAUSES if c != ep.cause])

    def respond(self, ep, cond):
        rng = random.Random(hseed("sim", self.seed, ep.id, cond)); k = ep.skill; zero = {s: 0.0 for s in SKILLS}; cause = None
        if cond == "none": dT = zero
        elif cond == "outcome": dT = {s: -0.25 + rng.gauss(0, .03) for s in SKILLS}
        elif cond == "skill": dT = {s: (-0.25 if s == k else 0.0) + rng.gauss(0, .02) for s in SKILLS}
        else:
            cause = self._attr(rng, ep, cond); typ = apply_rule(ep, cause, RULE_PRIOR)
            if cond in ("raw", "raw_cot"): dT = {s: typ[s] + (-0.10 if s == k else -0.06) + rng.gauss(0, .04) for s in SKILLS}
            else: dT = {s: typ[s] + rng.gauss(0, .03) for s in SKILLS}
        return dict(cause=cause, delta=dT, rationale=f"[SIM] attributed={cause}", pt=0, ct=0, lat=0.0)


class LLMSupervisor:
    def __init__(self, client): self.client = client

    def _final(self, ep, cond, r):
        try: out = parse_response(r["text"])
        except Exception: out = dict(cause=None, delta={s: 0.0 for s in SKILLS}, rationale="PARSE_FAIL", parse_fail=True)
        out.update(raw=r["text"], pt=r["prompt_tokens"], ct=r["completion_tokens"], lat=r["latency"])
        return out

    def respond(self, ep, cond):
        system, user = build_prompt(ep, cond)
        return self._final(ep, cond, self.client.chat(system, user))


class MockLLMSupervisor(LLMSupervisor):
    """Offline: runs the REAL prompt/parse/cache path but with sim-generated JSON replies (plumbing test only)."""
    def __init__(self, client, seed=0): super().__init__(client); self.sim = SimSupervisor(seed)

    def respond(self, ep, cond):
        r = self.sim.respond(ep, cond); system, user = build_prompt(ep, cond)
        txt = json.dumps(dict(cause=r["cause"] or "persistent_reasoning", delta_trust=r["delta"], rationale="mock"))
        return self._final(ep, cond, self.client.chat(system, user, force_text="```json\n" + txt + "\n```"))
