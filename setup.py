import configuration
import mic
import voicecmd
import numpy as np


def select_device(current_value):
    import alsaaudio
    print("----------CAPTURE DEVICES----------")
    capture_devices = alsaaudio.pcms(alsaaudio.PCM_CAPTURE)
    return get_user_choice(current_value, capture_devices)


def device_test(current_config):
    print("----------DEVICE TEST----------")
    user_input = input("Do you want to test microphone '{}' (Y/N)?".format(current_config.device_name))
    if user_input.lower() != "y":
        return
    get_frame_mean_value(current_config)


def get_frame_mean_value(current_config):
    audio_in = mic.create_mic(current_config)
    raw_stream = \
        voicecmd.get_labels(
            audio_in.get_mic_data_async())

    frame_means = [0]*(10 * 16)
    counter = 0
    for idx, score, label, first in raw_stream:
        mean = np.sum(np.absolute(first))
        frame_means[counter] = mean
        display_value = min(int(mean), 80)
        print("#" * display_value)
        counter += 1
        if counter == len(frame_means):
            # remove extrema
            return (sum(frame_means) - max(frame_means) - min(frame_means)) / (counter-2)


def select_sampling_rate(current_value):
    print("----------SAMPLE RATES----------")
    possible_rates = ["16000", "32000", "44100", "48000"]
    return int(get_user_choice(current_value, possible_rates))


def calibrate_silence_threshold(current_value, current_config):
    print("----------SILENCE THRESHOLD----------")
    print("Current threshold is '{}'.".format(current_value))
    while True:
        user_input = input("Do you want to recalibrate '{}' (Y/N)?".format(current_value))
        if user_input.lower() != "y":
            break
        current_value = get_frame_mean_value(current_config)
    return current_value


def get_user_choice(current_value, possible_values):
    for i in range(0, len(possible_values) - 1):
        print(str(i + 1) + " - " + possible_values[i])
    print("-----------------------------------")
    user_input = input("Type a number or ENTER to keep '{}':".format(current_value))
    if user_input == "":
        return current_value
    index = int(user_input) - 1
    return possible_values[index]


config = configuration.load()
print("Current configuration:")
config.print_config()

if configuration.is_raspberry():
    print("Select your input device, microphone.")
    config.device_name = select_device(config.device_name)
print("Select the smallest sample rate supported by your device higher or equal to 16000")
config.device_sampling_rate = select_sampling_rate(config.device_sampling_rate)
device_test(config)

config.silence_threshold = calibrate_silence_threshold(config.silence_threshold, config)
print("----------SAVE CONFIGURATION----------")
print("Current configuration:")
config.print_config()
should_save = input("Do you want to save this configuration?")
if should_save.lower() == "y":
    config.save()
    print("Configuration saved.")
