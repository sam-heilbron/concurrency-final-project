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
        positionMutex: Controls atomic access to centr and radius variables
        direction: The current direction of the circle
        directionMutex: Controls atomic access to direction variable
        directions: Map of directions to movement methods
    """

    def __init__(self, initialCenter, initialRadius = 1):
        self.__center           = initialCenter
        self.__radius           = initialRadius
        self.__positionMutex    = threading.Lock()
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
        with self.__positionMutex:
            center = self.__center
        return center

    def getRadius(self):
        with self.__positionMutex:
            radius = self.__radius
        return radius

    def getCurrentDirection(self):
        with self.__directionMutex:
            direction = self.__direction
        return direction


    ##########################   SETTERS   ##########################

    def setCurrentDirection(self, direction):
        with self.__directionMutex:
            self.__direction = direction

    def holdPosition(self):
        self.__positionMutex.acquire()
        return self.__center, self.__radius

    def releasePosition(self):
        self.__positionMutex.release()

    def move(self, game, user):
        self.__directions[self.getCurrentDirection()](game.getGameboard(), user)
        self._checkCollisions(game, user)

    def setCenter(self, newCenter):
        with self.__positionMutex:
            self.__center = newCenter

    def increaseRadiusByN(self, radiusIncrease):
        with self.__positionMutex:
            self.__radius += radiusIncrease

    def draw(self, color):  
        pygame.draw.circle(
            pygame.display.get_surface(), 
            color, 
            self.__center, 
            self.__radius)

    #########################   PROTECTED   #########################

    def _goLeft(self, gameboard, user):
        """ Move left """
        (col, row) = self.getCenter()

        if (col - (self.getRadius() + 1)) >= 0:
            gameboard.moveUser((col, row), (col - 1, row), user)

    def _goRight(self, gameboard, user):
        """ Move right """
        boardWidth = gameboard.getWidth()
        (col, row) = self.getCenter()

        if (col + (self.getRadius() + 1)) <= boardWidth:
            gameboard.moveUser((col, row), (col + 1, row), user)

    def _goUp(self, gameboard, user):
        """ Move up """
        (col, row) = self.getCenter()

        if (row - (self.getRadius() + 1)) >= 0:
            gameboard.moveUser((col, row), (col, row - 1), user)

    def _goDown(self, gameboard, user):
        """ Move down """
        boardHeight = gameboard.getHeight()
        (col, row) = self.getCenter()

        if (row + (self.getRadius() + 1)) <= boardHeight:
            gameboard.moveUser((col, row), (col, row + 1), user)

    def _stayInPlace(self, gameboard, user):
        """ Stay in place """
        return

    def _checkCollisions(self, game, user):
        """ Go through all pixels in player's radius and 
            check for a collision 
        """
        gameboard = game.getGameboard()
        (centerCol, centerRow) = self.getCenter()
        radius = self.getRadius()
        (width, height) = gameboard.getDimensions()
        for col in range(max(0, centerCol - radius), 
                         min(height - 1, centerCol + radius)):
            for row in range(max(0, centerRow - radius), 
                             min(width - 1, centerRow + radius)):
                if gameboard.getLockAtPosition((col,row)).locked() \
                        and (col, row) != (centerCol, centerRow):
                    print("Collision occured at (%s, %s)" % (col, row))
                    otherUserID = gameboard.getPlayerAtPosition((col, row))
                    self._handleCollisions(game, user, otherUserID)
                    return

    def _handleCollisions(self, game, currentUser, otherUserID):
        """ Kill the blob and increase the size of the player """
        try:
            otherUser = game.getUserFromID(otherUserID)
            if currentUser.getRadius() >= otherUser.getRadius():
                userToKill = otherUser
                userToLive = currentUser
            else:
                userToKill = currentUser
                userToLive = otherUser
        except:
            """ It's possible that a user will be killed right before
                it moves so the movement will still happen. This catches that
                scenario since either otherUser.getRadius() or 
                currentUser.getRadius() will fail since the user is None
            """
            return

        center, radius = userToKill.holdPosition()
            
        userToLive.increaseRadiusByN(radius)
        game.killUserWithID(userToKill.getID())

        userToKill.releasePosition()