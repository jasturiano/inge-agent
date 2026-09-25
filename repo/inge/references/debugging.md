# Diagnose with a useful feedback loop

Bound the exact symptom, environment and expected behavior. Read relevant code,
contracts and history. Prefer an existing reproduction. Otherwise identify a safe
test, HTTP/CLI fixture, captured-input replay, differential run, bisection harness,
or browser flow that detects this symptom. Creating a harness or instrumentation
is a write: it needs the user's scope and the adapter's permitted writer.

Run the reproduction before claiming it works. Tighten its signal, setup time and
determinism. For intermittent failures, record attempts, failures and conditions;
absence in a small sample is not proof of correction. Redact secrets before showing
commands, traces, headers or outputs. Preserve evidence needed to repeat the run.

Minimize while retaining the original scenario. Rank plausible hypotheses without
a numeric quota; give each a falsifiable prediction. Change one relevant variable
per experiment. Prefer a debugger or targeted, uniquely tagged instrumentation.
For performance, measure a baseline and compare under equivalent conditions.
After two attempts without new evidence, change the experiment or report the blocker.

When no reproduction is possible, static investigation may continue. Label causal
claims as hypotheses; list attempted checks and the specific missing evidence.
Ask for targeted redacted artifacts or access, not an unrestricted environment dump.
Never instrument production merely because local investigation is difficult.

For an authorized fix, use implementation.md. Test at the interface that exercises
the actual failure, not a nearby function that cannot reveal it. Expected outcomes
come from accepted behavior. Re-run both minimized and original scenarios, inspect
affected consumers, remove temporary instrumentation, and retain relevant evidence.
If no useful regression seam exists, report that gap instead of creating a filler test.
