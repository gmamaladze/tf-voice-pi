#!/usr/bin/python

# Library for PiMotor Shield V2
# Developed by: SB Components
# Author: Ankur
# Project: RPi Motor Shield

import RPi.GPIO as GPIO                        #Import GPIO library
import time

GPIO.setmode(GPIO.BOARD)                       #Set GPIO pin numbering

GPIO.setwarnings(False)


class LinkedMotors:
    ''' Links 2 or more motors together as a set.

        This allows a single command to be used to control a linked set of motors
        e.g. For a 4x wheel vehicle this allows a single command to make all 4 wheels go forward.
        Starts the motor turning in its configured "forward" direction.

        Arguments:
        *motors = a list of Motor objects
     '''
    def __init__(self, *motors):
        self.motor = []
        for i in motors:
            print(i.pins)
            self.motor.append(i)

    def forward(self,speed):
        ''' Starts the motor turning in its configured "forward" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
     '''
        for i in range(len(self.motor)):
            self.motor[i].forward(speed)

    def reverse(self,speed):
        """ Starts the motor turning in its configured "reverse" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
     """
        for i in range(len(self.motor)):
            self.motor[i].reverse(speed)

    def stop(self):
        ''' Stops power to the motor,
     '''
        for i in range(len(self.motor)):
            self.motor[i].stop()

class Sensor:
    """ Defines a sensor connected to the sensor pins on the MotorShield

        Arguments:
        sensortype = string identifying which sensor is being configured.
            i.e. "IR1", "IR2", "ULTRASONIC"
        boundary = an integer specifying the minimum distance at which the sensor
            will return a Triggered response of True.
    """
    Triggered = False
    def iRCheck(self):
        input_state = GPIO.input(self.config["echo"])
        if input_state == True:
            print("Sensor 2: Object Detected")
            self.Triggered = True
        else:
            self.Triggered = False

    def sonicCheck(self):
        print("SonicCheck has been triggered")
        time.sleep(0.333)
        GPIO.output(self.config["trigger"], True)
        time.sleep(0.00001)
        GPIO.output(self.config["trigger"], False)
        start = time.time()
        while GPIO.input(self.config["echo"])==0:
            start = time.time()
        while GPIO.input(self.config["echo"])==1:
            stop = time.time()
        elapsed = stop-start
        measure = (elapsed * 34300)/2
        self.lastRead = measure
        if self.boundary > measure:
            print("Boundary breached")
            print(self.boundary)
            print(measure)
            self.Triggered = True
        else:
            self.Triggered = False

    sensorpins = {"IR1":{"echo":7, "check":iRCheck}, "IR2":{"echo":12, "check":iRCheck},
                  "ULTRASONIC":{"trigger":29, "echo": 31, "check":sonicCheck}}

    def trigger(self):
        ''' Executes the relevant routine that activates and takes a reading from the specified sensor.

        If the specified "boundary" has been breached the Sensor's Triggered attribute gets set to True.
    '''
        self.config["check"](self)
        print("Trigger Called")

    def __init__(self, sensortype, boundary):
        self.config = self.sensorpins[sensortype]
        self.boundary = boundary
        self.lastRead = 0
        if "trigger" in self.config:
            print("trigger")
            GPIO.setup(self.config["trigger"],GPIO.OUT)
        GPIO.setup(self.config["echo"],GPIO.IN)

class Arrow():
    ''' Defines an object for controlling one of the LED arrows on the Motorshield.

        Arguments:
        which = integer label for each arrow. The arrow number if arbitrary starting with:
            1 = Arrow closest to the Motorshield's power pins and running clockwise round the board
            ...
            4 = Arrow closest to the motor pins.
    '''
    arrowpins={1:33,2:35,3:37,4:36}

    def __init__(self, which):
        self.pin = self.arrowpins[which]
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin,GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin,GPIO.LOW)
