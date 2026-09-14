# Supervised implementation

Before changing anything: confirm scope/acceptance criteria, inspect git status if
Git exists, and preserve the user's prior work. Capture relevant checks as a baseline
when feasible. Do not require an already broken repository to become entirely green.
Do not execute tests that mutate real services without confirming environment and
authorization.

Bugs: reuse or build a reproduction that captures the symptom. For difficult bugs,
minimize the case and test hypotheses with predictions. Do not rewrite code based
only on a plausible explanation. Without a viable reproduction, document the limit
and request targeted evidence. Static investigation may continue, but do not claim
confirmed causality.

STANDARD/STRICT: a short plan of observable steps tied to acceptance criteria; use
planning.md for scenario consistency, seams, explain-back and proportional review.
QUICK: a criterion, bounded files, and verification are enough. Use existing conventions
and seams in either case. Introduce new structure only when required by scope. If a
new file is needed within scope, investigate it and update the note. Request a decision
when scope, contract, or risk changes, not for every mechanical plan adjustment.

Implement vertical slices. When a behavior test is useful and feasible, make it fail
for the right reason and verify the correction. Do not create tests that replicate
the algorithm or filler tests for documentation/configuration. Use native checks.
Fixtures and tests may be repaired/refactored without weakening their meaning;
changing acceptance requires an oracle decision. Propose incidental out-of-scope
refactoring separately. Explain small adjustments necessary for correctness.

Run relevant checks per phase. Run broader checks at the end when justified by impact,
availability, and cost. Report command, result, and tested revision:
PASS / FAIL_NEW / FAIL_PREEXISTING / BLOCKED / NOT_RUN. Do not label a failure
preexisting without a baseline or other evidence. Do not fix unrelated failures to
get green. If a decisive check is missing, report "implemented, verification blocked".
Remove temporary instrumentation from the change and review the actual diff before closing.

Infrastructure: identify the actual platform, provisioning/deployment tools, target
environments, operating systems, and supported versions. Clarify ambiguous deliverables
rather than assuming a tool or package format. Use applicable native syntax, lint,
validation, plan, or preview checks, then test behavior in an authorized environment.
When idempotence is expected, a second run should produce no unexpected changes.
A preview or dry-run is partial evidence: inspect its tool-specific limitations,
overrides, and possible side effects before execution. It does not authorize applying
changes. Limit/redact sensitive output. Present the exact remote target, action,
and recovery procedure before asking for approval.

Destructive Git operations/resets, deleting the only copy, force pushes, migrations,
and deployments require explicit approval. Harness permissions remain in effect even
when a plan is approved. If a tool is denied, do not seek an alternative channel.

Both dilbert-worker and dilbert-worker-strong follow this reference and WORKFLOW.md.
One active writer at a time; no nested delegation. Return missing oracle decisions to
the router. Save-only requests authorize only the named artifact. Verify saved content
and report its path. On provider failure, stop and report partial work; the router
coordinates manual resume after inspection, never an automatic account retry.


For an explicit phase request, validate that phase against the existing plan, read its
accepted scenarios, implement only that slice and stop at its checkpoint. Expected
values must come from accepted examples/criteria, not mirror the algorithm. Record
actual phase checks, observed behavior, plan deviations and next action in the existing
05-implement.md (or compact note). Do not assert a human ran a check without evidence.
Changes to test structure/fixtures are allowed when semantics remain intact; weakening
acceptance requires an oracle decision. Do not commit or launch extra reviews merely
because an imported implement/tdd skill would do so. Use continuity.md for closure.
