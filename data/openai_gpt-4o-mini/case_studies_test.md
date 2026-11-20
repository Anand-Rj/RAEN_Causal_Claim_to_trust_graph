# Case studies (test split)
**LLM:openai/gpt-4o-mini | profiles:measured**

Selection rule: for each misalignment type, the highest-TCE episode from each of up to 3 distinct conditions (fixed rule, not hand-picked) + 1 random episode (seeded).

## blamed_agent_for_context  (n=777 episode-condition pairs)

**Episode** `hotpotqa-35|missing_context`  |  condition `raw_cot`  |  true cause `missing_context`  |  failing agent `multihop_agent`  |  TCE=0.250
- Task: What is the middle name of the actress who played Lucy Baker in the TV series Lassie ?
- Subagent said: *Rosalind Ayres* (conf 0.92); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Wanda
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.5, 'multihop': -0.5, 'quant': 0.0, 'tool': 0.0}  attributed cause: tool_failure
- Lead agent rationale: The agent's reliance on an unreliable tool led to incorrect output. This issue may recur if the tool's accuracy does not improve, affecting both fact and multihop skills.
- Regret: 0.000

**Episode** `tool_synth-38|missing_context`  |  condition `graph_no_parent`  |  true cause `missing_context`  |  failing agent `tool_agent`  |  TCE=0.225
- Task: Using the lookup tool, which has the larger founding year: Kelby or Arvel?
- Subagent said: *Kelby* (conf 0.7); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Arvel
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': -0.2, 'tool': -0.3}  attributed cause: missing_context
- Lead agent rationale: The agent failed to provide sufficient evidence and context, leading to incorrect output. This significantly impacts trust in its tool-related capabilities.
- Regret: 0.160

**Episode** `hotpotqa-35|missing_context`  |  condition `raw`  |  true cause `missing_context`  |  failing agent `multihop_agent`  |  TCE=0.175
- Task: What is the middle name of the actress who played Lucy Baker in the TV series Lassie ?
- Subagent said: *Rosalind Ayres* (conf 0.92); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Wanda
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': 0.0, 'tool': -0.3}  attributed cause: tool_failure
- Lead agent rationale: The agent relied on an unreliable tool, leading to an incorrect answer. Trust in its ability to use tools effectively is notably diminished.
- Regret: 0.010

**Episode** `gsm8k-51|missing_context`  |  condition `graph`  |  true cause `missing_context`  |  failing agent `quant_agent`  |  TCE=0.050
- Task: How many guests did not get a second hotdog?
- Subagent said: *27* (conf 0.72); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer 26
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.2, 'tool': 0.0}  attributed cause: missing_context
- Lead agent rationale: The agent failed due to missing context in a quant task, directly impacting its reliability in future quant tasks.
- Regret: 0.000

## blamed_agent_for_tool_fault  (n=701 episode-condition pairs)

**Episode** `tool_synth-7|tool_failure`  |  condition `raw_cot`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.250
- Task: Using the lookup tool, which has the larger elevation (m): Calloway or Oakridge?
- Subagent said: *Oakridge* (conf 0.93); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.5, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.5}  attributed cause: tool_failure
- Lead agent rationale: The agent's reliance on a faulty tool led to an incorrect conclusion. Although the tool is now repaired, past reliance on flawed data raises concerns for future tasks.
- Regret: 0.360

**Episode** `tool_synth-5|tool_failure`  |  condition `graph_masked`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.188
- Task: Using the lookup tool, which has the larger annual rainfall (mm): Jarrow or Lyndale?
- Subagent said: *Jarrow* (conf 0.72); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Lyndale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.25, 'tool': -0.5}  attributed cause: tool_failure
- Lead agent rationale: The agent failed to retrieve necessary data, leading to an incorrect conclusion. This significantly impacts trust in future tool-related tasks.
- Regret: 0.360

