import alsaaudio
import time
import numpy as np

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max
CHUNK_SIZE = 1000
DEFAULT_DEVICE = "sysdefault:CARD=Device"

end = False


def get_mic_data_asis(device=DEFAULT_DEVICE):
    print("Initializing audio.")
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)
    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    inp.setperiodsize(160)

    while not end:
        l, data = inp.read()
        if l > 0:
            yield np.array(data)
        else:
            time.sleep(.001)


def get_mic_data(chunk_size=CHUNK_SIZE, device=DEFAULT_DEVICE):
    dt = np.dtype(np.int16)
    dt.newbyteorder('>')

    data_buffer = np.array([], dtype=np.float)
    for data in get_mic_data_asis(device=device):
        data_int = np.frombuffer(data, dtype=dt)
        data_float = np.true_divide(data_int, MAX_INT16)
        data_buffer = np.concatenate([data_buffer, data_float])
        if len(data_buffer) < chunk_size:
            time.sleep(.001)
        while len(data_buffer) >= chunk_size:
            yield data_buffer[0:chunk_size]
            data_buffer = data_buffer[chunk_size:]
