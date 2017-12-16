import numpy as np
from collections import deque
import gate
import classify

INPUT_SIZE = 16000
CHUNK_SIZE = 1000
CHUNK_COUNT = INPUT_SIZE // CHUNK_SIZE


def is_gauss_like_distribution(averages):
    avg_list = list(averages)
    head = sum(avg_list[:4])
    middle = sum(avg_list[4:12]) / 2
    tail = sum(avg_list[12:16])
    return head < middle and tail < middle


def is_silence(averages, threshold):
    for current in averages:
        if current > threshold:
            return True
    return False


def do_classify(classifier, frames):
    stacked = np.hstack(frames)
    padded = np.concatenate([stacked, np.zeros(INPUT_SIZE - len(stacked))])
    input_vector = np.reshape(padded, (INPUT_SIZE, 1))
    idx, score, label = classifier.run(input_vector)
    return idx, score, label


def get_labels(data_stream,
               classifier=classify.NullClassifier(),
               should_skip=lambda a: False,
               gate_=gate.NullGate()):
    frames, averages = clear_frames()
    for data in data_stream:
        frames.append(data)
        frames.popleft()
        averages.append(np.mean(data) ** 2)
        averages.popleft()
        if should_skip(averages):
            gate_.reset()
            continue
        idx, score, label = do_classify(classifier, frames)
        if not gate_.is_confident(idx, score):
            continue
        if idx == 0:  # silence
            continue
        yield idx, score, label, data
        frames, averages = clear_frames()
        gate_.reset()


def clear_frames():
    return deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT), deque([0] * CHUNK_COUNT)
