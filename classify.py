from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# noinspection PyUnresolvedReferences
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio

import tensorflow as tf

DEFAULT_GRAPH_FILE = "conv_actions_frozen.pb"
DEFAULT_LABELS_FILE = "conv_actions_labels.txt"
DEFAULT_INPUT_SIZE = 16000


class NullClassifier:
    def __init__(self):
        self.labels = ["_none_"]
        pass

    def run(self, data):
        return 0, 1, self.labels[0]


class Classifier:
    def __init__(self,
                 graph_file=DEFAULT_GRAPH_FILE,
                 labels_file=DEFAULT_LABELS_FILE,
                 input_size=DEFAULT_INPUT_SIZE):
        load_graph(graph_file)
        self.labels = load_labels(labels_file)
        self.sample_rate = input_size
        pass

    def run(self, data):
        predictions = run_graph(data, self.sample_rate)
        return get_best(predictions, self.labels)


def get_best(predictions, labels):
    idx = predictions.argmax()
    return idx, predictions[idx], labels[idx]


def print_predictions(predictions, labels):
    # Sort to show labels in order of confidence
    top_k = predictions.argsort()[-3:][::-1]
    for node_id in top_k:
        human_string = labels[node_id]
        score = predictions[node_id]
        print('%s (score = %.5f)' % (human_string, score))


def load_graph(filename=DEFAULT_GRAPH_FILE):
    print("Loading graph: ", filename)
    with tf.gfile.FastGFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename=DEFAULT_LABELS_FILE):
    print("Loading labels: ", filename)
    labels = [line.rstrip() for line in tf.gfile.GFile(filename)]
    for label in labels:
        if not (label.startswith("_") and label.endswith("_")):
            print(label)
    return labels


INPUT_LAYER_NAME = "decoded_sample_data:0"
OUTPUT_LAYER_NAME = "labels_softmax:0"
SAMPLE_RATE_NAME = "decoded_sample_data:1"


def run_graph(sound_data, sample_rate):
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name(OUTPUT_LAYER_NAME)
        predictions, = sess.run(softmax_tensor, {INPUT_LAYER_NAME: sound_data, SAMPLE_RATE_NAME: sample_rate})
        return predictions
