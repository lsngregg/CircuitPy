"""
So this is where we're going to put together the "main" code for utilizing
    the display and the light sensor. End goal is to just output sensor
    readings to the display. This will serve as ground work for making
    a light meter for use with cameras.

 --- Components ---
1) Adafruit RP2040 Feather
2) Adafruit 128x64 OLED Featherwing
3) Adafruit TSL2591 Light Sensor

- 9/27/21 - 
    Started separating the pages
    Page 1 will be just Lux and IR measurements
    Page 2 will be Raw counts and CPU stats

    I need to figure out how the main loop will run.
    I also need to bite the bullet and buy just the RP2040 itself.
    I can't do interrupts, I can't do threading with the CircuitPython lib.

- 11/16/21 -
     Soldered on stacking headers
     Reprogrammed buttons on display
     Broke the display, but not completely.
     Going to figure out where i can use the display.

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
pixel.brightness = 0.3

# Initalize display
display = adafruit_displayio_sh1107.SH1107(display_bus, rotation=270, width=64, height=128,)

""""
Here is where we are defining the different pages as fucntions to call
in the "Main routine"

Page 1: This will have our "raw data" from the TSL light sensor.

Page 2: This will just be to test out a page-switching routine.
        It will include some board-level parameters for testing

"""

### PAGE 1 ####

def Page_1():

    page = displayio.Group()

    # Draw some lines to break up the screen
    line1 = displayio.Bitmap(64, 1, 1)
    line1_color = displayio.Palette(1)
    line1_color[0] = 0xFFFFFF
    line1area = displayio.TileGrid(line1, pixel_shader=line1_color, x=1, y=45)
    page.append(line1area)
  
    # Define strings for display (page1)
    lux_text = "Lux: "
    ir_text = "IR: "

    # Make text areas for displaying senssor info
    #   Lux, IR
    lux_area = label.Label(terminalio.FONT, text=lux_text, x=4, y=52)
    ir_area = label.Label(terminalio.FONT, text=ir_text, x=4, y=66)



    page.append(lux_area)
    page.append(ir_area)

            # Read-in lux/IR/and visible counts
    lux = int(sensor.lux)          # Data is read-in as a float, so convert to int
    ir = sensor.infrared

    # Update display
    # This involves converting int's to srt in order to add them
    #   to the text strings on the display
    lux_area.text = lux_text + str(lux)
    ir_area.text = ir_text + str(ir)

    # Draw the display on the display
    display.show(page)

### PAGE 2 ###

def Page_2():
    # define page2
    page = displayio.Group()
    # Draw some lines to break up the screen
    line1 = displayio.Bitmap(64, 1, 1)
    badbox = displayio.Bitmap(64,41,1)
    line1_color = displayio.Palette(1)
    line1_color[0] = 0xFFFFFF
    line1area = displayio.TileGrid(line1, pixel_shader=line1_color, x=1, y=45)
    badbox_area = displayio.TileGrid(badbox, pixel_shader=line1_color, x=0, y=0)
    page.append(line1area)
    page.append(badbox_area)

    # Define strings for page2
    counts_text = "Raw Counts: \n"
    cpu_temp_text = "CPU Temp: \n"
    cpu_freq_text = "CPU Freq: \n"

    # Make text areas for page2
    counts_area = label.Label(terminalio.FONT, text=counts_text, x=0, y=52)
    cpuTemp_area = label.Label(terminalio.FONT, text=cpu_temp_text, x=0, y=64)
    cpuFreq_area = label.Label(terminalio.FONT, text=cpu_freq_text, x=0, y=74)

    page.append(counts_area)
    page.append(cpuTemp_area)
    page.append(cpuFreq_area)

    # Tossing in CPU temp read for S's & G's
    cpuTemp = int(microcontroller.cpu.temperature)

    # Also adding in CPU Freq
    cpuFreq = microcontroller.cpu.frequency

    cpuTemp_area.text = cpu_temp_text + str(cpuTemp) + "C"
    cpuFreq_area.text = cpu_freq_text + str(cpuFreq)[:3] + "Hz"

    # Draw the display on the display
    display.show(page)


"""
Main code or runtime area

Button "B" calls Page_1
Button "A" calls Page_2

Holding either button continues to call the page function
and continutes to update until released

"""
# Array for page selection?

# clear display

# Change neopixel to blue before while-loop
pixel.fill((0, 0, 255))

while True:
    if not pb_b.value:

        pixel.fill(((0, 255, 0)))           # Change neopixel to green
        pixel.brightness = 0.1              # Dim led to signal begin of DAQ
        
        Page_1()                            # "Call" page 1 function on button press

    elif not pb_a.value:

        pixel.fill(((255, 0, 0)))
        pixel.brightness = 0.1

        Page_2()

    else:

        # LED is brighter when "out of loop"
        pixel.brightness = 0.2
        # Monitor for button press fast AF
        time.sleep(0.01)

