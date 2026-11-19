#!/usr/bin/env python3
"""Run this FIRST on your machine. Verifies the four dataset families load and (optionally) that your OpenRouter key/model works.
  python check_data.py                       # data only
  OPENROUTER_API_KEY=... python check_data.py --ping --model openai/gpt-4o-mini"""
import argparse, os, sys
import ctb
from llm import LLMClient

ap = argparse.ArgumentParser(); ap.add_argument("--ping", action="store_true"); ap.add_argument("--model", default="openai/gpt-4o-mini"); a = ap.parse_args()
ok = True
for name, fn in [("GSM8K (quant)", lambda: ctb.load_gsm8k("gsm8k_test.jsonl", 2)), ("synthetic AgentBench-style tool tasks", lambda: ctb.gen_tool_tasks(2)),
                 ("HotpotQA (multihop)", lambda: ctb.load_hotpot(2)), ("FEVER (fact)", lambda: ctb.load_fever(2))]:
    try:
        t = fn(); assert len(t) >= 1 and t[0]["facts"]; print(f"OK   {name}: {t[0]['question'][:90]!r} | facts={len(t[0]['facts'])} | answer={t[0]['answer']!r}")
    except Exception as e:
        ok = False; print(f"FAIL {name}: {type(e).__name__}: {e}")
if a.ping:
    if not os.environ.get("OPENROUTER_API_KEY"): sys.exit("OPENROUTER_API_KEY not set")
    c = LLMClient(a.model, 0.0, 0, None); r = c.chat("Reply with JSON only.", 'Return {"ok": true}'); print("PING:", r["text"][:80], "| tokens", r["prompt_tokens"], r["completion_tokens"], "| latency", r["latency"])
print("ALL DATA FAMILIES OK" if ok else "Fix the FAIL lines above (paste them to me if stuck) before running the experiment.")
