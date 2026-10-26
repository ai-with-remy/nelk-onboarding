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

**Codex:**

```text
codex plugin marketplace add ai-with-remy/nelk-onboarding
```

Then open `/plugins`, install `nelk`, and start a new session.

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

Run `/onboard` again anytime to update the folder. In Claude Code the full
name is `/nelk:onboard`; in Codex it is `$nelk:onboard`.

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
