# Practice drills

[Back to installation and overview](../README.md) · [Live acceptance cases](../validation/BEHAVIOR.md)

These drills are examples, not commands to run against production. Replace ticket
IDs, paths, symptoms, and environments with your actual inputs. Start OpenCode at
the repository root with the kit installed. Use `/dilbert` for every intent; authorized writes route to supervised workers. Stay in the same session when a
prompt refers to "the previous result". Across sessions, use saved artifact paths.

### Drill A: work an existing brownfield ticket

**Situation:** a ticket requests a behavior change in an unfamiliar codebase.

1. Use `/dilbert` and provide the actual ticket text:

   > Ticket BILL-142: [paste the ticket]. This is brownfield. Investigate the
   > affected flow and consumers. Separate what is stated, inferred, and unknown.
   > Ask the oracle only about decisions that block safe implementation. Do not edit.

2. Answer the intent questions, or identify the person who can. Ask Dilbert to
   investigate questions that the code or configuration can answer. An already
   clear ticket should not produce a questionnaire merely to fill a template.
3. Save the agreed scope and plan:

   ```text
   /dilbert Save the agreed BILL-142 request, oracle answers, acceptance criteria, evidence, and short plan to thoughts/BILL-142/task.md. Do not change application code yet.
   ```

4. Review the note, then request implementation:

   ```text
   /dilbert Implement BILL-142 from thoughts/BILL-142/task.md in my current branch. Preserve unrelated changes. Show relevant baseline and final checks. Keep edit approvals enabled.
   ```

5. Review the result:

   ```text
   /dilbert Review the current local changes against thoughts/BILL-142/task.md, including new files. Report regressions and unmet acceptance criteria.
   ```

**Expected:** targeted investigation, oracle decisions where needed, bounded changes,
and check evidence. Any decisive blocked check remains visible. Review does not
commit or integrate anything. Ask `/dilbert` to fix agreed findings or save the
final result; do not assume the read-only review updated the task note.

### Drill B: greenfield Prefect setup

**Situation:** you want a new Prefect installation, but the deployment design has
not been agreed. This remains an alignment problem even though the technology is named.

1. Start with `/dilbert`:

   > PREFECT-001: I want to introduce Prefect for [describe the actual processes].
   > Treat the new service as greenfield and any existing infrastructure integration
   > as brownfield. I am the oracle for [decisions you own]. Start with a questionnaire
   > about objectives, constraints, operations, and acceptance. Do not implement yet.

2. Supply what you know: POC or production, allowed infrastructure, who operates it,
   authentication and secret constraints, and a concrete demonstration of success.
   Ask for researched options when you cannot yet choose. Unresolved decisions stay
   unresolved; a recommended deployment option is not an approved option.
3. Request a saved decision record and plan:

   ```text
   /dilbert Save the confirmed Prefect decisions, remaining blockers, acceptance scenarios, and proposed plan to thoughts/PREFECT-001/task.md. Do not create deployment files yet.
   ```

4. Once material decisions are resolved and you approve the scope:

   ```text
   /dilbert Implement the approved first slice of PREFECT-001. Prepare the configuration and verification steps for the agreed test environment. Do not deploy to real infrastructure.
   ```

5. Inspect the files and checks. If you later want a remote deployment, request it
   separately for a named environment; review its action and recovery procedure
   before approving execution.

**Expected:** a real questionnaire, researched tradeoffs, and explicit acceptance.
No assumed cloud/self-hosted choice, scale, HA requirement, or production authorization.
A greenfield directory without Git does not require Dilbert to initialize Git.

### Drill C: quick fix without an external ticket

**Situation:** a typo or small, well-understood local defect.

```text
/dilbert Fix the typo [actual text] in [actual file]. Expected text: [replacement]. Use QUICK if appropriate, create a brief LOCAL task note, and keep my edit approvals. No unrelated cleanup or commit.
```

**Expected:** one brief success criterion, targeted inspection, a small change,
proportionate verification, and a local note. No mandatory questionnaire, separate
plan, architecture review, or worktree. A documentation typo does not need a new test.
If investigation reveals a shared contract or sensitive behavior, Dilbert explains
why QUICK no longer fits before expanding the work.

To check the result, run:

```text
/dilbert Review this quick fix for scope and correctness. Include uncommitted changes.
```

### Drill D: difficult brownfield bug

**Situation:** intermittent timeouts, duplicate processing, or another unclear failure.

1. Start with `/dilbert`:

   > BUG-208: [describe the exact symptom]. Here are the reproduction steps and
   > redacted logs: [provide them]. Diagnose before proposing a fix. Identify what
   > can be verified locally and any oracle decisions about expected behavior.

