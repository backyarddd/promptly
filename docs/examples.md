# Example expansions

These examples are illustrative, not deterministic snapshots. In default mode Promptly prints the complete rewritten prompt under `Promptly prompt:` before continuing. Use `--show` to inspect without execution.

## A feature request stays bounded

```text
/promptly add keyboard shortcuts to the editor
```

> Inspect the existing editor input and command architecture, then add shortcuts using its conventions. Preserve current mouse and accessibility behavior, handle conflicts with browser or operating-system shortcuts, and keep the change limited to the requested commands. Verify the shortcuts in the supported layouts and run relevant existing checks.

## A duplication bug is a diagnosis task

```text
/promptly records sometimes duplicate after retry; fix it
```

> Reproduce or trace the duplicate-record path, including request handling, persistence, retries, concurrent operations, and reconnect behavior. Distinguish observations from hypotheses and establish the failing transition before changing code. Apply the smallest fix that preserves identity and consistency invariants, add focused regression coverage when appropriate, and report evidence and remaining limitations.

## Optimization starts with evidence

```text
/promptly optimize the application
```

> Establish a representative scenario and baseline before changing code. Inspect available profiling tools, measure the relevant bottlenecks, and prioritize bounded improvements that preserve behavior. Compare the same scenario before and after; if profiling is unavailable, provide a reproducible measurement plan rather than presenting guesses as findings.

## A database question is not automatically a migration

```text
/promptly --research should we use PostgreSQL or MongoDB?
```

> Recommend a storage choice for the intended workload. Establish relationships, access patterns, consistency needs, scale, deployment constraints, and team context from available evidence; state assumptions where they are unknown. Compare fit, operations, ecosystem, costs, and migration implications using current primary sources for changeable claims. Deliver a concise recommendation and unresolved decision criteria without changing the database.

## UI polish retains identity

```text
/promptly make the settings screen easier to use
```

> Inspect the relevant screen and design conventions, then improve hierarchy, spacing, labels, states, keyboard focus, and responsive behavior while retaining the established visual identity and interactions. Reuse existing components and keep the change within the requested area. Summarize visible changes and verification.

## A trivial edit stays trivial

```text
/promptly --no-run --compact rename the Save button to Save draft; don't change behavior
```

> Locate the existing Save button and change only its displayed label to “Save draft,” preserving its handler, state, and layout. Update related localization or accessibility text if applicable. Return this prompt only; do not edit files or run checks.

## An important missing decision

```text
/promptly migrate the entire backend
```

If context and inspection cannot establish the target or intended outcome, ask one focused question before dependent work. Do not invent a platform, architecture, or migration plan to fill a consequential missing decision.
