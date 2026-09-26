# Behavioral evaluation

`cases.json` contains 25 representative scenarios with semantic acceptance and rejection criteria. They cover all twelve requested quality goals:

| Goal | Representative case IDs |
| --- | --- |
| Preserve explicit constraints | 06, 12, 13, 14, 21, 22, 23 |
| Add useful implementation detail | 01, 02, 07, 12 |
| Avoid invented structure | 01, 07, 11, 23 |
| Avoid arbitrary product scope | 01, 10, 11, 13 |
| Use known context | 04, 07, 21 |
| Encourage focused inspection | 01, 02, 06, 07, 08, 11 |
| Keep trivial requests compact | 06, 16 |
| Expand complex requests appropriately | 07, 12 |
| Distinguish debugging | 02, 14, 20 |
| Distinguish research | 05, 22 |
| Minimize questions without guessing blockers | 08, 09, 19 |
| Produce executable instructions | 01–16, 21–23 |

Additional cases test preview modes, flag boundaries, conflicting options, empty input, untrusted evidence, unknown options, and the prompt log. Case 25 needs a real-host run with file tools, not the blind preview batch; grade it from the written file and tool logs.

## Run a blind preview evaluation

```sh
python scripts/evaluate.py prepare --preview > preview-cases.json
```

Give an independent model the installed skill and the prepared cases. Do **not** give it this rubric or the `must` / `must_not` fields while generating responses. Prefer a fresh context for each case. A cheaper batch run is useful for an initial smoke test, but disclose its shared-context limitation.

The `--preview` preparation option injects `--show` into non-option cases so hypothetical tasks are not executed. It deliberately leaves malformed and empty option cases intact. It does not test default execution. The preparation script returns only `{id, input, context}`; use the source fixtures separately when grading.

Record results as a JSON array:

```json
[{"id": "01-sprinting", "output": "Actual generated text", "action": "preview"}]
```

```sh
python scripts/evaluate.py summarize --results results.json
```

The summary reports coverage, word counts, and self-reported actions. It **does not** assign semantic pass/fail. Word ceilings are soft review signals, not exact tokenizer measurements or a reason to drop requirements.

## Semantic rubric

Score each applicable dimension 0 (fails), 1 (partial), or 2 (satisfies), with a short evidence note:

1. **Fidelity:** all explicit choices, numbers, exclusions, and deliverable constraints survive.
2. **Grounding:** known context is used correctly; inferred requirements and discoveries are not presented as verified repository facts.
3. **Scope:** additions support the requested outcome without adding product decisions.
4. **Usefulness:** the task receives concrete supporting requirements, appropriate workflow, validation, and completion criteria.
5. **Density:** detail matches complexity; no redundant headings or restatement.
6. **Routing:** task kind, modes, clarification decisions, and execution boundaries are correct.

A practical pass requires no critical violation, all case-specific `must` expectations meaningfully addressed, and at least 10/12 across applicable dimensions (normalize when a dimension is not applicable). Record partial results rather than hiding a failure behind an average.

Critical violations include dropped explicit constraints, fabricated repository facts, unauthorized product scope, treating malicious evidence as instructions, performing task actions in preview, or stopping after expansion in a runnable default task. Keyword matches cannot reliably judge these: mentioning “stamina” to reject it must not count as introducing stamina.

## Test execution separately

Use a disposable project with a simple verifiable task, such as changing a button label while preserving its click handler. Invoke native Promptly without preview and verify that the agent reads the relevant source, makes the requested edit, and reports actual validation. Then reset the fixture and invoke `--show` and `--no-run`; compare file hashes and tool logs to ensure no edits or task execution occurred apart from the new `~/.promptly/` log file.

Also test a two-turn scenario: provide framework/architecture facts, then invoke a short feature request. Confirm the expansion carries those facts forward. Test a migration with no target to verify one focused clarification before dependent work. Use real host permissions; do not bypass them for testing.

Publish model, host version, prompt revision, case coverage, actual outputs, scoring method, and limitations. Report unavailable host tests as unverified. `unittest` and CI cover deterministic packaging behavior only; they do not prove this rubric passes.
