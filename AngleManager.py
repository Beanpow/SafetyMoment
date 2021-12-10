import serial
import sys
import binascii

class AngleManager:
    # TODO
    def __init__(self, port, byterate=115200, timeout=0.5) -> None:
        self.req = ""
        self.currentState = -1
        self.standUpOrSit = bytes([0xAA, 0x55, 0x66, 0x77])
        self.confirm = bytes([0xAA, 0x55, 0x44, 0x77])
        self.walkOrPause = bytes([0xAA, 0x55, 0x55, 0x77])
        self.emergencyStop = bytes([0xAA, 0x55, 0x55, 0x99])

        try:
            self.ser = serial.Serial(port, byterate, timeout=timeout)
        except Exception as e:
            print(e)
            sys.exit()

    def __del__(self):
        self.ser.close()

    def _sendMessage(self, req):
        self.ser.write(req)

    def emergencyStopButton(self):
        for _ in range(1000):
            self._sendMessage(self.emergencyStop)

    def waitingForState(self, state):
        while 1:
            print(self.getInfo()[0])
            if self.getInfo()[0] == state:
                break

        self.assertState(state)

    def assertState(self, state):
        info = self.getInfo()
        nowState = info[0]
        if nowState != state:
            raise AssertionError

    def standUpOrSitButton(self):
        self._sendMessage(self.standUpOrSit)

    def confirmButton(self):
        self._sendMessage(self.confirm)

    def walkOrPauseButton(self):
        self._sendMessage(self.walkOrPause)

    def autoStartWalk(self):
        #done init
        self.waitingForState(0)

        #stand up
        self.standUpOrSitButton()
        self.waitingForState(2)

        #confirm stand up
        self.confirmButton()

        #waiting for state 1
        self.waitingForState(1)

        #walk
        self.walkOrPauseButton()

    def manualControl(self):
        # done init
        pass





    def getInfo(self):
        rawDataHex = self.ser.read(4)
        parsedDataHex = binascii.b2a_hex(rawDataHex)
        parsedDataHex = str(parsedDataHex).split('\'')[1]

        timeStamp = int(parsedDataHex[4:8], 16) / 1000



        self.currentState = int(parsedDataHex[1], 16)
        return self.currentState, timeStamp

if __name__ == "__main__":
    port = input("Please input AngleManager Port: ")
    if port == "":
        port = "com7"
    am = AngleManager(port)
    am.autoStartWalk()