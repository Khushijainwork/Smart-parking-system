import time
from backend.arduino import *


def run_arduino(q):
    # Initialise connection to Arduino
    try:
        a = Arduino()
        time.sleep(3)
    except:
        return -1

    # Declare the pins
    LED_PIN = 3
    SONIC_PIN = 4
    SERVO_PIN = 2

    # Initialise the digital pin as output
    a.set_pin_mode(LED_PIN, 'O')
    a.set_pin_mode(SERVO_PIN, 'O')

    time.sleep(1)
    print("Arduino initialised")

    # Lower the barrier and activate the LED
    a.digital_write(LED_PIN, 1)
    a.servo_write(SERVO_PIN, 100)

    # Wait for the car to park
    while a.ultrasonic_read(SONIC_PIN) > 10:
        pass

    # Begin timer
    start = time.time()

    # Raise the barrier and deactivate the LED
    a.digital_write(LED_PIN, 0)
    # a.servo_write(SERVO_PIN, 0)

    # Wait for the car to leave
    while a.ultrasonic_read(SONIC_PIN) < 10:
        pass

    # End timer
    end = time.time()

    # Lower barrier after short delay
    time.sleep(1)
    a.digital_write(LED_PIN, 1)
    a.servo_write(SERVO_PIN, 45)

    # Close connection to Arduino
    a.close()

    duration = end - start
    print("Duration: " + str(duration) + " seconds")
    q.put(duration)
