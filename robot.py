import Motor
import PiMotor

class Robot:

    def __init__(self, left = "MOTOR4", right = "MOTOR2", config = 1):
        self.leftMotor = Motor.Motor(left, config)
        self.rightMotor = Motor.Motor(right, config)

    def forward(self):
        self.leftMotor.reverse(100)
        self.rightMotor.reverse(100)

    def backward(self):
        self.leftMotor.forward(100)
        self.rightMotor.forward(100)

    def left(self):
        self.leftMotor.forward(100)
        self.rightMotor.reverse(100)

    def right(self):
        self.leftMotor.reverse(100)
        self.rightMotor.forward(100)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
