# Build OS Root-v3 File Templates

These are the only files `/ai-os:build-os` creates for student knowledge. Replace
every bracketed placeholder with interview facts. Preview files containing the
student's words before writing. Built files never mention the course, setup
session, or plugin. There is no root `CLAUDE.md` template: root `AGENTS.md` is
the one instructions file that both Claude Code and Codex read.

## Root `AGENTS.md` — canonical cross-harness master

Write to `<OS_ROOT>/AGENTS.md`.

```markdown
# [Name]'s AI Operating System

This is the canonical instruction file for this workspace. All paths are
relative to the AI OS root.

The `context/` folder describes me and my business. `MEMORY.md` holds approved
lessons learned over time. Claude Code and Codex both read this file directly.

## Who I am

- **Name:** [A1]
- **Role and business:** [A2]
- **What I do most days:** [A3]
- **Expertise:** [A4]
- **Technical comfort:** [A5]

## My tools

[D6 as short `job → tool` bullets.]

## How to work with me

[D1 output preferences and global D2 rules as short bullets. Scope-specific
preferences belong in the relevant context file.]

## Context source map

- Before a task about me, my background, or my expertise, read `context/about-me.md` in full.
- Before a task about the business, strategy, priorities, or team, read `context/business.md` in full.
- Before a task about offers, pricing, or packaging, read `context/offers.md` in full.
- Before a task about customers, positioning, pains, objections, or research, read `context/ideal-customer-profile.md` in full.
- Before deciding how to communicate, collaborate, plan, or format an output, read `context/working-style.md` in full.
- Before writing in my voice, read `context/voice-dna.md` in full.

## Core operating principles

- Check the relevant context before acting. Search the workspace before asking me to repeat something already recorded.
- State assumptions and uncertainty plainly. Show materially different interpretations before choosing.
- Plan non-trivial work before acting. If reality changes, stop and re-plan.
- Preserve unrelated work. Never make destructive changes without explicit approval.
- Verify results before saying something is complete.
- Prefer the clean permanent solution without over-engineering simple tasks.

## Execution standards

### Delegate execution

Keep the main agent focused on communicating with me, making decisions,
orchestrating work, and integrating the final result.

When subagents are available, delegate substantial execution such as:

- Research across multiple sources.
- Reading or searching broadly across the workspace.
- Implementation that can be completed independently.
- Independent testing or verification.

Run independent tasks in parallel when useful. Give each subagent a clear
scope, the context it needs, and a specific expected output. Continue with the
same subagent for related follow-up work when the harness supports it.

Do not delegate trivial one-step actions, decisions that require my judgement,
or external and irreversible actions requiring my approval.

The main agent remains responsible for reviewing delegated work, resolving
conflicts, and delivering a coherent final result.

### Finish and verify

Complete all safe work inside the agreed scope. Do not leave avoidable loose
ends or offer a temporary workaround when the permanent fix is reasonably
within scope.

Search before building. Test before shipping. Never claim completion without
evidence such as inspected output, passing tests, checked logs, or another
direct demonstration that the result works.

### Workspace hygiene

- Plan changes to a file before editing it and apply them as one coherent edit
  whenever practical.
- Keep the OS root clean. Put every project inside an appropriate folder rather
  than creating loose files at the top level.
- Keep reusable skills in `.agents/skills/`. The `.claude/skills` compatibility
  path points to the same Skills collection and must not contain separate
  copies.

## Learning and memory

Read `MEMORY.md` in full at the start of every task.

When I correct you or give you a new instruction, do not automatically save it
to memory. Store it in the narrowest place where it should control future work:

- A rule for one workflow → the relevant `SKILL.md`.
- A fact about me, my business, offers, customers, brand, voice, or working
  style → the relevant `context/` file.
- Information for one project, client, or deliverable → that project or client
  folder.
- A general preference or operating rule spanning different tasks, projects,
  and skills → `MEMORY.md`.
- A rule governing the entire AI OS → `AGENTS.md`, only when I explicitly ask
  to change the system.
- A temporary request, draft decision, or one-off detail → nowhere permanent.

Never duplicate an instruction across files.

### Memory save gate

Save to `MEMORY.md` only when every condition is true:

1. I stated or confirmed it directly; it is not an inference.
2. It will materially affect future work and is likely to remain true.
3. It applies across multiple tasks, projects, or skills.
4. It is a general operating preference with no more specific home.
5. It is not already recorded and contains no secret or sensitive information.
6. It can be written as one short, actionable line that I approve before saving.

### Processing corrections

1. Determine the correction's future scope and read the relevant existing file.
2. If the rule is already recorded, correct the work without saving a duplicate.
   An execution mistake is not a new memory.
3. If it is new and enduring, propose the destination, exact wording, and why
   it belongs there.
4. Wait for approval, update only that destination, then read it back and
   confirm the change.

Put approved memories under `## Approved memory` in `MEMORY.md`. Update an
existing entry instead of adding a near-duplicate. Without approval, do not
change a persistent instruction file.
```

## Root `MEMORY.md`

Write to `<OS_ROOT>/MEMORY.md`.

```markdown
# Memory

This file holds only enduring knowledge that will change a future chat.

## Save gate

Add nothing unless it is not task-specific, is not already in `AGENTS.md` or
this file, and the owner explicitly approved the exact one-line entry first.
Never save wording nits, draft-only taste, rejected outputs, one-off task
details, or debugging history.

Keep entries short. Consolidate or update an existing entry before appending a
near-duplicate.

## Approved memory

_(None yet.)_
```

## Core six context files

Write these six files into `<OS_ROOT>/context/`. Use the interview facts already
captured; leave a short honest “still to fill in” note where depth belongs in
the context session.

### `about-me.md`

```markdown
# About Me

## Identity
- **Name:** [A1]
- **Role:** [A1]
- **Business:** [A2]

## What I do
[A3]

## Expertise
[A4]

## Technical comfort
[A5]
```

### `business.md`

```markdown
# The Business

## What it is
[A2]

## How it works
[B1]

## Offers summary
[B2 light sketch]

## Customers
[B3 light sketch]

## Team
[B4]

## Priorities
[B5, ranked]
```

### `offers.md`

```markdown
# Offers and Pricing

_(A light starting sketch. Deepen this before treating it as the complete
commercial record.)_

[B2: offer, rough price, captured currency]
```

### `ideal-customer-profile.md`

```markdown
# Ideal Customer Profile

_(A light starting sketch. Pains, exact language, objections, and buying
triggers are still to fill in.)_

[B3 customer sketch]
```

### `working-style.md`

```markdown
# Working Style

## Output preferences
[D1]

## Hard rules
[D2]

## Daily rhythm
[D3]

## Weekly rhythm
[D4]

## Timezone
[D5]

## Tools
[D6 as `job → tool` bullets]
```

### `voice-dna.md`

```markdown
# Voice DNA

_(The personal voice layer is built from real writing samples. For now, use the
base human-writing rules below.)_

## Base Writing Rules

[Embed `<PLUGIN_ROOT>/shared/voice-dna-base.md` verbatim.]

## My Voice

[Any volunteered voice note, otherwise: `_(Add real writing samples here.)_`]
```

For an employee, keep the same filenames but frame `business.md` as work
context, `offers.md` as responsibilities/deliverables, and
`ideal-customer-profile.md` as internal stakeholders.
