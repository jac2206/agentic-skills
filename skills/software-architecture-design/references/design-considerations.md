# Conditional design considerations

Use as prompts, not a checklist or required architecture. Select concerns that
affect the decision and tie each to evidence or an explicit gap.

- **Frontend and mobile:** client boundaries, navigation and state ownership,
  offline behavior, device limits, accessibility and release compatibility. Respect
  UI/UX decisions; do not prescribe visual design.
- **Distributed systems and events:** ownership, contracts, delivery and ordering,
  duplicates, recovery, consistency, timeouts, retries and observability. Specify
  only guarantees the design can support and verify.
- **Data and cloud:** ownership, retention, migration, backup, recovery, residency,
  capacity, operating model and cost drivers where relevant. Avoid choosing a
  provider or database without context.
- **AI, RAG and agents:** model and data boundaries, retrieval provenance and
  freshness, evaluation, prompt/data trust, tool permissions, human oversight,
  latency and cost. Do not assume an agent, vector database or autonomous action
  is needed. Refer security assessment to the specialist.
- **Evolution and migration:** current evidence and target, compatibility,
  dependencies, sequencing, data transition, rollout, monitoring and rollback;
  identify irreversible steps and unknown prerequisites. Do not imply a migration
  is reversible if unverified.

For material choices compare realistic options using relevant qualitative or
supported quantitative criteria. Record a conditional decision and evidence that
would change it; no technology is universally superior.
