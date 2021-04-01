from colorsys import hls_to_rgb
from rpi_ws281x import Color

def rgb_to_color(r: float, g: float, b: float) -> int:
    return Color(int(255 * r) & 255, int(255 * g) & 255, int(255 * b) & 255)

def hls_to_color(h, l, s):
    (r, g, b) = hls_to_rgb(h, l, s)
    return rgb_to_color(r, g, b)
