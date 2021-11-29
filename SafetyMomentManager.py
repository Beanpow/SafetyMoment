import time
import numpy as np
from AngleManager import AngleManager
import os
from MomentManager import MomentManager

class SafetyMomentManager:
    def __init__(self, userName, sampleRate=4) -> None:
        '''
        userName:       The User Name
        sampleRate:     Hz, the value must less than 4, because of the momentManager have the limited rate
        '''
        self.userName = userName
        self.sampleRate = sampleRate
        self.GetSafetyMoment()

    def GetSafetyMoment(self):
        path = './data/' + self.userName + '_Safety.npy'
        if os.path.exists(path):
            choise = input("Found Existing Safety Data, Do you want to load from existing data?[y]/n:")
            if choise == '' or choise == 'y' or choise == 'Y':
                self.SafetyMoment = np.load(path)
            else:
                self.SafetyMoment = self.RecordRawSafetyMoment()
        
        else:
            input("You will record the raw data, press any key to continue...press CTRL-C to terminate")
            self.SafetyMoment = self._ProcessRawSafetyMoment()

    # TODO
    def _ProcessRawSafetyMoment(self):
        '''
        process raw safety moment data to get the final safety moment data throught Least squares method 
        '''
        rawMomentData, rawAngleData = self._RecordRawSafetyMoment()
        assert(len(rawAngleData) == len(rawMomentData))

        # for indx in rawAngleData:


    # TODO
    def _RecordRawSafetyMoment(self):
        '''
        record angle and moment 
        '''
        momentManager = MomentManager()
        #angelManager = AngleManager()
        timeDuration = 1.0 / self.sampleRate
        momentData = []
        angleData = []

        try:
            while(1):
                startTime = time.time()
                moment = momentManager.GetAllMoments()
                #angle = angelManager.GetAllMoment()

                momentData.append(moment[0])
                #angleData.append(angle[0])
                
                endTime = time.time()
                print(endTime - startTime)
                assert(endTime - startTime <= timeDuration)

                time.sleep(timeDuration - (endTime - startTime))

        except KeyboardInterrupt:
            print("End the Record!")
         
        np.save('rawdata.npy', momentData)
        return momentData, angleData


if __name__ == "__main__":
    smm = SafetyMomentManager('hkb', sampleRate=6)
