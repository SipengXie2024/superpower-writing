#!/usr/bin/env bash
# Initialize a .writing/ directory in the current project. Combines the
# writing-domain skeleton (manuscript/, claims/, figures/, reviews/, archive/
# plus metadata.yaml and outline.md) with upstream planning-foundation's
# idempotent re-run + .gitignore auto-registration behavior.
#
# Usage: ./init-writing-dir.sh [target-dir]
#   Default target: .writing in the current working directory.
#   Re-running is safe: missing files are created, existing files are preserved.

set -euo pipefail

TARGET="${1:-.writing}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
TEMPLATE_DIR="$PLUGIN_ROOT/templates"
DATE=$(date +%Y-%m-%d)

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template directory not found: $TEMPLATE_DIR" >&2
  echo "Is CLAUDE_PLUGIN_ROOT set correctly?" >&2
  exit 1
fi

mkdir -p "$TARGET"/{manuscript,claims,figures,reviews,archive}

# .gitignore: add .writing/ build artifacts and LaTeX compile outputs if not present.
# (Full .writing/ is NOT ignored — .tex sources live under version control.)
PROJECT_ROOT="$(pwd)"
GITIGNORE="${PROJECT_ROOT}/.gitignore"
add_ignore_line() {
  local line="$1"
  if [[ -f "$GITIGNORE" ]]; then
    if ! grep -qF "$line" "$GITIGNORE" 2>/dev/null; then
      echo "$line" >> "$GITIGNORE"
      echo "Added $line to .gitignore"
    fi
  elif [[ -d "${PROJECT_ROOT}/.git" ]]; then
    printf '%s\n' "$line" > "$GITIGNORE"
    echo "Created .gitignore with $line"
  fi
}
add_ignore_line ".writing/verify-cache.json"
add_ignore_line ".writing/stash/"
# LaTeX compile artifacts
add_ignore_line ".writing/main.aux"
add_ignore_line ".writing/main.log"
add_ignore_line ".writing/main.out"
add_ignore_line ".writing/main.toc"
add_ignore_line ".writing/main.bbl"
add_ignore_line ".writing/main.blg"
add_ignore_line ".writing/main.synctex.gz"
add_ignore_line ".writing/main.pdf"
add_ignore_line ".writing/main.fdb_latexmk"
add_ignore_line ".writing/main.fls"

create_if_missing() {
  local src="$1" dst="$2"
  if [[ -f "$dst" ]]; then
    echo "$dst already exists, skipping"
  else
    sed "s|\[YYYY-MM-DD\]|$DATE|g; s|\[DATE\]|$DATE|g" "$src" > "$dst"
    echo "Created $dst"
  fi
}

create_if_missing "$TEMPLATE_DIR/progress.md"   "$TARGET/progress.md"
create_if_missing "$TEMPLATE_DIR/findings.md"   "$TARGET/findings.md"
create_if_missing "$TEMPLATE_DIR/metadata.yaml" "$TARGET/metadata.yaml"
[[ -f "$TARGET/outline.md" ]] || : > "$TARGET/outline.md"

# refs.bib: empty file that `submission` will later populate from Zotero.
[[ -f "$TARGET/refs.bib" ]] || : > "$TARGET/refs.bib"

# main.tex: top-level LaTeX skeleton that \input{}s each manuscript section.
# Generic \documentclass{article} — customize the preamble per-venue if needed.
if [[ ! -f "$TARGET/main.tex" ]]; then
  cat > "$TARGET/main.tex" <<'MAINTEX'
\documentclass[11pt]{article}

% Core packages (generic / venue-agnostic). Swap documentclass and style
% files per venue (acmart / IEEEtran / neurips / icml / llncs) without
% touching section files under manuscript/.
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{hyperref}
\usepackage[numbers,sort&compress]{natbib}

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}

\title{TITLE TODO}
\author{AUTHORS TODO}
\date{\today}

\begin{document}

\maketitle

% Each section below lives in its own file under manuscript/. Add or remove
% \input{} lines to match the paper's structure. Files are created by
% `outlining` + `drafting` skills as sections are written.
\input{manuscript/00_abstract}
\input{manuscript/01_introduction}
% --- Motivation (opt-in, systems/architecture venues) ---
% When enabled, UNCOMMENT the \input below, RENAME the filename to reflect
% its actual position (e.g., 02_motivation), and RENUMBER every subsequent
% section's file and \input entry so the numbers match the paper's order.
% Example post-enable layout: 02_motivation -> 03_background -> 04_methods -> ...
% \input{manuscript/02_motivation}
\input{manuscript/02_background}
\input{manuscript/03_methods}
\input{manuscript/04_results}
\input{manuscript/05_discussion}
\input{manuscript/06_conclusion}
% --- Related Work placement ---
% Choose ONE of these, not both. Late placement (NeurIPS/ICML) is the default;
% early placement (SIGCOMM/NSDI/CCS) usually renumbers to 02_related_work and
% bumps every following file by 1.
% \input{manuscript/07_related_work}

\bibliographystyle{plainnat}
\bibliography{refs}

\end{document}
MAINTEX
  echo "Created $TARGET/main.tex"
fi

cat <<EOF

Initialized $TARGET/
  files:   progress.md  findings.md  metadata.yaml  outline.md
           main.tex  refs.bib
  subdirs: manuscript/ (LaTeX sections)  claims/  figures/  reviews/  archive/

Next step: open \`$TARGET/outline.md\` and start outlining, or invoke the
\`superpower-writing:outlining\` skill. Sections are drafted as individual
.tex files under manuscript/ and pulled together by main.tex at submission.
EOF
