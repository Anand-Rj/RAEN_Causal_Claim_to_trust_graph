"""Claim-level ClaimGraph metrics: (b) provenance attribution accuracy, (c) claim lineage reconstruction accuracy."""
import json
import ctb
from llm import extract_json

SYS = ('[[ROLE:provenance]] You reconstruct claim provenance from an agent transcript. Reply ONLY with JSON: '
       '{"origin_agent": "<agent name>", "source_evidence": ["e0", ...] (evidence ids the final answer ultimately depends on), '
       '"tool_dependency": "retrieve:<ok|failed|empty|stale>" or null, "claims": [{"id":"c1","parent":null},{"id":"c2","parent":"c1"}, ...]}')


def extract(client, ep):
    r = client.chat(SYS, "TRANSCRIPT\n" + ctb.transcript_text(ep))
    try: o = extract_json(r["text"])
    except Exception: return dict(parse_fail=1, r=r)
    return dict(parse_fail=0, o=o, r=r)


def score(ep, res):
    if res["parse_fail"]: return dict(prov_origin=0, prov_source_f1=0.0, prov_tool=0, prov_joint=0, lineage_acc=0.0, lineage_exact=0, prov_parse_fail=1)
    o = res["o"]; gt = ep.gt
    origin = int(o.get("origin_agent") == gt["origin_agent"])
    ps, gs = set(o.get("source_evidence") or []), set(gt["sources"])
    tp = len(ps & gs); f1 = 1.0 if not ps and not gs else (0.0 if not tp else 2 * tp / (len(ps) + len(gs)))
    tool = int((o.get("tool_dependency") or "") == f"retrieve:{ep.tool_state}")
    pred = {c.get("id"): c.get("parent") for c in o.get("claims", []) if isinstance(c, dict)}
    gte = {a: b for a, b in gt["edges"]}
    corr = sum(1 for k, v in gte.items() if pred.get(k, "__x") == v)
    return dict(prov_origin=origin, prov_source_f1=f1, prov_tool=tool, prov_joint=int(origin and f1 == 1.0 and tool),
                lineage_acc=corr / len(gte), lineage_exact=int(corr == len(gte)), prov_parse_fail=0)
