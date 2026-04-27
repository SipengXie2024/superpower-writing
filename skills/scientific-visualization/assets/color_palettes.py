"""
Colorblind-friendly color palettes for CS publications.

Drops biology-specific palettes (fluorophores, DNA bases, microscopy channels)
from the upstream skill — those don't apply to CS figures.

Usage:
    from color_palettes import OKABE_ITO_LIST, apply_palette
    apply_palette('okabe_ito')
"""

# Okabe-Ito palette (Okabe & Ito, 2008): the most widely-recommended
# colorblind-safe categorical palette. Distinguishable under deuteranopia,
# protanopia, and tritanopia.
OKABE_ITO = {
    'orange':         '#E69F00',
    'sky_blue':       '#56B4E9',
    'bluish_green':   '#009E73',
    'yellow':         '#F0E442',
    'blue':           '#0072B2',
    'vermillion':     '#D55E00',
    'reddish_purple': '#CC79A7',
    'black':          '#000000',
}

OKABE_ITO_LIST = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                  '#0072B2', '#D55E00', '#CC79A7', '#000000']

# 4-color subset that survives B/W print well; recommended default for paper
# figures with ≤ 4 series (baseline / ours / ablation A / ablation B).
OKABE_ITO_4 = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']

# 2-color subset for baseline-vs-ours plots
OKABE_ITO_2 = ['#56B4E9', '#D55E00']

# Wong palette (Nature Methods, 2011)
WONG = ['#000000', '#E69F00', '#56B4E9', '#009E73',
        '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

# Paul Tol palettes (https://personal.sron.nl/~pault/)
TOL_BRIGHT = ['#4477AA', '#EE6677', '#228833', '#CCBB44',
              '#66CCEE', '#AA3377', '#BBBBBB']

TOL_MUTED = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933',
             '#DDCC77', '#CC6677', '#882255', '#AA4499']

TOL_LIGHT = ['#77AADD', '#EE8866', '#EEDD88', '#FFAABB',
             '#99DDFF', '#44BB99', '#BBCC33', '#AAAA00', '#DDDDDD']

TOL_HIGH_CONTRAST = ['#004488', '#DDAA33', '#BB5566']

# Sequential colormaps suitable for single-variable continuous CS data
SEQUENTIAL_COLORMAPS = [
    'viridis',   # default, perceptually uniform, grayscale-safe
    'cividis',   # optimized for protanopia / deuteranopia
    'plasma',    # perceptually uniform, more saturated
    'inferno',   # high-contrast, dark-background
    'magma',     # subtle, less saturated than inferno
    'YlGnBu',    # multi-hue sequential
    'Blues',     # single-hue
]

# Diverging colormaps (data with meaningful center, e.g., speedup, correlation)
DIVERGING_COLORMAPS_SAFE = [
    'RdBu_r',    # standard for correlation matrices, centered at 0
    'PuOr',      # excellent colorblind contrast
    'BrBG',      # brown-blue-green, good colorblind contrast
    'coolwarm',  # blue-white-red, slightly less colorblind-safe but intuitive
]

# Diverging maps to AVOID (red-green endpoints fail for ~ 8 % of male readers)
DIVERGING_COLORMAPS_AVOID = [
    'RdGn',
    'RdYlGn',
]


def apply_palette(palette_name='okabe_ito'):
    """
    Apply a colorblind-safe palette to matplotlib's default color cycle.

    Parameters
    ----------
    palette_name : str
        'okabe_ito' (default), 'okabe_ito_4', 'okabe_ito_2', 'wong',
        'tol_bright', 'tol_muted', 'tol_light', 'tol_high_contrast'

    Returns
    -------
    list
        The applied list of color hex codes.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed")
        return None

    palettes = {
        'okabe_ito':         OKABE_ITO_LIST,
        'okabe_ito_4':       OKABE_ITO_4,
        'okabe_ito_2':       OKABE_ITO_2,
        'wong':              WONG,
        'tol_bright':        TOL_BRIGHT,
        'tol_muted':         TOL_MUTED,
        'tol_light':         TOL_LIGHT,
        'tol_high_contrast': TOL_HIGH_CONTRAST,
    }
    if palette_name not in palettes:
        available = ', '.join(palettes.keys())
        raise ValueError(f"Palette '{palette_name}' not found. Available: {available}")

    colors = palettes[palette_name]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    return colors


def get_palette(palette_name='okabe_ito'):
    """Return a palette as a list of hex codes (without applying it)."""
    palettes = {
        'okabe_ito':         OKABE_ITO_LIST,
        'okabe_ito_4':       OKABE_ITO_4,
        'okabe_ito_2':       OKABE_ITO_2,
        'wong':              WONG,
        'tol_bright':        TOL_BRIGHT,
        'tol_muted':         TOL_MUTED,
        'tol_light':         TOL_LIGHT,
        'tol_high_contrast': TOL_HIGH_CONTRAST,
    }
    if palette_name not in palettes:
        available = ', '.join(palettes.keys())
        raise ValueError(f"Palette '{palette_name}' not found. Available: {available}")
    return palettes[palette_name]


if __name__ == "__main__":
    print("Colorblind-friendly palettes for CS figures:")
    print(f"  Okabe-Ito:           {len(OKABE_ITO_LIST)} colors")
    print(f"  Okabe-Ito 4-subset:  {len(OKABE_ITO_4)} colors (B/W-friendly)")
    print(f"  Okabe-Ito 2-subset:  {len(OKABE_ITO_2)} colors (baseline vs ours)")
    print(f"  Wong:                {len(WONG)} colors")
    print(f"  Tol Bright:          {len(TOL_BRIGHT)} colors")
    print(f"  Tol Muted:           {len(TOL_MUTED)} colors")
    print(f"  Tol Light:           {len(TOL_LIGHT)} colors")
    print(f"  Tol High Contrast:   {len(TOL_HIGH_CONTRAST)} colors")
    print("\nOkabe-Ito (recommended default):")
    for name, hexv in OKABE_ITO.items():
        print(f"  {name:15s}: {hexv}")
