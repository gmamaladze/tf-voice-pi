import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Motor:
    MOTOR_PINS = {"MOTOR4": {"config": {1: {"e": 32, "f": 24, "r": 26}, 2: {"e": 32, "f": 26, "r": 24}}},
                  "MOTOR3": {"config": {1: {"e": 19, "f": 21, "r": 23}, 2: {"e": 19, "f": 23, "r": 21}}},
                  "MOTOR2": {"config": {1: {"e": 22, "f": 16, "r": 18}, 2: {"e": 22, "f": 18, "r": 16}}},
                  "MOTOR1": {"config": {1: {"e": 11, "f": 15, "r": 13}, 2: {"e": 11, "f": 13, "r": 15}}}}

    def __init__(self, motor, config):
        """
        Motor class
        :param motor: string corresponding to the motor pin label on the shield ("MOTOR1","MOTOR2","MOTOR3","MOTOR4")
        :param config: int 1 or 2 defining which pins control "forward" and "backward" movement.
        """
        self.testMode = False
        self.pins = self.MOTOR_PINS[motor]["config"][config]
        GPIO.setup(self.pins['e'], GPIO.OUT)
        GPIO.setup(self.pins['f'], GPIO.OUT)
        GPIO.setup(self.pins['r'], GPIO.OUT)
        self.PWM = GPIO.PWM(self.pins['e'], 50)  # 50Hz frequency
        self.PWM.start(0)
        GPIO.output(self.pins['e'], GPIO.HIGH)
        GPIO.output(self.pins['f'], GPIO.LOW)
        GPIO.output(self.pins['r'], GPIO.LOW)

    def forward(self, speed):
        """
        Forward
        :param speed: 0 to 100, 0 - stop and 100 - maximum speed
        """
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.pins['f'], GPIO.HIGH)
        GPIO.output(self.pins['r'], GPIO.LOW)

    def reverse(self, speed):
        """
        Reverse
        :param speed: 0 to 100, 0 - stop and 100 - maximum speed
        """
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.pins['f'], GPIO.LOW)
        GPIO.output(self.pins['r'], GPIO.HIGH)

    def stop(self):
        """
        Stop
        """
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.pins['f'], GPIO.LOW)
        GPIO.output(self.pins['r'], GPIO.LOW)
