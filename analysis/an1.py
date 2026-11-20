import os
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from load import *
pd.set_option("display.width",250); pd.set_option("display.max_columns",40)
D={k:load(k)[0] for k in RUNS}; A=pd.concat(D.values())
LLM=["none","raw","raw_cot","outcome","skill","graph_masked","graph","graph_no_parent","graph_no_toolstate","graph_no_persist","graph_rule_inferred"]
S=A[A.cond.isin(LLM)]
print("overall LLM-row parse-fail rate by run:"); print(S.groupby("run").parse_fail.agg(["sum","count","mean"]).round(4))
print(S[S.parse_fail==1].groupby(["run","cond"]).size())
h=A[(A.run=="haiku")&(A.cond=="raw")]; f=h[h.parse_fail==1]
print(f[["attr_cause","attr_correct","dT_fact","dT_quant","tce","regret","correct_decision","cause"]].head(5))
print("attr NaN rows in haiku raw:",h.attr_correct.isna().sum(), "of pf", len(f))
