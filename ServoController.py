import math
from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = None
pitchServo = None
yawServo = None

pitchValue = 90
yawValue = 90

maxAngle = 180
minAngle = 0

lastPitch = pitchValue
lastYaw = yawValue


def setup():
    # Declare the variables as global
    global factory, pitchServo, yawServo, lastPitch, lastYaw

    factory = PiGPIOFactory()
    pitchServo = Servo(14, min_pulse_width=0.5/1000,
                       max_pulse_width=2.5/1000, pin_factory=factory)
    yawServo = Servo(15, min_pulse_width=0.5/1000,
                     max_pulse_width=2.5/1000, pin_factory=factory)


def movePosition(deltaPitch, deltaYaw):
    global pitchValue, yawValue, lastPitch, lastYaw  # Declare the variables as global

    if (factory is None):
        setup()

    # print("Current pitch: " + str(pitchValue) +
    # ", current yaw: " + str(yawValue))

    # print("Moving servos by " + str(deltaPitch) + " and " + str(deltaYaw) +
    # " degrees")

    pitchValue = limit(pitchValue + deltaPitch)
    yawValue = limit(yawValue + deltaYaw)

    print("Setting pitch to " + str((pitchValue / 90) - 1) +
          " and yaw to " + str((yawValue / 90) - 1))

    newPitch = (pitchValue / 90) - 1
    newYaw = (yawValue / 90) - 1

    if (newPitch != lastPitch or newYaw != lastYaw):
        try:
            lastPitch = newPitch
            lastYaw = newYaw
            pitchServo.value = lastPitch
            yawServo.value = lastYaw
            sleep(0.1)  # Delay to allow the servos to move
            pitchServo.detach()
            yawServo.detach()
        except Exception as exception:
            print("Could not move servos: " + str(exception))


def floor_to_nearest_5(value):
    return math.floor(value / 5) * 5


def limit(value):
    if value > maxAngle:
        value = maxAngle
    elif value < minAngle:
        value = minAngle

    # print("Limited value to " + str(value))
    return value
