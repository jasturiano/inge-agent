# Intake, research, acceptance, and planning

Use only the requested or necessary parts. QUICK needs a clear success criterion,
targeted inspection, a change, and proportionate verification; it does not need the
tables below. STANDARD/STRICT use them where uncertainty or impact warrants them.
Readers return analysis; a worker saves authorized artifacts. A stage-only request
stops at that stage. Research, questions, and plans never authorize application edits.

## Intake and targeted research

Read the request and existing decisions first. Record Stated (literal request),
Implied (inference), and Unknown (blocking intent / investigable mechanics / reversible
detail), the source/owner, scope, and consumers. The agent may help with intake; it
cannot fill an unknown with a plausible requirement. Reuse confirmed answers.

Bound research by the affected flow: input/trigger → transformations → output → side
effects. Inspect contracts, direct callers/readers/writers, tests, configuration, and
existing seams. Use current graphs for relationships, rg for names, and decisive source
for behavior. Record repository/revision and path:line (or document section/date),
observed versus inferred evidence, and explored/unexplored scope. If source is absent
in greenfield, research constraints and relevant documentation; do not invent code paths.

When useful, use F# for findings, S# for request/current-behavior disagreements, K# for
material alternatives, and Q# for decisions. Preserve IDs already in numbered notes.
Zero surprises/forks is valid. Do not manufacture uncertainty to fill a quota.

| ID | Current behavior or decision fork | Evidence and revision | Affected consumers / consequence | Unknown or next check |
|---|---|---|---|---|

Return technical unknowns for investigation and consequential intent/tradeoffs to the
oracle using `oracle.md`. A request for research alone returns findings/open decisions,
not an unsolicited implementation plan. Save in task.md when requested or in the
existing 01-research.md for an explicit legacy research stage.

## Scenarios and consistency

Translate accepted intent into observable criteria. For material behavior, use stable
AC#/SC# IDs and Given / When / Then, linked to a confirmed answer, approved ticket,
contract, or real example. Include negative/boundary and must-not-change cases according
to risk. Do not invent a scenario count or require every criterion to come from a
questionnaire when another approved source already defines it.

| Criterion ID | Given / When / Then | Acceptance source / owner | Consumer or invariant protected | Confirmation |
|---|---|---|---|---|

Before relying on scenarios in STANDARD/STRICT, perform this proportional consistency
check; an explicit scenario-check always does it. Use research, oracle answers, and
criteria, and return findings with their Q/SC/F/S/K IDs where available:

1. Which answers contradict each other?
2. Which accepted requirements lack scenarios, and which scenarios lack an acceptance
   source? Identify deliberately deferred scope rather than silently discarding it.
3. Could two engineers test a scenario differently (input, outcome, threshold, boundary)?
4. Does research contradict a scenario, especially a claim that behavior is unchanged?
   Check the affected consumers with available evidence; list unverified consumers.

For findings-only requests, do not rewrite scenarios or choose between oracle answers.
Record finding, evidence, consequence, and proposed question/check. The owner resolves
intent conflicts; recommendations remain proposals. Empty findings are valid. Previously
accepted criteria remain accepted unless new evidence or scope changes challenge them.

## Plan and explain-back

Use accepted criteria and relevant research. Prefer existing seams (public interfaces
where behavior is observable); add structure only when warranted. A plan should say:

| Phase / step | Observable change | Paths / investigated evidence | Criterion IDs | Seam and proving check |
|---|---|---|---|---|

Group nontrivial work into vertical slices with checkpoints. Expected results come
from acceptance, not calculations copied from the implementation. Record each material
assumption, evidence needed, owner, and status (open / confirmed / disproved); do not
treat an asserted default as confirmation. Investigate newly needed in-scope files and
update evidence; return scope/contract changes to the oracle. No mechanical file-count gate.

Explain back the plan as inputs → transformations → outputs → effects → downstream
consumers/risks, using the project's confirmed vocabulary. Keep the stakeholder paragraph
free of code and file names; put evidence links separately when useful. List actual
uncertainties without a quota. If the explanation contradicts accepted intent, identify
the mismatch before implementation. A standalone explanation can target any specified
stage file and returns in chat unless saving is requested; default to the plan only
when no file is supplied and that is clearly the intended subject.

## Proportional plan review

For ordinary STANDARD work, one brief check can cover both lenses. STRICT uses the
depth warranted by risk; no automatic second expert pass or mandatory new session.
When the user explicitly requests legacy round 1 or 2, honor that bounded round:

- **Round 1 — coverage:** criteria with no serving step; steps with no criterion or
  necessary supporting rationale. Cite scenario and step IDs, including scope creep.
- **Round 2 — evidence:** planned files not investigated; assumptions lacking an owner
  or resolved by assertion. Then give at most three substantive objections, each tied
  to a specific step and consequence. Do not invent objections to reach three.

Return findings, not a rewritten plan, unless changes were requested. Track dispositions
(resolved / owner decision pending / accepted limitation with source) and check only
changed findings on retry. No independent review is claimed from already exposed context.

## Alignment, decomposition, and validating someone else's work

For competing proposals, name both readings of ambiguous terms and boundaries. Use
the existing CONTEXT.md vocabulary, propose glossary additions and evidence-backed
questions, and let the oracle resolve material differences. Do not send them automatically.

For story decomposition, establish acceptance and relevant scale/operations first.
Each proposed local task cites its criteria, bounded scope, dependency/blocker, and
checkpoint. Report uncovered criteria and tasks serving none. Publishing to a tracker
is a separate authorized action, even when a skill normally publishes.

When validating an existing plan or task list, keep it as the base: check ANCHORED
(names/paths exist), DERIVED (accepted intent covers it), and ACTIONABLE (mechanism,
unknowns, verification). Mark suggested changes KEPT / ADJUSTED / ADDED / MERGED and
explain why; do not replace the author's work wholesale. Independent ground truth is
optional when needed and must be established without prior exposure if claimed.
