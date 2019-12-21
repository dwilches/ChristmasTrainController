
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)

from train_util import *


class TrainConfig:

    _config_in_progress = True
    _ir_sensor_threshold = 50
    _debouncing = False
    _motor = None

    def __init__(self, motor: Motor):
        self._motor = motor

    def is_config_in_progress(self):
        return self._config_in_progress

    def get_ir_sensor_threshold(self):
        return self._ir_sensor_threshold


    def process_button_input(self):
        buttons_pressed = brick.buttons()

        if not any(buttons_pressed):
            if self._debouncing:
                self._debouncing = False
            return

        # Config enable/disable
        if Button.CENTER in buttons_pressed:
            if not self._debouncing:
                self._config_in_progress = not self._config_in_progress
                self._debouncing = True
                if self._config_in_progress:
                    self._enable_config_mode()
                else:
                    self._disable_config_mode()

        # Motor position adjustement
        if self._config_in_progress:
            if Button.UP in buttons_pressed:
                display_text("Motor towards curve")
                self._manually_offset_motor(1000)
            elif Button.DOWN in buttons_pressed:
                display_text("Motor towards straight")
                self._manually_offset_motor(-1000)

            if Button.LEFT in buttons_pressed:
                self._manually_offset_sensor(10)
                display_text("Offseting sensor to far")
            elif Button.RIGHT in buttons_pressed:
                self._manually_offset_sensor(-10)
                display_text("Offseting sensor to near")


    def _enable_config_mode(self):
        brick.sound.beeps(1)
        display_text("Config started")


    def _disable_config_mode(self):
        brick.sound.beeps(2)
        display_text("Config finished")
        brick.light(Color.GREEN)


    def _manually_offset_motor(self, speed):
        self._motor.run(speed)
        while any(brick.buttons()):
            pass
        self._motor.stop()
        self._motor.reset_angle(0)


    def _manually_offset_sensor(self, amount):
        self._ir_sensor_threshold = self._ir_sensor_threshold + amount
        if self._ir_sensor_threshold > 100:
            self._ir_sensor_threshold = 100
        if self._ir_sensor_threshold < 0:
            self._ir_sensor_threshold = 0

