import numpy as np
import math
import random
from commonLibraries import Vector, Clustering, extras
import pygame

class Boids(object):
    """docstring for Boids"""
    def __init__(self, display, walls):
        self.boids = []
        self.walls = walls
        self.gameDisplay = display

    def addBoid(self, pos):
        self.boids.append(Boid(pos))

    def flock(self, globalTarget):
        for boid in self.boids:
            self.applyWalls(boid)
            boid.seek(globalTarget)
            boid.flock(self.boids)
            boid.update()
            boid.display(self.gameDisplay)

    def applyWalls(self, boid):
        wall = False
        if boid.pos.x < self.walls[0]:
            desired = Vector.Vector([boid.maxspeed, boid.vel.y])
            wall    = True
        if boid.pos.x > self.walls[1]:
            desired = Vector.Vector([-boid.maxspeed, boid.vel.y])
            wall    = True
        if boid.pos.y < self.walls[2]:
            desired = Vector.Vector([boid.vel.x, boid.maxspeed])
            wall    = True
        if boid.pos.y > self.walls[3]:
            desired = Vector.Vector([boid.vel.x, -boid.maxspeed])
            wall    = True
        if wall:
            steer = desired.sub(boid.vel)
            if extras.upperLimit(steer.mag(), boid.maxforce) == boid.maxforce:
                steer = steer.unit().mulScalar(boid.maxforce*1.5)
            boid.addForce(steer)

class Boid(object):
    """docstring for Boid"""
    def __init__(self, pos):
        self.acc               = Vector.Vector([0, 0])
        self.vel               = Vector.Vector([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)])
        self.pos               = Vector.Vector([pos[0], pos[1]])
        self.theta             = random.uniform(-math.pi, math.pi)
        self.boidSize          = 10
        self.desiredSeparation = self.boidSize*2
        self.neighbourhoodDist = 4*self.desiredSeparation
        self.maxspeed          = 4
        self.maxforce          = 0.2

    def update(self):
        self.vel = self.vel.add(self.acc)
        if extras.upperLimit(self.vel.mag(), self.maxspeed) == self.maxspeed:
            self.vel = self.vel.unit().mulScalar(self.maxspeed)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector.Vector([0, 0])

    def addForce(self, force):
        self.acc = self.acc.add(force)

    def seek(self, globalTarget):
        self.Centre            = self.pos.add(self.vel.mulScalar(self.boidSize/2))
        self.theta             = random.uniform(self.theta-0.5, self.theta+0.5)
        randomPointOnCircle    = Vector.Vector([self.boidSize*math.cos(self.theta), self.boidSize*math.sin(self.theta)])
        self.randomLocalTarget = self.Centre.add(randomPointOnCircle)

        if globalTarget == None:
            desired = self.randomLocalTarget.sub(self.pos).unit().mulScalar(self.maxspeed)
        else:
            globalTarget = Vector.Vector(globalTarget)
            desired = globalTarget.sub(self.pos).unit().mulScalar(self.maxspeed).sub(self.randomLocalTarget.sub(self.pos).unit().mulScalar(self.maxspeed).mulScalar(0.4))

        desired = desired.sub(self.vel)
        if extras.upperLimit(desired.mag(), self.maxforce) == self.maxforce:
            desired = desired.unit().mulScalar(self.maxforce)
        self.addForce(desired)

    def flock(self, boids):
        Dictionary = self.rules(boids)
        try:
            separationForce = Dictionary['Separation'].mulScalar(1.0)
            self.addForce(separationForce)
        except KeyError:
            pass
        try:
            cohesionForce   = Dictionary['Cohesion'].mulScalar(1.1)
            self.addForce(cohesionForce)
        except KeyError:
            pass
        try:
            directionForce  = Dictionary['Direction'].mulScalar(1)
            self.addForce(directionForce)
        except KeyError:
            pass

    def rules(self, boids):
        separationCount        = 0
        cohesionCount          = 0
        summedSeparationVector = Vector.Vector([0, 0])
        summedCohesionVector   = Vector.Vector([0, 0])
        summedDirectionVector  = Vector.Vector([0, 0])
        Dictionary             = {}

        for boid in boids:
            d = self.pos.sub(boid.pos).mag()
            if 0<d<self.desiredSeparation:
                summedSeparationVector = summedSeparationVector.add(self.pos.sub(boid.pos).unit())
                separationCount += 1
            if 0<d<self.neighbourhoodDist:
                summedCohesionVector = summedCohesionVector.add(self.pos.sub(boid.pos).unit())
                summedDirectionVector = summedDirectionVector.add(boid.vel)
                cohesionCount += 1

        if separationCount>0:
            separationSteering = summedSeparationVector.mulScalar(1.0/separationCount).unit().mulScalar(self.maxspeed).sub(self.vel)
            if extras.upperLimit(separationSteering.mag(), self.maxforce) == self.maxforce:
                separationSteering = separationSteering.unit().mulScalar(self.maxforce)
            Dictionary['Separation'] = separationSteering

        if cohesionCount>0:
            cohesionSteering = summedCohesionVector.mulScalar(1.0/cohesionCount).unit().mulScalar(-self.maxspeed).sub(self.vel)
            if extras.upperLimit(cohesionSteering.mag(), self.maxforce) == self.maxforce:
                cohesionSteering = cohesionSteering.unit().mulScalar(self.maxforce)
            Dictionary['Cohesion'] = cohesionSteering

            directionSteering = summedDirectionVector.mulScalar(1.0/cohesionCount).unit().mulScalar(self.maxspeed).sub(self.vel)
            if extras.upperLimit(directionSteering.mag(), self.maxforce) == self.maxforce:
                directionSteering = directionSteering.unit().mulScalar(self.maxforce)
            Dictionary['Direction'] = directionSteering

        return Dictionary

    def display(self, frame):
        debugging      = False
        triangle       = extras.polygon(3, self.boidSize)
        theta          = math.atan2(self.vel.x, self.vel.y)
        rotationMatrix = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        triangle       = [Vector.Vector(np.matmul(pair, rotationMatrix)).add(self.pos).pos for pair in triangle]
        pygame.draw.lines(frame, (0,0,0), True, triangle, 1)
        if debugging:
            pygame.draw.circle(frame, (255,0,0), map(int, self.pos.pos), int(2))
            pygame.draw.circle(frame, (150,150,150), map(int, self.Centre.pos), int(self.boidSize), 1)
            pygame.draw.circle(frame, (0,0,255), map(int, self.randomLocalTarget.pos), int(2))
            pygame.draw.line(frame, (0,0,255), self.Centre.pos, self.randomLocalTarget.pos, 1)
