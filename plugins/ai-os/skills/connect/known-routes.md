# Known Routes — the routing facts behind /ai-os:connect

Internal reference for the running agent — never read this file to a student.
This is the ONE source of truth for "which door does app X go through." Both the
The Tools module flow and Quick Connect read it. Always trust the active host's live
inventory and a live probe over anything remembered — endpoints rot.

---

## Pinned routes (these override the discovery ladder)

For these categories, skip the generic hunt — the route is already decided:

| Tool / category | Claude Code route | Codex route |
|---|---|---|
| **The core stack: Firecrawl, Apify, Perplexity, Higgsfield, OpenRouter, Chrome DevTools, Playwriter, Kie.ai, Meta Ads — plus the hubs themselves, Composio and Zapier** | **Baked guide: `guides/<tool>.md` — overrides every other route, including the rows below** (`quick-connect.md` §3 Step 0a / §3a) | Same guides, Codex variants inside |
| Gmail, Google Calendar, Microsoft 365 / Outlook | claude.ai → Settings → Connectors (browser sign-in), when live inspection confirms them | Connector plugin via `/plugins` / Settings → Plugins |
| Notion, HubSpot, Stripe, Slack, Sheets, Cal.com, most CRMs, Granola, Apify, Firecrawl | Composio gateway (see below) | Composio gateway (see below) |
| Higgsfield (AI image/video) | Direct: `https://mcp.higgsfield.ai/mcp` — no Composio toolkit exists | Same, via `codex mcp add` |
| **Anything referencing rube.app** | **NEVER.** Composio's old "Rube" connector was shut down. Hard-ignore rube.app URLs everywhere, including in web-search results. | Same |

## Two doors for HOSTED servers: app-level vs machine-level

Machine-level (`claude mcp add --scope user ...`) lives in the student's
config on THIS computer and reaches Claude Code only. **App-level lives in
their Claude ACCOUNT** (claude.ai → Settings → Connectors) and flows one way
into everything — web, desktop, mobile, AND Claude Code — provided they're
signed into Claude Code with their Claude account (API-key users don't
receive connectors).

- **Hosted server + Claude student → offer the app door FIRST:** "connect it
  in the app and it works everywhere, including here." Machine door as the
  fallback or on preference.
- **Local programs (npx/stdio) can NEVER be app-level** — claude.ai cannot
  run programs on their computer. Machine door only.
- **Codex has no app door** — always `codex mcp add`.
- There is NO command or file that creates an app-level connector from this
  session — it lives server-side in their account, so the student clicks it
  in. The assist is the pre-filled link (opened in a BROWSER; undocumented,
  may break — if the form arrives empty they add it manually with the same
  name + URL):
  `https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=<Name>&connectorUrl=<url-encoded-endpoint>`
- Free Claude plans allow ONE custom connector (Pro and up: unlimited). A
  student on the free plan should spend that slot on their AGGREGATOR, not a
  single app — say so if it comes up; the machine door protects the slot.
- Apps already in the connector DIRECTORY (Gmail, Google Calendar, …) don't
  need the custom form — the directory tile is the app door.

## The Composio gateway (the aggregator route — and the DEFAULT door)

**Composio-first is the rule:** whenever the student's Composio gateway is
already in the live inventory, it is ALWAYS the first route offered for a new
app — check its coverage (below) BEFORE hunting for vendor or community
servers. One hub means one place to manage, re-check, and revoke every
connection, and no new server to add or trust-review per app. Official vendor
MCPs are the route when Composio is out of play, not the default.

Composio is a one-stop connection hub covering 1,400+ apps. It is NOT
pre-installed — it gets added once, into the student's OWN config (user scope,
so it survives plugin updates, disables, and removal), and each student signs
into their OWN free Composio account. No shared credentials.

```bash
# Claude Code
claude mcp add --scope user --transport http composio https://connect.composio.dev/mcp
# Codex
codex mcp add composio --url https://connect.composio.dev/mcp
```

Then the one-time browser sign-in (Claude: `/mcp`; Codex: the live auth
prompt; a restart / new session may be needed before it shows up). Individual
apps then connect through Composio's live tools, each with its own browser
sign-in. Apps whose Composio connection takes an API key (e.g. Apify,
Firecrawl) enter that key on **Composio's own connection page — never in
chat**, which keeps the secrets rule intact.

**Respect a "no Composio" preference.** Some students won't want a third-party
hub in the middle of their connections — that's a legitimate security posture,
not a mistake. Say so respectfully, skip the Composio rung without friction,
and lean on official/direct routes instead.

### Checking whether an app is on Composio (agent-readable — do this, never guess)

- **Gateway installed (the normal case):** call the Composio server's own
  `COMPOSIO_SEARCH_TOOLS` tool with the app's name and the student's use case.
  The response answers everything in one shot: whether a toolkit for the app
  exists (a "toolkit" is Composio's word for one app's connection), whether
  the student already has an ACTIVE connection to it, and the pointer to
  `COMPOSIO_MANAGE_CONNECTIONS` to start the browser sign-in. Verified live:
  searching "Cal.com" returns the `cal` toolkit with its connection status.
- **Gateway not installed yet:** fetch the public catalogue with the host's
  web capability — `https://composio.dev/toolkits` is the browsable directory,
  and `https://composio.dev/toolkits/<app-slug>` is a single app's page. If
  the app is there, offer to add the gateway and connect through it.

## Official vendor MCPs (the direct route — for when Composio is out of play)

Use these when the Composio gateway isn't installed and the student doesn't
want it, when Composio has no toolkit for the app, or when the student
explicitly prefers the vendor's own door. Many vendors host their own official
MCP endpoint — the vendor's own front door, usually rich and current.
Known-good direct endpoints (probe before use — see `mcp-safety.md`):

| Vendor | Endpoint | Notes |
|---|---|---|
| Notion | `https://mcp.notion.com/mcp` | browser OAuth |
| HubSpot | `https://mcp.hubspot.com/anthropic` | browser OAuth |
| Stripe | `https://mcp.stripe.com` | browser OAuth |
| Apify | `https://mcp.apify.com` | browser OAuth; free plan credits |
| Firecrawl | `https://mcp.firecrawl.dev/v2/mcp` | keyless rate-limited free tier; OAuth unlocks full tools. AVOID the legacy `mcp.firecrawl.dev/<API_KEY>/...` key-in-URL form |
| Higgsfield | `https://mcp.higgsfield.ai/mcp` | browser OAuth |
| OpenRouter | `https://mcp.openrouter.ai/mcp` | browser OAuth (`claude mcp login openrouter`); sign-in re-expires EVERY 7 DAYS (normal, not broken); default $10 spend cap approved at sign-in; model calls bill the student's OpenRouter credits |
| Meta Ads | `https://mcp.facebook.com/ads` | Meta's official server (Apr 2026); business OAuth, per-ad-account grant at sign-in; gradual rollout — a failed connect may mean not enrolled yet; revoke at Business Suite → Business integrations |

Vendors known to ship an official MCP whose endpoint you should hunt from
their own docs (don't recite from memory): Arcads, Beehiiv, and a fast-growing
list — always web-search "<vendor> MCP" and confirm the endpoint on the
vendor's own domain or official docs before recommending it.

## Add commands (direct route, per host)

```bash
# Claude Code
claude mcp add --scope user --transport http <name> <url>   # then /mcp for the browser sign-in
# Codex
codex mcp add <name> --url <url>                            # then the live auth prompt; new session if not visible
```

Always `--scope user` on Claude so the connection belongs to the student and
survives any plugin change. If a newly added server isn't visible yet, save
progress and have them restart the host — it appears on the next start.
