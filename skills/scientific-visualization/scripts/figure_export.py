#!/usr/bin/env python3
"""
Figure export utilities for CS publication-quality figures.

Saves matplotlib figures with venue-appropriate format and resolution, and
verifies dimensions match the target venue's column width.

Adapted from K-Dense AI's scientific-agent-skills, with biology-focused
venues (Nature, Science, Cell) replaced by CS venues.
"""

import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Union


def save_publication_figure(
    fig: plt.Figure,
    filename: Union[str, Path],
    formats: List[str] = ('pdf',),
    dpi: int = 600,
    transparent: bool = False,
    bbox_inches: str = 'tight',
    pad_inches: float = 0.05,
    facecolor: str = 'white',
    **kwargs
) -> List[Path]:
    """
    Save a figure in publication-ready format(s).

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    filename : str or Path
        Base filename without extension. Path may include directories.
    formats : list of str, default ('pdf',)
        File formats: 'pdf' (default, vector), 'png' (raster, set dpi=600),
        'svg', 'eps'.
    dpi : int, default 600
        Resolution for raster formats and rasterized portions of vector formats.
    transparent : bool, default False
    bbox_inches : str, default 'tight'
    pad_inches : float, default 0.05
    facecolor : str, default 'white'

    Returns
    -------
    list of Path
        Paths of saved files.
    """
    filename = Path(filename)
    base = filename.with_suffix('')
    saved = []

    for fmt in formats:
        out = base.with_suffix(f'.{fmt}')
        save_kwargs = {
            'dpi': dpi,
            'bbox_inches': bbox_inches,
            'pad_inches': pad_inches,
            'facecolor': facecolor if not transparent else 'none',
            'edgecolor': 'none',
            'transparent': transparent,
            'format': fmt,
        }
        save_kwargs.update(kwargs)
        try:
            fig.savefig(out, **save_kwargs)
            saved.append(out)
            print(f"Saved: {out}")
        except Exception as e:
            print(f"Failed to save {out}: {e}")
    return saved


# Per-venue defaults: (formats, dpi). PDF is always preferred for plots; PNG is
# the raster fallback for screenshots and very dense heatmaps.
VENUE_EXPORT_SPECS = {
    'ieee':    {'plot': {'formats': ['pdf'],        'dpi': 600},
                'raster': {'formats': ['png'],      'dpi': 600}},
    'acm':     {'plot': {'formats': ['pdf'],        'dpi': 600},
                'raster': {'formats': ['png'],      'dpi': 600}},
    'usenix':  {'plot': {'formats': ['pdf'],        'dpi': 300},
                'raster': {'formats': ['png'],      'dpi': 300}},
    'neurips': {'plot': {'formats': ['pdf'],        'dpi': 600},
                'raster': {'formats': ['png'],      'dpi': 600}},
    'icml':    {'plot': {'formats': ['pdf'],        'dpi': 600},
                'raster': {'formats': ['png'],      'dpi': 600}},
    'iclr':    {'plot': {'formats': ['pdf'],        'dpi': 600},
                'raster': {'formats': ['png'],      'dpi': 600}},
    'arxiv':   {'plot': {'formats': ['pdf'],        'dpi': 300},
                'raster': {'formats': ['png'],      'dpi': 300}},
}


def save_for_venue(
    fig: plt.Figure,
    filename: Union[str, Path],
    venue: str,
    figure_type: str = 'plot',
) -> List[Path]:
    """
    Save with per-venue defaults.

    Parameters
    ----------
    venue : str
        'ieee', 'acm', 'usenix', 'neurips', 'icml', 'iclr', 'arxiv'
    figure_type : str
        'plot' (vector PDF, default) or 'raster' (PNG at venue's required DPI)
    """
    venue = venue.lower()
    if venue not in VENUE_EXPORT_SPECS:
        available = ', '.join(VENUE_EXPORT_SPECS.keys())
        raise ValueError(f"Venue '{venue}' not recognized. Available: {available}")
    if figure_type not in VENUE_EXPORT_SPECS[venue]:
        available = ', '.join(VENUE_EXPORT_SPECS[venue].keys())
        raise ValueError(f"Type '{figure_type}' not valid. Available: {available}")

    spec = VENUE_EXPORT_SPECS[venue][figure_type]
    print(f"Saving for {venue.upper()} ({figure_type}): formats={spec['formats']}, dpi={spec['dpi']}")
    return save_publication_figure(
        fig=fig,
        filename=filename,
        formats=spec['formats'],
        dpi=spec['dpi'],
    )


# Per-venue figure-size specs (width in inches; max height in inches)
VENUE_SIZE_SPECS = {
    'ieee':    {'single': 3.5,  'double': 7.16, 'max_height': 9.7},
    'acm':     {'single': 3.33, 'double': 7.0,  'max_height': 9.0},
    'usenix':  {'single': 3.33, 'double': 7.0,  'max_height': 9.0},
    'neurips': {'single': 5.5,  'double': 5.5,  'max_height': 8.5},
    'icml':    {'single': 6.75, 'double': 6.75, 'max_height': 8.5},
    'iclr':    {'single': 5.5,  'double': 5.5,  'max_height': 8.5},
    'arxiv':   {'single': 5.5,  'double': 7.0,  'max_height': 9.0},
}


