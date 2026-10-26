# Baked guide — Chrome DevTools

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student. (Students say
"chrome dev tools", "devtools", "chrome browser" — same tool.)

**What to say it is:** "A fresh browser your OS can drive — logged into
nothing. For checking your website the way a stranger sees it, testing a
signup flow, filling a public form."

## Route

**No aggregator check needed — this is a local program** (it runs on their
computer, not in the cloud). Two prerequisites, handled quietly:

1. **Chrome installed?** Mac: does `/Applications/Google Chrome.app` exist;
   Windows: is Chrome in the registry/Program Files. Missing → they install
   Chrome first (google.com/chrome), then come back. Most already have it.
2. **Node** — run `guides/node-install.md` (check silently; install with one
   line of narration if missing).

Then register it with the ABSOLUTE npx path (node-install §4):

```bash
# Claude Code (macOS)
claude mcp add --scope user chrome-devtools -- <absolute-npx> chrome-devtools-mcp@latest
# Claude Code (Windows)
claude mcp add --scope user chrome-devtools -- cmd /c npx chrome-devtools-mcp@latest
# Codex: same command shape via `codex mcp add chrome-devtools -- <absolute-npx> chrome-devtools-mcp@latest`
```

Restart the host so it loads.

## Prove it (read-only)

"I'll open your homepage in the fresh browser and tell you the page title."
**A new Chrome window opening on its own is the feature, not a glitch** —
tell them before it happens: "a separate, clean Chrome is about to open —
that's the stranger's browser." Real title back = working.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| First use hangs for a minute | It downloads itself on first run | Normal — wait it out once |
| `env: node: No such file` | The spawned program can't find node | node-install §5 — re-register with the PATH env fix |
| Server not visible after adding | Loads at startup | Fully quit and reopen the host |
| It opens but pages won't load | A VPN/firewall blocking the fresh profile | Try one more page; note it and move on — not worth a session derail |

## The rule to teach alongside it

"Fresh browser unless it needs your login." This one is the FRESH browser.
Anything behind a password is Playwriter's job (`guides/playwriter.md`) —
one line, so they know which door is which.

## Record

`## Tools` row per §6. How connected = "Local program (chrome-devtools-mcp)"
— the runs-on-this-computer kind.
