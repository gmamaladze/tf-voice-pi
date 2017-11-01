from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# noinspection PyUnresolvedReferences
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio

import tensorflow as tf


class Classifier:
    def __init__(self,
                 sample_rate=16000,
                 graph_filename="conv_actions_frozen.pb",
                 label_filename="conv_actions_labels.txt"):
        load_graph(graph_filename)
        self.labels = load_labels(label_filename)
        self.sample_rate = sample_rate

    def run(self, sound_data):
        predictions = run_graph(sound_data, self.sample_rate)
        return predictions

    def get_best(self, predictions):
        idx = predictions.argmax()
        return idx, predictions[idx], self.labels[idx]

    def print_predictions(self, predictions):
        # idx = predictions.argmax()
        # Sort to show labels in order of confidence
        top_k = predictions.argsort()[-3:][::-1]
        for node_id in top_k:
            human_string = self.labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))


def load_graph(filename):
    with tf.gfile.FastGFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename):
    return [line.rstrip() for line in tf.gfile.GFile(filename)]

INPUT_LAYER_NAME = "decoded_sample_data:0"
OUTPUT_LAYER_NAME = "labels_softmax:0"
SAMPLE_RATE_NAME = "decoded_sample_data:1"


def run_graph(sound_data, sample_rate):
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name(OUTPUT_LAYER_NAME)
        predictions, = sess.run(softmax_tensor, {INPUT_LAYER_NAME: sound_data, SAMPLE_RATE_NAME: sample_rate})
        return predictions
