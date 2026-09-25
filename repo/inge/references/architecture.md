# Architecture: proportional A0-A5 without infrastructure changes

For greenfield, begin with goals, constraints, actors, interfaces and operations;
compare viable designs against agreed quality scenarios. Existing-system drift
sections can be marked not applicable. Do not invent an A2 deployed system.

For improvement requests, prioritize the user's pain point or actively changing
areas from recent history. Consider how much callers must understand, where behavior
is testable, and whether removing an abstraction would eliminate complexity or
scatter it across consumers. Propose alternatives with evidence and tradeoffs,
not speculative cleanup of untouched code. Respect existing domain language/ADRs.
Use history.md for surprising design choices and security.md for trust boundaries.

Use this sequence as report sections, not six mandatory sessions. Inge returns
the report in chat; the router can delegate saving it to `thoughts/<ID>/architecture.md` through a worker
with approval. Six separate files are unnecessary. For a descriptive map, A2 and
limitations suffice. For an evaluation, apply the following.

A0 INTENT: bound the system, environment, decision, oracle, and prioritized qualities
(e.g. recovery, availability, security, cost). Ask what blocks judgment. Inventory may
proceed while intent is clarified; do not invent thresholds.
A1 CLAIMED: documents, diagrams, ADRs; cite source/section and date when known.
Record components/responsibilities, flow guarantees, decisions and non-goals as claims,
without correcting them from code. Inspect diagrams as images when needed; disclose any
unreadable/unavailable source rather than claiming it was reviewed.
A2 ACTUAL: structure, flows, contracts, dependency directions and triggers from sources.
Locate persistent state, behavior-changing config, and secret handling locations without
exposing values. Examine cycles/coupling/churn when relevant, not as mandatory metrics. Separate observed
from inferred and unverified scope. When independence from A1 is needed, leave a note
and request a new A2 session with A0 only. Do not claim independence if this context
has already read A1.
A3 CONTRAST: MATCH / MISMATCH / UNDOCUMENTED / NOT_VERIFIED. Link each scoped claim
and actual row; include unmatched actual evidence and unknown coverage. Define MATCH as
supported agreement, MISMATCH as evidenced disagreement, UNDOCUMENTED as actual evidence
absent from scoped claims, NOT_VERIFIED as insufficient evidence. Summarize counts if useful. Absence from a summary
is not proof of nonexistence. Record drift separately from risk.
A4 SCENARIOS: agree on concrete situations, expected responses, and measurable criteria
with the oracle. Preserve quality/scenario IDs and owner confirmation. Trace only the
selected quality when requested, using A2 to locate decisive source/operational evidence.
Record scenario ID, handled / partial / not handled / unverified, trace and evidence
limits. A missing observation is unverified, not a demonstrated failure. Do not invent
thresholds or treat drafted cases as owner-confirmed; other quality sections stay intact.
A5 RESULT: each risk has evidence, a related scenario or drift finding, impact,
tradeoff when supported (otherwise unknown), and next check or recommendation.
Do not infer why the original designers chose something without evidence. A citation alone does not establish impact.
Include demonstrated strengths without a minimum quota. Prioritize impact/uncertainty.
Do not automatically turn recommendations into tickets.

Infrastructure and platforms: distinguish documented design, desired configuration
(IaC or other provisioning sources), deployed state, and operational behavior.
Do not assume a provider, orchestrator, network model, or deployment tool. Identify
the actual platforms and management boundaries first; the system may span public
cloud, private cloud, on-premises infrastructure, or several of these.
A code graph does not replace a deployed-resource inventory. Record each evidence
source's environment, collection date, scope, and platform-specific identifiers
where relevant (account/project/subscription, region/zone, cluster, site/datacenter).
Use authorized read queries and minimize sensitive data. Without access, request
relevant exports, not credentials. Declare inventory coverage gaps.
Consult current documentation for the actual services, products, and versions before
claiming behavior. Use a provider or industry architecture framework only when it
fits the task; it guides questions, not mandatory findings.

Possible scenarios, depending on objectives and actual topology: loss of a relevant
failure domain (zone, site, cluster, or host), verified restoration, excess load,
dependency failure, and access boundaries. Do not assume that similarly named failure
domains provide equivalent guarantees across platforms. Do not invent RTO/RPO or
claim recoverability merely because backups exist. Request observations or authorized
tests as needed; a review does not authorize production failure simulations.

For existing legacy reviews, preserve A0-A5 numbered artifacts and approved scenarios.
The compact report is for ordinary requests, not a requirement to consolidate old files.
See `legacy-stages.md` for exact stage inputs/outputs and `recon.md` for optional
inventory, traces, boundary maps and evidence-based diagrams. A requested report orders
intent → drift → scenario results → risks/strengths → open questions/owners. Visual
outputs are optional and must cite actual evidence and retain unknowns. No automatic
HTML/atlas generation, publication, or remediation is implied.
