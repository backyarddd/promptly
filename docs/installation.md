# Installation, updates, and removal

Run installer commands from the cloned Promptly repository. The installer uses Python's standard library, makes no network requests or model calls, and writes only the selected Promptly files. Run `python scripts/promptly.py install --help` for options.

## Destinations

| Adapter | `--scope project --project PATH` | `--scope user` |
| --- | --- | --- |
| `codex` | `PATH/.agents/skills/promptly/` | `~/.agents/skills/promptly/` |
| `claude` | `PATH/.claude/skills/promptly/` | `~/.claude/skills/promptly/` |
| `opencode` | `PATH/.opencode/commands/promptly.md` | `$XDG_CONFIG_HOME/opencode/commands/promptly.md`, or `~/.config/opencode/commands/promptly.md` |
| `generic` | `PATH/.agents/skills/promptly/` | `~/.agents/skills/promptly/` |

The default scope is **project**, with the current directory as project root. Always specify `--project` when installing into a different repository. Installing at project scope makes the files available to commit with that project's source if desired.

`--destination` overrides destination calculation. For skills it means the exact `promptly` folder; for OpenCode it means the **commands directory**. For example, in PowerShell:

```powershell
python scripts/promptly.py install codex --destination "$env:USERPROFILE/.codex/skills/promptly"
python scripts/promptly.py install opencode --project 'C:/Projects/My Game'
```

The first example supports an existing Codex installation using its older/configured personal skills location. The installer does not infer this from `CODEX_HOME`; supply your configured path explicitly. The recommended portable Codex default follows current documentation at `~/.agents/skills`.

## Manual installation without Python

Copy the adapter's complete bundle:

- `bundles/codex/promptly/` → your Codex skills directory, retaining `agents/openai.yaml`.
- `bundles/claude/promptly/` → your Claude Code skills directory.
- `bundles/opencode/promptly.md` → your OpenCode commands directory.
- `bundles/generic/promptly/` → your other host's supported skills directory.

Each bundle contains the complete core prompt. There are no runtime references to the clone, so the installed files keep working if you move the source checkout. Select only one definition for the same host/name; overlapping personal and project skills can shadow each other or appear twice.

## Verify discovery

In Codex CLI/IDE, use `/skills` or type `$promptly`. In Claude Code, type `/promptly`. In OpenCode, use the TUI command picker or `/promptly`. Restart the host if it started before the top-level skills directory existed or does not refresh discovery.

Try preview first:

```text
/promptly --show --compact rename the Save button to Save draft; keep its behavior
```

Use `$promptly` in Codex. You should receive a short execution instruction, with no changed files or test runs. Then try a small real request in a disposable project without `--show` to verify continued execution.

## Updates and conflicts

```sh
git pull --ff-only
python scripts/promptly.py install claude --scope user --dry-run
python scripts/promptly.py install claude --scope user --force
```

Use the same adapter/scope/destination as the initial install. Reinstalling identical content does nothing. Differing existing files are refused unless `--force` is provided; forced replacement saves the previous bytes beside the original with `.promptly-backup`, adding a numeric suffix if necessary. Review conflicts before forcing an update. Backups do not have `.md` extensions and are not additional command entries.

The installer preflights file conflicts and rejects symlink/junction paths. It preserves unrelated files. An I/O failure or interrupted install is not a transaction; inspect the printed paths and rerun after resolving the error. Manual copy is appropriate when your intentional directory layout uses links.

## Removal

Remove only the Promptly skill folder you installed, or OpenCode's `promptly.md` file. Keep any personal notes/backups you want to retain. No other settings, package registrations, or background processes need removal. If a previous version was replaced, restore the relevant `.promptly-backup` file and reload the host.

## Troubleshooting

- **Codex rejects `/promptly`:** invoke the skill as `$promptly` or through the picker.
- **Command missing:** verify the destination, filename, YAML frontmatter, and host reload; inspect competing definitions and host skill permissions.
- **Only planning occurs:** check your selected agent and permission mode. Promptly keeps the host's capabilities and does not force a build agent.
- **Preview performs work:** stop the run and report a behavioral regression with the invocation, model, host version, and a redacted transcript. Preview modes are model instructions, not a permissions boundary.
- **Old behavior after changing the core:** rebuild bundles and reinstall. Installed copies intentionally do not track your checkout automatically.
