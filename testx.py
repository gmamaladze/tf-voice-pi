import numpy as np


def word2int16(low_byte, high_byte):
    return int.from_bytes([low_byte, high_byte], 'little', signed=True)




words2int16s = np.vectorize(word2int16, otypes=[np.int])

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = [1, 2, 3, 4, 5, 6]

d = np.reshape(c, (2, 3))
print(d[1])
MAX_INT16 = np.iinfo(np.int16).max
print (words2int16s(d[0], d[1]) / MAX_INT16)
