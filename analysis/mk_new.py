import os
import sys,json,pickle; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
import tax
D={k:load(k)[0] for k in RUNS}; fam=["gpt","haiku","llama"]
A=pd.concat([D[k] for k in fam]); rng=np.random.default_rng(2)
def bm(df,col): return df.groupby("base")[col].mean()
def bci(v,B=5000):
    v=np.asarray(v); bs=[v[rng.integers(0,len(v),len(v))].mean() for _ in range(B)]; return v.mean(),np.percentile(bs,2.5),np.percentile(bs,97.5)
W=lambda n,L: open(OUT+"/"+n+".tex","w").write("\n".join(L))
# --- measured-target table
rows=[("outcome","Outcome-only"),("skill","Skill-cond."),("graph","ClaimGraph"),("graph_rule_inferred","Graph+rule (inf.)"),("graph_rule_fit","Graph+rule (fit)"),("graph_rule","Graph+rule (true)")]
def cell(c,causes,ci=False):
    s=A[(A.cond==c)&(A.cause.isin(causes))]; m,lo,hi=bci(bm(s,"tce").values)
    return f"{m:.3f} [{lo:.3f}, {hi:.3f}]" if ci else f"{m:.3f}"
L=[]
for c,l in rows:
    L.append(l+" & "+cell(c,["persistent_reasoning"],True)+" & "+cell(c,["out_of_specialty"])+" & "+cell(c,["missing_context","tool_failure"])+r" \\")
    if c=="graph": L[-1]+="\n\\midrule"
W("tab_meas",L)
# --- parse failure table (Haiku) + other runs
LLMC=[("none","No memory"),("raw","Raw history"),("raw_cot","Raw + CoT"),("outcome","Outcome-only"),("skill","Skill-cond."),("graph_masked","Graph, masked"),("graph","ClaimGraph"),("graph_no_toolstate","No tool state"),("graph_no_persist","No persistence fields"),("graph_no_parent","No parent links")]
H=D["haiku"]; C4=["missing_context","tool_failure","out_of_specialty","persistent_reasoning"]
L=[]
for c,l in LLMC:
    s=H[H.cond==c]; cells=[str(int(s[s.cause==x].parse_fail.sum())) for x in C4]; tot=int(s.parse_fail.sum())
    L.append(l+" & "+" & ".join(cells)+f" & {tot} & {100*tot/len(s):.1f}\\%"+r" \\")
# inferred-cause rule rows with no inferred cause
s=H[H.cond=="graph_rule_inferred"]; na=s[s.attr_cause.isna()]
L.append("Graph+rule (inf.)$^{\\dagger}$ & "+" & ".join(str(int((na.cause==x).sum())) for x in C4)+f" & {len(na)} & {100*len(na)/len(s):.1f}\\%"+r" \\")
W("tab_parse",L)
print(open(OUT+"/tab_parse.tex").read())
# --- exclusion vs imputation
def rmk(df,c,m,excl):
    d=df[df.cond==c]
    if excl: d=d[(d.parse_fail==0)&(d.attr_cause.notna()|(c!="graph_rule_inferred"))]
    return d.groupby("base")[m].mean().mean()
ex=[("none","No memory"),("raw","Raw history"),("outcome","Outcome-only"),("skill","Skill-cond."),("graph_masked","Graph, masked"),("graph","ClaimGraph"),("graph_rule_inferred","Graph+rule (inf.)")]
Ms=["tce","tuse","regret","under_distrust"]
L=[]
for c,l in ex:
    cells=[]
    for m in Ms:
        a=np.mean([rmk(D[k],c,m,False) for k in fam]); b=np.mean([rmk(D[k],c,m,True) for k in fam])
        cells.append(f"{a:.3f} & {b:.3f}")
    L.append(l+" & "+" & ".join(cells)+r" \\")
