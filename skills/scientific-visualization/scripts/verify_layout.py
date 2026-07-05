"""Geometric self-check for a rendered matplotlib figure.

Ported from the render-then-verify discipline: after you build a figure and
before you commit the PDF, run ``verify(fig)`` to catch text that collides with
other text or with an axis spine, and text that spills off the canvas. These are
geometric defects a style preset cannot prevent -- they surface only once real
labels sit at real sizes, which is exactly when a reviewer sees them.

Usage inside a generator script (``.writing/figures/src/<fig_id>.py``)::

    from verify_layout import verify
    fig, ax = plt.subplots(...)
    ...
    fig.savefig("fig.pdf", bbox_inches="tight")
    verify(fig, crop_dir=".writing/figures/.crops/<fig_id>")

``verify`` prints a defect report and, when ``crop_dir`` is given, writes one PNG
per panel so you -- or a review agent -- can open each with the Read tool and run
the perceptual pass the geometry check cannot: low-contrast labels, leaders that
cross a neighbor, two series in near-identical colors, a legend keyed to the
wrong panel.

The geometry check is deliberately conservative: a tick label resting on its own
axes spine is not a finding, only text-vs-text and text-vs-foreign-spine overlaps
are. Runs headless -- force the Agg backend before importing pyplot if you have no
display.
"""

import os

import matplotlib as mpl


def _renderer(fig):
    fig.canvas.draw()
    try:
        return fig.canvas.get_renderer()
    except AttributeError:  # non-Agg canvas without a cached renderer
        from matplotlib.backends.backend_agg import FigureCanvasAgg

        return FigureCanvasAgg(fig).get_renderer()


def _visible_texts(fig, renderer):
    out = []
    for t in fig.findobj(mpl.text.Text):
        if not t.get_visible():
            continue
        s = t.get_text()
        if not s or not s.strip():
            continue
        try:
            ext = t.get_window_extent(renderer)
        except Exception:
            continue
        if ext.width <= 0 or ext.height <= 0:
            continue
        out.append((t, ext))
    return out


def find_overlaps(fig, renderer=None):
    """Return geometric defects as a dict of lists.

    Keys: ``text_text`` (label pairs that overlap), ``text_spine`` (a label over
    a spine that is not its own axes' tick), ``out_of_bounds`` (labels past the
    figure edge).
    """
    if renderer is None:
        renderer = _renderer(fig)
    texts = _visible_texts(fig, renderer)

    spines = []
    for ax in fig.axes:
        for name, sp in ax.spines.items():
            if not sp.get_visible():
                continue
            try:
                spines.append((ax, name, sp.get_window_extent(renderer)))
            except Exception:
                pass

    # A tick label sitting on its own axes' spine is expected, not a defect.
    tick_axes = {}
    for ax in fig.axes:
        labels = (
            ax.get_xticklabels()
            + ax.get_yticklabels()
            + ax.get_xticklabels(minor=True)
            + ax.get_yticklabels(minor=True)
        )
        for tl in labels:
            tick_axes[tl] = ax

    text_text = []
    for i, (ta, ba) in enumerate(texts):
        for tb, bb in texts[i + 1:]:
            if ba.overlaps(bb):
                text_text.append((ta.get_text(), tb.get_text()))

    text_spine = []
    for t, bt in texts:
        for ax, name, bs in spines:
            if not bt.overlaps(bs):
                continue
            if tick_axes.get(t) is ax:
                continue
            text_spine.append((t.get_text(), name))

    fb = fig.bbox
    tol = 0.5
    out_of_bounds = []
    for t, bt in texts:
        if t in tick_axes:
            # Tick labels routinely overrun the figure edge; savefig with
            # bbox_inches='tight' absorbs it. Only non-tick text (titles,
            # annotations, axis labels, legend) being clipped is a real defect.
            continue
        inside = (
            bt.x0 >= fb.x0 - tol
            and bt.y0 >= fb.y0 - tol
            and bt.x1 <= fb.x1 + tol
            and bt.y1 <= fb.y1 + tol
        )
        if not inside:
            out_of_bounds.append(t.get_text())

    return {
        "text_text": text_text,
        "text_spine": text_spine,
        "out_of_bounds": out_of_bounds,
    }


