# Host and Platform Detection Contract

Every skill in the ai-os plugin that touches the filesystem must follow this
contract. First resolve `PLUGIN_ROOT` and `HOST_RUNTIME` from
`<PLUGIN_ROOT>/shared/runtime.md`, then run the operating-system detection
below, then resolve the workspace shape from
`<PLUGIN_ROOT>/shared/workspace-layout.md`. Host, operating system, and
workspace layout are separate values.

---

## Step 1 — Detect the Host, Then the Platform

Store `HOST_RUNTIME` from `runtime.md`, then run the appropriate platform detection. Never infer the host merely from an installed executable, and never skip OS detection even if you think you know.

### macOS (zsh)

```zsh
uname -s
# Returns: Darwin
```

### Windows (PowerShell)

```powershell
$env:OS
# Returns: Windows_NT
```

If you're in a shell environment: check `uname -s` first. If that returns "Darwin" you're on macOS. If the command isn't found, you're on Windows — switch to PowerShell.

---

## Step 2 — Resolve the Home Directory

### macOS

```zsh
echo $HOME
# Example: /Users/sarah
```

### Windows (PowerShell)

```powershell
$env:USERPROFILE
# Example: C:\Users\Sarah Johnson
```

**Always quote paths that contain spaces.** Windows usernames with spaces (e.g. "Sarah Johnson") are common and will break any unquoted command.

---

## Step 3 — Resolve the REAL Desktop Default

This is the most important detection step. On Windows, the Desktop is often NOT where you'd expect it.

### macOS

The Desktop is always:
```
$HOME/Desktop
```

No trap here. Proceed.

### Windows — The OneDrive Desktop Trap

On many Windows machines, Microsoft OneDrive moves the Desktop to:
```
C:\Users\<name>\OneDrive\Desktop
```

Not:
```
C:\Users\<name>\Desktop
```

If you use the wrong path, the OS folder ends up in the wrong place — or the mkdir silently succeeds in the wrong location.

**The reliable fix: read the registry.** Windows stores the real Desktop path in the registry regardless of OneDrive:

```powershell
# The authoritative source — always use this
$desktop = (Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" -Name "Desktop").Desktop
Write-Output $desktop
# Example output: C:\Users\Sarah Johnson\OneDrive\Desktop
# OR:             C:\Users\Sarah Johnson\Desktop
```

If the registry key isn't readable for any reason, fall back to:

```powershell
# Fallback
$desktop = [Environment]::GetFolderPath("Desktop")
Write-Output $desktop
```

Both return the real, current Desktop path — whichever one Windows is actually using.

The Desktop path supplies the recommended default. It is not a requirement.
The `build-os` skill may use a different student-approved location under the
rules in Step 4.

**Tell the student where their OS folder ended up.** After the final root is
chosen, say one plain line like:

> "Your OS folder is at `C:\Users\Sarah Johnson\OneDrive\Desktop\OS` — bonus: OneDrive is already backing it up."

or:

> "Your OS folder is at `C:\Users\Sarah Johnson\Desktop\OS`."

No technical explanation needed. Just tell them where it is.

---

## Step 4 — Resolve the Actual OS Root

Store `DEFAULT_OS_ROOT=<DESKTOP>/OS`, then choose one of two modes.

### New build target

Only `build-os` may create a new workspace. It offers `DEFAULT_OS_ROOT` first
and may instead accept an exact student-approved custom folder named `OS`.
Resolve the custom path to an absolute path, confirm it back to the student,
and require its parent to exist. Do not inspect or write the target until the
student has approved the path and the build skill has passed its empty-target
gate.

### Existing workspace

Every later skill resolves in this order:

1. Use the active workspace root when it is a supported AI OS layout.
2. Cross-check `student.os_root` when the progress file exists there. If the
   stored path and active workspace disagree, stop before writes and ask the
   student to open the stored path.
3. If the active workspace is not an OS, check only `DEFAULT_OS_ROOT` as the
   legacy/default fallback.
4. If neither is a valid OS, tell the student to open the OS folder they chose
   during `build-os`. Do not broadly search their disk, Documents, cloud
   drives, or nearby folders.

After the final root is resolved, store `OS_ROOT` and derive the layout paths
through `workspace-layout.md`.

Use these canonical variable names throughout the skill so there's no ambiguity:

| Variable | macOS value | Windows value (example) |
|---|---|---|
| `DETECTED_OS` | `macos` | `windows` |
| `HOME_DIR` | `/Users/sarah` | `C:\Users\Sarah Johnson` |
| `DESKTOP` | `/Users/sarah/Desktop` | `C:\Users\Sarah Johnson\OneDrive\Desktop` |
| `DEFAULT_OS_ROOT` | `/Users/sarah/Desktop/OS` | `C:\Users\Sarah Johnson\OneDrive\Desktop\OS` |
| `OS_ROOT` | approved or active absolute OS path | approved or active absolute OS path |
| `DOTCLAUDE` | `<OS_ROOT>/.claude` | `<OS_ROOT>\.claude` |

The Desktop OS is the default, not the only supported root. Master, memory,
skills, progress, and backup paths are not inferred here; use the resolved
layout variables.

