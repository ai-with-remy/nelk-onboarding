#!/usr/bin/env bash
# Install the marketplace into a temporary Codex home, leaving real user state untouched.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_BIN="${CODEX_BIN:-codex}"

if ! command -v "$CODEX_BIN" >/dev/null 2>&1; then
  printf 'Codex CLI not found. Install Codex or set CODEX_BIN, then retry.\n' >&2
  exit 2
fi

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/nelk-codex-smoke.XXXXXX")"
trap 'rm -rf "$TMP_ROOT"' EXIT

export HOME="$TMP_ROOT/home"
export CODEX_HOME="$HOME/.codex"
mkdir -p "$CODEX_HOME"

"$CODEX_BIN" plugin marketplace add "$ROOT"
"$CODEX_BIN" plugin add nelk@nelk-onboarding

INSTALLED="$("$CODEX_BIN" plugin list --marketplace nelk-onboarding)"
printf '%s\n' "$INSTALLED"
if ! grep -Eq 'nelk@nelk-onboarding[[:space:]]+installed' <<<"$INSTALLED"; then
  printf 'Codex did not mark nelk as installed.\n' >&2
  exit 1
fi
if ! find "$CODEX_HOME/plugins/cache" -path '*/skills/onboard/SKILL.md' | grep -q .; then
  printf 'Installed plugin is missing skills/onboard/SKILL.md.\n' >&2
  exit 1
fi
printf 'Clean-room Codex install smoke test passed.\n'
