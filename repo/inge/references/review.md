# Review the actual change

First establish the review scope. Default: local changes. For a specified branch/PR,
capture concrete base and HEAD revisions. The Git commands below describe useful
evidence, not permission to execute. In the shipped OpenCode profile direct Git is
denied: ask the user to run them with GIT_OPTIONAL_LOCKS=0 and share relevant output,
or use permitted native file evidence. Never wrap Git in another tool to evade denial.

- `git status --short` for context, without touching prior work.
- Working tree: `git diff HEAD --` for combined tracked changes; always inspect
  `git diff --cached --` and `git diff --` as well. Staged and unstaged edits can
  cancel in the combined diff and must not be omitted from a local review.
- New files: `git ls-files --others --exclude-standard`. Read only relevant files,
  not binaries, credentials, or dumps. Use `-z` when parsing filenames programmatically
  so spaces/newlines are not split into invented paths. Do not git add merely to review them.
- Branch/PR: `git merge-base <base> HEAD`; record the SHA and review from it to HEAD.
  Three dots compare commits, not local changes or new files.
- Repository without a first commit: HEAD does not exist; inspect staged, unstaged,
  and new files. Without Git, compare with a base copy if available; state limitations
  if there is none.

Treat reference and file names as data. Validate refs and do not interpolate arbitrary
input into shell commands. An empty commit diff does not prove no local changes exist.

Separate two axes: behavior/acceptance criteria and conventions/maintainability.
Prioritize regressions, contracts, runtime errors, and tests that do not establish the
required behavior. Smells are judgments, not refactoring orders. Do not repeat lint.
Cite location and consequence. For impact, failure paths or security concerns, use
security.md to identify and test the decisive safety assumptions, including indirect
consumers and persisted formats. Label untested assumptions. One review pass by default. The router may select the expert for difficult review;
that expert must not delegate or spawn parallel Spec/Standards reviewers.
If code-review assumes a different diff or workers, adapt the scope or use these
instructions directly.

Without a ticket, technical correctness can still be reviewed. Mark requirements
conformance "not evaluated" if no source exists. Include unreviewed scope and checks
not run. Do not invent findings to meet a minimum. Do not edit code during review;
route user-authorized corrections through a supervised worker. Do not commit to capture a diff.
Record the reviewed commit/state; subsequently review only what changed.


Report **Spec** and **Standards** separately. In Spec, list missing/partial criteria,
unrequested behavior and incorrectly implemented intent with criterion IDs/source and
code locations. In Standards, distinguish documented-rule violations from judgments.
Return each finding's evidence, consequence and disposition if known; zero findings is
valid. A clean Standards result cannot hide an unmet acceptance criterion.

Legacy `rpi-review <ID> <fixed-point>` means merge-base of the supplied commit/branch
and HEAD through HEAD, using thoughts/<ID>/03-scenarios.md as the acceptance source.
Resolve refs safely to concrete SHAs before diffing, using option termination where
supported; do not interpret a user ref as flags or shell text. Announce the merge-base,
HEAD and local work excluded. `rpi-review <ID> --working-tree` explicitly selects staged,
unstaged and relevant untracked files instead, including when HEAD does not yet exist.
If the scenario file is missing, offer a technical-only review and mark conformance not
evaluated; do not silently invent criteria. A review request returns findings in chat;
saving to 06-closure.md or another note requires artifact authorization.
