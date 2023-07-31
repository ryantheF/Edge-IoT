import RPi.GPIO as GPIO
import time
import smbus

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins connected to the motion sensor and ultrasonic sensor
motion_pin = 17
trigger_pin = 18
echo_pin = 24

# Set the GPIO pins as INPUT and OUTPUT
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# LCD1602 I2C address
LCD_ADDR = 0x27

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line

# Define some device constants for LCD1602
LCD_CHR = 1   # Mode - Sending data
LCD_CMD = 0   # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Increased timing constants for faster measurement frequency
E_PULSE_FAST = 0.0001
E_DELAY_FAST = 0.0001

# Open I2C interface
bus = smbus.SMBus(1)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = 1 for data, 0 for command

    bits_high = mode | (bits & 0xF0) | 0x08
    bits_low = mode | ((bits << 4) & 0xF0) | 0x08

    # High bits
    bus.write_byte(LCD_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(LCD_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(LCD_ADDR, (bits | 0x04))
    time.sleep(E_PULSE)
    bus.write_byte(LCD_ADDR, (bits & ~0x04))
    time.sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def lcd_clear():
    # Clear the LCD display
    lcd_byte(0x01, LCD_CMD)

def get_distance_fast():
    # Function to read distance from the ultrasonic sensor

    # Send a trigger pulse to the ultrasonic sensor
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(E_PULSE_FAST)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Wait for the echo response
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate the distance (in cm) based on the time of flight of the ultrasonic pulse
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s

    return distance
    
def main():
    try:
        # Initialize the LCD
        lcd_byte(0x33, LCD_CMD)
        lcd_byte(0x32, LCD_CMD)
        lcd_byte(0x06, LCD_CMD)
        lcd_byte(0x0C, LCD_CMD)
        lcd_byte(0x28, LCD_CMD)
        lcd_byte(0x01, LCD_CMD)
        time.sleep(E_DELAY)

        # Initialize the counter
        count = 0
        # initialize the distance and flucuation of distance
        distance = get_distance_fast()
        # Get distance from the ultrasonic sensor
        distance_fluc = 100
        while True:               
            if 2 < distance < 60 and distance_fluc > 5:
                # Distance range in cm, adjust as needed              
                count += 1
                lcd_string("Motion Detected!", LCD_LINE_1)
                lcd_string(f"Count: {count}", LCD_LINE_2)
                print(f"Person passed by. Total count: {count}")
            else:
                lcd_clear()
                lcd_string("No Motion", LCD_LINE_1)
                
            old_distance = float(distance)  #Record current distance in a new variable
            time.sleep(1)  # Wait for 1 seconds before checking again
            distance = get_distance_fast()  #Re-read distance from the sensor
            distance_fluc = abs(distance - old_distance)  #Update distance fluctuation
    except KeyboardInterrupt:
        lcd_clear()
        GPIO.cleanup()

if __name__ == "__main__":
    
    main()
