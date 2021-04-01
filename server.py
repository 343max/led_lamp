from showfall import snowfall
from aiohttp import web
import asyncio
from rpi_ws281x import PixelStrip, Color
from lava_lamp import lava_lamp
from off import off
from starry_night import starry_night
from walker import walker
from rainbow_walker import rainbow_walker

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

async def wait_task():
    try:
        i = 0
        while True:
            print("step {i}".format(i=i))
            i += 1
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Canceled")

async def run_task(request):
    global task
    if (task != None):
        task.cancel()
    task = asyncio.create_task(wait_task())
    return web.Response()

async def run_lava_lamp(request):
    global task
    if (task != None):
        task.cancel()
    task = asyncio.create_task(lava_lamp(strip, 10, 600))
    return web.Response()

async def run_snowfall(request):
    print('snowfall')
    global task
    if (task != None):
        task.cancel()
    task = asyncio.create_task(snowfall(strip))
    return web.Response()

async def run_starry_night(request):
    print('starry_night')
    global task
    if (task != None):
        task.cancel()
    task = asyncio.create_task(starry_night(strip))
    return web.Response()

async def run_walker(request):
    print('walker')
    global task
    if (task != None):
        task.cancel()
    task = asyncio.create_task(walker(strip))
    return web.Response()

async def run_rainbow_walker(request):
    print('rainbow_walker')
    global task
    if (task != None):
        task.cancel()
    task = asyncio.create_task(rainbow_walker(strip))
    return web.Response()

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
    # Create NeoPixel object with appropriate configuration.
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    print('go')
    asyncio.run(rainbow_walker(strip))

    app = web.Application()
    # app.router.add_get('/', handle)
    # app.router.add_get('/{name}', handle)

    app.router.add_post('/off', cancel_task)
    app.router.add_post('/on', run_task)
    app.router.add_post('/lava_lamp', run_lava_lamp)
    app.router.add_post('/snowfall', run_snowfall)
    app.router.add_post('/walker', run_walker)
    app.router.add_post('/rainbow_walker', run_rainbow_walker)

    web.run_app(app)

