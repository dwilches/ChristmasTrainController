#!/usr/bin/env pybricks-micropython

# Ev3 MicroPython documentation:
# https://le-www-live-s.legocdn.com/sc/media/files/ev3-micropython/ev3micropythonv100-71d3f28c59a1e766e92a59ff8500818e.pdf

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from time import clock


# Configuration parameters
change_rail_threshold = 50
needed_angle = 360*4
max_speed = 2000


def move_to_curve():
    motor.run_target(max_speed, needed_angle)


def move_to_straight():
    motor.run_target(max_speed, 0)


def manually_offset_motor(speed):
    motor.run(speed)
    while any(brick.buttons()):
        pass
    motor.stop()
    motor.reset_angle(0)


def manually_offset_sensor(amount):
    sensor_threshold = sensor_threshold + amount
    if sensor_threshold > 100:
        sensor_threshold = 100
    if sensor_threshold < 0:
        sensor_threshold = 0


def display_text(msg):
    #print(msg)
    brick.display.text(msg)


def process_button_input():
    global config_in_progress

    buttons_pressed = brick.buttons()
    if not any(buttons_pressed):
        return

    # Config enable/disable
    if Button.CENTER in buttons_pressed:
        config_in_progress = not config_in_progress
        if config_in_progress:
            brick.sound.file(SoundFile.DOG_BARK_1)
            display_text("Config started")
            # Wait until the CENTER button is no longer pressed
            while Button.CENTER in buttons_pressed:
                buttons_pressed = brick.buttons()
        else:
            brick.sound.file(SoundFile.DOG_BARK_1)
            display_text("Config finished")
            brick.light(Color.GREEN)
    
    # Motor position adjustement
    if config_in_progress:
        if Button.UP in buttons_pressed:
            display_text("Motor towards curve")
            manually_offset_motor(1000)
        elif Button.DOWN in buttons_pressed:
            display_text("Motor towards straight")
            manually_offset_motor(-1000)

        if Button.LEFT in buttons_pressed:
            manually_offset_sensor(10)
            display_text("Offseting sensor to far")
        elif Button.RIGHT in buttons_pressed:
            manually_offset_sensor(-10)
            display_text("Offseting sensor to near")


can_breach_again = True
def process_ir_sensor_input():
    global is_sensor_breached, ir_sensor, change_rail_threshold, can_breach_again, is_on_straight_rail

    is_sensor_breached = ir_sensor.distance() < change_rail_threshold
    if is_sensor_breached and can_breach_again:
        can_breach_again = False
        if is_on_straight_rail:
            is_on_straight_rail = False
            move_to_curve()
        else:
            is_on_straight_rail = True
            move_to_straight()
    
    if not is_sensor_breached:
        can_breach_again = True


next_light_change_time = 0
is_light_on = False
def blink_light():
    global is_light_on, next_light_change_time

    if next_light_change_time < clock():
        is_light_on = not is_light_on
        current_light_color = None if is_light_on else Color.RED
        brick.light(current_light_color)
        next_light_change_time = clock() + 0.1


motor = Motor(Port.A)
ir_sensor = InfraredSensor(Port.S1)
brick.light(None)
motor.reset_angle(0)

config_in_progress = True
is_on_straight_rail = True


while True:

    process_button_input()

    if config_in_progress:
        blink_light()
        continue
    
    process_ir_sensor_input()
