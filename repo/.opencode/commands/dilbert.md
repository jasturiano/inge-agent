---
description: Investigate, clarify, save, implement, review, or evaluate architecture through Dilbert.
agent: dilbert
---
Request: $ARGUMENTS
Read dilbert/WORKFLOW.md and dilbert/references/routing.md. Route the user's intent
through the appropriate role. An empty request without usable context needs one short
question about the task. Preserve oracle decisions and native approvals.

If the request names an old rpi-* or recon-* stage, read dilbert/references/legacy-stages.md
and execute that bounded contract through the router; do not print a command as execution.
