# Diagram catalog

Read the selected entries during modeling. Each type supports both `.mmd` and
native editable `.drawio`. Use `flowchart` for types 1–9, 11 and 13;
`sequenceDiagram` for 10; `erDiagram` for 12. These are representation choices,
not permission to flatten sequence or ER semantics into a generic graph.

C4 is an abstraction model, not a requirement to use Mermaid's experimental C4
grammar. Express its levels with stable flowchart syntax, typed labels and
boundaries. Do not use experimental `C4Context`, `C4Container`, `C4Component` or
`architecture-beta` as the default. See the [C4 diagram definitions](https://c4model.com/diagrams)
and [Mermaid C4 status](https://mermaid.js.org/syntax/c4.html).

## Architecture

### 1. C4 context — `c4-context`

- **Select for:** who uses one software system and what external systems it
  interacts with; useful for a non-specialist overview.
- **Required information:** focal system name and purpose, people/roles, external
  systems, and meaningful interactions with evidence/status.
- **Visual conventions:** one prominent focal system; distinguish people and
  external systems by symbols and typed labels; concise relationship verbs.
  Mermaid uses `flowchart LR`; Draw.io uses an actor pictogram and system cards.
- **Representation rules:** keep internals opaque; no modules, database tables,
  cloud subnets or deployment nodes. A system boundary is not a network boundary.

### 2. C4 containers — `c4-container`

- **Select for:** applications and data stores within one software system and
  their principal communications.
- **Required information:** enclosing system, applications/data stores, each
  responsibility and known technology, external actors/systems and connections.
- **Visual conventions:** a system container enclosing its C4 containers;
  application and storage symbols, external actors outside; relationship purpose
  and evidenced protocol. Use Mermaid subgraphs and native Draw.io containers.
- **Representation rules:** a C4 container is an application or data store, not
  necessarily Docker. Do not turn every internal module into a separately
  deployable application or infer deployment from this logical view.

### 3. C4 components — `c4-component`

- **Select for:** responsibilities and collaborations inside one C4 container.
- **Required information:** parent container, component names/responsibilities,
  relevant interfaces, collaborations and external dependencies.
- **Visual conventions:** a labeled parent boundary; component symbols/cards
  inside; neighboring containers outside; Mermaid subgraph for that parent.
- **Representation rules:** show the component abstraction consistently, excluding
  classes/methods unless required to clarify an interface. Components are not
  automatically independent services or deployment units.

### 4. Software components — `software-components`

- **Select for:** a logical software decomposition that does not require a
  particular C4 level, such as frontend modules or backend subsystems.
- **Required information:** components, responsibilities, exposed/consumed
  contracts, dependencies and meaningful software groupings.
- **Visual conventions:** component symbols, API/service cues, persistence
  symbols; group by module or responsibility. Use labeled directed edges and
  Mermaid classes for roles; separate editable Draw.io captions where useful.
- **Representation rules:** state the abstraction level; distinguish “calls”,
  “imports” and “implements”. Do not mix runtime hosting with logical ownership
  or infer an interface merely from a package dependency.

### 5. Layers and dependencies — `layers-dependencies`

- **Select for:** architectural dependency direction, allowed dependencies and
  observed violations across layers/modules.
- **Required information:** layers, members, actual dependencies; allowed rules
  only when supplied. Record whether edges are imports, calls or data access.
- **Visual conventions:** horizontal bands or vertical tiers, consistent reading
  direction, clear arrows; an explicit legend for allowed/prohibited edges.
- **Representation rules:** arrows point from dependent to dependency. Keep
  declared rules and observed edges distinct. Report cycles and violations;
  do not silently reverse or remove them to make the diagram look compliant.

## Infrastructure and integrations

### 6. Infrastructure / cloud — `cloud-infrastructure`

- **Select for:** hosting resources, managed services, network scopes and
  infrastructure connectivity.
- **Required information:** known provider(s) or explicit provider-neutral scope,
  resources, connections and known containment; regions, accounts/projects,
  networks and subnets only when present in the source/proposal.
  Supported provider guidance covers AWS, Azure, Google Cloud and IBM Cloud;
  choose only those evidenced or explicitly requested.
- **Visual conventions:** recognizable verified provider icons in Draw.io,
  distinct external-client zone, provider frame, relevant account/region/network
    nesting, tiered ingress/compute/data/messaging placement using the bundled
    provider diagram as a visual reference. Identify tiers as visual groupings,
    not network boundaries; omit empty or unsupported tiers. Mermaid uses typed
  service labels and subgraphs instead of unverified icon syntax.
- **Representation rules:** external systems remain outside their provider scope;
  place managed services according to documented topology rather than putting
  everything in a VPC. Mark unknown placement `TBD` and proposals visibly.
  Do not select AWS or translate services between providers by default.

### 7. Deployment — `deployment`

- **Select for:** where software artifacts/instances run in an environment.
- **Required information:** environment, deployment nodes, artifact/workload to
  runtime mapping, network connections, and known replica/placement facts.
- **Visual conventions:** nested host/cluster/runtime containers, workload symbols
  inside actual runtime boundaries, external consumers outside. Mermaid uses
  nested subgraphs; Draw.io uses movable nested objects and server/container cues.
- **Representation rules:** distinguish software artifact from instance and
  physical/logical host. Show replicas, ports, zones and scaling only when
  sourced; no icon or duplicated box implies high availability. A deployment
  view is not a CI/CD pipeline unless the requested subject is that process.

### 8. System integration — `system-integration`

- **Select for:** contracts and communication across independently bounded
  systems, including frontend/backend/external APIs.
- **Required information:** system boundaries and ownership when known,
  initiating/receiving endpoints, interaction purpose, and supplied protocols,
  contracts, authentication and sync/async distinctions.
- **Visual conventions:** separate system zones, interface/API cues, directed
  request/event paths; mark sync/async using explicit labels and a legend.
- **Representation rules:** distinguish requests from callbacks and responses;
  annotate trust boundaries only when established. Do not infer authentication,
  retries or a reverse channel from a single integration edge.

### 9. Events and messaging — `events-messaging`

- **Select for:** asynchronous publication, routing, subscriptions and consumers.
- **Required information:** producers, event/message names, topics/queues/brokers,
  consumers and evidenced routes; known delivery and ordering guarantees.
- **Visual conventions:** producer → channel/router → consumer tiers; queue and
  topic symbols; event labels and clearly differentiated competing consumers
  versus fan-out. Group by ownership where known, not by decorative service type.
- **Representation rules:** distinguish event, command, topic and queue. Model
  retries, DLQs, outbox, acknowledgments, ordering and delivery guarantees only
  when supplied; absence stays unknown. Do not turn broker routing into a
  direct synchronous service call.

## Behavior and processes

### 10. Sequence — `sequence`

- **Select for:** ordered interactions for one bounded scenario or use case.
- **Required information:** participants, initiator, ordered messages, sync/async
  and returns when known, guards and alternative/repeated paths when supplied.
- **Visual conventions:** participants horizontally, time downward; distinct
  calls and returns, labeled messages, optional activations and `alt`/`opt`/`loop`
  fragments. Mermaid uses `sequenceDiagram`; Draw.io uses native participant
  heads, dashed lifelines, attached message connectors and fragment frames.
- **Representation rules:** preserve message order, direction, call/return and
  guards. A dashed lifeline is not a message. Do not invent return content or
  parallelism. Attach messages to lifelines/anchors so they move with participants;
  record message IDs/order separately from decorative cells. Icons belong in
  participant heads only when compatible and useful.

### 11. Process flow — `process-flow`

- **Select for:** steps, decisions and outcomes of a technical/business process.
- **Required information:** entry, actions, decisions and conditions, branches,
  outcomes and loops; responsible roles only when known.
- **Visual conventions:** readable top-down or left-right flow, distinct start/end,
  actions and decision diamonds, labeled decision exits; optional role swimlanes.
  Mermaid uses stable flowchart shapes; Draw.io uses editable flowchart symbols.
- **Representation rules:** each decision exit carries its condition; distinguish
  parallel execution from exclusive branches. Preserve failure paths supplied by
  the source. Do not add success/error paths merely for visual symmetry.

## Data

### 12. Entity-relationship — `entity-relationship`

- **Select for:** entities, attributes, keys and relationship cardinalities in a
  conceptual, logical or physical data model; state the chosen level.
- **Required information:** entities, sourced relationships, cardinality and
  optionality; attributes, data types and PK/FK/UK only when supplied by that level.
- **Visual conventions:** Mermaid `erDiagram`; native editable Draw.io entity
  tables and crow's-foot relationships with key/attribute compartments. Maintain
  type/name/key rows, legible relationship captions and numeric multiplicities
  when the editor's crow's-foot support cannot be verified.
- **Representation rules:** cardinality belongs at both ends; identifying and
  non-identifying relations differ. Do not infer a physical FK from a conceptual
  association. Unknown cardinality cannot be expressed truthfully by inventing
  `||` or `o{`: omit that relationship from the ER notation and list it in a visible
  “relationship unresolved” note in both formats until clarified. Keep the
  unresolved relationship in the working model. Table notation itself is the
  identifying visual symbol; do not replace entity rows with cloud/database logos.

### 13. Data flow — `data-flow`

- **Select for:** what data moves between external entities, transformations and
  stores, including scoped DFD levels.
- **Required information:** scope/level, external entities, numbered processes,
  stores, named data flows and known trust/sensitivity boundaries.
- **Visual conventions:** distinct external-entity, process and store symbols;
  directed, noun-labeled flows. Mermaid uses a flowchart with explicit typed
  labels/classes; Draw.io uses native DFD symbols or clearly labeled equivalents.
- **Representation rules:** depict data movement, not control order or timing.
  Keep one level per view; balance external inputs/outputs across decomposition.
  External-to-store or store-to-store direct paths require explanation when
  outside the selected DFD convention; never add an unsupported process to fix
  them. Show sensitive data and trust boundaries only when supported.
