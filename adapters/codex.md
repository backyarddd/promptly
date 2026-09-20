---
name: promptly
description: Expand a rough request into a concise execution specification and carry it out, or preview the improved prompt. Use when the user invokes Promptly or asks for prompt expansion before agent work.
---

<!-- Generated from core/prompt.md; SHA256 {{CORE_SHA256}}. Edit source, then rebuild. -->

Adapter: Codex. Take the rough request and leading options following the user's explicit Promptly skill invocation (normally `$promptly`), or the request they designated for expansion. Keep available conversation/project context and continue in this agent. Do not invoke Promptly recursively or create an unnecessary separate task; honor explicit user or host delegation requests.

{{CORE}}
