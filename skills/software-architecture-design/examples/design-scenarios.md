# Illustrative design scenarios

These fictional examples teach behavior; they are neither prescribed designs nor
evidence of an executed system.

## New: small service

**Input:** A small team needs an internal order application with order creation
and viewing; expected load and availability targets are unknown. **Design:**
Propose one deployable application with order and persistence responsibilities;
storage technology is undecided. These are proposed boundaries. **Reason:** Fewer
operational units suit the stated team context. **Trade-off:** Independent scaling
is limited; revisit if measured workload warrants it. **Validation:** Trace both
operations to proposed responsibilities; agree on workload, recovery and access
requirements. No performance test was run.

## Evolve: existing application

**Input:** The user reports order creation and notifications are coupled; source
evidence is unavailable. **Proposal:** Inspect the call path; if confirmed and
reliability needs justify it, assess separating notification processing. Preserve
the existing contract during transition and plan rollout and recovery once delivery
requirements are known. **Risk:** Duplicate notifications and delivery guarantees
are unresolved. No queue or integration is asserted as fact; no migration test ran.

## Compare: deployment boundaries

**Input:** One team owns a functional application and has no stated independent
scaling or release requirement. **Options:** retain one deployment or split into
services. The former reduces coordination and operations; the latter may permit
independent deployment but adds network failure modes and operational cost.
**Decision:** Prefer the existing deployment provisionally; revisit if verified
team autonomy, isolation or scaling needs outweigh the cost. Availability and
workload targets remain unknown. No benchmark ran.
