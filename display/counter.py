# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, miscellaneous stuff and some white text.

Hacked up by Ellison Gregg
"""


import time
import board
import displayio
import terminalio
import adafruit_tsl2591
import adafruit_displayio_sh1107


from adafruit_display_text import label


displayio.release_displays()
# oled_reset = board.D9

# Define display I2C address
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# tossing in the i2c init for the sensor just to see what happens
tsl = adafruit_tsl2591.TSL2591(i2c)

# Initalize display
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)

# define "splash"
splash = displayio.Group()

counter = label.Label(terminalio.FONT, text="Count: ", x=5, y=8)

splash.append(counter)
display.show(splash)

count = 1


while True:
   counter.text = str(count)    # can't append int to label
   count += 1
   time.sleep(1)