from math import sqrt
from process_pixel import process_pixel
from typing import List
from rpi_ws281x import Color
import asyncio
from random import uniform, randint
from pprint import pprint

# adapted from https://github.com/FastLED/FastLED/blob/master/src/colorutils.cpp#L465
def heatColor(temp: float):
  temp = min(3, temp * 3)
  if temp >= 2:
    return Color(255, 255, int((temp - 2) * 255))
  elif temp >= 1:
    return Color(255, int((temp - 1) * 255), 0)
  else:
    return Color(int(temp * 255), 0, 0)

class Spark:
  intensity = 0
  speed = 0
  decay = 0
  position = 0
  length = 0

  def __init__(self, num_pixels):
    self.intensity = uniform(0.1, 0.5)
    self.speed = randint(3, 7)
    self.decay = uniform(0.9, 0.99)
    self.position = randint(0, int(num_pixels / 6))
    self.length = randint(4, 20)

  def apply(self, heat_map: List[float]) -> List[float]:
    for pos in range(self.position, min(self.position + self.length, len(heat_map) - 1)):
      heat_map[pos] += self.intensity

    return heat_map
  
  def advance(self):
    self.intensity *= self.decay
    self.position += self.speed

  def off_screen(self, num_pixels: int) -> bool:
    return self.position > num_pixels


async def fireplace(strip, wait_ms=20):
  num_pixels = strip.numPixels()

  sparks: List[Spark] = []

  while True:
    heat = [0] * num_pixels

    for spark in sparks:
      heat = spark.apply(heat)
      spark.advance()

    sparks = list(filter(lambda s: s.off_screen(num_pixels) == False, sparks))

    if uniform(0, 1) < 0.3:
      sparks += [Spark(num_pixels)]

    for pos, h in enumerate(heat):
        strip.setPixelColor(pos, process_pixel(heatColor(h)))
    
    strip.show()
    
    await asyncio.sleep(wait_ms / 1000.0)
