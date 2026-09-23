"""
Color palettes for CS publications.

The default is the semantic palette from figures4papers
(https://github.com/ChenLiu-1996/figures4papers): deep blue for the proposed
method, green and red families for related and contrasting baselines, grays
for references. Okabe-Ito and the Tol sets stay available for figures that
need strict colorblind safety without redundant encoding.

Drops biology-specific palettes (fluorophores, DNA bases, microscopy channels)
from the upstream skill — those don't apply to CS figures.

Usage:
    from color_palettes import F4P, F4P_CYCLE, apply_palette
    apply_palette('f4p')
"""

# figures4papers semantic palette (default). Roles, not a free cycle:
# blue = ours, green family = related methods / positive variants,
# red family = contrasting baselines, grays = references and background.
F4P = {
    'blue_main':      '#0F4D92',  # the proposed method
    'blue_secondary': '#3775BA',  # ablation ramps of the proposed method
    'green_1':        '#DDF3DE',
    'green_2':        '#AADCA9',
    'green_3':        '#8BCF8B',
    'red_1':          '#F6CFCB',
    'red_2':          '#E9A6A1',
    'red_mid':        '#D88F8A',
    'red_strong':     '#B64342',
    'teal':           '#42949E',
    'violet':         '#9A4D8E',
    'neutral':        '#CFCECE',  # bar fill only; too light for lines
    'gray':           '#767676',
    'gray_dark':      '#4D4D4D',
    'highlight':      '#FFD700',  # a single callout, never a series
}

# Line/marker cycle ordered by colorblind separation. Under simulated
# deuteranopia, protanopia and tritanopia the first four keep a pairwise
# CAM02-UCS distance >= 21; gray as the fifth drops the minimum to 12.8, so
# from the fifth series on the marker and line style must carry the
# distinction. Violet is left out: it sits 8.7 from blue_main under
# protanopia, too close to the color that means "ours".
F4P_CYCLE = ['#0F4D92', '#B64342', '#8BCF8B', '#42949E', '#767676']

# Family ramps, light to dark. Put the strongest member of a family nearest to
# the proposed method. Under deuteranopia the light reds (red_1, red_2,
# red_mid) sit 4.4-8.1 from greens of similar lightness, so a figure that
# shows a light red next to any green hatches or dashes the reds. red_strong
# stays >= 28 from every green.
F4P_GREENS = ['#DDF3DE', '#AADCA9', '#8BCF8B']
F4P_REDS = ['#F6CFCB', '#E9A6A1', '#B64342']

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


def apply_palette(palette_name='f4p'):
    """
    Apply a palette to matplotlib's default color cycle.

    Parameters
    ----------
    palette_name : str
        'f4p' (default), 'okabe_ito', 'okabe_ito_4', 'okabe_ito_2', 'wong',
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
        'f4p':               F4P_CYCLE,
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


def get_palette(palette_name='f4p'):
    """Return a palette as a list of hex codes (without applying it)."""
    palettes = {
        'f4p':               F4P_CYCLE,
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
    print("Palettes for CS figures:")
    print(f"  figures4papers:      {len(F4P_CYCLE)} colors (default cycle)")
    print(f"  Okabe-Ito:           {len(OKABE_ITO_LIST)} colors")
    print(f"  Okabe-Ito 4-subset:  {len(OKABE_ITO_4)} colors (B/W-friendly)")
    print(f"  Okabe-Ito 2-subset:  {len(OKABE_ITO_2)} colors (baseline vs ours)")
    print(f"  Wong:                {len(WONG)} colors")
    print(f"  Tol Bright:          {len(TOL_BRIGHT)} colors")
    print(f"  Tol Muted:           {len(TOL_MUTED)} colors")
    print(f"  Tol Light:           {len(TOL_LIGHT)} colors")
    print(f"  Tol High Contrast:   {len(TOL_HIGH_CONTRAST)} colors")
    print("\nfigures4papers roles (default):")
    for name, hexv in F4P.items():
        print(f"  {name:15s}: {hexv}")
