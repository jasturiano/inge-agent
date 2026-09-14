# Existing tasks, skills and installation upgrades

[Back to README](../README.md) · [Legacy task drill](DRILLS.md#drill-k-preserve-a-numbered-ticket-and-reuse-evidence)

Dilbert preserves the original RPI/recon engineering capabilities through one entry point.
It does not require the original command files, empty scaffolds or archives at runtime.
Existing numbered artifacts remain usable in place: no task.md prerequisite, repeated
questionnaire, or recreation of completed work.

## Capability map

| Existing capability | Current procedure |
|---|---|
| Intake, research, consumers, Stated/Implied/Unknown | [planning.md](../repo/dilbert/references/planning.md) |
| Questionnaire and oracle decisions | [oracle.md](../repo/dilbert/references/oracle.md) |
| Acceptance scenarios, consistency checks, plan, explain-back and plan review | [planning.md](../repo/dilbert/references/planning.md) |
| Supervised phase implementation and baseline-aware verification | [implementation.md](../repo/dilbert/references/implementation.md) |
| Actual-diff review with separate Spec/Standards findings | [review.md](../repo/dilbert/references/review.md) |
| Closure, resumable state, glossary/decision reuse | [continuity.md](../repo/dilbert/references/continuity.md) |
| A0–A5 intent, claimed/actual evidence, drift, quality scenarios and justified risks | [architecture.md](../repo/dilbert/references/architecture.md) |
| Optional inventory, tracing, synthesis, graph operations and cross-repo boundaries | [recon.md](../repo/dilbert/references/recon.md) |
| Requested worktree context transfer, delivery and integration | [worktrees.md](../repo/dilbert/references/worktrees.md) |

## Existing stage requests

The router recognizes old stage names **inside** `/dilbert`:

```text
/dilbert rpi-research BILL-142
/dilbert rpi-explain BILL-142 04-plan.md
/dilbert rpi-plan-review BILL-142 2
/dilbert rpi-implement BILL-142 1
/dilbert rpi-review BILL-142 --working-tree
/dilbert rpi-review BILL-142 main
/dilbert recon-trace BILL-142 billing
```

The [complete stage table](../repo/dilbert/references/legacy-stages.md) defines all sixteen
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
Discover their actual names, paths, permissions and supporting resources in OpenCode's
native skill catalog; do not reinstall upstream copies or mass-move files.

The original archive stored skill copies at `.agents/<name>/SKILL.md`. Current
[OpenCode documentation](https://opencode.ai/docs/skills/) lists
`.agents/skills/<name>/SKILL.md`, `.opencode/skills/<name>/SKILL.md`, and compatible
project/global locations. Archive presence alone does not prove discovery. Verify your
installed version before deciding a move is needed; preserve custom content and avoid
duplicate names. Original copies remain available in the optional local recovery archive.

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
