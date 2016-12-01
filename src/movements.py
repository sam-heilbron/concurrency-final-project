#!/usr/bin/env python

#   movements.py
#
#   Sam Heilbron
#   Last Updated: November 30, 2016
#
#   List of movement classes

from enums import Direction, Color
import threading
import pygame

class Circle_(object):
    """A Circle. Class circular blobs.

    Attributes:
        center: The center of the circle.
        radius: The radius of the circle.
        direction: The current direction of the circle
        directionMutex: Controls atomic access to direction variable
        directions: Map of directions to movement methods
    """

    def __init__(self, initialCenter, initialRadius = 1):
        self.__center           = initialCenter
        self.__radius           = initialRadius
        self.__direction        = Direction.STAY
        self.__directionMutex   = threading.Lock()

        self.__directions       = dict(
            {
                Direction.LEFT  : self._goLeft,
                Direction.RIGHT : self._goRight,
                Direction.UP    : self._goUp,
                Direction.DOWN  : self._goDown,
                Direction.STAY  : self._stayInPlace
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

    def move(self, game):
        self.__directions[self.getCurrentDirection()](game.getGameboard())
        self._checkCollisions(game)

    def draw(self, color):  
        pygame.draw.circle(
            pygame.display.get_surface(), 
            color, 
            self.__center, 
            self.__radius)

    #########################   PROTECTED   #########################

    def _goLeft(self, gameboard):
        """ Move left """
        (col, row) = self.__center

        if (col - (self.__radius + 1)) >= 0:
            gameboard.getLockAtCenter(self.__center).release()
            self.__center = (col - 1, row)
            gameboard.getLockAtCenter(self.__center).acquire()

    def _goRight(self, gameboard):
        """ Move right """
        boardWidth = gameboard.getWidth()
        (col, row) = self.__center

        if (col + (self.__radius + 1)) <= boardWidth:
            gameboard.getLockAtCenter(self.__center).release()
            self.__center = (col + 1, row)
            gameboard.getLockAtCenter(self.__center).acquire()

    def _goUp(self, gameboard):
        """ Move up """
        (col, row) = self.__center

        if (row - (self.__radius + 1)) >= 0:
            gameboard.getLockAtCenter(self.__center).release()
            self.__center = (col, row - 1)
            gameboard.getLockAtCenter(self.__center).acquire()

    def _goDown(self, gameboard):
        """ Move down """
        boardHeight = gameboard.getHeight()
        (col, row) = self.__center

        if (row + (self.__radius + 1)) <= boardHeight:
            gameboard.getLockAtCenter(self.__center).release()
            self.__center = (col, row + 1)
            gameboard.getLockAtCenter(self.__center).acquire()

    def _stayInPlace(self, gameboard):
        """ Stay in place """
        return

##
## We can change this to check only BORDER elements
## This is because a piece only moves 1 space (no matter how quickly)
## So it can only change a few positions
## iF each user checks then we don't have to worry about faster users
##  moving multiple times for each move by a slower user
    def _checkCollisions(self, game):
        """ Go through all pixels in player's radius and check for a collision """
        gameboard = game.getGameboard()
        (centerCol, centerRow) = self.__center
        (width, height) = gameboard.getDimensions()
        for col in range(centerCol - self.__radius, centerCol + self.__radius):
            if col < 0 or col > height:
                continue
            for row in range(centerRow - self.__radius, centerRow + self.__radius):
                if row < 0 or row > width:
                    continue
                elif gameboard.getLockAtCenter((col,row)).locked() and (col, row) != self.__center:
                    print("Collision occured at (%s, %s)" % (col, row))
                    """ 
                    Here were would kill a user BUT we need some way of figuring out the
                    userID of the user holding the lock
                    """
                    blobID = gameboard.getPlayerAtPosition((col, row))
                    self._handleCollisions(game, blobID)
                    return

    def _handleCollisions(self, game, blobID):
        """ Kill the blob and increase the size of the player """
        """ TODO: probably need to add logic to handle different sized
            users (if a small users collides into a larger user, the larger 
            should still eat the smaller)"""
        blob = game.getUserFromID(blobID)
        game.getGameboard().getLockAtCenter(blob.getMovement().__center).release()
        game.killUserWithID(blobID) 
        self.__radius = self.__radius + blob.getMovement().__radius