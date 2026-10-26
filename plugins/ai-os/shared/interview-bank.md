# Interview Bank

Resolve `PLUGIN_ROOT` and `HOST_RUNTIME` from `<PLUGIN_ROOT>/shared/runtime.md` before using this bank. Render skill mentions, web lookups, interactive choices, instruction filenames, and scheduling language for the active host only.

The single, shared question bank for the ai-os interview. Three skills read from this one file so their questions never drift apart:

- **onboard** (Build OS module) — runs the core interview to build a solid **surface-level** base. No private tools connected yet. Builds the OS and skeleton context files without exhausting the student.
- **context** (Context module) — the **deep dive**. Fills the core-six context files and voice layer. By now the student may have supplied real writing samples and, after connect, may have private tools available.
- **update-context** (utility, anytime) — pulls a single section or question to refresh one file.

Because all three share this file, a change here updates every skill at once. That is the whole point — edit the question once, here.

---

## The onboard-surface vs context-deep split — READ THIS FIRST

Every question below carries a **scope tag** on its own line. There are exactly two:

- **`[SCOPE: onboard-surface]`** — asked in **Build OS module (`/ai-os:build-os`)** to build the base, AND re-visited (never re-asked cold — see below) in Context module. These get the *surface* answer only.
- **`[SCOPE: context-deep]`** — **NOT asked in `/ai-os:build-os` at all.** These belong to **Context module (`/ai-os:build-context`)**, where there's time and (often) real samples/scanned sources to do them justice. The whole voice deep-dive (Section V) is context-deep.

Some questions are **split**: `/ai-os:build-os` captures a light one-liner (`onboard-surface`), and a **separate deeper companion question** owns the depth in `/ai-os:build-context` (`context-deep`). Those are paired and cross-referenced so nothing is lost and nothing is asked twice.

### The golden rule: `/ai-os:build-context` and `/ai-os:update-context` PRE-FILL from onboard — they NEVER re-ask

By the time `/ai-os:build-context` runs, `/ai-os:build-os` has already captured the surface answers into the progress file. `/ai-os:build-context` must **read that file first** and, for every question, do one of two things:

1. **Deepen** what onboard already got — open with *"In Build OS module you told me [X] — let's build on that,"* then go deeper. Never make the student repeat an answer they already gave.
2. **Fill a gap** — only ask cold if onboard genuinely didn't capture it (i.e. a `context-deep` question with no onboard companion).

To make this easy, every `onboard-surface` question below has an **`Onboard captures:`** line stating exactly what Build OS module pulls out — so the `/ai-os:build-context` author knows precisely what's already on file to build on, and the `context-deep` companion knows where to pick up.

This is the fix for the repeated-answer fatigue Remy flagged in the v2 test. If `/ai-os:build-context` ever re-asks something onboard already answered, that's a bug.

---

## Renumbering / mapping note (for skill authors)

This bank was trimmed ~20% in the v2 pass. IDs kept their section-prefix scheme (A/B/C/D + V). What changed from v1:

| v1 ID | v2 status |
|---|---|
| A1–A3, A5 | unchanged, now tagged `onboard-surface` |
| A4 (expertise) | **split** → `A4` surface one-liner in onboard; depth folded into `/ai-os:build-context` (see A4 note) |
| B1, B4, B5 | unchanged, `onboard-surface` |
| B2 (offers/pricing) | **split** → `B2` surface list in onboard; **new `B2-deep`** owns full offer breakout (`context-deep`) |
| B3 (customers/ICP) | **split** → `B3` surface sketch in onboard; **new `B3-deep`** owns full ICP (`context-deep`) |
| C1–C4 | `onboard-surface`; C1 expanded with more examples + ASCII-tree pairing |
| D1 | `onboard-surface`; more concrete output examples added |
| D2 (hard rules) | `onboard-surface`; split into 3 labelled buckets + scope-specific routing rule added |
| D3, D4 (daily/weekly) | `onboard-surface`, kept but **lighter** (see note) |
| D5 (timezone) | `onboard-surface`, unchanged |
| **D6 (tools inventory)** | **NEW** `onboard-surface` — feeds a `tools` legend; precursor to Tools module `/ai-os:connect` |
| V1–V4 | unchanged, all `context-deep` (voice was already context-only) |

**Net:** `/ai-os:build-os` now runs A1–A5, B1–B5 (B2/B3 light), C1–C4, D1–D6. The deep companions (A4 depth, B2-deep, B3-deep) and all of Section V run only in `/ai-os:build-context`.

**v3 (beginner-test fixes):** A2 gained the **website-first flow** (paste a link → fetch → confirm; allowed on Day 1 — a public page is not a connector); B2 gained the **ask-once currency follow-up** (`student.currency`); B5 reframed from a single #1 priority to **1–3 ranked priorities**; C4 is now **gated behind a code-experience yes/no** (using an interactive choice when available, otherwise one plain-language yes/no question) so true beginners are never interrogated about folders.

---

## How a skill consumes this file

1. **Pull only the questions your scope owns.** `/ai-os:build-os` runs every `onboard-surface` question, A → B → C → D, in order. `/ai-os:build-context` runs the `context-deep` questions AND re-visits the `onboard-surface` ones in *deepen/fill-gap* mode (never re-asking — see the golden rule). `/ai-os:update-context` pulls one question or one section.
2. **Ask ONE question at a time.** Never batch. Ask, wait for the answer, acknowledge briefly ("Got it."), then move on. This is the battle-tested `HARD-GATE` from the old repos — keep it verbatim in every skill.
3. **Always show examples.** Every question below ships 4–8 concrete example answers. Show them every time. Most students can't answer "what's your voice?" from a blank page — they react to examples. Examples are not optional.
4. **Show, don't ask, when you can pre-fill.** If earlier answers already imply the answer, propose it and let them react ("Based on what you said, I'd guess X — right?") rather than asking cold.
5. **Multiple choice beats free text** for beginners wherever the answer fits a short list. Free text only where the answer is genuinely open.
6. **Preview before writing.** Never write a context file without showing it first and getting a yes.

