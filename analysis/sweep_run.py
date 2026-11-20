import os
import sys,pickle,itertools,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sweep import *
B=pickle.load(open(OUT+"/B.pkl","rb"))
fam=["gpt","haiku","llama"]
CO=["outcome","skill","graph","graph_rule_inferred","graph_rule","raw","none","graph_masked"]
G=dict(q=[0.5,0.7,0.9],cv=[0.04,0.08,0.12],cr=[0.02,0.05,0.10],Ralt=[0.80,0.87,0.93],sp=[0.5,1.0,1.5],so=[2/3,1.0,4/3])
BASE=dict(q=0.7,cv=0.08,cr=0.05,Ralt=0.87,sp=1.0,so=1.0)
def run(p):
    out={}
    for k in fam:
        df,pr,po,dTp=B[k]; po2=po.copy()
        pers=(df.cause.values=="persistent_reasoning"); oos=(df.cause.values=="out_of_specialty")
        po2[pers]=pr[pers]-p["sp"]*(pr[pers]-po[pers]); po2[oos]=pr[oos]-p["so"]*(pr[oos]-po[oos])
        r=regret(pr,po2,dTp,p["q"],p["cv"],p["cr"],p["Ralt"])
        out[k]={c:float(r[(df.cond.values==c)].mean()) for c in CO}
    out["pool"]={c:float(np.mean([out[k][c] for k in fam])) for c in CO}
    return out
keys=list(G); grid=[dict(zip(keys,v)) for v in itertools.product(*[G[x] for x in keys])]
res=[(p,run(p)) for p in grid]
def frac(a,b,which):
    return float(np.mean([r[which][a]<r[which][b]-1e-12 for p,r in res]))
summ={}
for a in ["graph","graph_rule_inferred","graph_rule"]:
    for b in ["outcome","skill"]:
        summ[f"{a}<{b}"]={w:round(frac(a,b,w),3) for w in ["pool"]+fam}
print(len(res),"grid points"); print(json.dumps(summ,indent=1))
# ordering of pooled regret at base
print("base pooled",{c:round(v,4) for c,v in run(BASE)["pool"].items()})
# one-at-a-time
oat={}
for x in keys:
    oat[x]={}
    for v in G[x]:
        p=dict(BASE); p[x]=v; r=run(p)["pool"]
        oat[x][v]={c:round(r[c],4) for c in ["outcome","skill","graph","graph_rule_inferred","graph_rule"]}
for x in keys:
    for v in G[x]:
        r=oat[x][v]; print(x,round(v,3),"out",r["outcome"],"skill",r["skill"],"graph",r["graph"],"inf",r["graph_rule_inferred"],"true",r["graph_rule"], "| g-o",round(r["graph"]-r["outcome"],4),"g-s",round(r["graph"]-r["skill"],4))
# where does graph lose to outcome / skill (pooled)? list worst
lose=[(p,r["pool"]["graph"]-r["pool"]["outcome"]) for p,r in res if r["pool"]["graph"]>=r["pool"]["outcome"]]
print("graph>=outcome pooled count",len(lose)); 
loseS=[(p,round(r["pool"]["graph"]-r["pool"]["skill"],4)) for p,r in res if r["pool"]["graph"]>=r["pool"]["skill"]]
print("graph>=skill pooled count",len(loseS)); print(loseS[:5])
d=[r["pool"]["graph"]-r["pool"]["outcome"] for p,r in res]; print("g-o range",min(d),max(d))
d=[r["pool"]["graph"]-r["pool"]["skill"] for p,r in res]; print("g-s range",min(d),max(d))
d=[r["pool"]["graph_rule_inferred"]-r["pool"]["skill"] for p,r in res]; print("inf-s range",min(d),max(d))
d=[r["pool"]["graph_rule"]-r["pool"]["outcome"] for p,r in res]; print("true-o range",min(d),max(d))
json.dump(dict(summ=summ,oat={x:{str(v):oat[x][v] for v in oat[x]} for x in oat}),open(OUT+"/sweep_out.json","w"))
