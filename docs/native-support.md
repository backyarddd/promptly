# Native support

The presets below target documented local Agent Skills locations checked on September 19, 2026. “Portable” means Promptly installs the generic `SKILL.md`; discovery, invocation syntax, context, and permissions remain controlled by each host.

| Host/preset | Integration | Project location | User location | Status and limits |
| --- | --- | --- | --- | --- |
| Codex | Native skill plus optional `agents/openai.yaml` | `.agents/skills` | `.agents/skills` | `$promptly` or the skill picker; no fabricated slash alias |
| Claude Code | Native skill command with `$ARGUMENTS` | `.claude/skills` | `.claude/skills` | `/promptly`; current session and host permissions are retained |
| OpenCode | Markdown custom command with `$ARGUMENTS` | `.opencode/commands` | XDG config `opencode/commands` | `/promptly`; selected agent/model and permissions are retained |
| Pi | Portable Agent Skill | `.pi/skills` | `.pi/agent/skills` | Host-specific discovery and invocation |
| Cursor | Portable Agent Skill | `.cursor/skills` | `.cursor/skills` | Host-specific discovery and invocation |
| DeepSeek Harness (`dsh`) | Portable Agent Skill | `.dsh/skills` | `.dsh/skills` | Developer-preview/opt-in; enable skill-composition packages; installer does not interpret `DSH_HOME` |
| Grok Build | Portable Agent Skill | `.grok/skills` | `.grok/skills` | Supported local harness; this is not consumer Grok Bot |
| Muse Code | Portable Agent Skill | `.agents/skills` | XDG config `muse/skills` | Supported coding harness; this is not consumer Muse |
| Gemini CLI | Portable Agent Skill | `.gemini/skills` | `.gemini/skills` | Host-specific discovery and invocation |
| GitHub Copilot | Portable Agent Skill | `.github/skills` | `.copilot/skills` | Host-specific discovery and invocation |
| Goose | Portable Agent Skill | `.agents/skills` | `.agents/skills` | Host-specific discovery and invocation |

The installer uses exact mappings above. `muse --scope user` resolves `XDG_CONFIG_HOME/muse/skills/promptly`, falling back to `~/.config/muse/skills/promptly`; `deepseek-harness` uses `.dsh` directly. Use `--destination` for an organization-specific root or environment convention.

Grok Build and Muse Code are the documented local coding harnesses covered here. Promptly does not claim support for consumer Grok Bot or consumer Muse because they do not expose the same local `SKILL.md` installation contract.

## Sources and validation boundary

The native Codex, Claude Code, and OpenCode bindings follow their official skill/command documentation: [OpenAI Build Skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills), and [OpenCode commands](https://opencode.ai/docs/commands/). The portable format follows the [Agent Skills specification](https://agentskills.io/specification). The additional presets are packaging support for their documented local skill directories; Promptly does not claim that every host version has been end-to-end smoke-tested.

For a new host, first try the generic bundle. Add a native adapter only when the host documents a distinct input or metadata contract. Record observed discovery and execution separately from deterministic installer checks.
