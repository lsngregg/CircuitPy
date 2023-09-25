'''

Ki Pro Ultra Record Control with Pi Pico
Author: Ellison Gregg
Date: 9.25.2023

Operate Aja Ki Pro recorder using GPIO input on Pi Pico
    to send RS422 start/stop commands to Aja SDI Recorder

Utilizes MAX485 module and UART

Red Means Recording

'''

from machine import UART, Pin
import time


#setup the onboard LED
obLed = Pin(25, Pin.OUT)
obLed.high()

#Setup red LED
redLed = Pin(28, Pin.OUT)
redLed.low()

# Setup input pin for Recording control
#   High = recording
#   Low = stop

# Init UART interface for RS422
#   RS422/Sony 9-pin
uart0 = UART(0, baudrate=38400, tx=Pin(0), rx=Pin(1))

record = 0x2002
stop = 0x2000

uart0.write(record)

print('RS422 send test...')

time.sleep(0.1)

while True:
    time.sleep(3)
    redLed.toggle() 
    print ("recording")