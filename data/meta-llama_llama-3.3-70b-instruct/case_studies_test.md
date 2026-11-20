# Case studies (test split)
**LLM:meta-llama/llama-3.3-70b-instruct | profiles:measured**

Selection rule: for each misalignment type, the highest-TCE episode from each of up to 3 distinct conditions (fixed rule, not hand-picked) + 1 random episode (seeded).

## blamed_agent_for_context  (n=371 episode-condition pairs)

**Episode** `tool_synth-48|missing_context`  |  condition `raw_cot`  |  true cause `missing_context`  |  failing agent `tool_agent`  |  TCE=0.175
- Task: Using the lookup tool, which has the larger population (thousands): Jarrow or Oakridge?
- Subagent said: *Jarrow* (conf 0.94); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Oakridge
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.1, 'quant': -0.1, 'tool': -0.3}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect inference from partial data
- Regret: 0.185

**Episode** `hotpotqa-2|missing_context`  |  condition `outcome`  |  true cause `missing_context`  |  failing agent `multihop_agent`  |  TCE=0.125
- Task: The Un-Americans contained which wrestler who also went by what TNA Wrestling name?
- Subagent said: *Suicide (wrestling)* (conf 0.9); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer Andrew Martin
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': -0.1, 'tool': -0.1}  attributed cause: out_of_specialty
- Lead agent rationale: Rejected recommendation impacts trust
- Regret: 0.025

**Episode** `gsm8k-0|missing_context`  |  condition `graph_rule_inferred`  |  true cause `missing_context`  |  failing agent `quant_agent`  |  TCE=0.087
- Task: How many miles did Ahito run?
- Subagent said: *17* (conf 0.9); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer 16
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.3, 'tool': -0.05}  attributed cause: persistent_reasoning
- Lead agent rationale: rule(prior) on inferred cause
- Regret: 0.095

**Episode** `hotpotqa-44|missing_context`  |  condition `raw`  |  true cause `missing_context`  |  failing agent `multihop_agent`  |  TCE=0.050
- Task: What team plays within the Big 12 Conference and has Kevin Bookout playing for them?
- Subagent said: *2015–16 Baylor Lady Bears basketball team* (conf 0.81); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Oklahoma Sooners men's basketball
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: missing_context
- Lead agent rationale: Lacked relevant facts
- Regret: 0.000

## blamed_agent_for_tool_fault  (n=450 episode-condition pairs)

**Episode** `hotpotqa-30|tool_failure`  |  condition `raw`  |  true cause `tool_failure`  |  failing agent `multihop_agent`  |  TCE=0.175
- Task: Which American film director hosted the 18th Independent Spirit Awards in 2002?
- Subagent said: *Independent Spirit Awards* (conf 0.95); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer John Waters
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.3, 'quant': -0.1, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Overconfident answer
- Regret: 0.025

**Episode** `tool_synth-12|tool_failure`  |  condition `raw_cot`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.150
- Task: Using the lookup tool, which has the larger population (thousands): Calloway or Kelby?
- Subagent said: *Kelby* (conf 0.74); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.1, 'quant': -0.1, 'tool': -0.2}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect inference despite tool failure
- Regret: 0.045

**Episode** `gsm8k-0|tool_failure`  |  condition `graph`  |  true cause `tool_failure`  |  failing agent `quant_agent`  |  TCE=0.125
- Task: How many miles did Ahito run?
- Subagent said: *17* (conf 0.89); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer 16
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.2, 'tool': -0.3}  attributed cause: tool_failure
- Lead agent rationale: Tool failure in quant task
- Regret: 0.128

**Episode** `tool_synth-7|tool_failure`  |  condition `graph_masked`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.050
- Task: Using the lookup tool, which has the larger elevation (m): Calloway or Oakridge?
- Subagent said: *Oakridge* (conf 0.93); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.2}  attributed cause: tool_failure
- Lead agent rationale: Tool failure in specialty area
- Regret: 0.020

## cause_misattribution  (n=1548 episode-condition pairs)

**Episode** `tool_synth-1|tool_failure`  |  condition `raw_cot`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.175
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.85); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': -0.2, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect reasoning despite tool output.
- Regret: 0.045

**Episode** `hotpotqa-30|tool_failure`  |  condition `raw`  |  true cause `tool_failure`  |  failing agent `multihop_agent`  |  TCE=0.175
- Task: Which American film director hosted the 18th Independent Spirit Awards in 2002?
- Subagent said: *Independent Spirit Awards* (conf 0.95); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer John Waters
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.3, 'quant': -0.1, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Overconfident answer
- Regret: 0.025

**Episode** `tool_synth-12|persistent_reasoning`  |  condition `graph_rule_inferred`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.163
- Task: Using the lookup tool, which has the larger population (thousands): Calloway or Kelby?
- Subagent said: *Kelby* (conf 0.73); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.075, 'quant': -0.075, 'tool': -0.4}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}  attributed cause: tool_failure
- Lead agent rationale: rule(prior) on inferred cause
- Regret: 0.667

**Episode** `hotpotqa-48|tool_failure`  |  condition `graph_masked`  |  true cause `tool_failure`  |  failing agent `multihop_agent`  |  TCE=0.050
- Task: When did the park at which Tivolis Koncertsal is located open?
- Subagent said: *Takino Suzuran Hillside National Government Park* (conf 0.88); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer 15 August 1843
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect multihop reasoning
- Regret: 0.000

