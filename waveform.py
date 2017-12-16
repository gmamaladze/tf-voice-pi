import numpy as np
import curses
import voicecmd
import mic


def draw():
    screen = curses.initscr()
    height, width = screen.getmaxyx()
    curses.endwin()

    audio_in = mic.MicPortAudio(16000)

    raw_stream = \
        voicecmd.get_labels(
            audio_in.get_mic_data_async())

    counter = 0

    for idx, score, label, first in raw_stream:
        mean = np.sum(np.absolute(first))
        display_value = min(int(mean), width - 12)
        nr = counter % 16
        nr_text = str(nr) if nr < 10 else chr(ord('A') + (nr - 10))
        print(nr_text + " " + label.ljust(10) + " " + str(int(score * 100)) + " " + ("#" * display_value))
        counter += 1


draw()
