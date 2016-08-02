import numpy as np
import cv2
import skvideo.io as sk
import csv
import threading
import psutil
import Queue
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
# print cv2.getNumThreads()

q = deque(maxlen=20)
cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FPS, 10)

print "start of the program\n"
def report_threads(self):
    # sleep(0.1)  # Otherwise process reported thread count can be behind
    print('process.num_threads', self.process.num_threads(),
        'threading.active_count', threading.active_count(),
        'cv2.getNumThreads', cv2.getNumThreads())

class Reader(object):
    def __init__(self):
        signal.signal(signal.SIGALRM, self.get_alarm)
        self.go_on = True

    def get_alarm(self, signum, stack):
        print "say stop reading\n"
        self.go_on = False

    def get_frames(self):
        ret, frame = cap.read()
        print frame.shape
        while(self.go_on):
            ret, frame = cap.read()
            if not ret:
                print "no video \n"
                cap.release()
                break
            else:
                q.append(frame)
                if q.__len__() > MAX_QUEUE:
                    print "maxlen reached, deleting \n"
                    for k in range (5):
                        q.popleft()
        cap.release()
        print "stop reading\nbuy\n"




class Watcher(object):
    def __init__(self):
        self.MIN_AREA = 1500
        self.NUMBER_OF_SECTIONS = 2
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.line = read_line()
        # self.sectioned_line = process_line(self.line)
        # self.bottom = []
        # self.right = []
        # self.left =[]
        # self.top = []
        # self.process = psutil.Process()
        self.points = self.chose_line_points(self.line)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        print 'You pressed Ctrl+C!'
        signal.alarm(1)
        time.sleep(2)
        # read_thread.join()
        # cap.release()
        sys.exit(0)

    def chose_line_points(self, line):
        points = []
        gap = MIN_OBJECT_SIZE
        n = len(line) / gap
        for i in range(n):
            points.append(line[i * gap / 2])
        return points

    def check(self, c):
        for p in self.points:
            # cv2.circle(self.m, tuple(p), 3, (255, 0, 0), -1)
            if cv2.pointPolygonTest(c,tuple(p),False) == 1:
                cv2.circle(self.m, tuple(p), 5, (0, 0, 255), -1)
                print "alarm!\n"

    def watch(self):
        # ret, frame = self.cap.read()
        # for j in range(20):
        while(True):
            # ret, frame = self.cap.read()
            try:
                frame = q.pop()
                print q.__len__()
            except:
                print "bad queue \n"
                cap.release()
                break
            self.m = np.zeros(frame.shape, dtype=np.uint8)
            for p in self.points:
                cv2.circle(self.m, tuple(p), 3, (255, 0, 0), -1)
            fgmask = self.fgbg.apply(frame)
            # self.report_threads()
            thresh = cv2.dilate(fgmask, None, iterations=4)
            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts = []

            i = 0
            for c in contours:
                if i == 0 or i == 1:
                    i += 1
                    continue
                if cv2.contourArea(c) < MIN_AREA:
                    continue
                cnts.append(c)
                self.check(c)
            cv2.drawContours(self.m, cnts, -1, (255, 255, 255))
            # print cnts
            # print self.m.shape
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                signal.alarm(1)
                break
                cap.release()
            cv2.imshow('cnts',self.m)
            cv2.imshow('frame',frame)
            # self.report_threads()
        # self.cap.release()


def read_line():
    line = []
    with open('line.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line.append([int(row['x']), int(row['y'])])
    print line
    return line

print "start_reading_thread\n"
reader = Reader()
read_thread = threading.Thread(target=reader.get_frames)
read_thread.start()
time.sleep(2)
watcher = Watcher()
print "start processing\n"
watcher.watch()
