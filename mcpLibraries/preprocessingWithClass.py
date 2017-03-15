from operator import itemgetter
import copy
import math
import cv2
import numpy as np
import time
import myLibraries.extras as e
import myLibraries.Vector as v
import matplotlib.pyplot as plt
import random
import threading
import Queue
import matplotlib.cm as cm
import matplotlib as mpl

class Papillae(object):
    """docstring for Papillae"""
    def __init__(self, oldPos):
        self.oldPos  = v.Vector([oldPos[0], oldPos[1]])
        # self.oldSize = oldSize

    def label(self, xyn):
        self.number  = blobCheck([self.oldPos.x, self.oldPos.y], xyn)

    def update(self, newPos):
        if np.isnan(newPos[0]):
            newPos[0] = self.oldPos.x
        if np.isnan(newPos[1]):
            newPos[1] = self.oldPos.y
        self.newPos  = v.Vector([newPos[0], newPos[1]])
        self.measure()

    def measure(self):
        self.difference   = self.newPos.sub(self.oldPos)
        self.displacement = self.difference.mag()
        if self.displacement > 0:
            self.unit = self.difference.unit()
        else:
            self.unit = v.Vector([0, 0])
        # self.changeinSize = self.newSize - self.oldSize
        self.bearing = e.bearingMeasurement(self.difference.x, self.difference.y)
        if (self.displacement < 2 or self.displacement > 25):
            self.state = False
        else:
            self.state = True
        self.colour = self.displacementColour(self.displacement)

    def bearingColour(self, bearing):
        if bearing < 90:
            colour = (0, 0, 255)
        elif bearing < 180:
            colour = (0, 255, 0)
        elif bearing < 270:
            colour = (255, 0, 0)
        elif bearing <= 360:
            colour = (0, 0, 0)
        else:
            print bearing
        return colour

    def displacementColour(self, displacement):
        norm   = mpl.colors.Normalize(vmin=0, vmax=10)
        m      = cm.ScalarMappable(norm=norm, cmap=cm.jet)
        colour = np.array(m.to_rgba(displacement)[:-1])*255
        return colour[::-1]

def blobCheck(coords, xyn):
    """ get the blob name from a predefined blobposition"""
    columns, rows = countRnC(xyn)
    for i in xrange(len(xyn)):
        if coords[1] < xyn[i][1]:
            for j in xrange(columns):
                if coords[0] < xyn[j][0]:
                    return xyn[i + j][2]

def countRnC(data):
    Columns = 1
    Rows    = 1
    gap     = 10
    for i in xrange(len(data)-1):
        if ((data[i][1] + gap) > data[i+1][1]) & (data[i+1][1] > (data[i][1] - gap)):
            Columns += 1
        else:
            Rows += 1
            Columns = 1
    return Columns, Rows

