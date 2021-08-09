"""
So this is where we're going to put together the "main" code for utilizing
    the display and the light sensor. End goal is to just output sensor
    readings to the display. This will serve as ground work for making
    a light meter for use with cameras.

 --- Components ---
1) Adafruit RP2040 Feather
2) Adafruit 128x64 OLED Featherwing
3) Adafruit TSL2591 Light Sensor

- 8/8/21 -

Added in CPU temp, CPU Frequency
Even added in units to the end of the readings

started setting up DIO pins.
I want to see if I can get the buttons on the display to
"change pages." 

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
tsl = adafruit_tsl2591.TSL2591(i2c)

# Define the digital IO pins
pb_a = digitalio.DigitalInOut(board.A1)
pb_b = digitalio.DigitalInOut(board.A2)
pb_c = digitalio.DigitalInOut(board.A3)

# set pins to pull-up
pb_a.switch_to_input(pull=digitalio.Pull.UP)
pb_b.switch_to_input(pull=digitalio.Pull.UP)
pb_c.switch_to_input(pull=digitalio.Pull.UP)

"""
Initialize the display & Define label(text) areas

End goal is to display the Lux/IR/and maybe raw luminosity

    Bonus: add a battery level at top right corner

    Bouns Round 2: utilize the display buttons to maybe cycle
        through other sensor data

"""
# define the neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Initalize display
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)

# define "page1"
page1 = displayio.Group()
display.show(page1)

# Define strings for display
lux_text = "Lux: "
ir_text = "IR: "
counts_text = "Raw Counts: "
cpu_temp_text = "CPU Temp: "
cpu_freq_text = "CPU Freq: "

# Make text areas for displaying senssor info
#   Lux, IR, Raw Counts
lux_area = label.Label(terminalio.FONT, text=lux_text, x=0, y=4)
ir_area = label.Label(terminalio.FONT, text=ir_text, x=0, y=14)
counts_area = label.Label(terminalio.FONT, text=counts_text, x=0, y=24)
cpuTemp_area = label.Label(terminalio.FONT, text=cpu_temp_text, x=0, y=34)
cpuFreq_area = label.Label(terminalio.FONT, text=cpu_freq_text, x=0, y=44)

page1.append(lux_area)
page1.append(counts_area)
page1.append(ir_area)
page1.append(cpuTemp_area)
page1.append(cpuFreq_area)

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

pixel.fill((0, 0, 255))     # Change neopixel to blue before while

while True:
    if not pb_b.value:

        pixel.fill(((0, 255, 0)))           # Change neopixel to green
        pixel.brightness = 0.1              # Dim led to signal begin of DAQ

        # Read-in lux/IR/and visible counts
        lux = int(tsl.lux)          # Data is read-in as a float, so convert to int
        ir = tsl.infrared
        counts = tsl.full_spectrum

        # Tossing in CPU temp read for S's & G's
        cpuTemp = int(microcontroller.cpu.temperature)

        # Also adding in CPU Freq
        cpuFreq = microcontroller.cpu.frequency

        # Update display
        # This involves converting int's to srt in order to add them
        #   to the text strings on the display
        lux_area.text = lux_text + str(lux)
        ir_area.text = ir_text + str(ir)
        counts_area.text = counts_text + str(counts)
        cpuTemp_area.text = cpu_temp_text + str(cpuTemp) + "C"
        cpuFreq_area.text = cpu_freq_text + str(cpuFreq)[:3] + "Hz"

    else:

        # LED is brighter when "out of loop"
        pixel.brightness = 0.2
        # Monitor for button press fast AF
        time.sleep(0.1)
