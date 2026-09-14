# Validation

[Back to README](../README.md) · [Live behavior checklist](../validation/BEHAVIOR.md)

Run from the distribution root:

```bash
python3 validation/validate.py
```

Requirements: Python 3, Git, and Ruby's standard YAML parser. The tests do not need
OpenCode, providers, the optional `backup/` folder, or a Git checkout of Dilbert.
Temporary Git commits/worktrees exist only inside disposable test fixtures.

## Latest local results

2026-09-12, final cleanup verification: **12 tests passed**. The suite was also
run from a disposable source-only copy with no backup archives. This is a fresh run
against the cleaned layout, not a reused historical assertion count.

| Area | Deterministic checks |
|---|---|
| Roles and permissions | Exactly five roles; reader edit deny, writer edit ask, all Bash ask; router's ordered four-role Task allowlist and child Task deny |
| Models | One active model and requested commented alternative per agent; no guessed Terra pin |
| Commands | Main command plus four aliases, all target dilbert with arguments and no model overrides; no duplicate singular directories |
| Documentation | Shared reference paths and local Markdown links, including README drill anchors, resolve |
| Legacy capability coverage | All sixteen stage names, important argument contracts and artifact paths remain documented; static contract checks only |
| Source hygiene | Backups, ZIPs, generated results, caches and macOS clutter ignored; actual distribution sources stay visible to Git |
| Note creation | Correct installed repository from another cwd and paths with spaces; valid maximum-length ID; no Git initialization |
| Artifact continuity | Creating a compact note preserves existing answered questionnaire, scenarios, phase and recon notes; duplicate notes cannot overwrite decisions |
| Path safety | Unsafe IDs, traversal, and symlink escapes/collisions rejected without clobbering external files |
| Actual-diff scope | Staged, unstaged and new work distinguished from committed changes, including edits that cancel in the combined HEAD diff |
| Unborn Git repository | Staged, unstaged and new files inspectable without HEAD |
| Linked worktree excludes | Exact README rules use the resolved exclude file, preserve prior rules and unrelated commands, and do not assume notes transferred through Git |

The cleanup also verified the retained archives' integrity and compared active agent,
command, workflow, profile and helper files against the pre-cleanup snapshot: their
contents and permission configuration were unchanged. Historical reports and patches
are recovery data inside backup/pre-cleanup.zip, not inputs to the current test suite.

## Static checks versus live behavior

These tests validate configuration, procedures and deterministic helper/Git behavior.
They do not prove that an LLM asks the right question, preserves every section, obeys
phase boundaries, or that a particular OpenCode build enforces child approvals.

OpenCode was unavailable in the validation environment. Installed discovery paths,
effective merged permissions, provider availability, parent/child models, skill discovery,
rejected-edit behavior and manual quota recovery remain unverified at runtime. The original
model IDs were inspected previously; no provider calls were made to validate availability.

Use [Drill I](DRILLS.md#drill-i-routing-and-rejected-edit-smoke-test) and the live behavior
checklist in a disposable repository with your actual installation. Inspect effective
restrictions before testing. Do not trigger production operations or spend across accounts
merely to claim a passed quota test. No global installation, production query, deployment,
or real application integration was performed during this cleanup.
