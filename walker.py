from rpi_ws281x import Color
import asyncio

async def walker(strip, wait_ms=20):
  num_pixels = strip.numPixels()
  while True:
    for color in [
      Color(255, 0, 0), 
      Color(255, 15, 207),
      Color(0, 0, 255),
      Color(255, 115, 0),
      Color(15, 255, 223),
    ]:
      for j in range(num_pixels + 20, -20, -1):
        for i in range(num_pixels):
          strip.setPixelColor(i, 0)
        for k in range(j, j + 20):
          strip.setPixelColor(k, color)
        strip.show()
      await asyncio.sleep(wait_ms / 1000.0)
