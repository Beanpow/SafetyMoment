import time
import numpy as np
from AngleManager import AngleManager
import os
from MomentManager import MomentManager
import matplotlib.pyplot as plt

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

import scipy.signal
sns.set_style('whitegrid')

class SafetyMomentManager:
    def __init__(self, userName, momentManager, angelManager, sampleRate=20, autoPlot = False):
        '''
        userName:       The User Name
        sampleRate:     Hz, the value must less than 4, because of the momentManager have the limited rate
        '''
        self.userName = userName
        self.sampleRate = sampleRate
        self.autoPlot = autoPlot

        self.momentManager = momentManager
        self.angelManager = angelManager

        

    def DetectMoment(self, autoPlot = False):
        '''
        detect the moment is safe or not
        '''
        angelList = []
        momentList = None
        color = cm.viridis(0.7)
        xRangeConst = 50
        xRange = 50

        if autoPlot:
            fig = plt.figure(1)
        
        if self.SafetyMoment is None:
            print("You have not record the raw data, please record the raw data first!")
            return

        try:
            while True:
                if autoPlot:
                    fig.clf()
                    ax1 = fig.add_subplot(221)
                moment = self.momentManager.GetAllMoments()[0]
                angel = self.angelManager.getInfo()


                if angel[2] == 1:
                    checkResult, idx = self.CheckMoment(np.hstack((moment, angel[1])))

                    if type(momentList) != type(np.array([[1,2,3,4]])):
                        momentList = np.array(np.hstack((moment, self.SafetyMoment[idx, 0:8]))).reshape(1, 12)
                    else:
                        momentList = np.vstack((momentList, np.hstack((moment, self.SafetyMoment[idx, 0:8]))))
                    angelList.append(angel[1])

                    if autoPlot:

                        xRange = momentList.shape[0] if momentList.shape[0] <= xRangeConst else xRangeConst
                        
                        
                        # print(type(momentList[-xRange:, 0]),momentList[-xRange:, 0])
                        ax1.plot(range(momentList[-xRange:, 0].shape[0]), momentList[-xRange:, 0], color=color)
                        r1 = list(map(lambda x: x[0]-x[1], zip(momentList[-xRange:, 4], momentList[-xRange:, 8])))
                        r2 = list(map(lambda x: x[0]+x[1], zip(momentList[-xRange:, 4], momentList[-xRange:, 8])))
                        ax1.fill_between(range(momentList[-xRange:, 0].shape[0]), r1, r2, color=color, alpha=0.2)
                        plt.pause(0.01)


                        

                    # if not checkResult:
                        # self.angelManager.emergencyStopButton()
                else:
                    print('angel paresed failed!')
        except KeyboardInterrupt:
            print("Program Terminated!")

    def CheckMoment(self, momentAndAngel):
        '''
        check the moment is safe or not
        '''
        dangerousRate = 3
        momentAndAngel = momentAndAngel.reshape(1, momentAndAngel.shape[0])

        idx = np.abs(self.SafetyMoment[:, -1] - momentAndAngel[:, -1]).argmin()
        for i in range(4):
            if abs(self.SafetyMoment[idx, i] - momentAndAngel[0, i]) > dangerousRate * self.SafetyMoment[idx, 4+i]:
                return False, idx

        return True, idx


    def plotPic(self):
        '''
        plot the safety moment data
        '''
        color = cm.viridis(0.7)
        f, ax = plt.subplots(1,1)
        ax.plot(range(len(self.SafetyMoment[:, 0])), self.SafetyMoment[:, 0], color=color)
        r1 = list(map(lambda x: x[0]-x[1], zip(self.SafetyMoment[:, 0], self.SafetyMoment[:, 4])))
        r2 = list(map(lambda x: x[0]+x[1], zip(self.SafetyMoment[:, 0], self.SafetyMoment[:, 4])))
        ax.fill_between(range(len(self.SafetyMoment[:, 0])), r1, r2, color=color, alpha=0.2)
        plt.show()


    # TODO: maybe the 5 should changed 
    def GetSafetyMoment(self):
        # path = './data/' + self.userName + '_Safety.npy'
        path = './data/combinedData.npy'

        if os.path.exists(path):
            choise = input("Found Existing Safety Data, Do you want to load from existing data?[y]/n:")
            if choise == '' or choise == 'y' or choise == 'Y':
                self.SafetyMoment = np.load(path)

                for i in range(1, self.SafetyMoment.shape[0]):
                    for j in range(4):
                        if self.SafetyMoment[i, 4+j] < 5:
                            self.SafetyMoment[i, 4+j] = self.SafetyMoment[i - 1, 4+j]
                            # self.SafetyMoment[i, 4+j] = 5
                
                # scipy.signal.savgol_filter(self.SafetyMoment, )

            else:
                self.SafetyMoment = self._ProcessRawSafetyMoment()
        
        else:
            input("You will record the raw data, press any key to continue...press CTRL-C to terminate")

            self.SafetyMoment = self._ProcessRawSafetyMoment()

    # TODO
    def _ProcessRawSafetyMoment(self):
        '''
        process raw safety moment data to get the final safety moment data throught Least squares method 
        '''
        # self.angelManager.autoStartWalk()
        rawMomentData, rawAngleData = self._RecordRawSafetyMoment()
        assert(len(rawAngleData) == len(rawMomentData))

        rawAngleData = rawAngleData.reshape(rawAngleData.shape[0], 1)
        combinedData = np.hstack((rawMomentData, rawAngleData))
        print(combinedData)
        combinedData = combinedData[combinedData[:, -1].argsort()]

        lastValue = combinedData[0, -1]
        sumValue = combinedData[0, 0:4].reshape(1,4)
        avarageSafetyMoment = []
        for i in range(1, combinedData.shape[0]):
            if combinedData[i, -1] == lastValue:
                sumValue = np.vstack((sumValue, combinedData[i, 0:4]))
            else:
                avarag = np.mean(sumValue, axis=0)
                var = np.std(sumValue, axis=0)
                avarageSafetyMoment.append(np.hstack((avarag, var, lastValue)))
                lastValue = combinedData[i, -1]
                sumValue = combinedData[i, 0:4].reshape(1,4)
        
        combinedData = np.array(avarageSafetyMoment)
        print(combinedData)
        np.save('combinedData.npy', combinedData)
        return combinedData


    def _RecordRawSafetyMoment(self):
        '''
        record angle and moment 
        '''
        timeDuration = 1.0 / self.sampleRate
        momentData = []
        angleData = []

        timeLong = input("Please input how long you want to record,[60](s):")
        if timeLong == "":
            timeLong = "60"
        timeLong = int(timeLong)

        try:
            if self.autoPlot:
                plt.figure(1)
            recordStartTime = time.time()
            while(1):
                if self.autoPlot:
                    plt.clf()
                startTime = time.time()
                moment = self.momentManager.GetAllMoments()
                angel = self.angelManager.getInfo()

                if angel[2] == 1:
                    momentData.append(moment[0])
                    angleData.append(angel[1])
                else:
                    print('angel paresed failed!')
                
                endTime = time.time()
                
                assert(endTime - startTime <= timeDuration)

                # print('time stop: ', timeDuration - (endTime - startTime))

                time.sleep(timeDuration - (endTime - startTime))
                if self.autoPlot:
                    plt.plot(momentData[-100:])
                    plt.pause(0.01)
                
                if time.time() - recordStartTime > timeLong:
                    break
                print(endTime - startTime, 'remain ', timeLong - time.time() + recordStartTime)

        except KeyboardInterrupt:
            print("End the Record!")
         
        np.save('rawdata_' + self.userName + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.npy', momentData)
        return np.array(momentData), np.array(angleData)


if __name__ == "__main__":
    angleManagerPort = input("Please input angel manager port (like \"com7\"): ")
    if angleManagerPort == "":
        angleManagerPort = "com7"
        
    momentManagerPort = input("Please input moment manager port (like \"com3\"): ")
    if momentManagerPort == "":
        momentManagerPort = "com3"

    momentManager = MomentManager(momentManagerPort)
    angelManager = AngleManager(angleManagerPort)
    # momentManager = 1
    # angelManager = 2
    

    smm = SafetyMomentManager('hkb', sampleRate=38, autoPlot = False, momentManager = momentManager, angelManager = angelManager)
    smm.GetSafetyMoment()
    smm.plotPic()
    # angelManager.autoStartWalk()
    smm.DetectMoment(autoPlot = True)