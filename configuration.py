import json
import os

KEY_SILENCE_THRESHOLD = "silence_threshold"

KEY_DEVICE_NAME = "device_name"
KEY_DEVICE_SAMPLING_RATE = "device_sampling_rate"

DEFAULT_DEVICE_SAMPLING_RATE = 44100
DEFAULT_DEVICE_NAME = "hw:CARD=Device,DEV=0"
DEFAULT_FILE_NAME = "config.json"


def is_raspberry():
    return os.uname()[4][:3] == 'arm'


def load(file_name=DEFAULT_FILE_NAME):
    config = Configuration()
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            config.set_data(data)
    finally:
        return config


class Configuration:
    def __init__(self):
        pass

    device_sampling_rate = DEFAULT_DEVICE_SAMPLING_RATE
    device_name = DEFAULT_DEVICE_NAME
    silence_threshold = .0

    def save(self, file_name=DEFAULT_FILE_NAME):
        data = self.get_data()
        with open(file_name, 'w') as f:
            json.dump(data, f)

    def get_data(self):
        return {
            KEY_DEVICE_SAMPLING_RATE: str(self.device_sampling_rate),
            KEY_DEVICE_NAME: str(self.device_name),
            KEY_SILENCE_THRESHOLD: str(self.silence_threshold)
        }

    def set_data(self, data):
        raw_sampling_rate = data.get(KEY_DEVICE_SAMPLING_RATE, DEFAULT_DEVICE_SAMPLING_RATE)
        self.device_sampling_rate = parse_int(raw_sampling_rate, DEFAULT_DEVICE_SAMPLING_RATE)
        self.device_name = data.get(KEY_DEVICE_NAME, DEFAULT_DEVICE_NAME)
        raw_silence_threshold = data.get(KEY_SILENCE_THRESHOLD, 0)
        self.silence_threshold = parse_float(raw_silence_threshold, 0)

    def print_config(self):
        print(self.get_data())


def parse_float(s, default_value):
    try:
        res = float(str(s))
        if type(res) == float:
            return res
    except ValueError:
        pass
    return default_value


def parse_int(s, default_value):
    try:
        res = int(str(s))
        if type(res) == int:
            return res
    except ValueError:
        pass
    return default_value
