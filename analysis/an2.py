import os
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
pd.set_option("display.width",250)
D={k:load(k)[0] for k in RUNS}
fam=["gpt","haiku","llama"]
A=pd.concat([D[k] for k in fam])
rng=np.random.default_rng(0)
def ci(df,col):
    g=df.groupby("base")[col].mean().values  # mean over runs,seeds within base
    bs=[g[rng.integers(0,len(g),len(g))].mean() for _ in range(4000)]
    return g.mean(),np.percentile(bs,2.5),np.percentile(bs,97.5)
conds=["none","raw","outcome","skill","graph_masked","graph","graph_rule_inferred","graph_rule_fit","graph_rule"]
for name,causes in [("PERSISTENT (measured target)",["persistent_reasoning"]),("MC+TF (design 0)",["missing_context","tool_failure"]),("OOS (design -0.15)",["out_of_specialty"])]:
    print("==",name)
    for c in conds:
        s=A[(A.cond==c)&(A.cause.isin(causes))]
        print(f"{c:22s}", "  ".join(f"{m}={ci(s,m)[0]:.3f}[{ci(s,m)[1]:.3f},{ci(s,m)[2]:.3f}]" for m in ["tce","tce_aff","regret"]))
# per-run persistent TCE
print("per-run persistent TCE")
for k in RUNS:
    d=D[k]; print(k,{c:round(d[(d.cond==c)&(d.cause=="persistent_reasoning")].groupby("base").tce.mean().mean(),3) for c in ["outcome","skill","graph","graph_rule_inferred","graph_rule_fit","graph_rule"]})
