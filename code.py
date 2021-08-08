"""
So this is where we're going to put together the "main" code for utilizing
    the display and the light sensor. End goal is to just output sensor
    readings to the display. This will serve as ground work for making
    a light meter for use with cameras.

 --- Components ---
1) Adafruit RP2040 Feather
2) Adafruit 128x64 OLED Featherwing
3) Adafruit TSL2591 Light Sensor

 Right now, i think the idea will be to initialize the display
    and make sure that is working before tyring to pull info
    from the light sensor.

- 8/8/21 -

Formatting changes

Setting up labels for displaying sensor data

testing sensor data aquisition

"""

import board                                # Currently set to the Feather RP2040
import time                                 # for sleep function
import displayio                            # OLED Coms
import terminalio                           # font?
import adafruit_tsl2591                     # For the sensor
import adafruit_displayio_sh1107            # For the OLED
from adafruit_display_text import label     # displaying text on the OLED

"""
Initialize the i2c components

1) OLED
2) TSL Sensor

"""

# This is for the OLED
# Reset/Release the display, initialize i2c bus and define the display address

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Initialize the Light sensor
tsl = adafruit_tsl2591.TSL2591(i2c)


"""
Initialize the display & Define label(text) areas

End goal is to display the Lux/IR/and maybe raw luminosity

    Bonus: add a battery level at top right corner

    Bouns Round 2: utilize the display buttons to maybe cycle
        through other sensor data

"""

# Initalize display
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)

# define "splash"
splash = displayio.Group()
display.show(splash)

lux_text = "Lux: "
ir_text = "IR: "
counts_text = "Raw Counts: "

# Make text areas for displaying senssor info
#   Lux, IR, Raw Counts
lux_area = label.Label(terminalio.FONT, text=lux_text, x=0, y=4)
ir_area = label.Label(terminalio.FONT, text=ir_text, x=0, y=14)
counts_area = label.Label(terminalio.FONT, text=counts_text, x=0, y=24)

splash.append(lux_area)
splash.append(ir_area)
splash.append(counts_area)

"""
Main code or runtime area
    This is where the sensor data aquistion will happen
    and where we will update the label text.

    Fun fact: you can't pass/append int's to labels.

1) Get the sensor data
2) Update the display
3) Wait for button press before taking another reading

(I don't know how to use the buttons yet)

"""
#

while True:

    # Read-in lux/IR/and visible counts
    lux = tsl.lux
    ir = tsl.infrared
    counts = tsl.full_spectrum

    # Update display
    lux_area.text = lux_text + str(lux)
    ir_area.text = ir_text + str(ir)
    counts_area.text = counts_text + str(counts)

    # Do every second
    time.sleep(1.0)
