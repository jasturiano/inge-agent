# Verify observable behavior

Choose checks from acceptance criteria and affected contracts. Reuse project tooling
and existing recipes. Run relevant baselines when feasible; preserve evidence for
PASS / FAIL_NEW / FAIL_PREEXISTING / BLOCKED / NOT_RUN. A claim that a check passed
must name the observed result and tested state. Tests passing does not prove the
ticket's intent if they do not exercise its criteria.

When a project repeatedly needs application-level proof, propose or maintain a
small repository-local verification recipe under its existing conventions. Creating
one requires authorized documentation/script work. It should specify:

1. Launch: exact command, prerequisites, safe environment and readiness signal.
2. Health: confirm the expected instance/build and access before driving it.
3. Exercise: a real user/API/CLI path, accepted input and expected outcome; include
   relevant negative cases and externally observable side effects.
4. Evidence: commands/actions, resulting state, timestamps/revision and retained
   artifacts. Avoid secrets and unnecessary private payloads.
5. Cleanup: stop only instances created by this run and remove their scratch state;
   preserve proof artifacts. Account for failures and partially started instances.

Run a new recipe end-to-end before calling it verified, including cleanup and evidence
retention. A recipe not executed is a draft. Check what a dry-run actually skips.
Do not start competing instances against shared data. After surprising behavior,
re-establish health before further driving. Update recipes only against observed
changes: distinguish stale documentation, a harness gap and a product regression.
Do not rewrite expected behavior merely to make a broken application pass.

For simple edits, native checks and inspection can suffice. Do not generate a
verification framework, feature inventory, or extra tests for every task.
