# AI Context file templates

Scaffolds for the `onboard` skill. Fill each one with the person's own answers.
Drop any heading with nothing real under it. Plain Markdown, no frontmatter.
Never mention the interview, the workshop or the plugin inside a file.

The finished folder:

```text
AI Context/
├── AGENTS.md
├── about-me.md
├── nelk.md
├── audience.md
├── voice-dna.md
└── working-style.md
```

---

## AGENTS.md

Written last. No preview needed. Fill in the name and role.

```markdown
# Instructions

You're working with [Name], [role] at Nelk. The files in this folder are your
briefing. Read the relevant ones before you start any task, and follow them
over your general habits.

## Read these first
- `about-me.md`: who [Name] is, their role and what they already know
- `nelk.md`: the brands and shows, how [Name]'s part of the business works,
  the team and current priorities
- `audience.md`: who watches, what lands and the language they use
- `voice-dna.md`: how [Name] writes. Use it for anything written in their name
- `working-style.md`: how they want answers, their hard rules and their tools

## How to work
- Match the voice in `voice-dna.md` for captions, titles, scripts, messages
  and anything else written as [Name].
- Follow the hard rules in `working-style.md` every time.
- Never invent numbers, names, quotes or results. Ask when something isn't
  in these files.
- Keep answers in the format [Name] asked for in `working-style.md`.
- If [Name] corrects you or tells you a new preference, suggest a one-line
  update to the right file so it sticks.
```

---

## about-me.md

```markdown
# About Me

- **Name:** [Q1]
- **Role:** [Q1]

## What I spend my time on
[Q2, in plain sentences.]

## What I'm great at
[Q3: strengths, and what the AI should never over-explain.]

## Still learning
[Q3: anything they named. Drop the heading if none.]

## Tech comfort
[Q4, plus an instruction. For example: "Beginner. Explain any technical term
the first time it comes up."]
```

---

## nelk.md

```markdown
# Nelk

## What I work on
[Q5: the brands, channels and shows they work on.]

## How it works
[Q6: who it's for and what it's trying to do, in their words.]

## The team
[Q7: who they work with and who signs off. Only names and roles they gave.]

## Current priorities
[Q8: one to three, ranked.]
```

---

## audience.md

```markdown
# Audience

## Who they are
[Q9: the typical viewer or fan, in a sentence someone could picture.]

## What lands
[Q10: content that does well.]

## What flops
[Q10: content that doesn't.]

## Their language
[Q11: words, slang, nicknames and inside jokes.]
```

---

## voice-dna.md

```markdown
# Voice DNA

## Base Writing Rules
[Paste the contents of voice-dna-base.md here, starting at "### Write Like a
Human".]

## My tone
[Q12, described in a sentence or two.]

## Words and phrases I use
[Q13]

## Words and phrases I never use
[Q13]

## Never sound like
[Q14: the archetypes they picked, each with its example line.]

## Real writing samples
[Q15: pasted exactly, labelled by type (caption, text, title, email). If none:
"Samples still to add. Paste some in anytime."]

## Patterns
[Only patterns the samples actually show: length, punctuation, emoji, sign-offs.]
```

---

## working-style.md

```markdown
# Working Style

## How I like answers
[Q16]

## Hard rules
[Q17]

## Tools I use
| Job | Tool |
|---|---|
| [e.g. Editing] | [e.g. Premiere] |
[Q18: only the real ones.]
```
