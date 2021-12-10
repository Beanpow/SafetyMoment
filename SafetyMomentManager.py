import time
import numpy as np
from AngleManager import AngleManager
import os
from MomentManager import MomentManager
import matplotlib.pyplot as plt

class SafetyMomentManager:
    def __init__(self, userName, momentManager, angelManager, sampleRate=20, autoPlot = False) -> None:
        '''
        userName:       The User Name
        sampleRate:     Hz, the value must less than 4, because of the momentManager have the limited rate
        '''
        self.userName = userName
        self.sampleRate = sampleRate
        self.autoPlot = autoPlot

        self.momentManager = momentManager
        self.angelManager = angelManager

        self.GetSafetyMoment()


    def GetSafetyMoment(self):
        path = '/data/' + self.userName + '_Safety.npy'
        if os.path.exists(path):
            choise = input("Found Existing Safety Data, Do you want to load from existing data?[y]/n:")
            if choise == '' or choise == 'y' or choise == 'Y':
                self.SafetyMoment = np.load(path)
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
        self.angelManager.autoStartWalk()
        rawMomentData, rawAngleData = self._RecordRawSafetyMoment()
        assert(len(rawAngleData) == len(rawMomentData))

        # for indx in rawAngleData:


    # TODO
    def _RecordRawSafetyMoment(self):
        '''
        record angle and moment 
        '''
        timeDuration = 1.0 / self.sampleRate
        momentData = []
        angleData = []

        timeLong = input("Please input how long you want to record,[60](s):")
        if timeLong == "":
            timeLong == "60"
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
                angle = self.angelManager.getInfo()

                momentData.append(moment[0])
                angleData.append(angle[1])
                
                endTime = time.time()
                print(endTime - startTime)
                assert(endTime - startTime <= timeDuration)

                # print('time stop: ', timeDuration - (endTime - startTime))

                time.sleep(timeDuration - (endTime - startTime))
                if self.autoPlot:
                    plt.plot(momentData[-100:])
                    plt.pause(0.01)
                
                if time.time() - recordStartTime > timeLong:
                    break

        except KeyboardInterrupt:
            print("End the Record!")
         
        np.save('rawdata_' + self.userName + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '.npy', momentData)
        return momentData, angleData


if __name__ == "__main__":
    angleManagerPort = input("Please input angel manager port (like \"com7\"): ")
    if angleManagerPort == "":
        angleManagerPort = "com7"
        
    momentManagerPort = input("Please input moment manager port (like \"com3\"): ")
    if momentManagerPort == "":
        momentManagerPort = "com3"

    momentManager = MomentManager(momentManagerPort)
    angelManager = AngleManager(angleManagerPort)

    smm = SafetyMomentManager('hkb', sampleRate=40, autoPlot = True, momentManager = momentManager, angelManager = angelManager)
