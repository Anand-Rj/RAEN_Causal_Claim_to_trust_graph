"""Live transcript generation: each failure episode's subagent writes its own 4-claim analysis (harness-induced final answer)."""
import json
from concurrent.futures import ThreadPoolExecutor
import ctb, agents
from llm import extract_json


def build_transcripts(client, eps, workers=8, mock=False):
    def one(e):
        s, u = agents.induce_prompt(e.agent, e.id, e.question, e.context_given, ctb.TOOL_LOG[e.tool_state], e.wrong)
        r = client.chat(s, u)
        try:
            cl = extract_json(r["text"])["claims"]; assert len(cl) >= 4
            ev_ids = {f"e{i}" for i in range(len(e.context_given))}
            new = []
            for i, c in enumerate(e.chain):
                txt = str(cl[i].get("text", c["text"])).strip()
                evs = [x for x in cl[i].get("evidence", []) if x in ev_ids]
                new.append(dict(id=c["id"], parent=c["parent"], text=txt, evidence=evs))
            new[-1]["text"] = f"Final answer: {e.wrong}."          # forced, identical across the 4 causal variants
            new[0]["evidence"] = sorted(ev_ids, key=lambda x: int(x[1:]))   # c1 = everything retrieved
            e.chain = new; e.reasoning = new[2]["text"]
            e.gt["sources"] = sorted({x for c in new[1:] for x in c["evidence"]} or ev_ids, key=lambda x: int(x[1:]))
            return True
        except Exception:
            return False
    with ThreadPoolExecutor(1 if mock else workers) as ex: ok = list(ex.map(one, eps))
    return sum(ok), len(ok)
