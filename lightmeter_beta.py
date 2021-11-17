"""

The beginning of my attempt at a light meter.
- Ellison Gregg Nov 16. 2021

"""

import board                                # Currently set to the Feather RP2040
import time                                 # gives you time/sleep finctions
import digitalio                            # Controls IO pins
import microcontroller                      # lib for reading rp2040 stuff
import neopixel                             # Controlling the NeoPixel on board
import displayio                            # OLED Coms
import terminalio                           # font?
import adafruit_tsl2591                     # For the sensor
import adafruit_displayio_sh1107            # For the OLED
from adafruit_display_text import label     # displaying text on the OLED

"""
Initialize the i2c components
and GPIO for buttons

1) OLED
2) TSL Sensor

"""

# This is for the OLED
# Reset/Release the display, initialize i2c bus and define the display address

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Initialize the Light sensor
sensor = adafruit_tsl2591.TSL2591(i2c)

# Initalize display
#   This is currently setup to work with my broken OLED
display = adafruit_displayio_sh1107.SH1107(display_bus, rotation=270, width=64, height=128,)

# Define the digital IO pins
#   for built-in buttons on OLED
pb_a = digitalio.DigitalInOut(board.D9)
pb_b = digitalio.DigitalInOut(board.D6)
pb_c = digitalio.DigitalInOut(board.D5)

#  set pins to pull-up
pb_a.switch_to_input(pull=digitalio.Pull.UP)
pb_b.switch_to_input(pull=digitalio.Pull.UP)
pb_c.switch_to_input(pull=digitalio.Pull.UP)


# define the neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

"""

Exposure calculation routines

"""
def getMeasurement():
    # Read-in lux/IR/and visible counts
    lux = int(sensor.lux)          # Data is read-in as a float, so convert to int
    ir = sensor.infrared

    # Update display
    # This involves converting int's to srt in order to add them
    #   to the text strings on the display
    lux_area.text = lux_text + str(lux)
    ir_area.text = ir_text + str(ir)



"""

Main page routine?

"""

Main_Page = displayio.Group()

# Draw some lines to break up the screen
line1 = displayio.Bitmap(64, 1, 1)
line1_color = displayio.Palette(1)
line1_color[0] = 0xFFFFFF
line1area = displayio.TileGrid(line1, pixel_shader=line1_color, x=1, y=45)
Main_Page.append(line1area)
  
# Define strings for display (page1)
lux_text = "Lux: "
ir_text = "IR: "

# Make text areas for displaying senssor info
#   Lux, IR
lux_area = label.Label(terminalio.FONT, text=lux_text, x=4, y=52)
ir_area = label.Label(terminalio.FONT, text=ir_text, x=4, y=66)

Main_Page.append(lux_area)
Main_Page.append(ir_area)

# Draw the display on the display
display.show(Main_Page)
#Button press calls a "get measurement routine"

while True:
    if not pb_b.value:
        pixel.fill(((0, 255, 0)))

        getMeasurement()

    else:
        time.sleep(0.1)



