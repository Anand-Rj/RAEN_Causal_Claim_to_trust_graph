# Reproducing the paper's tables

No API calls are needed to recompute the tables from the released per-episode data.

```
pip install pandas numpy
cd analysis
CTB_DATA=../data CTB_OUT=../analysis_out python reproduce_paper_tables.py
```

This regenerates, from `data/<run>/results.csv.gz` and `episodes.jsonl.gz`: the measured-target table (`tab_meas.tex`), the
unparseable-reply and exclusion tables (`tab_parse.tex`, `tab_excl.tex`), the attribution and taxonomy tables
(`tab_attr.tex`, `tab_tax.tex`, `tab_recon.tex`), the four-run pooled table (`tab_main4.tex`), the 729-setting sensitivity
sweep (`sweep_out.json`, `tab_sens.tex`), and the bootstrap intervals used for the signed-error figure (`an4.json`).
The per-condition main tables are written by `experiments/analyze.py` into `data/<run>/results_test.md`.

Contents of `data/<run>/` (runs: `openai_gpt-4o-mini`, `anthropic_claude-haiku-5.5`, `meta-llama_llama-3.3-70b-instruct`, `hetero`):
`results.csv.gz` (all conditions, seeds and splits), `episodes.jsonl.gz`, `provenance.csv`, `meta.json`, `profiles_used.json`,
`rule_fit.json`, `results_test.md`, `case_studies_test.md`, `transcripts.jsonl.gz` (logged transcripts),
`caches.tar.gz` (response caches: re-running `experiments/run_experiment.py` with the same arguments replays them without API calls).
`prompts/supervisor_prompts.md` shows the exact supervisor prompt for each memory condition and cause;
`prompts/render_prompts.py` regenerates it. Running new experiments needs an OpenRouter key in `OPENROUTER_API_KEY`
(`experiments/run_all.sh`; slugs are the exact ones used in the paper, run on 17 November 2026).
