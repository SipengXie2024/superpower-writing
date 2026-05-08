#!/usr/bin/env bash
# Lightweight dependency notice for cn-bid-writing.

set -euo pipefail

if ! python3 -c "import yaml" >/dev/null 2>&1; then
  echo "[cn-bid-writing] PyYAML not found; install it before running /check or /export-docx." >&2
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "[cn-bid-writing] pandoc not found; /export-docx will still build combined markdown but cannot create docx." >&2
fi
