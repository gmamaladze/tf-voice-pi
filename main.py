import os
import commands

isRaspberryPi = (os.uname()[4][:3] == 'arm')
print("Is raspberry pi:", isRaspberryPi)

if isRaspberryPi:
    import mic_pi as mic
else:
    import mic


def print_labels(threshold):
    labels_stream = \
            commands.get_labels(mic.get_mic_data(1000), threshold)

    for current_label in labels_stream:
        print(current_label)

#threshold = commands.calibrate_silence(mic.get_mic_data(400))
threshold = .00001
print_labels(threshold)
