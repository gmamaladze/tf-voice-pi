import alsaaudio
import time
import numpy as np
import struct
import mic_device
import audioop

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max
CHUNK_SIZE = 1000
DEFAULT_DEVICE = "hw:CARD=Device,DEV=0" #None

end = False


def get_mic_data(chunk_size=CHUNK_SIZE, device=DEFAULT_DEVICE):
    if device is None:
        device = mic_device.select_device()
    print("Initializing audio.")
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)

    chunk_byte_count = chunk_size * 2
    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(160)

    state = None

    data_buffer = ""
    while not end:
        l, data = inp.read()
        if l>0:
            data1, state = audioop.ratecv(data, 2, 1, 44100, 16000, state)
            data_buffer += data1
            while len(data_buffer) >= chunk_byte_count:
                chunk = data_buffer[:chunk_byte_count]
                data_int = struct.unpack('<'+'h'*chunk_size, chunk)
                data_float = np.true_divide(data_int, MAX_INT16)
                yield data_float
                data_buffer = data_buffer[chunk_byte_count:]
        else:
            pass
            #time.sleep(.001)
