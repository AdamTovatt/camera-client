from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = None
pitchServo = None
yawServo = None

pitchValue = 90
yawValue = 90

maxAngle = 179
minAngle = 1


def setup():
    factory = PiGPIOFactory()
    pitchServo = Servo(14, min_pulse_width=0.5/1000,
                       max_pulse_width=2.5/1000, pin_factory=factory)
    yawServo = Servo(15, min_pulse_width=0.5/1000,
                     max_pulse_width=2.5/1000, pin_factory=factory)


def movePosition(deltaPitch, deltaYaw):
    if (factory is None):
        setup()

    pitchAngle = (deltaPitch / 90) - 1
    yawAngle = (deltaYaw / 90) - 1

    pitchValue = limit(pitchValue + pitchAngle)
    yawValue = limit(yawValue + yawAngle)

    pitchServo.value = pitchValue
    yawServo.value = yawValue


def limit(value):
    if value > maxAngle:
        value = maxAngle
    elif value < minAngle:
        value = minAngle
    return value
