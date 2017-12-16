import mic
import voicecmd
import classify
import configuration
import gate

config = configuration.load()
audio_in = mic.create_mic(config)

classifier = classify.Classifier()


def should_skip(averages):
    is_silence = voicecmd.is_silence(averages, config.silence_threshold * 2)
    return is_silence or not voicecmd.is_gauss_like_distribution(averages)


labels_confident = \
    voicecmd.get_labels(
        audio_in.get_mic_data_async(),
        classify.Classifier(),
        should_skip,
        gate.HitCountGate())

labels_quick = \
    voicecmd.get_labels(
        audio_in.get_mic_data_async(),
        classify.Classifier(),
        should_skip,
        gate.SimpleGate(.4))

labels_paranoid = \
    voicecmd.get_labels(
        audio_in.get_mic_data_async(),
        classify.Classifier(),
        should_skip,
        gate.HitCountGate([.9, .9, .4]))


for idx, score, label, _ in labels_confident:
    print(idx, score, label)
