import board
import busio
import time
import displayio
import adafruit_ssd1327
from adafruit_display_text.label import Label

displayio.release_displays()
arial12 = bitmap_font.load_font("/fonts/Arial-12.pcf")
arial18 = bitmap_font.load_font("/fonts/Arial-18.pcf")


iic = board.I2C()
iic_db = displayio.I2CDisplay(iic, device_address=0x3C)

display = adafruit_ssd1327.SSD1327(iic_db, width=128, height=128)
splash = displayio.Group(max_size=10)

tempC = Label(arial18, x=5, y=32, text="---.0 C")
splash.append(tempC)
display.show(splash)

n = 10
while True:
    tempC.text=n
    n += 1
    if n > 100: n = 0
    time.sleep(5)