**Episode** `hotpotqa-9|tool_failure`  |  condition `raw`  |  true cause `tool_failure`  |  failing agent `multihop_agent`  |  TCE=0.150
- Task: Who wrote the novel that the movie directed by Stanley Kubrick that was sampled in the album "Where Blood and Fire Bring Rest" was based on?
- Subagent said: *Stanley Kubrick's Boxes* (conf 0.86); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Stephen King
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.2}  attributed cause: tool_failure
- Lead agent rationale: The agent's reliance on a faulty tool led to an incorrect answer. Trust in fact and multihop skills decreases, while tool trust improves post-repair.
- Regret: 0.130

**Episode** `hotpotqa-4|tool_failure`  |  condition `graph`  |  true cause `tool_failure`  |  failing agent `multihop_agent`  |  TCE=0.050
- Task: What church was the college Marjorie Hass is the 20th president of formerly affiliated with?
- Subagent said: *Debora Spar* (conf 0.77); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Presbyterian Church
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': -0.2, 'quant': 0.0, 'tool': 0.0}  attributed cause: tool_failure
- Lead agent rationale: The multihop_agent's failure was due to tool issues, affecting its multihop performance. Trust is reduced in multihop but remains unchanged in other skills.
- Regret: 0.000

## cause_misattribution  (n=1398 episode-condition pairs)

**Episode** `tool_synth-12|persistent_reasoning`  |  condition `raw`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.194
- Task: Using the lookup tool, which has the larger population (thousands): Calloway or Kelby?
- Subagent said: *Kelby* (conf 0.73); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': -0.25, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: The agent failed to process the tool output correctly, indicating a lack of proficiency in fact-checking despite high tool reliability.
- Regret: 0.490

**Episode** `tool_synth-12|persistent_reasoning`  |  condition `raw_cot`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.181
- Task: Using the lookup tool, which has the larger population (thousands): Calloway or Kelby?
- Subagent said: *Kelby* (conf 0.73); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': -0.2, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: The agent misidentified the larger population due to a lack of understanding of the context, indicating a recurring issue with reasoning in its specialty.
- Regret: 0.490

**Episode** `tool_synth-40|persistent_reasoning`  |  condition `graph_masked`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.181
- Task: Using the lookup tool, which has the larger population (thousands): Marlow or Pennard?
- Subagent said: *Pennard* (conf 0.92); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Marlow
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': -0.3, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.1}  attributed cause: out_of_specialty
- Lead agent rationale: The agent's final answer was incorrect, indicating a failure in competency within its declared specialty, justifying a reduction in trust for future tool tasks.
- Regret: 0.490

**Episode** `tool_synth-1|persistent_reasoning`  |  condition `outcome`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.156
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.87); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.1}  attributed cause: out_of_specialty
- Lead agent rationale: The rejection indicates a failure in the agent's ability to provide accurate recommendations, particularly affecting its reliability in the tool skill.
- Regret: 0.490

## misled_by_subagent_self_report  (n=133 episode-condition pairs)

**Episode** `hotpotqa-35|missing_context`  |  condition `raw_cot`  |  true cause `missing_context`  |  failing agent `multihop_agent`  |  TCE=0.250
- Task: What is the middle name of the actress who played Lucy Baker in the TV series Lassie ?
- Subagent said: *Rosalind Ayres* (conf 0.92); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Wanda
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.5, 'multihop': -0.5, 'quant': 0.0, 'tool': 0.0}  attributed cause: tool_failure
- Lead agent rationale: The agent's reliance on an unreliable tool led to incorrect output. This issue may recur if the tool's accuracy does not improve, affecting both fact and multihop skills.
- Regret: 0.000

**Episode** `tool_synth-1|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.188
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.81); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.3, 'multihop': -0.3, 'quant': 0.0, 'tool': -0.3}  attributed cause: tool_failure
- Lead agent rationale: The multihop_agent misinterpreted reliable tool data due to tool output issues, impacting its multihop reasoning and fact accuracy.
- Regret: 0.000

**Episode** `tool_synth-7|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `fact_agent`  |  TCE=0.087
- Task: Using the lookup tool, which has the larger elevation (m): Calloway or Oakridge?
- Subagent said: *Oakridge* (conf 0.89); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.3, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.2}  attributed cause: tool_failure
- Lead agent rationale: The agent misinterpreted the tool output, indicating a significant drop in trust regarding fact retrieval and tool usage, while its multihop and quant skills remain unaffected.
- Regret: 0.063

