from rpi_ws281x import Color

opacity = 1.0

def set_global_opacity(o: float):
  global opacity
  opacity = o

def get_global_opacity() -> float:
  global opacity
  return opacity

def process_pixel(pixel: int) -> int:
  global opacity
  red = (pixel >> 16) & 0xFF
  green = (pixel >> 8) & 0xFF
  blue = pixel & 0xFF

  return Color(int(opacity * red), int(opacity * green), int(opacity * blue))