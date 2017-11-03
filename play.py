import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1000
MAX_INT16 = np.iinfo(np.int16).max

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

for i in range(0, 18):
    print(i)
    f = open(str(i) + ".raw", "rb")
    with f:
        data = f.read()
        data_float = np.frombuffer(data, dtype=np.float)
        data_scaled = data_float * MAX_INT16
        data_int = data_scaled.astype(int)
        buff = memoryview(data_int).tobytes()
        stream.write(buff)

stream.stop_stream()
stream.close()

p.terminate()
