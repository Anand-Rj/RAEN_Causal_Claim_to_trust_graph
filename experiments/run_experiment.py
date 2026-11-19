#!/usr/bin/env python3
"""Run CausalTrustBench (manuscript Phases B-E).  See README.md for the full ordered runbook.
  python run_experiment.py --backend sim  --out out_sim                  # pipeline check, NO LLM (assumed behaviours)
  python run_experiment.py --backend mock --out out_mock ...             # tests the real prompt/parse path offline
  python run_experiment.py --backend openrouter --model openai/gpt-4o-mini --profiles calib/profiles.json \
      --probe-answers calib/probe_answers.json --live-transcripts --provenance --seeds 3 --temperature 0.7 --out out_gpt4omini
"""
import argparse, csv, json, os, sys
from concurrent.futures import ThreadPoolExecutor
import ctb, transcripts, provenance, llm
from llm import LLMClient


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["sim", "mock", "openrouter"], default="sim")
    ap.add_argument("--model", default="openai/gpt-4o-mini"); ap.add_argument("--gsm-path", default="gsm8k_test.jsonl")
    ap.add_argument("--n-gsm", type=int, default=50); ap.add_argument("--n-tool", type=int, default=50)
    ap.add_argument("--n-hotpot", type=int, default=50); ap.add_argument("--n-fever", type=int, default=50)
    ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--train-frac", type=float, default=0.6); ap.add_argument("--dev-frac", type=float, default=0.2); ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--profiles", default="designed", help="designed | designed-hetero | path/to/profiles.json (measured)")
    ap.add_argument("--probe-answers", default=None); ap.add_argument("--live-transcripts", action="store_true")
    ap.add_argument("--provenance", action="store_true"); ap.add_argument("--out", default="out"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)

    bases = []
    if a.n_gsm: bases += ctb.load_gsm8k(a.gsm_path, a.n_gsm)
    if a.n_tool: bases += ctb.gen_tool_tasks(a.n_tool)
    if a.n_hotpot: bases += ctb.load_hotpot(a.n_hotpot)
    if a.n_fever: bases += ctb.load_fever(a.n_fever)
    prof = ctb.designed_profiles(hetero=False) if a.profiles == "designed" else ctb.designed_profiles(hetero=True) if a.profiles == "designed-hetero" else ctb.load_profiles(a.profiles)
    eps = ctb.build_episodes(bases, train_frac=a.train_frac, dev_frac=a.dev_frac, profiles=prof)
    n_sup = len(eps) * len(ctb.LLM_CONDITIONS) * a.seeds
    print(f"{len(bases)} base tasks -> {len(eps)} episodes | profiles: {prof['source']} | supervisor calls: {n_sup}"
          f" + transcripts: {len(eps) if a.live_transcripts else 0} + provenance: {len(eps) * a.seeds if a.provenance else 0}")
    if a.dry_run: return
    banner = "SIMULATION - NOT LLM RESULTS" if a.backend in ("sim", "mock") else f"LLM:{a.model} | profiles:{prof['source']}"
    for e in eps: llm.MOCK_TRUTH[e.id] = dict(answer=e.correct, wrong=e.wrong)

    mk = lambda seed, tag: LLMClient(a.model, a.temperature, seed, f"{a.out}/cache_{tag}.jsonl", mock=(a.backend == "mock"))
    if a.live_transcripts and a.backend != "sim":
        c0 = LLMClient(a.model, 0.0, 0, f"{a.out}/cache_transcripts.jsonl", mock=(a.backend == "mock"))
        ok, n = transcripts.build_transcripts(c0, eps, a.workers, mock=(a.backend == "mock")); print(f"live transcripts: {ok}/{n} parsed (rest keep templated chain)")
    with open(f"{a.out}/episodes.jsonl", "w") as f:
        for e in eps: f.write(json.dumps(ctb.asdict(e)) + "\n")
    train = [e for e in eps if e.split == "train"]; rule_fit = ctb.fit_rule(train); json.dump(rule_fit, open(f"{a.out}/rule_fit.json", "w"), indent=1)
    pe = None
    if a.probe_answers:
        import phase_e; pe = phase_e.ProbeExec(a.probe_answers)

    rows, trans, prov_rows, usage = [], [], [], {}
    for seed in range(a.seeds):
        if a.backend == "sim": sup = ctb.SimSupervisor(seed); client = None
        else:
            if a.backend == "openrouter" and not os.environ.get("OPENROUTER_API_KEY"): sys.exit("Set OPENROUTER_API_KEY in your shell first.")
            client = mk(seed, f"sup_seed{seed}"); sup = ctb.MockLLMSupervisor(client, seed) if a.backend == "mock" else ctb.LLMSupervisor(client)
        jobs = [(e, c) for e in eps for c in ctb.LLM_CONDITIONS]
        with ThreadPoolExecutor(a.workers if a.backend == "openrouter" else 1) as ex: res = list(ex.map(lambda j: sup.respond(*j), jobs))
        resp = {(e.id, c): r for (e, c), r in zip(jobs, res)}
        if client: usage[f"supervisor_seed{seed}"] = client.stats
        if a.provenance:
            pc = mk(seed, f"prov_seed{seed}")
            with ThreadPoolExecutor(a.workers if a.backend == "openrouter" else 1) as ex: pres = list(ex.map(lambda e: provenance.extract(pc, e), eps))
            for e, r in zip(eps, pres):
                prov_rows.append(dict(seed=seed, ep=e.id, base=e.base_id, split=e.split, source=e.source, cause=e.cause, **provenance.score(e, r)))
            usage[f"provenance_seed{seed}"] = pc.stats
        for e in eps:
            for c in ctb.CONDITIONS:
                if c == "graph_rule": r = dict(cause=e.cause, delta=ctb.apply_rule(e, e.cause, ctb.RULE_PRIOR), rationale="rule(prior)")
                elif c == "graph_rule_fit": r = dict(cause=e.cause, delta=ctb.apply_rule(e, e.cause, rule_fit), rationale="rule(fit on train split)")
                elif c == "graph_rule_inferred":
                    inf = resp[(e.id, "graph_masked")]["cause"]; r = dict(cause=inf, delta=ctb.apply_rule(e, inf, ctb.RULE_PRIOR), rationale="rule(prior) on inferred cause")
                else: r = resp[(e.id, c)]
                m = ctb.score(e, r["delta"]); m.update(pe.run(e, r["delta"]) if pe else {})
                rows.append(dict(banner=banner, seed=seed, cond=c, ep=e.id, base=e.base_id, split=e.split, source=e.source, cause=e.cause,
                                 skill=e.skill, agent=e.agent, attr_cause=r["cause"], attr_correct=(None if r["cause"] is None else int(r["cause"] == e.cause)),
                                 parse_fail=int(bool(r.get("parse_fail"))), sup_calls=int(c in ctb.LLM_CONDITIONS),
                                 prompt_tokens=r.get("pt", 0), completion_tokens=r.get("ct", 0), latency_s=r.get("lat", 0.0),
                                 **{f"dT_{s}": r["delta"][s] for s in ctb.SKILLS}, **m))
                trans.append(dict(seed=seed, cond=c, ep=e.id, cause=e.cause, rationale=r.get("rationale"), raw=r.get("raw"), delta=r["delta"], attr=r["cause"], self_report_cause=e.self_report_cause))
        print(f"seed {seed} done")
    def dump(name, rs):
        if not rs: return
        keys = list(dict.fromkeys(k for r in rs for k in r)); 
        with open(f"{a.out}/{name}", "w", newline="") as f: w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rs)
    dump("results.csv", rows); dump("provenance.csv", prov_rows)
    with open(f"{a.out}/transcripts.jsonl", "w") as f:
        for t in trans: f.write(json.dumps(t) + "\n")
    json.dump(dict(banner=banner, design=ctb.DESIGN, profiles_source=prof["source"], model=a.model, usage=usage, args=vars(a)), open(f"{a.out}/meta.json", "w"), indent=1, default=str)
    json.dump(prof, open(f"{a.out}/profiles_used.json", "w"), indent=1); print("wrote", a.out)


if __name__ == "__main__":
    main()
