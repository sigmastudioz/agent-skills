#!/usr/bin/env bash
# Wait inside the shell, not the model: one tool call instead of N polls.
# Usage: wait_for.sh [--timeout SEC] [--every SEC] -- <check command>
# Exits 0 when the check succeeds (prints its last 20 lines), 124 on timeout.
timeout=900; every=15
while [[ $# -gt 0 && "$1" != "--" ]]; do
  case "$1" in --timeout) timeout=$2; shift 2;; --every) every=$2; shift 2;; *) echo "unknown arg $1" >&2; exit 2;; esac
done
shift; [[ $# -gt 0 ]] || { echo "usage: wait_for.sh [--timeout S] [--every S] -- cmd" >&2; exit 2; }
start=$(date +%s); n=0
while :; do
  n=$((n+1)); out=$("$@" 2>&1); rc=$?
  if [[ $rc -eq 0 ]]; then printf '%s\n' "$out" | tail -20; echo "[wait_for] ready after $n checks, $(( $(date +%s)-start ))s"; exit 0; fi
  if (( $(date +%s) - start >= timeout )); then printf '%s\n' "$out" | tail -20; echo "[wait_for] timeout after $n checks"; exit 124; fi
  sleep "$every"
done
