#!/usr/bin/env python3
"""
Matplotlib style presets for CS publication-quality figures.

Provides preconfigured matplotlib styles tuned for IEEE, ACM, USENIX, NeurIPS,
ICML, ICLR, and arXiv submissions, plus a colorblind-friendly default palette.

Adapted from K-Dense AI's scientific-agent-skills, with biology-focused
venues (Nature, Science, Cell) replaced by CS venues.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import Dict, Any


# Okabe-Ito colorblind-friendly palette (default for categorical data)
OKABE_ITO_COLORS = [
    '#E69F00',  # Orange
    '#56B4E9',  # Sky Blue
    '#009E73',  # Bluish Green
    '#F0E442',  # Yellow
    '#0072B2',  # Blue
    '#D55E00',  # Vermillion
    '#CC79A7',  # Reddish Purple
    '#000000',  # Black
]

# High-contrast 4-color subset (best for B/W print and dense plots)
OKABE_ITO_4 = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']

# Paul Tol palettes
TOL_BRIGHT = ['#4477AA', '#EE6677', '#228833', '#CCBB44',
              '#66CCEE', '#AA3377', '#BBBBBB']
TOL_MUTED = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933',
             '#DDCC77', '#CC6677', '#882255', '#AA4499']
TOL_HIGH_CONTRAST = ['#004488', '#DDAA33', '#BB5566']

# Wong palette
WONG_COLORS = ['#000000', '#E69F00', '#56B4E9', '#009E73',
               '#F0E442', '#0072B2', '#D55E00', '#CC79A7']


def get_base_style() -> Dict[str, Any]:
    """Return base publication-quality matplotlib rcParams as a dict."""
    return {
        # Figure
        'figure.dpi': 100,
        'figure.facecolor': 'white',
        'figure.autolayout': False,
        'figure.constrained_layout.use': True,

        # Font
        'font.size': 8,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],

        # Embed fonts in PDF (avoid Type 3 warnings on submission portals)
        'pdf.fonttype': 42,
        'ps.fonttype': 42,

        # Axes
        'axes.linewidth': 0.5,
        'axes.labelsize': 9,
        'axes.titlesize': 9,
        'axes.labelweight': 'normal',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.edgecolor': 'black',
        'axes.labelcolor': 'black',
        'axes.axisbelow': True,
        'axes.prop_cycle': mpl.cycler(color=OKABE_ITO_COLORS),
        'axes.grid': False,

        # Ticks
        'xtick.major.size': 3,
        'xtick.minor.size': 2,
        'xtick.major.width': 0.5,
        'xtick.minor.width': 0.5,
        'xtick.labelsize': 7,
        'xtick.direction': 'out',
        'ytick.major.size': 3,
        'ytick.minor.size': 2,
        'ytick.major.width': 0.5,
        'ytick.minor.width': 0.5,
        'ytick.labelsize': 7,
        'ytick.direction': 'out',

        # Lines
        'lines.linewidth': 1.5,
        'lines.markersize': 4,
        'lines.markeredgewidth': 0.5,

        # Legend
        'legend.fontsize': 7,
        'legend.frameon': False,
        'legend.loc': 'best',

        # Save
        'savefig.dpi': 600,
        'savefig.format': 'pdf',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'savefig.transparent': False,
        'savefig.facecolor': 'white',

        # Image
        'image.cmap': 'viridis',
        'image.aspect': 'auto',
    }


def apply_publication_style(style_name: str = 'default') -> None:
    """
    Apply a preconfigured publication style.

    Parameters
    ----------
    style_name : str
        - 'default': General CS publication style
        - 'ieee': IEEE Transactions / conferences (3.5 in single column)
        - 'acm': ACM sigconf / acmsmall (3.33 in single column)
        - 'usenix': USENIX (3.33 in two-column)
        - 'neurips': NeurIPS / ICLR (5.5 in textwidth)
        - 'icml': ICML (6.75 in textwidth)
        - 'minimal': Stripped clean style
        - 'presentation': Larger fonts for posters / slides
    """
    base = get_base_style()

    if style_name == 'ieee':
        base.update({
            'font.size': 8, 'axes.labelsize': 9, 'axes.titlesize': 9,
            'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7,
            'figure.figsize': (3.5, 2.4),
            'savefig.dpi': 600,
        })
    elif style_name == 'acm':
        base.update({
            'font.size': 7, 'axes.labelsize': 8, 'axes.titlesize': 8,
            'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6,
            'figure.figsize': (3.33, 2.3),
            'savefig.dpi': 600,
        })
    elif style_name == 'usenix':
        base.update({
            'font.size': 7, 'axes.labelsize': 8, 'axes.titlesize': 8,
            'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6,
            'figure.figsize': (3.33, 2.3),
            'savefig.dpi': 600,
        })
    elif style_name == 'neurips':
        base.update({
            'font.size': 9, 'axes.labelsize': 10, 'axes.titlesize': 10,
            'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
            'figure.figsize': (5.5, 3.5),
            'savefig.dpi': 600,
        })
    elif style_name == 'icml':
        base.update({
            'font.size': 9, 'axes.labelsize': 10, 'axes.titlesize': 10,
            'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
            'figure.figsize': (6.75, 4.0),
            'savefig.dpi': 600,
        })
    elif style_name == 'minimal':
        base.update({
            'axes.linewidth': 0.8,
            'xtick.major.width': 0.8, 'ytick.major.width': 0.8,
            'lines.linewidth': 2.0,
        })
    elif style_name == 'presentation':
        base.update({
            'font.size': 14, 'axes.labelsize': 16, 'axes.titlesize': 18,
            'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 12,
            'axes.linewidth': 1.5, 'lines.linewidth': 2.5,
            'lines.markersize': 8, 'lines.markeredgewidth': 1.0,
            'figure.figsize': (8.0, 6.0),
        })
    elif style_name != 'default':
        print(f"Warning: style '{style_name}' not recognized. Using 'default'.")

    plt.rcParams.update(base)
    print(f"Applied '{style_name}' publication style")


def set_color_palette(palette_name: str = 'okabe_ito') -> None:
    """
    Set a colorblind-safe matplotlib color cycle.

    Parameters
    ----------
    palette_name : str
        'okabe_ito', 'okabe_ito_4', 'wong', 'tol_bright', 'tol_muted',
        'tol_high_contrast'
    """
    palettes = {
        'okabe_ito': OKABE_ITO_COLORS,
        'okabe_ito_4': OKABE_ITO_4,
        'wong': WONG_COLORS,
        'tol_bright': TOL_BRIGHT,
        'tol_muted': TOL_MUTED,
        'tol_high_contrast': TOL_HIGH_CONTRAST,
    }
    if palette_name not in palettes:
        available = ', '.join(palettes.keys())
        print(f"Warning: palette '{palette_name}' not found. Available: {available}")
        palette_name = 'okabe_ito'

    colors = palettes[palette_name]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    print(f"Applied '{palette_name}' palette ({len(colors)} colors)")


# Per-venue specifications: (single_column_in, double_column_in, style_name).
# double_column_in is the full text width for one-column venues (NeurIPS, ICML).
VENUE_SPECS = {
    'ieee':    {'single': 3.5,  'double': 7.16, 'style': 'ieee'},
    'acm':     {'single': 3.33, 'double': 7.0,  'style': 'acm'},
    'usenix':  {'single': 3.33, 'double': 7.0,  'style': 'usenix'},
    'neurips': {'single': 5.5,  'double': 5.5,  'style': 'neurips'},
    'icml':    {'single': 6.75, 'double': 6.75, 'style': 'icml'},
    'iclr':    {'single': 5.5,  'double': 5.5,  'style': 'neurips'},
    'arxiv':   {'single': 5.5,  'double': 7.0,  'style': 'default'},
}


def configure_for_venue(venue: str, figure_width: str = 'single') -> None:
    """
    Configure matplotlib for a specific CS venue.

    Parameters
    ----------
    venue : str
        'ieee', 'acm', 'usenix', 'neurips', 'icml', 'iclr', 'arxiv'
    figure_width : str
        'single' (column-width) or 'double' (full-width)

    Examples
    --------
    >>> configure_for_venue('ieee', figure_width='single')
    >>> fig, ax = plt.subplots()  # 3.5 in wide IEEE single-column figure
    """
    venue = venue.lower()
    if venue not in VENUE_SPECS:
        available = ', '.join(VENUE_SPECS.keys())
        raise ValueError(f"Venue '{venue}' not recognized. Available: {available}")

    spec = VENUE_SPECS[venue]
    apply_publication_style(spec['style'])

    width_in = spec['single'] if figure_width == 'single' else spec['double']
    plt.rcParams['figure.figsize'] = (width_in, width_in * 0.65)

    print(f"Configured for {venue.upper()} ({figure_width}: {width_in:.2f} in wide)")


def create_style_template(output_file: str = 'publication.mplstyle') -> None:
    """Write current rcParams to a `.mplstyle` file usable with `plt.style.use()`."""
    style = get_base_style()
    with open(output_file, 'w') as f:
        f.write("# CS publication-quality matplotlib style\n")
        f.write("# Usage: plt.style.use('publication.mplstyle')\n\n")
        for key, value in style.items():
            if isinstance(value, mpl.cycler):
                colors = [c['color'] for c in value]
                f.write(f"axes.prop_cycle: cycler('color', {colors})\n")
            else:
                f.write(f"{key}: {value}\n")
    print(f"Created style template: {output_file}")


def show_color_palettes() -> None:
    """Display the bundled palettes side-by-side for visual inspection."""
    palettes = {
        'Okabe-Ito':         OKABE_ITO_COLORS,
        'Okabe-Ito (4-set)': OKABE_ITO_4,
        'Wong':              WONG_COLORS,
        'Tol Bright':        TOL_BRIGHT,
        'Tol Muted':         TOL_MUTED,
        'Tol High Contrast': TOL_HIGH_CONTRAST,
    }

    fig, axes = plt.subplots(len(palettes), 1, figsize=(8, len(palettes) * 0.6))
    if len(palettes) == 1:
        axes = [axes]
    for ax, (name, colors) in zip(axes, palettes.items()):
        ax.set_xlim(0, len(colors))
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_ylabel(name, fontsize=9, rotation=0, ha='right', va='center')
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color,
                                       edgecolor='black', linewidth=0.5))
            text_color = 'white' if i == len(colors) - 1 else 'black'
            ax.text(i + 0.5, 0.5, color, ha='center', va='center',
                    fontsize=7, color=text_color)
    fig.suptitle('Colorblind-Safe Palettes', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.show()


def reset_to_default() -> None:
    """Reset matplotlib to its built-in defaults."""
    mpl.rcdefaults()
    print("Reset to matplotlib defaults")


if __name__ == "__main__":
    print("Matplotlib Style Presets for CS Publications")
    print("=" * 50)

    print("\nAvailable styles: default, ieee, acm, usenix, neurips, icml, minimal, presentation")
    print("Available palettes: okabe_ito, okabe_ito_4, wong, tol_bright, tol_muted, tol_high_contrast")
    print("Available venues: ieee, acm, usenix, neurips, icml, iclr, arxiv")

    print("\nExample:")
    print("  from style_presets import configure_for_venue, set_color_palette")
    print("  configure_for_venue('ieee', figure_width='single')")
    print("  set_color_palette('okabe_ito_4')")

    import numpy as np
    apply_publication_style('ieee')
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    x = np.linspace(0, 10, 50)
    for i in range(4):
        ax.plot(x, np.sin(x + i * 0.5) + i, marker='o', markersize=3,
                label=f'series {i+1}')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Value (a.u.)')
    ax.legend()
    plt.tight_layout()
    plt.show()

    show_color_palettes()
