from aiohttp import web
import asyncio
from rpi_ws281x import PixelStrip

from off import off

from lava_lamp import lava_lamp
from lighthouse import lighthouse
from rainbow_walker import rainbow_walker
from snowfall import snowfall
from starry_night import starry_night
from walker import walker
from whirl import whirl

# LED strip configuration:
LED_COUNT = 300        # Number of LED pixels.
LED_PIN = 13          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53

task = None
strip = None

scenes = [
    lava_lamp,
    lighthouse,
    rainbow_walker,
    snowfall,
    starry_night,
    walker,
    whirl
]

scene_names = list(map(lambda s: s.__name__, scenes))

async def run_scene(request):
    scene_name = request.path[1:]
    try:
        index = scene_names.index(scene_name)
    except ValueError:
        return web.Response(status=404)

    print('running {scene_name}'.format(scene_name=scene_name))

    scene = scenes[index]

    global task
    if task != None:
        task.cancel()

    task = asyncio.create_task(scene(strip))

    return web.Response()

async def scene_list(request):
    return web.json_response(scene_names)

async def cancel_task(request):
    print("off")
    global task
    if (task != None):
        task.cancel()
    task = None
    await off(strip)
    return web.Response()

if __name__ == '__main__':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    print('go')
    # asyncio.run(starry_night(strip))

    app = web.Application()

    app.router.add_get('/list', scene_list)
    app.router.add_post('/off', cancel_task)

    for name in scene_names:
        app.router.add_post('/{name}'.format(name=name), run_scene)

    web.run_app(app)
