# Repository-local profile

Optional template: keep the filled profile in the target repository's inge/PROJECT.md,
not in a shared framework. Fill in only what is known. "To discover" does not block investigation. This file
is not executable configuration and does not authorize commands by itself.

- Usual context: brownfield (confirm per ticket).
- Oracle/owner: to discover.
- Stack and conventions: read the repository's own guidance.
- Platforms and tooling: discover per task; no default cloud or provisioning tool.
- Infrastructure scope: relevant accounts/projects/subscriptions, clusters or sites;
  record identifiers only when needed and appropriate.
- Usual checks (exact commands): discover in manifests/CI.
- Safe test environment: confirm before executing external effects.
- Operations requiring additional approval: deployments, migrations, external changes.
- Models: capability roles mapped by the active adapter; effective harness configuration is authoritative. See references/routing.md.
- Verification recipe: existing project-local launch/health/exercise/evidence/cleanup guide, if any.
- Mandatory permission restrictions: discover effective global/repository rules; preserve stricter denials in every role.
- Optional skills available: confirm in the harness catalog.
- Graph: use only if present with known revision/scope; original evidence is authoritative.
- Branch/workspace: current by default; user creates/selects worktrees manually. Only explicitly approved stash push/pop may change Git state.

Record stable, discovered, approved commands and constraints here. Do not store
credentials, private dumps, or complete sensitive inventories.
