import alsaaudio

FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 16000

end = False


def get_mic_data(chunk_size):
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, "sysdefault:CARD=Device'")
    inp.setchannels(CHANNELS)
    inp.setrate(RATE)
    inp.setformat(FORMAT)

    inp.setperiodsize(chunk_size // 2)

    while not end:
        l, data = inp.read()
        if l:
            yield data
