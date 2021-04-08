from aiohttp import web
import asyncio
from rpi_ws281x import PixelStrip
import atexit
import logging

from off import off, off_animated
from settings import store_scene, load_scene

from droplets import droplets
from fireplace import fireplace
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
    droplets,
    fireplace,
    lava_lamp,
    lighthouse,
    rainbow_walker,
    snowfall,
    starry_night,
    walker,
    whirl,
]

scene_names = list(map(lambda s: s.__name__, scenes))

def run_scene(scene_name: str):
    index = scene_names.index(scene_name)
    print('running {scene_name}'.format(scene_name=scene_name))
    scene = scenes[index]

    global task
    if task != None:
        task.cancel()

    global strip
    task = asyncio.create_task(scene(strip))

    store_scene(scene_name, True)

async def handle_run_scene(request):
    scene_name = request.path[1:]
    try:
        run_scene(scene_name)
    except ValueError:
        return web.Response(status=404)
    return web.Response()

async def handle_scene_list(request):
    return web.json_response(scene_names)

async def on_startup(app):
    global strip
    (scene_name, on) = load_scene()
    if on == True and scene_name != None:
        print("restarting {scene_name}".format(scene_name=scene_name))
        run_scene(scene_name)
    else:
        off(strip)

async def handle_off(request):
    print("off")
    global strip
    await off_animated(strip)
    global task
    if (task != None):
        task.cancel()
    task = None
    
    (scene_name, _) = load_scene()
    store_scene(scene_name, False)

    off(strip)
    return web.Response()

async def handle_on(request):
    (scene_name, _) = load_scene()
    if scene_name == None:
        scene_name = scene_names[0]
    
    run_scene(scene_name)
    return web.Response()

async def handle_status(request):
    global task
    on = '0' if task == None else '1'
    return web.Response(body=on)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    print('go')

    atexit.register(off, strip)

    app = web.Application()

    app.on_startup.append(on_startup)

    app.router.add_get('/list', handle_scene_list)
    app.router.add_get('/status', handle_status)
    app.router.add_post('/on', handle_on)
    app.router.add_post('/off', handle_off)

    for name in scene_names:
        app.router.add_post('/{name}'.format(name=name), handle_run_scene)

    web.run_app(app)
