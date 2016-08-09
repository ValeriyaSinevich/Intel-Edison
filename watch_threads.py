import numpy as np
import cv2
import skvideo.io as sk
import csv
import threading
import time
import sys
import signal
from collections import deque


MIN_AREA = 1500
NUMBER_OF_SECTIONS = 2
INF = 1e+18
NOT_A_POINT = [INF, INF]
FLOAT_ZERO = 1e-8
MIN_OBJECT_SIZE = 5
MAX_QUEUE = 15

q = deque(maxlen=20)
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FPS, 25)

#function which informs how many threads are currently working
print "start of the program\n"
def report_threads(self):
    # sleep(0.1)  # Otherwise process reported thread count can be behind
    print('process.num_threads', self.process.num_threads(),
        'threading.active_count', threading.active_count(),
        'cv2.getNumThreads', cv2.getNumThreads())

#class which is responsible for reading images from camera
class Reader(object):
    def __init__(self):
        signal.signal(signal.SIGALRM, self.get_alarm)#signal that tells the thread that it should stop
        self.go_on = True

    #function to catch signal
    def get_alarm(self, signum, stack):
        print "got signal to stop\n"
        self.go_on = False

    #main function
    def get_frames(self):
        while(self.go_on):
            ret, frame = cap.read()
            if not ret:
                print "no video \n"
                cap.release()
                break
            else:#put frame in the deque
                q.append(frame)
                if q.__len__() > MAX_QUEUE:#if too many frames are currently in the deque, let's delete five oldest
                    print "maxlen reached, deleting \n"
                    for k in range(5):
                        q.popleft()
        cap.release()
        print "stop reading\nbye!\n"



#class responsible for processing images
class Watcher(object):
    def __init__(self):
        self.MIN_AREA = 1500
        self.NUMBER_OF_SECTIONS = 2
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.line = read_line()
        self.points = self.chose_line_points(self.line)
        signal.signal(signal.SIGINT, self.signal_handler)

    #function that responds to user input ("Ctrl+C")
    def signal_handler(self, signum, frame):
        print 'You pressed Ctrl+C!'
        signal.alarm(1)
        time.sleep(2)
        # read_thread.join()
        # cap.release()
        sys.exit(0)

    #function to choose line points which will be checked
    def chose_line_points(self, line):
        points = []
        gap = MIN_OBJECT_SIZE
        n = len(line) / gap
        for i in range(n):
            points.append(line[i * gap / 2])
        return points

    #function that checks if given contour c includes any of chosen line points
    def check(self, c, l):
        l_printed = False
        for p in self.points:
            #must be disabled on edison
            # cv2.circle(self.m, tuple(p), 3, (255, 0, 0), -1)
            if cv2.pointPolygonTest(c,tuple(p),False) == 1:
                #must be disabled on edison
                # cv2.circle(self.m, tuple(p), 5, (0, 0, 255), -1)
                if not l_printed:
                    print "alarm! {0}\n".format(l)
                    l_printed = True

    #main function
    def watch(self):
        #counter that helps to distinguish between different alarm calls
        l = 0
        while(True):
            l+=1
            try:#read from the deque
                frame = q.pop()
                print q.__len__()
            except:#if the deque is empty, let's wait for half a second and try one more time.
                #If it fails for five times, than something is wrong and we'd better stop.
                j = 0
                while j < 5:
                    j += 1
                    print "empty queue, trying one more time \n"
                    time.sleep(0.5)
                    try:
                        frame = q.pop()
                        break
                    except:
                        print "empty queue, trying one more time \n"
                        time.sleep(0.5)
                if j == 5:
                    print "bad queue, aborting \n"
                    cap.release()
                    break
            #self.m - image to draw if we execute the code on laptop. Must be disabled on edison/
            # self.m = np.zeros(frame.shape, dtype=np.uint8)
            # for p in self.points:
            #     cv2.circle(self.m, tuple(p), 3, (255, 0, 0), -1)
            #extract background
            fgmask = self.fgbg.apply(frame)
            #apply threshold
            thresh = cv2.dilate(fgmask, None, iterations=4)
            #find contours
            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts = []
            #check each contour on crossing
            i = 0
            for c in contours:
                if i == 0 or i == 1:
                    i += 1
                    continue
                if cv2.contourArea(c) < MIN_AREA:
                    continue
                cnts.append(c)
                self.check(c, l)
            #must be disabled on edison
            # cv2.drawContours(self.m, cnts, -1, (255, 255, 255))

#function to read line stored in csv file produced by image_send.py
def read_line():
    line = []
    with open('line.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line.append([int(row['x']), int(row['y'])])
    return line

#main thread is the one responsible for processing. Reader thread is its child.
print "start_reading_thread\n"
reader = Reader()
read_thread = threading.Thread(target=reader.get_frames)
read_thread.start()
time.sleep(2)
watcher = Watcher()
print "start processing\n"
watcher.watch()
