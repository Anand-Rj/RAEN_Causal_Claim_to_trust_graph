# CausalTrustBench: full implementation of "Causal Claim-to-Trust Graph" (as written in the manuscript)

> Anonymized for review. Run every command from this folder. The API key is read from `OPENROUTER_API_KEY` and is never stored.

**No result in this package is a manuscript result.** `out_sim/` was made with SIMULATED supervisors (assumed behaviour; the
ranking there is true by construction) and only validates the pipeline. `selftest.py` uses a MOCK LLM. Real results come from
`run_all.sh` / the runbook below, run where OpenRouter and Hugging Face are reachable. The build sandbox could not reach either.

## Runbook (your machine; 16 GB RAM is plenty, everything is API-bound)
```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=sk-or-...            # in your shell only; never paste/commit it
python selftest.py                              # offline plumbing test (mock LLM), should print ALL SELF-TESTS PASSED
python check_data.py --ping                     # 1. all 4 dataset families load + key works. Fix any FAIL first
# 2. smoke test (a few cents): catches prompt/format bugs before the full run
python calibrate.py --n-cal 4 --n-probe 4 --hotpot --fever --out calib_smoke
python run_experiment.py --backend openrouter --profiles calib_smoke/profiles.json --probe-answers calib_smoke/probe_answers.json \
   --n-gsm 4 --n-tool 4 --n-hotpot 4 --n-fever 4 --seeds 1 --live-transcripts --provenance --out out_smoke && python analyze.py out_smoke --split all
python run_experiment.py --dry-run --n-gsm 50 --n-tool 50 --n-hotpot 50 --n-fever 50 --seeds 3   # prints call counts
./run_all.sh                                    # 3. FULL experiment: 3 model families + heterogeneous team + mixed-effects
```
Calls are cached (`cache_*.jsonl`), so a crashed run resumes for free. Cost is roughly (#calls x ~700 tokens); check `--dry-run`, then OpenRouter pricing.

## Manuscript -> code map
| Manuscript item | Where |
|---|---|
| Datasets: FEVER, HotpotQA, GSM8K (50 each), AgentBench-style tool tasks (50) -> 200 base, 800 episodes | `ctb.load_*`, `gen_tool_tasks` (tool family is a synthetic AgentBench-style generator) |
| 4 persistent specialists, same base LLM, different prompts + tool permissions | `agents.py` (`PERSONAS`, `TOOL_PERMS`); heterogeneous team: `calibrate.py --hetero-models` |
| 4 causal variants, same wrong recommendation + rejection; tool fault injection; withheld-then-restored context | `ctb.build_episodes`, `ctb.apply_tool_fault`, `transcripts.py` |
| Phase A reliability calibration on held-out tasks (measured) | `calibrate.py` -> `profiles.json` (R_pre with Wilson CIs) |
| Ground-truth trust target: (a) controlled weak profile + (b) empirical estimate over probes | `agents.CORRUPT` (controlled), `calibrate.py` measures R_post on a disjoint probe pool; dT* = paired difference |
| Phase B-D: failure, attribution, trust update | `run_experiment.py`, `ctb.build_prompt`, 10 LLM conditions + 3 rule conditions |
| Conditions 1-6 + ablations (parent links, tool state, cause labels, persistence/resolution, update rule) | `none, raw, outcome, skill, graph, graph_rule` + `graph_no_parent, graph_no_toolstate, graph_masked (=no cause labels), graph_no_persist`, `graph` vs `graph_rule` (rule) ; extra control `raw_cot` |
| Future-probe set: 2 same, 1 nearby, 1 unrelated | `Episode.probes` |
| Phase E: reuse, redundant verification, avoidance/replacement, downstream success | `ctb.score` (verify/redundant/reroute rates), `phase_e.py` (empirical success from measured subagent correctness) |
| TCE, Delegation Regret, TUSE, over/under-distrust | `ctb.score` |
| Failure-cause attribution acc., provenance attribution acc., lineage reconstruction acc., FCSR | `analyze.py` Table 5; `provenance.py` Table 7; FCSR in Table 1b |
| Utility/cost: success, redundant verification, #calls, tokens, latency, replacement | Tables 1b and 8 (token/latency logged in `LLMClient`) |
| Paired design, bootstrap CIs, mixed-effects (fixed: condition, cause, interactions; random: task, model family), McNemar, multiple seeds | `analyze.py` (cluster bootstrap, Wilcoxon+Holm), `mixed_effects.py` |
| Robustness: >=2 more model families + heterogeneous team | `run_all.sh` |
| 60/20/20 train/dev/test split at the base-task level (causal variants never cross splits) | `build_episodes(train_frac=.6, dev_frac=.2)`; the explicit rule is fit on train (`graph_rule_fit`), prompts/design are tuned on dev only, `analyze.py` reports the test split (default) |
| Reproducibility: task IDs, templates, profiles, prompts, schemas, code, seeds | everything under this folder + `episodes.jsonl`, `profiles_used.json`, `meta.json` |
| PI request: case studies of subagent/lead-agent interaction and misalignment errors | `analyze.py` -> `case_studies_<split>.md` + Table 6 taxonomy (includes subagent self-reports that mislead the lead agent) |

## Implementation notes you should know (so the paper and code agree)
1. The target wrong recommendation is harness-induced (manuscript: "force/induce"): the live subagent writes its own claim chain, the final claim text is forced identical across the four variants.
2. The persistent weakness uses the manuscript's option (a) (controlled profile via seeded answer corruption) and option (b) (empirical estimate), both implemented.
3. Delegation actions are chosen by maximizing expected utility under the supervisor's belief R_pre + dT (fixed rule, so calibration is what differs between conditions). Execution of the probes uses measured subagent correctness (`emp_*`) plus an analytic regret against the true R_post.
4. FCSR = expected share of false claims the subagent would produce on the 4 future probes that survive into the final answer (delegate: all survive; verify: 1-q survive; reroute: none).
5. `graph_rule_fit` fits magnitudes on the train split (an upper bound); `graph_rule` uses pre-specified magnitudes.
6. HotpotQA/FEVER loaders and every live-LLM path were exercised only with the mock LLM. `check_data.py` and the smoke test exist to surface any field-name/format issue quickly.
