from operator import itemgetter
import numpy as np
import sys, os
import cv2
import math
import time
import copy
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
import mcpLibraries.preprocessingWithClass as pp
import commonLibraries.extras as e
import commonLibraries.Vector as v
import commonLibraries.Clustering as c
import itertools
from scipy.interpolate import griddata, interp2d
import matplotlib.pyplot as plt

np.set_printoptions(precision=3, suppress=True, linewidth = 250)

Dictionary = {
    'Display'          : 1,
    'Record'           : 0,
    'interpolating'    : 0,
    'extrnl'           : 0,
    'resolutionX'      : 30,
    'resolutionY'      : 16,
    'ztool'            : 167.5,
    'zcoordinate'      : 358.0,
    'zcoordinate2'     : 350.0,
    'Sign'             : ['P', 'N'],
    'ProgramsData'     : os.path.join("..", "..","TSP_Pictures"),
    'refPt'            : [(124, 83), (1057, 585)],
    'Start'            : 1
    # 'End'              : int(1 + len([name for name in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, name))]))
}
# Dictionary['DIR'] = os.path.join(Dictionary['ProgramsData'], "TSP_Pictures", "NewPillowRepeatabilityTest", "EE{0}".format(Dictionary['ztool']), "{0}mm".format(Dictionary['zcoordinate']))
Dictionary['DIR']        = os.path.join(Dictionary['ProgramsData'], "NewPillowRotationTest", "RotationTest{0}".format(Dictionary['ztool']), "{0}mm".format(Dictionary['zcoordinate2']))
Dictionary['End']        = int(1 + len([name for name in os.listdir(Dictionary['DIR']) if os.path.isdir(os.path.join(Dictionary['DIR'], name))]))
if Dictionary['Record']:
    savepath = os.path.join('TrackingIntersectionMean', *Dictionary['DIR'].split('\\')[2:])
    savepath = os.path.join(savepath)
    e.makedir(savepath)
    savepath = os.path.join(savepath, "0{}".format(int(1 + len([name for name in os.listdir(savepath) if os.path.isdir(os.path.join(savepath, name))]))))
    e.makedir(savepath)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'CVID')
    out    = cv2.VideoWriter(os.path.join(savepath, "InterpolatedIntersections.avi"), fourcc, 20.0, (900,500))

