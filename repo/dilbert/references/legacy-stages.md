# Numbered RPI/recon compatibility through /dilbert

The original `dilbert-kit (4) (1).zip` was inspected. Its useful stage contracts are
consolidated below, not restored as sixteen competing slash commands. The router must
recognize `/dilbert <old-stage-name> <arguments>` as well as the equivalent plain-English
request. These are request forms inside the real `/dilbert` command, not additional
OpenCode commands or a script engine. Load only the referenced procedure and needed
artifacts. Use native Task for specialists, never a printed slash command as execution.

IDs/SYSTEM names must be safe path components (1-80 letters, numbers, hyphens, underscores,
starting with a letter or number). Treat a repo path, subsystem, or Git ref as data, not
interpolated shell code. A specified stage file must resolve inside thoughts/<ID>/;
reject traversal or symlink escapes rather than reading an unintended target.

## Ticket stages

All artifact paths below are relative to `thoughts/<ID>/`. Preserve existing sections,
IDs, oracle answers and unrelated content. The original explain contract is **<ID>
<file>**, not just <ID>; the fixed point for review is a commit/branch the work started
from. Round must be 1 or 2; phase must identify one phase in the actual plan. Missing
or invalid arguments require one focused clarification, not guessed inputs.

| Original stage / arguments after /dilbert | Inputs | Behavior and output |
|---|---|---|
| `rpi-research <ID>` | 00-intake.md and affected sources | planning.md research procedure; save 01-research.md with flows, F/S/K evidence, consumers, scope gaps; no application edits or unsolicited plan |
| `rpi-questions <ID>` | 01-research.md and existing 02-questionnaire.md | oracle.md; update 02-questionnaire.md with evidence, consequences, options/recommendation, owner and answer/source; retain answers, never send or infer approval from silence |
| `rpi-scenario-check <ID>` | 01-research.md, answered 02-questionnaire.md, 03-scenarios.md | planning.md four consistency checks; findings with Q/SC/F/S/K IDs in chat, no rewrite unless requested |
| `rpi-plan <ID>` | 01-research.md and accepted 03-scenarios.md | planning.md; save 04-plan.md with seams, criteria/step/check mapping, phased checkpoints, assumptions/owners, explain-back; no application edits |
| `rpi-explain <ID> <file>` | Named stage file; existing CONTEXT.md vocabulary when relevant | planning.md explain-back; inputs, transformations, outputs, effects, consumers and real uncertainties in chat; no code/file names in stakeholder explanation, no automatic save |
| `rpi-plan-review <ID> <round>` | Round 1: 03-scenarios.md + 04-plan.md; round 2: 01-research.md + 04-plan.md | planning.md round 1 coverage or round 2 evidence/assumptions and at most three step-specific objections; findings only unless saving requested |
| `rpi-implement <ID> <phase>` | 04-plan.md and accepted 03-scenarios.md; existing 05-implement.md | implementation.md; implement only named phase through appropriate writer; record scenario/check results, baseline, observed checkpoints, deviations and next action in 05-implement.md; stop before further phases |
| `rpi-review <ID> <fixed-point>` | Accepted 03-scenarios.md and resolved Git base/HEAD | review.md; preserve original merge-base-to-HEAD commit review, separate Spec/Standards results in chat; report excluded local work, no automatic save |
| `rpi-review <ID> --working-tree` | Accepted 03-scenarios.md and current index/disk/new files | review.md; explicit local alternative covering staged, unstaged and relevant new files; no commit necessary |

For new scenarios, `/dilbert Draft acceptance scenarios for <ID>` uses planning.md and
the current oracle decisions; save in the existing 03-scenarios.md for a numbered ticket
or the compact note for ordinary work. Drafted scenarios are not automatically approved.
`/dilbert Close <ID>` uses continuity.md and updates 06-closure.md for a numbered ticket.
No new numbered scaffold is required to resume. The old 05 template required recording
phase results even though its slash command emphasized a diff; the consolidated contract
makes that checkpoint explicit without requiring immutable test code or universal green.

## Architecture stages

