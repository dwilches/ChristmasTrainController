
from pybricks import ev3brick as brick
from pybricks.tools import print


def display_text(msg):
    print(msg)
    brick.display.text(msg)
