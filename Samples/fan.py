import RPi.GPIO as GPIO
import time

motor_pin = 17
def Makerobo_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(motor_pin, GPIO.OUT)

def Makerobo_motor(direction):
    if direction == 1:
        GPIO.output(motor_pin, GPIO.HIGH)
    if direction == 0:
        GPIO.output(motor_pin, GPIO.LOW)

def Makerobo_main():
    fs_directions = {'Open':1, 'STOP': 0}
    while True:
        Makerobo_motor(fs_directions['Open'])
        time.sleep(1)
        Makerobo_motor(fs_directions['STOP'])
        time.sleep(5)
    
def destroy():
    GPIO.output(motor_pin, GPIO.LOW)
    GPIO.cleanup()
    
if __name__ == '__main__':
    Makerobo_setup()
    try:
        Makerobo_main()
    except KeyboardInterrupt:
        destroy()