class ImagePP(object):
    '''docstring for InitialImage'''
    def __init__(self, image, refPts):
        self.image  = image
        self.refPts = refPts

    def getFrame(self):
        '''Get the frame from the camera, convert it to gray, threshold it,
        apply some transformations, then crop it'''
        # Crop to ROI
        # x1,y1            = self.refPts[0][0],self.refPts[0][1]
        # x2,y2            = self.refPts[1][0],self.refPts[1][1]
        sframe           = self.image[self.refPts[0][1]:self.refPts[1][1], self.refPts[0][0]:self.refPts[1][0]]
        # Convert the frame to GRAY, and blur it.
        image            = cv2.cvtColor(sframe, cv2.COLOR_BGR2GRAY)
        # Apply adaptive threshold
        blur             = cv2.GaussianBlur(image, (5, 5), 0)
        ret, thresholded = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) #200 255
        # thresholded    = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]
        # Dialate the thresholded image to fill in holes
        imaget           = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, None, iterations = 1)
        ROI              = cv2.dilate(imaget, None, iterations = 2)
        frame_with_box   = cv2.rectangle(copy.deepcopy(self.image), (self.refPts[0][0], self.refPts[0][1]), (self.refPts[1][0], self.refPts[1][1]), (0,255,0), 1)
        self.keypoints   = self.detectorParameters().detect(ROI)
        return ROI, frame_with_box#, image, thresholded, imaget


    def dataExtract(self,xyn, coordinates):
        """Setup the frame for blob detection"""
        data = [Papillae([round(coords[0],1), round(coords[1],1)]).label(xyn) for coords in coordinates]
        return data


    def detectorParameters(self):
        """Set up the blob detector parameters"""
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 150;
        params.maxThreshold = 255;
        # Filter by Colour
        params.filterByColor = True
        params.blobColor = 255
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 90 # 120, 142
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.7 # 0.8
        # Create a detector with the parameters
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 4:
            self.detector = cv2.SimpleBlobDetector_create(params)
        else :
            self.detector = cv2.SimpleBlobDetector_create(params)
        return self.detector

    def vertical(self,Rows,coords):
        coords = sorted(coords, key=itemgetter(0))
        minmax = []
        chunkedCoords = e.chunker(coords, Rows)
        for row in chunkedCoords:
            c = []
            for item in row:
                c.append(item[0])
            minmax.append([min(c),max(c)])

        minmax[len(minmax)-1][1] = self.refPts[1][0] - self.refPts[0][0]
        minmax.append([self.refPts[1][0] - self.refPts[0][0], self.refPts[1][0] - self.refPts[0][0]])
        midpoints = [(round((minmax[i+1][0] - minmax[i][1]),2))/2 for i in xrange(len(minmax)-1)]
        return midpoints, minmax


    def horizontal(self,Columns,coords):
        minmax = []
        chunkedCoords = e.chunker(coords, Columns)
        for column in chunkedCoords:
            c = []
            for item in column:
                c.append(item[0])
            minmax.append([min(c),max(c)])

        minmax[len(minmax)-1][1] = self.refPts[1][1] - self.refPts[0][1]
        minmax.append([self.refPts[1][1] - self.refPts[0][1], self.refPts[1][1] - self.refPts[0][1]])
        midpoints = [(round((minmax[i+1][0] - minmax[i][1]),2))/2 for i in xrange(len(minmax)-1)]
        return midpoints, minmax


    def chopRC(self):
        roundedCoordinates, crosspointsx, crosspointsy = [], [], []
        coordinates = [self.keypoints[i-1].pt for i in xrange(len(self.keypoints))]
        coordinates = sorted(coordinates, key=itemgetter(1))
        [roundedCoordinates.append((round(coordinates[i][0],1), round(coordinates[i][1],1))) for i in xrange(len(coordinates))]
        Columns, Rows = countRnC(roundedCoordinates)

        Vmidpoints, Vminmax = self.vertical(Rows,roundedCoordinates)
        Hmidpoints, Hminmax = self.horizontal(Columns,roundedCoordinates)
        for i in xrange(len(Hmidpoints)):
            for j in xrange(len(Vmidpoints)):
                crosspointsx.append((int(Vmidpoints[j])+int(Vminmax[j][1])))
                crosspointsy.append((int(Hmidpoints[i])+int(Hminmax[i][1])))
        crosspoints = zip(crosspointsx,crosspointsy)
        for i in xrange(len(crosspoints)):
            crosspoints[i] = crosspoints[i]+(i+1,)
        crosspoints = map(list, crosspoints)
        return Columns, Rows, crosspoints

def vectors(data, kernel, value, percentage=0.9, BearingImage=None):
    centrePins   = []
    extendedPins = []
    test         = lambda x: x<0
    s            = e.size(value)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # textsize = cv2.getTextSize("%.2f" % data[i,j].displacement, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
            # cv2.putText(BearingImage, "%.2f" % data[i,j].displacement, (int(data[i,j].oldPos.x - (textsize[0]/2.0)), int(data[i,j].oldPos.y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            # if data[i,j].state:
            # cv2.line(BearingImage, (int(data[i,j].oldPos.x), int(data[i,j].oldPos.y)), (int(data[i,j].newPos.x + (50 * math.sin(math.radians(data[i,j].bearing)))), int(data[i,j].newPos.y + (50 * math.cos(math.radians(data[i,j].bearing))))), data[i,j].colour, 1)
            cv2.line(BearingImage, (int(data[i,j].oldPos.x), int(data[i,j].oldPos.y)), (int(data[i,j].newPos.x), int(data[i,j].newPos.y)), data[i,j].colour, 2)
            centrePin = convolution(i, j, data, kernel, s, percentage)
            if centrePin != None:
                centrePins.append(centrePin)
    # print len(centrePins)
    if len(centrePins) >= 1:
        for pin in centrePins:
            cv2.circle(BearingImage, (int(pin.oldPos.x), int(pin.oldPos.y)), 4, (0, 0, 255), -1)
    return centrePins

