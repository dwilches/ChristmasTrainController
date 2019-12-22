
# System modules
import time

# Ev3 modules
from pybricks import ev3brick as brick
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)

class TrainLight:

    _next_light_change_time = 0
    _should_blink = False
    _is_light_on = False
    _current_light_color = None


    def process_lights(self):
        if self._should_blink:
            self._run_blink_cycle()


    def enable_blink(self, enable: bool):
        self._should_blink = enable

        # Don't let the light ON when blinking is disabled
        if not self._should_blink:
            brick.light(None)


    def _run_blink_cycle(self):
        if self._next_light_change_time < time.clock():
            self._is_light_on = not self._is_light_on
            self._current_light_color = None if self._is_light_on else Color.RED
            brick.light(self._current_light_color)
            self._next_light_change_time = time.clock() + 0.1

