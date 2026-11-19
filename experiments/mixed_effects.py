#!/usr/bin/env python3
"""Mixed-effects models, McNemar tests, and cross-model robustness.
  python mixed_effects.py out_modelA out_modelB out_modelC --split test
Model: metric ~ C(cond, ref=outcome) * C(cause)  [+ C(affected/unaffected skill) via per-skill rows for TUSE-style analysis]
Random effects: crossed variance components for base task and model family (model family only if >1 run dir)."""
import argparse, json, os, warnings
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import ctb
warnings.filterwarnings("ignore")
KEY = ["outcome", "skill", "raw", "raw_cot", "graph_masked", "graph", "graph_rule"]


def load(dirs, split):
    fr = []
    for d in dirs:
        meta = json.load(open(f"{d}/meta.json")); df = pd.read_csv(f"{d}/results.csv")
        df["model"] = meta.get("model", os.path.basename(d)) if meta["banner"].startswith("LLM") else os.path.basename(d)
        if split != "all": df = df[df.split == split]
        fr.append(df)
    return pd.concat(fr, ignore_index=True)


def fit(df, metric):
    d = df[df.cond.isin(KEY)].groupby(["base", "model", "cond", "cause"], as_index=False)[metric].mean().dropna()
    f = f"{metric} ~ C(cond, Treatment('outcome')) * C(cause)"
    d["g"] = 1
    vc = {"task": "0 + C(base)"}
    if d.model.nunique() > 1: vc["model"] = "0 + C(model)"
    try:
        r = smf.mixedlm(f, d, groups=d["g"], vc_formula=vc, re_formula="0").fit(method="lbfgs", maxiter=300)
        return r, "crossed variance components: task" + (" + model family" if "model" in vc else "")
    except Exception as e:
        r = smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["base"])[0]})
        return r, f"FALLBACK to OLS with task-clustered SEs ({type(e).__name__})"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dirs", nargs="+"); ap.add_argument("--split", default="test"); ap.add_argument("--out", default="mixed_effects_report.md")
    a = ap.parse_args(); df = load(a.dirs, a.split); L = [f"# Mixed-effects, McNemar and robustness ({a.split} split)", f"banners: {sorted(set(json.load(open(d + '/meta.json'))['banner'] for d in a.dirs))}", ""]
    for metric in ("tce", "tuse", "regret"):
        r, note = fit(df, metric)
        L += [f"## Mixed model: {metric}   ({note})", "", "```", r.summary().as_text(), "```", ""]
    L += ["## McNemar (exact): binary 'correct delegation decision on both same-skill probes' (paired by episode x seed x model)", "", "| contrast | b (A right, B wrong) | c (A wrong, B right) | p |", "|---|---|---|---|"]
    for A in ("graph", "graph_masked", "graph_rule"):
        for B in ("outcome", "skill", "raw", "raw_cot"):
            pa = df[df.cond == A].set_index(["model", "seed", "ep"]).correct_decision; pb = df[df.cond == B].set_index(["model", "seed", "ep"]).correct_decision
            j = pd.concat([pa, pb], axis=1, keys=["a", "b"]).dropna(); b_ = int(((j.a == 1) & (j.b == 0)).sum()); c_ = int(((j.a == 0) & (j.b == 1)).sum())
            p = stats.binomtest(b_, b_ + c_, 0.5).pvalue if b_ + c_ > 0 else 1.0
            L.append(f"| {A} vs {B} | {b_} | {c_} | {p:.2e} |")
    L += ["", "## Robustness across model families (per-model means; graph vs baselines)", "", "| model | condition | TCE | TUSE | regret | FCSR |", "|---|---|---|---|---|---|"]
    for m_ in df.model.unique():
        for c in KEY:
            s = df[(df.model == m_) & (df.cond == c)]
            if len(s): L.append(f"| {m_} | {c} | {s.tce.mean():.3f} | {s.tuse.mean():.3f} | {s.regret.mean():.3f} | {s.fcsr.mean():.3f} |")
    L += ["", "Sign-consistency check: for each model, does graph beat outcome AND skill on TCE and regret?", ""]
    for m_ in df.model.unique():
        g = {c: df[(df.model == m_) & (df.cond == c)] for c in ("graph", "outcome", "skill")}
        ok = all(g["graph"][x].mean() < g[b][x].mean() for x in ("tce", "regret") for b in ("outcome", "skill"))
        L.append(f"- {m_}: {'YES' if ok else 'NO'}")
    open(a.out, "w").write("\n".join(L)); print("\n".join(L[:40])); print("wrote", a.out)


if __name__ == "__main__":
    main()