## routing_error_penalized_true_specialty  (n=256 episode-condition pairs)

**Episode** `tool_synth-1|out_of_specialty`  |  condition `raw`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.188
- Task: Using the lookup tool, which has the larger elevation (m): Eastvale or Pennard?
- Subagent said: *Pennard* (conf 0.81); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Eastvale
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.3, 'multihop': -0.3, 'quant': 0.0, 'tool': -0.3}  attributed cause: tool_failure
- Lead agent rationale: The multihop_agent misinterpreted reliable tool data due to tool output issues, impacting its multihop reasoning and fact accuracy.
- Regret: 0.000

**Episode** `tool_synth-12|out_of_specialty`  |  condition `raw_cot`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.188
- Task: Using the lookup tool, which has the larger population (thousands): Calloway or Kelby?
- Subagent said: *Kelby* (conf 0.82); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.15}
- Lead agent trust change: {'fact': -0.3, 'multihop': -0.3, 'quant': 0.0, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: The agent's error stemmed from operating outside its declared specialty, leading to a significant misjudgment. This weakness may persist in future tasks that fall outside its expertise.
- Regret: 0.070

**Episode** `gsm8k-19|out_of_specialty`  |  condition `graph`  |  true cause `out_of_specialty`  |  failing agent `multihop_agent`  |  TCE=0.138
- Task: How much longer does Ray take to swim 3 miles on a hot day than a cold day?
- Subagent said: *49* (conf 0.72); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer 54
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': -0.15, 'tool': 0.0}
- Lead agent trust change: {'fact': 0.0, 'multihop': -0.2, 'quant': -0.5, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: The multihop agent failed in quant tasks due to being out of specialty, significantly decreasing trust in its quant capabilities for future tasks.
- Regret: 0.000

**Episode** `gsm8k-7|out_of_specialty`  |  condition `raw_cot`  |  true cause `out_of_specialty`  |  failing agent `fact_agent`  |  TCE=0.037
- Task: How many tubes of paint does Jasper have?
- Subagent said: *13* (conf 0.88); self-report: "This task is outside my declared specialty."
- Lead agent rejection: correct answer 11
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': -0.15, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.15, 'multihop': 0.0, 'quant': -0.15, 'tool': 0.0}  attributed cause: out_of_specialty
- Lead agent rationale: The agent answered incorrectly due to operating outside its specialty, leading to a decrease in trust for fact and quant skills. This issue may recur if tasks remain outside its expertise.
- Regret: 0.000

## scope_spillover_to_unaffected_skills  (n=152 episode-condition pairs)

**Episode** `tool_synth-7|tool_failure`  |  condition `raw_cot`  |  true cause `tool_failure`  |  failing agent `tool_agent`  |  TCE=0.250
- Task: Using the lookup tool, which has the larger elevation (m): Calloway or Oakridge?
- Subagent said: *Oakridge* (conf 0.93); self-report: "The retrieval tool returned unreliable output."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.5, 'multihop': 0.0, 'quant': 0.0, 'tool': -0.5}  attributed cause: tool_failure
- Lead agent rationale: The agent's reliance on a faulty tool led to an incorrect conclusion. Although the tool is now repaired, past reliance on flawed data raises concerns for future tasks.
- Regret: 0.360

**Episode** `tool_synth-38|missing_context`  |  condition `graph_no_parent`  |  true cause `missing_context`  |  failing agent `tool_agent`  |  TCE=0.225
- Task: Using the lookup tool, which has the larger founding year: Kelby or Arvel?
- Subagent said: *Kelby* (conf 0.7); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Arvel
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': 0.0, 'quant': 0.0, 'tool': 0.0}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.2, 'quant': -0.2, 'tool': -0.3}  attributed cause: missing_context
- Lead agent rationale: The agent failed to provide sufficient evidence and context, leading to incorrect output. This significantly impacts trust in its tool-related capabilities.
- Regret: 0.160

**Episode** `hotpotqa-2|persistent_reasoning`  |  condition `graph_no_toolstate`  |  true cause `persistent_reasoning`  |  failing agent `multihop_agent`  |  TCE=0.194
- Task: The Un-Americans contained which wrestler who also went by what TNA Wrestling name?
- Subagent said: *Suicide (wrestling)* (conf 0.81); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Andrew Martin
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': -0.2, 'quant': -0.1, 'tool': 0.175}
- Lead agent trust change: {'fact': -0.2, 'multihop': -0.3, 'quant': -0.2, 'tool': -0.2}  attributed cause: persistent_reasoning
- Lead agent rationale: The agent demonstrated persistent reasoning issues, leading to a significant error in a multihop task, impacting trust across related skills.
- Regret: 0.063

**Episode** `hotpotqa-25|persistent_reasoning`  |  condition `raw_cot`  |  true cause `persistent_reasoning`  |  failing agent `multihop_agent`  |  TCE=0.119
- Task: What speech by Abraham Lincoln was part of Richard Heffner's A Documentary History of the United States?
- Subagent said: *Abraham Lincoln High School (Des Moines, Iowa)* (conf 0.81); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Gettysburg Address
- Oracle trust change (dT*): {'fact': 0.0, 'multihop': -0.2, 'quant': -0.1, 'tool': 0.175}
- Lead agent trust change: {'fact': -0.15, 'multihop': -0.15, 'quant': 0.0, 'tool': 0.0}  attributed cause: persistent_reasoning
- Lead agent rationale: The agent's incorrect conclusion stemmed from flawed reasoning rather than a lack of information. This persistent reasoning issue may recur in future multihop tasks.
- Regret: 0.000

## under_reaction_to_persistent_weakness  (n=862 episode-condition pairs)

**Episode** `tool_synth-40|persistent_reasoning`  |  condition `graph_no_parent`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.431
- Task: Using the lookup tool, which has the larger population (thousands): Marlow or Pennard?
- Subagent said: *Pennard* (conf 0.92); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Marlow
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': -0.5, 'multihop': -0.5, 'quant': -0.5, 'tool': -0.1}  attributed cause: persistent_reasoning
- Lead agent rationale: The agent's persistent reasoning led to a significant error in its conclusion, undermining trust across all skills, particularly in fact, multihop, and quant.
- Regret: 0.490

**Episode** `tool_synth-23|persistent_reasoning`  |  condition `graph`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.406
- Task: Using the lookup tool, which has the larger elevation (m): Pennard or Lyndale?
- Subagent said: *Lyndale* (conf 0.88); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Pennard
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': -0.5, 'multihop': -0.5, 'quant': -0.5, 'tool': -0.2}  attributed cause: persistent_reasoning
- Lead agent rationale: The agent demonstrated persistent reasoning errors, affecting all skills related to logical conclusions, while minor trust reduction for tool skill reflects its previous reliability.
- Regret: 0.055

**Episode** `tool_synth-12|persistent_reasoning`  |  condition `graph_no_toolstate`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.381
- Task: Using the lookup tool, which has the larger population (thousands): Calloway or Kelby?
- Subagent said: *Kelby* (conf 0.73); self-report: "I was not given all of the relevant facts for this question."
- Lead agent rejection: correct answer Calloway
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': -0.5, 'multihop': -0.5, 'quant': -0.5, 'tool': -0.3}  attributed cause: persistent_reasoning
- Lead agent rationale: The agent exhibited persistent reasoning errors leading to a critical mistake, warranting significant trust reduction across all skills.
- Regret: 0.055

**Episode** `tool_synth-36|persistent_reasoning`  |  condition `graph_rule`  |  true cause `persistent_reasoning`  |  failing agent `tool_agent`  |  TCE=0.094
- Task: Using the lookup tool, which has the larger annual rainfall (mm): Norwick or Pennard?
- Subagent said: *Pennard* (conf 0.75); self-report: "I had all the information I needed; my reasoning was wrong."
- Lead agent rejection: correct answer Norwick
- Oracle trust change (dT*): {'fact': -0.1, 'multihop': 0.1, 'quant': -0.1, 'tool': -0.425}
- Lead agent trust change: {'fact': 0.0, 'multihop': 0.0, 'quant': -0.05, 'tool': -0.3}  attributed cause: persistent_reasoning
- Lead agent rationale: rule(prior)
- Regret: 0.055
