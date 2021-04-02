from rpi_ws281x import Color
import asyncio
from colorsys import hls_to_rgb
import math
from random import randint, uniform
from helpers import hls_to_color

class Droplet:
  pos = 0
  color = 0
  expansion = 1
  num_pixels = 0

  def __init__(self, num_pixels):
      self.num_pixels = num_pixels
      self.pos = randint(num_pixels / 4, num_pixels / 4 * 3)
      self.color = hls_to_color(uniform(0, 1), uniform(0.4, 0.6), 1)

  def tick(self):
    self.expansion += 2

  def draw(self, strip):
    for i in range(self.pos - self.expansion, self.pos + self.expansion):
      strip.setPixelColor(i, self.color)

  def filled(self):
    return self.expansion >= self.pos and self.expansion + self.pos >= self.num_pixels

async def droplets(strip, wait_ms=20):
  num_pixels = strip.numPixels()

  droplet = Droplet(num_pixels)
  background = 0
  while True:
    for i in range(num_pixels):
      strip.setPixelColor(i, background)
    droplet.draw(strip)
    if droplet.filled():
      background = droplet.color
      droplet = Droplet(num_pixels)
    else:
      droplet.tick()

    strip.show()

    await asyncio.sleep(wait_ms / 1000.0)