def crop_panels(fig, out_dir, dpi=200, renderer=None):
    """Save one PNG per axes so each panel can be perceptually reviewed.

    Returns the list of written paths. Open each with the Read tool.
    """
    from matplotlib.transforms import Bbox

    os.makedirs(out_dir, exist_ok=True)
    if renderer is None:
        renderer = _renderer(fig)
    inv = fig.dpi_scale_trans.inverted()
    pad = 0.05  # inches
    paths = []
    for i, ax in enumerate(fig.axes):
        try:
            tight = ax.get_tightbbox(renderer)
        except Exception:
            tight = ax.get_window_extent(renderer)
        bb = tight.transformed(inv)
        bb = Bbox.from_extents(bb.x0 - pad, bb.y0 - pad, bb.x1 + pad, bb.y1 + pad)
        path = os.path.join(out_dir, f"panel_{i}.png")
        fig.savefig(path, dpi=dpi, bbox_inches=bb)
        paths.append(path)
    return paths


def _print_report(f):
    tt, ts, oob = f["text_text"], f["text_spine"], f["out_of_bounds"]
    if not (tt or ts or oob):
        print("Layout geometry: clean -- no text/text or text/spine overlaps, nothing off-canvas.")
        return
    print("Layout geometry defects (fix by moving/shortening/staggering, then re-run):")
    for a, b in tt:
        print(f"  [text/text]  {a!r} overlaps {b!r}")
    for a, name in ts:
        print(f"  [text/spine] {a!r} overlaps the {name} spine of another axes")
    for a in oob:
        print(f"  [warn: off-canvas] {a!r} extends past the figure edge "
              f"(bbox_inches='tight' will expand the canvas, but the layout is cramped)")


def verify(fig, crop_dir=None, dpi=200, verbose=True):
    """Run the geometry check and optionally write per-panel crops.

    Returns the findings dict with two extra keys: ``crops`` (paths written) and
    ``clean`` (True when no text/text, text/spine, or off-canvas findings).
    """
    renderer = _renderer(fig)
    findings = find_overlaps(fig, renderer=renderer)
    if verbose:
        _print_report(findings)

    crops = []
    if crop_dir:
        crops = crop_panels(fig, crop_dir, dpi=dpi, renderer=renderer)
        if verbose:
            print(f"\nWrote {len(crops)} panel crop(s) to {crop_dir}/ -- open each with the Read")
            print("tool and run the perceptual pass the geometry check cannot: contrast, smallest")
            print("mark visible, no crossing leaders, no two series in near-identical colors,")
            print("legend keyed to its own panel.")

    findings["crops"] = crops
    findings["clean"] = not (
        findings["text_text"] or findings["text_spine"] or findings["out_of_bounds"]
    )
    return findings


if __name__ == "__main__":
    # Self-test: a deliberately broken figure must report defects; a clean one
    # should report none. Run: python verify_layout.py
    mpl.use("Agg")
    import matplotlib.pyplot as plt

    broken, ax = plt.subplots(figsize=(2, 2))
    ax.plot([0, 1], [0, 1])
    ax.text(0.5, 0.5, "BIG OVERLAP LABEL", fontsize=40)
    ax.text(0.5, 0.5, "SECOND OVERLAP", fontsize=40)
    print("== broken figure ==")
    res_broken = verify(broken, verbose=True)
    assert not res_broken["clean"], "expected the broken figure to report defects"
    plt.close(broken)

    clean, ax2 = plt.subplots(figsize=(4, 3))
    ax2.plot([1, 2, 3], [1, 4, 9], marker="o", label="ours")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.legend(frameon=False)
    clean.tight_layout()
    print("\n== clean figure ==")
    verify(clean, verbose=True)
    plt.close(clean)

    print("\nself-test ok")
