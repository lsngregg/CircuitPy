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
    
- 8/7/21 -
 
 Need to add in code for displaying sensor readings.
   
"""

import board            # Currently set to the Feather RP2040
import digitalio        # lib for digital pins
import time             # Seems important
import displayio
import terminalio


"""
Initialize the i2c components

    I still have no idea how to setup two different
        i2c components

"""

# This is for the OLED
i2c = board.I2C()                                   # create i2c object
display_bus = displayio.I2CDisplay(i2c)             # set the display to the i2c

# How do for TSL?

"""
Initialize the display

End goal is to display the Lux/IR/and maybe raw luminosity
Bonus: add a battery level at top right corner
Bouns Round 2: utilize the display buttons to maybe cycle
    through other sensor data

"""

from adafruit_display_text import label
import adafruit_displayio_sh1107

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)


#Make display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle in black
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Make text areas for displaying senssor info
lux_area = 


while True:
    pass
