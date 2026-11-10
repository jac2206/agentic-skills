# Usage Examples

### Example 1 — Documenting a REST use case

**Input**

A backend exposes `POST /orders`, whose route applies an authentication
middleware, validates a `CreateOrderDto`, calls `CreateOrder`, persists through
`OrderRepository`, and publishes `OrderCreated`.

**Expected behavior**

Trace that route through the actual controller, application service, domain
objects, repository, and event publisher.

Document only the fields and status or error contracts confirmed by validators,
implementation, schemas, or tests.

Generate the use-case flow diagram showing the actual execution path, including
authentication, validation, order creation, persistence, event publication, and
the final response when those behaviors are confirmed by the implementation.

Link the use case from `docs/main.md` and omit sections for components not present.

### Example 2 — Missing evidence

**Input**

A controller calls `PaymentGateway`, but the repository contains no provider
configuration, implementation, tests, or response contract.

**Expected behavior**

Document the observed call as an external dependency.

Identify the available evidence and mark provider details, authentication,
timeout behavior, and failure mapping as unresolved.

Do not invent a provider, payment flow, or error code.

If the flow diagram includes the external dependency, represent only the confirmed
call to `PaymentGateway` and do not infer the underlying provider.

### Example 3 — Existing diagram requires synchronization

**Input**

An existing use-case document contains a Mermaid diagram showing:

```text
Controller
  ↓
UseCase
  ↓
Repository
  ↓
Database
```

The current implementation now performs an authorization check and publishes an
event after persistence.

**Expected behavior**

Update the documentation and diagram to reflect the current implementation.

The resulting flow should include the confirmed authorization step and event
publication.

Remove or update any obsolete flow elements.

Do not modify unrelated documentation.

### Example 4 — Specification and registered route disagree

**Input:** An older specification names `POST /accounts/refresh`, while the
current route registration and use-case documentation show `POST /auth/refresh`.
No decision identifying the authoritative specification is available.

**Expected behavior:** Trace registration prefixes and the handler to confirm
the active route; cite the spec, route and documentation paths. Document the
observed implementation and flag the intended-contract conflict. Do not silently
edit the specification, infer its status or change the route; hand the decision
to the specification and implementation owners.

