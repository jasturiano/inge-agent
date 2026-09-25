# Validation

[Back to README](../README.md) · [Behavior evaluations](../validation/BEHAVIOR.md)

Agent-safe static checks (no Git calls or metadata writes):

```bash
python3 validation/validate.py --policy-only
```

Human-maintainer-only full suites, run manually from the distribution root. They
initialize disposable Git repositories and may create commits/worktrees or synthetic
Git metadata. Inge must not run these under the standing no-Git-writes policy:

```bash
python3 validation/validate.py
python3 validation/test_installation_check.py
python3 validation/security_check.py
```

Requirements: Python 3, Git and Ruby's standard YAML parser. The suite makes no
provider calls and changes no installed configuration. Git commits/worktrees and
test notes exist only in disposable fixtures. Backup archives are not dependencies.

## Executed results

2026-09-25 helper follow-up: seven --policy-only checks and thirteen selected
security regression checks passed. Four new checks cover failed discovery with an
ancestor Git marker, genuine non-Git fallback, successful nested checkout resolution,
and inventory exit 2 for a skipped FIFO. Git discovery/marker responses were mocked;
no Git commands or metadata writes were performed. Existing containment, private-note,
bounded-read, timeout, diagnostic escaping and budget checks also passed. The full
Git-mutating suites were not rerun. OpenCode was not found on PATH, so live permission
and prompt-injection checks remain NOT RUN.

2026-09-25 stash exception: seven --policy-only checks passed, including approved
stash push/pop/list patterns and continued denial of commit/merge/push/pull and other
stash operations. No Git commands or live OpenCode tests were run for this update.

2026-09-24 no-Git-writes policy: seven static policy/configuration/documentation
checks passed with --policy-only. Full Git-mutating suites were not rerun. Earlier
40-test results below describe the previous hardening checkpoint, not this revision.

2026-09-24 hardening verification: **40 tests passed** (19 distribution, 7 inventory,
14 security regressions). Former attack-characterization fixtures now require safe
behavior. Live OpenCode injection/permission drills remain NOT RUN.

2026-09-24 rename verification: **19 distribution tests and 7 installation-audit
tests passed**. Active files, paths, commands, roles and discovery use `inge` only.
Cleanup-audit fixtures cover coexisting old/new agents, named legacy backups,
local and ancestor leftovers, stale environment/config/instruction references,
partial non-Git installs, redacted output and unchanged file snapshots.

2026-09-24: **18 tests passed** after the portable-core and shared-installation change.
The initial review found 11/12 passing: the source-hygiene test expected ZIP,
textClipping and validation-results exclusions absent from .gitignore. Those intended
local-artifact exclusions are now restored. The older 2026-09-12 result is historical,
not proof of the current checkout.

| Area | Deterministic coverage |
|---|---|
| OpenCode permissions | Five roles; read-only readers, approval-gated writers, four-child allowlist and no child delegation |
| Model configuration | One active provider/model identifier per role; structural checks do not certify provider availability |
| Commands and docs | Five command aliases target Inge; no command model overrides; local links/anchors and reference paths resolve |
| Legacy procedures | All sixteen stage contracts retained; static checks only |
| Shared discovery | Explicit/environment trust selection; local/nearer kits cannot replace selected core; incomplete selection errors |
| Local state | Optional local profile does not shadow shared core; note destination independent of helper installation and shell cwd |
| Worktrees and non-Git | Linked worktree targeting, explicit framework outside ancestor tree, spaces, existing non-Git directory without initialization |
| Diagnostic behavior | Read-only execution without bytecode cache, missing bundled references, known optional-skill dependency gaps and duplicate directories |
| Task helper | Explicit target required; invalid/nonexistent targets and unsafe IDs rejected; duplicate and symlink collisions do not overwrite |
| Continuity | Existing numbered artifacts and accepted answers preserved |
| Git evidence | Staged, unstaged and untracked scope; canceling diffs; unborn repository; resolved worktree excludes preserve unrelated settings |

The doctor checks filesystem state and a small curated set of skill dependency
edges. It is not a generic skill interpreter, permission validator or runtime monitor.
It reports runtime capabilities as unverified and never connects to providers.

## Runtime limitations

The [security review](SECURITY-REVIEW.md) records original findings and current
remediation status. `python3 validation/security_check.py` now requires safe behavior:
rejection/containment of the original attacks, bounded reads, controlled timeout
failures and fail-closed unsupported platforms. Passing does not prove live model
injection resistance. Older characterization tests have been replaced, not retained
as requirements for insecure behavior.

The separate installation-inventory suite checks global current/customized/changed
definitions, nested local installs, profile-only worktrees, shared frameworks,
legacy command directories, symlink traversal avoidance and source-checkout exclusion.
Fixture snapshots verify that inventory leaves file contents unchanged.

OpenCode is unavailable in this environment. Native discovery, effective merged
permissions, loaded skills, parent/child model identity, denied-edit behavior, and
quota recovery remain live checks. Existing model examples were retained without
provider probes. The generic adapter is a manual capability contract, not a tested
native integration for another harness.

The framework specifies natural skill/model announcements and handoff evidence.
No automatic dispatch-event collector or guaranteed runtime model identification
has been implemented. When runtime metadata is unavailable, the agent must label
configured/unknown identity rather than claiming confirmation.

Behavioral quality cannot be established by Markdown presence or the helper tests.
Use the comparison protocol in validation/BEHAVIOR.md: identical scenarios and
snapshots, repeat trials, compare against the plain harness and the previous baseline,
and grade scope, correctness, verification and communication from actual results.
No live behavioral scores or multi-harness equivalence are claimed.

Use [Drill I](DRILLS.md#drill-i-routing-and-rejected-edit-smoke-test) for the native
approval boundary, and the shared/capability exercises for path and fallback behavior.
No production operations, deliberate quota exhaustion or cross-account probes are
needed to establish these checks.
