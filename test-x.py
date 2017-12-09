import numpy as np

a1 = np.array(range(0, 6))
print(a1)
a2 = np.array(range(6, 10))
print(a2)
frames = []
frames.append(a1)
frames.append(a2)
print(frames)
frames = np.hstack(frames)
print(frames)
frames = np.concatenate([frames, np.zeros(2)])
#frames = frames[3:]
print(frames)
frames = np.reshape(frames, (12, 1))
print(frames)