def vectorLines(data, kernel, value, shape, percentage=0.9, BearingImage=None):
    centrePins   = []
    extendedPins = []
    test         = lambda x: x<0
    s            = e.size(value)
    Px = []
    Py = []
    binsx = np.arange(BearingImage.shape[1]+1)
    binsy = np.arange(BearingImage.shape[0]+1)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i,j].state:
                for m in range(data.shape[0]):
                    for n in range(data.shape[1]):
                        if data[m,n].state:
                            denominator = (((data[i,j].oldPos.x - data[i,j].newPos.x)*(data[m,n].oldPos.y - data[m,n].newPos.y)) - ((data[i,j].oldPos.y - data[i,j].newPos.y)*(data[m,n].oldPos.x - data[m,n].newPos.x)))
                            if denominator !=0:
                                x = int(round(((((data[i,j].oldPos.x*data[i,j].newPos.y) - (data[i,j].oldPos.y*data[i,j].newPos.x))*(data[m,n].oldPos.x - data[m,n].newPos.x)) - ((data[i,j].oldPos.x - data[i,j].newPos.x)*((data[m,n].oldPos.x*data[m,n].newPos.y) - (data[m,n].oldPos.y*data[m,n].newPos.x))))/denominator, 0))
                                y = int(round(((((data[i,j].oldPos.x*data[i,j].newPos.y) - (data[i,j].oldPos.y*data[i,j].newPos.x))*(data[m,n].oldPos.y - data[m,n].newPos.y)) - ((data[i,j].oldPos.y - data[i,j].newPos.y)*((data[m,n].oldPos.x*data[m,n].newPos.y) - (data[m,n].oldPos.y*data[m,n].newPos.x))))/denominator, 0))
                                if 0 <= x < BearingImage.shape[1]:
                                    if 0 <= y < BearingImage.shape[0]:
                                        Px.append(x)
                                        Py.append(y)
                                        # BearingImage[y,:] = BearingImage[y,:] - 5
                                        # BearingImage[:,x] = BearingImage[:,x] - 5
                                        cv2.circle(BearingImage, (int(x), int(y)), 1, (100, 100, 100), -1)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i,j].state:
                # cv2.line(BearingImage, (int(data[i,j].oldPos.x - (1000 * math.sin(math.radians(data[i,j].bearing)))), int(data[i,j].oldPos.y - (1000 * math.cos(math.radians(data[i,j].bearing))))), (int(data[i,j].newPos.x + (1000 * math.sin(math.radians(data[i,j].bearing)))), int(data[i,j].newPos.y + (1000 * math.cos(math.radians(data[i,j].bearing))))), data[i,j].colour, 1)
                # cv2.circle(BearingImage, (int(data[i,j].oldPos.x), int(data[i,j].oldPos.y)), 4, data[i,j].colour, -1)
                cv2.line(BearingImage, (int(data[i,j].oldPos.x), int(data[i,j].oldPos.y)), (int(data[i,j].newPos.x + (50 * math.sin(math.radians(data[i,j].bearing)))), int(data[i,j].newPos.y + (50 * math.cos(math.radians(data[i,j].bearing))))), data[i,j].colour, 2)
            # textsize = cv2.getTextSize("%.2f" % data[i,j].displacement, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
            # cv2.putText(BearingImage, "%.2f" % data[i,j].displacement, (int(data[i,j].oldPos.x - (textsize[0]/2.0)), int(data[i,j].oldPos.y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            centrePin = convolution(i, j, data, kernel, s, percentage)
            if centrePin != None:
                centrePins.append(centrePin)
    # print len(centrePins)
    if len(centrePins) >= 1:
        for pin in centrePins:
            cv2.circle(BearingImage, (int(pin.oldPos.x), int(pin.oldPos.y)), 4, (0, 0, 255), -1)
    drawEllipses(Px, Py, BearingImage)
    return centrePins

