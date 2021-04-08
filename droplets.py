from process_pixel import process_pixel
import asyncio
from random import randint, uniform
from helpers import hls_to_color

class Droplet:
  pos = 0
  color = 0
  expansion = 0
  num_pixels = 0

  def __init__(self, num_pixels):
      self.num_pixels = num_pixels
      self.pos = randint(num_pixels / 4, num_pixels / 4 * 3)
      self.color = hls_to_color(uniform(0, 1), uniform(0.4, 0.6), 1)

  def tick(self):
    self.expansion += 2

  def draw(self, strip):
    for i in range(self.pos - self.expansion, self.pos + self.expansion):
      strip.setPixelColor(i, process_pixel(self.color))

  def filled(self):
    return self.expansion >= self.pos and self.expansion + self.pos >= self.num_pixels

async def droplets(strip, wait_ms=20):
  num_pixels = strip.numPixels()

  droplets: list[Droplet] = [Droplet(num_pixels)]
  while True:
    for droplet in droplets:
      droplet.tick()
      droplet.draw(strip)

    if len(droplets) > 0 and droplets[0].filled():
      droplets = droplets[1:]

    if len(droplets) < 4 and randint(0, 40) == 0:
      droplets += [Droplet(num_pixels)]

    strip.show()

    await asyncio.sleep(wait_ms / 1000.0)
