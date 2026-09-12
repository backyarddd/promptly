# Contributing

Change the canonical prompt in `core/prompt.md`, keeping scope and token efficiency central. Use adapters only for native discovery, input binding, context, and delivery. Do not edit generated bundles independently.

For a behavior change:

1. Add or update a realistic scenario in `evals/cases.json`, describing acceptable behavior and scope mistakes without requiring exact wording.
2. Modify the smallest relevant portion of the core.
3. Rebuild with `python scripts/promptly.py build`.
4. Run `python -m unittest discover -s tests -v` and `python scripts/promptly.py build --check`.
5. Forward-test affected cases with a model that did not see expected answers; report the host/model and observed output.
6. Update documentation when behavior, installation, or native support changes.

Keep runtime bundles self-contained. Adding a dependency, provider API, hook, or extra LLM call needs a demonstrated benefit over native same-conversation execution. Avoid tests that only enforce preferred wording or mirror a paragraph of the prompt.

Issues and pull requests should include a redacted reproduction, expected outcome, actual behavior, host/version/model, and relevant mode flags. Never include credentials, private project contents, or unredacted conversation logs.
