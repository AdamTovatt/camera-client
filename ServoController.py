from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = None
pitchServo = None
yawServo = None

pitchValue = 0.5
yawValue = 0.5

maxAngle = 179
minAngle = 1


def setup():
    global factory, pitchServo, yawServo  # Declare the variables as global

    factory = PiGPIOFactory()
    # pitchServo = Servo(14, min_pulse_width=0.5/1000,
    #                   max_pulse_width=2.5/1000, pin_factory=factory)
    # yawServo = Servo(15, min_pulse_width=0.5/1000,
    #                 max_pulse_width=2.5/1000, pin_factory=factory)
    pitchServo = Servo(14, pin_factory=factory)
    yawServo = Servo(15, pin_factory=factory)


def movePosition(deltaPitch, deltaYaw):
    global pitchValue, yawValue  # Declare the variables as global

    if (factory is None):
        setup()

    print("Current pitch: " + str(pitchValue) +
          ", current yaw: " + str(yawValue))

    print("Moving servos by " + str(deltaPitch) + " and " + str(deltaYaw) +
          " degrees")

    deltaPitchAngle = (deltaPitch / 90) - 1
    deltaYawAngle = (deltaYaw / 90) - 1

    pitchAngle = deltaPitchAngle
    yawAngle = deltaYawAngle

    pitchValue = limit(pitchValue + pitchAngle)
    yawValue = limit(yawValue + yawAngle)

    print("Setting pitch to " + str(pitchValue) +
          " and yaw to " + str(yawValue))

    pitchServo.value = pitchValue
    yawServo.value = yawValue


def limit(value):
    if value > maxAngle:
        value = maxAngle
    elif value < minAngle:
        value = minAngle

    print("Limited value to " + str(value))
    return value
