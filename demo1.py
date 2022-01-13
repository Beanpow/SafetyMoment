import numpy as np
import scipy.signal
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import copy

a = np.load('./data/key_data/1-11/detect_dyj2022-01-11_16-34-39.npy')


rawMomentData, rawAngleData = a[:, 0:4], a[:, -1] 


assert(len(rawAngleData) == len(rawMomentData))

rawAngleData = rawAngleData.reshape(rawAngleData.shape[0], 1)
combinedData = np.hstack((rawMomentData, rawAngleData))
print(combinedData[:400, -1].argsort())
combinedData = combinedData[combinedData[:, -1].argsort()]
print(combinedData.shape)

lastValue = combinedData[0, -1]
sumValue = combinedData[0, 0:4].reshape(1,4)
avarageSafetyMoment = []
for i in range(1, combinedData.shape[0]):
    if abs(combinedData[i, -1] - lastValue) < 0.01:
        sumValue = np.vstack((sumValue, combinedData[i, 0:4]))
    else:
        avarag = np.mean(sumValue, axis=0)
        var = np.std(sumValue, axis=0)
        avarageSafetyMoment.append(np.hstack((avarag, var, lastValue)))
        lastValue = combinedData[i, -1]
        sumValue = combinedData[i, 0:4].reshape(1,4)

combinedData = np.array(avarageSafetyMoment)
print(combinedData.shape)


# for i in range(1, combinedData.shape[0]):
#     for j in range(4):
#         if combinedData[i, 4+j] < 4:
#             # combinedData[i, 4+j] = combinedData[i - 1, 4+j]
#             combinedData[i, 4+j] = 4
# for i in range(8):
#     combinedData[:, i] = scipy.signal.savgol_filter(combinedData[:, i], 51, 3)



