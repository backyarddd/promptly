# Promptly

**Turn rough ideas into execution-ready instructions for AI agents.**

```text
/promptly make me a roblox inventory system where players can equip weapons and save them
```

Promptly sharpens that request using the context already in your conversation, adds relevant requirements and failure cases, and lets the agent carry out the improved task. It preserves your technology, scope, and product decisions.

**More useful context, not simply more context.** A button-label edit stays small. A multiplayer trading system gets the consistency and failure-handling detail it needs.

## How it works

```text
Your rough request + available context
                  ↓
     Preserve intent and constraints
                  ↓
  Add useful requirements and discovery
                  ↓
     Concise execution specification
                  ↓
   Same agent inspects → implements → validates
```

This is a model-executed skill, not a separate model service. The host agent expands the task and continues in the same conversation. There is no API key, background server, subprocess redispatch, or manual copy/paste step in the native workflow. Preview modes return the improved prompt instead.

## Supported hosts

| Host | Native integration | Invocation |
| --- | --- | --- |
| OpenAI Codex | Agent skill | `$promptly request`, or select Promptly in the skill picker |
| Claude Code | Agent skill exposed as a command | `/promptly request` |
| OpenCode | Markdown custom command | `/promptly request` |
| Other Agent Skills hosts | Generic `SKILL.md` | Host-specific; select Promptly or ask it to use the skill |

Codex does **not** receive a fabricated `/promptly` alias. Its documented explicit invocation is `$promptly` or `/skills` in CLI/IDE surfaces. Check the [native support notes](docs/native-support.md) for official sources, version observations, and limitations.

## Installation

Clone this repository. Python 3.10+ is needed only for the installer/build tools; the installed skill itself requires no Python runtime.

```sh
git clone https://github.com/backyarddd/promptly.git
cd promptly
```

The following commands work in PowerShell, Bash, and similar shells when `python` is available. On systems where Python 3 is named `python3`, use that command instead.

### Codex

```sh
python scripts/promptly.py install codex --scope user
```

This installs to `~/.agents/skills/promptly`. Invoke:

```text
$promptly build a quest system
$promptly --show add trading
```

For an existing setup that keeps personal skills under `CODEX_HOME/skills`, use the exact destination option described in the [installation guide](docs/installation.md). Choose one location to avoid duplicate skill entries.

### Claude Code

```sh
python scripts/promptly.py install claude --scope user
```

This installs to `~/.claude/skills/promptly`. Invoke:

```text
/promptly build a quest system
```

### OpenCode

```sh
python scripts/promptly.py install opencode --scope user
```

This installs `promptly.md` to `~/.config/opencode/commands`, respecting `XDG_CONFIG_HOME` when set. Invoke `/promptly` in the TUI with an agent that can perform your task; selecting a read-only planning agent keeps that agent's restrictions.

### Project or generic installation

```sh
python scripts/promptly.py install codex --scope project --project /path/to/your/project
python scripts/promptly.py install claude --scope project --project /path/to/your/project
python scripts/promptly.py install opencode --scope project --project /path/to/your/project
python scripts/promptly.py install generic --scope project --project /path/to/your/project
```

Use the appropriate command for your host. Codex and generic use the same project destination; do not install both there. Quote paths containing spaces. Reload or restart the host if the command/skill does not appear. No host configuration files are modified.

You can also copy the ready-to-use files from [bundles/](bundles/) manually. See [installation, updates, and removal](docs/installation.md).

## Usage and modes

| Option | Behavior |
| --- | --- |
| None | Expand internally, then execute the requested task in the current conversation |
| `--show` | Show the enhanced instruction only |
| `--no-run` | Same as `--show` |
| `--compact` | Minimal useful expansion |
| `--deep` | More detail for complex requirements without enlarging scope |
| `--research` | Favor research and decision methodology |
| `--debug` | Favor evidence-led diagnosis |
| `--` | Stop parsing Promptly options; subsequent text is the request |

Options go before the request. Detail flags conflict with each other, as do task-kind flags; conflicts and unknown leading flags produce a usage correction without execution. Quoted text and flags inside a request remain task content. Flags are interpreted by the host model, not a shell parser. They apply to the current invocation only.

```text
/promptly --show --deep design ranked 2v2 matchmaking using our existing backend
/promptly --compact make the loading animation faster
/promptly --debug my inventory sometimes dupes items fix it
/promptly --research compare postgres and mongodb for this project
/promptly --show -- add a --debug flag to our CLI
```

Execution means carrying out the requested deliverable: an analysis request produces analysis; a design-document request produces a document. It does not automatically authorize code changes, deployment, spending, or contacting others. Preview is an instruction-level restriction, not a sandbox; normal host permissions still apply.

## Before → after

Input:

```text
/promptly --compact make the loading animation faster; keep Vue and the current artwork
```

Illustrative enhanced instruction:

> Locate the existing Vue loading animation and inspect its timing. Shorten the animation while preserving the current artwork, behavior, and reduced-motion handling if present. Keep the change local to the timing controls. Verify the result visually and run relevant existing checks.

Input, with Roblox/Knit/ProfileStore/Fusion already established:

```text
/promptly add trading
```

Illustrative excerpt:

> Inspect and reuse the existing inventory, persistence, networking, and UI conventions. Build a player-to-player offer and confirmation flow with server-side ownership checks. Offer edits reset confirmation. Prevent duplicate settlement and handle cancellation or disconnect safely. Inspect storage guarantees before choosing a recoverable settlement strategy.

Promptly does not invent filenames, a paid economy, fixed inventory limits, or a new aesthetic. It distinguishes supplied facts from things the agent still needs to inspect. See [more examples](docs/examples.md).

## Development and validation

```sh
python scripts/promptly.py build
python scripts/promptly.py build --check
python -m unittest discover -s tests -v
```

Edit [core/prompt.md](core/prompt.md) for expansion behavior. Adapters only bind native input and metadata; bundles are generated copies, not separate prompts to maintain. See [architecture](docs/architecture.md) and [contributing](CONTRIBUTING.md).

There are [24 behavioral fixtures](evals/cases.json) and a [semantic evaluation rubric](evals/README.md). Unit tests verify packaging and installation, **not** model judgment. The [validation record](docs/validation.md) separates automated checks, observed behavioral output, and native-host coverage.

## Limits

- Prompt quality depends on the host model and the context it actually sees.
- The same-agent approach is native instruction composition, not interception of every user message or an independently auditable second model call.
- Expansion adds a fixed instruction cost. Smaller prompts and better outcomes are goals, not measured token-saving guarantees.
- A text-only host can return an improved prompt but cannot execute it. Generic command discovery and context access remain host-specific.

MIT licensed. See [LICENSE](LICENSE).
