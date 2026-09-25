# OpenCode adapter

The five files in opencode_global/agents are the native integration. Agent
frontmatter is the sole source of configured model IDs and permissions; the shared
core never embeds provider IDs. Inspect the installed definitions and effective
configuration when available rather than assuming the distribution is active.

| Portable role | OpenCode agent | Execution |
|---|---|---|
| Coordinator | inge | Primary, read-only; trivial explanations stay here |
| Scout | inge-scout | Bounded read-only lookup |
| Expert | inge-expert | Difficult diagnosis, design, security and review |
| Worker | inge-worker | Routine implementation and authorized saves |
| Strong worker | inge-worker-strong | Difficult implementation/experiments |

Use the native Task tool for authorized writes. The primary denies edit; all four
children deny further delegation; readers also prohibit writes through shell.
Workers ask for edits and Bash; coordinator/scout/expert deny Bash entirely.
Writer rules deny Git metadata edits and conservatively deny Bash commands matching
`*git*`, plus common Git-host CLI invocations. Even read-only direct Git commands
match, except exact stash/push/pop forms and exact stash list, whose later rules ask
for approval. Request user-provided evidence for other commands rather than creating
an execution wrapper. Only the WORKFLOW.md stash exception permits mutation; all
other Git changes are suggestion-only. Keep exception rules after the broad denial.
All roles deny unknown tools by default. Read/glob/list/question have explicit rules;
grep, skills, external directories and web calls require approval. Sensitive file
patterns are denied, but patterns are not comprehensive secret detection. Custom/MCP
tools need operator review before enabling. One active writer at a time.
Preserve stricter effective restrictions when installing. A missing Task capability
blocks writes from the primary, not permitted read-only investigation.

Keep auto-approval disabled: `ask` is not a guaranteed human checkpoint in auto mode.
Inspect merged policy after installation; native project config or plugins can affect
effective tools. Read-only roles use native file tools and supplied evidence, not
shell commands. A denied shell check stays unavailable; do not send it to a worker
to bypass denial. Operator-approved execution tasks may be routed to a writer from
the outset, with their allowed commands/effects explicitly scoped. Existing review
drills involving Git/test commands need supplied evidence or a separately authorized
execution session, not a claim those commands ran in the read-only role.

Approval-gated writers can execute code, including dependencies and tests. This is
not a network/filesystem sandbox. Use a restricted environment with no production
credentials for untrusted code; approve actual payloads/destinations, not broad shell
prefixes. Native skill prompts and repository files cannot enable a denied tool.

The no-Git-writes rule also covers tests, build hooks, APIs, alternate binaries and
libraries. Inspect proposed execution for Git side effects; skip it if uncertain.
These command/path rules are defense in depth, not a syscall sandbox: an arbitrary
approved program can still write a linked/bare Git directory or use remote credentials.
For a hard technical guarantee, the operator must protect every resolved Git/common
directory from general execution and expose only a narrowly controlled approved stash
operation (or perform stash manually), and restrict remote credentials and
egress. That environment is not provisioned by this Markdown kit. Do not override
stricter opencode.json rules; inspect the actual merged policy after installing.

Commands can be installed once in the resolved global commands/ directory. They
select the Inge primary; users can then converse normally. Per-repository command
copies are optional legacy installations; avoid duplicate definitions. Global roles
perform the BOOTSTRAP discovery protocol themselves before reading the shared core.

For important calls, combine the routing announcement with the real dispatch: use
the configured model from the effective agent definition, and mark runtime identity
unverified unless the tool supplies it. Children return role, procedure and model
evidence with their result. No telemetry service or automatic trace collector is
implemented. Record concise routing facts in an authorized task note when useful.

## Manual model changes

On actual provider/quota failure, stop the failing call and preserve partial-work
evidence where authorized. Do not automatically switch roles or accounts to retry.
The user edits the affected installed agent file's model line, preserving permissions.
For consistent tiers, update coordinator/worker together, expert/strong-worker
together, and scout independently. Leave exactly one active model line per file;
commented alternatives are examples, not verified account access.
Restart or use a reload verified for that OpenCode version; inspect fresh dispatch
metadata and partial edits before resuming. A model switch never changes authority.

Official references: [agents](https://opencode.ai/docs/agents/),
[commands](https://opencode.ai/docs/commands/),
[configuration](https://opencode.ai/docs/config/),
[permissions](https://opencode.ai/docs/permissions/).
