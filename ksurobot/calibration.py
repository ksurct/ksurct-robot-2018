
from hardware import MAX192AEPP



def get_reading(channel, filename):

    with open(filename, 'w') as f:
        f.write('Ruler Distance, Sensor measured value\n')
        while True:
            distance = input('Enter the distance to read (q to quit): ')

            if distance == 'q':
                break

            try:
                distance = int(distance)
            except ValueError:
                print('Invalid input')
            else:
                measured = MAX192AEPP.read_channel(channel)
                f.write('{0}, {1}\n'.format(distance, measured))

