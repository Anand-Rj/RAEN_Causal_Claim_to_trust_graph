#!/usr/bin/env python3
"""Analysis: tables with cluster-bootstrap CIs, paired tests vs baselines (Holm), taxonomy, case studies, figures.
   python analyze.py out_dir            (analyzes the TEST split by default; --split dev|test|all)"""
import argparse, json, math, os, random
from collections import Counter, defaultdict
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
import ctb

ORDER = ctb.CONDITIONS
METRICS = ["tce", "tce_aff", "tuse", "regret", "over_distrust", "under_distrust"]
METRICS2 = ["verify_rate", "reroute_rate", "redundant_verify", "fcsr", "utility", "emp_success", "emp_regret"]
B = 2000


def boot_ci(df, col, rng):
    """Cluster bootstrap over base tasks (and seeds averaged within task)."""
    g = df.groupby("base")[col].mean().dropna()
    v = g.values
    if len(v) == 0: return (float("nan"),) * 3
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(B)]
    return v.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def holm(ps):
    idx = sorted(range(len(ps)), key=lambda i: ps[i]); out = [0] * len(ps); mx = 0
    for r, i in enumerate(idx):
        mx = max(mx, min(1, (len(ps) - r) * ps[i])); out[i] = mx
    return out


def fmt(m, lo, hi): return "n/a" if math.isnan(m) else f"{m:.3f} [{lo:.3f}, {hi:.3f}]"