## misled_by_subagent_self_report  (n=150 episode-condition pairs)

**Episode** `fever-75|persistent_reasoning`  |  condition `raw`  |  true cause `persistent_reasoning`  |  failing agent `fact_agent`  |  TCE=0.156
- Task: Claim: The Bahamas is a city.  Answer SUPPORTS or REFUTES.
- Subagent said: *SUPPORTS* (conf 0.71); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer REFUTES
- Oracle trust change (dT*): {'fact': -0.425, 'multihop': -0.05, 'quant': 0.1, 'tool': -0.1}
- Lead agent trust change: {'fact': -0.05, 'multihop': -0.05, 'quant': -0.05, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: Incorrect answer outside specialty
- Regret: 0.120

**Episode** `fever-75|persistent_reasoning`  |  condition `raw_cot`  |  true cause `persistent_reasoning`  |  failing agent `fact_agent`  |  TCE=0.156
- Task: Claim: The Bahamas is a city.  Answer SUPPORTS or REFUTES.
- Subagent said: *SUPPORTS* (conf 0.71); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer REFUTES
- Oracle trust change (dT*): {'fact': -0.425, 'multihop': -0.05, 'quant': 0.1, 'tool': -0.1}
- Lead agent trust change: {'fact': -0.05, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: Wrong due to out-of-specialty task.
- Regret: 0.120

**Episode** `tool_synth-40|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.113
- Task: Using the lookup tool, which has the larger population (thousands): Marlow or Pennard?
- Subagent said: *Pennard* (conf 0.87); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Marlow
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect reasoning despite correct evidence
- Regret: 0.025

## routing_error_penalized_true_specialty  (n=49 episode-condition pairs)

**Episode** `tool_synth-5|out_of_specialty`  |  condition `raw_cot`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.138
- Task: Using the lookup tool, which has the larger annual rainfall (mm): Jarrow or Lyndale?
- Subagent said: *Jarrow* (conf 0.93); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Lyndale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': -0.1, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect comparison in final step
- Regret: 0.025

**Episode** `gsm8k-19|out_of_specialty`  |  condition `outcome`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.113
- Task: How much longer does Ray take to swim 3 miles on a hot day than a cold day?
- Subagent said: *49* (conf 0.72); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer 54
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': -0.15, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: Rejected outside specialty
- Regret: 0.025

**Episode** `tool_synth-1|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.113
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.81); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect conclusion from correct evidence
- Regret: 0.025

**Episode** `tool_synth-1|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.113
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.81); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect conclusion from given evidence
- Regret: 0.025

## scope_spillover_to_unaffected_skills  (n=163 episode-condition pairs)

**Episode** `tool_synth-1|tool_failure`  |  condition `raw_cot`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.175
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.85); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': -0.2, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect reasoning despite tool output.
- Regret: 0.045

**Episode** `hotpotqa-30|tool_failure`  |  condition `raw`  |  true cause `tool_failure`  |  failing agent `multihop_agent`  |  TCE=0.175
- Task: Which American film director hosted the 18th Independent Spirit Awards in 2002?
- Subagent said: *Independent Spirit Awards* (conf 0.95); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer John Waters
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.3, 'quant': -0.1, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Overconfident answer
- Regret: 0.025

**Episode** `gsm8k-0|tool_failure`  |  condition `graph`  |  true cause `tool_failure`  |  failing agent `quant_agent`  |  TCE=0.125
- Task: How many miles did Ahito run?
- Subagent said: *17* (conf 0.89); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer 16
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.2, 'tool': -0.3}  attributed cause: tool_failure
- Lead agent rationale: Tool failure in quant task
- Regret: 0.128

**Episode** `tool_synth-5|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.113
- Task: Using the lookup tool, which has the larger annual rainfall (mm): Jarrow or Lyndale?
- Subagent said: *Jarrow* (conf 0.93); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Lyndale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.1, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect conclusion from given evidence
- Regret: 0.025

## under_reaction_to_persistent_weakness  (n=1047 episode-condition pairs)

**Episode** `tool_synth-25|persistent_reasoning`  |  condition `graph_no_parent`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.225
- Task: Using the lookup tool, which has the larger population (thousands): Jarrow or Fairhaven?
- Subagent said: *Fairhaven* (conf 0.85); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Jarrow
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.075, 'quant': -0.075, 'tool': -0.4}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.3, 'quant': -0.2, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Incorrect conclusion despite correct data
- Regret: 0.102

**Episode** `tool_synth-1|persistent_reasoning`  |  condition `graph`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.200
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.87); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.075, 'quant': -0.075, 'tool': -0.4}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': -0.2, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Rejected due to persistent reasoning error
- Regret: 0.102

**Episode** `tool_synth-1|persistent_reasoning`  |  condition `graph_no_toolstate`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.200
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.87); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.075, 'quant': -0.075, 'tool': -0.4}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': -0.2, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: Rejected due to persistent reasoning error
- Regret: 0.102

**Episode** `tool_synth-5|persistent_reasoning`  |  condition `graph_rule`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.075
- Task: Using the lookup tool, which has the larger annual rainfall (mm): Jarrow or Lyndale?
- Subagent said: *Jarrow* (conf 0.83); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Lyndale
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.075, 'quant': -0.075, 'tool': -0.4}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.05, 'tool': -0.3}  attributed cause: persistent_reasoning
- Lead agent rationale: rule(prior)
- Regret: 0.027
