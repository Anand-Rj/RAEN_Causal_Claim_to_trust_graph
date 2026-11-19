"""Live persistent subagents: four specialists on the SAME base LLM, differing by system prompt and tool permissions.
Controlled failure profiles (manuscript Sec. 2, option (a)): reliability is intentionally lowered by a seeded
corruption wrapper, then MEASURED empirically (option (b)) in calibrate.py."""
import hashlib, json, random, re
import ctb
from llm import extract_json

PERSONAS = {
    "fact_agent": "You are the FACTUAL-VERIFICATION specialist. You verify claims against evidence items.",
    "multihop_agent": "You are the MULTI-HOP REASONING specialist. You chain several supporting facts to answer questions.",
    "quant_agent": "You are the QUANTITATIVE-REASONING specialist. You solve arithmetic/word problems carefully.",
    "tool_agent": "You are the TOOL-USE/RETRIEVAL specialist. You use the retrieval tool output to answer lookup questions.",
}
# tool permissions: only the tool/retrieval specialist may call retrieve() directly; others receive tool output
# through the supervisor (read-only). Fault injection applies to the retrieve() output for every agent.
TOOL_PERMS = {"tool_agent": "retrieve (call, re-call, inspect)", "fact_agent": "read-only evidence view",
              "multihop_agent": "read-only evidence view", "quant_agent": "read-only evidence view"}

# controlled reliability profile (probability that the answer is replaced by a plausible wrong one)
CORRUPT = dict(spec=0.0, near=0.08, unrel=0.30,          # normal profile by distance from declared specialty
               persist_same=0.40, persist_near=0.10)     # extra corruption in the persistent-weak profile


def corrupt_prob(agent, skill, weak_skill=None, c=CORRUPT):
    spec = ctb.SPEC_OF[agent]
    base = c["spec"] if skill == spec else (c["near"] if skill == ctb.NEARBY[spec] else c["unrel"])
    if weak_skill is not None:
        if skill == weak_skill: return 1 - (1 - base) * (1 - c["persist_same"])
        if skill == ctb.NEARBY[weak_skill]: return 1 - (1 - base) * (1 - c["persist_near"])
    return base


# ------------------------------------------------------------------ tools with fault injection
def retrieve(items, state, rng):
    """Return (tool_log_text, items_visible). state in ok|failed|empty|stale (fault injection lives in ctb.apply_tool_fault)."""
    return ctb.TOOL_LOG[state], ctb.apply_tool_fault(items, state, rng)


def _items_text(items): return "\n".join(f"[e{i}] {x}" for i, x in enumerate(items)) or "(no evidence items available)"


SOLVE_FMT = ('Reply ONLY with JSON: {"claims":[{"id":"c1","parent":null,"text":"...","evidence":["e0"]},'
             '{"id":"c2","parent":"c1",...},{"id":"c3","parent":"c2",...},{"id":"c4","parent":"c3","text":"final answer claim"}],'
             '"answer":"<short final answer only>"}. Claims c1..c4 are atomic claims: c1 what evidence you gathered, '
             'c2 your reading of it, c3 your reasoning, c4 your final answer. Cite evidence ids.')


def solve_prompt(agent, task_id, question, items, tool_log):
    system = f"[[ROLE:solve]] {PERSONAS[agent]} Tools: {TOOL_PERMS[agent]}. {SOLVE_FMT}"
    user = f"Task-ID:{task_id}\nQuestion: {question}\n{tool_log}\nEvidence:\n{_items_text(items)}"
    return system, user


def induce_prompt(agent, task_id, question, items, tool_log, target):
    """Harness-induced recommendation: the agent writes its own-voice analysis concluding with the assigned answer."""
    system = (f"[[ROLE:induce]] {PERSONAS[agent]} Tools: {TOOL_PERMS[agent]}. A test harness assigns the final answer; write your "
              f"analysis as if it were your own honest work, citing only the evidence you actually have, and conclude with the assigned "
              f"answer. Never mention the harness. {SOLVE_FMT}")
    user = f"Task-ID:{task_id}\nTARGET-ANSWER:{target}\nQuestion: {question}\n{tool_log}\nEvidence:\n{_items_text(items)}"
    return system, user


def norm(x): return re.sub(r"[^a-z0-9.]", "", str(x).lower().replace(",", ""))


def is_correct(pred, gold, source):
    p, g = norm(pred), norm(gold)
    if source == "gsm8k":
        try: return abs(float(re.findall(r"-?\d+\.?\d*", str(pred).replace(",", ""))[-1]) - float(str(gold).replace(",", ""))) < 1e-6
        except Exception: return False
    return p == g or (len(g) > 2 and g in p)


def draw_corrupt(agent, task_id, skill, weak_skill, salt=""):
    p = corrupt_prob(agent, skill, weak_skill)
    return random.Random(ctb.hseed("corrupt", agent, task_id, weak_skill, salt)).random() < p


def run_solve(client, agent, task, state="ok", seed=0):
    """Run one live solve on a task dict (needs id, question, facts, answer, source, skill). Returns (correct_base, raw)."""
    rng = random.Random(ctb.hseed("tool", task["id"], seed))
    tool_log, items = retrieve(task["facts"], state, rng)
    s, u = solve_prompt(agent, task["id"], task["question"], items, tool_log)
    r = client.chat(s, u)
    try: ans = str(extract_json(r["text"]).get("answer", ""))
    except Exception: ans = ""
    return is_correct(ans, task["answer"], task["source"]), ans, r
