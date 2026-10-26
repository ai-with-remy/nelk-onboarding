# Archetype Templates

Internal guidance for the active AI host when proposing a student's workspace tree in onboard Phase 3. Resolve `PLUGIN_ROOT` and `HOST_RUNTIME` from `<PLUGIN_ROOT>/shared/runtime.md` first. **This file is NEVER shown to the student.** It is not a menu. The student never sees the six archetype names or picks from a list. Infer one recommended tree from their real answers, pre-fill it with their real names, then iterate with them.

> Product principle (spec §2.7, §4): "Templates are internal guidance for Claude, not a menu the student is locked into. Every tree is bespoke." Blend these freely. Rename anything. Add or drop folders to fit the real business.

## The universal root-v3 spine (added separately by /ai-os:build-os — NOT shown here)

Every student gets this identical spine regardless of archetype. `/ai-os:build-os` creates it directly; the archetype trees below add the BUSINESS folders on top of it:

```
Desktop/OS/
├── .agents/
│   └── skills/         ← canonical editable custom skills
├── .claude/
│   ├── skills/         ← link to ../.agents/skills
│   ├── sounds/         ← optional workspace chimes
│   └── .ai-os-progress.json
├── AGENTS.md           ← the one instructions file Claude Code and Codex read
├── MEMORY.md           ← conservative, approval-gated memory
├── context/            ← the OS's brain, the core six
└── [business folders — from the archetype trees below]
```

The trees below show ONLY the business and client folders. Never re-print the
technical spine as if it were part of a template.

## Folder naming rules (apply to every tree)

- **Every business gets its own named root folder — even a single business.** Its areas (`content/`, `marketing/`, `finance/`, `legal/`…) nest INSIDE `[business-name]/`, never loose at the OS root. One business = one root folder; two businesses = two root folders side by side. The only category folder allowed beside a business folder is `clients/` (archetypes 1 and 5). Exception: archetype 6 (an employee with no business of their own) keeps its four role folders at the root.
- Lowercase-with-hyphens, always: `client-deliverables/`, not `Client Deliverables/`.
- English folder names (course + live-support consistency); content inside can be any language.
- Root-v3 keeps guidance in the root master and `context/`; onboarding does not
  create guidance files inside business or client folders.
- Only create a folder that earns its place. No `team/` if they're solo. No `clients/` if they have no named clients. A sparse, true tree beats a bloated, aspirational one.

---

## 1. Client services / agency

**Inference signals (from Section B/C):**
- B1: paid a retainer or per-project/deliverable; "clients pay me to…".
- A3: "client work" is a big share of the day.
- B3: customers are named businesses, not lots of small consumers.
- C2: names actual clients.
- B4: often a small team (designer, VA, contractors) but can be solo.

**Reference tree (business folders):**
```
[agency-name]/
├── content/          ← the agency's own marketing: social, blog, lead magnets
├── sales/            ← pipeline, proposals, outreach, discovery-call notes
├── finance/          ← invoices, expenses, revenue tracking, contracts
├── operations/       ← SOPs, hiring, tools, internal process docs
└── legal/            ← agreements, NDAs, terms, insurance
clients/
└── [each-client]/
    ├── deliverables/ ← the actual work product for this client
    ├── comms/        ← emails, call notes, briefs, feedback threads
    ├── assets/       ← their logos, brand files, raw materials
    └── strategy/     ← plans, competitor notes, reporting for this client
```
Repeat the `[each-client]/` block once per named client from C2.

---

## 2. Solo brand / creator

**Inference signals:**
- B1: audience-funded — course sales, newsletter, sponsorships, coaching an audience.
- A3: "content creation" dominates the day.
- B3: customers are lots of individuals (subscribers, students), not named B2B clients.
- B4: usually solo or a tiny team. This is Remy's own shape (`ai-with-remy/`).

**Reference tree (business folders):**
```
[brand]/
├── content/
│   ├── newsletter/   ← issues, drafts, research briefs
│   ├── social/       ← posts, reels, scripts, hooks
│   ├── youtube/      ← titles, thumbnails, descriptions, scripts
│   └── ideas/        ← the content backlog / swipe file
├── offers/           ← courses, products, lead magnets, sales pages
├── audience/         ← ICP notes, subscriber data, community, testimonials
├── finance/          ← revenue, sponsorships, subscriptions, expenses
└── partnerships/     ← sponsors, collabs, affiliate deals
```

---

## 3. Product / e-com

**Inference signals:**
- B1: customers buy a product (physical or digital/SaaS), usually one-off or subscription purchases.
- B3: many individual customers, not named clients.
- A3: mix of marketing, product, and ops; not "client work".
- B2: SKUs / product lines / tiers rather than services.

**Reference tree (business folders):**
```
[brand-name]/
├── marketing/        ← ads, content, email, social, launches, creative
├── sales/            ← channels, promotions, conversion, wholesale/retail
├── product/          ← catalog, roadmap, suppliers, specs, packaging
├── operations/       ← fulfillment, inventory, shipping, vendors
├── finance/          ← revenue, COGS, margins, expenses
└── customers/        ← support, reviews, feedback, ICP, returns
```
For SaaS/digital, `product/` leans toward roadmap, features, and docs; `operations/` leans toward infrastructure and support workflows — adapt the subfolders to physical vs digital.

---

## 4. Local / service business

**Inference signals:**
- B1: paid per job for a location-bound service (trades, clinic, restaurant, salon).
- B3: local customers, often found via Google/referral, usually 40+ homeowners or local residents.
- B5: priorities like reviews, local ranking, more bookings.
- B4: often has a small on-site team.

