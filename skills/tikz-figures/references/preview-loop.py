#!/usr/bin/env python3
"""Preview loop for TikZ figures: compile one figure at a time and report the
width it will actually occupy in the paper, against the venue's column budget.

Why this exists. Compiling the whole manuscript to see one figure is slow, and
the compiled page does not tell you whether the figure fits: LaTeX silently
scales an oversized \\includegraphics, and an \\input'd tikzpicture that is 20pt
too wide just overflows into the gutter. This script answers the one question
that matters after every edit, in about two seconds: how wide is it, and does it
fit. Everything else in the loop (1:1 render, tiled overlap check) hangs off that.

Usage
-----
    python3 preview-loop.py --venue usenix fig1_pipeline fig2_depgraph
    python3 preview-loop.py --venue ieee --wide fig1_overview
    python3 preview-loop.py --col-pt 240.1 --text-pt 504 fig3

Each argument is a figure source under --src (default: the current directory),
named <figure>.tex and containing a bare tikzpicture, no preamble. Append :wide
to a single figure to give it the full text width instead of one column:

    python3 preview-loop.py --venue usenix fig2_depgraph fig1_pipeline:wide

Outputs, under --out (default: ./out):
    <figure>_preview.pdf   the figure alone, at its natural size
    <figure>_screen.png    150 dpi, i.e. 1:1 with how it reads on screen
    <figure>_print.png     300 dpi, for inspecting detail and overlaps

Read the screen PNG, not the print PNG, when judging legibility. A 4pt label is
perfectly readable in a print-resolution render and unreadable in the paper.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

# Text block and column widths in points. Verify against the venue's current
# style file before trusting these; templates do get revised.
VENUES = {
    # USENIX (usenix2019_v3.1): 7in text block, 0.33in gutter.
    "usenix":  {"text": 7.0 * 72, "col": (7.0 - 0.33) / 2 * 72},
    # ACM acmart sigconf.
    "acm":     {"text": 7.0 * 72, "col": (7.0 - 0.33) / 2 * 72},
    # IEEEtran conference.
    "ieee":    {"text": 7.25 * 72, "col": 3.5 * 72},
    # NeurIPS / ICLR / ICML: single column.
    "neurips": {"text": 5.5 * 72, "col": 5.5 * 72},
}

WRAPPER = r"""\documentclass[%(pt)dpt,border=%(border)gpt,varwidth=%(maxw)fpt]{standalone}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
%(font)s
\usepackage{amsmath,amssymb}
%(style)s
\begin{document}
\input{%(body)s}
\end{document}
"""


def build(name, span, args):
    body = Path(args.src) / f"{name}.tex"
    if not body.exists():
        print(f"  MISS {name}: no {body}")
        return None

    budget = args.text_pt if span == "wide" else args.col_pt
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tex = out / f"{name}_preview.tex"
    tex.write_text(WRAPPER % {
        "pt": args.pt,
        "border": args.border,
        "maxw": budget + 60,          # generous; we measure, we never clip
        "font": args.font,
        "style": f"\\input{{{Path(args.style).with_suffix('').as_posix()}}}" if args.style else "",
        "body": body.with_suffix("").as_posix(),
    })

    r = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
         "-output-directory", str(out), str(tex)],
        capture_output=True, text=True)
    pdf = out / f"{name}_preview.pdf"
    if r.returncode != 0 or not pdf.exists():
        log = out / f"{name}_preview.log"
        err = ""
        if log.exists():
            lines = log.read_text(errors="replace").splitlines()
            err = "\n".join(l for l in lines if l.startswith("!") or "Error" in l)[:900]
        print(f"  FAIL {name}\n{err or r.stdout[-900:]}")
        return None

    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    if not m:
        print(f"  FAIL {name}: cannot read page size")
        return None
    # The standalone border is preview padding, not part of the typeset figure.
    w = float(m.group(1)) - 2 * args.border
    h = float(m.group(2)) - 2 * args.border
    over = w - budget
    flag = "OK  " if over <= 0.5 else "WIDE"
    print(f"  {flag} {name}: {w:.1f} x {h:.1f} pt   "
          f"(budget {budget:.1f}pt, {'+' if over > 0 else ''}{over:.1f})")

    for dpi, tag in ((150, "screen"), (300, "print")):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile",
                        str(pdf), str(out / f"{name}_{tag}")], check=True)
    return w, h


def main():
    p = argparse.ArgumentParser(
        description="Compile TikZ figures one at a time and report their typeset width.")
    p.add_argument("figures", nargs="+",
                   help="figure basenames under --src; append :wide for full text width")
    p.add_argument("--venue", choices=sorted(VENUES), help="preset column geometry")
    p.add_argument("--col-pt", type=float, help="column width in pt (overrides --venue)")
    p.add_argument("--text-pt", type=float, help="text width in pt (overrides --venue)")
    p.add_argument("--src", default=".", help="directory holding the figure sources")
    p.add_argument("--out", default="out", help="directory for previews (default: out)")
    p.add_argument("--style", default="",
                   help="shared style file to \\input before the figure")
    p.add_argument("--font", default=r"\usepackage{mathptmx}",
                   help=r"font package line; match the paper (default: \usepackage{mathptmx})")
    p.add_argument("--pt", type=int, default=10, help="body font size (default: 10)")
    p.add_argument("--border", type=float, default=2.0,
                   help="preview margin in pt, subtracted from the report (default: 2)")
    args = p.parse_args()

    if args.venue:
        args.col_pt = args.col_pt or VENUES[args.venue]["col"]
        args.text_pt = args.text_pt or VENUES[args.venue]["text"]
    if not args.col_pt or not args.text_pt:
        p.error("give --venue, or both --col-pt and --text-pt")

    print(f"column {args.col_pt:.1f}pt, text {args.text_pt:.1f}pt")
    bad = 0
    for spec in args.figures:
        name, _, span = spec.partition(":")
        if build(name, span or "col", args) is None:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
