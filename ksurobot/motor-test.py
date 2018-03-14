from Adafruit_PCA9685 import PCA9685

pca = PCA9685(0x70)

pca.set_pwm_freq(10)

try:
    while True:
        for x in range(2048, 4096):
            pca.set_pwm(0, 0, x)
except KeyboardInterrupt:
    pca.set_all_pwm(0, 0)