2. When instrumentation or a test harness needs editing:

   ```text
   /dilbert Save BUG-208 to thoughts/BUG-208/task.md and build the proposed reproduction in the approved local test environment. Show the experiment and result. Do not instrument production.
   ```

3. After evidence supports a cause:

   ```text
   /dilbert Apply the bounded fix for BUG-208. Verify the original symptom and a suitable regression check, remove temporary instrumentation, and record limitations.
   ```

**Expected:** falsifiable hypotheses and new evidence, not repeated speculative patches.
If the symptom cannot be reproduced, Dilbert can investigate statically but must not
claim a confirmed cause. Existing unrelated failures are recorded separately.

### Drill E: review cloud, on-premises, or hybrid architecture

**Situation:** evaluate an existing workload without changing infrastructure.
Name its actual platforms: AWS, GCP, Azure, on-premises, or a combination. None is
a default. Supply the tools and evidence you actually have; IaC is useful when
present, not a prerequisite.

1. Start with scope and oracle:

   ```text
   /dilbert Architecture review: ARCH-001: review [workload/environment] on [platforms, regions/sites, and relevant boundaries]. The decision is [what you need to decide]. Here are diagrams, provisioning/configuration sources, and available inventory exports: [actual sources]. Clarify priorities and acceptance scenarios with me. Read-only; no infrastructure changes.
   ```

2. Answer questions about priorities and constraints. Supply only needed, authorized
   evidence. If environment access is unavailable, use relevant exports; do not supply
   credentials in chat. Ask for a descriptive map first if that is all you need.
3. Let Dilbert distinguish documented design, desired configuration, observed deployment,
   and demonstrated operational behavior. Ask for scenario-backed risks, tradeoffs,
   and unverified areas. If an independent A2 pass is required, save A0 and start a
   new session with A0 only; do not describe an already exposed context as independent.
4. Save the reviewed report:

   ```text
   /dilbert Save the reviewed ARCH-001 report to thoughts/ARCH-001/architecture.md and its scope, platforms, oracle decisions, evidence references, and next action to thoughts/ARCH-001/task.md. Do not implement recommendations.
   ```

**Expected:** A0-A5 in one report when useful, grounded findings and explicit limits.
Graphify may help with code relationships; it does not prove deployed infrastructure state.
Use platform-appropriate evidence and failure domains rather than translating service
names as though different platforms provide identical guarantees.
No invented RTO/RPO, automatic remediation, or production failure simulation.

### Drill F: an Ansible package task

**Situation:** this particular ticket uses Ansible to add package installation
behavior to an existing role or playbook. Ansible is an example here, not a kit
dependency. For another tool, substitute its native validation and execution model.

1. Start with `/dilbert`:

   > OPS-310: add [package and required state/version] to [existing role/playbook].
   > Supported targets are [known OS/environments]. Inspect existing conventions,
   > consumers, and verification. Ask about missing requirements; do not assume
   > "package" means a new role or collection.

2. Confirm scope and the safe test target, then request the change:

   ```text
   /dilbert Implement the agreed OPS-310 change in my current branch. Save the task note, run appropriate local syntax/lint checks, and propose behavior and idempotence verification for the authorized test environment. Do not run against production.
   ```

3. Review and approve any environment-affecting test separately. For expected
   idempotence, check a second run for unexpected changes.

**Expected:** existing conventions preserved, no unnecessary abstractions, and checks
appropriate to infrastructure. `--check --diff` is not treated as complete proof or
as permission to mutate a target; inspect task overrides and module limitations.

### Drill G: resume after a break

Before leaving a session, persist the current state:

```text
/dilbert Update thoughts/BILL-142/task.md with the actual progress, checked revision, pending decisions or approvals, and one next action. Do not change application code.
```

In the new session:

```text
/dilbert Resume BILL-142
```

**Expected:** Dilbert reads the note, checks whether its evidence is still current,
and reports the next action. It does not equate an existing note with a completed
stage. Use `/dilbert` when you want to resume editing. If saving was previously
blocked, provide the unsaved handoff explicitly.

### Drill H: explicitly request a worktree and bring the result back

**Situation:** isolation is useful for this particular task. Ordinary tasks can stay
in the current branch.

1. Use `/dilbert` to request a proposal:

   > For BILL-142, I want an isolated worktree. Inspect my current branch and dirty
   > state, then propose a worker path, base revision, context transfer, and delivery
   > back to this branch. Do not create or integrate anything yet.

