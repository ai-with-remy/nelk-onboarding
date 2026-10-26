#!/usr/bin/env bash
# Install the marketplace into a temporary Codex home, leaving real user state untouched.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_BIN="${CODEX_BIN:-codex}"

usage() {
  printf 'Usage: %s\n' "$0"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
  shift
done

if ! command -v "$CODEX_BIN" >/dev/null 2>&1; then
  printf 'Codex CLI not found. Install Codex or set CODEX_BIN, then retry.\n' >&2
  exit 2
fi

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ai-os-codex-smoke.XXXXXX")"
chmod 700 "$TMP_ROOT"

cleanup() {
  if [ "${KEEP_SMOKE_HOME:-0}" = "1" ]; then
    printf 'Temporary Codex home kept at: %s\n' "$TMP_ROOT"
  else
    rm -rf "$TMP_ROOT"
  fi
}
trap cleanup EXIT

export HOME="$TMP_ROOT/home"
export CODEX_HOME="$HOME/.codex"
mkdir -p "$CODEX_HOME"

printf 'Using isolated Codex home: %s\n' "$CODEX_HOME"
"$CODEX_BIN" plugin marketplace add "$ROOT"

AVAILABLE="$("$CODEX_BIN" plugin list --marketplace nelk-onboarding)"
printf '%s\n' "$AVAILABLE"

LOCAL_PLUGINS=(ai-os)
for plugin in "${LOCAL_PLUGINS[@]}"; do
  if ! grep -Fq "$plugin" <<<"$AVAILABLE"; then
    printf 'Marketplace listing did not expose %s.\n' "$plugin" >&2
    exit 1
  fi
  "$CODEX_BIN" plugin add "$plugin@nelk-onboarding"
done

INSTALLED="$("$CODEX_BIN" plugin list --marketplace nelk-onboarding)"
printf '%s\n' "$INSTALLED"
for plugin in "${LOCAL_PLUGINS[@]}"; do
  if ! grep -Eq "${plugin}@nelk-onboarding[[:space:]]+installed" <<<"$INSTALLED"; then
    printf 'Codex did not mark %s as installed.\n' "$plugin" >&2
    exit 1
  fi
done
printf 'Clean-room Codex install smoke test passed for %s local plugins.\n' "${#LOCAL_PLUGINS[@]}"
