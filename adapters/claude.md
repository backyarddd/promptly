---
name: promptly
description: Expand a rough request into a concise execution specification and carry it out, or preview the improved prompt. Use when the user invokes Promptly or asks for prompt expansion before agent work.
argument-hint: "[--show|--no-run] [--compact|--deep] [--research|--debug] request"
---

<!-- Generated from core/prompt.md; SHA256 {{CORE_SHA256}}. Edit source, then rebuild. -->

Adapter: Claude Code. Use the invocation arguments at the end as the rough request and leading options. If invoked through natural language with no arguments, use the current user-designated request. Keep available conversation/project context. Continue in this agent; do not fork, create a second task, or call Promptly recursively.

{{CORE}}

## Invocation arguments

$ARGUMENTS
