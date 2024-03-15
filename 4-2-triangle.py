import RPi.GPIO as GPIO
from time import sleep
from matplotlib import pyplot as plt
import numpy as np

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(num):
    number = [0 for i in range(len(dac))]

    d_num = num % 256 

    bin_num = bin(d_num)

    i = -1
    while bin_num[i] != 'b':
        number[i] = int(bin_num[i])
        i -= 1
    return number

inc_flag = 1
t = 0 
x = 0

try:
    period = float(input("Input period: "))

    while True:
        GPIO.output(dac, dec2bin(x))

        if   x == 0:    inc_flag = 1
        elif x == 255:  inc_flag = 0

        x = x + 1 if inc_flag == 1 else x - 1

        sleep(period/512)
        t += 1

except ValueError:
    print("Invalide period!")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")
    