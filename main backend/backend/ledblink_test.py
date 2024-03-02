from arduino import *
import time

if __name__ == '__main__':

    # Attempt connection to Arduino
    print("Establishing connection to Arduino")
    a = Arduino()

    # Wait for serial connection
    time.sleep(3)
    print("Established!")

    # Set pin 3 to output (LED)
    PIN = 3
    a.set_pin_mode(PIN, 'O')

    time.sleep(1) # Allow time for connection

    while True:
        distance = a.ultrasonic_read(4)
        print(distance)

    # Blink LED
    for i in range(1000):
        try:
            if i%2 == 0:
                a.digital_write(PIN, 1)
            else:
                a.digital_write(PIN, 0)

            time.sleep(1)
        except KeyboardInterrupt:
            break

    # Close connection
    print("Closing connection")
    a.digital_write(PIN, 0)
    a.close()
