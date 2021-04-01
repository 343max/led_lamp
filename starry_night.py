from rpi_ws281x import Color
import asyncio
from colorsys import hls_to_rgb
import math
from random import randint, uniform
from helpers import hls_to_color

class Star:
  pos = 0
  hue = 0
  speed = 0.02
  maxLum = 1

  phase = 0

  def __init__(self, num_pixels):
      self.pos = randint(0, num_pixels)
      self.hue = uniform(0, 1)
      self.speed = uniform(0.003, 0.02)
      self.maxLum = uniform(0.5, 1.0)

  def color(self):
    return hls_to_color(self.hue, math.sin(math.pi * self.phase) * self.maxLum, 1)

  def tick(self):
    self.phase += self.speed

  def dead(self):
    return self.phase >= 1

async def starry_night(strip, wait_ms=20):
  stars = []
  num_pixels = strip.numPixels()
  skip = 4
  while True:
    for i in range(num_pixels):
      strip.setPixelColor(i, Color(0, 0, 0))
    for star in stars:
      strip.setPixelColor(star.pos, star.color())
      star.tick()
    strip.show()

    stars = list(filter(lambda s: s.dead() == False, stars))

    prob = math.sqrt(1 / (len(stars) + 1))
    if uniform(0, 2.5) < prob:
      stars += [Star(num_pixels)]
      print(len(stars))

    await asyncio.sleep(wait_ms / 1000.0)
