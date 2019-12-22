
# Ev3 modules
from pybricks.ev3devices import InfraredSensor


class RailroadSensor:
        
    _debouncing = False

    # If we read a value smaller than this from the IR sensor, then we consider the train is close to the sensor
    _ir_sensor_threshold = 50
    
    def __init__(self, ir_sensor: InfraredSensor):
        self._ir_sensor = ir_sensor

    # This method does debouncing:
    # * It returns True the first time it detects the train is too close.
    # * Then, it will start returning False during all the time the train remains too close.
    # * Once the train gets far from the sensor, this method is rearmed and will return True the next time the
    #   train gets close.
    def is_train_close(self):
        is_sensor_breached = self._ir_sensor.distance() < self._ir_sensor_threshold

        if is_sensor_breached and not self._debouncing:
            self._debouncing = True
            return True
        
        if not is_sensor_breached:
            self._debouncing = False
        
        return False

    def manually_offset_sensor(self, amount):
        self._ir_sensor_threshold = self._ir_sensor_threshold + amount
        if self._ir_sensor_threshold > 100:
            self._ir_sensor_threshold = 100
        if self._ir_sensor_threshold < 0:
            self._ir_sensor_threshold = 0

        return self._ir_sensor_threshold
