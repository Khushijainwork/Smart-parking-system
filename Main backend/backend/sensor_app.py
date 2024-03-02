from flask import Flask, render_template, request, redirect, url_for
from arduino import *
import time

app = Flask(__name__)

# Initialise connection to Arduino
a = Arduino()
time.sleep(3)

# Declare the pins
LED_PIN = 3
SONIC_PIN = 4
SERVO_PIN = 2

# Initialise the digital pin as output
a.set_pin_mode(LED_PIN, 'O')
a.set_pin_mode(SERVO_PIN, 'O')

print("Arduino initialised")

@app.route('/', methods = ['POST', 'GET'])
def index():
     # Handle form submission (control arduino)
    if request.method == 'POST':
        if request.form['submit'] == 'Turn On':
            print("TURN ON")
            a.digital_write(LED_PIN, 1)
        elif request.form['submit'] == 'Turn Off':
            print("TURN OFF")
            a.digital_write(LED_PIN, 0)

        if request.form['submit'] == 'Turn 90':
            print('SERVO')
            a.servo_write(SERVO_PIN, 90)
            time.sleep(1)
            a.servo_write(SERVO_PIN, 0)

    distance = a.analog_read(SONIC_PIN)
    return render_template('sensor.html', distance=distance)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')