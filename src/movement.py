#!/usr/bin/env python

#   movement.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of movement classes


from enum import Enum
from collections import defaultdict

class Direction(Enum):
    LEFT    = 1
    RIGHT   = 2
    UP      = 3
    DOWN    = 4

class Stationary(object):

    def move(self, currentXCoordinate, currentYCoordinate):
        return (currentXCoordinate, currentYCoordinate)


class KeyInput(object):

    def __init__(self, leftKey, rightKey, upKey, downKey):
        self.__curDirection = Direction.UP
        
        self.__leftKey      = leftKey
        self.__rightKey     = rightKey
        self.__upKey        = upKey
        self.__downKey      = downKey

        self.__directions   = defaultdict(
            lambda: KeyInput.stayInPlace,
            {
                self.__leftKey  : self.goLeft,
                self.__rightKey : self.goRight,
                self.__upKey    : self.goUp,
                self.__downKey  : self.goDown
            }
        )

    @staticmethod
    def stayInPlace(currentXCoordinate, currentYCoordinate):
        return (currentXCoordinate, currentYCoordinate)

    def goLeft(self, currentXCoordinate, currentYCoordinate):
        self.setCurrentDirection(Direction.LEFT)
        return (currentXCoordinate - 1, currentYCoordinate)

    def goRight(self, currentXCoordinate, currentYCoordinate):
        self.setCurrentDirection(Direction.RIGHT)
        return (currentXCoordinate + 1, currentYCoordinate)

    def goUp(self, currentXCoordinate, currentYCoordinate):
        self.setCurrentDirection(Direction.UP)
        return (currentXCoordinate, currentYCoordinate + 1)

    def goDown(self, currentXCoordinate, currentYCoordinate):
        self.setCurrentDirection(Direction.DOWN)
        return (currentXCoordinate, currentYCoordinate - 1)


    def setCurrentDirection(self, currentDirection):
        self.__curDirection = currentDirection


    def move(self, currentXPos, currentYPos, keyPressed):
        return self.__directions[keyPressed](currentXPos, currentYPos)