def classify(row, ep, tau=0.10):
    """Multi-label misalignment taxonomy between lead agent (supervisor) and subagent state."""
    labs = []; k = ep["skill"]; ds = ep["dT_star"]
    dT = {s: row[f"dT_{s}"] for s in ctb.SKILLS}
    if ep["cause"] in ("missing_context", "tool_failure") and dT[k] < -tau:
        labs.append("blamed_agent_for_context" if ep["cause"] == "missing_context" else "blamed_agent_for_tool_fault")
    if ep["cause"] == "out_of_specialty":
        spec = ctb.SPEC_OF[ep["agent"]]
        if dT[spec] < -tau: labs.append("routing_error_penalized_true_specialty")
    if ep["cause"] == "persistent_reasoning" and dT[k] > ds[k] + tau: labs.append("under_reaction_to_persistent_weakness")
    un = [s for s in ctb.SKILLS if abs(ds[s]) < 1e-9]
    if un and np.mean([abs(dT[s]) for s in un]) > tau: labs.append("scope_spillover_to_unaffected_skills")
    if row["attr_cause"] is not None and row["attr_cause"] != ep["cause"]:
        labs.append("misled_by_subagent_self_report" if (row["cond"] in ("raw", "raw_cot") and row["attr_cause"] == ep["self_report_cause"])
                    else "cause_misattribution")
    if row["parse_fail"]: labs.append("unparseable_supervisor_output")
    return labs or ["calibrated"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--split", default="test"); a = ap.parse_args()
    d = a.out; meta = json.load(open(f"{d}/meta.json")); banner = meta["banner"]
    df = pd.read_csv(f"{d}/results.csv"); eps = {json.loads(l)["id"]: json.loads(l) for l in open(f"{d}/episodes.jsonl")}
    if a.split != "all": df = df[df.split == a.split]
    rng = np.random.default_rng(0); L = []
    L += [f"# CausalTrustBench results ({a.split} split)", f"**{banner}**", "",
          f"{df.base.nunique()} base tasks, {df.ep.nunique()} episodes, {df.seed.nunique()} seed(s). Mean [95% cluster-bootstrap CI over base tasks].", ""]
    # ---- main table
    L += ["## Table 1. Metrics by memory condition (all causes pooled)", "",
          "| condition | " + " | ".join(METRICS) + " |", "|---|" + "---|" * len(METRICS)]
    conds = [c for c in ORDER if c in df.cond.unique()]
    for c in conds:
        sub = df[df.cond == c]; L.append(f"| {c} | " + " | ".join(fmt(*boot_ci(sub, m, rng)) for m in METRICS) + " |")
    m2 = [m for m in METRICS2 if m in df.columns]
    L += ["", "## Table 1b. System utility, oversight cost and False Claim Survival Rate (FCSR, expected; lower is better)", "",
          "| condition | " + " | ".join(m2) + " |", "|---|" + "---|" * len(m2)]
    for c in conds:
        sub = df[df.cond == c]; L.append(f"| {c} | " + " | ".join(fmt(*boot_ci(sub, m, rng)) for m in m2) + " |")
    L += ["", "emp_* columns (if present) execute the probes with real measured subagent correctness; fcsr = expected fraction of the false claims the subagent would produce on the 4 probes that survive into the final answer.", ""]
    abl = [c for c in ("graph_masked", "graph_no_parent", "graph_no_toolstate", "graph_no_persist") if c in conds]
    if "graph" in conds and abl:
        L += ["## Table 1c. Ablations: paired difference (ablation minus full graph; positive = ablation is worse)", "",
              "| ablation | metric | mean diff | 95% CI | p (Wilcoxon) |", "|---|---|---|---|---|"]
        for A_ in abl:
            for m_ in ("tce", "tuse", "regret", "fcsr"):
                pa = df[df.cond == A_].groupby("base")[m_].mean(); pb = df[df.cond == "graph"].groupby("base")[m_].mean(); dd = (pa - pb).dropna()
                if len(dd) == 0: continue
                bs = [dd.values[rng.integers(0, len(dd), len(dd))].mean() for _ in range(B)]
                try: p_ = stats.wilcoxon(dd.values).pvalue if np.any(dd.values != 0) else 1.0
                except ValueError: p_ = 1.0
                L.append(f"| {A_} | {m_} | {dd.mean():+.4f} | [{np.percentile(bs, 2.5):+.4f}, {np.percentile(bs, 97.5):+.4f}] | {p_:.2e} |")
        L += ["", "(graph_no_cause = graph_masked. The explicit update rule ablation = graph vs graph_rule in Table 4.)", ""]
    pp = f"{d}/provenance.csv"
    if os.path.exists(pp):
        pv = pd.read_csv(pp)
        if a.split != "all": pv = pv[pv.split == a.split]
        cols = ["prov_origin", "prov_source_f1", "prov_tool", "prov_joint", "lineage_acc", "lineage_exact", "prov_parse_fail"]
        L += ["## Table 7. ClaimGraph provenance metrics (LLM extractor on the raw transcript)", "",
              "| group | n | " + " | ".join(cols) + " |", "|---|---|" + "---|" * len(cols)]
        L.append("| ALL | %d | " % len(pv) + " | ".join(fmt(*boot_ci(pv, c_, rng)) for c_ in cols) + " |")
        for k_ in ctb.CAUSES:
            sub = pv[pv.cause == k_]; L.append(f"| {k_} | {len(sub)} | " + " | ".join(fmt(*boot_ci(sub, c_, rng)) for c_ in cols) + " |")
        for k_ in sorted(pv.source.unique()):
            sub = pv[pv.source == k_]; L.append(f"| source={k_} | {len(sub)} | " + " | ".join(fmt(*boot_ci(sub, c_, rng)) for c_ in cols) + " |")
        L += ["", "prov_* = (a) origin agent, (b) source-evidence F1, tool dependency incl. tool state, joint = all three exact; lineage_* = claim parent-link reconstruction.", ""]
    cost = df[df.sup_calls == 1] if "sup_calls" in df.columns else df.iloc[0:0]
    if len(cost):
        L += ["## Table 8. Cost and latency per incident (supervisor call; LLM conditions only)", "",
              "| condition | prompt tokens | completion tokens | latency (s) | extra verifier calls / incident | replacements / incident |", "|---|---|---|---|---|---|"]
        for c in conds:
            sub = cost[cost.cond == c]
            if len(sub): L.append(f"| {c} | {sub.prompt_tokens.mean():.0f} | {sub.completion_tokens.mean():.0f} | {sub.latency_s.mean():.2f} | {(sub.verify_rate*4).mean():.2f} | {(sub.reroute_rate*4).mean():.2f} |")
        L += ["", "Rule-based conditions (graph_rule*) need no extra LLM call beyond graph labelling. Token/latency are 0 for sim/mock backends.", ""]
    # ---- by cause
    L += ["", "## Table 2. Signed error on the affected skill (dT - dT*) by cause (negative = over-penalized, positive = under-reaction)", "",
          "| condition | " + " | ".join(ctb.CAUSES) + " |", "|---|" + "---|" * 4]
    for c in conds:
        L.append(f"| {c} | " + " | ".join(fmt(*boot_ci(df[(df.cond == c) & (df.cause == k)], "signed_aff", rng)) for k in ctb.CAUSES) + " |")
    L += ["", "## Table 3. Delegation regret by cause", "", "| condition | " + " | ".join(ctb.CAUSES) + " |", "|---|" + "---|" * 4]
    for c in conds:
        L.append(f"| {c} | " + " | ".join(fmt(*boot_ci(df[(df.cond == c) & (df.cause == k)], "regret", rng)) for k in ctb.CAUSES) + " |")
    # ---- paired tests
    L += ["", "## Table 4. Paired comparisons (per-base-task means; Wilcoxon signed-rank, Holm-corrected within metric)", "",
          "| contrast | metric | mean diff (A-B) | 95% CI | p (raw) | p (Holm) |", "|---|---|---|---|---|---|"]
    contrasts = [(x, y) for x in ("graph", "graph_masked", "graph_rule", "graph_rule_inferred") for y in ("outcome", "skill", "raw", "raw_cot")]
    for m in ("tce", "tuse", "regret"):
        res = []
        for A, Bc in contrasts:
            if A not in conds or Bc not in conds: continue
            pa = df[df.cond == A].groupby("base")[m].mean(); pb = df[df.cond == Bc].groupby("base")[m].mean()
            diff = (pa - pb).dropna(); bs = [diff.values[rng.integers(0, len(diff), len(diff))].mean() for _ in range(B)]
            try: p = stats.wilcoxon(diff.values).pvalue if np.any(diff.values != 0) else 1.0
            except ValueError: p = 1.0
            res.append((A, Bc, diff.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), p))
        ph = holm([r[5] for r in res])
        for r, p2 in zip(res, ph):
            L.append(f"| {r[0]} vs {r[1]} | {m} | {r[2]:+.3f} | [{r[3]:+.3f}, {r[4]:+.3f}] | {r[5]:.2e} | {p2:.2e} |")
    # ---- attribution
    att = df[df.attr_correct.notna()]
    if len(att):
        L += ["", "## Table 5. Failure-cause attribution accuracy", "", "| condition | accuracy | " + " | ".join(ctb.CAUSES) + " |", "|---|---|" + "---|" * 4]
        for c in conds:
            s = att[att.cond == c]
            if len(s): L.append(f"| {c} | {s.attr_correct.mean():.3f} | " + " | ".join(f"{s[s.cause == k].attr_correct.mean():.2f}" for k in ctb.CAUSES) + " |")
    # ---- taxonomy
    tax = defaultdict(Counter); ex = defaultdict(list)
    transcripts = {(t["seed"], t["cond"], t["ep"]): t for t in map(json.loads, open(f"{d}/transcripts.jsonl"))}
    for _, r in df.iterrows():
        labs = classify(r, eps[r.ep])
        for lb in labs: tax[r.cond][lb] += 1; ex[lb].append((r.tce, r))
    labels = sorted({lb for c in tax.values() for lb in c})
    L += ["", "## Table 6. Lead-agent/subagent misalignment taxonomy (count of episodes, multi-label)", "",
          "| condition | n | " + " | ".join(labels) + " |", "|---|---|" + "---|" * len(labels)]
    for c in conds:
        n = (df.cond == c).sum(); L.append(f"| {c} | {n} | " + " | ".join(str(tax[c][lb]) for lb in labels) + " |")
    open(f"{d}/results_{a.split}.md", "w").write("\n".join(L))
    # ---- case studies
    CS = [f"# Case studies ({a.split} split)", f"**{banner}**", "",
          "Selection rule: for each misalignment type, the highest-TCE episode from each of up to 3 distinct conditions (fixed rule, not hand-picked) + 1 random episode (seeded).", ""]
    rs = random.Random(0)
    for lb in labels:
        if lb == "calibrated": continue
        items = sorted(ex[lb], key=lambda x: -x[0]); pick = []; seen = set()
        for it in items:  # highest-TCE episode from each distinct condition (diverse), then 1 random
            if it[1].cond not in seen and it[1].cond not in ("none", "graph_rule", "graph_rule_fit"):
                pick.append(it); seen.add(it[1].cond)
            if len(pick) >= 3: break
        if len(items) > 3: pick.append(rs.choice(items))
        CS += [f"## {lb}  (n={len(items)} episode-condition pairs)", ""]
        for tce, r in pick:
            e = eps[r.ep]; t = transcripts[(int(r.seed), r.cond, r.ep)]
            CS += [f"**Episode** `{e['id']}`  |  condition `{r.cond}`  |  true cause `{e['cause']}`  |  failing agent `{e['agent']}`  |  TCE={tce:.3f}",
                   f"- Task: {e['question']}", f"- Subagent said: *{e['wrong']}* (conf {e['confidence']}); self-report: \"{e['self_report']}\"",
                   f"- Lead agent rejection: correct answer {e['correct']}",
                   f"- Oracle trust change (dT*): {e['dT_star']}",
                   f"- Lead agent trust change: { {s: round(r[f'dT_{s}'], 2) for s in ctb.SKILLS} }  attributed cause: {t['attr']}",
                   f"- Lead agent rationale: {t['rationale']}", f"- Regret: {r.regret:.3f}", ""]
    open(f"{d}/case_studies_{a.split}.md", "w").write("\n".join(CS))
    # ---- figures
    cs = [c for c in ["none", "raw", "raw_cot", "outcome", "skill", "graph_masked", "graph", "graph_rule"] if c in conds]
    fig, ax = plt.subplots(figsize=(9, 4)); w = 0.8 / len(cs)
    for i, c in enumerate(cs):
        mu = [df[(df.cond == c) & (df.cause == k)].apply(lambda r: r[f"dT_{r.skill}"], axis=1).mean() for k in ctb.CAUSES]
        ax.bar([x + i * w for x in range(4)], mu, w, label=c)
    ors = [np.mean([eps[x]["dT_star"][eps[x]["skill"]] for x in df[df.cause == k].ep.unique()]) for k in ctb.CAUSES]
    ax.plot([x + 0.4 - w / 2 for x in range(4)], ors, "k_", ms=40, mew=2, label="oracle dT*")
    ax.set_xticks([x + 0.4 - w / 2 for x in range(4)]); ax.set_xticklabels(ctb.CAUSES, fontsize=8)
    ax.set_ylabel("trust change on affected skill"); ax.set_title(f"Trust change by cause and memory condition\n{banner}", fontsize=9)
    ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1.01, 0.5)); fig.tight_layout(); fig.savefig(f"{d}/fig1_trust_by_cause_{a.split}.png", dpi=200); plt.close(fig)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for j, (m, t) in enumerate([("tuse", "TUSE (spillover to unaffected skills)"), ("regret", "Delegation regret / episode")]):
        v = [boot_ci(df[df.cond == c], m, rng) for c in cs]
        ax[j].bar(range(len(cs)), [x[0] for x in v], yerr=[[x[0] - x[1] for x in v], [x[2] - x[0] for x in v]], capsize=2)
        ax[j].set_xticks(range(len(cs))); ax[j].set_xticklabels(cs, rotation=45, ha="right", fontsize=7); ax[j].set_title(t, fontsize=9)
    fig.suptitle(banner, fontsize=8); fig.tight_layout(); fig.savefig(f"{d}/fig2_tuse_regret_{a.split}.png", dpi=200); plt.close(fig)
    fig, ax = plt.subplots(figsize=(5, 4))
    for c in cs:
        s = df[df.cond == c]; ax.scatter(s.verify_rate.mean() + s.reroute_rate.mean(), s.utility.mean(), label=c)
    ax.set_xlabel("fraction of probes verified or re-routed"); ax.set_ylabel("mean true utility / probe"); ax.legend(fontsize=6)
    ax.set_title(f"Utility vs. oversight cost\n{banner}", fontsize=8); fig.tight_layout(); fig.savefig(f"{d}/fig3_utility_vs_oversight_{a.split}.png", dpi=200); plt.close(fig)
    print("\n".join(L[:30])); print("... see", d)


if __name__ == "__main__":
    main()
