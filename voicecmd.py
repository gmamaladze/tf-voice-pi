import numpy as np
import math

RATE = 16000


def is_silence(data, threshold):
    square_mean = np.mean(data ** 2)
    return square_mean < threshold


def get_raw(data_stream, threshold):
    all_frames = np.array([], dtype=np.float)
    print("Listening for commands:")
    for data in data_stream:
        all_frames = np.concatenate([all_frames, data])
        total_length = len(all_frames)
        if total_length < RATE:
            continue
        else:
            all_frames = all_frames[total_length - RATE:total_length]

        first_third = all_frames[0:RATE // 3]
        if is_silence(first_third, threshold):
            yield None
            continue
        yield all_frames


def get_labels(data_stream, classifier, threshold):
    classifier.run(np.zeros((RATE, 1)))  # void call to avoid latency on firs word later
    for all_frames in get_raw(data_stream, threshold):
        if all_frames is None:
            continue
        input_tensor = np.reshape(all_frames, (RATE, 1))
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


def calibrate_silence(data_stream, classifier, sample_count=100):
    max_silence = 0
    max_sound = 0
    commands = np.array([0])
    frames = []
    print("Calibrating silence threshold. Please say random commands with 2-3 seconds pauses in between.")

    for data in data_stream:
        frames.append(data)
        all_frames = np.concatenate(frames)
        if len(all_frames) < RATE:
            continue
        sound_data = np.reshape(all_frames, (len(all_frames), 1))
        input_data = sound_data[0:RATE]
        idx, score, label = classifier.run(input_data)
        square_mean = np.mean(input_data ** 2)
        symbol = "." if idx == 0 else "*"
        # print(symbol)
        print(label, ";", score, ";", square_mean)
        frames.pop(0)
        max_sound = max(max_sound, math.sqrt(square_mean))
        if idx == 0:
            max_silence = max(max_silence, square_mean)
            sample_count -= 1
            if sample_count == 0:
                break
        else:
            if score > 0.5:
                np.append(commands, [square_mean])
    return max_silence, np.average(commands), max_sound


def get_labels_simple(data_stream, classifier):
    hit_count = 0
    hit_index = -1
    frames = []

    for data in data_stream:
        frames.append(data)
        all_frames = np.concatenate(frames)
        if len(all_frames) < RATE:
            continue
        sound_data = np.reshape(all_frames, (len(all_frames), 1))
        input_data = sound_data[0:RATE]
        idx, score, label = classifier.run(input_data)
        frames.pop(0)
        if idx == hit_index and score > .4:
            hit_count += 1
        else:
            hit_count = 0
            hit_index = idx
        if hit_index != 0 and hit_count > 3:
            yield label
            frames = []


def get_labels_raw(data_stream, classifier):
    frames = []

    for data in data_stream:
        frames.append(data)
        all_frames = np.concatenate(frames)
        if len(all_frames) < RATE:
            continue
        sound_data = np.reshape(all_frames, (len(all_frames), 1))
        input_data = sound_data[0:RATE]
        yield classifier.run(input_data)
