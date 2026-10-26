# Baked guide — Zapier (the other aggregator)

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student.

**What to say it is:** "Zapier's version of the one-hub idea — log into your
apps at Zapier once, give your OS one connection. Same shape as Composio,
different company, and you pick which actions it's allowed to use."

**One honest line BEFORE they invest setup time:** Zapier's free tier is
tight for this — the monthly task allowance is shared with their automations
and covers roughly a few dozen AI tool calls. Fine for a look around; thin
for daily work. Their call, said plainly, no pressure either way.

## Route

This sets up the HUB. Individual apps get enabled inside it afterwards.

1. **Their Zapier MCP settings first:** they log into Zapier and set up
   Zapier MCP from zapier.com/mcp — that page generates their personal
   server and is where they choose WHICH apps and actions the OS may use.
   Teach the allowlist as the feature it is: "turn on only the few actions
   you actually want — everything else stays off."
2. **Two doors** (`known-routes.md` "Two doors"): app door — claude.ai →
   Settings → Connectors (the directory tile if Zapier appears there, else
   Add custom connector with the URL from step 1). Machine door —
   `claude mcp add --scope user --transport http zapier <their URL>`
   (Codex: `codex mcp add zapier --url <their URL>`).
3. **Secrets check (mcp-safety §1):** if the URL Zapier hands them embeds a
   long token, that URL IS a key. Fine to paste into the connector form or
   the add command; never into notes, files, or read back in chat. Prefer
   the OAuth option whenever Zapier's setup page offers one.
4. Record the aggregator answer per §3a:
   `**Aggregator:** Zapier — confirmed <date>`.

## Prove it (read-only)

One read through an action they enabled: "list my 3 most recent [whatever
the first enabled app holds]." A real result = hub live and the allowlist
works.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| A tool they expect is missing | That action isn't enabled in their Zapier MCP settings | Back to zapier.com/mcp — flip it on there |
| Calls fail mid-month | The shared task allowance ran out | Wait for the reset or upgrade — their call, flagged honestly up front |
| The URL stopped working | They regenerated their server URL at Zapier | Reconnect with the new URL; the old one is dead on purpose |

## Record

`## Tools` row per §6 for the hub, plus the `**Aggregator:**` line.
