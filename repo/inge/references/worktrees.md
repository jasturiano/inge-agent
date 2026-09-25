# User-managed worktrees: handoff, not Git execution

Inge never creates, removes or changes Git worktrees/branches and never performs
integration. Suggest exact scoped commands for the user to review and run manually.
Only the scoped stash push/pop exception in WORKFLOW.md is approval-gated; other
Git mutations remain manual regardless of task-level approval.
A Git worktree is neither a sandbox nor automatic synchronization.

BEFORE: identify the intended path/branch, known base and existing changes using
permitted read-only evidence. The user creates/selects the worktree. Do not automatically stash,
commit, reset, switch branches or edit Git metadata. Ask for missing evidence rather
than running denied commands.

CONTEXT: once the user supplies an existing worktree path, use the explicitly trusted
framework. Preserve its local profile/instructions and copy only requested task
context through authorized file edits. Never copy secrets, Git metadata or a whole
repository. Do not symlink thoughts between worktrees.

DELIVERY: list changed/new files, actual checks and remaining uncommitted work.
Suggest a commit message and integration steps if useful; clearly label them
NOT EXECUTED. Uncommitted/new/ignored files do not travel through a branch merge.
Status is pending-integration until the user has integrated and evidence is checked.

INTEGRATION AND CLEANUP: the user handles commit, merge, cherry-pick, pull, push,
conflict-related Git commands, branch deletion and worktree removal. Inge may explain
conflicts or make explicitly requested source edits, but must not stage the result,
continue/abort a Git operation or apply a patch through Git. After manual integration,
inspect permitted evidence and run only checks known not to mutate Git. Distinguish
verified source changes from user-integrated delivery; never claim an action ran
merely because its suggested command was printed.
