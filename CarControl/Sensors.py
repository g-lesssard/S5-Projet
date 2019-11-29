from StateMachine import Event
import threading
import time
from Libraries.SunFounder_Ultrasonic_Avoidance.Ultrasonic_Avoidance import Ultrasonic_Avoidance, GPIO
import Libraries.line_follower as lf

from picar import filedb
config_file = '/home/projet/CarControl/config'

########################################################################################################################
RADAR_CHANNEL = 20
THRESHOLD_DISTANCE = 3
DIFFERENCE_THRESHOLD = 40
########################################################################################################################

class Radar(object):

    def __init__(self, printing=False):
        self.UA = Ultrasonic_Avoidance(channel=RADAR_CHANNEL)
        self.onObjectDetected = Event()
        self.reading_thread = None
        self.filtered_distance = 50
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
            new_data = self.UA.get_distance()
            if abs(new_data - self.filtered_distance) > THRESHOLD_DISTANCE or new_data == -1:
                new_data = self.filtered_distance
            self.filtered_distance = int(0.5*self.UA.get_distance() +  0.5*self.filtered_distance)
            if self.printing:
                print("Object at {}".format(self.filtered_distance))
            if self.filtered_distance < THRESHOLD_DISTANCE and self.filtered_distance != -1:
                self.onObjectDetected()
            time.sleep(0.05)
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
        self.line_found = Event()
        self.printing = printing
        self.running = False
        self.fire_count = 0

        self.pietons_count = 0
        self.stop_zone_count = 0
        time.sleep(0.5)

    def calibrate(self):
        db = filedb.fileDB(db=config_file)
        key = input('Enter Y to calibrate, N otherwise: ')
        if key == 'Y':    
            lf.cali()
            db.set('line_follower_references', lf.lf.references)
        else:
            reference_string = (db.get('line_follower_references'))
            reference_string = reference_string[1:(len(reference_string)-2)].split(',')
            for i in range(0, len(reference_string)): 
                reference_string[i] = float(reference_string[i])
                lf.lf.references = reference_string
            print("References are: {}".format(lf.lf.references))
            

    def setPrinting(self, printing):
        self.printing = True

    def addObserver(self, observer_method, event):
        if event == 'pietons':
            self.pietons += observer_method
        elif event == 'sharp_turn':
            self.sharp_turn += observer_method
        elif event == 'stop_zone':
            self.stop_zone += observer_method
        elif event == 'line_found':
            self.line_found += observer_method


    def removeObserver(self, observer_method, event):
        if event == 'pietons':
            self.pietons -= observer_method
        elif event == 'sharp_turn':
            self.sharp_turn -= observer_method
        elif event == 'stop_zone':
            self.stop_zone -= observer_method
        elif event == 'line_found':
            self.line_found += observer_method
            self.fire_count = 0

    def detectLine(self):
        count = 0
        while self.running:
            self.mutex.acquire()
            self.previous_data = self.data
            self.data = lf.lf.read_digital()
            self.lookForEvents()
            if self.printing:
                print("Linefollower data: {0}, count: {1}".format(self.data, count))
            self.mutex.release()
            time.sleep(0.05)            
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
        self.lookForLine()

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

    def lookForLine(self):
        if (self.data == [1,0,0,0,0] or self.data == [1,1,0,0,0] and self.fire_count == 0):
            print('Firing line found event')
            self.line_found()
            self.fire_count += 1
        



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
