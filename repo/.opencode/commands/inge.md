---
description: Investigate, clarify, save, implement, review, or evaluate architecture through Inge.
agent: inge
---
Request: $ARGUMENTS
Follow the agent's framework discovery and BOOTSTRAP.md. Read FRAMEWORK/WORKFLOW.md and FRAMEWORK/references/routing.md. Route the user's intent
through the appropriate role. An empty request without usable context needs one short
question about the task. Preserve oracle decisions and native approvals.

If the request names an old rpi-* or recon-* stage, read FRAMEWORK/references/legacy-stages.md
and execute that bounded contract through the router; do not print a command as execution.
