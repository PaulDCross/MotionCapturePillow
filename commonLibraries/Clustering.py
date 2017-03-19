import Vector as v
import random
import numpy as np

class Clusters(object):
    """Clusters(data, iterations, K=2)

        Parameters
        ==========
        data        = list of positions
        i           = number of iterations to atempt to converge
        K           = number of clusters

        Attributes
        ==========
        clusters    = a list containing the cluster objects.
        data        = a list containing Vector objects of the data parameter.
        positions   = a list containing the positions in array format of the clusters.

        Methods
        =======
        run(i)      = calls the update() method for i number of times
        update()    = calculates the distance between each data point position and the current cluster
                      candidate position and then adds the data point to the closest cluster.
                      For each cluster, it's update() method is called and then new cluster objects are
                      made with the positions calculated from the mean position of the data points within
                      the current clusters. The old clusters are no longer refereced and so disappear.

    """
    def __init__(self, data, iterations, K=2):
        self.K         = K
        self.clusters  = [Cluster([random.randint(int(min(data[0])),int(max(data[0]))), random.randint(int(min(data[1])), int(max(data[1])))], i) for i in range(self.K)]
        self.data      = [v.Vector([element[0], element[1]]) for element in zip(*data)]
        self.positions = [cluster.pos.pos for cluster in self.clusters]
        self.run(iterations)


    def run(self, iterations):
        # for iteration in range(iterations):
        previous = [[0, 0]]*self.K
        while previous != self.positions:
            # print previous, self.positions
            previous = self.positions
            self.update()
            self.positions = [cluster.pos.pos for cluster in self.clusters]

    def update(self):
        for data in self.data:
            distance = [data.sub(cluster.pos).mag() for cluster in self.clusters]
            self.clusters[distance.index(min(distance))].addData(data)
        for cluster in self.clusters:
            cluster.update()
        self.clusters = [Cluster([cluster.pos.x, cluster.pos.y], i) for i, cluster in enumerate(self.clusters)]

class Cluster(object):
    """Cluster(x, y, number)

        Parameters
        ==========
        x       = the x coordinate of a data point.
        y       = the y coordinate of a data point.
        number  = the identity of the cluster, an integer value.

        Attributes
        ==========
        pos     = a Vector object made using the x and y parameters
        number  = the identity of the cluster, an integer value.
        cluster = an array containing Vector objects of the data.

        Methods
        =======
        addData(data)       = adds data to the cluster attribute.
        removeData(data)    = removes data from the cluster attribute.
        update()            = calculates the mean position of the data contained in cluster and updates
                              pos to be a Vector object of the mean values.

    """
    def __init__(self, xy, number):
        self.pos     = v.Vector(xy)
        self.number  = number
        self.cluster = []

    def addData(self, data):
        self.cluster.append(data)

    def removeData(self, data):
        del self.cluster[data]

    def update(self):
        # print "Position: ", self.pos.pos
        if len(self.cluster) == 1:
            self.cluster*2
        meanValue = np.array([element.pos for element in self.cluster]).mean(0)
        # print self.cluster
        # print "mean: ", meanValue
        self.pos  = v.Vector(meanValue)
