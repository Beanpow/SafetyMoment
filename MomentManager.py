import serial
import time
import binascii
import sys

class MomentManager:
    def __init__(self, port='com3', byterate=9600, timeout=0.5) -> None:
        self.reqListForPortList = [ bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A]),
                                    bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x39]),
                                    bytes([0x03, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0xE8]),
                                    bytes([0x04, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x5F])]

        try:
            self.ser = serial.Serial(port, byterate, timeout=timeout)
        except Exception as e:
            print(e)
            sys.exit()
    
    def __del__(self):
        self.ser.close()

    def GetMoment(self, portNum):
        '''
        portNum = [1, 2, 3, 4]
        '''
        req = self.reqListForPortList[portNum - 1]
        self.ser.write(req)
        time.sleep(0.04)#the time must more than 0.05(may be less?)
        dataHex = self.ser.read_all()
        rawDataHex = dataHex

        # parse received data
        dataHex = binascii.b2a_hex(rawDataHex)
        dataHex = str(dataHex)
        dataHex = dataHex.split('\'')[1]
        assert(len(dataHex) == 14)
        
        id = int(dataHex[0:2])
        assert(id == portNum)

        moment = int(dataHex[6:10], 16)
        if moment > 32768:
            moment = moment - 65536
        moment /= 10

        return moment, id, rawDataHex

    def GetMoments(self, portList):
        momentList = []
        idList = []
        rawDataHexList = []
        for i in portList:
            moment, id, rawdataHex = self.GetMoment(i)
            momentList.append(moment)
            idList.append(id)
            rawDataHexList.append(rawdataHex)
        
        return momentList, idList, rawDataHexList
    
    def GetAllMoments(self):
        return self.GetMoments([1,2,3,4])

if __name__ == "__main__":
    m = MomentManager()
    print(m.GetMoments([1]))















#     # dataHex = str(dataHex).split('\'')[1]
#     # dataHex = dataHex.split('\\x')

#     # id = int(dataHex[1])
#     # try:
#     #     lowByte = dataHex[5][0:2]
#     # except IndexError:
#     #     print(rawDataHex)
#     #     break
#     # highByte = dataHex[4]
#     # # moment = lowByte + 

#     # print(id, lowByte, highByte)
#     # print(dataHex, rawDataHex)

    