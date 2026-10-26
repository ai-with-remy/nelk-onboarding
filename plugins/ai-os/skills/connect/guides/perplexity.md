# Baked guide — Perplexity

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student.

**What to say it is:** "Perplexity is better search. Your OS can already
search the web — Perplexity is the upgrade it calls when answer quality
matters: research with real sources, not just links."

**One honest line up front:** Perplexity's connection uses their API, which
is pay-as-you-go — a small credit top-up on their site (a few dollars goes a
long way). Say this BEFORE they create anything, not after.

## Route

Run the aggregator check (§3a). **Perplexity IS covered by Composio — and
Composio is genuinely the easy path here** (the direct route means running a
local program). Recommend it plainly.

**Composio path (aggregator = Composio):**
1. "You can add this through Composio to make things easier — head to your
   Composio dashboard and log in to Perplexity there." Offer to kick off the
   sign-in from here (`COMPOSIO_MANAGE_CONNECTIONS` → browser link).
2. The connection takes an API key, entered on **Composio's own page — never
   in chat**: account at perplexity.ai → Settings → API → buy a small credit
   pack → create a key.
3. When they say it's connected, verify below.

**Direct path (no aggregator):** there is no official hosted server —
Perplexity's own connector is a local program. Treat it as the local-server
path (`mcp-safety.md` §4): Node via `guides/node-install.md` (quietly),
verify the CURRENT package name from Perplexity's own official docs/repo
before using it (last known: `server-perplexity-ask` — confirm, don't
recite), and the key goes in via the student's OWN terminal with the
placeholder pattern:

```bash
claude mcp add --scope user perplexity --env PERPLEXITY_API_KEY=PASTE_KEY_HERE -- <absolute-npx> -y server-perplexity-ask
```

They paste that in their own terminal window and replace the placeholder —
the key never enters this chat.

## Prove it (read-only)

One real question through it: "Ask Perplexity what the latest Claude model
is." A sourced answer back = working.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| 401 / unauthorized | Key is wrong, or the account has no API credits | Check the credit balance on perplexity.ai first — an unfunded key looks identical to a broken one |
| Composio live but no Perplexity tools | App not connected inside Composio yet | Back to the dashboard — hub ≠ app |
| Answers come back but slowly | Research-grade queries take longer | Normal — that's the depth they're paying for |

## Record

`## Tools` row per §6. How connected = "Composio" or
"Local program (Perplexity's official connector)".
