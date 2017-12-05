import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

BACKWARD = 1
LEFT = 2
FORWARD = 3
RIGHT = 4


class Arrow:
    """ Defines an object for controlling one of the LED arrows on the Motorshield.

        Arguments:
        which = integer label for each arrow. The arrow number if arbitrary starting with:
            1 = Arrow closest to the Motorshield's power pins and running clockwise round the board
            ...
            4 = Arrow closest to the motor pins.
    """
    arrow_pins = {1: 33, 2: 35, 3: 37, 4: 36}

    def __init__(self, which):
        self.pin = self.arrow_pins[which]
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
