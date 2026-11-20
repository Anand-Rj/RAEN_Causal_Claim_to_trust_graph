import os
import gzip, json, numpy as np, pandas as pd, sys
U=os.environ.get("CTB_DATA","data")+"/"
OUT=os.environ.get("CTB_OUT","analysis_out"); os.makedirs(OUT,exist_ok=True)
RUNS={"gpt":"openai_gpt-4o-mini","haiku":"anthropic_claude-haiku-5.5","llama":"meta-llama_llama-3.3-70b-instruct","hetero":"hetero"}
NM={"gpt":"GPT-4o-mini","haiku":"Haiku 5.5","llama":"Llama-3.3-70B","hetero":"Team"}
def load(k):
    d=U+RUNS[k]; df=pd.read_csv(d+"/results.csv.gz"); df=df[df.split=="test"].copy(); df["run"]=k
    eps={}
    for l in gzip.open(d+"/episodes.jsonl.gz","rt"):
        e=json.loads(l); eps[e["id"]]=e
    return df,eps
