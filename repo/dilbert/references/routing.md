# Roles, approvals, and manual model switching

The router uses OpenCode's native Task tool. Commands express user intent; printing
a command does not execute it. Choose roles directly for the task's difficulty,
without making a cheaper role fail first. QUICK / STANDARD / STRICT set process depth;
architecture and explanation are intents. Announce role, configured model, and reason.
If runtime model identity is unavailable, label it configured, not verified effective.

| Role | Use | Active model | Commented manual alternative |
|---|---|---|---|
| dilbert | Thin primary, oracle conversation, coordination, delivery | litellm/claude-sonnet-5 | github-copilot/claude-sonnet-5 |
| dilbert-scout | Bounded read-only lookup/extraction | litellm/claude-haiku | github-copilot/claude-haiku-4.5 |
| dilbert-expert | Hard diagnosis, architecture, tradeoffs, difficult review | litellm/claude-opus-4-8 | github-copilot/gpt-5.6-sol |
| dilbert-worker | Routine edits and approved artifact persistence | litellm/claude-sonnet-5 | github-copilot/claude-sonnet-5 |
| dilbert-worker-strong | Difficult implementation | litellm/claude-opus-4-8 | github-copilot/gpt-5.6-sol |

These IDs match the inspected original kit and the user-specified role mapping;
provider availability is not verified.
Terra has no verified ID here. Its reminder comments are not active placeholders.

Handle short read-only answers directly. Delegate substantial bounded lookup to scout;
hard analysis to expert; a save-only request or ordinary implementation to worker;
difficult implementation to worker-strong. Avoid a mandatory expert pass for a typo.
Readers return proposed content. The router sends authorized persistence to a writer
and confirms the saved path/content before claiming completion.

Only the router delegates, and only to these four named children. All children deny
Task. One active writer at a time, including note updates; stay in the current working
directory unless a worktree was requested. Additional independent reviewers or parallel
work require the user's request. No nested delegation to satisfy a skill's defaults.

Every packet contains only:

- Goal, intent, context, process mode, and expected output.
- Oracle decisions, accepted criteria, unresolved blockers, and their sources.
- Permitted actions and exact write scope; all relevant permission restrictions.
- Relevant paths/revisions, current directory, existing changes, and prior attempts.
- Evidence needed to resume and any pending delivery/integration status.

Do not dump the conversation or assume context automatically transfers. Missing oracle
decisions return to the router/user. A child cannot independently expand scope or change
acceptance. An investigation does not authorize application edits. An implementation
request authorizes starting its worker without another conversational approval; native
edit/bash approvals remain. A request to save authorizes that artifact only.

Router/scout/expert deny edit and must not write through Bash. Writers ask for edits;
all roles ask for Bash. These are routing roles, not technical sandboxes. Effective
global/repository restrictions may be stricter: preserve them when installing because
agent rules can override global rules. If an edit is rejected, stop that action. Never
try a different worker, provider, or shell to bypass it. Do not relax permissions.

## Manual provider fallback

On quota/provider failure, stop that call. Report failing role/model, completed work,
partial edits, unsaved continuity, and next action. Preserve progress only if already
authorized and possible without bypassing the failure. Do not automatically retry on
Sol, another account, or a different role. The user must switch configuration manually.

In the resolved global agent directory, comment the active `model:` and uncomment the
desired alternative, leaving exactly one active line in each affected file:

- Sonnet tier: **both** `dilbert.md` and `dilbert-worker.md`.
- Strong tier: **both** `dilbert-expert.md` and `dilbert-worker-strong.md`.
- Scout tier: `dilbert-scout.md`.

Restart OpenCode after saving, or use a reload confirmed for the installed version.
Inspect effective parent and child models in a fresh session before resuming; an existing
child may retain old configuration. Do not spend tokens across accounts just to test.
Review partial worker edits and current evidence before the next bounded action.
Model changes never change approvals. If the router cannot start, the user must edit
`dilbert.md` and its tier companion directly in their editor; it cannot recover itself.
