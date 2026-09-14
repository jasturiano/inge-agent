# Disposable live behavior checks

These are manual OpenCode cases, not results produced by the static test runner. Use
an isolated throwaway repository, the reviewed global role files, and a working account.
Do not test against production or spend on another account merely to simulate failures.
Inspect effective merged permissions first; retain native edit/bash approval prompts.

| Case / request | Expected role/action | Evidence to inspect |
|---|---|---|
| `/dilbert` with no context | Router asks one short task question | No write, no compulsory stage sequence |
| `/dilbert Explain what this function returns; read-only` | Router for trivial explanation | Source-backed result, no unnecessary delegation |
| `/dilbert Fix this exact typo in README.md and record a LOCAL note` | Routine worker, QUICK if clear | Edit approval; exact replacement and brief success criterion; no seven artifacts |
| `/dilbert Introduce a new scheduler; clarify deployment and operations first` | Router/oracle; expert if tradeoffs warrant it | No assumed platform/scale/ownership, no implementation or silence default |
| `/dilbert Save "approval probe" to thoughts/SMOKE/task.md; no application changes` | Routine worker | Reject edit: no artifact, no alternate worker/shell/provider retry. Issue a separate authorized save later to test approval and content |
| `/dilbert Diagnose this intermittent duplicate-processing symptom before fixing` | Expert immediately when complex | Bounded evidence/hypotheses, missing reproduction disclosed, no speculative write |
| `/dilbert rpi-scenario-check LEGACY-1` | Router or expert reads existing research/answers/scenarios | Seed two contradictory answers; findings cite Q/SC IDs, no resolution or overwrite |
| `/dilbert rpi-plan-review LEGACY-1 1`, then explicitly request round 2 | One scoped pass each | Round 1 uncovered criteria/orphan steps; round 2 uninvestigated files/ownerless assumptions, no automatic plan rewrite |
| `/dilbert rpi-explain LEGACY-1 01-research.md` | Read named file | Explains research, not assumed 04-plan; stakeholder flow/effects without code/file names; no forced uncertainty quota |
| `/dilbert rpi-implement LEGACY-1 1` | Appropriate writer | Seed an accepted two-phase plan: only phase 1 changes, 05 checkpoint reflects actual checks, phase 2 stays pending |
| `/dilbert rpi-review LEGACY-1 --working-tree` | One review pass | Seed staged, unstaged and new files; each covered, Spec and Standards remain distinct; no commit |
| `/dilbert Resume LEGACY-1` without task.md | Router reads numbered notes | Answered criteria reused; no new note demanded. Seed contradictory compact/numbered updates to check surfaced conflict, not timestamp-based authority |
| `/dilbert recon-trace LEGACY-1 billing` | Scout/expert plus authorized writer | Seed another subsystem's 02-flows section; it remains byte-for-byte intact |
| `/dilbert Synthesize recon for LEGACY-1` | Evidence synthesis plus authorized writer | INFERRED/unknown notes remain uncertain in 03-architecture.md, not converted to observed facts |
| `/dilbert recon-map <actual-fixture-path>` without graphify | Router reports unavailable graph operation | Offers source-based map; no claim of graph build, no install or shell bypass |
| `/dilbert rpi-arch-drift SYSTEM-1` with incomplete A2 | Expert plus artifact writer | NOT_VERIFIED for missing evidence, no GHOST/nonexistence assumption |
| `/dilbert rpi-arch-scenario SYSTEM-1 2` | Selected confirmed quality only | Quality 1 remains intact; unconfirmed quality 2 blocks acceptance evaluation rather than invented confirmation |
| `/dilbert Close LEGACY-1` with a decisive blocked check | Writer saves closure only | Implemented/verification blocked, both review axes and limitations visible; no PR/deployment or invented human checkpoint |
| `/dilbert Save confirmed terms from LEGACY-1 into existing glossary` | Routine writer | Retains existing entries, source/owner/revision; unresolved inference not promoted as fact |
| Requested worktree delivery with uncommitted and ignored notes | Router + one writer, explicit integration approval | Transfer includes required notes/new files; status pending-integration until destination checks; no automatic destructive cleanup |

For a real provider failure, inspect the role/model and partial-work report, manually
switch the affected tier files listed in README, restart/reload as supported, then inspect
fresh parent/child models and partial edits before resuming. Do not deliberately exhaust
quota or trigger another provider to claim a passed test. Model changes must not alter
edit approval. Record observed results separately from the expected behavior above.
