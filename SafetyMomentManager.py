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

from MutliprocessPlot import MutliprocessPlot
from multiprocessing import Pipe

import scipy.signal
sns.set_style('whitegrid')

class SafetyMomentManager:
    def __init__(self, userName, momentManager, angelManager, sampleRate=20, autoPlot = False, savePath = './data', safetyRate = 3.5):
        '''
        userName:       The User Name
        sampleRate:     Hz, the value must less than 4, because of the momentManager have the limited rate
        '''
        self.userName = userName
        self.sampleRate = sampleRate
        self.autoPlot = autoPlot

        self.momentManager = momentManager
        self.angelManager = angelManager

        self.savePath = './data/' + self.userName + '_Safety.npy'
        
        self.safetyRate = safetyRate

        self.minMoment = np.array([-10000, -10000, -10000, -10000])
        self.maxMoment = np.array([10000, 10000, 10000, 10000, ])


        self.main_conn, self.plot_conn = Pipe()
        self.plotProcess = MutliprocessPlot(self.plot_conn, drawSize=100, bound=[-60, 60])
        self.plotProcess.SetStatus(True)

    def Update(self, data):
        '''
        update the safety moment data
        '''
        data[8:] *= self.safetyRate
        self.main_conn.send(data)

        
    def DetectMoment(self):
        '''
        detect the moment is safe or not
        '''
        angelList = []
        momentList = None
        idxList = []
        indx = 0

        
        if self.SafetyMoment is None:
            print("You have not record the raw data, please record the raw data first!")
            return

        try:
            print('detecting...')
            while True:
                indx += 1
                moment = self.momentManager.GetAllMoments()[0]
                angel = self.angelManager.getInfo()


                if angel[2] == 1:
                    checkResult, idx = self.CheckMoment(np.hstack((moment, angel[1])))
                    idxList.append(idx)

                    tempdata = np.hstack((moment, self.SafetyMoment[idx, 0:8]))

                    if type(momentList) != type(np.array([[1,2,3,4]])):
                        momentList = tempdata.reshape(1, 12)
                    else:
                        momentList = np.vstack((momentList, tempdata))
                    angelList.append(angel[1])


                    if not checkResult:
                        self.angelManager.emergencyStopButton()
                        print('Emergency Stop!')
                        self.plotMomentList(momentList[-400:])
                        break
                        # return
                    
                    # Send Data to plot process
                    self.Update(tempdata)

                else:
                    print('angel paresed failed!')
                

        except KeyboardInterrupt:
            print("Program Terminated!")
        finally:
            angelList = np.array(angelList)
            angelList = np.reshape(angelList, (len(angelList), 1))
            print(momentList.shape, angelList.shape)
            np.save('./data/detect_' + self.userName + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.npy', np.hstack((momentList, angelList)))

    def CheckMoment(self, momentAndAngel):
        '''
        check the moment is safe or not
        '''
        momentAndAngel = momentAndAngel.reshape(1, momentAndAngel.shape[0])

        idx = np.abs(self.SafetyMoment[:, -1] - momentAndAngel[:, -1]).argmin()
        for i in range(4):
            if abs(self.SafetyMoment[idx, i] - momentAndAngel[0, i]) > self.safetyRate * self.SafetyMoment[idx, 4+i]:
                return False, idx

        return True, idx

    def SimpleCheckMoment(self, momentAndAngel):
        dangerousRate = 10

        if max(self.maxMoment) > 9999 or min(self.minMoment) < -9999:
            self.maxMoment = np.max(self.rawMomentData, axis=0)
            self.minMoment = np.min(self.rawMomentData, axis=0)
        

        if (momentAndAngel[:4] > dangerousRate + self.maxMoment).any() or (momentAndAngel[:4] < self.minMoment - dangerousRate).any():
            return False, 0
        
        return True, 0

            
    def plotMomentList(self, momentList):
        color = cm.viridis(0.7)
        
        plt.subplot(221)
        plt.plot(momentList[:, 0])
        plt.plot(momentList[:, 4], color = color)
        plt.fill_between(range(len(momentList[:, 0])), momentList[:, 4] + self.safetyRate * momentList[:, 8], momentList[:, 4] - self.safetyRate * momentList[:, 8], color=color, alpha=0.2)
        plt.title('left hip')

        plt.subplot(223)
        plt.plot(momentList[:, 1])
        plt.plot(momentList[:, 5], color = color)
        plt.fill_between(range(len(momentList[:, 0])), momentList[:, 5] + self.safetyRate * momentList[:, 9], momentList[:, 5] - self.safetyRate * momentList[:, 9], color=color, alpha=0.2)
        plt.title('left knee')
        
        plt.subplot(222)
        plt.plot(momentList[:, 2])
        plt.plot(momentList[:, 6], color = color)
        plt.fill_between(range(len(momentList[:, 0])), momentList[:, 6] + self.safetyRate * momentList[:, 10], momentList[:, 6] - self.safetyRate * momentList[:, 10], color=color, alpha=0.2)
        plt.title('right hip')
        
        plt.subplot(224)
        plt.plot(momentList[:, 3])
        plt.plot(momentList[:, 7], color = color)
        plt.fill_between(range(len(momentList[:, 0])), momentList[:, 7] + self.safetyRate * momentList[:, 11], momentList[:, 7] - self.safetyRate * momentList[:, 11], color=color, alpha=0.2)
        plt.title('right knee')
        
        
        plt.show()



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

    def isSafetyMomentExisting(self):
        '''
        check if the safety moment data is existing
        '''
        # path = './data/' + self.userName + '_Safety.npy'
        if os.path.exists(self.savePath):
            return True
        else:
            return False

    def AskForLoadExistingData(self):
        '''
        ask if the user want to load existing data
        '''
        choise = input("Found Existing Safety Data, Do you want to load from existing data?[y]/n:")
        if choise == '' or choise == 'y' or choise == 'Y':
            return True
        else:
            return False

    def LoadExistingData(self):
        '''
        load existing data
        '''
        self.SafetyMoment = np.load(self.savePath)
        # self.plotPic()

        for i in range(1, self.SafetyMoment.shape[0]):
            for j in range(4):
                if self.SafetyMoment[i, 4+j] < 2:
                    # self.SafetyMoment[i, 4+j] = self.SafetyMoment[i - 1, 4+j]
                    self.SafetyMoment[i, 4+j] = 2
        for i in range(8):
            self.SafetyMoment[:, i] = scipy.signal.savgol_filter(self.SafetyMoment[:, i], 101, 3)
        
        # np.save(self.savaPath + '/filterData.npy', self.SafetyMoment)

    def RecordNewData(self, timeDuration = None):
        '''
        record new data
        '''
        self.SafetyMoment = self._ProcessRawSafetyMoment(timeDuration)



    # TODO: maybe the 5 should changed 
    def GetSafetyMoment(self):
        if self.isSafetyMomentExisting():
            if self.AskForLoadExistingData():
                self.LoadExistingData()
            else:
                self.RecordNewData()
        
        else:
            self.RecordNewData()

        

    # TODO
    def _ProcessRawSafetyMoment(self, timeDuration):
        '''
        process raw safety moment data to get the final safety moment data throught Least squares method 
        '''
        rawMomentData, rawAngleData = self._RecordRawSafetyMoment(timeDuration)
        self.rawMomentData = rawMomentData
        self.rawAngleData = rawAngleData
        assert(len(rawAngleData) == len(rawMomentData))

        rawAngleData = rawAngleData.reshape(rawAngleData.shape[0], 1)
        combinedData = np.hstack((rawMomentData, rawAngleData))
        print(combinedData)
        combinedData = combinedData[combinedData[:, -1].argsort()]

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


        for i in range(1, combinedData.shape[0]):
            for j in range(4):
                if combinedData[i, 4+j] < 4:
                    # self.SafetyMoment[i, 4+j] = self.SafetyMoment[i - 1, 4+j]
                    combinedData[i, 4+j] = 4
        for i in range(8):
            combinedData[:, i] = scipy.signal.savgol_filter(combinedData[:, i], 51, 3)

        # print(combinedData)
        np.save(self.savaPath + '/combinedData.npy', combinedData)
        return combinedData


    def _RecordRawSafetyMoment(self, timeDuration):
        '''
        record angle and moment 
        '''
        timeDuration = 1.0 / self.sampleRate
        momentData = []
        angleData = []

        if timeDuration is None:
            timeLong = input("Please input how long you want to record,[60](s):")
            if timeLong == "":
                timeLong = "60"
            timeLong = int(timeLong)
        else:
            timeLong = timeDuration

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
                    print('angel paresed failed!', angel)
                
                endTime = time.time()
                
                assert(endTime - startTime <= timeDuration)

                # print('time stop: ', timeDuration - (endTime - startTime))

                time.sleep(timeDuration - (endTime - startTime))
                if self.autoPlot:
                    plt.plot(momentData[-100:])
                    plt.pause(0.01)
                
                if time.time() - recordStartTime > timeLong:
                    break
                print("used %.3f, remains: %.3f"%( endTime - startTime, timeLong - time.time() + recordStartTime))

        except KeyboardInterrupt:
            print("End the Record!")
         
        np.save('rawdata_' + self.userName + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.npy', momentData, angleData)
        return np.array(momentData), np.array(angleData)


if __name__ == "__main__":
    angleManagerPort = input("Please input angel manager port (like \"com8\"): ")
    if angleManagerPort == "":
        angleManagerPort = "com3"
        
    momentManagerPort = input("Please input moment manager port (like \"com3\"): ")
    if momentManagerPort == "":
        momentManagerPort = "com4"

    momentManager = MomentManager(momentManagerPort)
    angelManager = AngleManager(angleManagerPort)
    # momentManager = 1
    # angelManager = 2
    

    smm = SafetyMomentManager(
        'dyj',
        sampleRate=35,
        autoPlot = False,
        momentManager = momentManager,
        angelManager = angelManager,
        safetyRate=4
        )
    angelManager.autoStartWalk()
    smm.GetSafetyMoment()
    # smm.plotPic()
    smm.DetectMoment()