color = cm.viridis(0.7)
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
key_item = 1
combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)
ax1.plot(range(len(combinedData[:, key_item])), combinedData[:, key_item], color=color)
r1 = list(map(lambda x: x[0]-3 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: x[0]+2 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax1.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=color, alpha=0.2)
plt.ylabel('Torque (N·m)')
# ax1.title('Patient Torque')

key_item = 3

# temp = list(combinedData[:, key_item])
# temp.shift(len(combinedData) // 2)
# combinedData[:, key_item] = np.array(temp)


temp = copy.copy(combinedData[:len(combinedData) // 2, key_item ])
combinedData[:len(combinedData) // 2, key_item ] = combinedData[len(combinedData) // 2:, key_item ]
combinedData[len(combinedData) // 2:, key_item ] = temp

temp = copy.copy(combinedData[:len(combinedData) // 2, key_item + 4])
combinedData[:len(combinedData) // 2, key_item + 4 ] = combinedData[len(combinedData) // 2:, key_item + 4]
combinedData[len(combinedData) // 2:, key_item + 4] = temp

combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)

# combinedData[len(combinedData) // 2:, key_item ], combinedData[:len(combinedData) // 2, key_item ]  = combinedData[:len(combinedData) // 2, key_item ] ,combinedData[len(combinedData) // 2:, key_item ]
# combinedData[len(combinedData) // 2:, key_item + 4], combinedData[:len(combinedData) // 2, key_item  + 4]  = combinedData[:len(combinedData) // 2, key_item  + 4] ,combinedData[len(combinedData) // 2:, key_item  + 4]
# plt.plot(combinedData[:, key_item], color=color)

ax1.plot(range(len(combinedData[:, key_item])), -1 * combinedData[:, key_item], color=cm.viridis(0.4))
r1 = list(map(lambda x: -1 * (x[0]-3 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: -1 * (x[0]+2 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax1.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=cm.viridis(0.4), alpha=0.2)
ax1.legend(['Right Hip', 'Left Hip'])
ax1.set_ylabel('Torque (N·m)')
ax1.set_title('Patient Torque')


key_item = 0
combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)
ax3.plot(range(len(combinedData[:, key_item])), combinedData[:, key_item], color=color)
r1 = list(map(lambda x: x[0]-3 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: x[0]+2 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax3.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=color, alpha=0.2)
plt.ylabel('Torque (N·m)')


key_item = 2

# temp = list(combinedData[:, key_item])
# temp.shift(len(combinedData) // 2)
# combinedData[:, key_item] = np.array(temp)


temp = copy.copy(combinedData[:len(combinedData) // 2, key_item ])
combinedData[:len(combinedData) // 2, key_item ] = combinedData[len(combinedData) // 2:, key_item ]
combinedData[len(combinedData) // 2:, key_item ] = temp

temp = copy.copy(combinedData[:len(combinedData) // 2, key_item + 4])
combinedData[:len(combinedData) // 2, key_item + 4 ] = combinedData[len(combinedData) // 2:, key_item + 4]
combinedData[len(combinedData) // 2:, key_item + 4] = temp

combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)

# combinedData[len(combinedData) // 2:, key_item ], combinedData[:len(combinedData) // 2, key_item ]  = combinedData[:len(combinedData) // 2, key_item ] ,combinedData[len(combinedData) // 2:, key_item ]
# combinedData[len(combinedData) // 2:, key_item + 4], combinedData[:len(combinedData) // 2, key_item  + 4]  = combinedData[:len(combinedData) // 2, key_item  + 4] ,combinedData[len(combinedData) // 2:, key_item  + 4]
# plt.plot(combinedData[:, key_item], color=color)

ax3.plot(range(len(combinedData[:, key_item])), -1 * combinedData[:, key_item], color=cm.viridis(0.4))
r1 = list(map(lambda x: -1 * (x[0]-3 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: -1 * (x[0]+2 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax3.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=cm.viridis(0.4), alpha=0.2)
ax3.legend(['Right Knee', 'Left Knee'])
ax3.set_ylabel('Torque (N·m)')












a = np.load('./data/key_data/1-12/detect_hkb2022-01-12_16-56-02.npy')
a = a[:,:2500]


rawMomentData, rawAngleData = a[:, 0:4], a[:, -1] 


assert(len(rawAngleData) == len(rawMomentData))

rawAngleData = rawAngleData.reshape(rawAngleData.shape[0], 1)
combinedData = np.hstack((rawMomentData, rawAngleData))
print(combinedData[:400, -1].argsort())
combinedData = combinedData[combinedData[:, -1].argsort()]
print(combinedData.shape)

lastValue = combinedData[0, -1]
sumValue = combinedData[0, 0:4].reshape(1,4)
avarageSafetyMoment = []
for i in range(1, combinedData.shape[0]):
    if abs(combinedData[i, -1] - lastValue) < 0.01:
        sumValue = np.vstack((sumValue, combinedData[i, 0:4]))
    else:
        avarag = np.mean(sumValue, axis=0)
        var = np.std(sumValue, axis=0)
        avarageSafetyMoment.append(np.hstack((avarag, var, lastValue)))
        lastValue = combinedData[i, -1]
        sumValue = combinedData[i, 0:4].reshape(1,4)

combinedData = np.array(avarageSafetyMoment)
print(combinedData.shape)


# for i in range(1, combinedData.shape[0]):
#     for j in range(4):
#         if combinedData[i, 4+j] < 4:
#             # combinedData[i, 4+j] = combinedData[i - 1, 4+j]
#             combinedData[i, 4+j] = 4
# for i in range(8):
#     combinedData[:, i] = scipy.signal.savgol_filter(combinedData[:, i], 51, 3)



color = cm.viridis(0.7)
key_item = 1
combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)
ax2.plot(range(len(combinedData[:, key_item])), combinedData[:, key_item], color=color)
r1 = list(map(lambda x: x[0]-3 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: x[0]+2 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax2.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=color, alpha=0.2)
plt.ylabel('Torque (N·m)')
# ax1.title('Patient Torque')

key_item = 3

# temp = list(combinedData[:, key_item])
# temp.shift(len(combinedData) // 2)
# combinedData[:, key_item] = np.array(temp)


temp1 = copy.copy(combinedData[:len(combinedData) // 2, key_item ])
temp2 = copy.copy(combinedData[len(combinedData) // 2:, key_item ])
combinedData[:, key_item] = np.hstack((temp2, temp1))

temp1 = copy.copy(combinedData[:len(combinedData) // 2, key_item + 4 ])
temp2 = copy.copy(combinedData[len(combinedData) // 2:, key_item + 4 ])
combinedData[:, key_item + 4] = np.hstack((temp2, temp1))

combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)

# temp = copy.copy(combinedData[:len(combinedData) // 2, key_item + 4])
# combinedData[:len(combinedData) // 2, key_item + 4 ] = combinedData[len(combinedData) // 2:, key_item + 4]
# combinedData[len(combinedData) // 2:, key_item + 4] = temp

# combinedData[len(combinedData) // 2:, key_item ], combinedData[:len(combinedData) // 2, key_item ]  = combinedData[:len(combinedData) // 2, key_item ] ,combinedData[len(combinedData) // 2:, key_item ]
# combinedData[len(combinedData) // 2:, key_item + 4], combinedData[:len(combinedData) // 2, key_item  + 4]  = combinedData[:len(combinedData) // 2, key_item  + 4] ,combinedData[len(combinedData) // 2:, key_item  + 4]
# plt.plot(combinedData[:, key_item], color=color)

ax2.plot(range(len(combinedData[:, key_item])), -1 * combinedData[:, key_item], color=cm.viridis(0.4))
r1 = list(map(lambda x: -1 * (x[0]-3 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: -1 * (x[0]+2 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax2.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=cm.viridis(0.4), alpha=0.2)
ax2.legend(['Right Hip', 'Left Hip'])
ax2.set_ylabel('Torque (N·m)')
ax2.set_title('Healthy People Torque')


key_item = 0
combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)
ax4.plot(range(len(combinedData[:, key_item])), combinedData[:, key_item], color=color)
r1 = list(map(lambda x: x[0]-3 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: x[0]+2 * x[1], zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax4.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=color, alpha=0.2)
plt.ylabel('Torque (N·m)')


key_item = 2

# temp = list(combinedData[:, key_item])
# temp.shift(len(combinedData) // 2)
# combinedData[:, key_item] = np.array(temp)


temp1 = copy.copy(combinedData[:len(combinedData) // 2, key_item ])
temp2 = copy.copy(combinedData[len(combinedData) // 2:, key_item ])
combinedData[:, key_item] = np.hstack((temp2, temp1))

temp1 = copy.copy(combinedData[:len(combinedData) // 2, key_item + 4 ])
temp2 = copy.copy(combinedData[len(combinedData) // 2:, key_item + 4 ])
combinedData[:, key_item + 4] = np.hstack((temp2, temp1))

combinedData[:, key_item] = scipy.signal.savgol_filter(combinedData[:, key_item], 51, 3)
combinedData[:, key_item + 4] = scipy.signal.savgol_filter(combinedData[:, key_item + 4], 51, 3)

# combinedData[len(combinedData) // 2:, key_item ], combinedData[:len(combinedData) // 2, key_item ]  = combinedData[:len(combinedData) // 2, key_item ] ,combinedData[len(combinedData) // 2:, key_item ]
# combinedData[len(combinedData) // 2:, key_item + 4], combinedData[:len(combinedData) // 2, key_item  + 4]  = combinedData[:len(combinedData) // 2, key_item  + 4] ,combinedData[len(combinedData) // 2:, key_item  + 4]
# plt.plot(combinedData[:, key_item], color=color)

ax4.plot(range(len(combinedData[:, key_item])), -1 * combinedData[:, key_item], color=cm.viridis(0.4))
r1 = list(map(lambda x: -1 * (x[0]-3 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
r2 = list(map(lambda x: -1 * (x[0]+2 * x[1]), zip(combinedData[:, key_item], combinedData[:, key_item + 4])))
ax4.fill_between(range(len(combinedData[:, key_item])), r1, r2, color=cm.viridis(0.4), alpha=0.2)
ax4.legend(['Right Knee', 'Left Knee'])
ax4.set_ylabel('Torque (N·m)')





plt.show()
