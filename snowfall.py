from process_pixel import process_pixel
from rpi_ws281x import Color
import asyncio
from random import randint

class Snowflake:
  pos = 0
  speed = 0.6

  def __init__(self, speed: float):
    self.speed = speed

  def tick(self):
    self.pos += self.speed

  def position(self):
    return round(self.pos)

async def snowfall(strip, wait_ms=20):
  snowflakes = []
  num_pixels = strip.numPixels()
  skip = 4
  while True:
    for i in range(num_pixels):
      strip.setPixelColor(i, process_pixel(0))
    for snowflake in snowflakes:
      pos = round((num_pixels - snowflake.position()) / skip) * skip
      strip.setPixelColor(pos, process_pixel(Color(255, 255, 255)))
      strip.setPixelColor(pos + skip, process_pixel(Color(255, 255, 255)))
      snowflake.tick()
    strip.show()

    snowflakes = list(filter(lambda s: s.position() <= num_pixels, snowflakes))

    if randint(0, 40) == 0:
      snowflakes += [Snowflake(randint(300, 1500)/1000)]

    # print(len(snowflakes))

    await asyncio.sleep(wait_ms / 1000.0)
