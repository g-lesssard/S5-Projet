from StateMachine import Event
import threading
import time
from Libraries.SunFounder_Ultrasonic_Avoidance.Ultrasonic_Avoidance import Ultrasonic_Avoidance, GPIO
import Libraries.line_follower as lf

########################################################################################################################
RADAR_CHANNEL = 20
THRESHOLD_DISTANCE = 30
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
            self.filtered_distance = int(0.5*self.UA.get_distance() +  0.5*self.filtered_distance)
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
        self.previous_data = [0,0,0,0,0]
        self.reading_thread = None
        self.mutex = threading.Lock()

        self.pietons = Event()
        self.sharp_turn = Event()
        self.stop_zone = Event()
        self.printing = printing
        self.running = False

        self.pietons_count = 0
        self.stop_zone_count = 0
        time.sleep(0.5)

    def calibrate(self):
        lf.cali()

    def setPrinting(self, printing):
        self.printing = True

    def addObserver(self, observer_method, event):
        if event == 'pietons':
            self.pietons += observer_method
        elif event == 'sharp_turn':
            self.sharp_turn += observer_method
        elif event == 'stop_zone':
            self.stop_zone += observer_method


    def removeObserver(self, observer_method, event):
        if event == 'pietons':
            self.pietons -= observer_method
        elif event == 'sharp_turn':
            self.sharp_turn -= observer_method
        elif event == 'stop_zone':
            self.stop_zone -= observer_method

    def detectLine(self):
        count = 0
        while self.running:
            self.mutex.acquire()
            self.previous_data = self.data
            self.data = lf.lf.read_digital()
            self.lookForEvents()
            #if self.printing:
            #    print("New data is: {0}, and old data is: {1}".format(data, self.data))
            

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

    def lookForEvents(self):
        self.lookForPietons()
        self.lookForSharpTurn()
        self.lookForStopZone()

    def lookForPietons(self):
        if (self.previous_data == [0,0,1,0,0] or self.previous_data == [0,1,1,0,0] or self.previous_data == [0,0,1,1,0]) and self.data == [0,0,0,0,0]:
            self.pietons_count += 1
        if self.pietons_count != 0 and (self.data == [0,0,0,0,0]):
            self.pietons_count += 1
        else:
            self.pietons_count = 0
        if self.pietons_count == 10:
            self.pietons()
            self.pietons_count = 0
    
    def lookForSharpTurn(self):
        if self.data == [0,0,1,1,1]:
            self.sharp_turn()

    def lookForStopZone(self):
        if self.data == [1,1,1,1,1]:
            self.stop_zone_count +=1
        else:
           self.stop_zone_count = 0 
        if self.stop_zone_count == 10:
            self.stop_zone()
        



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
