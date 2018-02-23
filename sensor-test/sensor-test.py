import RPi.GPIO as io
from time import sleep

io.setmode(io.BCM)

io.setup(21, io.IN)

while(true):
    print(io.INPUT(21))
    sleep(1)