W("tab_excl",L)
print(open(OUT+"/tab_excl.tex").read())
# --- four-run pooled main
F4=list(RUNS); rows4=[("none","No memory"),("raw","Raw history"),("outcome","Outcome-only"),("skill","Skill-cond."),("graph_masked","Graph, masked"),("graph","ClaimGraph"),("graph_rule_inferred","Graph+rule (inf.)"),("graph_rule","Graph+rule (true)")]
L=[]
for c,l in rows4:
    L.append(l+" & "+" & ".join(f"{np.mean([bm(D[k][D[k].cond==c],m).mean() for k in F4]):.3f}" for m in ["tce","tuse","regret","fcsr","over_distrust","under_distrust"])+r" \\")
W("tab_main4",L); print(open(OUT+"/tab_main4.tex").read())
# --- attribution micro accuracy (3-family pooled) by cause, and reconcile
acs=[("none","No memory"),("raw","Raw history"),("raw_cot","Raw + CoT"),("outcome","Outcome-only"),("skill","Skill-cond."),("graph_masked","Graph, masked"),("graph","ClaimGraph")]
L=[]
for c,l in acs:
    s=A[(A.cond==c)&A.attr_correct.notna()]
    L.append(l+f" & {s.attr_correct.mean():.2f} & "+" & ".join(f"{s[s.cause==x].attr_correct.mean():.2f}" for x in C4)+r" \\")
W("tab_attr",L); print(open(OUT+"/tab_attr.tex").read())
# taxonomy 3-family corrected
T,N,NA=tax.table(fam)
tx=[("blamed_agent_for_context","Blamed for context"),("blamed_agent_for_tool_fault","Blamed for tool fault"),("cause_misattribution","Cause misattributed"),("misled_by_subagent_self_report","Misled by self-report"),("routing_error_penalized_true_specialty","Routing$\\to$specialty penalized"),("scope_spillover_to_unaffected_skills","Scope spillover"),("under_reaction_to_persistent_weakness","Persistent under-reaction"),("unparseable_supervisor_output","Unparseable output")]
cc=["raw","outcome","skill","graph_masked","graph","graph_rule_inferred"]
W("tab_tax",[l+" & "+" & ".join(str(T[c][k]) for c in cc)+r" \\" for k,l in tx])
print(open(OUT+"/tab_tax.tex").read())
L=[]
for c,l in [("raw","Raw history"),("outcome","Outcome-only"),("skill","Skill-cond."),("graph_masked","Graph, masked"),("graph","ClaimGraph"),("graph_rule_inferred","G+rule (inf.)")]:
    mis=T[c]["cause_misattribution"]; ml=T[c]["misled_by_subagent_self_report"]; err=mis+ml
    L.append(f"{l} & {N[c]} & {NA[c]} & {mis} + {ml} = {err} & {1-err/NA[c]:.3f} & {A[(A.cond==c)&A.attr_correct.notna()].attr_correct.mean():.3f}"+r" \\")
W("tab_recon",L); print(open(OUT+"/tab_recon.tex").read())
# sweep table
S=json.load(open(OUT+"/sweep_out.json"))
lab=[("q","Verify catch rate $q$",["0.5","0.7","0.9"]),("cv","Verify cost $c_v$",["0.04","0.08","0.12"]),("cr","Reroute cost $c_r$",["0.02","0.05","0.1"]),("Ralt","Alt.\\ reliability $R_{\\mathrm{alt}}$",["0.8","0.87","0.93"]),("sp","Persistent damage $\\times$",["0.5","1.0","1.5"]),("so","OOS penalty (0.10 / 0.15 / 0.20)",["0.6666666666666666","1.0","1.3333333333333333"])]
L=[]
def f(x): return ("$-$" if x<0 else "$+$")+f"{abs(x):.3f}"
for key,name,vals in lab:
    cells=[]
    for v in vals:
        r=S["oat"][key][v]; cells.append(f"{f(r['graph']-r['outcome'])} / {f(r['graph']-r['skill'])}")
    shown=[("0.10","0.15","0.20")] if key=="so" else None
    L.append(name+(" (low / mid / high)" if key!="so" else "")+" & "+(" / ".join(vals) if key not in("so",) else "")+" & "+" & ".join(cells)+r" \\")
W("tab_sens",L); print(open(OUT+"/tab_sens.tex").read())
