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
        #write chip select 0 low
        #io.output(8, False)
        #time.sleep(2)
        #io.output(8, False)

        # spi.writebytes([0x8F])
        # rb1 = spi.readbytes(1)
        resp = spi.xfer2([0x8f, 0, 0])
        data = (resp[1]<<5) + resp[2]>>3
        print(hex(resp[0]), hex(resp[1]), hex(resp[2]))
        print(data)

        time.sleep(.1) # sleep for 0.25 seconds

except KeyboardInterrupt: # Ctrl+C pressed, so
    spi.close() # … close the port before exit
#end try
