import alsaaudio


def select_device():
    print("----------CAPTURE DEVICES----------")
    capture_devices = alsaaudio.pcms(alsaaudio.PCM_CAPTURE)
    for i in range(0, len(capture_devices) - 1):
        print(str(i + 1) + " - " + capture_devices[i])
    print("-----------------------------------")
    index = input("Enter device number:") - 1
    return capture_devices[index]
