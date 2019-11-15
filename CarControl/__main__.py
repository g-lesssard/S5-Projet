from Sensors import Radar, Line_Follower
from StateMachine import StateController
import time



########################################################################################################################


if __name__ == "__main__":
    
    master = StateController(printing=True)
    master.startReadingThreads()
    #master.calibrate()
    
    while True:
        try:
            master.run()
        except KeyboardInterrupt:
            master.radar.stopReading()
            master.lf.stopReading()
            exit()