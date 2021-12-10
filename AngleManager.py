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

    def emergencyStop(self):
        while 1:
            self._sendMessage(self.emergencyStop)

    def waitingForState(self, state):
        while 1:
            if self.getCurrentState() == state
                break

    def assertState(self, state):
        nowState = self.getCurrentState()
        if nowState != state:
            raise StateERROR
            


    def standUp(self):
        self.waitingForState(1)
        self._sendMessage(self.standUpOrSit)
        self.waitingForState(2)

    def walk(self):
        self.waitingForState(1)
        self._sendMessage(self.standUpOrSit)
        self.waitingForState(2)
        self._sendMessage(self.standUpOrSit)

    def manualControl(self):


    def getCurrentState(self):
        rawDataHex = self.ser.read(3)
        parsedDataHex = binascii.b2a_hex(rawDataHex)
        parsedDataHex = str(parsedDataHex).split('\'')[1][1]

        self.currentState = parsedDataHex
        return parsedDataHex

if __name__ == "__main__":
    port = input("Please input AngleManager Port: ")
    if port == "":
        port = "com7"
    am = AngleManager(port)
    print(am.getCurrentState())

    am._sendMessage(am.standUpOrSit)
    print(am.getCurrentState())