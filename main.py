import os
import record

isRaspberryPi = (os.uname()[4][:3] == 'arm')
print("Is raspberry pi:", isRaspberryPi)

if isRaspberryPi:
    import mic_pi as mic
else:
    import mic


def print_labels():
    labels_stream = \
        record.get_labels(
            record.get_sound_data(
                mic.get_mic_data(record.CHUNK)))

    for current_label in labels_stream:
        print(current_label)


def print_noise():
    noise_stream = \
            record.get_sound_data(
                mic.get_mic_data(record.CHUNK))

    for noise in noise_stream:
        print(len(noise))
