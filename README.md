<div align="center">

# Causal Claim-to-Trust Graph / CausalTrustBench

**Calibrating long-horizon trust in LLM subagents from claim-level failure provenance.**

![python](https://img.shields.io/badge/python-3.12-3776AB)
![license](https://img.shields.io/badge/license-Apache--2.0-green)


</div>

When a supervisor LLM rejects a subagent's recommendation, the same wrong answer can come from missing
context, a failed tool, a task routed to the wrong specialist, or a genuine reasoning weakness. Each cause
implies a different future. **CausalTrustBench** holds the subagent, task, wrong recommendation and rejection
fixed and varies only the cause (4 matched variants of each of 200 base tasks, 800 episodes), then scores how
well a supervisor's trust update matches the subagent's measured post-failure reliability and how well it
delegates, verifies or reroutes on four future probes.

Paper source (AAAI-27 workshop submission, anonymized): [`docs/paper/`](docs/paper/).

---

## Results (test split: 40 base tasks, 160 episodes, 3 seeds)

Mean over three model families (GPT-4o-mini, Claude Haiku 5.5, Llama-3.3-70B-Instruct). Lower is better
except success. TCE = trust-calibration error, TUSE = trust-update scope error.

| Memory condition | TCE | TUSE | Regret | FCSR | Success |
|---|---|---|---|---|---|
| No memory | 0.064 | 0.025 | 0.068 | 0.159 | 0.825 |
| Raw history | 0.069 | 0.043 | 0.041 | 0.111 | 0.836 |
| Outcome-only | 0.068 | 0.032 | 0.050 | 0.126 | 0.836 |
| Skill-conditioned | 0.048 | 0.014 | 0.039 | 0.121 | 0.837 |
| ClaimGraph | 0.054 | 0.018 | 0.029 | 0.104 | 0.839 |
| ClaimGraph + rule, LLM-inferred cause | 0.043 | 0.019 | 0.030 | 0.115 | 0.840 |
| ClaimGraph + rule, true cause (upper bound) | 0.024 | 0.003 | 0.005 | 0.115 | 0.845 |

Outcome-only memory over-penalizes resolved transient failures and under-reacts to persistent weakness.
The graph lowers regret, but it does **not** uniformly beat skill-conditioned memory, and a rule driven by
LLM-inferred causes recovers only part of the gain because supervisors rarely recognize missing context.
Per-run tables, paired contrasts and case studies are in [`experiments/results/`](experiments/results/).

## Repository layout

```text
experiments/               code, calibration profiles and result summaries
  ctb.py                   benchmark construction, memory conditions, update rule, metrics
  agents.py                specialist agents and controlled corruption profiles
  calibrate.py             measures pre-failure reliability and post-failure probe reliability
  run_experiment.py        full run (--backend openrouter), resumable via a disk cache
  analyze.py               tables, figures, case studies on the test split
  mixed_effects.py         mixed-effects model across model families
  provenance.py, transcripts.py, phase_e.py   claim extraction, transcripts, downstream execution
  selftest.py              offline plumbing test with a mock LLM
  results/<run>/           results_test.md, case_studies_test.md, meta.json, figures
  calibration/<run>/       measured reliability profiles
docs/paper/                anonymized paper source (AAAI style), figures, references
```

See [`experiments/README.md`](experiments/README.md) for the run order. Raw per-episode CSVs and response
caches are large and are not committed; the committed summaries regenerate the paper tables via
`analyze.py` when the CSVs are present.

## Notes and limitations

- Persistent weakness is induced by seeded answer corruption, and the rule table is hand-set, so the
  true-cause row is an upper bound, not a deployable system.
- The test split is 40 base tasks per run; tool tasks are synthetic; one temperature (0.7) and one API provider.
- Several design choices were made after inspecting an initial run; they are listed in the paper's limitations.
- Models are served via OpenRouter. **Never commit API keys** (`.env` is git-ignored).

## License

[Apache License 2.0](LICENSE).