def gaussian():
    X,Y = np.meshgrid(np.linspace(-1,1,10), np.linspace(-1,1,10))
    D = np.sqrt(X*X, Y*Y)
    sigma, mu = 1.0, 0.0
    gaussian = np.array(np.exp(-((D-mu)**2 / (2.0*sigma**2))))
    return gaussian

def drawEllipses(Px, Py, BearingImage):
    xcenter = np.mean(Px)
    ycenter = np.mean(Py)
    ra      = np.std(Px)
    rb      = np.std(Py)
    ang     = 0
    for i in [0.5, 1, 2, 3]:
        cv2.ellipse(BearingImage, (int(round(xcenter,0)), int(round(ycenter, 0))), (int(round(i*ra, 0)), int(round(i*rb, 0))), ang, 0, 360, (255, 0, 0), 2, 8, 0)

    return BearingImage

def findCentres(data, kernel, value, percentage=0.9):
    centrePins = []
    s          = e.size(value)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            centrePin = convolute(i, j, data, kernel, s, percentage)
            if centrePin != None:
                centrePins.append(centrePin)
    if centrePins:
        return centrePins


def convolute(i, j, data, kernel, s, percentage):
    test      = lambda x: x<0
    sliceData = np.array([element.state for row in data[i-s:i+s, j-s:j+s] for element in row])
    if sliceData.any():
        total   = 0
        counter = 0
        for m in e.linspace(0, -kernel, 1, "-"):
            for n in e.linspace(-kernel, kernel, 1, "+"):
                if m==0:
                    if n>=0:
                        continue
                try:
                    if test(np.dot(data[int(i+m)][int(j+n)].unit.pos, data[int(i+(-m))][int(j+(-n))].unit.pos)):
                        counter+=1
                except IndexError:
                    pass
                total+=1
        if counter>=(total*percentage):
            return data[i,j]

def convolution(i, j, data, kernel, s, percentage):
    test      = lambda x: x<0
    sliceData = np.array([element.state for row in data[i-s:i+s, j-s:j+s] for element in row])
    # if sliceData.any():
    if True:
        counterLeft   = 0
        counterRight  = 0
        counterTop    = 0
        counterBottom = 0
        for m in e.linspace(-kernel, kernel, 1, 1, "+"):
            for n in e.linspace(-kernel, kernel, 1, 1, "+"):
                if m==0:
                    if n==0:
                        continue
                try:
                    if n == -1:
                        if data[int(i+m)][int(j+n)].unit.x < 0:
                            counterLeft+=1
                            # print "Adding to counterLeft"
                        if m == -1:
                            if data[int(i+m)][int(j+n)].unit.y < 0:
                                counterTop+=1
                                # print "Adding to counterTop"
                        if m == 1:
                            if data[int(i+m)][int(j+n)].unit.y > 0:
                                counterBottom+=1
                                # print "Adding to counterBottom"
                    if n == 0:
                        if m == -1:
                            if data[int(i+m)][int(j+n)].unit.y < 0:
                                counterTop+=1
                                # print "Adding to counterTop"
                        if m == 1:
                            if data[int(i+m)][int(j+n)].unit.y > 0:
                                counterBottom+=1
                                # print "Adding to counterBottom"
                    if n == 1:
                        if data[int(i+m)][int(j+n)].unit.x > 0:
                            counterRight+=1
                            # print "Adding to counterRight"
                        if m == -1:
                            if data[int(i+m)][int(j+n)].unit.y < 0:
                                counterTop+=1
                                # print "Adding to counterTop"
                        if m == 1:
                            if data[int(i+m)][int(j+n)].unit.y > 0:
                                counterBottom+=1
                                # print "Adding to counterBottom"
                    # if i == 4:
                    #     if j == 3:
                    #         print m, n, data[int(i+m)][int(j+n)].unit.pos
                    #         print counterTop, counterLeft, counterRight, counterBottom, data[int(i+m)][int(j+n)].number
                except IndexError:
                    pass
        if (counterTop + counterLeft + counterRight + counterBottom) == 12:
            # print i, j
            # print counterTop, counterLeft, counterRight, counterBottom
            return data[i,j]

