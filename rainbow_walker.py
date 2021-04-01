from rpi_ws281x import Color
import asyncio
from helpers import hls_to_color

async def rainbow_walker(strip, wait_ms=10):
  hue = 0
  num_pixels = strip.numPixels()
  badge_width = 60
  while True:
    for r in [
      range(num_pixels - badge_width),
      range(num_pixels - badge_width, 0, -1)
    ]:
      for j in r:
        for i in range(num_pixels):
          strip.setPixelColor(i, Color(0, 0, 0))
        for k in range(j, j + badge_width):
          strip.setPixelColor(k, hls_to_color(hue, 0.5, 1.0))
        strip.show()
        hue += 0.001
        if hue > 1:
          hue = 0
      await asyncio.sleep(wait_ms / 1000.0)
