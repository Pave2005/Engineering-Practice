import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setup(led, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    out_val = 0
    n = 0
    for i in range(len (dac)):
        row2 = 2**(len(dac) - i - 1)
        n = out_val + row2
        dac_val = dec2bin(n)
        GPIO.output(dac, dac_val)
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val == 0:
            out_val = n
    return out_val

def Volume (val):
    val = int(val/256*10)
    arr = [0]*8
    for i in range (val - 1):
        arr[i] = 1
    return arr

try:
    while True:
        i = adc()
        voltage = i * 3.3 / 256.0
        if i: 
            print("{:.2f}V".format(voltage))
            volume_val = Volume (i)
            GPIO.output (led, volume_val)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")
    