class threadCentres():
    def __init__(self, data, kernel, value, percentage=0.9, BearingImage=None):
        self.data         = data
        self.kernel       = kernel
        self.percentage   = percentage
        self.BearingImage = BearingImage
        x                 = data.shape[0]-self.kernel
        y                 = data.shape[1]-self.kernel
        # self.work       = [((0, 0), (x/2, y/2)),
        #                    ((x/2, 0), (x, y/2)),
        #                    ((0, y/2), (x/2, y)),
        #                    ((x/2, y/2), (x, y))]

        self.work       = [((0      , 0      ), (x/4    , y/4    )),
                           ((x/4    , 0      ), (x/2    , y/4    )),
                           ((x/2    , 0      ), ((3*x)/4, y/4    )),
                           (((3*x)/4, 0      ), (x      , y/4    )),
                           ((0      , y/4    ), (x/4    , y/2    )),
                           ((x/4    , y/4    ), (x/2    , y/2    )),
                           ((x/2    , y/4    ), ((3*x)/4, y/2    )),
                           (((3*x)/4, y/4    ), (x      , y/2    )),
                           ((0      , y/2    ), (x/4    , (3*y)/4)),
                           ((x/4    , y/2    ), (x/2    , (3*y)/4)),
                           ((x/2    , y/2    ), ((3*x)/4, (3*y)/4)),
                           (((3*x)/4, y/2    ), (x      , (3*y)/4)),
                           ((0      , (3*y)/4), (x/4    , y      )),
                           ((x/4    , (3*y)/4), (x/2    , y      )),
                           ((x/2    , (3*y)/4), ((3*x)/4, y      )),
                           (((3*x)/4, (3*y)/4), (x      , y      )),
                           ]

        # self.work = [((0, 0), (x, y))]

        self.s          = extras.size(value)
        self.q          = Queue.Queue()
        self.a          = Queue.Queue()
        self.printLock  = threading.Lock()

    def findCentres(self):
        print len(self.work)
        for x in range(len(self.work)):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()
        for worker in self.work:
            self.q.put(worker)
        self.q.join()
        with self.printLock:
            return list(self.a.queue)

    def threader(self):
        while True:
            count = 0
            worker = self.q.get()
            for i in range(worker[0][0], worker[1][0]):
                for j in range(worker[0][1], worker[1][1]):
                    with self.printLock:
                        cv2.line(self.BearingImage, (int(self.data[i,j].oldPos.x), int(self.data[i,j].oldPos.y)), (int(self.data[i,j].newPos.x), int(self.data[i,j].newPos.y)), bearingColour(self.data[i,j].bearing), 2)
                    centrePin = self.convolute(i, j)
                    if centrePin != None:
                        self.a.put(centrePin)
                    count += 1
            with self.printLock:
                if count < 10:
                    print worker
            self.q.task_done()

    def convolute(self, i, j):
        test      = lambda x: x<0
        sliceData = np.array([element.state for row in self.data[i-self.s:i+self.s, j-self.s:j+self.s] for element in row])
        if sliceData.any():
            total   = 0
            counter = 0
            for m in extras.linspace(0, -self.kernel, 1, "-"):
                for n in extras.linspace(-self.kernel, self.kernel, 1, "+"):
                    if m==0:
                        if n>=0:
                            continue
                    if test(np.dot(self.data[int(i+m)][int(j+n)].unit.pos, self.data[int(i+(-m))][int(j+(-n))].unit.pos)):
                        counter+=1
                    total+=1
            if counter>=(total*self.percentage):
                return self.data[i,j]
