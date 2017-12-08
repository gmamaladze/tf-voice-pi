import threading
import Queue

import alsaaudio
import numpy as np
import struct
import audioop

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
    stream.setrate(44100)
    stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    stream.setperiodsize(CHUNK_SIZE * 44100 // 16000)
    return stream


inp = get_input_stream(DEFAULT_DEVICE)


def worker():
    state = None
    while not end:
        l, data = inp.read()
        if l > 0:
            chunk, state = audioop.ratecv(data, 2, 1, 44100, 16000, state)
            data_int = struct.unpack('<' + 'h' * (len(chunk) // 2), chunk)
            data_float = np.true_divide(data_int, MAX_INT16)
            queue.put(data_float)


def get_mic_data():
    producer = threading.Thread(target=worker)
    producer.daemon = True
    producer.start()

    while not end:
        if queue.qsize() > 2:
            print("WARNING: Sound buffer overrun!", queue.qsize())
        yield queue.get()
