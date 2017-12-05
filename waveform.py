import os
import math
import numpy as np
import curses

isRaspberryPi = (os.uname()[4][:3] == 'arm')
if isRaspberryPi:
    import mic_pi as mic
else:
    import mic


def draw():
    screen = curses.initscr()
    height, width = screen.getmaxyx()
    curses.endwin()

    for data in mic.get_mic_data():
        mean = math.sqrt(np.mean(data ** 2))
        display_value = min(int(mean * 1000), width)
        print("#"*display_value)


draw()
