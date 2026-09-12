# Validation record

Run date: **September 11, 2026 (Pacific time)**. This records observed behavior, not a guarantee for every model, host, or project.

## Deterministic checks

- 18 Python `unittest` checks passed locally on Windows / Python 3.12.10.
- Generated bundles matched canonical sources byte-for-byte.
- The bundled Codex skill passed Codex skill-creator's `quick_validate.py`.
- Installation tests covered all four adapter layouts, idempotence, paths with spaces/Unicode, dry runs, preflight conflicts, forced-update backups, invalid parents, and linked-path rejection.
- GitHub Actions runs the suite on Windows and Ubuntu with Python 3.10 and 3.12. Current remote status is visible in [Actions](https://github.com/backyarddd/promptly/actions).

These checks validate packaging and installation mechanics, not the quality of generated prompts.

## Independent behavioral forward-test

An independent Codex subagent, using the parent session's inherited GPT-6 model with no model override, received only the generic skill and blind raw scenarios. It did not receive expected answers or the grading rubric. The 24 scenarios were processed as separate stated contexts in one batch; non-option scenarios were forced to preview.

The initial run produced 21 enhanced prompts, two usage corrections, and one empty-request clarification. Every response fit its fixture's soft word ceiling; the shortest task expansion was 72 words and the longest was 409 words. A manual semantic review judged 21 cases acceptable and three partial:

| Case | Initial gap | Narrow change and retest |
| --- | --- | --- |
| 02: inventory duplication | Did not explicitly cover network entrypoints and trade/drop integrations | Added conditional inventory diagnosis guidance; retest covered those paths and root-cause-first validation |
| 05: database choice | Did not explicitly compare ecosystem fit and migration costs | Added those infrastructure comparison criteria; retest incorporated them without authorizing migration |
| 10: inventory | Referred to authoritative state but did not explicitly require server mutation validation | Added the ownership/quantity invariant; retest included server validation and rejected invalid mutations |

All three retests met their case criteria. The other 21 cases were not rerun after this narrow prompt revision. Read the [initial outputs](../evals/results/initial-preview.json), [targeted retest outputs](../evals/results/targeted-retest.json), and [review notes](../evals/results/review.md).

Limitations: this was a single-model batch smoke test with manual review by the implementing agent. It was not a blind multi-rater study, isolated repeated trials, or a measured improvement over a baseline prompt. Preview preparation does not validate default execution; that was tested separately below.

## Native host smoke tests

Each test used an isolated disposable project with this one-line fixture:

```html
<!doctype html><button id="save" onclick="window.saved=true">Save</button>
```

The request was to rename the button to `Save draft` while preserving click behavior. No permission bypass flags or model overrides were used. Claude's normal `acceptEdits` mode and Codex's `workspace-write` sandbox allowed local fixture edits.

| Host/version | Test | Observed result |
| --- | --- | --- |
| Codex 0.153.2 | `$promptly --compact ...` | Agent loaded the native skill, changed the label, preserved the ID and handler, and reported the result |
| Codex 0.153.2 | `$promptly --show --compact ...` | Returned the enhanced instruction; fixture hash unchanged |
| Codex 0.153.2 | `$promptly --no-run --compact ...` | Returned the enhanced instruction; fixture hash unchanged |
| Claude Code 2.1.261 | `/promptly --compact ...` | Changed the label and preserved the ID and handler; successful completion with no denied permissions |
| Claude Code 2.1.261 | `/promptly --show --compact ...` | Returned the enhanced instruction in one model turn; fixture hash unchanged |
| OpenCode 1.18.25 | Native `run --command promptly` preview | Exported session contained the canonical prompt and substituted request, with no unresolved argument placeholder. Provider rejected the model request with HTTP 404: no endpoint supporting tool use |

Claude reported the configured model as `claude-opus-5[1m]`. Codex used its configured model; the CLI event stream did not report a model identifier, so it is not inferred here. The actual request/result summaries are in [native-smoke.json](../evals/results/native-smoke.json).

The edited fixture was inspected at source level; its unchanged inline handler was verified. No interactive browser click test was performed. Native previews used this small fixture rather than a broad adversarial tool-use test. Full OpenCode generation/execution, interactive UI discovery, all flag combinations on every host, arbitrary generic hosts, and repeated multi-turn context retention remain unverified.

No credentials or raw host logs are included in this repository. The published behavioral outputs contain only synthetic task context.
