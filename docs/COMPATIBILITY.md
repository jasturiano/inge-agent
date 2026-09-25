# Existing tasks, skills and installation upgrades

[Back to README](../README.md) · [Legacy task drill](DRILLS.md#drill-k-preserve-a-numbered-ticket-and-reuse-evidence)

Inge preserves the original RPI/recon engineering capabilities through one entry point.
It does not require the original command files, empty scaffolds or archives at runtime.
Existing numbered artifacts remain usable in place: no task.md prerequisite, repeated
questionnaire, or recreation of completed work.

## Capability map

| Existing capability | Current procedure |
|---|---|
| Intake, research, consumers, Stated/Implied/Unknown | [planning.md](../repo/inge/references/planning.md) |
| Questionnaire and oracle decisions | [oracle.md](../repo/inge/references/oracle.md) |
| Acceptance scenarios, consistency checks, plan, explain-back and plan review | [planning.md](../repo/inge/references/planning.md) |
| Supervised phase implementation and baseline-aware verification | [implementation.md](../repo/inge/references/implementation.md) |
| Actual-diff review with separate Spec/Standards findings | [review.md](../repo/inge/references/review.md) |
| Closure, resumable state, glossary/decision reuse | [continuity.md](../repo/inge/references/continuity.md) |
| A0–A5 intent, claimed/actual evidence, drift, quality scenarios and justified risks | [architecture.md](../repo/inge/references/architecture.md) |
| Optional inventory, tracing, synthesis, graph operations and cross-repo boundaries | [recon.md](../repo/inge/references/recon.md) |
| Requested worktree context transfer, delivery and integration | [worktrees.md](../repo/inge/references/worktrees.md) |

## Existing stage requests

The router recognizes old stage names **inside** `/inge`:

```text
/inge rpi-research BILL-142
/inge rpi-explain BILL-142 04-plan.md
/inge rpi-plan-review BILL-142 2
/inge rpi-implement BILL-142 1
/inge rpi-review BILL-142 --working-tree
/inge rpi-review BILL-142 main
/inge recon-trace BILL-142 billing
```

The [complete stage table](../repo/inge/references/legacy-stages.md) defines all sixteen
original stage inputs, outputs and arguments. These are request forms interpreted by the
router, not sixteen additional OpenCode commands or a separate execution engine.

Key contracts: explain accepts ID **and file**; implementation stops at the named phase;
plan review honors round 1 or 2; architecture scenario tracing touches only the selected
confirmed quality; recon tracing preserves other subsystems. Review accepts a commit/branch
fixed point, or `--working-tree` for staged, unstaged and relevant new files. Recon-map
accepts a repository **path**, not a ticket ID. Findings-only stages do not save unless
requested; artifact-producing stages save through a supervised worker.

Resume by reading actual notes and their evidence. Keep valid oracle decisions and IDs.
An old defaulted answer is not approved just because its deadline passed. If compact and
numbered notes conflict, surface the disagreement rather than trusting a timestamp.

## Updating an old installation

### Renaming Dilbert to inge

The repository is now `inge-agent`; the primary agent and command are `inge` and
`/inge`, never `inge-agent` or the expanded display name. Internal roles use `inge-*`.
There are no active `dilbert` aliases or fallback discovery paths.

Run `python3 scripts/check-installation.py --root /absolute/path/to/code` from the
new checkout before and after migration. It reports legacy leftovers without
deleting, moving or rewriting them; review each candidate and preserve custom content.

Install the new definitions and framework using the README. Migrate `DILBERT_HOME`
to `INGE_HOME`, shared `.dilbert` to `.inge`, and local `dilbert/PROJECT.md` to
`inge/PROJECT.md`, preserving the filled profile. Update personal launchers, instruction
pointers, excludes and JSON/JSONC overrides. Keep `thoughts/` and existing task IDs
unchanged. Do not bulk-replace historical evidence or edit recovery archives.

Once the new installation is verified, move superseded `dilbert*.md` definitions
and old framework files to a reviewed backup outside harness discovery. The checker
does not certify a complete migration: it does not parse effective configuration,
scan arbitrary shell profiles or unpack archives. It never performs cleanup itself.

### Moving to the portable shared core

Install the complete contents of repo/inge once as a shared .inge and select it
using trusted-launcher INGE_HOME or an operator-approved session path. Update the OpenCode agent and command definitions too:
old prompts still assume repository-local paths and will not discover the new core.
Install commands globally once if desired; inspect and retire duplicate local
definitions only after verification, preserving unrelated commands.

Local kits no longer win by discovery: each must be explicitly trusted. Compare custom changes,
then move only superseded framework files to a backup outside discovery when ready.
Keep each repository's inge/PROJECT.md and thoughts/ in place. A profile alone
does not shadow the shared framework. Use doctor.py to verify the selected paths.
Do not symlink thoughts or a shared project profile across repositories.

Security hardening removes implicit ancestor/local selection. Upgrade the entire kit,
including scripts/safeio.py; do not copy individual new helpers into an old kit. An
operator-selected root symlink is allowed, but internal links are rejected by helpers.
Protected operations require POSIX directory descriptors and fail closed elsewhere.
The inventory returns exit 2 for skipped links/incomplete coverage; it never removes
them. Read-only native roles now deny Bash, unknown tools default to denied, and
web/skill calls require approval. Disable auto-approval and verify effective merged
permissions before use; do not weaken existing global restrictions while upgrading.

Breaking helper change: new-task.py now requires --repo TARGET. Update personal
aliases/scripts that previously relied on the helper's installation location. This
is necessary for safe shared installations. The target must already exist; nested
Git directories resolve to their worktree root. A shared framework may be symlinked,
because its location no longer determines the task-note destination.

SOUL.md and BOOTSTRAP.md are explicit portable entry points, not magic filenames.
Other harnesses use adapters/generic.md and their own instruction-loading mechanism;
native model dispatch and permissions are not automatically translated from OpenCode.

### OpenCode configuration upgrades

First identify the installed OpenCode version, discovery paths and configuration overrides.
The distribution uses plural paths; an old archive's singular layout does not establish
what your current version supports. Avoid duplicate agent/command names across Markdown,
JSON, global and local definitions.

Back up changed files outside discovery directories, inspect custom edits and callers,
and verify the replacements before moving superseded kit-owned definitions out of discovery.
The active roles are router, scout, expert, routine writer and strong writer. A second
primary `dilbert-build`, provider-specific workers, and old recon-specific agents are not
needed by this distribution. Preserve any independent custom usage you actually have.

Do not overwrite installed AGENTS.md, provider configuration, project settings or skills.
Older instructions may require universal-green checks, a fresh session per stage, automatic
worktrees/PRs, immutable test code, or numeric quotas. Reconcile only conflicting process
rules with the current workflow. Preserve no-fabrication, destructive/external-action
confirmation rules and stricter effective permissions. Silence remains non-approval;
acceptance semantics remain protected even when test structure changes.

Keep old templates/prompts as historical material if useful, not a competing source of
active policy. Never remove existing thoughts. For retained legacy kit files, append
only exact kit-owned patterns to the target's resolved local exclude file: for example,
`/dilbert_scripts/`, `/dilbert_templates/`, `/dilbert_arch-templates/`, `/dilbert_prompts/`,
`/DILBERT.md`, and the exact installed path of each retained RPI/recon command. Do not
hide all `.opencode/`, project AGENTS.md or unrelated commands.

## Skills

Preserve installed Matt Pocock/custom skills, graphify, ponytail and optional i-have-adhd.
Discover their actual names, paths, invocation permissions and supporting resources in
the active harness's catalog; do not reinstall upstream copies or mass-move files.

The original archive stored skill copies at `.agents/<name>/SKILL.md`. Current
[OpenCode documentation](https://opencode.ai/docs/skills/) lists
`.agents/skills/<name>/SKILL.md`, `.opencode/skills/<name>/SKILL.md`, and compatible
project/global locations. Archive presence alone does not prove discovery. Verify your
installed version before deciding a move is needed; preserve custom content and avoid
duplicate names. Original copies remain available in the optional local recovery archive.

The recovery archive's grill-with-docs refers to grilling, but no grilling/SKILL.md
was found there during the 2026-09-24 review. That says nothing about an independently
installed live catalog. Verify dependency availability before invoking the wrapper;
proposal-grill is not an automatic alias. The read-only doctor checks selected known
dependency edges in explicitly supplied skill directories; it cannot certify native
discovery or all supporting resources. Use the bundled oracle guideline if needed.

See [skill mapping and provenance](../repo/inge/references/skills.md) for current
integration candidates and known renames. Track exact upstream revisions for future
updates, retain adaptations, and re-run relevant behavior evaluations. Do not install
an entire upstream framework merely because one procedure is useful.

Code-review skills may assume parallel reviewers and commit-only diffs; adapt them to
selected scope and no nested delegation, or use the local reference. Implement/to-spec/
to-tickets defaults do not authorize committing or publishing. Use current graphs only
when relevant; graph builds require authorized writes. Presentation skills change delivery,
not acceptance, evidence, or approval requirements.

## Local recovery files

When retained locally, `backup/original-kit.zip` contains the original kit and custom skill
copies. `backup/pre-cleanup.zip` contains the complete polished distribution before repository
cleanup, including historical snapshots, migration notes and patches. Both are outside
agent/command discovery and excluded by this repository's `.gitignore`.

Backups are not dependencies and need not be uploaded to GitHub. The current editable
source is the repository itself; do not treat a recovery ZIP as the current release.
