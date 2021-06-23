import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
        2: {"name" : "GREEN LED", "state" : GPIO.LOW },
        3: {"name" : "RED LED", "state" : GPIO.LOW},
        14: {"name" : "BLUE LED", "state" : GPIO.LOW }
        }
for p in pins:
    GPIO.setup(p, GPIO.OUT) # set pin as an output
    GPIO.output(p, GPIO.LOW) # set pin low

@app.route("/")
def led_control():
    for p in pins:
        pins[p]["state"] = GPIO.input(p)

    template = { "pins" : pins}
    return render_template("led_control.html", **template)

@app.route("/<activate>/<action>") # request url with pin number
def action(activate, action):
    change = int(activate) # convert pin from url into int
    device = pins[change]["name"]

    if action ==  "on":
        GPIO.output(change, GPIO.HIGH)
        text = device + "is on"

    if action == "off":
        GPIO.output(change, GPIO.LOW)
        text = device + "is off"

    for p in pins:
        pins[p]["state"] = GPIO.input(p)

    template = {"pins" : pins}

    return render_template("led_control.html", **template)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
