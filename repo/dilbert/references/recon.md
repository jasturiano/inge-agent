# Optional reconnaissance and cross-repository evidence

Recon supports unfamiliar code and architecture's actual-evidence pass. It is optional;
targeted ticket research must not trigger a full inventory or graph build. Establish the
requested repository/path, scope, subsystem, evidence revision, and output before acting.
Use scout for bounded inventory/lookup, expert for difficult traces/synthesis, and a
worker for authorized persistence. Short traces may stay with the router. No new roles,
nested delegation, or concurrent writers. Readers return proposed artifacts, never writes.

## Graph operation

An explicit graph build/refresh request authorizes only the requested repository graph
through native approvals, not a filesystem-wide crawl or application edits. Inspect the
installed graphify skill/tool and its actual invocation, output locations, costs, and
side effects before running it; do not assume local-only parsing or no model calls.
Do not simulate invoking a slash command by printing it. A reader cannot build through
Bash. A worker must use the permitted tool with applicable native approval; if the
graph operation cannot preserve required write controls, report that limit and leave
the concrete command for the user to run, never bypass an edit denial through shell.

For an existing graph, inspect its repository, scope, source revision/date, and known
gaps. Query only if relevant and current; stale edges need source confirmation. Building
or refreshing is not implied by a query. If graphify is unavailable, say the graph
operation is unavailable and offer source-based mapping, labeled as such.

After a requested build, check actual queryability for entry points, top-level modules,
and external dependencies. Report command/tool, target, graph location/revision, query
results and limits. Preserve EXTRACTED (explicit evidence) versus INFERRED (inferred
relationship); neither proves live execution. Record in recon/00-graph.md only if saving
was requested. A missing graph does not block source-based inventory or tracing.

## Inventory, trace, synthesis, contrast

For a new compact recon request, save one report when useful. For numbered recon notes,
use `thoughts/<ID>/recon/` and the following output contracts. Load existing content first;
update only requested sections, retaining IDs, evidence and unrelated subsystem notes.

| Operation | Read / inspect | Output content |
|---|---|---|
| Inventory | Requested repo, current graph if available, manifests/CI/config and decisive source | 01-inventory.md: stack/frameworks, entry points, modules, config/infra surface, external systems, explored scope and unknowns; evidence per item, no architecture verdict |
| Trace `<subsystem>` | Inventory plus relevant source/graph | 02-flows.md: named subsystem only; entry → handler/service → state/output/effects, evidence at each hop, seams, external dependencies, EXTRACTED/INFERRED, untraced paths and why |
| Synthesize | 01-inventory.md and 02-flows.md | 03-architecture.md: observed shape, critical flows, contracts/invariants, coupling hotspots, unknowns; every claim linked to supporting notes, description without fixes or score |
| Contrast | Explicit declared docs plus flows/synthesis | 04-drift.md: claim/source, actual evidence, MATCH / MISMATCH / UNDOCUMENTED / NOT_VERIFIED, scope/date; drift separate from risk, no automatic fixes |

Synthesis must carry uncertainty forward. If notes cannot support a claim, report the
gap or request a bounded source check, updating evidence before synthesizing; do not
launder an inference into fact. Recon synthesis may feed A2-actual with provenance.
There are no missing `/recon-arch` or `/recon-drift` commands to invoke: use `/dilbert
Synthesize recon for <ID>` or `/dilbert Contrast recon for <ID> with <declared-source>`.
Those explicit artifact-producing requests authorize only the table's saved output.

## Boundaries and diagrams

For a multi-repository request, inspect only identified, authorized repositories. Keep
one graph per repo if using graphs, not a mandatory combined graph. Trace by flow. At
each boundary record caller, callee if known, direction, protocol, data/schema crossing,
assumed guarantees, and source/revision. For mid-tier services record inbound and outbound.
Do not guess the far side of an HTTP call, queue, shared database, or external dependency.

Match explicit outbound evidence to inbound evidence and report:

- MATCHED: both sides agree on the relevant contract; cite both.
- MISMATCH: evidence on both sides disagrees; state the consequence without inventing it.
- UNRESOLVED: missing counterpart, ambiguous mapping, or unknown contract; name the next
  authorized source needed. An inbound with no observed caller is not proof it is unused.

Quality scenarios for cross-service behavior must include relevant boundary crossings.
For a diagram request, use the verified boundary map or actual-architecture evidence,
label connections with protocol and evidence IDs, and distinguish mismatched/unresolved
edges visually (Mermaid by default when suitable). Preserve unknowns rather than drawing
a healthy-looking topology from guesses. Diagrams may be returned in chat; saving them
needs artifact authorization. Publishing/HTML tooling is not implied.
