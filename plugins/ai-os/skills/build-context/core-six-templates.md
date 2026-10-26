# Core-Six File Templates + Per-Department Brain

*(The tools legend is no longer its own file — it lives as the `## Tools` section at the bottom of `working-style.md`, §4 below. "How I work" and "what I work with" are one file.)*

Internal guidance for the `build-context` skill. Resolve `PLUGIN_ROOT` and `HOST_RUNTIME` from `<PLUGIN_ROOT>/shared/runtime.md` before using it. These are scaffolds for the active AI host, not a form the student fills in. Every generated file is bespoke: keep only headings that fit the real business and fill them with the student's words and examples.

Rules that apply to every file below:

- **Pre-fill FIRST, then deepen — never re-ask.** By the time `/ai-os:build-context` runs, `/ai-os:build-os` has already captured the surface answers into the progress file and written skeleton files. For every file, LOAD what's already known, SHOW it back to the student ("here's what I've already got"), and interview ONLY the gaps. The opening move for any gap is *"When we built your OS, you told me [X]. Let's go deeper,"* never a cold ask. If a skeleton file already exists, **edit/extend it — carry its facts forward, don't regenerate from scratch.** Each template below has an **`Already on file`** line telling you what `build-os` captured.
- **Preview before writing.** Never write a file without showing it first (with a plain-English "here's what you're looking at" beat) and getting a yes (interaction-contract rule 4).
- **Plain Markdown.** Headings, short bullets, the occasional table. No frontmatter on context files (they're read as knowledge, not run as skills).
- **Write in the student's voice where it's their words** (voice samples, phrases they use), in plain neutral prose where it's facts about them.
- **Built files never reference the setup.** Nothing written to the student's disk may mention sessions ("Tools module will…" must never appear in a generated file), the course, this plugin, or the setup process — every generated file must read as a standalone document that still makes sense a year from now, in any AI app. Skill narration can say those things out loud; files never carry them.

---

## 1. `business.md` — the anchor doc

The single most important file. Everything else hangs off it. Built FIRST because the later files reference it.

**Already on file (SHOW, don't re-ask):** A2 one-liner, B1 model, B3 customer sketch, B4 team, B5 priority — all captured by `/ai-os:build-os` and mostly in the skeleton. This file is largely a *confirm-and-top-up*: read the skeleton back, then just deepen stage + market and fold in any drag-in docs.

```markdown
# Business

## What it is
[One clear paragraph: what the business does, in plain language. Start from the A2 one-liner already on file, expand to 3–4 sentences.]

## The model — how money flows
[From B1 (already on file). Who pays, for what, and how (retainer / one-off / subscription / per-job / package / salary). Be concrete: "Clients pay a monthly retainer of roughly $X to run their content" beats "we do content".]

## Stage
[Where the business is right now: just starting / finding product-market fit / growing / established / scaling. One or two lines. GAP to deepen — usually not in the skeleton. If unknown, ask.]

## The market
[Who the business serves at a high level and roughly how big / competitive the space is. The deep ICP lives in ideal-customer-profile.md — keep this to the 30,000-foot view.]

## Team
[From B4 (already on file). Solo, or who does what. Only include if there's a team.]

## Current #1 priority
[From B5 (already on file). A durable, quarter-plus goal — not a this-week to-do.]
```

---

## 2. `about-me.md` — the person

**Already on file (SHOW, don't re-ask):** A1 name/role, A3 daily focus, A4 expertise *headline*, A5 tech comfort — all in the skeleton. The one real DEEPEN here is the **A4 depth pass**: onboard only got a one-line expertise headline, so build on it (sub-specialisms, what NOT to explain, authority vs still-learning). Add story/background only if volunteered.

```markdown
# About Me

## Identity
- **Name:** [A1 — already on file]
- **Role:** [A1 — already on file]
- **Business:** [A2 one-liner — already on file]

## Background / story
[Short — how they got here, what they did before. Only what they volunteer. This helps the AI understand where they're coming from. Skip if they don't offer it.]

## What I'm great at (expertise)
[From A4. Onboard has the one-line headline — build on it here: the sub-areas they're strongest in, the things the AI should NOT over-explain because they know them cold, and (flip side) where they're still learning. This nuance is what stops the OS over-explaining.]

## What I spend my time on
[From A3 (already on file) — the daily focus, translated into natural language.]

## Tech comfort
[From A5 (already on file). State it plainly AND translate it into an instruction, e.g. "Total beginner — explain every technical term the first time it appears, never assume prior knowledge."]
```

---

## 3. `voice-dna.md` — how they write

The richest file, and the one file with **nothing pre-filled from `build-os`**. Structure it with the proven base rules embedded verbatim from `<PLUGIN_ROOT>/shared/voice-dna-base.md`, then the student's personal layers and real writing samples.

**Already on file:** nothing (`build-os` skipped voice by design). Build from V1–V4 + pasted samples. This is where the module spends its real time.

```markdown
# Voice DNA

## Base Writing Rules
[EMBED the full contents of shared/voice-dna-base.md here, verbatim, starting at its "### Write Like a Human" section. These are the anti-AI-slop foundation rules — banned words, banned rhetorical constructions, "would a real person write it this way?". They apply to ALL output regardless of personal style. The student's personal layers below sit ON TOP of these.]

## My tone
[From V1. Where they sit on the formal ↔ casual spectrum, described richly (not one word). Quote the pasted samples that place them there.]

## Voice character
[From V3. The one or two characteristics that fit (direct and confident / warm and friendly / technical and precise / casual and conversational / inspiring). Expand each into what it sounds like in practice.]

## Words and phrases I use
[From V2 part 1. Specific: greetings, sign-offs, pet phrases, sentence-length habits.]

## Words and phrases I never use
[From V2 part 2. Specific words and patterns to avoid — layered on top of the base banned list, not replacing it.]

## Anti-voice — what I must NEVER sound like
[From V4. Which of the six cringe archetypes make them wince, plus any they added. Keep the archetype examples so the AI knows exactly what to avoid:]
- **Corporate drone** — "Per our previous correspondence, I wanted to circle back regarding the deliverables timeline..."
- **Fake enthusiastic** — "I'm SO excited to share this AMAZING opportunity!!!"
- **Generic AI** — "In today's rapidly evolving digital landscape, it's important to leverage cutting-edge solutions..."
- **Overly academic** — "One might argue that the intersection of digital transformation and..."
- **Salesy pusher** — "Don't miss out! Limited time offer! Act now before it's too late!"
- **Passive and vague** — "It might be worth considering potentially looking into whether there could be..."
[Mark which ones they flagged as their personal anti-voice.]

## Real writing samples
These are actual examples of how I write. Use them as the reference for tone, rhythm, and pacing.

### [Email / message / post — label each sample by type]
[Paste the real samples the student dropped in, verbatim. The more the better. This is the single best signal for matching their voice — a real sample beats any description.]

## Writing patterns
[Observed from the samples: greeting style, sign-off style, sentence length, punctuation habits, emoji usage, paragraph style. Only claim a pattern the samples actually show.]
```

**Note:** if the student has no samples to paste yet, build the file from V1–V4 alone and add a line: "Samples still to add — paste writing samples here anytime and ask me to update your voice file." Never fabricate samples. (Narration can mention that connected email makes this easier later; the file itself stays timeless.)

---

## 4. `working-style.md` — how to work with them (including the tools legend)

**Already on file (SHOW, don't re-ask):** D1 output format, D2 hard rules, D3 daily rhythm, D4 weekly rhythm, D5 timezone, and the light D6 `tools` legend — all in the skeleton. DEEPEN here: any thin spots, plus the tools legend gets its own deepen pass (caveats + where-things-live) in the `## Tools` section — see Phase 2.5 of the skill.

Note on D2: global rules belong here and in resolved `MASTER_PATH`. In root-v3/root-v2,
scope-specific rules live in the relevant context file. Cohort-v1 may retain
approved folder guidance.

**One file, not two.** How they like to work and what they work with belong together — so the tools legend is the last section of THIS file, not a separate `tools.md`. The Tools module (`/ai-os:connect`) upgrades that same `## Tools` section into the live connected-tools record; it never creates a second file.

```markdown
# Working Style

## How I like output
[From D1 + follow-up (already on file). Concise bullets / detailed narrative / structured / depends — plus any specific formatting rules ("bottom line first", "never a wall of text", "table when comparing").]

## Hard rules
[From D2 — global rules only. These also go into resolved `MASTER_PATH`; when
`ROOT_SIGNPOST` resolves to a file (not root-v3), verify it still points to it.]

## Daily rhythm
[From D3 (already on file). Evergreen repeating tasks, not this week's to-dos. The Autopilot module may schedule these through the active host's supported scheduling surface.]

## Weekly rhythm
[From D4 (already on file). Same — durable weekly patterns, not one-offs.]

## Timezone
[From D5 (already on file). The IANA zone or city. Load-bearing for scheduling in the Autopilot module. If they travel, note that it varies and record the current one.]

## Tools
A map of what I use and what I use it for. This is a legend, not a connection — it records what I actually use each tool for, and it's the map to work from whenever tools get wired up. The Tools module (`/ai-os:connect`) upgrades this same section into the live "what's connected" record.

The slim job → tool version is mirrored in resolved `MASTER_PATH` under “My
stack”; the full legend and caveats live here.

### Job → tool
[The clean legend, one row per job. Deepened from the D6 inventory; fill obvious gaps by proposing likely tools from their business type.]
| Job | Tool |
|---|---|
| Newsletter / publishing | [e.g. Beehiiv] |
| Marketing email / broadcasts | [e.g. Resend] |
| Projects + content planning | [e.g. Notion] |
| Email | [e.g. Gmail] |
| Calendar | [e.g. Google Calendar] |
| Scheduling (others book time) | [e.g. Cal.com] |
| Payments / invoicing | [e.g. Stripe] |
| Storage / files | [e.g. Google Drive] |
| Design | [e.g. Canva] |
| Meeting notes | [e.g. Granola] |
| Chat / team comms | [e.g. Slack] |
[Only include the rows that are real for them. Drop the rest.]

### Caveats — what to trust, what not to
[Per-tool trust notes — the gold this section adds. E.g. "CRM data is messy — don't treat it as gospel"; "the calendar is the source of truth, the to-do app isn't"; "spreadsheet prices lag the real ones — confirm before quoting". Only capture ones they actually give.]

### Where things live (source of truth)
[For each job, where the real answer lives — e.g. "client comms only happen in Slack, never email"; "meeting notes live in Granola"; "invoices live in Stripe, not the spreadsheet". This tells the AI where to look first.]
```

**Note on the tools legend:** inventory-plus-caveats only. Do NOT attempt to connect, authenticate, or scan any tool in the Context module. That is the Tools module's job. Just make the map rich enough that `/ai-os:connect` starts with a head start.

---

## 5. `offers.md` — what they sell, in detail

**Already on file (SHOW, don't re-ask):** the B2 offer LIST + rough prices — the skeleton has the shape. `/ai-os:build-context` fills the detail via **B2-deep**, one offer at a time. **Never re-collect the offer names or prices** — read them back and expand each. Drag-in docs (price list, offer doc, sales page) are gold here — extract through the validation gate.

```markdown
# Offers

[One block per offer/product/service. Repeat the block per offer. Drop any heading that doesn't apply. The names + rough prices are already on file — expand each, don't re-ask them.]

## [Offer name — already on file]
- **What it is:** [one line]
- **Who it's for / not for:** [which slice of the ICP — and who it's a bad fit for]
- **Price:** [already on file from B2 — exact if known, ballpark if not; never guess a hard number; flag as approximate if unsure]
- **What's included / deliverables:** [the actual thing they get — B2-deep]
- **Format / length:** [1:1, group, self-serve, per-job; duration if time-boxed]
- **The promise / outcome:** [what changes for the customer — B2-deep]
- **Guarantee / risk reversal:** [if any — B2-deep]
- **Common objection:** [what people hesitate about before buying — B2-deep]
- **Positioning vs the others:** [when to point someone here vs another offer — B2-deep]

## [Next offer]
[same block]

## Notes
[Bundles, upsells, payment plans, seasonal pricing, anything that shapes how offers are sold.]
```

**Money rule:** never invent or guess a price. The rough prices are already on file from onboard — confirm them, don't re-ask; if the student is vague, capture the range and mark it approximate. This mirrors the common hard rule "never guess at money figures".

---

## 6. `ideal-customer-profile.md` — who they serve

**Already on file (SHOW, don't re-ask):** the B3 customer sketch — the skeleton has the one-paragraph sketch. `/ai-os:build-context` expands it into a real ICP via **B3-deep**. **Never re-collect the basics** — read the sketch back and build on it. Drag-in docs (personas, research) and, post-`/ai-os:connect`, real customer emails deepen this further.

```markdown
# Ideal Customer Profile

## Who they are
[From the B3 sketch already on file, expanded. Demographics AND psychographics: who the typical customer/client is, in a sentence someone could picture.]

## Their pains — what keeps them up at night
[B3-deep. The problems that drive them to buy. Concrete, in their world's terms.]

## What they want — the outcome they're buying
[B3-deep. The transformation or result they're really after, beyond the product itself.]

## The language they use
[B3-deep. Actual words and phrases customers use to describe their problem and their goal. This is gold for copywriting — capture real quotes if the student has them. Say "I keep losing leads because I forget to follow up", not "prospect nurture inefficiency".]

## What they've tried that didn't work
[B3-deep. What they reached for before finding the student — context that sharpens positioning.]

## Objections — why they hesitate
[B3-deep. The reasons they don't buy: price, trust, timing, "will this work for me", etc. And, if known, how the student answers each.]

## Who to avoid — the bad-fit customer
[B3-deep. The type of customer that's a bad fit / to steer clear of, if they named one.]

## Where they hang out
[Channels, communities, platforms where these people actually are — useful for the marketing brain later.]
```

---

## Business-area context

For root-v3/root-v2, keep business-area knowledge in the appropriate core context file;
do not create nested guidance/signposts. For cohort-v1, preserve and deepen its
existing folder `CLAUDE.md` plus thin `AGENTS.md` signpost.

**Structure (brief F — durable context only):** the brain has exactly three moves — **What this folder is → What I know about it → How to work here.** DELIBERATELY NO "what's currently in it" file inventory — a list of the files sitting in the folder goes stale the moment anything changes (same reason the workspace map was dropped). Everything in the brain must be *durable*: true next month, not just today.

**Pre-fill first.** Before asking, load the relevant context and—on
cohort-v1—existing folder guidance. Show it back, then deepen.

**Flow:** show what is known → ask one tailored question → preview the target
context diff. Root-v2 writes the relevant core file; cohort-v1 may update and
verify its folder guidance/signpost.

```markdown
# [Folder name]

## What this folder is
[What this area of the business IS and what belongs in it. Durable — the area's purpose, not a file list. One or two lines. E.g. "This is where all marketing lives — content, channels, campaigns."]

## What I know about it
[The durable context that makes the AI a briefed specialist here: how this area actually works, the channels/clients/systems it involves, the standing facts that stay true over time. Folded from interview answers + anything migrated in. NOT "what files are in here right now" — that rots. Facts, not a directory listing.]

## How to work here
[The rules, preferences, and gotchas specific to this area — including any scope-specific hard rule routed here from onboard. E.g. for marketing: "always run copy through the voice-dna file, then the de-slop pass"; for a client: "they hate jargon, keep everything plain"; a routed rule: "social posts always end with the clipboard CTA".]
```

**Tailored per-folder prompts** (adapt to the student's real folders — these are examples, not a fixed set; and open by showing what's already known where you can):

- **marketing / content:** "Tell me about your marketing — what is this area for you (channels, what you do here), and are there any rules for how you like marketing work done?"
- **sales:** "How does sales work for you — where do leads come from, and how do you like it handled?"
- **finance:** "What should I know about the money side — how you think about it, and anything I should never guess at or touch without checking?"
- **operations:** "What runs the business day-to-day here — the systems and the way you like things done?"
- **a client folder:** "Tell me about [client] — what do you do for them, and how do they like to be communicated with? (Durable stuff, not this week's tasks.)"
- **product:** "What's the shape of the product side — what it is, and how you like product work approached?"

Only walk the folders that actually exist in the student's tree. Don't invent departments. If a folder is genuinely empty of durable context ("nothing there yet"), leave a light stub and move on — don't force detail that isn't real.
