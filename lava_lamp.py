from process_pixel import process_pixel
from rpi_ws281x import Color
import asyncio
from helpers import hls_to_color

async def lava_lamp(strip, wait_ms=50, iterations=1):
    print("timed rainbow")
    for j in range(0, iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, process_pixel(hls_to_color(j / 100, 0.5 - (i / strip.numPixels() / 2), 1)))
        strip.show()
        await asyncio.sleep(wait_ms / 1000.0)
        print(j)
