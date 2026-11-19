#!/usr/bin/env python3
"""Offline end-to-end self-test with a MOCK LLM (no network, no cost). Verifies plumbing only; produces NO results."""
import os, subprocess, sys
OUT = "out_selftest"; os.makedirs(OUT, exist_ok=True)
run = lambda *a: subprocess.run([sys.executable, "selftest_runner.py", *a], capture_output=True, text=True)

import fakes; fakes.install(); import ctb
bases = ctb.load_gsm8k("gsm8k_test.jsonl", 4) + ctb.gen_tool_tasks(4) + ctb.load_hotpot(4) + ctb.load_fever(4)
eps = ctb.build_episodes(bases)
for e in eps:
    m = ctb.score(e, e.dT_star); assert m["tce"] == 0 and m["regret"] < 1e-9 and m["tuse"] == 0, e.id
for b in {e.base_id for e in eps}:
    v = [e for e in eps if e.base_id == b]; assert len({e.wrong for e in v}) == 1 and len({e.chain[-1]["text"] for e in v}) == 1
print("1) oracle + matched-variant checks OK:", len(eps), "episodes")

r = run("calibrate.py", "--mock", "--n-cal", "8", "--n-probe", "8", "--hotpot", "--fever", "--out", f"{OUT}/calib"); print(r.stdout[-900:], r.stderr[-1200:]); assert r.returncode == 0
print("2) calibrate OK")
r = run("run_experiment.py", "--backend", "mock", "--n-gsm", "6", "--n-tool", "6", "--n-hotpot", "6", "--n-fever", "6", "--seeds", "2",
        "--profiles", f"{OUT}/calib/profiles.json", "--probe-answers", f"{OUT}/calib/probe_answers.json", "--live-transcripts", "--provenance", "--out", f"{OUT}/run")
print(r.stdout[-500:], r.stderr[-1500:]); assert r.returncode == 0
import pandas as pd
df = pd.read_csv(f"{OUT}/run/results.csv"); assert {"emp_success", "emp_regret", "fcsr", "redundant_verify"} <= set(df.columns); assert os.path.exists(f"{OUT}/run/provenance.csv")
print("3) run OK; rows:", len(df))
r = run("analyze.py", f"{OUT}/run", "--split", "all"); print(r.stderr[-1500:]); assert r.returncode == 0
print("4) analyze OK\nALL SELF-TESTS PASSED (plumbing only; mock LLM; no results)")
