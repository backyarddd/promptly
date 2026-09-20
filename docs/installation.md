# Installation, updates, and removal

Run the installer from the Promptly checkout. It uses only Python's standard library, makes no network or model calls, and writes only the selected Promptly files.

```sh
python scripts/promptly.py install --help
```

## Destinations

Codex, Claude, and OpenCode install their native bundles. The `generic` preset and the additional portable Agent Skills presets install `generic/promptly/SKILL.md`; those aliases do not generate duplicate prompt bodies.

| Harness | Project scope | User scope |
| --- | --- | --- |
| `codex` | `PATH/.agents/skills/promptly/` | `~/.agents/skills/promptly/` |
| `claude` | `PATH/.claude/skills/promptly/` | `~/.claude/skills/promptly/` |
| `opencode` | `PATH/.opencode/commands/promptly.md` | `$XDG_CONFIG_HOME/opencode/commands/promptly.md`, or `~/.config/opencode/commands/promptly.md` |
| `generic` | `PATH/.agents/skills/promptly/` | `~/.agents/skills/promptly/` |
| `pi` | `PATH/.pi/skills/promptly/` | `~/.pi/agent/skills/promptly/` |
| `cursor` | `PATH/.cursor/skills/promptly/` | `~/.cursor/skills/promptly/` |
| `deepseek-harness` | `PATH/.dsh/skills/promptly/` | `~/.dsh/skills/promptly/` |
| `grok` (Grok Build) | `PATH/.grok/skills/promptly/` | `~/.grok/skills/promptly/` |
| `muse` (Muse Code) | `PATH/.agents/skills/promptly/` | `$XDG_CONFIG_HOME/muse/skills/promptly/`, or `~/.config/muse/skills/promptly/` |
| `gemini` | `PATH/.gemini/skills/promptly/` | `~/.gemini/skills/promptly/` |
| `copilot` | `PATH/.github/skills/promptly/` | `~/.copilot/skills/promptly/` |
| `goose` | `PATH/.agents/skills/promptly/` | `~/.agents/skills/promptly/` |

The DeepSeek Harness preset uses the documented `.dsh` locations. It is developer-preview/opt-in; enable the harness's skill-composition packages as required. The installer does not interpret `DSH_HOME`, so use `--destination` when that variable points to a non-default root.

The `grok` preset targets Grok Build's local skills support. It does not claim support for consumer Grok Bot. The `muse` preset targets Muse Code's Agent Skills directories. It does not claim support for the consumer Muse application.

The default scope is project and the default project is the current directory. Specify `--project` for another repository. `--destination` means the exact skill folder, except for OpenCode where it means the commands directory.

Examples:

```sh
python scripts/promptly.py install pi --scope project --project /path/to/project
python scripts/promptly.py install muse --scope user
python scripts/promptly.py install opencode --scope user
python scripts/promptly.py install cursor --destination /path/to/project/.cursor/skills/promptly
```

Use one definition for a given host/name. Overlapping project and user skills may shadow each other or appear twice. Reload the host if it does not refresh discovery.

## Manual installation

Copy the complete bundle when Python is unavailable:

- `bundles/codex/promptly/` to the Codex skill directory, retaining `agents/openai.yaml`.
- `bundles/claude/promptly/` to the Claude Code skill directory.
- `bundles/opencode/promptly.md` to the OpenCode commands directory.
- `bundles/generic/promptly/` to any portable Agent Skills directory listed above.

## Updates and conflicts

```sh
git pull --ff-only
python scripts/promptly.py install pi --scope user --dry-run
python scripts/promptly.py install pi --scope user --force
```

Identical content is skipped. Differing files are refused unless `--force` is used; forced replacement saves the previous bytes beside the file as `.promptly-backup` (with a numeric suffix if needed). The installer preflights all files and rejects symlink/junction paths before writing. It preserves unrelated files. An interrupted install is not transactional; inspect the printed paths and rerun after resolving the error.

## Removal

Remove only the Promptly folder installed for the selected host, or OpenCode's `promptly.md`. Keep any backups or notes you want. No host configuration or background process needs removal.
