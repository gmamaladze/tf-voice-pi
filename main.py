import os
import voicecmd
import classify

isRaspberryPi = (os.uname()[4][:3] == 'arm')
print("Is raspberry pi:", isRaspberryPi)

if isRaspberryPi:
    import mic_pi as mic
else:
    import mic

classifier = classify.Classifier()

'''
max_silence, avg_sound, max_sound = \
    voicecmd.calibrate_silence(
        mic.get_mic_data(),
        classifier)

threshold = (avg_sound - max_silence) / 4 + max_silence
'''

labels_stream = \
    voicecmd.get_labels_simple(
            mic.get_mic_data(),
            classifier)

raw_stream = \
    voicecmd.get_labels_raw(
        mic.get_mic_data(),
        classifier)

'''
for current_label in labels_stream:
    print(current_label)
'''

for idx, score, label in raw_stream:
    print(idx, score, label)
