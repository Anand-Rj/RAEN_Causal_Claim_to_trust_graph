"""Regenerate the paper's tables from the released per-episode data (no API calls).
Usage: CTB_DATA=../data CTB_OUT=../analysis_out python reproduce_paper_tables.py
Outputs: LaTeX table fragments (tab_*.tex), an*.json, sweep_out.json in CTB_OUT, plus printed summaries."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ); env.setdefault("CTB_DATA", os.path.join(here, "..", "data")); env.setdefault("CTB_OUT", os.path.join(here, "..", "analysis_out"))
for step in ["an1.py", "an2.py", "an3.py", "an4.py", "sweep.py", "sweep_run.py", "mk_new.py"]:
    print("== running", step, flush=True)
    subprocess.run([sys.executable, os.path.join(here, step)], check=True, env=env, cwd=here)
