# Validation record

Promptly's required checks cover deterministic packaging and installation. Prompt behavior evaluations are optional/manual: a prompt edit does not require rerunning model trials, and this repository does not claim fresh behavioral results for every revision.

## Deterministic checks

Run from the repository root:

```sh
python scripts/promptly.py build --check
python -m unittest discover -s tests -v
```

The suite checks generated-bundle drift (including unexpected files), one embedded core per bundle, adapter argument slots, all project and user destination mappings, aliases installing only the portable generic bundle, conflict preflight, backups, dry-run behavior, and linked-path rejection. It does not call a model or overwrite a user's installed skill.

The Codex bundle can also be checked with the Agent Skills quick validator when that validator is available. Generic-bundle validation should use the same frontmatter and body checks supported by the target host.

## Optional prompt evaluation

The [fixtures](../evals/cases.json) and [rubric](../evals/README.md) are useful for deliberate investigations of prompt behavior. They are not a per-edit CI gate. Run them when comparing a substantial semantic redesign, investigating a regression, or preparing a release claim; report the model, host, revision, cases, and limitations. Do not present fixture output as proof of broad model quality.

## Native support boundary

Deterministic installation does not prove host discovery or execution. Verify those separately with a disposable project and the host's own command or picker. The additional presets target documented local Agent Skills paths, but Pi, Cursor, DeepSeek Harness, Grok Build, Muse Code, Gemini CLI, GitHub Copilot, and Goose are not represented as universally end-to-end tested. DeepSeek Harness remains developer-preview/opt-in. `grok` means Grok Build and `muse` means Muse Code; consumer Grok Bot and consumer Muse are unsupported.
