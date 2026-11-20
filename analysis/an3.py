import os
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
pd.set_option("display.width",250)
D={k:load(k) for k in RUNS}
fam=["gpt","haiku","llama"]
CO=["none","raw","raw_cot","outcome","skill","graph_masked","graph","graph_rule_inferred","graph_rule"]
M=["tce","tuse","regret","over_distrust","under_distrust","fcsr"]
def rm(df,c,m,excl):
    d=df[df.cond==c]
    if excl: d=d[d.parse_fail==0]
    return d.groupby("base")[m].mean().mean()
print("POOLED 3 fam: imputed -> excluded")
for c in CO:
    print(f"{c:20s}", "  ".join(f"{m}: {np.mean([rm(D[k][0],c,m,False) for k in fam]):.3f}->{np.mean([rm(D[k][0],c,m,True) for k in fam]):.3f}" for m in M))
print("HAIKU only")
for c in CO:
    print(f"{c:20s}", "  ".join(f"{m}: {rm(D['haiku'][0],c,m,False):.3f}->{rm(D['haiku'][0],c,m,True):.3f}" for m in M))
