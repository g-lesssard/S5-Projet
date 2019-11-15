from StateMachine import Event
import threading
import time
from Libraries.SunFounder_Ultrasonic_Avoidance.Ultrasonic_Avoidance import Ultrasonic_Avoidance, GPIO
import Libraries.line_follower as lf

########################################################################################################################
RADAR_CHANNEL = 20
THRESHOLD_DISTANCE = 12
########################################################################################################################

class Radar(Ultrasonic_Avoidance):

    def __init__(self, printing=False):
        self.channel=RADAR_CHANNEL
        self.onObjectDetected = Event()
        self.reading_thread = None
        self.filtered_distance = 0
        self.printing = printing
        self.mutex = threading.Lock()
        self.running = False
        GPIO.setmode(GPIO.BCM)

    def addObserver(self, observer_method):
        self.onObjectDetected += observer_method

    def removeObserver(self, observer_method):
        self.onObjectDetected -= observer_method

    def detectObject(self):
        while self.running:
            #self.mutex.acquire()
            self.filtered_distance = int(0.70*self.distance() + 0.30*self.filtered_distance)
            if self.printing:
                print("Object at {}".format(self.filtered_distance))
            if self.filtered_distance < THRESHOLD_DISTANCE and self.filtered_distance != -1:
                self.onObjectDetected()
            time.sleep(0.1)
            #self.mutex.release()
        return

    def startReading(self):
        self.reading_thread = threading.Thread(target=self.detectObject)
        self.running = True
        self.reading_thread.start()
        

    def stopReading(self):
        self.running = False

    def getData(self):
        return self.filtered_distance


########################################################################################################################

class Line_Follower():

    def __init__(self, printing=False):
        self.goingOffTrack = Event()
        self.data= [0,0,0,0,0]
        self.reading_thread = None
        self.mutex = threading.Lock()
        self.printing = printing
        self.running = False

    def calibrate(self):
        lf.cali()

    def setPrinting(self, printing):
        self.printing = True

    def detectLine(self):
        while self.running:
            self.mutex.acquire()
            self.data = lf.lf.read_digital()
            time.sleep(0.1)
            if self.printing:
                print(self.data)
            self.mutex.release()
        return

    def startReading(self):
        self.reading_thread = threading.Thread(target=self.detectLine)
        self.running = True
        self.reading_thread.start()
        

    def stopReading(self):
        self.running = False

    def getData(self):
        return self.data


########################################################################################################################    

