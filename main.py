import os
import voicecmd
import classify

isRaspberryPi = (os.uname()[4][:3] == 'arm')
print("Is raspberry pi:", isRaspberryPi)

if isRaspberryPi:
    import mic_pi as mic
else:
    import mic

mic.CHUNK_SIZE = 1000
voicecmd.CHUNK_SIZE = mic.CHUNK_SIZE

classifier = classify.Classifier()

max_silence = \
    voicecmd.calibrate_silence(
        mic.get_mic_data(),
        classifier)

threshold = max_silence * 4

labels_stream = \
    voicecmd.get_labels_simple(
        mic.get_mic_data(),
        classifier,
        threshold)

raw_stream = \
    voicecmd.get_labels_raw(
        mic.get_mic_data(),
        classifier)

simple_stream = \
    voicecmd.get_labels_batched(
        mic.get_mic_data_async(),
        classifier,
        threshold,
        5)


for idx, score, label in simple_stream:
    print(idx, score, label)