### Pre-fill logic — read this carefully (it differs by skill)

Many questions below say *"pre-fill from..."*. There are **two very different pre-fill sources**, and which one is available depends on the skill:

- **In onboard (Build OS module): NO private tools are connected yet.** Tool scanning is Tools module (connect). The only pre-fill sources are **what the student has already told you in this conversation** and **their public website if they pasted the link in A2** (using the active host's public web capability). Do not claim to have read Gmail, Drive, or LinkedIn. If an earlier answer implies a later one, use it rather than asking cold.
- **In `/ai-os:build-context` / `/ai-os:update-context`: TWO pre-fill sources are now live.** (a) **The onboard progress file** — always read it first and deepen/fill-gap, per the golden rule above. (b) **Scanned sources** (if `/ai-os:connect` has run in Tools module) — sent emails for voice, Drive/Docs for business facts, meeting notes, brand guides. The *"check bios / email signatures / writing samples"* guidance below applies **only in this second pass.** When it runs, present findings the proven way: *"Based on your [emails / meeting notes / brand guide], it looks like [X]. Here's what I found: [examples]. Is that right, or would you change anything?"*

Every question below tags its pre-fill guidance as **[onboard: from conversation only]** and/or **[post-connect: from scanned sources]** so the skill author knows which applies.

### Section → context-file map (spec §5 core six)

| Section | Feeds |
|---|---|
| A — You | `about-me.md` (+ `business.md` one-liner) |
| B — The business | `business.md`, `offers.md`, `ideal-customer-profile.md` |
| C — Structure discovery | the folder tree + migration plan (not a core-six file — drives the build) |
| D — How you work | `working-style.md` (its `## Tools` section holds the D6 tools legend) |
| Voice deep-dive (Section V, `context-deep`) | `voice-dna.md` |

---

## Section A — You → `about-me.md` (+ business one-liner → `business.md`)

### A1. Name and role
**[SCOPE: onboard-surface]**
**Onboard captures:** their name + a plain label of what they do (the archetype signal).
**Ask:** "Let's start simple — what's your name, and what do you do?"
**Format:** Free text.
**Feeds:** `about-me.md` → Identity.
**Pre-fill:** [onboard: from conversation only — usually the first thing they say, so nothing to pre-fill] · [post-connect: from email signatures, bios, about pages].
**Examples:**
> "I'm Sarah, I run a content marketing agency."
> "I'm James, a freelance brand strategist."
> "I'm Maria, co-founder of a SaaS startup — I handle product and marketing."
> "I'm Dave, a solo consultant helping small businesses with their operations."
> "I'm Priya, I run a physiotherapy clinic with three staff."
> "I'm Tom, I'm a marketing manager at a mid-size software company." (employee — note the archetype signal for Section B)

### A2. Business one-liner (website-first)
**[SCOPE: onboard-surface]**
**Onboard captures:** one sentence describing the business — the anchor line for `business.md` — plus, if they have a website, the confirmed basics pulled from it (what the business does, offers, audience, tone) to pre-fill later questions.
**Ask (offer the website shortcut first):** "Got a website? Paste the link and I'll read it so you don't have to type out the basics. No website? No problem — just tell me: in one sentence, what does your business do?"
**Format:** URL or free text.
**Feeds:** `about-me.md` → Identity, and the anchor line of `business.md`; website basics also pre-fill B1/B2/B3 and a light voice note.
**⚑ URL flow (for onboard):** if they paste a link, use the active host's public web-browsing capability. This is allowed on Day 1: a public page is not a private connector or inbox/Drive scan. Extract the obvious basics, then **CONFIRM** them instead of asking cold. If browsing is unavailable or the fetch fails, fall back to the normal question without fuss.
**Pre-fill:** [onboard: from their website if they pasted one (fetch + confirm), otherwise from conversation only — may be implied by A1] · [post-connect: website tagline, email footer, about page].
**Examples:**
> "We help DTC brands create content that actually converts."
> "I coach founders through their first 18 months of business."
> "We build automation systems for agencies drowning in manual work."
> "I'm a fractional CMO for B2B startups."
> "We sell handmade ceramics online and at local markets."
> "We're a local plumbing company covering the north side of the city."

### A3. What you do all day
**[SCOPE: onboard-surface]**
**Onboard captures:** their main work buckets (multi-select) + one line of colour — the archetype signal for Section B.
**Ask:** "What do you spend most of your working time on? Pick all that apply."
**Format:** Multi-select, then a follow-up for colour.
**Feeds:** `about-me.md` → Daily Focus (also a signal for the archetype inference in Section B).
**Options:**
- Content creation (writing, video, social)
- Client work (consulting, coaching, services, deliverables)
- Strategy and planning
- Operations and admin
- Sales and outreach
- Product development
- Team management
- Other (free text)

**Follow-up (ask after they pick — for colour, one line):**
> - If content: "Mostly writing (blogs, newsletters), video (YouTube, Reels), social (LinkedIn, X), or a mix?"
> - If client work: "Mostly on calls, building deliverables, managing projects, or a mix?"
> - If operations: "Bookkeeping, invoicing, scheduling, hiring, or something else?"
> - If sales: "Cold outreach, warm follow-ups, calls, proposals?"

**Pre-fill:** [onboard: from conversation only — often implied by A1/A2] · [post-connect: calendar patterns, sent-email volume by type].

### A4. What you're great at (expertise)
**[SCOPE: onboard-surface]** — light one-liner in onboard; the depth is a `/ai-os:build-context` job (see note).
**Onboard captures:** a ONE-LINE headline of their expertise (the thing not to over-explain to them). Nothing more.
**Ask:** "What's your area of expertise — the thing I should know you already know cold? Just the headline for now; this stops me over-explaining stuff you're already expert in."
**Format:** Free text (one line).
**Feeds:** `about-me.md` → Expertise.
**Pre-fill:** [onboard: from conversation only] · [post-connect: bios, credentials, topic-heavy content].
**Examples:**
> "I know SEO inside out — 12 years of it."
> "I'm a certified financial planner, so I know the regulations cold."
> "I'm an expert in Notion and automations — I teach courses on it."
> "I've built and sold three e-commerce brands, so I know DTC deeply."
> "I'm not technical at all, but I know my customers better than anyone."
> "I'm a qualified physio — 15 years treating sports injuries."

**Note for /ai-os:build-context (the depth pass):** don't re-ask this. Open with *"In Build OS module you said your expertise is [X] — let's go deeper,"* then draw out the sub-specialisms, the things they DON'T want explained, and where they're the authority vs still learning. That nuance is what makes the OS stop over-explaining — but it's Context module work, not day one.

### A5. Tech comfort level
**[SCOPE: onboard-surface]**
**Onboard captures:** their tech-comfort setting — the single most important dial for how every later skill talks to them.
**Ask:** "Last one about you — how comfortable are you with tech and tools? Be honest, there's no wrong answer. It just tells me how much to explain."
**Format:** Multiple choice.
**Feeds:** `about-me.md` → Tech comfort (and it changes how EVERY later skill talks to them — a key setting).
**Options:**
- **Total beginner** — "I can use apps, but anything technical loses me. Explain everything."
- **Comfortable user** — "I'm fine with normal software (email, docs, Canva). New technical stuff I need walked through."
- **Fairly capable** — "I pick things up fast, I've dabbled with automations or no-code tools."
- **Technical** — "I can read code / I've built things. You can skip the basics."

**Pre-fill:** [onboard: from conversation only — if they've used technical words correctly, gently note it but still ASK; the course audience often forwards jargon they don't own] · [post-connect: n/a].
**Examples of what to say back:**
> "Total beginner is the most common answer here, and honestly the best starting point — I'll never assume you know a term. Sound right?"

---

## Section B — The business → `business.md`, `offers.md`, `ideal-customer-profile.md`

> **This section is what drives the archetype inference.** B1 (who pays for what) is the single most important signal for which reference tree in `templates.md` fits. Read the student's B answers against the inference signals in `templates.md` — never show them a menu, never name the template.
>
> **Depth split:** offers (B2) and customers (B3) each keep a LIGHT surface question in `/ai-os:build-os` and hand their real depth to a `context-deep` companion (B2-deep, B3-deep). Don't mine offers or ICP hard on day one — that's what fatigued the v2 tester.

### B1. Business model — who pays you, for what?
**[SCOPE: onboard-surface]**
**Onboard captures:** the money model in the student's own words — the key archetype driver.
**Ask:** "How does the money actually work — who pays you, and what do they pay for?"
**Format:** Free text (this is the key one — let them talk).
**Feeds:** `business.md` → Model (and drives the archetype pick).
**Pre-fill:** [onboard: from conversation only — often implied by A2] · [post-connect: invoices, Stripe, proposals].
**Examples (each hints a different archetype — see `templates.md`):**
> "Clients pay me a monthly retainer to run their content." → client services / agency
> "People buy my course and subscribe to my newsletter; some hire me 1:1." → solo brand / creator
> "Customers buy our product online, one-off purchases." → product / e-com
> "Locals book us for a job — a repair, an install — and pay per job." → local / service business
> "Clients pay for a coaching package — usually 3 months, weekly calls." → coaching / consulting
> "I don't own the business — I get a salary; I'm trying to level myself up." → employee / intrapreneur

### B2. Offers and rough pricing (surface)
**[SCOPE: onboard-surface]** — light list only; the full breakout is B2-deep in `/ai-os:build-context`.
**Onboard captures:** a simple LIST of what they sell and rough prices — the shape, not the detail — plus their **currency** (`student.currency`), asked once at the first mention of money.
**Ask:** "Quick version for now — what do you sell, and roughly what does each thing cost? A ballpark list is perfect; we'll go deeper on this later."
**Format:** Free text, encourage a short list.
**Feeds:** a summary line in `business.md`, and a skeleton `offers.md` that B2-deep fills out in Context module.
**Pre-fill:** [onboard: from conversation only] · [post-connect: price list, sales page, proposals, Stripe products].
**Examples:**
> "Content retainer — $3k/month. One-off audit — $1,500. Strategy day — $2,500."
> "Newsletter (free), course ($499), 1:1 coaching ($1,500/session)."
> "Three product lines, $25–$80 each; a bundle at $150."
> "Coaching package — $6k for 12 weeks. A group program — $2k."
> "Just the one service really — I install and service HVAC, priced per job."
> "I don't sell anything directly — I run marketing for my employer." (employee)

**Follow-up — currency (a quick beat, not a new question; ask ONCE, ever):** the first time money comes up — usually right here — add: "And that's in USD, euros, pounds…?" Store it as `student.currency` in the progress file and use it for every money figure from then on — never re-ask a currency already captured. (If money first appears somewhere else instead — say a revenue goal in B5 — ask it there. The rule is: first money moment, once.)

**Note for /ai-os:build-os:** capture the shape and STOP. Do not ask about features, guarantees, positioning, or why each offer exists — that's B2-deep in Context module. Getting the list is enough to stand up the OS.

### B3. Who are your customers? (surface sketch)
**[SCOPE: onboard-surface]** — a sketch only; the full ICP is B3-deep in `/ai-os:build-context`.
**Onboard captures:** a one-paragraph sketch of the typical customer — enough for a `business.md` line and a skeleton ICP file.
**Ask:** "Give me the quick sketch — who's your typical customer or client? A sentence or two; we'll build the full picture later."
**Format:** Free text.
**Feeds:** a line in `business.md`, and a skeleton `ideal-customer-profile.md` that B3-deep fills out in Context module.
**Pre-fill:** [onboard: from conversation only] · [post-connect: CRM, client folders, sent email recipients].
**Examples:**
> "DTC founders doing $1–5M a year who can't keep up with content."
> "First-time founders, 6–18 months in, overwhelmed and under-systematised."
> "Women 25–40 who buy our jewellery as a treat or a gift."
> "Homeowners in the local area, usually 40+, who found us on Google."
> "Corporate teams whose managers want their people coached."
> "My internal stakeholders — the sales team and the CEO." (employee)

**Note for /ai-os:build-os:** just the sketch. Don't dig into pains, objections, or the language they use — that's B3-deep in Context module.

### B4. Team or solo?
**[SCOPE: onboard-surface]**
**Onboard captures:** solo vs team, and if a team, a one-line "who does what" — drives whether the tree gets a `team/` folder.
**Ask:** "Is it just you, or do you have a team? If there's a team, who does what?"
**Format:** Free text.
**Feeds:** `business.md` → Team; also shapes the tree (a `team/` folder only earns its place if there's a team).
**Pre-fill:** [onboard: from conversation only] · [post-connect: email threads, org info].
**Examples:**
> "Just me right now."
> "Me plus two contractors — a designer and a VA."
> "Small team: me, an ops lead, and three part-time staff."
> "Me and a co-founder — she does product, I do growth."
> "I've got five employees at the clinic."
> "I'm one of a 20-person marketing department." (employee)

### B5. Top priorities (1–3, ranked)
**[SCOPE: onboard-surface]**
**Onboard captures:** their top 1–3 durable priorities, RANKED (quarter-plus goals, not to-dos). One is ideal; two or three ranked together is fine — never force exactly one.
**Ask:** "What's the #1 thing you're trying to make happen in the next 90 days? If you genuinely can't pick one, give me your top two or three and we'll rank them together."
**Format:** Free text.
**Feeds:** `business.md` → Top priorities (kept deliberately high-level — durable goals, not this-week to-dos).
**Pre-fill:** [onboard: from conversation only] · [post-connect: recent docs, project boards].
**Examples:**
> "Land three new retainer clients this quarter."
> "Launch my first course and get 100 people in."
> "Hit $50k months consistently."
> "Systematise the business so it runs without me in the room."
> "Get more 5-star reviews and rank higher on Google locally."
> "Prove ROI on our marketing so I get budget for next year." (employee)

**Steer:** keep these durable (a quarter-plus horizon), NOT transient tasks. If they give you a to-do ("finish the deck by Friday"), gently zoom out: "That's this week — what's the bigger goal it ladders up to?" If they give more than one, rank them together ("If you could only move ONE of these this quarter, which?") and capture the order — three max. And if a priority is a money goal and their currency isn't captured yet, ask the currency follow-up from B2 here (once, then reuse).

### B2-deep. Full offer breakout
**[SCOPE: context-deep]** — Context module only. Do NOT ask in `/ai-os:build-os`.
**Builds on:** the offer LIST captured by B2 in Build OS module. Read it from the progress file first.
**Ask (deepen, don't re-ask):** "In Build OS module you listed [their offers]. Let's turn that into a proper offers file. For each one — walk me through what's actually included, who it's for, what makes it worth the price, and any guarantee or promise attached."
**Format:** Free text, iterate offer by offer.
**Feeds:** the full `offers.md` — one block per offer: what's included, positioning, the promise/outcome, guarantees, common objections, where it sits vs the others.
**Pre-fill:** [post-connect: sales pages, proposals, Stripe products, price lists — pull the real details and confirm] · [from onboard: the offer list is already on file; expand each, never re-collect the names].
**Per-offer prompts (one at a time):**
> - "What exactly does someone get when they buy [offer]?"
> - "Who's it the right fit for — and who is it NOT for?"
> - "What's the main outcome or transformation it promises?"
> - "Any guarantee, refund policy, or risk-reversal?"
> - "What do people usually hesitate about before buying it?"
> - "How's it different from your other offers — when would you point someone to this one vs another?"

### B3-deep. Full ideal-customer profile
**[SCOPE: context-deep]** — Context module only. Do NOT ask in `/ai-os:build-os`.
**Builds on:** the customer SKETCH captured by B3 in Build OS module. Read it from the progress file first.
**Ask (deepen, don't re-ask):** "In Build OS module you sketched your customer as [their sketch]. Let's build the full picture now — this is what lets me write in a way that actually lands with them."
**Format:** Free text, guided by the prompts below, one at a time.
**Feeds:** the full `ideal-customer-profile.md` — demographics/firmographics, the pains, the exact language they use, what they've already tried, their objections, and what winning looks like for them.
**Pre-fill:** [post-connect: CRM, testimonials, sales-call notes, sent emails, reviews — mine the customer's OWN words and show them back] · [from onboard: the sketch is on file; expand it, never re-collect the basics].
**Deepening prompts (one at a time):**
> - "What's the painful problem that makes them come looking for you?"
> - "In their words — how would THEY describe that problem? (the phrases they actually use)"
> - "What have they already tried that didn't work?"
> - "What's their big objection or hesitation before buying?"
> - "What does a great outcome look like for them — how do they measure it?"
> - "Is there a type of customer you should AVOID / that's a bad fit?"

---

## Section C — Structure discovery → the folder tree + migration plan

> This section produces the raw material for the tree you propose in Phase 3 of /ai-os:build-os. Match their answers to a reference tree in `templates.md`, pre-fill it with their REAL names, and show it back. Never show a menu of archetypes.

### C1. Departments / areas
**[SCOPE: onboard-surface]**
**Onboard captures:** the handful of "areas" the student thinks about separately — these become the top-level business folders.
**Ask:** "Now let's map the shape of your business. Think of it as having a few different 'areas' — the parts you think about separately. Which ones are real for you? Don't overthink it."
**Format:** Free text / loose list.
**Feeds:** the top-level business folders in the tree.
**⚑ Pair this with a LIVE ASCII folder-tree preview.** As they name areas, the skill should draw the tree forming — *"here's the shape building up"* — so they SEE their answers turning into folders and understand WHY you're asking. (The skill owns the diagram; this question just prompts for it. Beginners get lost here without the visual.) Redraw it as they add or rename areas.
**Pre-fill:** [onboard: from conversation only — infer likely areas from B answers and PROPOSE them, e.g. "An agency usually has content, sales, finance, and client delivery — which of those feel right?"] · [post-connect: existing folder names].
**Examples — show a spread across business types so they see themselves:**
> **Agency / client services:** "Content, client delivery, sales, and finance."
> **Creator / solo brand:** "Content, my newsletter, products/courses, and audience/community."
> **E-commerce / product:** "Products, marketing, fulfilment/ops, customer support, and finance."
> **Local service business:** "Bookings/jobs, the actual service work, marketing, and admin/money." (e.g. a clinic: "bookings, treatment, marketing, admin")
> **Coach / consultant:** "Clients, my content/marketing, my offers/programs, and operations."
> **Employee inside a company:** "The projects I own, my reporting/analytics, stakeholder comms, and my own growth/learning."
> **Honestly it's all just me:** "I don't split it into areas yet." → that's fine; propose a light default from their B answers and show it in the tree.

### C2. Clients (names)
**[SCOPE: onboard-surface]**
**Onboard captures:** named clients (if any) — each becomes a subfolder under `clients/`.
**Ask:** "Do you work with named clients? If so, who are they? Just the names — I'll give each one its own folder."
**Format:** Free text list.
**Feeds:** the `clients/` grouping in the tree (one subfolder per client).
**Pre-fill:** [onboard: from conversation only] · [post-connect: client folders, CRM, invoice recipients].
**Examples:**
> "Yes — Acme Corp, BigCo, and N-Space."
> "Three regulars: Riverside Dental, Two Trees Cafe, and Landmark Homes."
> "I have clients but I'd rather not folder them individually — group them."
> "No named clients — I sell to lots of small customers." (→ no `clients/` folder; skip)
> "Just one big client right now, but more coming."

**Rule:** if there are multiple named clients → they go under a single `clients/` parent, one subfolder each. If none → skip the `clients/` folder entirely.

### C3. Brands / sub-businesses
**[SCOPE: onboard-surface]**
**Onboard captures:** whether there's one business or several (the HYBRID signal — one root vs sibling roots).
**Ask:** "Do you run more than one brand or business? Sometimes people have a main thing plus a side project, or a personal brand alongside their company."
**Format:** Free text.
**Feeds:** whether the tree has ONE business root or MULTIPLE sibling roots (the hybrid case — see `templates.md`).
**Pre-fill:** [onboard: from conversation only — watch for this in A/B answers; it's easy to miss] · [post-connect: distinct domains, separate email accounts].
**Examples:**
> "Just the one business."
> "My agency, plus I'm building a personal brand on LinkedIn." → HYBRID (two trees side by side)
> "Two e-com brands under one company."
> "The clinic, and a separate online course I sell." → HYBRID
> "My main consulting business and a small property side-thing." → HYBRID (business vs personal — separate)

**Rule:** if they name two distinct brands/businesses → propose TWO business-folder trees as siblings at the OS root (don't force one). See the HYBRID HANDLING section in `templates.md`.

### C4. Existing folders to migrate in (gated — Claude Code experience check first)
**[SCOPE: onboard-surface]**
**Onboard captures:** (a) whether they've used Claude Code or other coding tools before this course (the gate), and (b) — only if yes — the folders they want to bring in, one line each: the raw material for the migration plan.
**⚑ THE GATE — MANDATORY. Ask it in EVERY onboarding run, before any folder questioning.** Never skip this question, and never infer its answer from A5's tech-comfort rating or anything else the student has said — asking is the requirement, only the folder follow-up is conditional. (A real test run never asked it, so a student's existing Claude Code project folders were never offered a home.) Use the host's interactive choice control when available; otherwise ask one plain-language question and wait: "Before this course, had you already used Claude Code — or any other code or coding tools?" — **Yes / No.**
- **No** → skip the rest of C4 entirely. Don't interrogate a true beginner about folders and paths — it's meaningless and intimidating. Quietly keep anything the Phase 0 sweep spotted on file for later sessions, and move on to Section D.
- **Yes** → continue with the ask below.
**Ask (only after a YES on the gate):** "Do you have any existing project folders — from Claude Code or anything else you've worked in — that you'd like to fold into this setup? If so, tell me the names of the folders and what each one is."
**Format:** Free text, iterative — collect them one at a time, ask a one-liner for each.
**Feeds:** the migration plan (old-path → new-path table) in Phase 4.
**Pre-fill:** [onboard: surface the specific work-looking folders the Phase 0 sweep spotted, BY NAME ("I spotted a folder called `Acme-grants` on your Desktop — is that work stuff you'd want to bring in?") rather than making them remember paths; names only — file contents are never read in Build OS module] · [post-connect: actual filesystem listing].
**Examples:**
> "I've got ~/Projects/website — that's my company site."
> "~/marketing has all my content and social stuff."
> "Freelance work in ~/clients/acme and ~/clients/bigcorp."
> "A ~/courses folder with all my course material."
> "Loads of random stuff on my Desktop, honestly."
> "Nothing organised yet — I'm starting fresh." (→ skip migration entirely)

**Follow-up for each folder:** "What's in [folder]? One line, so I can file it in the right place."

**Grouping rules (apply when proposing the migrated structure):**
- Multiple client folders → group them under `clients/`.
- A mix of business and personal → separate top-level folders; never blend personal into a business root.
- A code project (a website, an app) → keep it as its own top-level project folder.
- Folder names → always lowercase-with-hyphens (`my-website/`, not `My Website/`).
- **Confirm before ANY move.** Show the old-path → new-path table, get an explicit yes, then move. Never move a file silently.
- Starting fresh with no folders → skip this whole step.

---

## Section D — How you work → `working-style.md` (its `## Tools` section holds the D6 tools legend)

### D1. Output-format preferences
**[SCOPE: onboard-surface]**
**Onboard captures:** how they want output laid out — the pick + any concrete formatting rules they react to.
**Ask:** "When I hand you something back — a summary, a draft, an answer — how do you like it laid out?"
**Format:** Multiple choice + a follow-up.
**Feeds:** `working-style.md` → Output preferences.
**Options:**
- **Concise bullets** — short, scannable, no fluff.
- **Detailed narrative** — full explanations, the reasoning, the "why".
- **Structured with headers** — organised sections, clear hierarchy.
- **Depends on the task** — let me judge from context.

**Clarifying examples:**
> - Concise bullets: "3–5 points, no intro paragraph, just the key info."
> - Detailed narrative: "Full paragraphs. I want to understand the reasoning."
> - Structured: "Headers and sub-sections, like a well-organised doc."
> - Depends: "Short for a quick message, detailed for a strategy doc."

**Follow-up — show these CONCRETE examples (someone who's never used AI can't answer this abstractly; let them point at the ones that feel right):**
> "Here's how other people put it — tick any that sound like you, and add your own:"
> - "Bullet points, not paragraphs."
> - "Bottom line first, THEN the detail." (the answer up top, reasoning below)
> - "A TLDR at the top of long answers." (a 1–2 line summary before the full thing)
> - "Number your lists — 1, 2, 3 — so I can just reply 'option 2'."
> - "Keep it short — no preamble, no 'Sure! Here's...', just the thing."
> - "Always show me a table when you're comparing options."
> - "Give me 3 options, not just 1."
> - "Tell me what YOU'd do — don't just hand me a list of choices to make."
> - "Never a wall of text — break it up with headers or line breaks."
> - "Put the action items / next steps at the very end."

**Pre-fill:** [onboard: from conversation only] · [post-connect: n/a].

### D2. Hard rules (MUST / NEVER)
**[SCOPE: onboard-surface]**
**Onboard captures:** their always/never rules — sorted into the three buckets below, with scope-specific ones routed to the right folder (not the global rules).
**Ask:** "Any hard rules? Things that must ALWAYS happen, or must NEVER happen, when I work for you? These become permanent instructions I follow every time."
**Format:** Free text — show ALL three buckets of examples below to spark ideas.
**Feeds:** `working-style.md` → Rules, and resolved `MASTER_PATH` — **but only
the global ones**.
**Pre-fill:** [onboard: from conversation only — you can propose obvious ones from their tech level and business, e.g. a beginner almost always wants "never auto-send, always show me the draft first"] · [post-connect: SOPs, process docs, team guidelines].

**Present the examples in THESE THREE LABELLED BUCKETS (it helps beginners think of their own):**
> "Here are rules other people set, grouped by type — see what resonates, and add your own:"
>
> **① Communication rules** — how things should sound / be worded:
> - "Never use emojis in client emails."
> - "Always include a call-to-action in social posts."
> - "Don't write in 'we' — it's just me, so use 'I'."
> - "Keep client-facing writing formal; internal notes can be casual."
> - "One exclamation mark per email, max."
>
> **② Process rules** — how work should be done / handled:
> - "Never send anything to a client without me reviewing it first."
> - "Never commit to a deadline without checking with me first."
> - "Never delete files — archive instead."
> - "Always draft in a doc, never straight into email."
> - "Always check my calendar before scheduling anything."
> - "Spell-check anything client-facing before showing me."
>
> **③ AI-specific rules** — how I (the AI) should behave with you:
> - "Never auto-send emails — always show me the draft first."
> - "Never guess at money figures — if you're not certain, ask or flag it."
> - "Never make assumptions — check my files first, ask me last."
> - "If you're not sure, flag it rather than guessing."
> - "Don't summarise what you just did — I can see the changes."
> - "Don't ask me to confirm small things — just do them."
> - "Always explain your reasoning on a judgment call."
> - "Keep responses short — skip the preamble."

**⚑ ROUTING RULE — global vs scope-specific (bake this into the skill's behaviour):**
Some "rules" only apply to ONE area of their business, not everywhere. Example: *"always tag the clipboard action in social posts"* is a **social-posts** rule — it has no business governing their invoices or client emails. When the student gives a rule, the skill must decide:
- **Global rule** → resolved `MASTER_PATH` + `working-style.md`.
- **Scope-specific rule** → root-v3/root-v2 puts it in the relevant context file;
  cohort-v1 may put it in that folder's existing `CLAUDE.md`. Tell the student
  where it is filed.
When in doubt, ASK: *"Does this apply to everything, or just [that area]?"* Getting this right stops the global rules from filling up with narrow instructions that misfire elsewhere.

### D3. Recurring daily tasks (light)
**[SCOPE: onboard-surface]** — kept, but deliberately LIGHT on day one.
**Onboard captures:** a short list of durable daily-repeating tasks (the pattern, not today's to-dos). Just the list; don't over-mine.
**Ask:** "Quick one — what do you do most days, the routine tasks that come back every day? Just name them; I'm not after today's to-do list, the repeating ones."
**Format:** Free text, a short list is plenty.
**Feeds:** `working-style.md` → Daily rhythm. These are candidates for the active host's scheduling surface in the Autopilot module.
**Pre-fill:** [onboard: from conversation only — infer likely ones from A3, and PROPOSE them] · [post-connect: calendar, email patterns].

**Examples (show a handful — don't run the full checklist on day one):**
> "Common daily ones — which apply?"
> - "Check and respond to email."
> - "Review the calendar and prep for the day."
> - "Check messages (Slack / WhatsApp) and reply."
> - "Post on social."
> - "Write or edit content."
> - "Respond to client messages."
> - "Do some prospecting or outreach."

**CRITICAL steer — evergreen, not transient:** capture the *pattern*, not this week's calendar. "Triage my inbox each morning" is a keeper. "Prep for the Tuesday 3pm with Acme" is not. Generalise a specific meeting or project into a durable rhythm because the Autopilot module may schedule it on either host.
**Note for /ai-os:build-os:** keep this light — the goal is the shape of their day, not an exhaustive audit. `/ai-os:build-context` can deepen the rhythm later if useful.

### D4. Recurring weekly tasks (light)
**[SCOPE: onboard-surface]** — kept, but deliberately LIGHT on day one.
**Onboard captures:** a short list of durable weekly-repeating tasks (the pattern, with the day if they know it).
**Ask:** "And weekly — anything that comes round once a week, maybe on a set day?"
**Format:** Free text, a short list is plenty.
**Feeds:** `working-style.md` → Weekly rhythm. These are also candidates for the active host's scheduling surface.
**Pre-fill:** [onboard: from conversation only] · [post-connect: recurring calendar events].

**Examples (show a handful):**
> "Common weekly ones — which apply?"
> - "Write the newsletter (which day?)."
> - "Team standup or weekly meeting."
> - "Invoice clients."
> - "Plan content for the week."
> - "Review analytics / reporting."
> - "Client check-in calls."
> - "Weekly review or retrospective."

**Same evergreen steer as D3:** capture the recurring pattern ("send the weekly report every Friday", "plan next week's content on Sunday"), NOT a one-off ("send the Q3 board deck this Friday"). If it won't still be true in two months, generalise it or leave it out.

### D5. Timezone
**[SCOPE: onboard-surface]** — **always ask, never infer.**
**Onboard captures:** their timezone (city or TZ name), and a flag if it moves — load-bearing for the Autopilot module.
**Ask:** "Last one — what timezone are you in? I need this so that when we schedule things later, they fire at the right time for you."
**Format:** Free text (accept a city or a timezone name — normalise to something like "Europe/London" or note the city).
**Feeds:** `working-style.md` → Timezone. **Load-bearing for scheduling in the Autopilot module** — neither host may assume it.
**Pre-fill:** [onboard: from conversation only — do NOT guess from language or anything else; always ASK] · [post-connect: n/a — still ask, never infer].
**Examples:**
> "London (GMT/BST)."
> "US Eastern — New York time."
> "AEST, Sydney."
> "I travel a lot, so it changes — I'm in Bali right now." (note that it varies; capture current + flag it moves)
> "GMT+7."

**Why this exists:** scheduling needs the correct local time. Capturing it in Build OS module makes the active host's scheduling flow reliable. Never assume a timezone anywhere in the system.

### D6. Tools inventory — what you use, for what
**[SCOPE: onboard-surface]** — **NEW.** An inventory only. Do NOT connect anything here — connecting is Tools module (`/ai-os:connect`).
**Onboard captures:** a simple legend of their tools mapped to what each one is FOR — the raw list that Tools module `/ai-os:connect` will actually wire up.
**Ask:** "Let's list the tools you use and what you use each one for. I'm not connecting anything yet — just building a map."
**Format:** Category menu — show the common-stack categories below with a blank after each arrow and ask them to fill in the tool they use for each one. Skipping a line is fine ("no CRM" is a real answer); add extra lines for anything they use that isn't listed.
**Feeds:** the `## Tools` section of `working-style.md` and a slim mirror in
resolved `MASTER_PATH`.
**Pre-fill:** [onboard: from conversation only — infer likely tools from their business type and PROPOSE them as pre-filled lines in the menu, e.g. "Most agencies I see use Gmail + Google Calendar + something like Notion or Asana — I've penciled those in, correct me"] · [post-connect: the actual connected-tools list from Tools module confirms/expands this].
**The category menu (present this; they fill in the right-hand side):**
> "Here are the jobs most businesses have a tool for — tell me what you use for each. Skip any that don't apply, and add anything I've missed:"
> - Newsletter / publishing →
> - Marketing email →
> - Projects / planning →
> - Email →
> - Calendar →
> - Scheduling calls →
> - CRM →
> - Meeting notes →
> - Note taking →
> - Team comms →
> - Client comms →
**Extra categories to offer when they fit the business type:**
> - Payments / invoicing → (Stripe, PayPal, QuickBooks)
> - Storage / files → (Google Drive, Dropbox)
> - Design / graphics → (Canva, Figma)
> - Social scheduling → (Buffer, Later)
**Filled example (the shape to capture — how Remy's own maps out):**
> - Newsletter / publishing → **Beehiiv**
> - Marketing email → **Resend**
> - Projects / planning → **Notion**
> - Email → **Gmail**
> - Calendar → **Google Calendar**
> - Scheduling calls → **Cal.com**
**Note for /ai-os:build-os:** inventory ONLY. Do not attempt to connect, authenticate, or scan any tool here — that's the whole job of Tools module `/ai-os:connect`. Just capture the map so `/ai-os:connect` has a running start.

---

## Section V — Voice deep-dive → `voice-dna.md`

> **Entire section is `[SCOPE: context-deep]` — NONE of it runs in `/ai-os:build-os`.** Voice is the Context module job (`/ai-os:build-context`), because good voice work needs real writing samples and more time than day one allows. `/ai-os:build-os` may capture a light "how do you write?" note if it comes up naturally, but the real voice-DNA build happens here. The proven `voice-dna-base.md` anti-AI-slop rules are embedded at the TOP of every generated `voice-dna.md` before these personal layers.

### V1. Tone spectrum
**[SCOPE: context-deep]**
**Ask:** "How do you communicate? Think about your emails, messages, and posts — where do you sit?"
**Format:** Spectrum with examples.
**Feeds:** `voice-dna.md` → Tone.
**Pre-fill:** [post-connect: ALWAYS pre-fill from scanned sent emails / messages / posts once tools are connected — pull 2–3 real excerpts and show them] · [pre-connect: ask them to paste 2–3 real samples they've written, then place them].
**Spectrum:**
- **Very formal:** "Dear Mr. Smith, I hope this message finds you well. I am writing to enquire about…"
- **Professional:** "Hi John, thanks for reaching out. Here's what I'm thinking…"
- **Conversational:** "Hey! So here's the deal…"
- **Very casual:** "yo so basically here's what I reckon…"

**Present pre-filled like this (post-connect, or from pasted samples):**
> "From your writing, you sound like this:
> *Example 1:* '[real excerpt]'
> *Example 2:* '[real excerpt]'
> That reads as [conversational] to me. Match how you want me to write for you?"

### V2. Words you use / words you hate
**[SCOPE: context-deep]**
**Ask:** two parts — "Any words or phrases that feel very *you*?" then "Any words you'd never use — ones that make you cringe?"
**Format:** Free text, two parts.
**Feeds:** `voice-dna.md` → Language preferences.
**Pre-fill:** [post-connect: pull recurring phrases and patterns from their real writing] · [pre-connect: from any pasted samples].
**Examples — words you use:**
> - "I say 'let's crack on', not 'let's get started'."
> - "I use 'mate' and 'legend' a lot."
> - "I always open with 'Hope you're well'."
> - "Short, punchy sentences. I rarely write long paragraphs."
> - "I explain things with analogies."
> - "I swear casually internally, never externally."

**Examples — words you hate:**
> - "I hate 'synergy'."
> - "Never 'reach out' — just 'contact' or 'message'."
> - "One exclamation mark per email, max."
> - "No corporate speak: no 'circle back', 'deep dive', 'touch base'."
> - "Never 'I hope this email finds you well' — it's fake."
> - "No emojis in anything external."

### V3. Voice character
**[SCOPE: context-deep]**
**Ask:** "When I write as you, what should it sound like? Pick the one or two that fit best."
**Format:** Multiple choice (1–2).
**Feeds:** `voice-dna.md` → Voice characteristics.
**Options + examples:**
- **Direct and confident** — "Here's what we need to do," not "Perhaps we might consider…"
- **Warm and friendly** — like talking to a friend who's really good at their job.
- **Technical and precise** — data, specifics, evidence; no vague claims.
- **Casual and conversational** — you write like you talk; short, no fluff, the odd joke.
- **Inspiring and motivational** — big picture first, then practical; makes people want to act.

**Pre-fill:** [post-connect: strongly inferable from writing samples] · [pre-connect: infer from pasted samples].

### V4. Anti-voice (the six cringe archetypes)
**[SCOPE: context-deep]**
**Ask:** "What should I NEVER sound like? Here are six voices people usually hate — tell me which make you cringe, and add your own."
**Format:** Free text, react to the six.
**Feeds:** `voice-dna.md` → Anti-voice.
**The six anti-voice archetypes (present all six):**
> - **Corporate drone:** "Per our previous correspondence, I wanted to circle back regarding the deliverables timeline and ensure alignment across stakeholders."
> - **Fake enthusiastic:** "I'm SO excited to share this AMAZING opportunity!!! This is going to be INCREDIBLE!!!"
> - **Generic AI:** "In today's rapidly evolving digital landscape, it's important to leverage cutting-edge solutions to optimise your workflow."
> - **Overly academic:** "One might argue that the intersection of digital transformation and organisational change management presents a compelling case for…"
> - **Salesy pusher:** "Don't miss out! Limited time offer! Act now before it's too late! This exclusive deal won't last!"
> - **Passive and vague:** "It might be worth considering potentially looking into whether there could be an opportunity to perhaps…"

**Pre-fill:** [post-connect / pre-connect: if they write casually, "corporate drone" and "generic AI" are safe guesses — propose them] — "Based on how you write, I'd guess you'd hate the corporate-drone and generic-AI voices. Anything to add?"

---

## After the interview — what gets built

Once the relevant sections are done, the skill has enough to generate:

- **`about-me.md`** — from A1–A5 (A4 surface in onboard, deepened in /ai-os:build-context).
- **`business.md`** — from A2, B1, B3, B4, B5.
- **`offers.md`** — skeleton from B2 in /ai-os:build-os, full breakout from B2-deep in /ai-os:build-context.
- **`ideal-customer-profile.md`** — skeleton from B3 in /ai-os:build-os, full ICP from B3-deep in /ai-os:build-context.
- **`working-style.md`** — from D1–D5 plus its `## Tools` section from D6. The
  slim map is mirrored in resolved `MASTER_PATH`.
- **`voice-dna.md`** — from V1–V4 + `voice-dna-base.md` at the top (Context module / `/ai-os:build-context` only).
- **The new business/client folder tree** — from Section C, matched against
  `templates.md`.
- **Resolved `MASTER_PATH` Rules section** — from D2 (global hard rules only;
  scope-specific rules follow the resolved layout).

**Always preview each file and get a yes before writing it.**
