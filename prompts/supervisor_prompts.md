# Supervisor prompts (one example episode per cause)

## Cause: missing_context (episode gsm8k-0|missing_context)

### Condition: none

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

No record of any earlier incident is available.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Earlier interaction transcript:
Agent:quant_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> OK
Evidence shown to agent:
  [e0] Amber, Micah, and Ahito ran 52 miles in total.
  [e1] Micah ran 3.5 times what Amber ran.
  Step c1 (parent: none; evidence: e0,e1): Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.
  Step c2 (parent: c1; evidence: e0,e1): Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.
  Step c3 (parent: c2; evidence: e0,e1): This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.
  Step c4 (parent: c3; evidence: e0,e1): Final answer: 17.
  Confidence 0.9. I was not given all of the relevant facts for this question.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: The withheld item was later restored to the agent's context.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw_cot

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Earlier interaction transcript:
Agent:quant_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> OK
Evidence shown to agent:
  [e0] Amber, Micah, and Ahito ran 52 miles in total.
  [e1] Micah ran 3.5 times what Amber ran.
  Step c1 (parent: none; evidence: e0,e1): Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.
  Step c2 (parent: c1; evidence: e0,e1): Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.
  Step c3 (parent: c2; evidence: e0,e1): This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.
  Step c4 (parent: c3; evidence: e0,e1): Final answer: 17.
  Confidence 0.9. I was not given all of the relevant facts for this question.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: The withheld item was later restored to the agent's context.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). First reason explicitly about WHY the recommendation was wrong and whether that cause will recur, inside the rationale field (up to 80 words). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: outcome

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Record: quant_agent produced 1 recommendation that was rejected as incorrect.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: skill

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Record: quant_agent produced 1 rejected recommendation on 'quant' tasks.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_masked

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Claim graph for the rejected recommendation (cause fields not yet diagnosed):
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 2,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "UNKNOWN",
   "persistence": "UNKNOWN",
   "scope": "UNKNOWN",
   "resolved": "UNKNOWN"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 2,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "missing_context",
   "persistence": "transient",
   "scope": [],
   "resolved": "yes"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_parent

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 2,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "REJECTED (correct answer differs)",
   "tool_state": "ok",
   "failure_cause": "missing_context",
   "persistence": "transient",
   "scope": [],
   "resolved": "yes"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_toolstate

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 2
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c1"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c2"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "failure_cause": "missing_context",
   "persistence": "transient",
   "scope": [],
   "resolved": "yes"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_persist

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 2,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Amber, Micah, and Ahito ran 52 miles in total, and Micah ran 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Let Amber's distance be A miles. Then Micah's distance is 3.5A miles. The total distance run by all three is A + 3.5A + Ahito's distance = 52 miles.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "This simplifies to 4.5A + Ahito's distance = 52. To find Ahito's distance, we need to express it in terms of A: Ahito's distance = 52 - 4.5A.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1"
   ],
   "confidence": 0.9,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "missing_context"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

## Cause: tool_failure (episode gsm8k-0|tool_failure)

### Condition: none

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

