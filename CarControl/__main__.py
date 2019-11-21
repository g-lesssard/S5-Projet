from Sensors import Radar, Line_Follower, Ultrasonic_Avoidance
from StateMachine import StateController
import time



########################################################################################################################


if __name__ == "__main__":
    
    master = StateController(printing=False)
    master.calibrate()
    master.startReadingThreads()
    

    
    while True:
        try:
            time.sleep(0.1)
            master.run()
        except KeyboardInterrupt:
            master.radar.stopReading()
            master.line_follower.stopReading()
            master.stop()
            exit()