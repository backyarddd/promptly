---
name: promptly
description: Expand a rough request into a concise execution specification and carry it out, or preview the improved prompt. Use when the user invokes Promptly or asks for prompt expansion before agent work.
---

<!-- Generated from core/prompt.md; SHA256 {{CORE_SHA256}}. Edit source, then rebuild. -->

Adapter: generic Agent Skills host. Take the current user-designated request or text after the host's Promptly invocation as the rough request and leading options. Use only context the host exposes. In an agent host, continue in the same conversation. In a text-only host, return the complete rewritten prompt followed by one line stating that execution and the prompt log are unavailable (in preview mode, only the log); never imply automatic forwarding. Do not invoke Promptly recursively or create an unnecessary separate task; honor explicit user or host delegation requests.

{{CORE}}
