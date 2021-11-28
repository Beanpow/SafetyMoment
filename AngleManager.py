import serial
import sys

class AngleManager:
    # TODO
    def __init__(self, port='com3', byterate=9600, timeout=0.5) -> None:
        self.req = ""

        try:
            self.ser = serial.Serial(port, byterate, timeout=timeout)
        except Exception as e:
            print(e)
            sys.exit()

    def __del__(self):
        self.ser.close()

    def GetAngle(self):
        pass

if __name__ == "__main__":
    am = AngleManager()
    print(am.GetAngle())