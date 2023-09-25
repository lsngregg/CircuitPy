# Make the light blink on the Pi Pico

from machine import Pin, UART
import time

#setup the onboard LED
obLed = Pin(25, Pin.OUT)
LED_state = True

#Setup red LED
redLed = Pin(28, Pin.OUT)
redLed.low()


# Alternate blinking red and onboard LED
while True:
    obLed.high()
    time.sleep(0.5)
    obLed.low()
    redLed.high()
    time.sleep(0.5)
    redLed.low()

