# Questionnaire and oracle

1. Extract what the ticket, conversation, contracts, and examples already confirm.
   Cite the source. Do not ask again unless something changed or conflicts.
2. Investigate code and documents to separate technical uncertainty from intent.
   Greenfield may require researching options before presenting a decision.
3. Ask only about unresolved decisions affecting scope, acceptance, cost, operations,
   or responsibility. Start with the blocker that unlocks the most useful work.
4. Present viable options, consequences, and a recommendation when supported.
   Allow another answer; do not force a false dichotomy. A real example and behavior
   that must remain unchanged are useful prompts, not mandatory quotas.
5. Record the answer, decision owner, and source. A recommendation is NOT approval.
   Silence does not approve defaults. Use a default only if the person explicitly
   authorized that policy for this decision and it remains applicable.

Compact format in task.md, or questionnaire.md if intended for a separate recipient:

| Pending decision | Evidence/why it matters | Options and recommendation | Owner | Answer/source |
|---|---|---|---|---|

Classify unknowns as blocking, investigable, or reversible details. Do not substitute
a default percentage or count of open questions for impact. Never send a questionnaire
to someone else without authorization.

Turn answers into observable acceptance criteria. Use Given/When/Then when helpful;
add negative cases and invariants according to risk, without a fixed count. In STRICT,
confirm material scenarios with the oracle before planning. In STANDARD, a ticket
with sufficient acceptance criteria can serve that purpose. QUICK needs a brief
criterion, not the full workflow.

Greenfield example: introducing a service requires understanding its purpose, POC/production scope, allowed infrastructure, identity/secrets,
maintenance, and acceptance demonstration. Do not assume cloud/self-hosted, high
availability, or scale.
Brownfield example: "Fix a timeout" requires checking the symptom and whether changing
retries affects duplicate processing or consumer contracts.

In ALIGN, disagreement can be the deliverable: present competing interpretations and
pending decisions without choosing a winner yourself. If the user only asks to explore,
do not turn that exploration into approved implementation.

Return proposed questionnaires/answers to the router. When persistence is requested,
the router delegates the specified artifact to a worker with native edit approval;
no primary-agent switch is required. Preserve answered content and oracle ownership.
