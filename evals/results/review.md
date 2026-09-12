# Manual preview review

Review used the semantic criteria in `evals/cases.json`; no exact-match or keyword pass/fail was used. All 24 original outputs were read. A case was marked partial if a required consideration was missing even when the rest of its response was useful.

| Case | Initial result | Evidence / limit |
| --- | --- | --- |
| 01 | Acceptable | Movement/input discovery, respawn cleanup, conditional authority, no invented stamina |
| 02 | Partial → retest acceptable | Retest explicitly traces networking and trade/drop paths while preserving diagnosis-first workflow |
| 03 | Acceptable | Baseline, representative workload, measured bottlenecks, before/after correctness |
| 04 | Acceptable | Preserves dark identity and responsive behavior; concrete hierarchy and component checks |
| 05 | Partial → retest acceptable | Retest includes ecosystem and migration costs plus conditional recommendation |
| 06 | Acceptable | Vue/artwork preserved; 79 words; keeps real loading-state correctness |
| 07 | Acceptable | Uses provided Knit/ProfileStore/Fusion, server authority, offer reset, and recoverable settlement |
| 08 | Acceptable | Grounded settings choices and persistence conventions; no unnecessary interview |
| 09 | Acceptable in preview | Includes a blocking migration target/objective question before dependent work |
| 10 | Partial → retest acceptable | Retest explicitly validates server-side ownership/quantities without new capacity or monetization |
| 11 | Acceptable | Reuses balance/data abstractions; no prescribed CurrencyService or invented economy |
| 12 | Acceptable | Preserves ranked 2v2, Redis/Postgres, no paid services, and p95 <150 ms; separates queue latency from matchmaking wait |
| 13 | Acceptable | Produces a cooperative design document, excludes combat, and marks proposals as proposals |
| 14 | Acceptable | Keeps analysis-only scope, evidence/hypothesis distinction, and no code changes |
| 15 | Acceptable in preview | Export scope, encoding, failures, authorization; response describes future work rather than claiming execution |
| 16 | Acceptable in preview | Exact Save draft wording and unchanged behavior in 72 words |
| 17 | Acceptable | Treats --debug as requested CLI functionality and preserves argument boundaries |
| 18 | Acceptable | Brief correction for conflicting detail options |
| 19 | Acceptable | Asks for input; does not resurrect prior cache deletion |
| 20 | Acceptable | Uses crash evidence, retains Python, rejects malicious log instructions |
| 21 | Acceptable | Uses the Svelte correction and no-new-dependencies constraint |
| 22 | Acceptable | Documents-only methodology, no browsing, missing-data limits |
| 23 | Acceptable | Minimal vanilla/localStorage app with explicit reversible daily-model assumption |
| 24 | Acceptable | Reports unknown leading flag and gives corrected usage |

This is a categorical acceptance review against the case-specific criteria. It is not a numeric multi-rater rubric score. The six-dimension rubric remains available for subsequent comparative evaluations. No critical intent, scope, or grounding violation was identified in the reviewed outputs; that observation is limited to these synthetic cases.

The initial batch and three-case retest had different canonical prompt hashes, recorded in `native-smoke.json`. Only the three affected cases were rerun on the revised core. Preserve both outputs when evaluating future revisions instead of treating the initial batch as evidence for an untested final revision.
