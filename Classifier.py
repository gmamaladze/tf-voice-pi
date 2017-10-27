import tensorflow as tf

class Classifier:
    def __init__(self, graph_filename="conv_actions_frozen.pb", label_filename="conv_actions_labels.txt"):
        load_graph(graph_filename)
        self.labels=load_labels(label_filename)
        self.prev_index = -1;
        self.confidence = 0;

    def run(self, wav_data):
        index = run_graph(wav_data);
        self.confidence = self.get_confidence(index);
        self.prev_index = index;
        return self.labels[index], self.confidence;

    def get_confidence(self, index):
        if self.prev_index==index:
            return self.confidence+1;
        else:
            return 0;

def load_graph(filename):
    print(filename)
    with tf.gfile.FastGFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename):
    return [line.rstrip() for line in tf.gfile.GFile(filename)]


def run_graph(wav_data):
    INPUT_LAYER_NAME='wav_data:0',
    OUTPUT_LAYER_NAME='labels_softmax:0',

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name(OUTPUT_LAYER_NAME)
        predictions, = sess.run(softmax_tensor, {INPUT_LAYER_NAME: wav_data})
        return predictions.argmax()

