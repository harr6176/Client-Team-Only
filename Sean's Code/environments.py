'''
Created on Nov 28, 2013

@author: Ranger
@modified: Sean
'''
import pygame
from math import pi, cos, sin

ETcolors = {'U': (150, 150, 150), 'F': (200, 0, 0), 'W': (50, 150, 50)}
STARTANGLE = pi / 2
UNITANGLE = pi / 8
LINECOLOR = (0, 200, 0)


class Environ():
    def __init__(self, parent, center, iradius, oradius, idnumber, type, size, race, creature, politics):
        self.parent = parent
        self.rect = pygame.Rect(center[0] - oradius, center[1] - oradius, oradius * 2, oradius * 2)
        self.id = idnumber
        self.type = type
        self.size = size
        self.race = race
        self.creature = creature
        self.politics = politics
        self.startangle = STARTANGLE + (self.id * UNITANGLE)
        self.endangle = self.startangle + UNITANGLE
        self.iradius = iradius
        self.oradius = oradius
        self.averadius = (iradius + oradius) / 2
        self.center = center
        self.getcolor(type)
        self.collision_points = []
        self.updatepoints()

    def __str__(self):
        return str(self.id)

    def getcolor(self, type):
        self.fillcolor = ETcolors[type]

    def shiftdown1(self):
        self.endangle = self.endangle + UNITANGLE
        self.startangle = self.startangle + UNITANGLE
        self.updatepoints()

    def shiftup1(self):
        self.endangle = self.endangle - UNITANGLE
        self.startangle = self.startangle - UNITANGLE
        self.updatepoints()

    def expand1(self):
        self.endangle = self.endangle + UNITANGLE
        self.updatepoints()
        return pygame.Rect(self.collision_points[-2], (1, 1))

    def contract1(self):
        self.endangle = self.endangle - UNITANGLE

    def updatepoints(self):
        self.collision_points = []
        angle = self.startangle
        while angle < self.endangle:
            angle = angle + UNITANGLE / 2
            self.collision_points.append((int(self.center[0] + (cos(angle) * self. averadius)), int(self.center[1] - (sin(angle) * self. averadius))))
            angle = angle + UNITANGLE / 2
        self.stacks = len(self.collision_points)

    def draw(self, surface):
        pygame.draw.line(surface, self.fillcolor, (self.center[0] + self.oradius * (cos(self.startangle)),
                                                  self.center[1] - self.oradius * (sin(self.startangle))),
                                                  (self.center[0] + self.iradius * (cos(self.startangle)),
                                                  self.center[1] - self.iradius * (sin(self.startangle))), 2)
        pygame.draw.line(surface, self.fillcolor, (self.center[0] + self.oradius * (cos(self.endangle)),
                                                   self.center[1] - self.oradius * (sin(self.endangle))),
                                                  (self.center[0] + self.iradius * (cos(self.endangle)),
                                                   self.center[1] - self.iradius * (sin(self.endangle))), 4)
        pygame.draw.arc(surface, self.fillcolor, pygame.Rect(self.rect.topleft, (2 * self.oradius, 2 * self.oradius)),
                                                            self.startangle, self.endangle + pi / 72, 3)
        pygame.draw.arc(surface, self.fillcolor, pygame.Rect(self.rect.topleft[0] + (self.oradius - self.iradius),
                                                             self.rect.topleft[1] + (self.oradius - self.iradius),
                                                             2 * self.iradius, 2 * self.iradius), self.startangle,
                                                             self.endangle + pi / 72, 3)
        for point in self.collision_points:
            pygame.draw.circle(surface, LINECOLOR, point, 5)


class EnvironBox():
    def __init__(self, parent, planetrect):
        self.parent = parent
        self.refresh = True
        self.planet = planetrect
        self.environ_list = []
        self.envarc = pygame.Rect(planetrect.topleft[0] - 75, planetrect.topleft[1] - 75, planetrect.width + 150, planetrect.height + 150)

    def addEnviron(self, idnumber, type, size, race, creature, politics):
        self.environ_list.append(Environ(self.parent, self.planet.center, self.planet.width / 2 + 50, self.planet.width / 2 + 150,
                                         idnumber, type, size, race, creature, politics))

    def update(self, unitlist):
        for environ in self.environ_list:
            environ.center = self.planet.center
            environ.rect.center = environ.center
            environ.updatepoints()
            if self.refresh:
                for i in range(1, environ.size):
                    environ.expand1()
                    for shift in self.environ_list[environ.id:]:
                        shift.shiftdown1()
        self.refresh = False

    def draw(self, surface):
        if self.parent.orient is "center":
            for environ in self.environ_list:
                environ.draw(surface)
