import classify
import numpy as np

RATE = 16000


def is_silence(data, threshold):
    square_mean = np.mean(data ** 2)
    return square_mean < threshold


def get_labels(data_stream, threshold):
    classify.load_graph()
    labels = classify.load_labels()
    all_frames = np.array([], dtype=np.float)
    relevant_predictions = []

    for data in data_stream:
        all_frames = np.concatenate([all_frames, data])
        total_length = len(all_frames)
        if total_length < RATE:
            continue
        else:
            all_frames = all_frames[total_length - RATE:total_length]

        first_third = all_frames[0:RATE // 3]
        if is_silence(first_third, threshold):
            # yield labels[0]
            relevant_predictions = []
            continue

        input_tensor = np.reshape(all_frames, (RATE, 1))
        result = classify.run_graph(input_tensor, RATE)
        relevant_predictions.append(result)
        if len(relevant_predictions) > 4:
            aggregated_result = np.sum(np.array(relevant_predictions) ** 2, axis=0)
            idx, score, label = classify.get_best(aggregated_result, labels)
            yield label
            relevant_predictions = []
            all_frames = np.array([], dtype=np.float)


def calibrate_silence(silence_data):
    classify.load_graph()
    labels = classify.load_labels()
    threshold = 0
    sample_count = 10
    frames = []

    for silence in silence_data:
        frames.append(silence)
        all_frames = np.concatenate(frames)
        if len(all_frames) > RATE:
            sound_data = np.reshape(all_frames, (len(all_frames), 1))
            silence_chunk = sound_data[0:RATE]
            result = classify.run_graph(silence_chunk, RATE)
            idx, score, label = classify.get_best(result, labels)
            square_mean = np.mean(silence_chunk ** 2)
            print(label, score, square_mean)
            frames = []
            if label == "_silence_":
                threshold = max(threshold, square_mean)
                sample_count -= 1
                if sample_count == 0:
                    threshold *= 1.5
                    print ("Silence threshold: ", threshold)
                    return threshold
            else:
                threshold = min(threshold, square_mean)
