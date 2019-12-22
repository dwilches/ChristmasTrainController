
# Ev3 modules
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, InfraredSensor)
from pybricks.parameters import (Button, SoundFile)

# This app's files
from railroad_util import *
from railroad_light import RailroadLight
from railroad_sensor import RailroadSensor


class RailroadConfig:

    _config_in_progress = False
    _debouncing = False

    def __init__(self, motor: Motor, train_light: RailroadLight, train_sensor: RailroadSensor):
        self._motor = motor
        self._train_light = train_light
        self._train_sensor = train_sensor

    def is_config_in_progress(self):
        return self._config_in_progress

    def process_button_input(self):
        buttons_pressed = brick.buttons()

        if not any(buttons_pressed):
            if self._debouncing:
                self._debouncing = False
            return

        # Config enable/disable
        if Button.CENTER in buttons_pressed and not self._debouncing:
            self._debouncing = True
            self.enable_config_mode(not self._config_in_progress)

        # Motor position adjustement
        if self._config_in_progress:
            if Button.UP in buttons_pressed:
                display_text("Motor towards curve")
                self._manually_offset_motor(1000)
            elif Button.DOWN in buttons_pressed:
                display_text("Motor towards straight")
                self._manually_offset_motor(-1000)

            if Button.LEFT in buttons_pressed:
                new_value = self._train_sensor.manually_offset_sensor(10)
                display_text("Offseting sensor to far: " + str(new_value))
            elif Button.RIGHT in buttons_pressed:
                new_value = self._train_sensor.manually_offset_sensor(-10)
                display_text("Offseting sensor to near: " + str(new_value))

    def enable_config_mode(self, enable):
        self._config_in_progress = not self._config_in_progress
        if enable:
            brick.sound.file(SoundFile.CONFIRM, volume=100)
            display_text("Config started")
        else:
            brick.sound.file(SoundFile.READY, volume=100)
            display_text("Config finished")
        self._train_light.enable_blink(enable)

    def _manually_offset_motor(self, speed):
        self._motor.run(speed)
        while any(brick.buttons()):
            pass
        self._motor.stop()
        self._motor.reset_angle(0)
