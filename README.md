# Promptly

Turn a rough request into a concise, execution-ready prompt for an AI agent. Promptly preserves intent, constraints, scope, and exclusions, adds only useful requirements, shows the complete rewrite, and then lets the same agent carry it out.

## How it works

```text
rough request + available context
              ↓
      concise rewritten prompt
              ↓
  print "Promptly prompt:" + full prompt
              ↓
      same agent executes it
```

This is a model-executed skill, not a separate model service. It makes no API calls, starts no background process, and does not create a second conversation. A text-only host can return the prompt but cannot execute it.

By default, the response first prints the full rewritten prompt under `Promptly prompt:` and then continues with the requested work. `--show` and `--no-run` print only that prompt and stop. These are host instructions, not a permission boundary; normal host permissions still apply.

## Supported hosts

| Host | Bundle | Invocation or discovery |
| --- | --- | --- |
| OpenAI Codex | Native Agent Skill | `$promptly request` or the skill picker |
| Claude Code | Native skill/command | `/promptly request` |
| OpenCode | Markdown custom command | `/promptly request` |
| Pi, Cursor, DeepSeek Harness, Grok Build, Muse Code, Gemini CLI, GitHub Copilot, Goose | Portable Agent Skill | Host-specific skill discovery |

Promptly supports documented local Agent Skills locations. `grok` means Grok Build, not consumer Grok Bot. `muse` means Muse Code, not the consumer Muse application. DeepSeek Harness support is developer-preview/opt-in and may require its skill-composition packages. See [native support notes](docs/native-support.md).

## Installation

Python 3.10+ is needed only for packaging and installation. The installed skill has no runtime dependency.

```sh
git clone https://github.com/backyarddd/promptly.git
cd promptly
```

Install a user skill:

```sh
python scripts/promptly.py install codex --scope user
python scripts/promptly.py install pi --scope user
python scripts/promptly.py install cursor --scope user
python scripts/promptly.py install deepseek-harness --scope user
python scripts/promptly.py install grok --scope user
python scripts/promptly.py install muse --scope user
python scripts/promptly.py install gemini --scope user
python scripts/promptly.py install copilot --scope user
python scripts/promptly.py install goose --scope user
```

Install into a project with `--scope project --project PATH`. The exact project and user destinations are listed in the [installation guide](docs/installation.md). `--destination` overrides the calculated location. The installer performs no network or model calls, preflights conflicts, preserves backups with `--force`, and supports `--dry-run`.

Codex, Claude, and OpenCode keep their native adapters. The other hosts use the same generated `generic/promptly/SKILL.md`; aliases do not create duplicate prompt sources. Reload the host if a newly installed skill is not discovered.

## Modes

| Option | Behavior |
| --- | --- |
| None | Print the complete rewritten prompt, then execute it in this conversation |
| `--show` / `--no-run` | Print only the complete rewritten prompt |
| `--compact` | Keep only the minimum useful detail |
| `--deep` | Include more dependencies and failure handling |
| `--research` | Favor comparison, sourcing, and decision criteria |
| `--debug` | Favor reproduction, evidence, and diagnosis |
| `--` | End option parsing; following text is literal request content |

Options must lead the request. Conflicting detail/task hints or unknown leading options produce a usage correction without execution. Flags inside quoted text, logs, or code remain request content.

```text
/promptly --show --deep design a migration plan for the current service
/promptly --compact rename the Save button while preserving its behavior
/promptly --debug investigate intermittent request failures
/promptly --research compare two storage options for this project
```

## Development

```sh
python scripts/promptly.py build
python scripts/promptly.py build --check
python -m unittest discover -s tests -v
```

Edit [core/prompt.md](core/prompt.md) for expansion behavior. Adapters only bind host input; bundles are generated copies. Packaging tests cover deterministic build and installation behavior. Prompt behavior fixtures in [evals/](evals/) are optional/manual and are not a required gate for every prompt edit. See [architecture](docs/architecture.md), [installation](docs/installation.md), and [validation](docs/validation.md).

## Limits

- Prompt quality depends on the host model and the context it exposes.
- Native Agent Skills discovery, command syntax, and execution permissions remain host-specific.
- Expansion adds a fixed instruction cost; smaller prompts and better outcomes are goals, not measured guarantees.

MIT licensed. See [LICENSE](LICENSE).
