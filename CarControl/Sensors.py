from StateMachine import Event
import threading
import time
from Libraries.SunFounder_Ultrasonic_Avoidance.Ultrasonic_Avoidance import Ultrasonic_Avoidance, GPIO

########################################################################################################################
RADAR_CHANNEL = 20
THRESHOLD_DISTANCE = 12
########################################################################################################################

class Radar(Ultrasonic_Avoidance):

    def __init__(self):
        self.channel=RADAR_CHANNEL
        self.onObjectDetected = Event()
        self.reading_thread = None
        GPIO.setmode(GPIO.BCM)

    def addObserver(self, observer_method):
        self.onObjectDetected += observer_method

    def removeObserver(self, observer_method):
        self.onObjectDetected -= observer_method

    def detectObject(self):
        while True:
            distance = self.distance()
            print("Object at {}".format(distance))
            if distance < THRESHOLD_DISTANCE and distance != -1:
                self.onObjectDetected()
            time.sleep(0.5)

    def startReading(self):
        self.reading_thread = threading.Thread(target=self.detectObject)
        self.reading_thread.start()

    def stopReading(self):
        self.reading_thread._stop()


########################################################################################################################
