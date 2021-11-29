from sys import platform
import numpy as np
import matplotlib.pyplot as plt


a = np.load('rawdata copy 4.npy')
print(a)
plt.plot(a[:, 0])
plt.plot(a[:, 1])
plt.plot(a[:, 2] * 10)
plt.plot(a[:, 3])
plt.legend(['1','2','3','4'])
plt.show()
