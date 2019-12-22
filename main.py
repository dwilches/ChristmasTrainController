#!/usr/bin/env pybricks-micropython

# Ev3 MicroPython documentation:
# https://le-www-live-s.legocdn.com/sc/media/files/ev3-micropython/ev3micropythonv100-71d3f28c59a1e766e92a59ff8500818e.pdf

# Ev3 modules
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, InfraredSensor)
from pybricks.parameters import (Port, Color)

# This app's files
from railroad_config import RailroadConfig
from railroad_light import RailroadLight
from railroad_sensor import RailroadSensor


# Configuration parameters
needed_angle = 360*4
max_speed = 2000


class Railroad:
    
    _is_on_straight_rail = True

    def __init__(self):
        self._motor = Motor(Port.A)
        self._motor.reset_angle(0)
        
        ir_sensor = InfraredSensor(Port.S1)
        brick.light(Color.GREEN)

        self._train_light = RailroadLight()
        self._train_sensor = RailroadSensor(ir_sensor)
        self._train_config = RailroadConfig(self._motor, self._train_light, self._train_sensor)

        self._train_config.enable_config_mode(True)

    def execute(self):
        # Enables/disables the config mode, and allows tweaking the motor/sensor thresholds
        # manually.
        self._train_config.process_button_input()

        # In each iteration, it changes the Ev3 Brick's lights according to the railroads needs
        # (blinking them, changing colors)
        self._train_light.process_lights()

        if self._train_config.is_config_in_progress():
            return
        
        if self._train_sensor.is_train_close():
            self._switch_rails()

    def _switch_rails(self):
        global needed_angle, max_speed

        if self._is_on_straight_rail:
            # Move rail to curve side
            self._motor.run_target(max_speed, needed_angle)
        else:
            # Move train to straight side
            self._motor.run_target(max_speed, 0)
        self._is_on_straight_rail = not self._is_on_straight_rail


if __name__ == "__main__":
    rail_road = Railroad()
    while True:
        rail_road.execute()
