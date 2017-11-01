import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

end = False


def get_mic_data(chunk_size):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=chunk_size)

    while not end:
        data = stream.read(chunk_size)
        yield data

    stream.stop_stream()
    stream.close()