2. After reviewing the proposal:

   ```text
   /dilbert Create the agreed BILL-142 worktree and transfer only its required kit files and task context. Preserve my existing changes. Do not commit or integrate without my approval.
   ```

3. Open OpenCode in the worker directory and work from its task note. Before returning,
   request a delivery record with origin, target, tested revision, commits if authorized,
   patch/new files otherwise, and any remaining dirty state.
4. Return to OpenCode in the target repository. Provide the worker location and record:

   > Inspect the BILL-142 delivery from [worker path]. Show the exact changes and
   > proposed integration into [target branch]. Do not integrate yet.

5. Approve the concrete integration through `/dilbert`, then request relevant
   checks in the target. Leave cleanup for a separate approval after verifying that
   changes and necessary artifacts are preserved.

**Expected:** pending-integration is visible until integration actually succeeds.
Uncommitted and excluded files are handled explicitly; a branch merge does not
transport them automatically. No automatic force removal, reset, or deletion.

### Drill I: routing and rejected-edit smoke test

Use a disposable repository with the kit copied locally and the reviewed global agents.

1. `/dilbert Locate the task-note template; read-only.` A short answer may stay in the
   router. A substantial bounded lookup should select scout and report evidence.
2. `/dilbert Save a note saying "routing smoke test" to thoughts/SMOKE/task.md. Change no application files.`
   Expect the routine worker, an edit approval, and no application changes.
3. Reject that edit. Verify the file was not written and no different worker, shell,
   or provider retries it. Static frontmatter checks cannot prove this behavior.
4. Start a separately authorized save request and approve it. Check the actual file and
   effective child model. Ask `/dilbert Explain what was saved; read-only.`
5. `/dilbert I want a new service; help clarify objectives and operations before implementation.`
   Expect oracle questions for unresolved choices and no assumed architecture.

### Drill J: manual quota fallback and safe resume

When an actual call fails, retain its role/model and partial-work report; do not force
requests across accounts to simulate quota exhaustion. If the strong worker failed,
edit **both** `<global>/agents/dilbert-expert.md` and
`<global>/agents/dilbert-worker-strong.md`: comment `model: litellm/claude-opus-4-8`,
uncomment `# model: github-copilot/gpt-5.6-sol`. For a router/routine failure edit
**both** `dilbert.md` and `dilbert-worker.md` using their Sonnet alternatives. For scout,
edit only `dilbert-scout.md`. Use your resolved discovery directory in these paths.

Restart/reload as verified for your version and confirm effective model identity in a
fresh parent/child session. Then use `/dilbert Resume <ID>; inspect partial edits and
saved evidence before continuing the authorized scope`. Keep native approvals enabled.
If saving failed, include the unsaved handoff explicitly. Switching accounts does not
turn a denied edit into an authorized action.

### Drill K: preserve a numbered ticket and reuse evidence

Given an existing ticket with answered 02-questionnaire.md and accepted 03-scenarios.md:

```text
/dilbert Resume BILL-142 from its numbered artifacts. Preserve accepted answers and show stale evidence or blockers; do not create task.md.
/dilbert rpi-scenario-check BILL-142
/dilbert rpi-plan-review BILL-142 1
/dilbert rpi-explain BILL-142 04-plan.md
/dilbert rpi-implement BILL-142 1
/dilbert rpi-review BILL-142 --working-tree
/dilbert Close BILL-142 using the actual checks and review findings. Do not publish anything.
```

Expected: reuse actual oracle decisions, report contradictions without resolving them,
implement only phase 1, record 05-implement.md, and close in 06-closure.md with accurate
status. Blocked verification remains visible. A past answer marked only as defaulted
is not confirmed merely because a deadline passed. No work is recreated to fill a gate.

For optional reconnaissance and knowledge reuse:

```text
/dilbert recon-orient BILL-142
/dilbert recon-trace BILL-142 billing
/dilbert Synthesize recon for BILL-142
/dilbert Contrast recon for BILL-142 with docs/architecture.md
/dilbert Save the confirmed billing term and approved decision from BILL-142 into the repository's existing glossary/decision notes, linking current evidence. Preserve prior entries.
```

Use actual subsystem and source paths. Expect scoped inventory, subsystem-only updates,
synthesis with unknowns, drift distinct from risk, and only confirmed knowledge promoted.
Graph creation is not required. For an explicit build use `/dilbert recon-map <repo-path>`
with the actual repository path, not the ticket ID; if graphify is absent, expect an
honest unavailable result and an offer of source-based mapping.

