#!/usr/bin/env python

#   decisions.py
#
#   Sam Heilbron
#   Last Updated: November 16, 2016
#
#   List of decision classes
##
##  super(ClassName, self).__init__()
##

from collections import defaultdict

class Basic(object):
    """ Base class for all decision classes """

    def continueDirection(self, currentPosition):
        currentPosition.continueDirection();

    def goLeft(self, currentPosition):
        currentPosition.goLeft()

    def goRight(self, currentPosition):
        currentPosition.goRight()

    def goUp(self, currentPosition):
        currentPosition.goUp()

    def goDown(self, currentPosition):
        currentPosition.goDown()



class Stationary(Basic):
    """ Decision class for a Stationary player """

    def move(self, currentPosition):
        currentPosition.stayInPlace()



class KeyInput(Basic):
    """ Decision class for keyboard inputs

    Attributes:
        directions: Map of key inputs to methods
    """

    def __init__(self, leftKey, rightKey, upKey, downKey):
        self.__directions   = defaultdict(
            lambda: self.continueDirection,
            {
                leftKey  : self.goLeft,
                rightKey : self.goRight,
                upKey    : self.goUp,
                downKey  : self.goDown
            }
        )

    def move(self, currentPosition, keyPressed):
        return self.__directions[keyPressed](currentPosition)


class AIInput(Basic):
    """ Decision class for AI input (auto-move) """

    def move(self, currentPosition):
        print("ai move")