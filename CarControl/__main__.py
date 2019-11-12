from Sensors import *


########################################################################################################################


if __name__ == "__main__":
    rad = Radar()
    master = StateController()

    rad.addObserver(master.objectDetected)

    rad.detectObject(10)

