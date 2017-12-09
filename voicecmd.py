import numpy as np
import math
from collections import deque
import threading

INPUT_SIZE = 16000
CHUNK_SIZE = 1000
CHUNK_COUNT = INPUT_SIZE / CHUNK_SIZE


def is_silence(data, threshold):
    square_mean = np.mean(data ** 2)
    return square_mean < threshold


def get_raw(data_stream, threshold):
    all_frames = np.array([], dtype=np.float)
    print("Listening for commands:")
    for data in data_stream:
        all_frames = np.concatenate([all_frames, data])
        total_length = len(all_frames)
        if total_length < INPUT_SIZE:
            continue
        else:
            all_frames = all_frames[total_length - INPUT_SIZE:total_length]

        first_third = all_frames[0:INPUT_SIZE // 3]
        if is_silence(first_third, threshold):
            yield None
            continue
        yield all_frames


def get_labels(data_stream, classifier, threshold):
    classifier.run(np.zeros((INPUT_SIZE, 1)))  # void call to avoid latency on firs word later
    for all_frames in get_raw(data_stream, threshold):
        if all_frames is None:
            continue
        input_tensor = np.reshape(all_frames, (INPUT_SIZE, 1))
        yield classifier.run(input_tensor)


def get_confident_labels(labels_stream):
    confidence = 0
    last_idx = 0

    for idx, score, label in labels_stream:
        if confidence < 0:
            confidence += 1
            last_idx = 0
            continue

        if idx == 0 or idx != last_idx:
            last_idx = idx
            confidence = 0
            continue

        if idx == last_idx:
            if confidence > 2:
                yield label
                confidence = -3
                last_idx = 0
            else:
                confidence += 1


def calibrate_silence(data_stream, classifier):
    max_silence = 0
    print("Calibrating silence threshold ...")
    chunk_count = 0
    batch_size = INPUT_SIZE // CHUNK_SIZE

    frames = deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT)
    for data in data_stream:
        frames.append(data)
        frames.popleft()

        if (chunk_count % batch_size) != 0:
            chunk_count += 1
            continue
        if chunk_count > batch_size * 10:
            break
        chunk_count += 1
        idx, label, score = classify(classifier, frames)

        square_mean = np.mean(np.hstack(frames) ** 2)
        if idx == 0:
            max_silence = max(max_silence, square_mean)
            print(".")
        else:
            print("*")
    return max_silence


def get_labels_batched(data_stream, classifier, threshold, batch_size):
    chunk_count = 0
    frames = deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT)
    for data in data_stream:
        frames.append(data)
        frames.popleft()

        if (chunk_count % batch_size) != 0:
            chunk_count += 1
            continue

        first_square_mean = np.mean(frames[0] ** 2)
        if threshold > first_square_mean:
            chunk_count = 0
            yield 0, classifier.labels[0], .9
            continue

        yield classify(classifier, frames)
        frames = deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT)
        chunk_count = 0


def get_labels_simple(data_stream, classifier, threshold):
    frames = deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT)
    for data in data_stream:
        frames.append(data)
        frames.popleft()
        first_square_mean = np.mean(frames[0] ** 2)
        if threshold * 2 > first_square_mean:
            yield 0, classifier.labels[0], .9
            continue

        idx, label, score = classify(classifier, frames)
        if idx != 0 and score > .5:
            yield idx, score, label
            frames = deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT)


def classify(classifier, frames):
    stacked = np.hstack(frames)
    padded = np.concatenate([stacked, np.zeros(INPUT_SIZE - len(stacked))])
    input_vector = np.reshape(padded, (INPUT_SIZE, 1))
    idx, score, label = classifier.run(input_vector)
    return idx, label, score


def get_labels_raw(data_stream, classifier):
    batch_size = 16
    frame_counter = 0
    frames = deque([np.zeros(CHUNK_SIZE)] * CHUNK_COUNT)
    for data in data_stream:
        frames.append(data)
        frames.popleft()
        frame_counter += 1
        if (frame_counter % batch_size) != 0:
            continue
        yield classify(classifier, frames)
