from rpi_ws281x import Color
import asyncio
from colorsys import rgb_to_hls, hls_to_rgb

async def off(strip):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
