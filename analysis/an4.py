import os
import sys,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
D={k:load(k)[0] for k in RUNS}; fam=["gpt","haiku","llama"]
A=pd.concat([D[k] for k in fam]); rng=np.random.default_rng(1)
C4=["missing_context","tool_failure","out_of_specialty","persistent_reasoning"]
def bm(df,col): return df.groupby("base")[col].mean()
def bci(v,B=5000):
    v=np.asarray(v); bs=[v[rng.integers(0,len(v),len(v))].mean() for _ in range(B)]; return v.mean(),np.percentile(bs,2.5),np.percentile(bs,97.5)
out={}
# fig signed CIs
conds=["outcome","skill","graph","graph_rule_inferred","graph_rule"]
out["signed"]={c:{x:bci(bm(A[(A.cond==c)&(A.cause==x)],"signed_aff")) for x in C4} for c in conds}
def diff(a,b,col,causes=None):
    sa=A[A.cond==a]; sb=A[A.cond==b]
    if causes: sa=sa[sa.cause.isin(causes)]; sb=sb[sb.cause.isin(causes)]
    d=(bm(sa,col)-bm(sb,col)).dropna(); m,lo,hi=bci(d.values)
    return dict(mean=m,lo=lo,hi=hi,up=int((d<0).sum()),down=int((d>0).sum()))  # negative diff favours first
for name,causes in [("all",None),("pers",["persistent_reasoning"]),("oos",["out_of_specialty"]),("trans",["missing_context","tool_failure"])]:
    out["d_"+name]={f"{a}-{b}":diff(a,b,"tce",causes) for a,b in [("graph","outcome"),("graph","skill"),("graph_rule_inferred","outcome"),("graph_rule_inferred","skill"),("graph_rule","outcome"),("graph_rule_fit","outcome"),("graph_rule","skill")]}
for k,v in out["d_all"].items(): print("ALL",k,{a:round(b,3) for a,b in v.items()})
for k,v in out["d_pers"].items(): print("PERS",k,{a:round(b,3) for a,b in v.items()})
for k,v in out["d_trans"].items(): print("TRANS",k,{a:round(b,3) for a,b in v.items()})
for k,v in out["d_oos"].items(): print("OOS",k,{a:round(b,3) for a,b in v.items()})
print({c:{x:[round(t,3) for t in v] for x,v in d.items()} for c,d in out["signed"].items()})
json.dump(out,open(OUT+"/an4.json","w"),default=float)
# tuse/regret contrasts all causes
for m in ["regret","under_distrust","over_distrust","tuse"]:
    print(m,{f"{a}-{b}":{x:round(y,3) for x,y in diff(a,b,m).items()} for a,b in [("graph_rule_inferred","skill"),("graph_rule_inferred","outcome")]})
