#!/usr/bin/env python

#   movements.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of movement classes

from enum import Enum

class Direction(Enum):
    LEFT    = 1
    RIGHT   = 2
    UP      = 3
    DOWN    = 4


class Sphere(object):

    """A Sphere. Class for circle positions.

    Attributes:
        pixels: List of pixel coordinates.
        size: The size of the sphere.
    """

    ###@TODO: Add list of pixels that user "owns"
    def __init__(self):
        self.__pixels   = [initialPos]
        self.__size     = 1
        self.__direction = Direction.UP


    def getSize(self):
        return self.__size

    def getPos(self):
        return self.__pixels


    def continueDirection(self):
        print("Sphere: " % self.__direction)

    def goLeft(self):
        self.setCurrentDirection(Direction.LEFT)
        print("Sphere: " % self.__direction)

    def goRight(self):
        self.setCurrentDirection(Direction.RIGHT)
        print("Sphere: " % self.__direction)

    def goUp(self):
        self.setCurrentDirection(Direction.UP)
        print("Sphere: " % self.__direction)

    def goDown(self):
        self.setCurrentDirection(Direction.DOWN)
        print("Sphere: " % self.__direction)

    def stayInPlace(self):
        return

    def setCurrentDirection(direction):
        self.__direction = direction
