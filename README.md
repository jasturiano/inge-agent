# Dilbert for OpenCode

Dilbert is a manually installed engineering framework for working safely in unfamiliar
codebases and designing new systems. Start every task with one command:

```text
/dilbert <what you want to investigate, clarify, build, review, or save>
```

Dilbert establishes what success means, investigates the relevant evidence, asks about
unresolved decisions, and routes work to the appropriate specialist. It preserves
existing behavior and consumers in **brownfield** projects, clarifies requirements and
operations in **greenfield** projects, and applies both disciplines to **mixed** work.
The core is platform-neutral: AWS, GCP, Azure, on-premises and hybrid environments fit
without prescribing a provider or deployment tool.

[How it works](#how-it-works) · [Manual installation](#manual-installation) ·
[Model switching](#models-and-manual-provider-switching) · [Drills](#practice-drills) ·
[Validation](#validation-and-troubleshooting)

## How it works

Tell Dilbert the task, relevant context, and constraints. It selects only the necessary
work: intake and research, oracle questions, acceptance scenarios, planning, implementation,
verification, diff review, architecture evaluation, or continuity. A short explanation
can stay in chat; a change uses a compact note at `thoughts/<ID>/task.md`.

The **oracle** is the source of accepted intent: you, the responsible owner, an approved
ticket, a contract, or confirmed examples. Code establishes current behavior, not what
you want it to become. Dilbert separates **Stated / Implied / Unknown**, investigates
technical questions, reuses confirmed answers, and asks about consequential tradeoffs.
A recommendation is not approval, and silence never supplies an answer.

| Process depth | Appropriate work | What to expect |
|---|---|---|
| QUICK | Clear, bounded, reversible change | Success criterion, targeted inspection, change, proportionate verification and brief review |
| STANDARD | Ordinary feature or bug | Relevant research, resolved intent, acceptance criteria, short plan, implementation and checks |
| STRICT | Sensitive contracts, permissions, data or broad impact | Explicit material decisions, scenarios, consumer analysis, deeper review and recovery planning |

Depth and model tier are independent. A small difficult bug may need a strong model;
a typo does not need seven documents or a questionnaire. Architecture and explanation
are intents, not additional process-depth modes.

### Five roles, supervised changes

| Agent | Responsibility | Edit | Shell | Delegation |
|---|---|---|---|---|
| `dilbert` | Primary router, oracle conversation, final delivery | deny | ask | Only the four specialists |
| `dilbert-scout` | Economy lookup and evidence extraction | deny | ask | deny |
| `dilbert-expert` | Strong diagnosis, architecture and difficult review | deny | ask | deny |
| `dilbert-worker` | Routine implementation and requested note saving | ask | ask | deny |
| `dilbert-worker-strong` | Difficult implementation | ask | ask | deny |

The router delegates authorized writes through OpenCode's native Task tool. You do not
switch to a second primary agent to save or implement. An implementation request permits
starting its worker; native edit/bash approvals still apply. Investigation alone does
not authorize application changes, and save-only means only the requested artifact.
A rejected action must not be retried through another worker, shell, or provider.
Readers must not write through Bash. One writer runs at a time; children cannot delegate.

Work stays in the current branch/directory by default. Dilbert preserves unrelated edits,
reports baseline failures separately from new regressions, and reviews staged, unstaged
and relevant new files. Worktrees require explicit context transfer, integration approval,
and verification in the destination. Excluded notes do not travel through commits.
Commits, publishing, deployments and destructive cleanup require their own authorization.

## Repository structure

```text
.
├── README.md                     Overview and manual installation
├── docs/
│   ├── DRILLS.md                 Guided examples with expected outcomes
│   ├── COMPATIBILITY.md          Existing RPI/recon workflows and upgrades
│   └── VALIDATION.md             Executed checks and runtime limitations
├── opencode_global/agents/       Five agents to install globally
├── repo/
│   ├── .opencode/commands/       Main command and four optional aliases
│   └── dilbert/                 Workflow, project profile, references and note helper
├── validation/                  Deterministic tests and live behavior checklist
└── backup/                      Local recovery ZIPs; ignored by Git
```

`opencode_global/` and `repo/` are distribution directories. Copy their contents to the
specified targets below; do not install this entire repository into your project.
`backup/` is optional local recovery data and is not needed to install or test Dilbert.
There is no package manager, database, service or publishing requirement.

## Manual installation

### 1. Identify your targets

Use an existing OpenCode installation with access to the configured models. Python 3
is optional for the note helper; Git is needed only for Git-related operations. A new
directory without Git works without initializing a repository.

In your terminal:

```bash
opencode --version
```

Identify the effective global configuration directory and the target repository root.
Account for `OPENCODE_CONFIG_DIR`, `OPENCODE_CONFIG`, and any XDG or managed settings in
your installation. In an existing repository, `git rev-parse --show-toplevel` identifies
its root. Do not assume the shell's current directory is the intended target.

This distribution uses the documented plural `agents/` and `commands/` directories.
The standard global location is `~/.config/opencode/agents/`. Verify discovery for your
installed version before copying; if it needs singular directories, use that supported
location consistently. Never install both to try to make discovery work.
See OpenCode's [agent documentation](https://opencode.ai/docs/agents/),
[commands](https://opencode.ai/docs/commands/) and [configuration](https://opencode.ai/docs/config/).

### 2. Compare and preserve existing configuration

For an update, inspect global and project agent/command directories and same-named JSON
configuration first. Back up files you will replace **outside all discovery directories**.
Compare changes and preserve your mandatory restrictions, custom behavior, project
instructions, existing `dilbert/PROJECT.md`, skills and `thoughts/`.

Agent permissions can override global rules. Merge stricter denials and shell restrictions
into the five role files before installing; do not replace a mandatory deny with ask.
If effective policy prohibits delegation, resolve that conflict before using the router.
Never blanket-replace `AGENTS.md`, `opencode.json`, or provider configuration.
See [OpenCode permission precedence](https://opencode.ai/docs/permissions/).

For old Dilbert installations, follow the [compatibility guide](docs/COMPATIBILITY.md)
to retire only superseded kit-owned definitions after verifying their replacements.

### 3. Copy the reviewed files

Run from this distribution's root. Replace both paths below with the targets you verified.
For updates, use your reviewed/merged agent definitions; `cp -i` prompts before overwriting
but does not merge custom permissions or project settings for you.

```bash
dilbert_global="/absolute/path/to/resolved/opencode"
dilbert_repo="/absolute/path/to/your-repository"

mkdir -p "$dilbert_global/agents" "$dilbert_repo/.opencode/commands"
cp -i opencode_global/agents/*.md "$dilbert_global/agents/"
cp -i repo/.opencode/commands/*.md "$dilbert_repo/.opencode/commands/"
cp -Ri repo/dilbert "$dilbert_repo/"
```

When updating, decline replacing `PROJECT.md` and merge any new profile fields manually.
Use real local copies of `dilbert/`; the helper resolves its repository from its own
installed location. Do not symlink it to a shared kit, and never copy another project's
`thoughts/` into the target.

The resulting installation is:

| Target | Contents |
|---|---|
| `<global-config>/agents/` | The five `dilbert*.md` agent definitions |
| `<repository-root>/.opencode/commands/` | `dilbert.md` and four optional aliases |
| `<repository-root>/dilbert/` | Shared workflow, references, template, script and PROJECT.md |
| `<repository-root>/thoughts/` | Created as tasks are saved; preserve existing notes |

### 4. Set the project profile and local excludes

Edit `<repository-root>/dilbert/PROJECT.md` with known stack conventions, check commands,
safe test environments, platforms and mandatory restrictions. Unknown values can stay
"to discover"; the profile does not itself authorize external operations.

For a Git repository, resolve its local exclude file from the target root:

```bash
cd "$dilbert_repo"
git rev-parse --git-path info/exclude
```

Append these rules **once** to the printed file, preserving its existing content. This
also works when `.git` is a linked-worktree metadata file. Use your confirmed singular
command path instead if that is what your OpenCode version supports.

```gitignore
# Local Dilbert files
/dilbert/
/thoughts/
/.opencode/commands/dilbert.md
/.opencode/commands/dilbert-work.md
/.opencode/commands/dilbert-review.md
/.opencode/commands/dilbert-arch.md
/.opencode/commands/dilbert-status.md
```

Do not exclude all of `.opencode/` or unrelated project instructions. For retained legacy
files, use the exact kit-owned paths in the compatibility guide. Excludes do not untrack
files; do not automatically remove anything from the index. Without Git, skip this step.

```bash
git check-ignore -v -- dilbert/WORKFLOW.md .opencode/commands/dilbert.md thoughts/TEST/task.md
git status --short
```

The distribution's own `.gitignore` excludes local backups and generated clutter. That
file is for maintaining Dilbert itself; it does not replace the target's local excludes.

### 5. Verify discovery and approvals

Restart OpenCode in the target repository. Confirm one Dilbert primary, its four
specialists, and `/dilbert` plus the optional aliases in the command list. Start with:

```text
/dilbert Locate the task-note template and explain its purpose. Read-only; do not save anything.
```

Then run [Drill I: routing and rejected edits](docs/DRILLS.md#drill-i-routing-and-rejected-edit-smoke-test)
in a disposable repository. Confirm the effective child model and native edit approval;
reject an edit and verify that no alternative worker/shell/provider retries it.
Static permission checks cannot prove effective runtime enforcement.

## Models and manual provider switching

Dilbert selects the role automatically. **Subscription/provider switching is manual**:
edit the installed agent frontmatter, leaving exactly one active `model:` per file.

| Tier | Files to change together | Active model | Commented alternative |
|---|---|---|---|
| Router/routine | `dilbert.md` and `dilbert-worker.md` | `litellm/claude-sonnet-5` | `github-copilot/claude-sonnet-5` |
| Strong | `dilbert-expert.md` and `dilbert-worker-strong.md` | `litellm/claude-opus-4-8` | `github-copilot/gpt-5.6-sol` |
| Economy | `dilbert-scout.md` | `litellm/claude-haiku` | `github-copilot/claude-haiku-4.5` |

These IDs were supplied in the original kit and requested role mapping; availability in
your account is not guaranteed. No verified Terra ID is included. Add it as a commented
alternative only after confirming its exact OpenCode ID. Commands contain no model pins.

On quota/provider failure, the call stops and reports its role/model, progress, partial
edits and files to switch. Comment the active line and uncomment the chosen alternative
in **both** tier files (economy has one), then restart or use a reload verified for your
version. Existing children may retain old settings: confirm effective models in fresh
parent/child sessions and inspect partial edits before resuming. Never change approvals.
If the router cannot start, edit `dilbert.md` and `dilbert-worker.md` yourself.
[Drill J](docs/DRILLS.md#drill-j-manual-quota-fallback-and-safe-resume) walks through recovery.
There is no automatic provider fallback or enforced monetary budget.

## Everyday commands and optional skills

`/dilbert` covers every intent. These aliases are convenience shortcuts to the same router:

| Alias | Purpose |
|---|---|
| `/dilbert-work <request>` | Implement or save |
| `/dilbert-review <scope>` | Review local changes by default, or an explicit commit range |
| `/dilbert-arch <request>` | Architecture evaluation |
| `/dilbert-status <ID>` | Resume from compact or numbered artifacts |

Existing RPI/recon work continues in place. For example, `/dilbert rpi-plan-review BILL-142 2`
performs that bounded review, and `/dilbert rpi-review BILL-142 --working-tree` includes
uncommitted work. See the [complete stage contracts](repo/dilbert/references/legacy-stages.md).
No task.md prerequisite, repeated oracle answers, or recreated completed stages is required.

Discover installed Matt Pocock skills, graphify, ponytail and optional i-have-adhd in the
actual OpenCode skill catalog before use. Preserve custom copies; do not reinstall them
or assume the original archive layout proves discovery. See [skill compatibility](docs/COMPATIBILITY.md#skills).
Use current graphs for relationships, rg for literals, source for decisive behavior, and
checks for verification. Graph creation is optional and requires write authorization.
Skill defaults do not authorize extra agents, commits, publishing or expanded scope;
presentation changes cannot suppress evidence or approval decisions.

For a note without an external ticket, ask Dilbert to save a LOCAL note. You may also
create a blank note yourself from the installed repository:

```bash
python3 dilbert/scripts/new-task.py LOCAL-001
```

The helper rejects unsafe IDs and existing notes. Filling a template does not establish
acceptance or prove completion.

## Practice drills

[Open the full drill guide](docs/DRILLS.md). Each drill gives a request sequence and
expected behavior. Replace example IDs, paths and symptoms with real inputs; keep real
infrastructure operations outside practice runs.

| Drill | What you learn |
|---|---|
| [A — Brownfield ticket](docs/DRILLS.md#drill-a-work-an-existing-brownfield-ticket) | Research consumers, clarify ambiguity, plan, implement and review |
| [B — Greenfield setup](docs/DRILLS.md#drill-b-greenfield-prefect-setup) | Questionnaire-driven intent and operations; Prefect is only an example |
| [C — QUICK fix](docs/DRILLS.md#drill-c-quick-fix-without-an-external-ticket) | Bounded work without an external ticket or artificial ceremony |
| [D — Difficult diagnosis](docs/DRILLS.md#drill-d-difficult-brownfield-bug) | Evidence and reproduction before a fix |
| [E — Architecture](docs/DRILLS.md#drill-e-review-cloud-on-premises-or-hybrid-architecture) | Claimed/actual evidence, quality scenarios and justified risks |
| [F — Infrastructure task](docs/DRILLS.md#drill-f-an-ansible-package-task) | Local checks and explicitly authorized environment tests; Ansible is an example |
| [G — Save and resume](docs/DRILLS.md#drill-g-resume-after-a-break) | Preserve decisions, checked state, blockers and next action |
| [H — Worktree integration](docs/DRILLS.md#drill-h-explicitly-request-a-worktree-and-bring-the-result-back) | Transfer context and verify delivery in the destination |
| [I — Routing and approvals](docs/DRILLS.md#drill-i-routing-and-rejected-edit-smoke-test) | Verify role selection, save-only scope and rejected-edit behavior |
| [J — Quota fallback](docs/DRILLS.md#drill-j-manual-quota-fallback-and-safe-resume) | Switch the account manually and inspect partial work |
| [K — Legacy notes and recon](docs/DRILLS.md#drill-k-preserve-a-numbered-ticket-and-reuse-evidence) | Continue numbered artifacts and reuse confirmed knowledge |

## Validation and troubleshooting

From this distribution's root:

```bash
python3 validation/validate.py
```

The deterministic suite requires Python 3, Git and Ruby's standard YAML parser. It
checks roles, permissions, models, commands, references, legacy contracts, safe note
creation, actual-diff scope and worktree excludes. Tests use disposable fixtures and
need neither `backup/` nor a configured provider. These tools are test dependencies,
not a package-install requirement for using the Markdown framework.

Read [validation results and limits](docs/VALIDATION.md) and the
[live behavior checklist](validation/BEHAVIOR.md). OpenCode was unavailable in the
validation environment, so discovery, effective child models and rejected-edit enforcement
remain live checks. No production operation or cross-account quota test is needed.

| Symptom | Check |
|---|---|
| Missing `/dilbert` | Target repository root, supported command directory, duplicate JSON/Markdown definitions; restart |
| Agent or model unavailable | Global config location, provider access, active model line in the affected role |
| No native approval or unexpectedly denied action | Effective merged permissions and stricter local/managed rules; do not bypass them |
| A skill is absent | Actual catalog, discovery path, frontmatter and permission; use the local reference if optional |
| Resume seems stale | Evidence revision and working-tree changes, numbered/compact conflicts, unsaved handoff |

Dilbert is a set of role prompts, shared procedures and one deterministic helper. Its
engineering discipline works with the harness's permissions; it is not a separate sandbox
or workflow engine. No publishing, Git initialization or global installation is performed
by this repository itself.
