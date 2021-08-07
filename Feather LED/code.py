"""CircuitPython status NeoPixel rainbow example."""
import time
import board
import neopixel
try:
    from rainbowio import colorwheel
except ImportError:
    try:
        from _pixelbuf import colorwheel
    except ImportError:
        from adafruit_pypixelbuf import colorwheel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, auto_write=False)

pixel.brightness = 0.3


def rainbow(delay):
    for color_value in range(255):
        for led in range(1):
            pixel_index = (led * 256 // 1) + color_value
            pixel[led] = colorwheel(pixel_index & 255)
        pixel.show()
        time.sleep(delay)


while True:
    rainbow(0.02)