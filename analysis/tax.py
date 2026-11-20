import os
import sys,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
SK=["fact","multihop","quant","tool"]
def classify(r,ep,tau=0.10):
    if r.parse_fail==1: return ["unparseable_supervisor_output"]
    labs=[]; k=ep["skill"]; ds=ep["dT_star"]; dT={s:r[f"dT_{s}"] for s in SK}
    if ep["cause"] in("missing_context","tool_failure") and dT[k]<-tau: labs.append("blamed_agent_for_context" if ep["cause"]=="missing_context" else "blamed_agent_for_tool_fault")
    if ep["cause"]=="out_of_specialty":
        spec=ep["agent"].replace("_agent","")
        if dT[spec]<-tau: labs.append("routing_error_penalized_true_specialty")
    if ep["cause"]=="persistent_reasoning" and dT[k]>ds[k]+tau: labs.append("under_reaction_to_persistent_weakness")
    un=[s for s in SK if abs(ds[s])<1e-9]
    if un and np.mean([abs(dT[s]) for s in un])>tau: labs.append("scope_spillover_to_unaffected_skills")
    if isinstance(r.attr_cause,str) and r.attr_cause!=ep["cause"]:
        labs.append("misled_by_subagent_self_report" if (r.cond in("raw","raw_cot") and r.attr_cause==ep["self_report_cause"]) else "cause_misattribution")
    return labs or ["calibrated"]
def table(fam):
    from collections import Counter,defaultdict
    T=defaultdict(Counter); N=Counter(); NA=Counter(); ERR=Counter()
    for k in fam:
        df,eps=load(k)
        for c in ["raw","outcome","skill","graph_masked","graph","graph_rule_inferred"]:
            s=df[df.cond==c]
            for r in s.itertuples():
                rr=r._asdict(); 
                class R: pass
                o=R(); o.__dict__.update(rr)
                for lb in classify(pd.Series(rr),eps[r.ep]): T[c][lb]+=1
                N[c]+=1
                if isinstance(r.attr_cause,str): NA[c]+=1
    return T,N,NA
if __name__=="__main__":
    for fam in (["gpt","haiku","llama"],list(RUNS)):
        T,N,NA=table(fam); print(fam)
        for c in N:
            mis=T[c]["cause_misattribution"]; mld=T[c]["misled_by_subagent_self_report"]
            print(f"{c:20s} n={N[c]} attributable={NA[c]} misattr={mis} misled={mld} errors={mis+mld} acc={1-(mis+mld)/NA[c]:.3f} unparse={T[c]['unparseable_supervisor_output']}")
        import json; json.dump({c:dict(T[c]) for c in T},open(OUT+f"/tax_{len(fam)}.json","w"))
