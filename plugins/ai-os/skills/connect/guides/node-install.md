# Node — the quiet prerequisite install

Shared recipe for the baked guides that run a local program (Chrome DevTools,
Playwriter, Kie.ai — and any future local server). Internal reference for the
running agent — never read this file to a student.

**The posture: install it, don't make a big deal of it.** Node is a free,
standard helper program. If it's missing, ONE line of narration and get on
with it — no lecture, no options menu, no "are you sure":

> "Your computer needs one small free helper program (called Node) for this
> one — installing it now, takes about a minute."

## 1. Check first (silently)

Run `node --version` (Windows: same in PowerShell). **v20 or newer → done.**
Say nothing about it and carry on with the guide. Older or missing → install
below for the student's OS.

## 2. macOS / Linux — official build into their home folder

No admin password, no Homebrew assumed (works fine alongside Homebrew too).

1. **Arch:** `uname -m` → `arm64` stays `arm64`; `x86_64` maps to `x64`.
   (Linux: platform is `linux-<arch>` instead of `darwin-<arch>`.)
2. **Latest LTS:** fetch `https://nodejs.org/dist/index.json` and take the
   FIRST entry whose `lts` field is not `false` — its `version` looks like
   `v22.17.0`. Never hardcode a version; this file is the source of truth.
3. **Download + unpack + link:**

   ```bash
   mkdir -p ~/.local/bin
   curl -fsSL "https://nodejs.org/dist/<ver>/node-<ver>-darwin-<arch>.tar.gz" -o /tmp/node.tgz
   tar -xzf /tmp/node.tgz -C ~/.local
   ln -sf ~/.local/node-<ver>-darwin-<arch>/bin/node ~/.local/bin/node
   ln -sf ~/.local/node-<ver>-darwin-<arch>/bin/npm  ~/.local/bin/npm
   ln -sf ~/.local/node-<ver>-darwin-<arch>/bin/npx  ~/.local/bin/npx
   rm /tmp/node.tgz
   ```

4. **PATH:** append `export PATH="$HOME/.local/bin:$PATH"` to `~/.zshrc` AND
   `~/.zprofile` if that line isn't already in them.
5. **Verify:** `~/.local/bin/node --version` prints the version → done.
6. **Global npm installs later:** with this home-folder setup, anything a
   guide installs via `npm i -g <package>` lands in the node folder's own
   `bin` — not `~/.local/bin` — so link each new binary the same way:
   `ln -sf ~/.local/node-<ver>-<platform>/bin/<binary> ~/.local/bin/`.
   (Homebrew/system Node users skip this — their global bin is already on
   PATH.)

## 3. Windows — winget (ships with Windows 10/11)

```powershell
winget install --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
```

New processes pick up the PATH — so after the guide finishes, the student
closes and reopens Claude Code / the terminal once (the guides already end
with a restart, so fold it into that one). Find the absolute path with
`where npx` (typically `C:\Program Files\nodejs\npx.cmd`).

## 4. The absolute-path rule (always, both platforms)

When registering the local server, use the ABSOLUTE npx path from
`command -v npx` (Windows: `where npx`) — never bare `npx` — so the
connection works no matter how the student launches the host:

```bash
# macOS example
claude mcp add --scope user <name> -- /Users/<them>/.local/bin/npx -y <package>
# Windows native shells wrap it:
claude mcp add --scope user <name> -- cmd /c npx -y <package>
```

## 5. If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Server errors `env: node: No such file` | The spawned program can't find node on its PATH | Re-register the server adding `--env PATH="$HOME/.local/bin:$PATH"` (use the expanded real path) |
| `npx` works in terminal but the host can't spawn it | Host launched from the Dock before PATH updated | Fully quit and reopen the host; if it persists, the absolute-path rule above fixes it |
| Corporate/locked-down Windows blocks winget | Policy restriction | Fall back to the official Node installer from nodejs.org — the one case where the website download is the honest answer; say so plainly |