No record of any earlier incident is available.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Earlier interaction transcript:
Agent:quant_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> [] (no rows)
Evidence shown to agent:
  (none)
  Step c1 (parent: none; evidence: none): There is no evidence available to determine how many miles Ahito ran.
  Step c2 (parent: c1; evidence: none): Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.
  Step c3 (parent: c2; evidence: none): Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.
  Step c4 (parent: c3; evidence: none): Final answer: 17.
  Confidence 0.89. I had all the information I needed; my reasoning was wrong.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: The tool was repaired and verified working for later tasks.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw_cot

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Earlier interaction transcript:
Agent:quant_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> [] (no rows)
Evidence shown to agent:
  (none)
  Step c1 (parent: none; evidence: none): There is no evidence available to determine how many miles Ahito ran.
  Step c2 (parent: c1; evidence: none): Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.
  Step c3 (parent: c2; evidence: none): Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.
  Step c4 (parent: c3; evidence: none): Final answer: 17.
  Confidence 0.89. I had all the information I needed; my reasoning was wrong.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: The tool was repaired and verified working for later tasks.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). First reason explicitly about WHY the recommendation was wrong and whether that cause will recur, inside the rationale field (up to 80 words). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: outcome

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Record: quant_agent produced 1 recommendation that was rejected as incorrect.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: skill

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Record: quant_agent produced 1 rejected recommendation on 'quant' tasks.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_masked

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Claim graph for the rejected recommendation (cause fields not yet diagnosed):
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 0,
  "retrieval_tool_state": "empty"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "There is no evidence available to determine how many miles Ahito ran.",
   "evidence": [],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "empty"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "empty"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "empty"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "empty",
   "failure_cause": "UNKNOWN",
   "persistence": "UNKNOWN",
   "scope": "UNKNOWN",
   "resolved": "UNKNOWN"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 0,
  "retrieval_tool_state": "empty"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "There is no evidence available to determine how many miles Ahito ran.",
   "evidence": [],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "empty"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "empty"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "empty"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "empty",
   "failure_cause": "tool_failure",
   "persistence": "transient",
   "scope": [],
   "resolved": "yes"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_parent

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 0,
  "retrieval_tool_state": "empty"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "There is no evidence available to determine how many miles Ahito ran.",
   "evidence": [],
   "confidence": null,
   "verification": "not independently verified",
   "tool_state": "empty"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "tool_state": "empty"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "tool_state": "empty"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "REJECTED (correct answer differs)",
   "tool_state": "empty",
   "failure_cause": "tool_failure",
   "persistence": "transient",
   "scope": [],
   "resolved": "yes"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_toolstate

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 0
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "There is no evidence available to determine how many miles Ahito ran.",
   "evidence": [],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c1"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c2"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "failure_cause": "tool_failure",
   "persistence": "transient",
   "scope": [],
   "resolved": "yes"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_persist

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 0,
  "retrieval_tool_state": "empty"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "There is no evidence available to determine how many miles Ahito ran.",
   "evidence": [],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "empty"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Without any specific information or data regarding Ahito's running distance, I cannot make any calculations or assumptions.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "empty"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Since there is no evidence to analyze, I cannot arrive at a conclusion about the number of miles Ahito ran.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "empty"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.89,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "empty",
   "failure_cause": "tool_failure"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

## Cause: out_of_specialty (episode gsm8k-0|out_of_specialty)

### Condition: none

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

