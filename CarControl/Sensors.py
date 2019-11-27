from StateMachine import Event
import threading
import time
from Libraries.SunFounder_Ultrasonic_Avoidance.Ultrasonic_Avoidance import Ultrasonic_Avoidance, GPIO
import Libraries.line_follower as lf

########################################################################################################################
RADAR_CHANNEL = 20
THRESHOLD_DISTANCE = 3
########################################################################################################################

class Radar(object):

    def __init__(self, printing=False):
        self.UA = Ultrasonic_Avoidance(channel=RADAR_CHANNEL)
        self.onObjectDetected = Event()
        self.reading_thread = None
        self.filtered_distance = 0
        self.printing = printing
        self.running = False
        time.sleep(0.5)


    def addObserver(self, observer_method):
        self.onObjectDetected += observer_method

    def removeObserver(self, observer_method):
        self.onObjectDetected -= observer_method

    def detectObject(self):
        while self.running:
            #self.mutex.acquire()
            self.filtered_distance = self.UA.get_distance()
            if self.printing:
                print("Object at {}".format(self.filtered_distance))
            if self.filtered_distance < THRESHOLD_DISTANCE and self.filtered_distance != -1:
                self.onObjectDetected()
            time.sleep(0.3)
            #self.mutex.release()
        return


    def startReading(self):
        self.reading_thread = threading.Thread(target=self.detectObject)
        print("Radar Thread Started")
        self.running = True
        self.reading_thread.start()
        

    def stopReading(self):
        self.running = False
        print("Radar Thread Stopped")

    def getData(self):
        return self.filtered_distance


########################################################################################################################

class Line_Follower():

    def __init__(self, printing=False):
        self.goingOffTrack = Event()
        self.data= [0,0,0,0,0]
        self.reading_thread = None
        self.mutex = threading.Lock()
        self.pietons = Event()
        self.printing = printing
        self.running = False
        time.sleep(0.5)

    def calibrate(self):
        lf.cali()

    def setPrinting(self, printing):
        self.printing = True

    def addObserver(self, observer_method):
        self.pietons += observer_method

    def removeObserver(self, observer_method):
        self.pietons -= observer_method

    def detectLine(self):
        count = 0
        while self.running:
            self.mutex.acquire()

            data = lf.lf.read_digital()
            #if self.printing:
            #    print("New data is: {0}, and old data is: {1}".format(data, self.data))
            if (self.data == [0,0,1,0,0] or self.data == [0,1,1,0,0] or self.data == [0,0,1,1,0]) and data == [0,0,0,0,0]:
                count += 1

            self.data = data
            if count != 0 and (self.data == [0,0,1,0,0] or self.data == [0,1,1,0,0] or self.data == [0,0,1,1,0] or self.data == [0,0,0,0,0]):
                count += 1
            else:
                count = 0
            if count == 10:
                self.pietons()
                count = 0

            if self.printing:
                print("Linefollower data: {0}, count: {1}".format(self.data, count))
            
            time.sleep(0.05)
            self.mutex.release()
        return

    def startReading(self):
        self.reading_thread = threading.Thread(target=self.detectLine)
        if self.printing:
            print("Thread started")
        self.running = True
        self.reading_thread.start()
        

    def stopReading(self):
        self.running = False

    def getData(self):
        return self.data


########################################################################################################################    

if __name__ == "__main__":

    rad = Radar(printing=True)
    try:
        rad.startReading()
        time.sleep(10)
        rad.stopReading()
    except KeyboardInterrupt:
        rad.stopReading()

    line = Line_Follower(printing=True)
    try:
        line.startReading()
        time.sleep(10)
        line.stopReading()
    except KeyboardInterrupt:
        line.stopReading()
