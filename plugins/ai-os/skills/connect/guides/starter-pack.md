# Baked guide — the Starter Pack (the whole recommended stack, one run)

Internal recipe for the running agent. Never read this file to a student.
Triggered by: "starter pack", "core stack", "recommended stack", "connect
everything", "set me up with the stack".

**What to say it is:** "The course's recommended stack, connected one at a
time — a safe read-only test after each, you can stop whenever you like,
and picking up later is the same command."

## 0. Ground rules

- This is a SEQUENCE of the individual baked guides — not a batch. One tool
  at a time, proof test after each, recorded after each. The no-batching
  rule holds; the pack just removes the "what next?" friction between tools.
- **Duplicate check first** (`quick-connect.md` §1): read the live inventory
  and the `## Tools` section. Anything already connected is announced and
  skipped — "you've already got Firecrawl, skipping it." A re-run of the
  starter pack therefore RESUMES it for free; no extra state needed.
- The **aggregator question is asked ONCE** at the start (per §3a) and the
  answer drives the whole run — never re-ask it between tools.
- Say the escape hatch up front: "say stop anytime — everything connected
  so far stays connected, and `/ai-os:connect starter pack` picks up where we
  left off."

## 1. The menu (ONE question)

Show the pack with its one-liners, then ask one question — all-in or pick:

**Core (recommended for everyone):**
1. **Composio** — the easy button: hundreds of apps, one connection
2. **Firecrawl** — actually read a page, not just search it
3. **Apify** — scrape anything on the internet
4. **Perplexity** — better search: research-grade answers *(needs a small
   paid credit on their site)*
5. **Higgsfield** — images and video
6. **OpenRouter** — let Claude ask other models *(needs a small paid
   credit)*
7. **Chrome DevTools** — a fresh browser, logged into nothing
8. **Playwriter** — your real browser, all your logins

**Optional (offer at the end, don't push):**
9. **Kie.ai** — same image/video models, the budget door
10. **Meta Ads** — your ad account through Meta's own connection (only
    worth it if they run ads)

> "Want the whole core eight, or shall we pick? There are two optional
> extras I'll ask about at the end."

## 2. The order (and why — don't reshuffle without a reason)

composio → firecrawl → apify → perplexity → higgsfield → openrouter →
chrome-devtools → playwriter → *(optional: kie-ai, meta-ads)*

- **Hub first:** it makes the next three nearly one-click.
- **Hosted before local:** easy momentum before the first on-your-computer
  install.
- **Node installs once** at Chrome DevTools and pays off again at
  Playwriter (and Kie.ai).
- If they said **no hub**, the order holds — firecrawl/apify/perplexity
  just take their direct paths from their own guides.

## 3. Running each tool

Open that tool's OWN guide and follow it exactly — the aggregator answer is
already in hand. Between tools, one line of momentum, not a question:

> "That's 3 of 8. Next: Higgsfield — the image studio. Here we go."

Ask an actual question only at the friction gates, BEFORE the tool's turn:
- The two paid-credit tools: "the next one needs about $5 loaded on their
  site — do it now, or skip and add it later?"
- The first local install: "the next two run on your computer rather than
  in the cloud — takes a couple of minutes, one small helper install. Good
  to go?"

## 4. If one fails

Its guide's own troubleshooting, ONE quick try. Still stuck → record
"attempted, not yet working" per that guide and MOVE ON — the pack never
stalls on one tool. Flag it at the recap: "X didn't finish — run
`/ai-os:connect X` later and we'll fix it fresh."

## 5. The recap (always, even on an early stop)

The `## Tools` rows were previewed and written per tool as you went. Close
with a plain scoreboard in chat: connected ✅ / skipped by choice / attempted
⚠️ — then the one-liner that makes the whole system click: "and any app you
ever want to add later is just `/ai-os:connect <name>`."
