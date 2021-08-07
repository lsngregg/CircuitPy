# this is a comment

import board            # Currently set to the Feather RP2040
import digitalio        # No idea
import time             # Seems important

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

## I have no idea what's going on here. Probably turning an led on and off
while True:
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(0.5)

# Gonna play around with the display now