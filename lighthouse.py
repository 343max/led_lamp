from process_pixel import process_pixel
from rpi_ws281x import Color
import asyncio

async def lighthouse(strip, wait_ms=400):
  num_pixels = strip.numPixels()
  while True:
    for color in [
      Color(255, 0, 0), 
      Color(255, 15, 207),
      Color(0, 0, 255),
      Color(255, 115, 0),
      Color(15, 255, 223),
    ]:
      skip = 4
      for j in range(skip):
        for i in range(num_pixels):
          c = color if (i + j) % skip == 0 else Color(0, 0, 0)
          strip.setPixelColor(i, process_pixel(c))
        strip.show()
        await asyncio.sleep(wait_ms / 1000.0)
