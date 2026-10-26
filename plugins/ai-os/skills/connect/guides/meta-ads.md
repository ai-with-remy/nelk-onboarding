# Baked guide — Meta Ads (Facebook / Instagram ads)

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student. (Students say
"meta", "facebook ads", "fb ads", "instagram ads" — same connection.)

**What to say it is:** "Your ad account, connected. Your OS can pull
campaign performance, compare ad sets, spot what's burning money — and,
once you trust it, make changes — through Meta's own official connection."

## Route

**No aggregator check needed — Meta runs its own official hosted server**
(launched April 2026): `https://mcp.facebook.com/ads`. Browser sign-in with
their normal Meta Business login — no developer app, no API key, ever.
Two doors (`known-routes.md` "Two doors"), and here the app door is ALSO
Meta's own documented path for Claude:

- **App door (first choice):** claude.ai → Settings → Connectors → Add
  custom connector — name `Meta Ads`, URL `https://mcp.facebook.com/ads`.
  Hand them the pre-filled link (template in known-routes).
- **Machine door:**

  ```bash
  # Claude Code
  claude mcp add --scope user --transport http meta-ads https://mcp.facebook.com/ads
  # Codex
  codex mcp add meta-ads --url https://mcp.facebook.com/ads
  ```

**The sign-in has a teaching moment in it — use it.** Meta's window asks
WHICH ad accounts and pages to grant, including an "all current and future"
option. Recommend selecting specific accounts instead: "grant only the
account you want it touching — this is the progressive-trust idea built
into the sign-in itself." And name the off-switch while they're looking at
it: access is revocable any time in Meta Business Suite → Settings →
Business integrations — the control that works no matter what.

Prerequisite worth one line up front: they need a Meta account with access
to the ad account (Business Suite access), not just a personal profile.

## Prove it (read-only)

Reads only for the first session — no edits until they've watched it work:
"List the ad accounts you can see" or "Pull the last 7 days of performance
for [a campaign they name]." Real numbers they recognise = working.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Connection fails outright | Meta rolled this out gradually — their ad account may not be enrolled yet | Note it, re-check in a few weeks; not their fault, nothing to debug |
| Sign-in loops or shows no accounts | Logged in with a profile that lacks business access | Redo the sign-in with the account that manages the ads |
| Connected but tools see nothing | The wrong ad account was granted | Reconnect and reselect accounts in Meta's window |
| A third-party "Meta ads MCP" URL with a token in it | A community bridge, key-in-URL | Hard-skip — the official server exists and needs no key (secrets rule) |

## Record

`## Tools` row per §6. How connected =
"Official MCP (mcp.facebook.com/ads)". Caveat column: can ACT on ad
spend once write actions are approved — reads first, per the session's
progressive-trust rule.
