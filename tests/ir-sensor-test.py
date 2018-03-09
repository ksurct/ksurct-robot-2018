import spidev
import time
import RPi.GPIO as io
spi = spidev.SpiDev() # create spi object
spi.open(0, 0) # open spi port 0, device (CS) 1

# print(spi.bits_per_word)
# print(spi.cshigh)
# print(spi.loop)
# print(spi.lsbfirst)
spi.max_speed_hz = 500000
# print(spi.max_speed_hz)
# print(spi.mode)
# io.setmode(io.BCM)
# io.setup(8, io.OUT)



def BytesToHex(Bytes):
 return ''.join(["0x%02X " % x for x in Bytes]).strip()

try:
    while True:
        
        for channel in range(8):
            print(channel, bin(0x8f|(channel<<4)), end="\t")
            resp = spi.xfer2([0x8f|(channel<<4), 0, 0])
            
            data = (resp[1]<<5) + (resp[2]>>3)
            print(data)
        print()

        time.sleep(.1) # sleep for 0.25 seconds

except KeyboardInterrupt: # Ctrl+C pressed, so
    spi.close() # … close the port before exit
#end try
