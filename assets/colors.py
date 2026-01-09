from colorsys import rgb_to_hls, hls_to_rgb

def generate_scale_from_primary(rgb, light_diff=0.8):
    """
    Generate a light -> dark scale around the given primary color.
    """
    def clamp(x): return max(0, min(1, x))
    def rgb_to_hex(rr, gg, bb): return f"#{int(rr*255):02x}{int(gg*255):02x}{int(bb*255):02x}"

    h, l, s = rgb_to_hls(*[x/255 for x in rgb])
    lightness_values = [l * (1-i*light_diff/10) for i in range(-4, 6, 1)]
    colors = [rgb_to_hex(*(hls_to_rgb(h, clamp(lv), s))) for lv in lightness_values]

    return colors

# =========================
# Build themes
# =========================

primaries = {
    "first":  (0, 90, 70),   # army green
    "second": (203, 217, 222),  # light gray-blue
    "third":  (242, 204, 22),   # yellow
    "fourth": (29, 80, 162),    # blue
    "fifth":  (195, 62, 71),    # red
    "sixth":  (224, 182, 143),  # beige,
    "gray": (210, 210, 210) # gray
}

theme_colors_light = {
    name: generate_scale_from_primary(rgb)
    for name, rgb in primaries.items()
}

theme_colors_dark = {
    name: list(reversed(colors))
    for name, colors in theme_colors_light.items()
}
