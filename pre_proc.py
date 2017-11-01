import numpy as np


def word2int16(low_byte, high_byte):
    return int.from_bytes([low_byte, high_byte], 'big', signed=True)

MAX_INT16 = np.iinfo(np.int16).max


def encode(data_16bit):
    length = len(data_16bit) // 2
    result = np.empty(length)
    for i in range(0, length):
        index = 2 * i
        low_byte = data_16bit[index]
        high_byte = data_16bit[index + 1]
        result[i] = word2int16(low_byte, high_byte) / MAX_INT16
    return result
