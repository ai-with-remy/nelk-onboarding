# Baked guide — OpenRouter

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student.

**What to say it is:** "Claude has one brain. OpenRouter lets your OS ask
OTHER models — GPT, Gemini, whichever fits — when a second opinion or a
different strength helps. One account, every model behind one door."

## Route

**No aggregator check needed — this one has an official hosted server** (no
Composio toolkit exists, and none is wanted: OpenRouter IS its own hub).
Offer BOTH doors per `known-routes.md` "Two doors": the app door first for
Claude students (claude.ai → Settings → Connectors → Add custom connector,
name `OpenRouter MCP`, URL `https://mcp.openrouter.ai/mcp` — works
everywhere including Claude Code; hand them the pre-filled link), or the
machine door:

```bash
# Claude Code
claude mcp add --scope user --transport http openrouter https://mcp.openrouter.ai/mcp
claude mcp login openrouter
# Codex
codex mcp add openrouter --url https://mcp.openrouter.ai/mcp
codex mcp login openrouter
```

(`/mcp` → authenticate works too.) They need an OpenRouter account
(openrouter.ai) with a small credit top-up — calling other models is
pay-as-you-go.

**The approval screen is a feature — say so:** the sign-in creates a scoped
key with a **default $10 spend cap** the student approves. Frame it warmly:
"you're not handing it your wallet — you're approving a $10 ceiling, and you
can change that number yourself."

## Prove it (read-only, spends nothing)

Catalog reads are free: "Show me a few of the trending models this week."
A real model list back = working. **Actually sending a prompt to another
model (or generating an image) bills their OpenRouter credits** — one plain
line before the first real use.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Worked last week, dead today | **The sign-in expires every 7 days — this is normal, not broken** | `/mcp` → authenticate again (or `claude mcp login openrouter`); 20 seconds |
| A model call fails with a payment error | No credits, or the $10 cap was hit | Top up / raise the cap at openrouter.ai — a deliberate choice, which is the point |
| Server not visible after adding | Loads at startup | Restart the host |

## Record

`## Tools` row per §6. How connected =
"Official MCP (mcp.openrouter.ai/mcp)". Note the 7-day re-sign-in in the
caveats column so a future session doesn't misdiagnose it.
