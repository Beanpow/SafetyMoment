from sys import platform
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm

a = np.load('./data/rawdata_zc2021-12-12_14-46-38.npy')

a = a[27300: 27900]

print(a[:,0])
for i in range(4):
    a[:, i] = scipy.signal.savgol_filter(a[:, i], 101, 3)

color = cm.viridis(0.7)
f, ax = plt.subplots(1,1)
ax.plot(range(len(a[:, 0])), a[:, 0], color=color)
r1 = list(map(lambda x: x[0]-x[1], zip(a[:, 0], 5 * np.ones((len(a[:,0]), 1)) )))
r2 = list(map(lambda x: x[0]+x[1], zip(a[:, 0], 5 * np.ones((len(a[:,0]), 1)) )))

# print(5 * np.ones((len(a[:,0]), 1)))

print(len(r1))
print(r1[0])

ax.fill_between(range(len(a[:, 0])), r1, r2, color=color, alpha=0.2)
plt.show()




# print(a)
plt.plot(a[:, 0])
plt.plot(a[:, 1])
plt.plot(a[:, 2])
plt.plot(a[:, 3])
plt.legend(['left hip','left knee','right hip','right knee'])
plt.ylabel('torque (N·m)')
plt.show()
