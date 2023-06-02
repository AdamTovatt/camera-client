import math
from gpiozero import Servo
from time import sleep
import threading

from gpiozero.pins.pigpio import PiGPIOFactory


class ServoController:
    factory = None  # the GPIO factory used to create the servo objects
    x_servo = None  # the x servo object
    y_servo = None  # the y servo object

    update_thread = None  # the thread used to update the servo positions

    running = False

    target_x = 0  # target servo positions, the servos will move towards these positions
    target_y = 0

    current_x = 0  # current servo positions, this is the (assumed) current position of the servos
    current_y = 0

    min_x = -1  # minimum and maximum values for the servo positions
    max_x = 1
    min_y = -1
    max_y = 1

    max_speed = 1  # maximum change in servo position per update
    update_interval = 0.1  # seconds to sleep before updating the servo positions

    def __init__(self, min_x, max_x, min_y, max_y, max_speed, update_interval):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.max_speed = max_speed
        self.update_interval = update_interval
        self.setup()

    def start(self):
        self.running = True
        self.update_thread = threading.Thread(target=self.update_servo_positions)
        self.update_thread.start()

    def stop(self):
        self.running = False
        self.update_thread.join()

    def setup(self):
        self.factory = PiGPIOFactory()

        self.x_servo = Servo(14, min_pulse_width=0.5/1000,
                             max_pulse_width=2.5/1000, pin_factory=self.factory)
        self.y_servo = Servo(15, min_pulse_width=0.5/1000,
                             max_pulse_width=2.5/1000, pin_factory=self.factory)

    def set_position(self, new_x, new_y):
        self.target_x = self.limit_x(new_x)
        self.target_y = self.limit_y(new_y)

    def update_servo_positions(self):
        while self.running:
            if not self.is_within_range(self.current_x, self.target_x, 0.1):
                new_x = self.move_value_towards(self.current_x, self.target_x, self.max_speed)
                self.x_servo.value = new_x
            else:
                self.x_servo.detach()

            if not self.is_within_range(self.current_y, self.target_y, 0.1):
                new_y = self.move_value_towards(self.current_y, self.target_y, self.max_speed)
                self.y_servo.value = new_y
            else:
                self.y_servo.detach()

            sleep(self.update_interval)

    def move_value_towards(self, current, target, max_change):
        if current < target:
            return min(current + max_change, target)
        else:
            return max(current - max_change, target)

    def is_within_range(self, value, target, range):
        return abs(value - target) <= range

    def limit_x(self, value):
        return max(min(value, self.max_x), self.min_y)

    def limit_y(self, value):
        return max(min(value, self.max_y), self.min_y)
