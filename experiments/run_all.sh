#!/usr/bin/env bash
# Full manuscript experiment for several model families + heterogeneous team. Edit MODELS to valid OpenRouter slugs (openrouter.ai/models).
set -euo pipefail
: "${OPENROUTER_API_KEY:?export OPENROUTER_API_KEY first}"
MODELS=("openai/gpt-4o-mini" "anthropic/claude-haiku-5.5" "meta-llama/llama-3.3-70b-instruct")   # exact OpenRouter slugs used in the paper (primary = first)
HETERO="quant_agent=openai/gpt-4o-mini,fact_agent=anthropic/claude-haiku-5.5,multihop_agent=meta-llama/llama-3.3-70b-instruct,tool_agent=openai/gpt-4o-mini"
COMMON="--n-gsm 50 --n-tool 50 --n-hotpot 50 --n-fever 50 --seeds 3 --temperature 0.7 --live-transcripts --provenance"
python check_data.py --ping --model "${MODELS[0]}"
DIRS=()
for M in "${MODELS[@]}"; do
  T=$(echo "$M" | tr '/' '_')
  python calibrate.py --model "$M" --n-cal 40 --n-probe 40 --hotpot --fever --out "calib_$T"
  python run_experiment.py --backend openrouter --model "$M" --profiles "calib_$T/profiles.json" --probe-answers "calib_$T/probe_answers.json" $COMMON --out "out_$T"
  python analyze.py "out_$T" --split test; DIRS+=("out_$T")
done
# heterogeneous-agent configuration (each subagent on a different base LLM), supervisor = primary model
python calibrate.py --model "${MODELS[0]}" --hetero-models "$HETERO" --n-cal 40 --n-probe 40 --hotpot --fever --out calib_hetero
python run_experiment.py --backend openrouter --model "${MODELS[0]}" --profiles calib_hetero/profiles.json --probe-answers calib_hetero/probe_answers.json $COMMON --out out_hetero
python analyze.py out_hetero --split test
python mixed_effects.py "${DIRS[@]}" out_hetero --split test --out mixed_effects_report.md
