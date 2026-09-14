# Optional worktrees: delivery and integration

Only when requested by the user. This kit does not automate merges or worktree
creation. Dilbert coordinates; a supervised worker executes authorized operations.
Git worktree is neither a sandbox nor branch synchronization. One worker by default.

BEFORE: record target path/branch, base SHA, dirty state, and scope. If the task depends
on the user's uncommitted changes, agree how to preserve/transfer them. Do not stash,
commit, reset, or copy everything automatically. Create a separate worker branch
from the confirmed base at an authorized path.

CONTEXT: install the same local `.opencode/commands/` and `dilbert/` directories in
the worktree using approved copies. Copy only relevant `thoughts/<ID>/` content,
never secrets or the full history. Excluded files do not travel through Git.
Do not symlink thoughts between workers; they can overwrite each other. Verify
repository instructions and check commands are available. Preserve the primary note.

DELIVERY: record worker path, target branch/base, authorized commits or proposed patch,
new files, remaining dirty files, and checks with revision in task.md. If commits
were not authorized, explicitly deliver the diff and new files; merging a branch
will not transport them. Status: pending-integration, not complete.

INTEGRATION: show the change and target before asking for approval. Verify the target
has not changed since inspection and preserve the user's work. Choose merge,
cherry-pick, or patch application according to approval; do not execute several
"just in case". If conflicts occur, report files and decisions; do not resolve them
by discarding one side. After integration, review the result and relevant checks
IN THE TARGET. Record the resulting revision and update the primary note without
overwriting newer decisions. If validation fails, mark integrated-with-failures/blocked,
not "verified".

CLEANUP: do not delete the worktree/branch without approval and verification that
changes, new files, and necessary artifacts are preserved. Do not use remove --force.
