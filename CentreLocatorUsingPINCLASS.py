from operator import itemgetter
import numpy as np
import sys, os
import cv2
import math
import time
import copy
import myLibraries.mcpLibraries.preprocessingWithClass as pp
import myLibraries.Vector as v
import myLibraries.extras as e
import myLibraries.Clustering as c
import itertools
from scipy.interpolate import griddata, interp2d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.set_printoptions(precision=3, suppress=True, linewidth = 150)

Dictionary = {
    'Display'          : 0,
    'Record'           : 0,
    'interpolating'    : 0,
    'extrnl'           : 0,
    'resolutionX'      : 180,
    'resolutionY'      : 100,
    'ztool'            : 167.5,
    'zcoordinate'      : 358.0,
    'zcoordinate2'     : 350.0,
    'Sign'             : ['P', 'N'],
    'refPts'           : [(124, 83), (1057, 585)],
    'Start'            : 1
}

firstDIR   = os.path.join('RelaxedCalibratedState', 'image.png')
secondDIR  = os.path.join('TwoSources', 'image.png')

FirstImage = cv2.imread(firstDIR)
centrePins = None

# If the first picture is valid
if (FirstImage.any()):
    # Setup the first image
    init                 = pp.ImagePP(FirstImage, Dictionary['refPts'])
    ROI1, frame_with_box = init.getFrame() #, Alpha, Beta, Charlie
    # cv2.imwrite("ProjectPictures_GreyScale.png", Alpha)
    # cv2.imwrite("ProjectPictures_Binary.png", Beta)
    # cv2.imwrite("ProjectPictures_Morphology.png", Charlie)
    # cv2.imwrite("ProjectPictures_ROI.png", ROI1)
    Columns, Rows, xyn   = init.chopRC()
    # Find the coordinates of the pins in the first image
    data1                = init.dataExtract(xyn, [x.pt + (x.size,) for x in init.keypoints])
    data1.sort(key=lambda x: x.number, reverse=False)

    SecondImage  = cv2.imread(secondDIR)
    frame        = copy.deepcopy(SecondImage)
    BlackImage   = np.zeros((frame.shape[0], Dictionary['refPts'][1][0] - Dictionary['refPts'][0][0], 3), np.uint8); BlackImage.fill(255)
    BearingImage = copy.deepcopy(BlackImage[Dictionary['refPts'][0][1]:Dictionary['refPts'][1][1], 0:Dictionary['refPts'][1][0] - Dictionary['refPts'][0][0]])

    if (SecondImage.any()):
        rec                 = pp.ImagePP(SecondImage, Dictionary['refPts'])
        ROI, frame_with_box = rec.getFrame()
        data2               = [(pp.blobCheck([round(coords[0],1), round(coords[1],1)], xyn), ) + coords for coords in [x.pt + (x.size,) for x in rec.keypoints]]
        data2.sort(key = itemgetter(0),reverse = False)

        for pin, coords in zip(data1, data2):
            pin.update([round(coords[1],1), round(coords[2],1)])

        DATA = [[pin.number, pin.oldPos.x, pin.oldPos.y, pin.difference.x, pin.difference.y, pin.state] for pin in data1 if pin.state]
        DATA = np.array(DATA).T

        if len(DATA):
            if Dictionary['interpolating']:
                xi, step1   = np.linspace(0, round(BearingImage.shape[1]*0.01)*100, Dictionary['resolutionX'], retstep=True)
                yi, step2   = np.linspace(0, round(BearingImage.shape[0]*0.01)*100, Dictionary['resolutionY'], retstep=True)
                zer         = np.zeros((Dictionary['resolutionX'], Dictionary['resolutionY']))
                xx, yy      = np.meshgrid(xi,yi)
                zx          = griddata((DATA[1], DATA[2]), DATA[3], (xx, yy), method='cubic')
                zy          = griddata((DATA[1], DATA[2]), DATA[4], (xx, yy), method='cubic')

                data1D      = np.array(zip(xx.reshape(-1), yy.reshape(-1), zx.reshape(-1), zy.reshape(-1)))#, zer.reshape(-1), zer.reshape(-1)))
                classedData = [pp.Papillae(entry[:2]) for entry in data1D]
                for pin, entry in zip(classedData, data1D):
                    pin.update(pin.oldPos.add(v.Vector(entry[2:])).pos)
                DATA = [[pin.oldPos.x, pin.oldPos.y, pin.difference.x, pin.difference.y] for pin in classedData]
                data2D      = np.array(e.chunker(classedData, Dictionary['resolutionX']))

                centrePins = pp.vectors(data2D, 1, Dictionary['resolutionX'], 0.9, BearingImage)
                # centrePins  = pp.findCentres(data2D, 3, Dictionary['resolutionX'], 0.9)
                # centrePins  = pp.threadCentres(data2D, 3, Dictionary['resolutionX'], 0.9).findCentres()
            else:
                data2D     = np.array(e.chunker(data1, Columns))
                # centrePins  = pp.findCentres(data2D, 2, Columns, 0.9)
                centrePins = pp.vectors(data2D, 1, Columns, 0.9, BearingImage)
                # centrePins = pp.vectorLines(data2D, 1, Columns, BearingImage.shape, 0.9, BearingImage)

            # plt.figure()
            # ax = plt.subplot(111)
            # plt.axis([0, Dictionary['refPts'][1][0]-Dictionary['refPts'][0][0], 0, Dictionary['refPts'][1][1]-Dictionary['refPts'][0][1]])
            # quiverData = np.array([[data.oldPos.x, data.oldPos.y, data.unit.x, data.unit.y, data.displacement] for data in classedData]).T
            # plt.quiver(quiverData[0], quiverData[1], quiverData[2], quiverData[3], quiverData[4])#, cmap=plt.cm.coolwarm, linewidth=0)
            # # plt.quiver([data.oldPos.x for data in data1], [data.oldPos.y for data in data1], [data.unit.x for data in data1], [data.unit.y for data in data1])
            # handles, labels = ax.get_legend_handles_labels()

            if (len(centrePins) >= 1):
                if 0 < len(centrePins) < 2:
                    centrePins = centrePins*2
                centrePinPositions = np.array([positions.oldPos.pos for positions in centrePins]).T
                clusters = c.Clusters(centrePinPositions, 5, 2)
                centres  = clusters.positions
                [cv2.circle(BearingImage, (int(centre[0]), int(centre[1])), 4, (255, 0, 0), -1) for centre in centres]
                meanCentre = np.array(centres).mean(0)
                # plt.scatter(centrePinPositions[0], centrePinPositions[1], c='r')
                # [plt.scatter(centre[0], centre[1]) for centre in centres]

    cv2.imshow("Camera2", BearingImage)
    # cv2.imshow("dst", dst)
    # cv2.imwrite("TwoSources.png", BearingImage)

    if cv2.waitKey(0) & 0xFF == 27:
        cv2.destroyAllWindows()
        sys.exit()
    cv2.destroyAllWindows()
    # plt.show()
