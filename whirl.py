from process_pixel import process_pixel
from rpi_ws281x import Color
import asyncio
from helpers import hls_to_color

async def whirl(strip, wait_ms=10):
  num_pixels = strip.numPixels()
  segment_length = 70
  while True:
    for j in range(segment_length):
      for i in range(num_pixels):
        index = (i+j) % segment_length
        color = hls_to_color(index / 150, 0.50, 1) if index < 12 else Color(0, 0, 0)
        strip.setPixelColor(i, process_pixel(color))
      strip.show()
      await asyncio.sleep(wait_ms / 1000.0)
