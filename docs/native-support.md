# Native support research

Checked **September 11, 2026** against official documentation. The design below is Promptly's integration decision, not a promise that every host version implements every feature identically.

| Host | Official mechanism and decision | Limitation |
| --- | --- | --- |
| Codex | `SKILL.md` with name/description; project/user discovery under `.agents/skills`. Use a native skill and optional `agents/openai.yaml`. | Explicit CLI/IDE invocation is `$promptly` or `/skills`; no custom bare slash alias is claimed. |
| Claude Code | Skills under `.claude/skills/promptly` expose `/promptly`; `$ARGUMENTS` receives the invocation text. Keep the skill in the current conversation. | No `context: fork`, forced model, or extra tool grants. Standalone installation preserves the desired command name. |
| OpenCode | Markdown under `.opencode/commands` or the user commands folder; `$ARGUMENTS` binds the request. Use `subtask: false` to retain current-session behavior. | Selected agent permissions still apply. The legacy and V2 docs differ on JSON configuration and file attachment expansion, so Promptly uses neither. |
| Generic | Standard `SKILL.md` with name/description and a self-contained body. | Discovery, command syntax, tools, and context availability are host-specific. Text-only environments can only return the expansion. |

Sources: [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills), [OpenCode commands](https://opencode.ai/docs/commands/), [OpenCode V2 commands](https://opencode.ai/v2/docs/commands), [Agent Skills specification](https://agentskills.io/specification).

OpenCode's V2 documentation retains `subtask` as a deprecated alias for `subagent`; using `subtask: false` is the compatible choice for the observed 1.x CLI and V2 documentation. The adapter omits `agent` and `model` to keep the user's current choices. It does not depend on `@file` inclusion or shell preprocessing.

For Codex, current official guidance prefers `.agents/skills`; the local desktop environment also exposes personal skills from `.codex/skills`. The installer defaults to the documented portable location and permits an exact destination for existing setups.

Observed local CLI versions were Codex **0.153.2**, OpenCode **1.18.25**, and Claude Code **2.1.261**. A version being present is not itself proof of successful native execution. See the [validation record](validation.md) for the tests actually completed.

## Why no interceptors or plugins in v1?

Each primary host can load native instructions into the current session. That already supplies the useful behavior: expand the user's intent and proceed with context intact. A plugin, shell wrapper, model proxy, or forked session would add packaging and context-transfer costs without improving the core expansion. A future distribution plugin can package these same bundles without introducing a second canonical prompt.
