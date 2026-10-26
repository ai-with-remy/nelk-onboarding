# Baked guide — Kie.ai

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student. (Students say
"kie", "kie.ai", "kie ai" — same tool.)

**What to say it is:** "The budget door to the big image and video models —
the same kinds of generations as Higgsfield, priced pay-as-you-go and
usually cheaper per image. Worth it when volume matters more than polish."

## Route

**No aggregator check needed — Composio has no Kie.ai toolkit.** No hosted
server either: this is a local program (a community-built one) plus an API
key. Steps:

1. **Node** — run `guides/node-install.md` (silent check, quiet install).
2. **The key.** They create an account at kie.ai and mint a key at
   kie.ai/api-key (free to create; generations draw on pay-as-you-go
   credits they top up).
3. **Register it — key via THEIR terminal, never this chat**
   (`mcp-safety.md` §4.3 placeholder pattern). Prepare this with the real
   absolute npx path and have them paste it into their own terminal window,
   swapping in the key:

   ```bash
   # Claude Code (macOS)
   claude mcp add --scope user kie-ai --env KIE_AI_API_KEY=PASTE_KEY_HERE -- <absolute-npx> -y @felores/kie-ai-mcp-server
   # Claude Code (Windows)
   claude mcp add --scope user kie-ai --env KIE_AI_API_KEY=PASTE_KEY_HERE -- cmd /c npx -y @felores/kie-ai-mcp-server
   ```

   One line after: "the key now lives in your Claude settings on this
   computer — not in your files, not in our chat."
4. Restart the host so it loads.
5. **Trust review is mandatory** — this is a community server, not a vendor
   one (`mcp-safety.md` §3): list its tools, plain-English capability
   review, their yes before first use.

## Prove it (spends nothing)

Prefer a free read: list the models/tools it exposes, or check credits if a
credit tool exists. If the server exposes no safe free read, use the
degraded verification tier (`quick-connect.md` §6): tools loaded + trust
review accepted, recorded as "connected — limited check". **Every actual
generation spends their kie.ai credits** — one plain line before the first.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| 401 / unauthorized | Wrong key, or no credits on the account | Check the balance at kie.ai first — an unfunded key looks broken |
| `env: node: No such file` | Spawned program can't find node | node-install §5 — the PATH env fix |
| Server not visible after adding | Loads at startup | Fully quit and reopen the host |

## Record

`## Tools` row per §6. How connected = "Local program
(felores/kie-ai-mcp-server, community)" — the runs-on-this-computer kind.
