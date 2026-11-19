#!/usr/bin/env python3
"""Phase A: calibrate each subagent's skill-conditional reliability by running the LIVE subagents on held-out tasks,
then measure post-failure reliability of the controlled persistent-weak profile on a disjoint probe pool (option (b)).
Writes profiles.json (same structure as ctb.designed_profiles) and probe_answers.json (used for empirical Phase E).
  python calibrate.py --model openai/gpt-4o-mini --n-cal 40 --n-probe 40 --out calib_gpt4omini
"""
import argparse, json, math, os
from concurrent.futures import ThreadPoolExecutor
import ctb, agents, llm
from llm import LLMClient


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def pools(a, offset_cal=600, offset_probe=900):
    P = {"cal": {}, "probe": {}}
    for name, off, sd in (("cal", offset_cal, 1), ("probe", offset_probe, 2)):
        P[name]["quant"] = ctb.load_gsm8k(a.gsm_path, a.n_cal if name == "cal" else a.n_probe, offset=off)
        P[name]["tool"] = ctb.gen_tool_tasks(a.n_cal if name == "cal" else a.n_probe, seed=sd)
        P[name]["multihop"] = ctb.load_hotpot(a.n_cal if name == "cal" else a.n_probe, offset=500 if name == "cal" else 700) if a.hotpot else []
        P[name]["fact"] = ctb.load_fever(a.n_cal if name == "cal" else a.n_probe, offset=500 if name == "cal" else 700) if a.fever else []
        for k, ts in P[name].items():
            for t in ts: t["id"] = f"{t['source']}-{t['base_idx']}-{name}"; llm.MOCK_TRUTH[t["id"]] = dict(answer=t["answer"], wrong=ctb.make_wrong(t, __import__('random').Random(1)))
    return P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai/gpt-4o-mini"); ap.add_argument("--gsm-path", default="gsm8k_test.jsonl")
    ap.add_argument("--n-cal", type=int, default=40); ap.add_argument("--n-probe", type=int, default=40)
    ap.add_argument("--hotpot", action="store_true"); ap.add_argument("--fever", action="store_true")
    ap.add_argument("--oos-drop", type=float, default=0.15, help="routing penalty in the out_of_specialty oracle (manuscript scoped penalty)")
    ap.add_argument("--workers", type=int, default=8); ap.add_argument("--mock", action="store_true"); ap.add_argument("--out", default="calib")
    ap.add_argument("--hetero-models", default="", help="comma list agent=model e.g. quant_agent=openai/gpt-4o,tool_agent=meta-llama/llama-3.1-8b-instruct")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    P = pools(a)
    models = {ag: a.model for ag in ctb.AGENT_OF.values()}
    for kv in filter(None, a.hetero_models.split(",")): ag, m = kv.split("="); models[ag] = m
    clients = {m: LLMClient(m, 0.0, 0, f"{a.out}/cache_{m.replace('/', '_')}.jsonl", mock=a.mock) for m in set(models.values())}
    jobs = [(ag, k, name, t) for ag in ctb.AGENT_OF.values() for k in ctb.SKILLS for name in ("cal", "probe") for t in P[name][k]]
    print(f"{len(jobs)} live subagent calls")
    def run(j):
        ag, k, name, t = j; ok, ans, r = agents.run_solve(clients[models[ag]], ag, t); return ok
    with ThreadPoolExecutor(a.workers if not a.mock else 1) as ex: res = list(ex.map(run, jobs))
    base = {}
    for (ag, k, name, t), ok in zip(jobs, res): base.setdefault((ag, k, name), []).append((t["id"], bool(ok)))
    pre, pre_ci, probe_norm, probe_weak, probe_answers = {}, {}, {}, {}, {}
    for ag in ctb.AGENT_OF.values():
        pre[ag], pre_ci[ag] = {}, {}; probe_answers[ag] = {}
        for k in ctb.SKILLS:
            cal = base[(ag, k, "cal")]; kk = [ok and not agents.draw_corrupt(ag, tid, k, None, "cal") for tid, ok in cal]
            pre[ag][k] = sum(kk) / max(1, len(kk)); pre_ci[ag][k] = [round(x, 3) for x in wilson(sum(kk), len(kk))]
            pr = base[(ag, k, "probe")]; probe_answers[ag][k] = [dict(id=tid, base_ok=ok) for tid, ok in pr]
            probe_norm[(ag, k)] = [ok and not agents.draw_corrupt(ag, tid, k, None, "probe") for tid, ok in pr]
    for k in ctb.SKILLS:  # persistent-weak profile for the specialist on affected skill k
        ag = ctb.AGENT_OF[k]; probe_weak[(ag, k)] = {}
        for j in ctb.SKILLS:
            pr = base[(ag, j, "probe")]
            probe_weak[(ag, k)][j] = [ok and not agents.draw_corrupt(ag, tid, j, k, "probe") for tid, ok in pr]
    mean = lambda v: sum(v) / max(1, len(v))
    post = {c: {ag: {k: dict(pre[ag]) for k in ctb.SKILLS} for ag in ctb.AGENT_OF.values()} for c in ctb.CAUSES}
    for k in ctb.SKILLS:
        ag = ctb.AGENT_OF[k]
        for j in ctb.SKILLS:
            delta = mean(probe_weak[(ag, k)][j]) - mean(probe_norm[(ag, j)])   # paired on the same probe tasks
            post["persistent_reasoning"][ag][k][j] = max(0.0, min(1.0, pre[ag][j] + delta))
    for ag in ctb.AGENT_OF.values():
        for k in ctb.SKILLS:
            if ag != ctb.AGENT_OF[k]: post["out_of_specialty"][ag][k][k] = max(0.0, pre[ag][k] - a.oos_drop)
    prof = dict(source="measured", model=a.model, models=models, n_cal=a.n_cal, n_probe=a.n_probe, pre=pre, pre_ci95=pre_ci, post=post,
                corruption=agents.CORRUPT, oos_drop=a.oos_drop)
    json.dump(prof, open(f"{a.out}/profiles.json", "w"), indent=1); json.dump(probe_answers, open(f"{a.out}/probe_answers.json", "w"))
    print("\nMeasured R_pre (rows=agent, cols=skill):")
    for ag in pre: print(f"  {ag:15s}", "  ".join(f"{k}={pre[ag][k]:.2f}{pre_ci[ag][k]}" for k in ctb.SKILLS))
    print("\nPersistent-weak profile: measured drop on the affected skill (should be clearly > 0.2):")
    for k in ctb.SKILLS: print(f"  {k}: {pre[ctb.AGENT_OF[k]][k]:.2f} -> {post['persistent_reasoning'][ctb.AGENT_OF[k]][k][k]:.2f}")
    for k in ctb.SKILLS:
        if pre[ctb.AGENT_OF[k]][k] < 0.75: print(f"WARNING: specialist for {k} has R_pre<0.75; the delegation oracle will mostly say 'reroute' (check tasks/prompts)")
    print("\nTokens/latency:", {m: c.stats for m, c in clients.items()}); print("wrote", a.out)


if __name__ == "__main__":
    main()
