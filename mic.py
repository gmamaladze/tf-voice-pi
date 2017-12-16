import abc
import numpy as np
import struct
import audioop
import configuration
import threading

try:
    # noinspection PyPep8Naming
    import Queue as queue
except ImportError:
    # noinspection PyUnresolvedReferences
    import queue

if configuration.is_raspberry():
    import alsaaudio
else:
    import pyaudio

CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max
CHUNK_SIZE = 1000


def create_mic(config):
    if configuration.is_raspberry():
        return MicAlsa(config.device_sampling_rate, config.device_name)
    else:
        return MicPortAudio(config.device_sampling_rate)


class Mic(metaclass=abc.ABCMeta):

    def __init__(self, device_sampling_rate):
        self.state = None
        self.device_sampling_rate = device_sampling_rate
        self.end = False
        self.queue = queue.Queue()
        self.state = None

    @abc.abstractmethod
    def get_mic_data_async(self):
        pass

    @abc.abstractmethod
    def get_mic_data(self):
        pass

    def to_float(self, data):
        chunk, self.state = audioop.ratecv(data, 2, 1, self.device_sampling_rate, RATE, self.state)
        data_int = struct.unpack('<' + 'h' * (len(chunk) // 2), chunk)
        data_float = np.true_divide(data_int, MAX_INT16)
        return data_float


def get_stream(p, callback):
    return p.open(format=pyaudio.paInt16,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK_SIZE,
                  stream_callback=callback)


class MicPortAudio(Mic):

    def __init__(self, device_sampling_rate):
        Mic.__init__(self, device_sampling_rate)

    # noinspection PyUnusedLocal
    def callback(self, in_data, frame_count, time_info, status):
        data_float = self.to_float(in_data)
        self.queue.put(data_float)
        return in_data, pyaudio.paAbort if self.end else pyaudio.paContinue

    def get_mic_data_async(self):
        p = pyaudio.PyAudio()
        stream = get_stream(p, self.callback)
        stream.start_stream()
        while not self.end:
            yield self.queue.get()

        stream.stop_stream()
        stream.close()
        p.terminate()
        self.queue.join()

    def get_mic_data(self):
        p = pyaudio.PyAudio()
        stream = get_stream(p, None)

        while not self.end:
            chunk = stream.read(CHUNK_SIZE)
            yield self.to_float(chunk)

        stream.close()
        p.terminate()


class MicAlsa(Mic):

    def __init__(self, device_sampling_rate, device_name):
        Mic.__init__(self, device_sampling_rate)
        self.device_name = device_name

    def get_mic_data_async(self):
        inp = self.get_input_stream(self.device_name)
        producer = threading.Thread(target=lambda: self.worker(inp))
        producer.daemon = True
        producer.start()

        while not self.end:
            yield self.queue.get()

        inp.close()
        self.queue.join()

    def get_mic_data(self):
        inp = self.get_input_stream(self.device_name)
        while not self.end:
            l, data = inp.read()
            if l > 0:
                data_float = self.to_float(data)
                yield data_float
            else:
                if l < 0:
                    # print("Buffer overflow")
                    pass
        inp.close()

    def get_input_stream(self, device):
        stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)
        stream.setchannels(1)
        stream.setrate(RATE)
        stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        stream.setperiodsize(CHUNK_SIZE * self.device_sampling_rate // RATE)
        return stream

    def worker(self, inp):
        while not self.end:
            l, data = inp.read()
            if l > 0:
                data_float = self.to_float(data)
                self.queue.put(data_float)


class MicFromFile(Mic):
    def get_mic_data_async(self):
        pass

    def get_mic_data(self):
        pass
