import RPi.GPIO as GPIO
import time
from time import sleep
import PiMotor

class Robot:

    def __init__(self, left = "MOTOR4", right = "MOTOR2", config = 1):
        self.leftMotor = PiMotor.Motor(left, config)
        self.rightMotor = PiMotor.Motor(right, config)

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
