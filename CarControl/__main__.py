from Sensors import Radar
from StateMachine import StateController
import time


########################################################################################################################


if __name__ == "__main__":
    rad = Radar()
    master = StateController()
    rad.startReading()

    rad.addObserver(master.objectDetected)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            rad.stopReading()
            exit()