#!/usr/bin/env python3

import time
from rpi_ws281x import PixelStrip, Color
from colorsys import rgb_to_hls, hls_to_rgb

# LED strip configuration:
LED_COUNT = 300        # Number of LED pixels.
LED_PIN = 13          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
    
def rgb_to_color(r: float, g: float, b: float) -> int:
    return Color(int(255 * r) & 255, int(255 * g) & 255, int(255 * b) & 255)

def hls_to_color(h, l, s):
    (r, g, b) = hls_to_rgb(h, l, s)
    return rgb_to_color(r, g, b)

def lavaLamp(strip, wait_ms=50, iterations=1):
    print("timed rainbow")
    for j in range(0, iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, hls_to_color(j / 100, 0.5 - (i / strip.numPixels() / 2), 1))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    try:
        colorWipe(strip, Color(0, 0, 0), 0)
        while True:
            # colorWipe(strip, Color(0, 0, 0), 0)
            lavaLamp(strip, 10, 600)
            # print('Color wipe animations.')
            # colorWipe(strip, Color(255, 60, 0))  # Red wipe
            # colorWipe(strip, Color(0, 255, 0))  # Green wipe
            # colorWipe(strip, Color(0, 0, 255))  # Blue wipe
            # print('Theater chase animations.')
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127, 0, 0))  # Red theater chase
            # theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
            # print('Rainbow animations.')
            # theaterChaseRainbow(strip)
            # rainbow(strip)
            # rainbowCycle(strip, 10, 20)

    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)
