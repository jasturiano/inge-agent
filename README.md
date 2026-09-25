# inge — Intelligent Godinez Engineer

`inge` (Intelligent Godinez Engineer) is a conversational engineering framework with a harness-independent core.
Describe the situation: a ticket, a vague requirement, a difficult bug, a greenfield
design, a security concern, or work to resume. Inge selects the relevant guidance
and model capability, explains important choices, and reports evidence.

OpenCode is the current native integration. Other harnesses can use the portable
instructions through a manual adapter; their discovery, delegation and model routing
must be verified separately. Inge is not a new runtime or permission sandbox.

[How it works](#how-it-works) · [Installation](#manual-installation) ·
[Examples](docs/DRILLS.md) · [Compatibility](docs/COMPATIBILITY.md) ·
[Validation](docs/VALIDATION.md) · [Behavior evaluations](validation/BEHAVIOR.md)

[Security review and remediation status](docs/SECURITY-REVIEW.md): this framework is not
a prompt-injection sandbox. Review trust and permissions before using untrusted repos.

## How it works

In OpenCode select the Inge agent, or start with:

```text
/inge I have this ticket, but its acceptance criteria are vague: [paste ticket].
```

Then converse normally. You do not need to name a skill, role, or process stage.
Optional aliases remain available: /inge-work, /inge-review, /inge-arch,
and /inge-status. Existing rpi-* and recon-* requests still work inside /inge.

| Your request | Appropriate response |
|---|---|
| “Implement this ticket…” | Inspect context and accepted criteria, plan proportionally, change and verify |
| “This ticket is vague…” | Investigate facts; ask a manageable round of consequential decisions |
| “This is greenfield; start architecture analysis” | Establish constraints and quality scenarios; compare viable designs |
| “Check beyond the happy path” | Examine relevant failure, retry, concurrency, partial-completion and recovery behavior |
| “Check the security concerns” | Inspect trust boundaries and concrete threats; distinguish confirmed and untested concerns |
| “Why was this built this way?” | Trace relevant history and decisions, separating inference from evidence |
| “Continue where we stopped” | Read saved state, check current changes and resume the authorized scope |

A read-only review produces findings. A request to fix authorizes implementation
within scope. Technical facts are investigated; consequential intent decisions go
to you or the identified owner (the “oracle”). Existing decisions remain valid unless
scope or evidence changes. No minimum questionnaire or finding count.

### Git is yours to operate

Inge edits approved source files. Its only Git mutation exception is explicitly
approved `git stash`/`git stash push` and `git stash pop` through a writer. No staging, commits,
merges, pushes, pulls, fetches, resets, rebases, branch/tag/worktree changes,
or metadata/config writes—even after a task-level approval. It may suggest commands
and a commit message, clearly marked NOT EXECUTED, for you to review and run manually.
Worktrees and integration are user-managed. Tests/builds that mutate Git are skipped.

The shipped OpenCode profile denies other direct Git commands (including read-only
ones) and direct Git metadata edits. Exact `git stash list` is approval-gated for
identifying entries. Stash clear/drop/apply/branch are not enabled. The agent must
identify affected changes and the exact entry before restoring, and stop on conflicts.
Use native file inspection or supply command output for
reviews. Command patterns cannot stop every indirect write by an approved program:
strict enforcement additionally needs filesystem/egress isolation with a narrowly
controlled stash exception, or stashing performed manually. Existing opencode.json restrictions
must not be weakened; this turn does not update your installed configuration.

QUICK is for clear bounded work; STANDARD adds a short plan and acceptance checks;
STRICT adds depth for sensitive contracts, permissions, data and broad impact.
Process depth and model capability are separate: a small hard bug may need strong
reasoning. QUICK edits need no task note unless requested.

### Transparent skill and model routing

At substantive entry, specialist dispatch and important changes of approach, expect:

> “I'm using the debugging guideline with the current session model to reproduce
> the duplicate processing; its model identifier isn't exposed here.”

> “I'm sending the architecture analysis to the expert, configured as MODEL, to
> compare recovery options. Its runtime model is not yet confirmed.”

Actual model names replace MODEL only when supported by configuration or runtime
metadata. Inge distinguishes skills from bundled guidelines, configured from
runtime-confirmed models, and intended from successful dispatch. Loading a skill
does not change a model. Missing optional skills fall back to local guidance.

Announcements are natural, brief, and not repeated for every tool call. Important
routing facts can be saved with authorized task state. There is no automatic
telemetry collector or guarantee that a harness exposes runtime model identity.

## Repository structure

```text
opencode_global/agents/         Native OpenCode roles and configured model IDs
repo/.opencode/commands/        Command sources, installable globally or locally
repo/inge/
  BOOTSTRAP.md                 Framework/repository discovery contract
  SOUL.md                      Identity, judgment and communication
  WORKFLOW.md                  Intent routing and shared engineering policy
  PROJECT.md                   Optional repository-profile template
  adapters/                    OpenCode mapping and generic integration contract
  references/                  On-demand engineering procedures and skill mapping
  templates/task.md            Compact task state with routing evidence
  scripts/                     Path resolver, read-only doctor and note helper
docs/                          Installation compatibility, drills and validation
validation/                    Deterministic tests and behavioral evaluation cases
backup/                        Optional ignored recovery archives
```

The core contains no provider model pins. OpenCode agent frontmatter is authoritative
for its configured models and permissions. External skills from Pocock/pstack are
optional integrations, not bundled dependencies. See
[skill selection and provenance](repo/inge/references/skills.md).

## Manual installation

### Shared installation recommended

Install reusable files once above your projects. The parent folder can have any name,
and repositories can be grouped at any depth:

```text
code/
  .inge/                    Contents of repo/inge/
  project-a/
    backend/
      inge/PROJECT.md       Optional local profile, not another full kit
      thoughts/                This checkout's task notes
    frontend/
  project-b/
    service/
```

Select this shared .inge once in a trusted launcher using INGE_HOME, or explicitly
approve its absolute path in the session. It then serves all your projects. Local
or nearer ancestor kits cannot silently replace it. There is no automatic trust
inheritance above a Git root; folder discovery alone is only an inventory hint.

1. Identify your effective OpenCode configuration directory and version. Account
   for XDG, OPENCODE_CONFIG_DIR, local overrides and managed permissions. Verify
   supported discovery with the [OpenCode documentation](https://opencode.ai/docs/config/).
2. Inspect existing same-named agents/commands and custom restrictions. Back up any
   replacements outside discovery directories. Agent permissions may override
   global rules: merge mandatory restrictions rather than weakening them.
3. From this distribution's root, copy to your reviewed targets:

```bash
inge_global="/absolute/path/to/resolved/opencode"
inge_shared="/absolute/path/to/code/.inge"

mkdir -p "$inge_global/agents" "$inge_global/commands" "$inge_shared"
cp -i opencode_global/agents/*.md "$inge_global/agents/"
cp -i repo/.opencode/commands/*.md "$inge_global/commands/"
cp -Ri repo/inge/. "$inge_shared/"
export INGE_HOME="$inge_shared"
```

For a new installation the standard global directory is ~/.config/opencode.
Commands are supported globally; avoid installing the same names both globally and
locally. Copy prompts are not configuration merges. On upgrades, compare modified
files first and preserve existing project profiles and thoughts.

4. Verify discovery for a target repository:

```bash
python3 "$inge_shared/scripts/doctor.py" --repo "/absolute/path/to/code/project-a/backend"
```

Doctor prints the resolved repository, framework, optional profile and note location.
It makes no provider calls or writes. A successful result does not prove runtime
command/skill discovery, permissions or model availability.

5. Restart OpenCode inside that target. Select Inge and ask:

```text
Locate your framework and task-note template. Explain which guideline and model
you are using. Read-only; do not save anything.
```

Run the routing/denied-edit drill in a disposable repository before normal use.

### Discovery and explicit paths

To inventory existing installations without changing them, run from this source
checkout (the checker needs its reference agent, command and framework files):

```bash
python3 scripts/check-installation.py --root "/absolute/path/to/code"
```

It reports global OpenCode agents/commands, local frameworks and profiles in nested
repos/worktrees, and shared .inge directories. Repeat --root for other project
folders. It checks the XDG/default global config directory and OPENCODE_CONFIG_DIR;
use --opencode-dir PATH (repeatable) to inspect explicit locations instead.

Example messages include “Inge is installed locally in this repo”, “Global
OpenCode agents is up to date with this checkout”, and “out of date or customized”.
Comparison is against this checkout, not a fetched upstream release. Changed agent
model/permission frontmatter alone is reported as customization; local PROJECT.md
is excluded from framework freshness checks. File contents and credentials are not
printed. JSON/JSONC and managed overrides are not evaluated, so absence of Markdown
definitions is not proof that no runtime agent exists.

The checker also acts as a **read-only cleanup audit** for the rename: it flags old
`dilbert`/`.dilbert` folders, legacy kit files, old agent/command definitions and
their named backups, `DILBERT_HOME`, and old-name references in known instruction,
exclude and OpenCode configuration files. Only paths and line numbers are printed,
never matching contents. A match is a review candidate, not permission to delete it.
It checks ancestor `.dilbert` locations even when scanning one nested repository.
It does not scan arbitrary shell profiles, unpack archives or rewrite task history.
See [rename migration](docs/COMPATIBILITY.md#renaming-dilbert-to-inge) before retiring
old installations. The old command/environment variable is not an alias for inge.

The checker only reads files. It skips dependency/build folders and directory
symlinks during traversal, identifies the source checkout separately, and does not
invoke OpenCode or Git. Exit 0 means the inventory completed, even if installations
differ; exit 2 indicates invalid input or a reported inspection error.

Unexpected symlinks and special files are reported without reading their targets;
skipped links make coverage incomplete (exit 2). Explicit scan/config roots may be
approved symlinks and resolve once. Reads are capped at 1 MiB per file, traversal at
10,000 inspected entries and 30 seconds of cooperative work. A stalled kernel I/O
call on a hostile mount is not interruptible by that deadline. Diagnostics and
note creation require POSIX no-follow directory descriptors (macOS/Linux); other
platforms fail closed. Use local trusted storage and keep helpers updated together.

Read-only OpenCode roles deny Bash. Writers retain supervised edits/Bash; unknown
tools default to denied, and search/web/skills require native approval. Keep auto mode
off. Review-only shell checks need supplied evidence or separately authorized execution;
never route a denied command to another role. See the [adapter](repo/inge/adapters/opencode.md).

Selection requires an operator-approved explicit framework argument/session path
or INGE_HOME from a trusted launcher (explicit path wins). There is no implicit
local/ancestor fallback. A local profile does not grant trust or shadow the kit.
A selected incomplete kit fails visibly; references from installations are not mixed.
Keep the selected installation operator-owned and review upgrades. Path approval
does not authenticate future edits. Never run helpers from an unreviewed clone.

To select a shared framework anywhere, set INGE_HOME in the environment
that launches the harness, or supply its absolute path in the session:

```bash
export INGE_HOME="/absolute/path/to/shared/inge"
```

GUI applications may not inherit terminal environment variables; confirm the path
inside the session. Framework discovery never changes the target repository.

For diagnostics of explicitly selected external skill directories:

```bash
python3 "$inge_shared/scripts/doctor.py" --repo "/absolute/path/to/repository" --skills-dir "/absolute/path/to/skills"
```

Repeat --skills-dir for multiple catalogs. The doctor flags duplicate directory
names and selected known dependency gaps, not arbitrary semantic dependencies or
native harness discovery. No skills are installed or updated.

### Project settings and task state

Optionally copy the PROJECT.md template into the target's inge/PROJECT.md and
fill only stable, useful facts. Existing project instructions remain authoritative
within their scope. Do not store a project's settings in the shared framework.

To create a blank note explicitly:

```bash
python3 "$inge_shared/scripts/new-task.py" BILL-142 --repo "/absolute/path/to/repository"
```

--repo is required, even for legacy local installations. Within Git it resolves
to the current checkout/worktree root; a non-Git directory must already exist.
The helper never infers a note destination from its installation path. It refuses
invalid IDs, duplicate files, and symlinked note/task directories. Agents must use
the adapter's authorized write tools rather than this helper to bypass edit approval.
If an ancestor has a Git marker, missing Git or failed discovery stops note creation
instead of treating a nested directory as a non-Git target. Linked or special Git
markers are rejected; genuine non-Git targets remain supported.

You may version project guidance and notes according to team policy. For a personal,
untracked installation, append only relevant rules once to the path returned by
git rev-parse --git-path info/exclude from the target repository. Legacy local
installations can use the complete list:

```gitignore
# Local Inge files
/inge/
/thoughts/
/.opencode/commands/inge.md
/.opencode/commands/inge-work.md
/.opencode/commands/inge-review.md
/.opencode/commands/inge-arch.md
/.opencode/commands/inge-status.md
```

Do not exclude unrelated commands or all of .opencode. Excludes do not untrack files.
Shared .inge belongs outside target repos; if you put it inside one, decide its
tracking policy explicitly. Skip Git-only setup for non-Git projects.

### Legacy local installation

You can still copy repo/inge to each repository and commands to its supported
local command directory. The core is the same. New shared installs remove that
copying requirement; any local kit must be explicitly selected and trusted.
See [upgrading and compatibility](docs/COMPATIBILITY.md).

### Other harnesses

Use [the generic adapter](repo/inge/adapters/generic.md): add a short pointer to
the resolved BOOTSTRAP.md in the harness's supported instruction mechanism, or ask
the session to read it explicitly. Select the generic adapter and target repository.

Do not copy OpenCode frontmatter into another product and assume it implements
models or permissions. A harness without specialist dispatch can apply the guidance
in the current session if authorized, announcing the limitation. A read-only harness
without an authorized writer must stop at a concrete proposed change. No verified
native integration beyond OpenCode is shipped.

## Models and manual provider switching

The five OpenCode agent files contain the configured model IDs and commented
alternatives retained from the original kit. They are examples of your prior mapping,
not a claim of provider availability. Confirm access before use.

Switch the four main roles to their existing provider mappings from this checkout:

```bash
./scripts/change_inge_models copilot
./scripts/change_inge_models litellm
```

The selected model line is uncommented and other active model lines are commented.
Haiku models and inge-scout.md remain untouched, as do permissions and agent prose.
All four files are validated before editing; a missing mapping stops the switch.
Repeated selection of the same provider makes no further changes.

To update an installed copy, explicitly select its agent directory:

```bash
./scripts/change_inge_models copilot --agents-dir "$HOME/.config/opencode/agents"
```

Use your actual installation path if different. The default only updates this
checkout. Add this checkout's scripts directory to PATH to invoke
`change_inge_models copilot` from anywhere. Restart or reload your harness afterward;
the script does not contact providers, change a running session, or modify opencode.json.

Role selection follows [routing.md](repo/inge/references/routing.md); native mapping,
permissions and manual changes are in [the OpenCode adapter](repo/inge/adapters/opencode.md).
Update coordinator/worker together for routine-tier consistency, expert/strong-worker
together for difficult work, and scout separately. Preserve permissions. Native
model selection is an adapter responsibility; the portable core does not switch
models by mentioning their names.

On actual provider failure, stop that call and report partial work. Resume after
a user-configured switch/reload and inspection of partial edits. No automatic
cross-account retry, quota probing or billing enforcement.

## Practice drills

[DRILLS.md](docs/DRILLS.md) includes natural-language tickets, vague requirements,
greenfield design, failure/security review, history, shared discovery and portable
fallbacks, plus detailed legacy scenarios. Start with an ordinary conversation,
not a checklist of internal role names.

## Validation and troubleshooting

Agent-safe static checks (no Git calls or metadata writes):

```bash
python3 validation/validate.py --policy-only
```

The full suites documented in docs/VALIDATION.md create disposable Git repositories
and some commits/worktrees. They are for the human maintainer to run manually, not
for inge under the standing no-Git-writes policy.

Requires Python 3, Git and Ruby's standard YAML parser. Fixtures are disposable;
no installed configuration, provider or production environment is changed.
See [executed checks and limitations](docs/VALIDATION.md).

Behavior tests are separate: compare the plain harness, current Inge and candidate
changes on the same scenarios. Measure outcomes, scope preservation, unnecessary
questions, honest model/skill reporting, verification, time and cost when exposed.
Repeat runs; static Markdown assertions are not proof of reliable agent behavior.

| Symptom | Check |
|---|---|
| Missing command | Effective global/local discovery, duplicate names, restart |
| Wrong framework | Approved explicit path or trusted-launcher INGE_HOME; no automatic fallback |
| Notes in wrong place | Explicit --repo and doctor output; never share thoughts |
| Missing skill dependency | Actual catalog and supporting files; use bundled fallback |
| Model/dispatch unavailable | Installed mapping and harness capability; disclose limitations |
| Unexpected approval behavior | Effective merged permissions; never bypass a denial |
| Stale resume | Recorded revision plus current working-tree changes and evidence |
