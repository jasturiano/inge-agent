# Security review — 2026-09-24

[Back to README](../README.md) · [Validation](VALIDATION.md)

## Scope and verdict

Reviewed the current uncommitted inge distribution: five OpenCode roles, shared
bootstrap/workflow/skill/continuity guidance, Python helpers and validation code.
This was a source review plus disposable local reproductions, not a penetration
test against an installed harness. No production resources, real credentials,
network destinations, live models or installed agents were tested or changed.

The framework **is not a prompt-injection sandbox**. The original review found the
issues below; a subsequent authorized hardening pass implemented source changes.
Severity describes the original finding, not a current CVSS score or compromise.
Do not treat passing tests or inventory exit codes as security certification.

## Current remediation status

2026-09-25 exception: explicitly approved stash push/pop is permitted for writers,
with exact stash list for identification. Other Git mutations remain human-only.
Conflicting pop must stop without dropping the entry or retrying. This supersedes
the absolute prohibition in the historical policy update below. Static checks passed;
live approval behavior is still unverified.

Historical policy update: Git mutations were made human-only, not approval-gated agent
operations. Direct Git/Git-host CLI patterns and Git metadata edits are denied for
writers; readers already deny Bash/edits. Scripts/APIs must not bypass this policy.
Arbitrary approved execution still requires OS-level Git-directory/egress isolation
for a hard guarantee. See the adapter and README. Only --policy-only tests were run
for this update; earlier full-suite results are historical.

| Finding | Implemented protection | Remaining boundary |
|---|---|---|
| SEC-01 | Explicit trusted path/INGE_HOME only; no local/ancestor fallback | Operator must protect/review that installation and native project configuration |
| SEC-02 | Catch-all tool deny; readers deny Bash; writers ask; explicit web/skill/grep approvals | Effective merged rules, auto-mode and live model behavior still need native validation |
| SEC-03 | Remove GIT_* overrides, isolate global config, validate root/nearest marker, five-second timeout | Trust the launcher, PATH and interpreter; unusual Git layouts fail closed |
| SEC-04 | No-follow descriptor-relative directory opens and exclusive private note creation | Not protection against a privileged attacker moving opened directories or changing mounts |
| SEC-05 | No-follow reads and traversal, special-file rejection, explicit roots resolve once | Unexpected links mean incomplete coverage; explicit roots are operator trust assertions |
| SEC-06 | Escape controls and Unicode format characters in diagnostic paths/errors | User-supplied argparse syntax errors are not an adversarial report channel |
| SEC-07 | 1 MiB/file, bounded chunk reads, 10,000-entry/30-second cooperative budget, Git timeout | Cooperative deadline cannot interrupt blocked kernel filesystem I/O |

Prompt policies now preserve source/trust labels through skill use, handoffs and
resume; saved approval claims cannot grant new authority. Native runtime tests below
remain NOT RUN because OpenCode is unavailable. No global installation was changed.
All helper operations requiring POSIX primitives fail closed on unsupported platforms.
Verification: 19 distribution + 7 inventory + 14 security regression tests passed;
all Python modules/classes/functions have docstrings. No live security score is claimed.

## Original review evidence

The finding narratives below preserve the pre-hardening behavior and reproduction
evidence for traceability. For current behavior use the status table and regression
suite, not the historical descriptions in present tense.

## Trust model

Trusted inputs should be the user's actual request, enforced harness policy, and
an explicitly trusted framework installation. Repository files, tickets, comments,
logs, web pages, tool results, task notes and third-party skills can contain
attacker-authored instructions. A malicious repository contributor need not control
the global agent file to influence what the agent reads next.

Assets include source integrity, private repository data, credentials available to
the process, local task state, connected tools, and shared guidance affecting other
repositories. Relevant attackers include an untrusted repository author, a compromised
skill/tool source, and a process able to modify the workspace concurrently. The
Python helpers run with the invoking user's filesystem privileges, not a separate
low-privilege service account.

## Findings

### SEC-01 — High: framework discovery promotes untrusted local files into policy

**Location:** [bootstrap](../repo/inge/BOOTSTRAP.md),
[primary agent](../opencode_global/agents/inge.md), and
[framework resolution](../repo/inge/scripts/paths.py), function `framework`.

**Precondition:** no explicitly trusted framework path is selected, and a repository
author can supply an `inge/` kit or a nearer `.inge` directory.

Local files take precedence over the shared installation. Validation checks that
required files exist, not who supplied them or whether the user trusts their revision.
The agent then reads the selected SOUL, workflow, routing and adapter as operational
guidance. A malicious local kit can replace those instructions; a helper copied into
that kit is also executable code if the operator subsequently runs it.

**Evidence:** the isolated selection fixture replaces local SOUL.md and confirms
that `framework()` selects it instead of the intact ancestor kit. This proves the
trust-boundary gap, not that a particular model obeys an injected instruction.