No record of any earlier incident is available.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Earlier interaction transcript:
Agent:multihop_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> OK
Evidence shown to agent:
  [e0] Amber, Micah, and Ahito ran 52 miles in total.
  [e1] Amber ran 8 miles.
  [e2] Micah ran 3.5 times what Amber ran.
  Step c1 (parent: none; evidence: e0,e1,e2): Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.
  Step c2 (parent: c1; evidence: e0,e1,e2): Read the retrieved items to see what they establish.
  Step c3 (parent: c2; evidence: e0,e1,e2): Combined the facts. Combining the information available, the answer is 17.
  Step c4 (parent: c3; evidence: e0,e1,e2): Final answer: 17.
  Confidence 0.77. The retrieval tool returned unreliable output.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: The task was re-routed; the agent was not asked about it again.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw_cot

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Earlier interaction transcript:
Agent:multihop_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> OK
Evidence shown to agent:
  [e0] Amber, Micah, and Ahito ran 52 miles in total.
  [e1] Amber ran 8 miles.
  [e2] Micah ran 3.5 times what Amber ran.
  Step c1 (parent: none; evidence: e0,e1,e2): Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.
  Step c2 (parent: c1; evidence: e0,e1,e2): Read the retrieved items to see what they establish.
  Step c3 (parent: c2; evidence: e0,e1,e2): Combined the facts. Combining the information available, the answer is 17.
  Step c4 (parent: c3; evidence: e0,e1,e2): Final answer: 17.
  Confidence 0.77. The retrieval tool returned unreliable output.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: The task was re-routed; the agent was not asked about it again.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). First reason explicitly about WHY the recommendation was wrong and whether that cause will recur, inside the rationale field (up to 80 words). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: outcome

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Record: multihop_agent produced 1 recommendation that was rejected as incorrect.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: skill

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Record: multihop_agent produced 1 rejected recommendation on 'quant' tasks.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_masked

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Claim graph for the rejected recommendation (cause fields not yet diagnosed):
{
 "task_provenance": {
  "agent_declared_specialty": "multihop",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Read the retrieved items to see what they establish.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Combined the facts. Combining the information available, the answer is 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "UNKNOWN",
   "persistence": "UNKNOWN",
   "scope": "UNKNOWN",
   "resolved": "UNKNOWN"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "multihop",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Read the retrieved items to see what they establish.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Combined the facts. Combining the information available, the answer is 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "out_of_specialty",
   "persistence": "routing",
   "scope": [
    "quant"
   ],
   "resolved": "rerouted"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_parent

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "multihop",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Read the retrieved items to see what they establish.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Combined the facts. Combining the information available, the answer is 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "REJECTED (correct answer differs)",
   "tool_state": "ok",
   "failure_cause": "out_of_specialty",
   "persistence": "routing",
   "scope": [
    "quant"
   ],
   "resolved": "rerouted"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_toolstate

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "multihop",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null
  },
  {
   "claim_id": "c2",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Read the retrieved items to see what they establish.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c1"
  },
  {
   "claim_id": "c3",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Combined the facts. Combining the information available, the answer is 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c2"
  },
  {
   "claim_id": "c4",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "failure_cause": "out_of_specialty",
   "persistence": "routing",
   "scope": [
    "quant"
   ],
   "resolved": "rerouted"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_persist

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of multihop_agent BEFORE this incident (P(correct) per skill): fact=0.65, multihop=0.65, quant=0.45, tool=0.70

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "multihop",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Retrieved evidence with the retrieve tool (ok); items: e0, e1, e2.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Read the retrieved items to see what they establish.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Combined the facts. Combining the information available, the answer is 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "multihop_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": 0.77,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "out_of_specialty"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

## Cause: persistent_reasoning (episode gsm8k-0|persistent_reasoning)

### Condition: none

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

No record of any earlier incident is available.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Earlier interaction transcript:
Agent:quant_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> OK
Evidence shown to agent:
  [e0] Amber, Micah, and Ahito ran 52 miles in total.
  [e1] Amber ran 8 miles.
  [e2] Micah ran 3.5 times what Amber ran.
  Step c1 (parent: none; evidence: e0,e1,e2): Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.
  Step c2 (parent: c1; evidence: e1,e2): First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.
  Step c3 (parent: c2; evidence: e0): Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.
  Step c4 (parent: c3; evidence: none): Final answer: 17.
  Confidence 0.8. I had all the information I needed; my reasoning was wrong.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: No change was made; context and tools were already complete.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: raw_cot

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Earlier interaction transcript:
Agent:quant_agent
Task: How many miles did Ahito run?
Tool call: retrieve -> OK
Evidence shown to agent:
  [e0] Amber, Micah, and Ahito ran 52 miles in total.
  [e1] Amber ran 8 miles.
  [e2] Micah ran 3.5 times what Amber ran.
  Step c1 (parent: none; evidence: e0,e1,e2): Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.
  Step c2 (parent: c1; evidence: e1,e2): First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.
  Step c3 (parent: c2; evidence: e0): Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.
  Step c4 (parent: c3; evidence: none): Final answer: 17.
  Confidence 0.8. I had all the information I needed; my reasoning was wrong.
[Supervisor] Rejected: verified correct answer is 16.
Follow-up: No change was made; context and tools were already complete.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). First reason explicitly about WHY the recommendation was wrong and whether that cause will recur, inside the rationale field (up to 80 words). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: outcome

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Record: quant_agent produced 1 recommendation that was rejected as incorrect.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: skill

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Record: quant_agent produced 1 rejected recommendation on 'quant' tasks.

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_masked

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Claim graph for the rejected recommendation (cause fields not yet diagnosed):
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.",
   "evidence": [
    "e1",
    "e2"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.",
   "evidence": [
    "e0"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.8,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "UNKNOWN",
   "persistence": "UNKNOWN",
   "scope": "UNKNOWN",
   "resolved": "UNKNOWN"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.",
   "evidence": [
    "e1",
    "e2"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.",
   "evidence": [
    "e0"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.8,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "persistent_reasoning",
   "persistence": "persistent",
   "scope": [
    "fact",
    "multihop",
    "quant",
    "tool"
   ],
   "resolved": "no"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_parent

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.",
   "evidence": [
    "e1",
    "e2"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.",
   "evidence": [
    "e0"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.8,
   "verification": "REJECTED (correct answer differs)",
   "tool_state": "ok",
   "failure_cause": "persistent_reasoning",
   "persistence": "persistent",
   "scope": [
    "fact",
    "multihop",
    "quant",
    "tool"
   ],
   "resolved": "no"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_toolstate

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.",
   "evidence": [
    "e1",
    "e2"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c1"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.",
   "evidence": [
    "e0"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c2"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.8,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "failure_cause": "persistent_reasoning",
   "persistence": "persistent",
   "scope": [
    "fact",
    "multihop",
    "quant",
    "tool"
   ],
   "resolved": "no"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

### Condition: graph_no_persist

SYSTEM:
```
[[ROLE:supervisor]] You are the supervisor of a team of persistent LLM subagents. After a subagent's recommendation was rejected, you update how much you trust that agent for FUTURE tasks in each skill. Skills: fact, multihop, quant, tool.
```
USER:
```
Team: fact_agent (declared specialty: fact); multihop_agent (declared specialty: multihop); quant_agent (declared specialty: quant); tool_agent (declared specialty: tool)
Calibrated reliability of quant_agent BEFORE this incident (P(correct) per skill): fact=0.68, multihop=0.55, quant=0.88, tool=0.85

Cause-aware claim graph for the rejected recommendation:
{
 "task_provenance": {
  "agent_declared_specialty": "quant",
  "task_skill": "quant",
  "required_items": 3,
  "items_provided": 3,
  "retrieval_tool_state": "ok"
 },
 "claims": [
  {
   "claim_id": "c1",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Ahito, Amber, and Micah ran a total of 52 miles, with Amber running 8 miles and Micah running 3.5 times what Amber ran.",
   "evidence": [
    "e0",
    "e1",
    "e2"
   ],
   "confidence": null,
   "verification": "not independently verified",
   "parent_claim_id": null,
   "tool_state": "ok"
  },
  {
   "claim_id": "c2",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "First, calculate how many miles Micah ran. Since Amber ran 8 miles, Micah ran 3.5 times that amount: 3.5 * 8 = 28 miles.",
   "evidence": [
    "e1",
    "e2"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c1",
   "tool_state": "ok"
  },
  {
   "claim_id": "c3",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Now, we can find out how many miles Ahito ran by subtracting the miles run by Amber and Micah from the total miles. Total miles = 52, Amber's miles = 8, Micah's miles = 28. Therefore, Ahito's miles = 52 - (8 + 28) = 52 - 36 = 16 miles.",
   "evidence": [
    "e0"
   ],
   "confidence": 0.8,
   "verification": "not independently verified",
   "parent_claim_id": "c2",
   "tool_state": "ok"
  },
  {
   "claim_id": "c4",
   "agent": "quant_agent",
   "skill": "quant",
   "claim_text": "Final answer: 17.",
   "evidence": [],
   "confidence": 0.8,
   "verification": "REJECTED (correct answer differs)",
   "parent_claim_id": "c3",
   "tool_state": "ok",
   "failure_cause": "persistent_reasoning"
  }
 ]
}

Decide how this incident changes the probability that the agent will answer FUTURE tasks correctly, per skill. delta_trust[skill] is the change in that probability, between -1.0 and +0.5 (0 = no change). Reply with ONLY a JSON object: {"cause": one of ["missing_context","tool_failure","out_of_specialty","persistent_reasoning"], "delta_trust": {"fact": x, "multihop": x, "quant": x, "tool": x}, "rationale": "<=40 words"}
```

