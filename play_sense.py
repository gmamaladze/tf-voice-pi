from sense_hat import SenseHat
import threading
import voicecmd
import classify
import mic_pi as mic

sense = SenseHat()

X = [255, 0, 0]
_ = [0, 0, 0]

UNKNOWN = [
    _, _, _, X, X, _, _, _,
    _, _, X, _, _, X, _, _,
    _, _, _, _, _, X, _, _,
    _, _, _, _, X, _, _, _,
    _, _, _, X, _, _, _, _,
    _, _, _, X, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, X, _, _, _, _
]

ARR_RIGHT = [
    _, _, _, _, X, _, _, _,
    _, _, _, _, _, X, _, _,
    _, _, _, _, _, _, X, _,
    _, _, _, _, _, _, _, X,
    _, _, _, _, _, _, _, X,
    _, _, _, _, _, _, X, _,
    _, _, _, _, _, X, _, _,
    _, _, _, _, X, _, _, _
]

ARR_UP = [
    _, _, _, X, X, _, _, _,
    _, _, X, _, _, X, _, _,
    _, X, _, _, _, _, X, _,
    X, _, _, _, _, _, _, X,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _
]

ARR_LEFT = [
    _, _, _, X, _, _, _, _,
    _, _, X, _, _, _, _, _,
    _, X, _, _, _, _, _, _,
    X, _, _, _, _, _, _, _,
    X, _, _, _, _, _, _, _,
    _, X, _, _, _, _, _, _,
    _, _, X, _, _, _, _, _,
    _, _, _, X, _, _, _, _
]

ARR_DOWN = [
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    X, _, _, _, _, _, _, X,
    _, X, _, _, _, _, X, _,
    _, _, X, _, _, X, _, _,
    _, _, _, X, X, _, _, _
]


def draw(sprite):
    sense.set_pixels(sprite)
    timer = threading.Timer(0.8, sense.clear)
    timer.start()

draw(ARR_UP)

classifier = classify.Classifier()

max_silence = \
    voicecmd.calibrate_silence(
        mic.get_mic_data(),
        classifier)

threshold = max_silence * 4

simple_stream = \
    voicecmd.get_labels_batched(
        mic.get_mic_data_async(),
        classifier,
        threshold,
        5)

sprites = {
    "_unknown_": UNKNOWN,
    "left": ARR_LEFT,
    "right": ARR_RIGHT,
    "up": ARR_UP,
    "down": ARR_DOWN
}

for idx, score, label in simple_stream:
    if idx == 0:
        print(".")
        continue
    print label
    sprite = sprites.get(label, UNKNOWN)
    draw(sprite)