**Recommendation:** establish the trust decision outside repository-controlled text.
Prefer an operator-selected shared installation and require explicit approval before
using a new local kit/revision. Keep trusted instructions separate from project data;
pin/review external skills and helper code. A checksum stored beside attacker-controlled
files is insufficient unless its expected value comes from a trusted source.

**Interim mitigation:** select a reviewed framework via INGE_HOME or an explicit
session path. This does not neutralize native project configuration or injected task
content; those need independent controls.

### SEC-02 — High: explicit role permissions do not cover the full tool surface

**Location:** all [OpenCode agent definitions](../opencode_global/agents/), especially
the `permission` blocks, and [adapter claims](../repo/inge/adapters/opencode.md).

**Precondition:** deployment has permissive defaults or enabled network/custom/MCP
tools, and the model follows an injected request. Exact exposure depends on effective
configuration and the installed harness version.

The definitions configure edit, Bash and Task, but no catch-all or explicit network/
custom-tool policy. A role called read-only can still have tools that disclose data
or cause external effects. Bash `ask` is also not a read-only execution sandbox:
approved shell commands can write files even when the edit tool is denied.

Current OpenCode documentation says most omitted permissions default to allow,
agent rules take precedence when merged, and auto mode approves requests that would
otherwise ask. Thus `ask` alone does not guarantee a human confirmation in every
deployment. These are documented semantics, not a live exploit demonstration.
[OpenCode permissions](https://opencode.ai/docs/permissions/)

**Recommendation:** define least-privilege adapter profiles for all installed tools,
including unknown/custom tools and egress; verify merged policy and auto-approval mode.
Use a disposable environment with narrow filesystem/network access for untrusted code.
Keep secrets out of the process environment where possible. Verify denied actions in
the actual harness rather than relying on role prose or a Markdown parser test.

### SEC-03 — Medium: inherited Git variables can redirect a note outside --repo

**Location:** [paths.py](../repo/inge/scripts/paths.py), `repository`, and
[new-task.py](../repo/inge/scripts/new-task.py), `main`.

**Precondition:** the launching shell, editor or wrapper sets Git directory/worktree
overrides. Repository content alone does not establish control over the process
environment; this is also a realistic accidental misconfiguration.

`git -C TARGET rev-parse --show-toplevel` inherits the environment. Its successful
output is accepted as the write root without checking that TARGET belongs to it.
With GIT_DIR and GIT_WORK_TREE pointing at another fixture repository, the helper
successfully writes the new note there despite `--repo` naming the intended target.

**Evidence:** reproduced end-to-end with the real helper and two temporary directories.
Existing files are not overwritten, but confidentiality and destination assumptions
can be violated. Doctor can also report the wrong repository/profile/note location.

**Recommendation:** control repository-discovery environment variables and verify
the returned root against the requested target while retaining linked-worktree support.
Use a trusted executable path/environment. Add a regression asserting that unrelated
Git overrides cannot redirect writes. Document an explicit policy for bare repositories.

### SEC-04 — Medium: task-directory symlink protection has a check/write race

**Location:** [new-task.py](../repo/inge/scripts/new-task.py), the `is_symlink`,
`mkdir`, and exclusive `open` sequence in `main`.

**Precondition:** another process can replace a task path's parent directory while
the helper is executing. This is not a remote exploit against an otherwise trusted,
single-user stable directory.

The helper checks thoughts and the task directory, then uses pathname-based creation.
A swap to a symlink after the check redirects creation. Exclusive final-file creation
prevents overwriting a pre-existing task.md, but does not contain the parent traversal.

**Evidence:** a deterministic fixture swaps thoughts at the mkdir boundary and
confirms a new task file appears outside the intended repo, still within the fixture.
No timing-sensitive process or real filesystem victim was used.

**Recommendation:** use directory-descriptor-relative operations with no-follow and
directory checks where supported, anchoring the write to verified directory handles.
Fail closed on unsupported platforms or explicitly document a trusted-directory-only
contract. Repeating a path check immediately before writing is not a complete fix.

### SEC-05 — Medium: inventory symlink skipping does not contain direct reads

**Location:** [check-installation.py](../scripts/check-installation.py),
`compare`, `definitions`, `references`, and `scan`;
[doctor.py](../repo/inge/scripts/doctor.py), framework Markdown traversal.

**Precondition:** a scanned directory contains attacker-controlled file links or
symlinked framework/config parents accessible to the invoking user.

os.walk pruning prevents ordinary recursion through directory links, but direct
framework/config probes happen separately. `read_bytes` comparisons follow file
symlinks. The final-component check in `references` does not reject linked parents
or eliminate concurrent replacement. Doctor similarly reads Markdown file links.

**Evidence:** instrumented comparison in a disposable fixture confirms a fake file
outside the installation is read through SOUL.md. Its contents are not printed, so
this is a read-scope violation, not demonstrated network exfiltration. Comparison
categories can disclose limited equality/difference information.

**Recommendation:** define permitted read roots and an explicit symlink policy;
reject/report untrusted links before comparisons and use safe handle-based reads
where race resistance is required. Preserve intentionally selected shared symlinks
only under an explicit trust contract. Correct blanket claims about skipping links.

### SEC-06 — Low: unescaped paths can forge or manipulate terminal reports

**Location:** [check-installation.py](../scripts/check-installation.py), `leftover`
and other interpolated path/error output; helper status/error messages also use paths.

**Precondition:** filenames or supplied paths contain newlines or terminal control
characters and output is displayed by a terminal that interprets them.

**Evidence:** a captured report contains a fixture path's literal escape sequence
and forged extra line. The test never sends those characters to a real terminal.
This can obscure findings or spoof report lines; no terminal-specific code execution
is claimed. “No file contents printed” does not mean all output is safely encoded.

**Recommendation:** escape control characters in display paths/errors consistently,
or provide structured JSON output and a safe renderer. Do not treat report text from
attacker-controlled filenames as executable advice or agent instructions.

### SEC-07 — Low: some diagnostic reads and discovery have no resource bounds

**Location:** [check-installation.py](../scripts/check-installation.py), `compare`;
[doctor.py](../repo/inge/scripts/doctor.py), `read_text` loop; and
[paths.py](../repo/inge/scripts/paths.py), Git subprocess.

**Precondition:** very large accessible files, expensive trees/network mounts, or
a stalled executable/environment. Impact is on this CLI process, not a hosted service.

Comparisons load entire files into memory; doctor loads every matching Markdown file;
Git has no timeout. The 1 MiB limit on old-name reference scanning does not cover those
paths. Static evidence confirms missing bounds; no resource-exhaustion test was run.

**Recommendation:** stream comparisons, bound inspection sizes and elapsed work,
and give subprocesses timeouts. Report incomplete coverage explicitly rather than
returning a misleading healthy result after truncation.

## Prompt-injection coverage gaps

Existing policies already reject treating investigated content as authorization,
forbid bypassing denied actions, constrain skill defaults, require approval for shared
instruction changes, and preserve provenance for durable knowledge. These are useful
defenses, not proof of resistance. There are no executed adversarial model evaluations.

Additional cases should exercise source comments, tickets, web/tool responses,
skill resources, task-note resume and child-result handoffs. In particular, verify
that a summary does not turn an untrusted “approved by user” claim into accepted
authority, and that stored notes cannot grant new permissions on resume. The compact
handoff contract does not explicitly require retaining trust labels for quoted hostile
content. External skill names and presence alone do not establish trust.

The desired controls are separation of instructions/data, bounded tool capabilities,
approval for sensitive actions, provenance, and adversarial testing in combination;
no keyword filter or stronger SOUL wording is a complete solution.
[OWASP agent security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html),
[OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

## Reproduction and positive checks

The full commands below are now human-maintainer-only because their fixtures mutate
Git. Inge uses `python3 validation/validate.py --policy-only` instead.

```bash
python3 validation/validate.py
python3 validation/test_installation_check.py
python3 validation/security_check.py
```

All three are now regression suites requiring safe behavior. The former five
characterization assertions were converted to rejection/containment checks and
extended with resource-bound and unsupported-platform cases. No live model injection
was executed; passing proves the named deterministic contracts only.

Existing positive checks cover strict task-ID validation, pre-existing directory/file
symlink collisions, exclusive creation, preservation of prior task content, scoped
role/delegation configuration, profile/shared-kit separation, and inventory content
redaction/non-mutation. Subprocess construction uses argument arrays, not interpolated
shell strings. No runtime helper uses eval, pickle, or downloaded code execution.

OpenCode is not installed in this environment, so native policy enforcement, tool
egress, model behavior and approval interactions remain unverified. No conclusion
about the safety of a particular global/local installation follows from this review.

## Remediation order and acceptance criteria

1. Establish trusted framework selection and a full adapter permission/egress policy.
   In a disposable live harness, try an injected repository instruction and an
   unapproved outbound tool call; neither may expand the authorized action scope.
2. Isolate Git discovery and contain note creation. Redirected Git variables and
   parent-directory swaps must fail safely or stay within the explicit target.
3. Harden diagnostic reads/output: links outside approved roots must be reported
   without reading their targets, controls escaped, and resource limits observable.
4. Add repeatable adversarial resume/skill/handoff evaluations with harmless canaries,
   no real secrets or external destinations. Grade actual tool calls and filesystem
   effects, not only the assistant's refusal text.

Any hardening should preserve harness portability, useful shared installations,
user-owned project profiles, existing approvals, and transparent skill/model routing.
