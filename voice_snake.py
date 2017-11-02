import curses
import time
import threading
import voicecmd
import classify
import Snake
import os

isRaspberryPi = (os.uname()[4][:3] == 'arm')
if isRaspberryPi:
    import mic_pi as mic
else:
    import mic


voice_actions = {
    "up": Snake.UP,
    "down": Snake.DOWN,
    "right": Snake.RIGHT,
    "left": Snake.LEFT,
    "stop": Snake.STOP
}


def main(screen):
    screen.refresh()
    time.sleep(2)
    snake = Snake.Snake(screen)

    voice_thread = threading.Thread(target=lambda: voice_loop(snake))
    voice_thread.start()

    with snake:
        snake.key_loop()


def voice_loop(snake):
    threshold = 2e-06

    classifier = classify.Classifier()
    commands_stream = \
        voicecmd.get_confident_labels(
            voicecmd.get_labels(
                mic.get_mic_data(),
                classifier,
                threshold))

    for command in commands_stream:
        next_direction = voice_actions.get(command)
        snake.set_direction(next_direction)
        snake.show_title("Keyboard: [ARROWS, ESC]  Voice: [up,down,left,right,stop]. #### " + command + "       ")
        if command == "stop":
            break

curses.wrapper(main)
