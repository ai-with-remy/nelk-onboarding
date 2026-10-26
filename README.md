# Nelk Onboarding

The AI with Remy onboarding plugin for the Nelk team. It builds your AI OS,
deepens its context with Nelk's brands, voice and audience, and connects the
tools you use.

## Install

**Claude Code** (desktop app or terminal), run these one at a time:

```text
/plugin marketplace add ai-with-remy/nelk-onboarding
/plugin install ai-os@nelk-onboarding
```

**Codex:**

```text
codex plugin marketplace add ai-with-remy/nelk-onboarding
```

Then open `/plugins` (or **Settings → Plugins**), install `ai-os`, and start a
new session.

## What's included

The `ai-os` plugin has three skills. In Claude Code you run them as
`/ai-os:<skill>`, and in Codex as `$ai-os:<skill>`.

| Skill | What it does |
|---|---|
| `/ai-os:build-os` | A short interview that builds your OS folder: `AGENTS.md`, `MEMORY.md`, your context files and a home for skills |
| `/ai-os:build-context` | Deepens your context files with your brands, voice, audience and offers |
| `/ai-os:connect` | Connects your apps, starting with Composio |

Codex equivalents: `$ai-os:build-os`, `$ai-os:build-context`, `$ai-os:connect`.

## Layout

```text
nelk-onboarding/
├── .claude-plugin/marketplace.json      Claude Code catalogue
├── .agents/plugins/marketplace.json     Codex catalogue
└── plugins/ai-os/
    ├── .claude-plugin/plugin.json
    ├── .codex-plugin/plugin.json
    ├── shared/
    └── skills/
```
