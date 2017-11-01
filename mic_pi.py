import alsaaudio
import numpy as np

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max


end = False


def get_mic_data(chunk_size, device="sysdefault:CARD=Device"):
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device)
    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    inp.setperiodsize(chunk_size)

    dt = np.dtype(np.int16)
    dt.newbyteorder('>')

    while not end:
        l, data = inp.read()
        if l > 0:
            data = np.array(data)
            data_int = np.frombuffer(data, dtype=dt)
            data_float = np.true_divide(data_int, MAX_INT16)
            yield data_float
