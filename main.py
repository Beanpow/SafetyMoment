from MomentManager import MomentManager
from SocketServer import SocketServer
from AngleManager import AngleManager
from MomentManager import MomentManager
from SafetyMomentManager import SafetyMomentManager

import numpy as np
import time


class MainServer:
    def __init__(self, momentManagerPort, angleManagerPort, userName, safetyRate, sampleRate) -> None:

        self.momentManager = MomentManager(momentManagerPort)
        self.angleManager = AngleManager(angleManagerPort)
        self.smm = SafetyMomentManager(
            userName,
            sampleRate=sampleRate,
            safetyRate=safetyRate,
            momentManager=self.momentManager,
            angleManager=self.angleManager
        )
        self.SocketServer = None
        self.InitSocketServer()

    def InitSocketServer(self):
        self.socketServer = SocketServer()
        self.socketServer.create_socket()


    def SendData(self, data):
        self.socketServer.send_data(data)
    
    def ReciveData(self):
        data = self.socketServer.receive_data()
        return data

    def Run(self):
        status = 0
        while True:
            data = self.ReciveData()
            if data == 'preWalk':
                self.smm.angelManager.preStartWalk()
                self.SendData('1')
                status = 1
            elif data == 'walk':
                if status == 1:
                    self.smm.angelManager.realStartWalk()

                    if self.smm.isSafetyMomentExisting():
                        self.SendData('2')
                        data = self.ReciveData()
                        if data == 'ReadOldData':
                            self.smm.LoadExistingData()
                        elif data[:11] == 'ReadNewData':
                            self.smm.RecordNewData(int(data[11:]))
                        self.SendData('3')
                    else:
                        self.smm.RecordNewData(20)
                        self.SendData('3')
                    status = 3

                    # data = self.ReciveData()
                    break
        

        # Start Detecting
        self.DetectMoment()

    def DetectMoment(self):
        angelList = []
        momentList = None
        idxList = []
        indx = 0

        flag = 0
        keyAngel = 0

        if self.smm.SafetyMoment is None:
            self.SendEmergencyStop()

            # Prevent the robot stopping before the stimulation
            # while True:
            #     data = self.ReciveData()
            #     if data == 'Emergency Stop':
            #         break

            self.angelManager.emergencyStopButton()
        
        else:
            try:
                print('detecting...')
                while True:
                    indx += 1
                    moment = self.momentManager.GetAllMoments()[0]
                    angel = self.angelManager.getInfo()


                    if angel[2] == 1:
                        checkResult, idx = self.smm.CheckMoment(np.hstack((moment, angel[1])))
                        idxList.append(idx)

                        tempdata = np.hstack((moment, self.smm.SafetyMoment[idx, 0:8]))

                        if type(momentList) != type(np.array([[1,2,3,4]])):
                            momentList = tempdata.reshape(1, 12)
                        else:
                            momentList = np.vstack((momentList, tempdata))
                        angelList.append(angel[1])

                        # TODO: maybe need to change the 0.3
                        if abs(angel[1] - keyAngel) < 0.01:
                            flag += 1
                            if flag == 100:
                                self.SendData('Start Stimulation')

                        if not checkResult:
                            self.SendEmergencyStop()

                            while True:
                                data = self.ReciveData()
                                if data == 'Emergency Stop':
                                    break

                            self.angelManager.emergencyStopButton()
                            print('Emergency Stop!')
                            break
                            # return
                        
                        # Send Data to plot process
                        # self.smm.Update(tempdata)

                    else:
                        print('angel paresed failed!')

            except KeyboardInterrupt:
                print("Program Terminated!")
            finally:
                angelList = np.array(angelList)
                angelList = np.reshape(angelList, (len(angelList), 1))
                print(momentList.shape, angelList.shape)
                np.save('./data/detect_' + self.userName + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.npy', np.hstack((momentList, angelList)))


    def SendEmergencyStop(self):
        self.SendData('Emergency Stop')



def main():
    angleManagerPort = input("Please input angel manager port (like \"com8\"): ")
    if angleManagerPort == "":
        angleManagerPort = "com3"
        
    momentManagerPort = input("Please input moment manager port (like \"com3\"): ")
    if momentManagerPort == "":
        momentManagerPort = "com4"


    mainServer = MainServer(
        momentManagerPort=momentManagerPort, 
        angleManagerPort=angleManagerPort, 
        userName="test", 
        safetyRate=4, 
        sampleRate=35
    )

    mainServer.Run()



if __name__ == "__main__":
    main()