import asyncio
from Adafruit_PCA9685 import PCA9685
from components import InputComponent
from settings import *


def test_sensor(voltage):
    sens1 = SensorComponent('test' , 0, SENSOR_0_COEFFICIENTS)
    print(sens1._convert_to_distance(1.5))


if __name__ == '__main__':
    test_sensor(1.5)
