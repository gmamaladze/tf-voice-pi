import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
MAX_INT16 = np.iinfo(np.int16).max
CHUNK_SIZE = 1000

end = False


def get_mic_data(chunk_size=1000, device="none"):
    print("Initializing audio.")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=chunk_size)

    dt = np.dtype(np.int16)
    dt.newbyteorder('>')

    while not end:
        data = np.array(stream.read(chunk_size))
        data_int = np.frombuffer(data, dtype=dt)
        data_float = np.true_divide(data_int, MAX_INT16)
        yield data_float

    stream.stop_stream()
    stream.close()

