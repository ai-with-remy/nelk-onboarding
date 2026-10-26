# Baked guide — Playwriter

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student. (Students say
"play writer", "playwrite" — same tool.)

**What to say it is:** "Your actual browser, actually logged in. For
anything behind a password — your LinkedIn, a dashboard with no export
button, the tools you're signed into. Chrome DevTools is the stranger's
browser; this is YOURS."

**Say the trust line up front:** because it acts in their real logged-in
browser, this is exactly where the progressive-trust habit applies — the
host asks before actions, and they approve one at a time.

## Route

**No aggregator check needed — this is a local program plus a Chrome
extension.** Chrome only (not Safari). Three steps:

1. **The extension (the one manual step).** Give them the link in chat:

   > Install this Chrome extension, then pin it to your toolbar:
   > https://chromewebstore.google.com/detail/playwriter/jfeammnjpkecdekppnclgkkffahnhfhe

   Wait for "done". (Pinning matters — the icon is how they SEE what's
   connected: green = a tab under control.)

2. **Node** — run `guides/node-install.md` (silent check, quiet install).

3. **Install the CLI** (absolute npm path per node-install §4):

   ```bash
   npm i -g playwriter
   ```

   If Node came from our quiet home-folder install, link the new binary
   too (node-install §2 step 6). Quick check: `playwriter --help` prints
   usage.

4. **Register the MCP** with the ABSOLUTE npx path (node-install §4):

   ```bash
   # Claude Code (macOS)
   claude mcp add --scope user playwriter -- <absolute-npx> -y playwriter@latest
   # Claude Code (Windows)
   claude mcp add --scope user playwriter -- cmd /c npx -y playwriter@latest
   # Codex: same shape via `codex mcp add playwriter -- <absolute-npx> -y playwriter@latest`
   ```

   Restart the host so it loads.

   (Source project: `remorses/playwriter`. We deliberately install BOTH
   doors: the MCP for tool access, and the CLI so the agent can also
   drive the browser straight from the terminal —
   `playwriter -e "<playwright code>"` — which is lighter on context, the
   same lesson as every other CLI. The README's extra `npx skills add`
   step is the author's skill route — not needed here.)

## Prove it (read-only)

With Chrome open: "Tell me the title of the tab I've got open right now."
Their real tab's title back = working. It connects to tabs automatically by
default; if a specific tab won't respond, clicking the Playwriter icon on
that tab (it turns green) wakes it up.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Tools time out / "no connection" | The extension isn't installed, or Chrome isn't running | Check the extension is in Chrome and Chrome is open |
| One tab won't respond | That tab isn't paired | Click the Playwriter icon on it — green means connected |
| `env: node: No such file` | Spawned program can't find node | node-install §5 — the PATH env fix |
| They use Safari/Firefox as their main browser | Playwriter is Chrome-only | Honest line: their logged-in work needs to happen in Chrome for this to help |

## Record

`## Tools` row per §6. How connected = "Local program
(remorses/playwriter: MCP + CLI + Chrome extension)" — the
runs-on-this-computer kind. Caveat column: acts in the student's real
logged-in browser, actions gated by approval; the CLI also works from the
terminal (`playwriter -e "<playwright code>"`).
