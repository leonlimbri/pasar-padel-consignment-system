"""assets/colors.py
Generates Mantine-compatible 10-step color scales for the app theme.

Each primary color is defined as an RGB tuple. Two theme dicts are produced:
  - theme_colors_light: lightest → darkest
  - theme_colors_dark:  reversed (darkest → lightest), for dark mode
"""

from colorsys import rgb_to_hls, hls_to_rgb


def generate_scale_from_primary(rgb, light_diff: float = 0.8):
    """Generate a 10-step light → dark hex color scale from a single RGB color.

    Args:
        rgb:        Base color as an (R, G, B) tuple with values 0–255.
        light_diff: How aggressively lightness spreads across the 10 steps.
                    Higher = wider contrast range.

    Returns:
        A list of 10 hex color strings, from lightest to darkest.
    """
    def clamp(x):
        return max(0, min(1, x))

    def rgb_to_hex(r, g, b):
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    h, l, s = rgb_to_hls(*[x / 255 for x in rgb])

    # Build 10 lightness steps spread around the base lightness
    lightness_values = [l * (1 - i * light_diff / 10) for i in range(-4, 6)]
    colors = [rgb_to_hex(*hls_to_rgb(h, clamp(lv), s)) for lv in lightness_values]

    return colors


# ── Primary color definitions (R, G, B) ──────────────────────────────────────
primaries = {
    "first":  (0,   90,  70),    # army green
    "second": (203, 217, 222),   # light gray-blue
    "third":  (242, 204, 22),    # yellow
    "fourth": (29,  80,  162),   # blue
    "fifth":  (195, 62,  71),    # red
    "sixth":  (224, 182, 143),   # beige
    "gray":   (210, 210, 210),   # gray
}

# ── Build light and dark theme color maps ─────────────────────────────────────
theme_colors_light = {
    name: generate_scale_from_primary(rgb)
    for name, rgb in primaries.items()
}

theme_colors_dark = {
    name: list(reversed(colors))
    for name, colors in theme_colors_light.items()
}
