# Investigate why before changing a surprising design

Anchor the question in concrete code and its revision. Inspect relevant blame,
history through renames, tests, ADRs, and linked PR/ticket discussion when available.
Use authorized external sources only when relevant to the question; no automatic
search of every connected service, private conversation, or entire repository history.

Separate current behavior, documented historical intent, and inferred rationale.
A recent commit or plausible explanation is not proof of original intent. Explain
conflicting accounts and missing sources. Stop when the scoped question is answered
or the remaining evidence cannot be obtained with available access.

For a proposed change, translate supported findings into constraints to preserve,
behavior the user wants changed, known traps to avoid, and unresolved risks. Historical
intent informs the decision; it does not override current authorized requirements.
Return findings in chat; persistence and external messages need their own scope.
