import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../libraries/MachineVisionAndmore")
from PillowEdited import rw
import numpy as np
import time
from matplotlib import pyplot as plt
from sklearn import linear_model
from operator import itemgetter
from itertools import groupby
np.set_printoptions(precision=3, suppress=True, linewidth = 150)

def makedir(DIR):
    if not os.path.exists(DIR):
        os.makedirs(DIR)
        time.sleep(0.5)

ztool        = 167.5
zcoordinate  = 350.0
directory    = os.path.join("..", "..", "IROS")
makedir(directory)
DIR          = os.path.join("..", "..", "TSP_Pictures", "NewPillowRotationTest", "RotationTest{0}".format(ztool), "{0}mm".format(zcoordinate))
# data       = np.load(os.path.join(DIR, "Otsudataline110.npy"))
data         = np.load(os.path.join(DIR, "dataline110.npy"))
print "Loaded Data"
names        = data.dtype.names
Column0      = names.index('Displacement')
Column1      = names.index('DifferenceX')
Column2      = names.index('DifferenceY')
axe          = 'Ry'
savingtext   = 0
savingGraph  = 1
Sets         = int(1 + len([name for name in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, name))]))
# Choose between using displacement or the change in x and y
for single in range(1):
    SaveDataArray = []

    # split the data into training and testing sets. for loops are to run the program quickly with different splits of training and testing sets.
    set_ = 9
    # for set_ in range(10, 11):
    # for set_ in range(2, Sets):
    SaveDataLine  = []

    # Choose the size of the step i.e. use every data point, every second data point etc. for loops are to run the program quickly with different steps.
    step = 1
    # for step in range(1, 2):
    # for step in range(1, Sets):

    # Create a Bayesian Ridge model for fitting.
    gnb = linear_model.BayesianRidge()
    # Initialise lists for containing data and labels.
    train, test, labels1, labels2, labels3, labels4, label1, label2, label3, label4 = [], [], [], [], [], [], [], [], [], []
    # Loop though the data and separate the data into training and testing data.
    for _, values in enumerate(data[['Displacement', 'DifferenceX', 'DifferenceY', 'Bearing', 'X', 'Y', 'Z', 'Rx', 'Ry', 'Rz', 'DataSet', 'State', 'Type', 'Sign']]):

        # filter the data to only include data from certain rotations.
        if values['Type'][0] == axe:

            # Filter the data to only include data from pictures where atleast four pins have moved a significant amount.
            if np.count_nonzero(values['State']) > 4:

                # Skip data values corresponding with the step size.
                if (round((data[values['Type'][0]][0][0] - abs(values[values['Type'][0]][0]))*10, 0)) % step == 0:

                    # the data from datasets numbered 0 to set_ are added to the training sets.
                    if 0 < values['DataSet'][0] < set_:
                        if single:
                            train.append(np.concatenate(((values[names[Column0]]*10).astype(int), )))
                        else:
                            train.append(np.concatenate(((values[names[Column1]]*10).astype(int), (values[names[Column2]]*10).astype(int))))
                        # Save some information about the data
                        labels1.append(values['Type'][0])
                        labels2.append(values['Sign'][0])
                        labels3.append(str(int(round((data[values['Type'][0]][0][0] - abs(values[values['Type'][0]][0]))*10, 0))*np.sign(values[values['Type'][0]][0])*-1) + values['Type'][0] + values['Sign'][0])
                        labels4.append(int(round((data[values['Type'][0]][0][0] - abs(values[values['Type'][0]][0]))*10, 0))*np.sign(values[values['Type'][0]][0])*-1)
                    # otherwise include the data in the testing sets.
                    else:
                        if single:
                            test.append(np.concatenate(((values[names[Column0]]*10).astype(int), )))
                        else:
                            test.append(np.concatenate(((values[names[Column1]]*10).astype(int), (values[names[Column2]]*10).astype(int))))
                        label1.append(values['Type'][0])
                        label2.append(values['Sign'][0])
                        label3.append(str(int(round((data[values['Type'][0]][0][0] - abs(values[values['Type'][0]][0]))*10, 0))*np.sign(values[values['Type'][0]][0])*-1) + values['Type'][0] + values['Sign'][0])
                        label4.append(int(round((data[values['Type'][0]][0][0] - abs(values[values['Type'][0]][0]))*10, 0))*np.sign(values[values['Type'][0]][0])*-1)

    # convert all the lists to numpy arrays
    print "\nSetting up train and test sets."
    train   = np.array(train)
    test    = np.array(test)
    labels1 = np.array(labels1)
    label1  = np.array(label1)
    labels2 = np.array(labels2)
    label2  = np.array(label2)
    labels3 = np.array(labels3)
    label3  = np.array(label3)
    labels4 = np.array(labels4)
    label4  = np.array(label4)
    print len(train), len(test)
    print "Predicting the Rotation"
    y_pred3  = gnb.fit(train, labels4).predict(test)
    y_pred3z = zip(y_pred3, label4)

    predictions        = sorted(y_pred3z, key=itemgetter(1))
    # Group the predictions based on the actual depth
    groupedPredictions = np.array([list(j) for i,j in groupby(map(list,predictions), itemgetter(1))])
    # Calculate the mean and mad of the difference between the values
    madPredictions     = np.array([np.mean(abs(np.subtract(abs(np.subtract([c[0] for c in b], [c[1] for c in b])), np.mean(abs(np.subtract([c[0] for c in b], [c[1] for c in b])))))) for b in groupedPredictions])
    meanPredictions    = np.array([np.mean(abs(np.subtract([c[0] for c in b], [c[1] for c in b]))) for b in groupedPredictions])
    stdPredictions     = np.array([np.std(abs(np.subtract([c[0] for c in b], [c[1] for c in b]))) for b in groupedPredictions])
    xValues = [float(b[0][1])/10 for b in groupedPredictions]

    print "Trained Classifier"
    # print("Number of mislabeled points out of a total %d points : %d" % (test.shape[0], np.array(label3 != y_pred3).sum()))
    print "Score = {0}%, {1}mm, #{2}".format(round(gnb.score(test,label4)*100, 3), float(step)/10, set_-1)
    # print y_pred3z
    SaveDataLine.append(gnb.score(test,label4))
    gnb = False
    SaveDataArray.append(SaveDataLine)
    if single:
        Name = "TSP_Rotation_Displacement_{0}".format(axe)
    else:
        Name = "TSP_Rotation_DistanceX_and_DistanceY_{0}".format(axe)
    # if single:
    #     Name = "Using Pin Displacement for the features of the Regression Model"
    # else:
    #     Name = "Using Delta X and Delta Y for the features of the Regression Model"
    # if single:
    #     Name = "TSP_Rotation_Displacement_Otsu"
    # else:
    #     Name = "TSP_Rotation_DistanceX_DistanceYO_tsu"
    print os.path.join(directory, Name)
    if savingtext:
        rw().writeList2File(os.path.join(directory, Name + ".txt"), SaveDataArray)
    print SaveDataArray

    if savingGraph:
        fig = plt.figure()
        ax  = plt.subplot(1,1,1)
        head = 'Training Sets: {0}    Testing Sets: {1}    Step distance: {2} Degrees'.format(set_-1, Sets-set_, float(step)/10)
        plt.title(Name + '\n' + head)
        plt.xlabel("Actual Angle, (Degrees)")
        # plt.ylabel("Angular Displacement, (Degrees)")
        plt.ylabel("Predicted Angle, (Degrees)")

        major_ticks = np.arange(-12, 12, 1)
        minor_ticks = np.arange(-12, 12, 0.2)

        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)

        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)

        ax.grid(which='major', alpha=1)

        # ax.grid(which='minor', alpha=0.5)
        # ax.set_xlim(-2,2)
        # ax.set_ylim(-2,2)

        x1                = [float(i[1])/10 for i in y_pred3z]
        y1                = [float(i[0])/10 for i in y_pred3z]
        labels4           = [float(i)/10 for i in label4]
        toMatlab          = zip(x1, y1)
        best_fit          = plt.plot(labels4, labels4, 'r-', label="Correct Value")
        Error             = plt.bar(x1, abs(np.subtract(x1, y1)), 0.1, label="Error")
        Classifier_Output = plt.scatter(x1, y1, c='blue', marker="x", label="Machine Learning Output")
        # MAD  = plt.plot(xValues, madPredictions, label="Deviation of the data from the mean")
        # mean = plt.plot(xValues, meanPredictions, label="Mean difference between actual and predicted")
        handles, labels   = ax.get_legend_handles_labels()
        header = [['Actual', 'Predicted', head]]
        header = header + map(list, toMatlab)
        rw().writeList2File(os.path.join(directory, Name + ".txt"), header)
        # print "Saved for Matlab"
        # plt.annotate('Rotation Y', xy=(-5, -4), xytext=(-10, 0), arrowprops=dict(facecolor='black', shrink=0.2))
        # plt.annotate('Rotation X', xy=(5, 6), xytext=(0, 10), arrowprops=dict(facecolor='black', shrink=0.2))
        plt.legend(handles, labels, loc=2)
        plt.savefig(os.path.join(directory, Name + '.png'), dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
        plt.show()