def check_figure_size(fig: plt.Figure, venue: str = 'ieee') -> dict:
    """
    Check whether the figure's dimensions match the target venue.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    venue : str

    Returns
    -------
    dict with keys: width_in, height_in, venue, column_type, width_ok,
    height_ok, compliant, recommendations
    """
    venue = venue.lower()
    if venue not in VENUE_SIZE_SPECS:
        print(f"Warning: venue '{venue}' not found, falling back to 'ieee'")
        venue = 'ieee'
    spec = VENUE_SIZE_SPECS[venue]

    width_in, height_in = fig.get_size_inches()

    # Tolerance: 0.05 in = ~ 1.3 mm
    tolerance = 0.05
    column_type = None
    width_ok = False
    if abs(width_in - spec['single']) < tolerance:
        column_type, width_ok = 'single', True
    elif abs(width_in - spec['double']) < tolerance:
        column_type, width_ok = 'double', True

    height_ok = height_in <= spec['max_height']

    result = {
        'width_in': width_in,
        'height_in': height_in,
        'venue': venue,
        'column_type': column_type,
        'width_ok': width_ok,
        'height_ok': height_ok,
        'compliant': width_ok and height_ok,
        'recommendations': {
            'single_column_in': spec['single'],
            'double_column_in': spec['double'],
            'max_height_in': spec['max_height'],
        }
    }

    print(f"\n{'=' * 60}")
    print(f"Figure size check for {venue.upper()}")
    print(f"{'=' * 60}")
    print(f"Current size: {width_in:.2f} x {height_in:.2f} inches")
    print(f"\n{venue.upper()} specifications:")
    print(f"  Single column: {spec['single']:.2f} in")
    print(f"  Double / full: {spec['double']:.2f} in")
    print(f"  Max height: {spec['max_height']:.1f} in")
    print(f"\nCompliance:")
    print(f"  Width: {'OK' if width_ok else 'NON-STANDARD'} ({column_type or 'custom'})")
    print(f"  Height: {'OK' if height_ok else 'TOO TALL'}")
    print(f"  Overall: {'COMPLIANT' if result['compliant'] else 'NEEDS ADJUSTMENT'}")
    print(f"{'=' * 60}\n")

    return result


def verify_font_embedding(pdf_path: Union[str, Path]) -> dict:
    """
    Check whether fonts in a PDF are embedded and not Type 3.

    Uses the `pdffonts` CLI tool. Returns a dict with `all_embedded` and
    `any_type3` booleans, and a list of font records.

    Returns None if pdffonts is unavailable.
    """
    import shutil
    import subprocess

    if shutil.which('pdffonts') is None:
        print("Warning: pdffonts not found. Install poppler-utils to verify font embedding.")
        return None

    try:
        result = subprocess.run(['pdffonts', str(pdf_path)],
                                capture_output=True, text=True, timeout=10)
    except Exception as e:
        print(f"pdffonts failed: {e}")
        return None

    fonts = []
    lines = result.stdout.splitlines()
    if len(lines) < 3:
        return {'all_embedded': True, 'any_type3': False, 'fonts': []}

    # pdffonts output:
    # name  type  encoding  emb  sub  uni  object ID
    # The `type` and `encoding` columns can contain spaces (e.g., "CID TrueType"),
    # so split-by-whitespace gets misaligned. Parse from the right: the last
    # six tokens are always [emb, sub, uni, object_id_a, object_id_b].
    # That is, parts[-5] = emb, parts[-4] = sub, parts[-3] = uni.
    # Type 3 detection scans the whole line because "Type 3" is two tokens.
    for line in lines[2:]:
        parts = line.split()
        if len(parts) < 7:
            continue
        font_name = parts[0]
        emb = parts[-5]
        # Heuristic: type spans tokens 1..n, where n is end of the encoding token,
        # before the emb column. Use line slice up to the emb column for display.
        type_field = ' '.join(parts[1:-5][:-1]) if len(parts) > 6 else ''
        is_type3 = 'type 3' in type_field.lower() or 'type 3' in line.lower()
        fonts.append({'name': font_name, 'type': type_field,
                      'embedded': emb == 'yes', 'is_type3': is_type3})

    all_embedded = all(f['embedded'] for f in fonts)
    any_type3 = any(f.get('is_type3', False) for f in fonts)

    print(f"PDF: {pdf_path}")
    print(f"  Fonts: {len(fonts)}")
    print(f"  All embedded: {all_embedded}")
    print(f"  Type 3 detected: {any_type3}")
    if any_type3:
        print("  -> Set `pdf.fonttype: 42` in your script to fix.")

    return {'all_embedded': all_embedded, 'any_type3': any_type3, 'fonts': fonts}


if __name__ == "__main__":
    import numpy as np

    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), label='sin')
    ax.plot(x, np.cos(x), label='cos')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend(frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    check_figure_size(fig, venue='ieee')

    print("Saving figure...")
    save_publication_figure(fig, 'example_figure', formats=['pdf', 'png'], dpi=600)

    print("\nSaving for IEEE...")
    save_for_venue(fig, 'example_figure_ieee', venue='ieee', figure_type='plot')

    plt.close(fig)
