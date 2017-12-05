import curses
import os
import math
import threading
import time
import datetime
import numpy as np

isRaspberryPi = (os.uname()[4][:3] == 'arm')
if isRaspberryPi:
    import mic_pi as mic
else:
    import mic


def draw_column(screen, column, value, max_value, char):
    rows = min(value, max_value)
    for row in range(1, rows):
        screen.addch(max_value - row, column, char)


def draw_columns(screen, values, max_value, char):
    for x in range(0, len(values) - 1):
        draw_column(screen, x, values[x], max_value, char)


def main(screen):
    curses.cbreak()
    screen.keypad(1)
    screen.nodelay(1)
    pause_flag = False

    display_stack = []
    height, width = screen.getmaxyx()
    for data in mic.get_mic_data():
        key = screen.getch()
        if key == ord(' '):
            pause_flag = not pause_flag
        if key == curses.KEY_EXIT:
            break
        if pause_flag:
            continue
        draw_columns(screen, display_stack, height, ord(' '))
        mean = math.sqrt(np.mean(data ** 2))
        display_value = int(mean * 1000)
        display_stack.append(display_value)
        if len(display_stack) == width:
            display_stack.pop(0)
        draw_columns(screen, display_stack, height, ord('#'))
        screen.refresh()


curses.wrapper(main)