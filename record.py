import pyaudio
import Classifier
import itertools
from numpy import array

CHUNK = 4000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
classifier = Classifier.Classifier()

FRAME_COUNT = int(RATE / CHUNK * RECORD_SECONDS)


def decode(low_byte, high_byte):
    data_int_16  = int.from_bytes([low_byte, high_byte], 'little', signed = True);
    data_normalized = data_int_16 / 32767
    return data_normalized


while True:
    data = stream.read(CHUNK)
    norm = [decode(data[2*i], data[2*i+1]) for i in range(0, CHUNK)];
    frames.append(norm)
    while (len(frames) > FRAME_COUNT):
        frames.pop(0);
    if (len(frames) == FRAME_COUNT):
        wav = list(itertools.chain.from_iterable(frames))
        input = array(wav).reshape(RATE, 1);
        result, confidence, idx = classifier.run(input, RATE)
        if (idx>1 and confidence>1):
            print(result, confidence)
            frames = []

stream.stop_stream()
stream.close()