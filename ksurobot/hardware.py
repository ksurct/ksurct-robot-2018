
import spidev

from settings import SPI_DEVICE

spi = spidev.SpiDev()
spi.open(0, SPI_DEVICE)
spi.max_speed_hz = 500000


def build_read_command(channel):
    ''' Create the command to send to the adc '''
    base_byte = 0x8f
    return [base_byte|(channel<<4), 0, 0]

def process_response(response):
    ''' Return the first 10 bits received back from the adc after 10 zeros '''
    return (response[1]<<5) + response[2]>>3


class MAX192AEPP(object):

    @staticmethod
    def read_channel(channel):
        ''' Read from the ADC on the requested channel '''

        if channel > 7 or channel < 0:
            raise ValueError('Channel for MAX192AEPP must be between 0 and 7 (inclusive)')

        command = build_read_command(channel)
        response = spi.xfer2(command)
        return process_response(response)

def test():
    try:
        while True:
            for channel in range(0, 7):
                print(channel, MAX192AEPP.read_channel(channel))

    except KeyboardInterrupt:
        spi.close()

if __name__ == '__main__':
    test()
