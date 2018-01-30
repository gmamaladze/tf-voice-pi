import os

from tfvoicepi import classify, voicecmd, mic

isRaspberryPi = (os.uname()[4][:3] == 'arm')
print("Is raspberry pi:", isRaspberryPi)

if isRaspberryPi:
    import mic_pi as mic
    import robot
else:
    import robot_mock as robot

classifier = classify.Classifier()

max_silence, min_sound = \
    voicecmd.calibrate_silence(
        mic.get_mic_data(),
        classifier)

threshold = (min_sound - max_silence) / 3 + max_silence

labels_stream = \
    voicecmd.get_confident_labels(
        voicecmd.get_labels(
            mic.get_mic_data(),
            classifier,
            threshold))

wall_e = robot.Robot()

label_to_action = {
    "left": lambda: wall_e.left(),
    "right": lambda: wall_e.right(),
    "go": lambda: wall_e.forward(),
    "stop": lambda: wall_e.stop()
}

for current_label in labels_stream:
    action = label_to_action.get(current_label, lambda: None)
    if not action:
        continue
    action()
