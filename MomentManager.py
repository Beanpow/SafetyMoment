import serial
import time
import binascii
import sys
import numpy as np

class MomentManager:
    def __init__(self, port='com3', byterate=38400, timeout=10) -> None:
        self.__reqListForPortList = [ bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A]),
                                    bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x39]),
                                    bytes([0x03, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0xE8]),
                                    bytes([0x04, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x5F])]

        self.reqListForAllPort = bytes([0x01, 0x03, 0x01, 0xf4, 0x00, 0x08, 0x04, 0x02])

        try:
            self.ser = serial.Serial(port, byterate, timeout=timeout)
        except Exception as e:
            print(e)
            sys.exit()
    
    def __del__(self):
        self.ser.close()

    def _SendMessage(self, req):
        self.ser.write(req)
        # while(1):
        #     # rawDataHex = self.ser.read_all()
        #     rawDataHex = self.ser.read(21)
        #     print(len(ra))
        #     if len(rawDataHex) == 21:
        #         print(len(rawDataHex))
        #         break

        rawDataHex = self.ser.read(21)
        # print(len(rawDataHex))
        # time.sleep(0.02)#the time must more than 0.02
        # rawDataHex = self.ser.read_all()

        # parse received data
        parsedDataHex = binascii.b2a_hex(rawDataHex)
        parsedDataHex = str(parsedDataHex)
        parsedDataHex = parsedDataHex.split('\'')[1]
        return rawDataHex, parsedDataHex

    def GetMoment(self, portNum):
        pass

    def __GetMoment(self, portNum):
        '''
        portNum = [1, 2, 3, 4]
        '''
        req = self.__reqListForPortList[portNum - 1]
        rawDataHex, parsedDataHex = self._SendMessage(req)

        try:
            assert(len(parsedDataHex) == 14)
        except AssertionError:
            print(rawDataHex)
            sys.exit()
        
        id = int(parsedDataHex[0:2])
        assert(id == portNum)

        moment = int(parsedDataHex[6:10], 16)
        if moment > 32768:
            moment = moment - 65536
        moment /= 10

        return moment, id, parsedDataHex

    def __GetMoments(self, portList):
        momentList = []
        idList = []
        rawDataHexList = []
        for i in portList:
            moment, id, rawdataHex = self.GetMoment(i)
            momentList.append(moment)
            idList.append(id)
            rawDataHexList.append(rawdataHex)
        
        return momentList, idList, rawDataHexList
    
    def __GetAllMoments(self):
        return self.__GetMoments([1,2,3,4])

    def GetAllMoments(self):
        req = self.reqListForAllPort
        rawDataHex, parsedDataHex = self._SendMessage(req)

        try:
            assert(len(parsedDataHex) == 42)
        except AssertionError:
            print(rawDataHex)
            sys.exit()

        momentList = []
        momentList.append(int(parsedDataHex[6:14], 16))
        momentList.append(int(parsedDataHex[14:22], 16))
        momentList.append(int(parsedDataHex[22:30], 16))
        momentList.append(int(parsedDataHex[30:38], 16))

        for i in range(4):
            if momentList[i] > 2147483648:
                momentList[i] =  momentList[i] - 4294967296
            momentList[i] /= 100

        return np.array(momentList), [1,2,3,4], parsedDataHex

if __name__ == "__main__":
    m = MomentManager()
    while(1):
        start = time.time()
        time.sleep(0)
        print(m.GetAllMoments(), time.time() - start)