for fold in range(Dictionary['Start'], Dictionary['End']):
    directory = os.path.join(Dictionary['DIR'], "%02d" % fold)
    for Type in [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]:
        # print MovementType
        MovementType   = os.path.join(directory, Type)
        #######################################################################################################
        # if True:
            # PictureFolder  = os.path.join(MovementType, "Internal")
            # PictureFolderE = os.path.join(MovementType, "External")

            # with open(os.path.join(directory, "LogFile.txt")) as File:
            #     Textfile = [line for line in File.read().splitlines() if line]
            #     lineNums = [_ for _,s in enumerate(Textfile) if 'Starting Sequence:' in s]
            # ls = []
            # for _,i in enumerate(lineNums):
            #     with open(os.path.join(directory, "LogFile.txt")) as File:
            #         resultlist = [line.split(":  [[")[-1].split("]] ")[0].split("], [")[0].split(", ") + line.split(":  [[")[-1].split("]]")[0].split("], [")[1].split(", ") for line in itertools.islice(Textfile, lineNums[_]+5, None, 3)]
            #         del resultlist[-1]
            #         resultlist.insert(0, [Textfile[lineNums[_]].split("\\")[-1][0][0]])
            #         ls.append(resultlist)
            #         if [Type] in resultlist:
            #             index = len(ls)-1
            ###################################################################################################

        ###################################################################################################
        for sign in Dictionary['Sign']:
            PictureFolder  = os.path.join(MovementType, sign, "Internal")
            PictureFolderE = os.path.join(MovementType, sign, "External")


            # if Dictionary['Record']:
            #     # Define the codec and create VideoWriter object
            #     fourcc = cv2.VideoWriter_fourcc(*'CVID')
            #     out    = cv2.VideoWriter(os.path.join(savepath, "{}{}0{}.avi".format(Type, sign, fold)), fourcc, 20.0, (900,500))


            with open(os.path.join(directory, "LogFile.txt")) as File:
                Textfile = [line for line in File.read().splitlines() if line]
                lineNums = [_ for _,s in enumerate(Textfile) if 'Starting Sequence:' in s]
            ls = []
            for _,i in enumerate(lineNums):
                if _+1 < 4:
                    with open(os.path.join(directory, "LogFile.txt")) as File:
                        resultlist = [line.split(":  [[")[-1].split("]] ")[0].split("], [")[0].split(", ") + line.split(":  [[")[-1].split("]] ")[0].split("], [")[1].split(", ") for line in itertools.islice(Textfile, lineNums[_]+5, lineNums[_+1], 3)]
                        resultlist.insert(0, [Textfile[lineNums[_]].split("\\")[-2], Textfile[lineNums[_]].split("\\")[-1][0][0]])
                        ls.append(resultlist)
                        if [Type, sign] in resultlist:
                            index = len(ls)-1
                else:
                    with open(os.path.join(directory, "LogFile.txt")) as File:
                        resultlist = [line.split(":  [[")[-1].split("]] ")[0].split("], [")[0].split(", ") + line.split(":  [[")[-1].split("]] ")[0].split("], [")[1].split(", ") for line in itertools.islice(Textfile, lineNums[_]+5, None, 3)]
                        del resultlist[-1]
                        resultlist.insert(0, [Textfile[lineNums[_]].split("\\")[-2], Textfile[lineNums[_]].split("\\")[-1][0][0]])
                        ls.append(resultlist)
                        if [Type, sign] in resultlist:
                            index = len(ls)-1

            ###############################################################################################

            first      = 2
            last       = (len([name for name in os.listdir(PictureFolder) if os.path.isfile(os.path.join(PictureFolder, name))]))
            pathname1  = os.path.join(PictureFolder, "%003d" % 1) + ".png"
            FirstImage = cv2.imread(pathname1)
            # If the first picture is valid
            if (FirstImage.all()):
                # Setup the first image
                init                 = pp.ImagePP(FirstImage, Dictionary['refPt'])
                ROI1, frame_with_box = init.getFrame()
                Columns, Rows, xyn   = init.chopRC()
                # Find the coordinates of the pins in the first image
                data1                = init.dataExtract(xyn, [x.pt + (x.size,) for x in init.keypoints])
                data1.sort(key=lambda x: x.ID, reverse=False)
                BearingImage = np.zeros((round((Dictionary['refPt'][1][1] - Dictionary['refPt'][0][1])*0.01)*100, round((Dictionary['refPt'][1][0] - Dictionary['refPt'][0][0])*0.01)*100, 3), np.uint8)

            for picture in range(first, last, 1):
                start = time.time()
                pathname2    = os.path.join(PictureFolder, "%003d" % picture) + ".png"
                SecondImage  = cv2.imread(pathname2)
                BearingImage.fill(255)

                if (SecondImage.any()):
                    print fold, Type, sign, first, picture
                    # Set up the second image
                    rec                 = pp.ImagePP(SecondImage, Dictionary['refPt'])
                    ROI, frame_with_box = rec.getFrame()
                    # Set the detectors parametors and detect blobs.
                    # Draw detected blobs as red circles. cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
                    data2               = [(pp.blobCheck([round(coords[0],1), round(coords[1],1)], xyn), ) + coords for coords in [x.pt + (x.size,) for x in rec.keypoints]]
                    data2.sort(key = itemgetter(0),reverse = False)

                    for pin, coords in zip(data1, data2):
                        pin.update([round(coords[1],1), round(coords[2],1)])

                    DATA = [[pin.ID, pin.oldPos.x, pin.oldPos.y, pin.difference.x, pin.difference.y, pin.state] for pin in data1 if pin.state]
                    DATA = np.array(DATA).T

                    if len(DATA):
                        if Dictionary['interpolating']:
                            xi, step1   = np.linspace(0, BearingImage.shape[1], Dictionary['resolutionX'], retstep=True)
                            yi, step2   = np.linspace(0, BearingImage.shape[0], Dictionary['resolutionY'], retstep=True)
                            xx, yy      = np.meshgrid(xi,yi)
                            zx          = griddata((DATA[1], DATA[2]), DATA[3], (xx, yy), method='cubic')
                            zy          = griddata((DATA[1], DATA[2]), DATA[4], (xx, yy), method='cubic')

                            data1D      = np.array(zip(xx.reshape(-1), yy.reshape(-1), zx.reshape(-1), zy.reshape(-1)))
                            classedData = [pp.PapillaePin(entry[:2]) for entry in data1D]
                            for pin, entry in zip(classedData, data1D):
                                pin.update(pin.oldPos.add(v.Vector(entry[2:])).pos)
                            data2D      = np.array(e.chunker(classedData, Dictionary['resolutionX']))

                            # centrePins  = pp.vectors(data2D, 2, Dictionary['resolutionX'], 0.9, BearingImage)
                            centrePins, stdxy = pp.vectorLines(data2D, 1, Columns, BearingImage.shape, 0.9, BearingImage)
                            # centrePins = pp.findCentres(data2D, 3, Dictionary['resolutionX'], 0.9)
                            # centrePins = pp.threadCentres(data2D, 3, Dictionary['resolutionX'], 0.9).findCentres()
                        else:
                            data2D     = np.array(e.chunker(data1, Columns))
                            # centrePins = pp.findCentres(data2D, 2, Columns, 0.9)
                            # centrePins = pp.vectors(data2D, 1, Columns, 0.9, BearingImage)
                            centrePins, stdxy = pp.vectorLines(data2D, 1, Columns, BearingImage.shape, 0.9, BearingImage)

                    if picture == first:
                        locationArray    = [['Picture Number', 'Mean X Coordinate', 'Mean Y Coordinate', 'std X', 'std Y']]
                    if (len(centrePins) >= 1):
                        if 0 < len(centrePins) < 2:
                            centrePins = centrePins*2
                        centrePinPositions = np.array([positions.oldPos.pos for positions in centrePins]).T
                        clusters = c.Clusters(centrePinPositions, 5, 1)
                        centres  = clusters.positions
                        [cv2.circle(BearingImage, (int(centre[0]), int(centre[1])), 4, (255, 0, 0), -1) for centre in centres]
                        meanCentre = np.array(centres).mean(0)
                        locationArray.append([picture, meanCentre[0], meanCentre[1], stdxy[0], stdxy[1]])

                    textsize = cv2.getTextSize(str('{}, {}, {}, {}, {}'.format(fold, Type, sign, first, picture)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                    width    = 60
                    cv2.putText(BearingImage, str('{}, {}, {}, {}, {}'.format(fold, Type, sign, first, picture)), (BearingImage.shape[1]-textsize[0][0]-20,BearingImage.shape[0]-textsize[0][1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

                    if Dictionary['Record']:
                        print "Writing"
                        out.write(BearingImage)

                    if Dictionary['Display']:
                        # cv2.imshow("Camera", video)
                        cv2.imshow("Camera2", BearingImage)
                        # cv2.imshow("Camera3", frame_with_box)
                        # cv2.imshow("Frame", Frame)

                        if cv2.waitKey(10) & 0xFF == 27:
                            cv2.destroyAllWindows()
                            sys.exit()
                    # plt.show()
                print "Time Taken: ", time.time()-start
                # if picture == 2:
                    # sys.exit()
            # if Dictionary['Record']:
            #     print "released"
            #     out.release()

            # e.writeList2File(os.path.join(savepath, "{}{}0{}_resolution{}_{}.txt".format(Type, sign, fold, Dictionary['resolutionX'], Dictionary['resolutionY'])), locationArray)

if Dictionary['Record']:
    print "released"
    out.release()
cv2.destroyAllWindows()
