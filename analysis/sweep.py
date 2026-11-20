import os
import sys, itertools, json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
SK=["fact","multihop","quant","tool"]
fam=["gpt","haiku","llama"]
CONDS=["none","raw","outcome","skill","graph_masked","graph","graph_rule_inferred","graph_rule"]
def build(k):
    df,eps=load(k); df=df[df.cond.isin(CONDS)].reset_index(drop=True)
    N=len(df); dT=np.clip(df[[f"dT_{s}" for s in SK]].values.astype(float),-1.0,0.5)
    pr=np.zeros((N,4)); po=np.zeros((N,4)); cause=df.cause.values
    cache={}
    for i,(ep) in enumerate(df.ep.values):
        if ep not in cache:
            e=eps[ep]; idx=[SK.index(p[0]) for p in e["probes"]]
            cache[ep]=(idx,[e["r_pre"][SK[j]] for j in idx],[e["r_post"][SK[j]] for j in idx])
        idx,a,b=cache[ep]; pr[i]=a; po[i]=b
        dTi=dT[i,idx]; 
        if i==0: pass
        pr_idx=idx
        # store per-probe dT
        if i==0: dTp=np.zeros((N,4))
        dTp[i]=dTi
    return df,pr,po,dTp
def regret(pr,po,dTp,q,cv,cr,Ralt):
    bel=np.clip(pr+dTp,0,1)
    def best(R):
        u=np.stack([R, R+(1-R)*q-cv, np.full_like(R,Ralt-cr)],0)
        # tie-break: first max with tolerance (delegate<verify<reroute)
        m=u.max(0); a=np.zeros(R.shape,int)
        a=np.where(u[1]>u[0]+1e-12,1,0); a=np.where(u[2]>np.take_along_axis(u,a[None],0)[0]+1e-12,2,a)
        return a,u
    asup,_=best(bel); aor,_=best(po)
    def util(a,R): return np.where(a==0,R,np.where(a==1,R+(1-R)*q-cv,Ralt-cr))
    return (util(aor,po)-util(asup,po)).sum(1)
if __name__=="__main__":
    B={k:build(k) for k in fam}
    # validate vs csv regret
    for k in fam:
        df,pr,po,dTp=B[k]; r=regret(pr,po,dTp,0.70,0.08,0.05,0.87)
        print(k,"max|diff| vs csv regret:",np.abs(r-df.regret.values).max())
    import pickle; pickle.dump(B,open(OUT+"/B.pkl","wb"))
