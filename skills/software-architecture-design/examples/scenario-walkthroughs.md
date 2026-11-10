# Scenario walkthroughs

Manual, hypothetical walkthroughs of version 1.0.0 against the inputs below.
These exercise the written decision rules, not a running application, independent
agent invocation, benchmark, security audit, or proof of production behavior.
All components and choices below are proposed unless explicitly described as
reported; absent targets remain unknown. Each walkthrough checks a proportionate
result, pattern neutrality, and the stated uncertainty.

| Scenario and supplied context | Walkthrough result and verification boundary |
| --- | --- |
| 1. Small backend; one team, basic operations | Design: consider a single deployment and compare a split only if justified. Load and security targets unknown; no benchmark. |
| 2. Modular monolith; reported module coupling | Analyze first, then evolve only the evidenced boundary; current coupling requires source verification. No service split assumed. |
| 3. Existing microservices; reported release friction | Analyze ownership and release evidence; compare coordinated improvement and consolidation. No assumption that services should remain or be merged. |
| 4. Event-driven system; reported duplicate events | Review delivery and consumer behavior, then consider idempotency if supported. Ordering and guarantees unknown; no queue invented. |
| 5. Frontend with multiple modules; inconsistent state ownership reported | Analyze actual dependencies and state boundaries; propose a scoped change if evidence supports it, respecting UX decisions. No microfrontend mandate. |
| 6. Mobile app; offline requirement supplied without duration | Design with offline behavior as an open requirement; assess synchronization and compatibility. No storage or availability guarantee assumed. |
| 7. Full-stack feature; create and view records required | Design the smallest necessary client/server contract and responsibilities; authentication and targets remain unknown. No framework prescribed. |
| 8. Cloud solution; budget constrained, provider unspecified | Compare operating and cost implications of viable hosting options; pricing and load are unknown, so no invented cost comparison or provider choice. |
| 9. AI question answering; source traceability required | Compare retrieval-supported and simpler approaches where viable; define provenance and evaluation needs. No agent or vector database assumed. |
| 10. Architectural refactor; behavior must remain compatible | Evolve only after verifying current interfaces; propose staged change, contract checks and conditional rollback. No migration test claimed. |
| 11. Technology migration; existing data must survive | Compare retain versus migrate, identify data transition and recovery evidence, test compatibility; reversibility remains unverified. |
| 12. Existing project; architecture documentation conflicts with code | Analyze without modifying files; inspect relevant relationships and report observed evidence, conflict and unknown authority. No current component inferred solely from docs. |
| 13. Small technical change; no architectural driver supplied | Explain a local change may suffice; no redesign, ADR or diagram required. Further implications depend on project evidence. |
| 14. Strict cost ceiling reported but amount missing | Compare operational complexity and cost drivers qualitatively; ask for ceiling if it determines feasibility. No invented cost or scalability target. |
| 15. Missing non-functional requirements | Design conditionally, mark latency, availability and workload unknown, and request targets before claiming satisfaction. Validation status is unverified. |

No diagram was needed for these bounded walkthroughs. The examples in
[design scenarios](design-scenarios.md) provide concrete proposed boundaries and
comparison; neither those examples nor this review prove runtime execution.
