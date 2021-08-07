# this is a comment

import board            # Currently set to the Feather RP2040
import digitalio        # lib for digital pins
import time             # Seems important
import displayio
import terminalio


"""
Initialize the i2c components
"""

# This is for the OLED
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# How do for TSL?

"""
Initialize the display

    from the sample code for the display

"""

from adafruit_display_text import label
import adafruit_displayio_sh1107

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

display.show()

while True:
    pass