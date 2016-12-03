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

    def growByN(self, N):
        self.__radius += N

    def getCurrentDirection(self):
        with self.__directionMutex:
            direction = self.__direction
        return direction


    ##########################   SETTERS   ##########################

    def setCurrentDirection(self, direction):
        with self.__directionMutex:
            self.__direction = direction

    def move(self, game, userID):
        self.__directions[self.getCurrentDirection()](game.getGameboard(), userID)
        self._checkCollisions(game, userID)

    def draw(self, color):  
        pygame.draw.circle(
            pygame.display.get_surface(), 
            color, 
            self.__center, 
            self.__radius)

    #########################   PROTECTED   #########################

    def _goLeft(self, gameboard, userID):
        """ Move left """
        (col, row) = self.__center

        if (col - (self.__radius + 1)) >= 0:
            gameboard.pullUserFromBoard(self.__center)
            self.__center = (col - 1, row)
            gameboard.placeUserOnBoard(self.__center, userID)

    def _goRight(self, gameboard, userID):
        """ Move right """
        boardWidth = gameboard.getWidth()
        (col, row) = self.__center

        if (col + (self.__radius + 1)) <= boardWidth:
            gameboard.pullUserFromBoard(self.__center)
            self.__center = (col + 1, row)
            gameboard.placeUserOnBoard(self.__center, userID)

    def _goUp(self, gameboard, userID):
        """ Move up """
        (col, row) = self.__center

        if (row - (self.__radius + 1)) >= 0:
            gameboard.pullUserFromBoard(self.__center)
            self.__center = (col, row - 1)
            gameboard.placeUserOnBoard(self.__center, userID)

    def _goDown(self, gameboard, userID):
        """ Move down """
        boardHeight = gameboard.getHeight()
        (col, row) = self.__center

        if (row + (self.__radius + 1)) <= boardHeight:
            gameboard.pullUserFromBoard(self.__center)
            self.__center = (col, row + 1)
            gameboard.placeUserOnBoard(self.__center, userID)

    def _stayInPlace(self, gameboard, userID):
        """ Stay in place """
        return

##
## We can change this to check only BORDER elements
## This is because a piece only moves 1 space (no matter how quickly)
## So it can only change a few positions
## iF each user checks then we don't have to worry about faster users
##  moving multiple times for each move by a slower user
    def _checkCollisions(self, game, userID):
        """ Go through all pixels in player's radius and check for a collision """
        gameboard = game.getGameboard()
        (centerCol, centerRow) = self.__center
        (width, height) = gameboard.getDimensions()
        for col in range(max(0, centerCol - self.__radius), 
                         min(height, centerCol + self.__radius)):
            for row in range(max(0, centerRow - self.__radius), 
                             min(width, centerRow + self.__radius)):
                if gameboard.getLockAtPosition((col,row)).locked() \
                        and (col, row) != self.__center:
                    print("Collision occured at (%s, %s)" % (col, row))
                    blobID = gameboard.getPlayerAtPosition((col, row))
                    self._handleCollisions(game, userID, blobID)
                    return

    def _handleCollisions(self, game, currentUserID, otherUserID):
        """ Kill the blob and increase the size of the player """
        """ TODO: probably need to add logic to handle different sized
            users (if a small users collides into a larger user, the larger 
            should still eat the smaller)"""
        otherUser = game.getUserFromID(otherUserID)
        currentUser = game.getUserFromID(currentUserID)

        if currentUser.getRadius() >= otherUser.getRadius():
            userToKill = otherUser
        else:
            userToKill = currentUser

        game.pullUserFromBoard(userToKill.getCenter())
        game.killUserWithID(userToKill.getID()) 
        self.growByN(userToKill.getRadius())