#!/usr/bin/env python

#   movements.py
#
#   Sam Heilbron
#   Last Updated: November 16, 2016
#
#   List of movement classes

from enum import Enum

class Direction(Enum):
    """ Enum representing possible directions """
    LEFT    = 1
    RIGHT   = 2
    UP      = 3
    DOWN    = 4
    STAY    = 5


class Sphere(object):
    """A Sphere. Class for circle positions.

    Attributes:
        pixels: List of pixel coordinates.
        size: The size of the sphere.
    """

    def __init__(self, initialPositionList):
        self.__pixels   = initialPositionList
        self.__size     = len(initialPositionList) ## length of list
        self.__direction = Direction.UP

        self.__directions   = dict(
            {
                Direction.LEFT  : self.goLeft,
                Direction.RIGHT : self.goRight,
                Direction.UP    : self.goUp,
                Direction.DOWN  : self.goDown,
                Direction.STAY  : self.stayInPlace
            })


    """ GETTERS """
    def getSize(self):
        return self.__size

    def getPos(self):
        return self.__pixels

    def getCurrentDirection(self):
        return self.__direction

    """ SETTERS """
    def setCurrentDirection(self, direction):
        self.__direction = direction


##
##  Change how the movemnt is handled
##  Shouldn't be able to move if ANY of the pixels will go 
##  less than 0 or greater than max
##

    def goLeft(self):
        """ Move left """
        self.setCurrentDirection(Direction.LEFT)
        self.__pixels =[(row,max(0,col-1)) for (row,col) in self.__pixels]
        print("Sphere: %s" % self.__direction)

    def goRight(self):
        """ Move right """
        self.setCurrentDirection(Direction.RIGHT)
        print("Sphere: %s" % self.__direction)

    def goUp(self):
        """ Move up """
        self.setCurrentDirection(Direction.UP)
        print("Sphere: %s" % self.__direction)

    def goDown(self):
        """ Move down """
        self.setCurrentDirection(Direction.DOWN)
        print("Sphere: %s" % self.__direction)

    def continueDirection(self):
        """ Continue in the current direction """
        self.__directions[self.getCurrentDirection()]()

    def stayInPlace(self):
        """ Stay in place """
        self.setCurrentDirection(Direction.STAY)
        print("Sphere: %s" % self.__direction)