**Reference tree (business folders):**
```
[business-name]/
├── marketing/        ← local SEO, Google Business, reviews, ads, referrals
├── sales/            ← quotes, enquiries, bookings, follow-ups
├── jobs/             ← job records, schedules, materials, per-job notes
├── finance/          ← invoices, payments, expenses, pricing
├── operations/       ← suppliers, equipment, compliance, licensing
└── team/             ← staff, rosters, training, onboarding
```
Drop `team/` if it's a solo operator. Rename `jobs/` to fit the trade — `bookings/` for a clinic/salon, `orders/` for a restaurant.

---

## 5. Coaching / consulting

**Inference signals:**
- B1: sells expertise as a package — 1:1 or group, usually time-boxed (a 12-week program, weekly calls).
- B2: packages/programs with a clear price, not products or per-deliverable agency work.
- A4: expertise IS the product.
- C2: may name individual clients (like an agency) but the deliverable is coaching, not production work.

**Reference tree (business folders):**
```
[practice]/
├── offers/           ← programs, packages, pricing, curriculum, frameworks
├── content/          ← lead-gen content: posts, talks, lead magnets, webinars
├── sales/            ← enquiries, discovery calls, proposals, follow-ups
└── finance/          ← invoices, revenue, expenses
clients/
└── [each-client]/
    ├── sessions/     ← call notes, recordings, session plans, homework
    ├── deliverables/ ← workbooks, plans, resources handed over
    └── progress/     ← goals, tracking, wins, check-ins
```
Repeat `[each-client]/` per named client. For a purely group/cohort model with no named 1:1 clients, swap `clients/` for a single `programs/[cohort-name]/` folder.

---

## 6. Employee / intrapreneur

**Inference signals:**
- B1: "I don't own the business — I get a salary." Doesn't sell anything directly.
- B3: customers are internal stakeholders (their team, their boss, other departments).
- B5: priorities framed around their role, proving ROI, or levelling themselves up.
- Building AI skills to future-proof their own work, not to run a business.

**Reference tree (business folders):**
```
my-role/              ← responsibilities, goals, OKRs, reporting lines, wins log
projects/             ← current work initiatives, one subfolder per project
team/                 ← colleagues, stakeholders, meeting notes, collaboration
career/               ← growth plan, reviews, skills, learning, portfolio
```
If their role is heavily one function (e.g. a marketing manager), you can specialise `projects/` into function-shaped subfolders (`campaigns/`, `content/`, `reporting/`) — but keep the four-folder spine so it stays about THEM, not a business they don't own.

---

## HYBRID HANDLING

**This is common — expect it.** Many students point to two archetypes at once (signal: C3 names two brands/businesses, or a clear "my company AND my personal brand" / "my business AND a side thing"). The rule:

> **When signals point to two archetypes, place BOTH business-folder trees at the OS root as siblings. Don't force one. Don't merge them into a Frankenstein tree.** Each brand keeps its own clean tree, exactly like Remy's own OS keeps his two brands side by side, each with its own folder tree.

Separate business from personal, and separate distinct brands, into distinct roots. Shared things (like personal finance) get their own top-level folder rather than being buried inside one brand.

### Worked example: agency owner also building a personal brand

**Their answers:** runs a content agency with three clients (agency signals — archetype 1); ALSO building a personal brand on LinkedIn with a newsletter and a course in the works (solo-brand/creator signals — archetype 2). C3 explicitly names both.

**The blended tree** (business folders only — the spine and `context/` sit above, once):

```
Desktop/OS/
├── .agents/          ← canonical custom skills (universal)
├── .claude/          ← linked skills, progress, settings, chimes (universal)
├── AGENTS.md         ← canonical cross-harness instructions (universal)
├── MEMORY.md         ← approval-gated memory (universal)
├── context/          ← spine (universal)
│
├── [agency-name]/            ← TREE 1: client services / agency (archetype 1)
│   ├── content/              ← the agency's own marketing
│   ├── sales/
│   ├── finance/
│   ├── operations/
│   └── legal/
├── clients/                  ← belongs to the agency tree
│   ├── acme/
│   │   ├── deliverables/
│   │   ├── comms/
│   │   ├── assets/
│   │   └── strategy/
│   ├── bigco/
│   │   └── … (same block)
│   └── n-space/
│       └── … (same block)
│
├── [personal-brand]/         ← TREE 2: solo brand / creator (archetype 2)
│   ├── content/
│   │   ├── newsletter/
│   │   ├── social/           ← LinkedIn posts, hooks
│   │   └── ideas/
│   ├── offers/               ← the course in the works
│   ├── audience/
│   └── finance/
│
└── personal/                 ← optional: personal/life admin kept out of both businesses
```

**How to present it:** propose both trees together as one recommended workspace, using their real names ("here's your agency side, and here's your personal-brand side — two clean areas, like separate rooms in the same house"), and let them react. Don't ask them to choose one archetype — show the blend and adjust.

**Other common hybrids, same rule:**
- Clinic + a separate online course → local-service tree + solo-creator tree, side by side.
- Consulting business + a property side-thing → coaching/consulting tree + a simple `property/` (or `investments/`) folder, business kept separate from the side venture.
- Two e-com brands under one company → two product/e-com trees as siblings (or one tree with a `brands/[each]/` split if they're run as one operation — ask which).

---

## Final note

These trees are **starting points, not cages.** Blend them freely, pre-fill every folder with the student's REAL names and REAL clients, and drop anything that doesn't fit their actual business. A confident recommendation they can react to beats a blank slate — but the tree they confirm is always bespoke to them. The student is never boxed in, and never sees the word "archetype".
