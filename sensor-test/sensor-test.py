import RPi.GPIO as io
from time import sleep
#import serial
import spidev

spi = spidev.SpiDev()
spi.open(0,0)


io.setmode(io.BCM)
io.setup(21, io.IN)

while(1):
    
    print(io.input(21))
    sleep(1)

