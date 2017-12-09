import threading
import Queue

import alsaaudio
import numpy as np
import struct
import audioop

DEVICE_SAMPLING_RATE = 44100

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max
CHUNK_SIZE = 1000
DEFAULT_DEVICE = "hw:CARD=Device,DEV=0"  # None

end = False

queue = Queue.Queue()


def get_input_stream(device):
    print("Initializing audio.")
    stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)
    stream.setchannels(1)
    stream.setrate(RATE)
    print(stream)
    stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    stream.setperiodsize(CHUNK_SIZE * DEVICE_SAMPLING_RATE // RATE)
    return stream


inp = get_input_stream(DEFAULT_DEVICE)


def worker():
    state = None
    while not end:
        l, data = inp.read()
        if l > 0:
            chunk, state = audioop.ratecv(data, 2, 1, DEVICE_SAMPLING_RATE, RATE, state)
            data_int = struct.unpack('<' + 'h' * (len(chunk) // 2), chunk)
            data_float = np.true_divide(data_int, MAX_INT16)
            queue.put(data_float)


def get_mic_data():
    state = None
    while not end:
        l, data = inp.read()
        if l > 0:
            chunk, state = audioop.ratecv(data, 2, 1, DEVICE_SAMPLING_RATE, RATE, state)
            data_int = struct.unpack('<' + 'h' * (len(chunk) // 2), chunk)
            data_float = np.true_divide(data_int, MAX_INT16)
            yield data_float
        else:
            if l < 0:
                # print("Buffer overflow")
                pass


def get_mic_data_async():
    producer = threading.Thread(target=worker)
    producer.daemon = True
    producer.start()

    while not end:
        if queue.qsize() > 4:
            queue.empty()
            # print("WARNING: Sound buffer overrun!", queue.qsize())
        yield queue.get()
