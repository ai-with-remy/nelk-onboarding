# Nelk Onboarding

The AI with Remy onboarding plugin for the Nelk team. It has one skill,
`/onboard`: a short interview that builds a folder called **AI Context** on your
computer. Upload that folder to your Claude and ChatGPT projects, and every
chat in them already knows who you are, how you write and how Nelk works.

## Install

**Claude app:** add the plugin marketplace `ai-with-remy/nelk-onboarding`,
install the `nelk` plugin, then type `/onboard` in a new chat.

**Claude Code** (desktop app or terminal), run these one at a time:

```text
/plugin marketplace add ai-with-remy/nelk-onboarding
/plugin install nelk@nelk-onboarding
```

Then start a new chat and type `/onboard`.

**Codex**, run these one at a time in a terminal:

```text
codex plugin marketplace add ai-with-remy/nelk-onboarding
codex plugin add nelk@nelk-onboarding
```

Then start a new Codex chat and type `$nelk:onboard`, or just say "onboard
me". You can also type `/skills` and pick `nelk:onboard`. In the Codex app you
can install it from **Settings → Plugins** instead of the terminal.

## What it builds

```text
AI Context/
├── AGENTS.md
├── about-me.md
├── nelk.md
├── audience.md
├── voice-dna.md
└── working-style.md
```

Run it again anytime to update the folder:

| | Claude | Codex |
|---|---|---|
| Run the interview | `/onboard` (full name `/nelk:onboard`) | `$nelk:onboard` or "onboard me" |

## Updating

**Claude** updates the plugin on its own. To force it:

```text
/plugin marketplace update nelk-onboarding
```

**Codex** doesn't update on its own. Ask Codex to run this, then start a new
chat:

```text
codex plugin marketplace upgrade nelk-onboarding
codex plugin add nelk@nelk-onboarding
```

## Layout

```text
nelk-onboarding/
├── .claude-plugin/marketplace.json      Claude catalogue
├── .agents/plugins/marketplace.json     Codex catalogue
└── plugins/nelk/
    ├── .claude-plugin/plugin.json
    ├── .codex-plugin/plugin.json
    ├── plugin.json
    └── skills/onboard/

scripts/smoke_codex_install.sh   clean-room Codex install test
```
