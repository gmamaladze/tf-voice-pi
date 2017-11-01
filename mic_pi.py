import alsaaudio
import numpy as np

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max


end = False


def get_mic_data(chunk_size):
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, "sysdefault:CARD=Device")
    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    inp.setperiodsize(chunk_size // 2)

    dt = np.dtype(np.int16)
    dt.newbyteorder('>')

    while not end:
        l, data = inp.read()
        if l:
            data = np.array(data)
            yield np.frombuffer(data, dtype=dt) / MAX_INT16