---

## Step 5 — Dual-Shell Command Patterns

For every filesystem operation, use the command for the student's detected platform. Never show both to the student — show only theirs.

### Create a folder

```zsh
# macOS
mkdir -p "/Users/sarah/Desktop/OS/active"
```

```powershell
# Windows
New-Item -ItemType Directory -Force -Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\active"
```

### Create the canonical skill folder and compatibility link

Instruction files do **not** branch by platform. On macOS, Windows, and Linux,
create one real canonical `<OS_ROOT>/AGENTS.md` and no root `CLAUDE.md`; Claude
Code and Codex both read `AGENTS.md` directly. Never use a symlink, hard link,
or junction for `AGENTS.md`. The platform-specific linking below applies only
to the skills directory.

```zsh
# macOS/Linux — one physical tree, then Claude's relative link
mkdir -p "/Users/sarah/Desktop/OS/.agents/skills" "/Users/sarah/Desktop/OS/.claude"
ln -s "../.agents/skills" "/Users/sarah/Desktop/OS/.claude/skills"
```

```powershell
# Windows — one physical tree, then Claude's directory junction
New-Item -ItemType Directory -Force -Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\.agents\skills", "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\.claude"
New-Item -ItemType Junction -Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\.claude\skills" -Target "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\.agents\skills"
```

Never create both paths as real skill directories. Verify a probe written in
`.agents/skills` can be read through `.claude/skills` before continuing.

### Move / rename a folder

```zsh
# macOS
mv "/Users/sarah/old-location/my-project" "/Users/sarah/Desktop/OS/my-business/my-project"
```

```powershell
# Windows
Move-Item -Path "C:\Users\Sarah Johnson\old-location\my-project" -Destination "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\my-business\my-project"
```

### Check whether a folder exists

```zsh
# macOS
test -d "/Users/sarah/Desktop/OS" && echo "exists" || echo "not found"
```

```powershell
# Windows
if (Test-Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS") { "exists" } else { "not found" }
```

### List the folder tree (verify structure)

```zsh
# macOS
find "/Users/sarah/Desktop/OS" -maxdepth 3 | sort
```

```powershell
# Windows
Get-ChildItem -Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS" -Recurse -Depth 3 | Select-Object FullName
```

### Write a file

Use the active host's safe file-editing capability and verify the result. Only use a shell-based write when no file-editing capability is available. Never require a capability by a host-specific display name.

```zsh
# macOS (shell fallback)
cat > "$MASTER_PATH" << 'EOF'
[file content here]
EOF
```

```powershell
# Windows (shell fallback)
Set-Content -Path $MASTER_PATH -Value @"
[file content here]
"@
```

---

## The Create-and-Verify Pattern (mandatory)

A known failure mode from the original build flow: a skill claimed a folder existed when the mkdir silently ran in the wrong location or failed without an error. **Always verify with a real listing after creating.**

```zsh
# macOS — create then verify
mkdir -p "/Users/sarah/Desktop/OS/active"
ls -A "/Users/sarah/Desktop/OS/"
# You must see "active" in the output before claiming success
```

```powershell
# Windows — create then verify
New-Item -ItemType Directory -Force -Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\active"
Get-ChildItem -Force -Path "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\"
# You must see "active" in the output before claiming success
```

**Never tell the student a folder was created without confirming it appears in the listing.** If it doesn't appear: stop, diagnose, fix. Don't move on.

> **Dot-folder rule:** When verifying a dot-folder, use `ls -A` on macOS — a
> bare `ls` hides dot-folders and will falsely report it missing. On Windows,
> use `Get-ChildItem -Force`.

---

## Edge Cases

### Username contains spaces
Always wrap paths in quotes. Both platforms support it:
- macOS: `"/Users/sarah anne/Desktop/OS"`
- Windows: `"C:\Users\Sarah Anne Johnson\OneDrive\Desktop\OS"`

### No Desktop folder exists
Rare but possible on a fresh Windows install or heavily customized environment.

```powershell
# Windows — check first
if (-not (Test-Path $desktop)) {
    Write-Output "Desktop folder not found at: $desktop"
    # Ask the student: "Can you tell me where your Desktop is? Or we can create the OS folder somewhere else."
}
```

On macOS this essentially never happens. If `~/Desktop` is missing, ask the student where they'd like the OS folder.

### No Desktop folder exists (macOS)
```zsh
if [ ! -d "$HOME/Desktop" ]; then
    echo "Desktop folder not found. Where would you like to create your OS folder?"
fi
```

---

## Golden Rule

Never print a `~/Desktop/...` Mac path to a Windows user. Never print a `C:\Users\...` Windows path to a Mac user. Never show a Claude command to a Codex user or a Codex command to a Claude user. After detection in Step 1, every path, command, skill mention, settings location, and recovery step is for the student's active environment only. Detection runs once per skill invocation; store the results and reuse them throughout.

Never assume Desktop when a supported active OS workspace is already open.
Never search broadly for a custom OS. If its location is not open and the
default fallback is absent, ask the student to open the folder they chose.