All paths are relative to `thoughts/arch-<SYSTEM>/`. Use architecture.md. A0-intent.md
holds purpose, consumers, scope, qualities, constraints and oracle confirmation; help
establish missing intent without demanding five ranked qualities or speculative changes.

| Original stage / arguments after /dilbert | Inputs | Behavior and saved output |
|---|---|---|
| `rpi-arch-claimed <SYSTEM>` | A0-intent.md + declared documents/diagrams | A1-claimed.md: components, flows/guarantees, decisions, non-goals, source/section/date; claims only, no code-based corrections |
| `rpi-arch-actual <SYSTEM>` | A0-intent.md + relevant source/config/observations | A2-actual.md: components, edges, triggers, state/config/secrets locations (not values), evidence scope/unknowns; no claimed-versus-actual comparison in this stage |
| `rpi-arch-drift <SYSTEM>` | A1-claimed.md + A2-actual.md | A3-drift.md: evidence-linked comparison, MATCH / MISMATCH / UNDOCUMENTED / NOT_VERIFIED; summaries including zero, no remediation or invented absence |
| `rpi-arch-scenario <SYSTEM> <quality-number>` | Selected owner-confirmed quality section in A4-quality-scenarios.md + A2-actual.md and decisive evidence | Update only that quality's trace results in A4-quality-scenarios.md; handled/partial/not handled/unverified with scenario evidence; preserve other qualities |
| `rpi-arch-report <SYSTEM>` | A0-intent.md + A3-drift.md + A4-quality-scenarios.md | A5-risks-and-report.md: traceable risks, quality impact, supported tradeoffs, justified strengths and open questions; no quotas or automatic HTML/atlas/publication |

A new `/dilbert Architecture review ...` uses compact A0-A5 report sections instead.
`/dilbert Draft quality scenarios for <SYSTEM>` uses A0 priorities and records the
owner's confirmation separately from proposed cases. Do not trace an unconfirmed quality
as an approved acceptance evaluation. Lack of confirmation can be the reported blocker.
If an independent A2 is requested, use an unexposed context with A0 and sources only;
if already exposed to A1, disclose it and arrange a scoped fresh pass. Do not require
fresh sessions for every stage or claim that an ordinary routed child is independent.

## Recon stages

Use recon.md for the full procedure and output contents.

| Original stage / arguments after /dilbert | Input and output contract |
|---|---|
| `recon-map <repo-path>` | Explicit graph build/refresh on that path; defaults to current repository when omitted. Verify installed invocation and queryability; return build/query evidence in chat. Save recon/00-graph.md only if requested. This argument is a repository path, not a ticket ID. |
| `recon-orient <ID>` | Bounded repository inventory with source evidence; save thoughts/<ID>/recon/01-inventory.md through a worker. A graph is optional. |
| `recon-trace <ID> <subsystem>` | Inventory + decisive source/graph; update only that subsystem in thoughts/<ID>/recon/02-flows.md with hops, seams, dependencies and unknowns. |

`/dilbert Synthesize recon for <ID>` saves recon/03-architecture.md from inventory/flows.
`/dilbert Contrast recon for <ID> with <declared-source>` saves recon/04-drift.md from
actual notes versus the named declared evidence. These replace the original scaffold's
references to nonexistent recon-arch/recon-drift commands. Never pass an ID as repo-path.

## Continuity and authorization

Read numbered artifacts directly; do not demand task.md, recreate completed stages,
copy answers, or treat empty scaffolds/old gate checkboxes as acceptance. Use continuity.md
when notes disagree or evidence is stale. An absent legacy mode field does not waive
real acceptance decisions. Current policy removes old numeric quotas, silence defaults,
mandatory sessions/worktrees/commits, and immutable-test rules, but preserves valid prior
oracle decisions. Flag answers recorded only as defaulted for confirmation if they matter;
do not erase them or treat them as approved solely because an old deadline passed.

Explicit artifact-producing stage requests authorize the documented local artifact via
native approvals. Findings-only stages do not authorize a save unless requested.
Research/planning do not authorize application changes; implementation does not authorize
external execution, publishing, or additional phases. A denied write ends that action.
