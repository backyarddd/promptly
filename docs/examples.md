# Example expansions

These are illustrative expected outputs, not deterministic snapshots or claims of a completed implementation. Native default mode uses the improved instruction internally; use `--show` to inspect it. Substitute `$promptly` in Codex.

## Sprinting without invented stamina

```text
/promptly add sprinting
```

Context: an existing Roblox game.

> Add sprinting using the existing movement and input architecture. First inspect character/controller code, supported devices, movement states, and any existing sprint or stamina abstractions. Reuse those conventions; do not introduce a stamina mechanic.
>
> Integrate sprint input and speed transitions without overriding other movement effects. Handle release/cancel, death, respawn, and character cleanup. Follow the game's authority model for gameplay-relevant speed. Verify transitions and lifecycle behavior using existing tooling or a repeatable playtest, then report changes and validation.

## A duplication bug is a diagnosis task

```text
/promptly my inventory sometimes dupes items fix it
```

> Diagnose and fix intermittent inventory duplication. Inspect item identity, inventory mutations, persistence, remote handling, retries, concurrent operations, and reconnect behavior. Trace trade/drop paths if present. Reproduce the issue or gather evidence that identifies the failing transition; distinguish observations from hypotheses.
>
> Apply the smallest fix that preserves ownership and quantity invariants. Avoid a broad inventory rewrite. Add meaningful regression coverage for the demonstrated scenario, including retries/concurrency where implicated. Run relevant checks and explain the cause, fix, evidence, and remaining reproduction limitations.

## Optimization starts with evidence

```text
/promptly optimize the game
```

> Establish a representative scenario and baseline performance before changing code. Inspect available profiling tools and measure relevant CPU, memory, rendering, network, and update-loop costs. Identify the highest-impact bottlenecks, including allocations, polling, object churn, or remote traffic only where measurements implicate them.
>
> Prioritize bounded improvements, preserve gameplay behavior, and compare the same scenario before and after. Report measured impact and methodology. If profiling is unavailable, identify the missing evidence and provide a reproducible measurement plan without presenting guesses as findings.

## A database decision, not a migration

```text
/promptly research whether I should use postgres or mongodb
```

> Recommend PostgreSQL or MongoDB for the user's intended workload. Use available project context to establish data relationships, query/access patterns, consistency needs, scale, deployment constraints, and team experience. Where these remain unknown, state the assumptions and conditions that would change the recommendation.
>
> Compare fit, operational complexity, ecosystem, cost drivers, and migration implications using current primary sources for changeable claims. Cite the evidence and distinguish it from judgment. Deliver a concise comparison, a recommended default with reasons, and the key unresolved decision criteria. Do not implement a database change.

## UI polish retains identity

```text
/promptly make the UI look better
```

Context: a responsive app with an established restrained dark identity.

> Inspect the relevant screens and design system, then improve visual hierarchy, spacing, typography, color consistency, and component states while retaining the restrained dark identity. Reuse existing components and keep the work within the requested UI area. Preserve interactions and check legibility, keyboard focus, and responsive behavior on the app's supported layouts. Summarize the visible changes and verification.

## A trivial edit stays trivial

```text
/promptly --no-run --compact rename the Save button to Save draft; don't change behavior
```

> Locate the existing Save button and change its displayed label to “Save draft,” preserving its handler, state, and layout. Update the corresponding localization/accessibility text if applicable. Verify the label in context and run any relevant existing check; do not add new infrastructure.

## An important missing decision

```text
/promptly migrate the entire backend
```

If available context and inspection do not establish the migration target:

> What platform or technology should the backend migrate to, or what outcome is the migration intended to achieve?

For `--show`, the improved instruction instead tells the executor to resolve that question before dependent changes. Reversible details such as menu spacing do not trigger the same stop.
