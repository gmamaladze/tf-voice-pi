import curses
import os
import threading
import time

import examples.Snake
from tfvoicepi import classify, voicecmd, mic

isRaspberryPi = (os.uname()[4][:3] == 'arm')
if isRaspberryPi:
    import mic_pi as mic
else:
    pass

voice_actions = {
    "up": examples.Snake.UP,
    "down": examples.Snake.DOWN,
    "right": examples.Snake.RIGHT,
    "left": examples.Snake.LEFT,
    "stop": examples.Snake.STOP
}


def main(screen):
    screen.refresh()
    time.sleep(2)
    snake = examples.Snake.Snake(screen)

    voice_thread = threading.Thread(target=lambda: voice_loop(snake))
    voice_thread.start()

    with snake:
        snake.key_loop()


def voice_loop(snake):

    classifier = classify.Classifier()
    commands_stream = \
        voicecmd.get_labels_simple(
            mic.get_mic_data(),
            classifier)

    for command in commands_stream:
        next_direction = voice_actions.get(command)
        snake.set_direction(next_direction)
        snake.show_title("Keyboard: [ARROWS, ESC]  Voice: [up,down,left,right,stop]. #### " + command + "       ")
        if command == "stop":
            break


curses.wrapper(main)
