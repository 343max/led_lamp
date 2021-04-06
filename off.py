import asyncio
from process_pixel import get_global_opacity, process_pixel, set_global_opacity

def off(strip):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, process_pixel(0))
        strip.show()

async def off_animated(strip):
    opacity = get_global_opacity()

    for i in range(10, 0, -1):
        set_global_opacity(opacity / 10 * i)
        await asyncio.sleep(0.05)
    
    off(strip)
    set_global_opacity(opacity)