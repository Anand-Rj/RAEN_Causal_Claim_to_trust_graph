"""Render the exact supervisor prompt for every memory condition on one example episode per cause.
Run from the experiments/ directory:  python ../prompts/render_prompts.py <episodes.jsonl.gz> > supervisor_prompts.md"""
import sys, json, gzip, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments"))
import ctb
from dataclasses import fields
names = {f.name for f in fields(ctb.Episode)}
op = gzip.open if sys.argv[1].endswith(".gz") else open
eps = [ctb.Episode(**{k: v for k, v in json.loads(l).items() if k in names}) for l in op(sys.argv[1], "rt")]
conds = ["none", "raw", "raw_cot", "outcome", "skill", "graph_masked", "graph", "graph_no_parent", "graph_no_toolstate", "graph_no_persist"]
print("# Supervisor prompts (one example episode per cause)\n")
for cause in ["missing_context", "tool_failure", "out_of_specialty", "persistent_reasoning"]:
    ep = next(e for e in eps if e.cause == cause)
    print(f"## Cause: {cause} (episode {ep.id})\n")
    for c in conds:
        sysm, user = ctb.build_prompt(ep, c)
        print(f"### Condition: {c}\n\nSYSTEM:\n```\n{sysm}\n```\nUSER:\n```\n{user}\n```\n")
