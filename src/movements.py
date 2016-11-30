#!/usr/bin/env python

#   movements.py
#
#   Sam Heilbron
#   Last Updated: November 21, 2016
#
#   List of movement classes

from enums import Direction, Color
import threading
import pygame

class _Circle(object):
    """A Circle. Class for circle positions.

    Attributes:
        pixels: List of pixel coordinates.
        size: The size of the sphere.
    """

    def __init__(self, initialCenter, initialRadius = 1):
        self.__center           = initialCenter
        self.__radius           = initialRadius
        self.__direction        = Direction.STAY
        self.__directionMutex   = threading.Lock()

        self.__directions       = dict(
            {
                Direction.LEFT  : self.goLeft,
                Direction.RIGHT : self.goRight,
                Direction.UP    : self.goUp,
                Direction.DOWN  : self.goDown,
                Direction.STAY  : self.stayInPlace
            })


    ##########################   GETTERS   ##########################

    def getCenter(self):
        return self.__center

    def getRadius(self):
        return self.__radius

    def getCurrentDirection(self):
        with self.__directionMutex:
            direction = self.__direction
        return direction


    ##########################   SETTERS   ##########################

    def setCurrentDirection(self, direction):
        with self.__directionMutex:
            self.__direction = direction


##
##  Change how the movemnt is handled
##  Shouldn't be able to move if ANY of the pixels will go 
##  less than 0 or greater than max
##
    def move(self, gameboard):
        self.__directions[self.getCurrentDirection()](gameboard)

    def draw(self, color):  
        pygame.draw.circle(
            pygame.display.get_surface(), 
            color, 
            self.__center, 
            self.__radius)

    def goLeft(self, gameboard):
        """ Move left """
        (col, row) = self.__center
        if (col - (self.__radius + 1)) >= 0:
            self.__center = (col - 1, row)

    def goRight(self, gameboard):
        """ Move right """
        boardWidth = gameboard.getWidth()
        (col, row) = self.__center
        if (col + (self.__radius + 1)) <= boardWidth:
            self.__center = (col + 1, row)

    def goUp(self, gameboard):
        """ Move up """
        (col, row) = self.__center
        if (row - (self.__radius + 1)) >= 0:
            self.__center = (col, row - 1)

    def goDown(self, gameboard):
        """ Move down """
        boardHeight = gameboard.getHeight()
        (col, row) = self.__center
        if (row + (self.__radius + 1)) <= boardHeight:
            self.__center = (col, row + 1)

    def stayInPlace(self, gameboard):
        """ Stay in place """
        return


###
###self.__pixels =[(max(0,row-1),col) for (row,col) in self.__pixels]
###


