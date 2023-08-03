"""This program output the reading of temperature and humidity with the DHT-11 sensor connected.
"""
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
pin = 22

GPIO.setmode(GPIO.BCM)

def setup():
    global sensor
    sensor = Adafruit_DHT.DHT11
    
def loop():
    hum, tem = Adafruit_DHT.read_retry(sensor, pin)
    while True:
        if hum is not None and tem is not None:
            print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(tem,hum))
        else:
            print('Failed to get reading. Try again!')
        time.sleep(1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()