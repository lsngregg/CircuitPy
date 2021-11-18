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
# Manual list of apetures, speeds and ISOs at 1/3 stop increments.
fstops = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.5, 2.8, 3.2, 3.5, 4, 4.5, 5.0, 5.6, 6.3, 7.1, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22, 27, 32, 38, 45, 54, 64, 76, 91, 108]
shutterSpeeds = [1/8000, 1/6400, 1/5000, 1/4000, 1/3200, 1/2500, 1/2000, 1/1600, 1/1250, 1/1000, 1/800, 1/640, 1/500, 1/400, 1/320, 1/250, 1/200, 1/160, 1/125, 1/100, 1/80, 1/60, 1/50, 1/40, 1/30, 1/25, 1/20, 1/15, 1/13, 1/10, 1/8, 1/6, 1/5, 1/4, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.3, 1.6, 2, 2.5, 3.2, 4, 5]
isos = [50, 100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6400, 12800, 25600]



def getMeasurement():
    global lux_value
    global lux_value_area
    global ISO_text
    global f_stop_text
    global shutter_text
    global shutter_value
    global ev_value
    

    # Read-in lux from sensor
    lux = int(sensor.lux)                           # Data is read-in as a float, so convert to int
    lux_value_area.text = lux_value + str(lux)      # Add text to the text area on screen

    # testing adding array value to display



"""

Main page routine?

"""

def MAIN_PAGE():
    global lux_value
    global lux_value_area
    #change neopixel to blue to know we've hit "main"
    pixel.fill(((0, 0, 255)))

    Main_Page = displayio.Group()

# Draw a line where OLED is broken
    line1 = displayio.Bitmap(64, 1, 1)
    line1_color = displayio.Palette(1)
    line1_color[0] = 0xFFFFFF
    line1area = displayio.TileGrid(line1, pixel_shader=line1_color, x=1, y=45)
    Main_Page.append(line1area)

# line under iso & f-stop
    line2 = displayio.Bitmap(64, 1, 1)
    line2_color = displayio.Palette(1)
    line2_color[0] = 0xFFFFFF
    line2area = displayio.TileGrid(line2, pixel_shader=line2_color, x=1, y=74)
    Main_Page.append(line2area)

# line under shutter-speed
    line3 = displayio.Bitmap(64, 1, 1)
    line3_color = displayio.Palette(1)
    line3_color[0] = 0xFFFFFF
    line3area = displayio.TileGrid(line3, pixel_shader=line3_color, x=1, y=102)
    Main_Page.append(line3area)
  
# Define strings for display (Main_Page)
    ISO_text = "ISO: XXXX"
    f_stop_text = "f/X.X"
    shutter_text = "T:"
    shutter_value = "X/XXXX"
    ev_value = "EV: XX.X"
    lux_value = "Lux: "

# Make text areas for displaying senssor info
#   ISO, F-stop, Shutter-speed
    ISO_area = label.Label(terminalio.FONT, text=ISO_text, x=2, y=52)
    f_stop_area = label.Label(terminalio.FONT, text=f_stop_text, x=2, y=66)

# Seperate areas for just the letter "T" and then the actual shutter speed
    shutter_text_area = label.Label(terminalio.FONT, text=shutter_text, x=2, y=80)
    shutter_value_area = label.Label(terminalio.FONT, text=shutter_value, x=2, y=94)

    ev_value_area = label.Label(terminalio.FONT, text=ev_value, x=2, y=108)
    lux_value_area = label.Label(terminalio.FONT, text=lux_value, x=2, y=118)


# add or "append" text to the areas
    Main_Page.append(ISO_area)
    Main_Page.append(f_stop_area)
    Main_Page.append(shutter_text_area)
    Main_Page.append(shutter_value_area)
    Main_Page.append(lux_value_area)
    Main_Page.append(ev_value_area)

# Draw the display on the display
    display.show(Main_Page)

def pixel_red():
    pixel.fill(((255,0,0)))

#----------------------------------------------------------------------------------------------------

# Start off by calling "MAIN_PAGE" to draw our initial text

MAIN_PAGE()


"""
I would very much like for this to work where:

- "Tap" B for a measurement update
- Hold B to initiate a "selection mode"
- Use A and C to move up/down in a list of selections
- Tap B to confirm selection

"""

# define a "selection" boolean
sel = True

# while selection is "True"
while sel == True:
    if not pb_b.value:
        
        #change neopixel to green on button press
        pixel.fill(((0, 255, 0)))

        # would very much like to implememnt a "change on hold" fn here

        
        # Call measurement routine which updates display "labels"
        getMeasurement()

        #change neopixel to xxx after fn call
        pixel.fill(((0, 64, 255)))

    else:
        time.sleep(0.3)
