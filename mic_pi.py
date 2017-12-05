import alsaaudio
import time
import numpy as np
import struct
import mic_device

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max
CHUNK_SIZE = 1000
DEFAULT_DEVICE = "sysdefault:CARD=Device" #None

end = False


def get_mic_data(chunk_size=CHUNK_SIZE, device=DEFAULT_DEVICE):
    if device is None:
        device = mic_device.select_device()
    print("Initializing audio.")
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)

    chunk_byte_count = chunk_size * 2
    inp.setperiodsize(CHUNK_SIZE)
    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    data_buffer = ""
    while not end:
        l, data = inp.read()
        if l:
            data_buffer += data
            while len(data_buffer) >= chunk_byte_count:
                chunk = data_buffer[:chunk_byte_count]
                data_int = struct.unpack('<'+'h'*chunk_size, chunk)
                data_float = np.true_divide(data_int, MAX_INT16)
                yield data_float
                data_buffer = data_buffer[chunk_byte_count:]
        else:
            time.sleep(.001)
