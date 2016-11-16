#!/usr/bin/env python

#   decisions.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of decision classes


from collections import defaultdict

class Basic(object):
    def __init__(self):
        self.__name = "Basic"

    def continueDirection(currentPosition):
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

    def __init__(self):
        Basic.__init__()

    def move(self, currentPosition):
        currentPosition.stayInPlace()


class KeyInput(Basic):

    def __init__(self, leftKey, rightKey, upKey, downKey):
        Basic.__init__()

        self.__leftKey      = leftKey
        self.__rightKey     = rightKey
        self.__upKey        = upKey
        self.__downKey      = downKey

        self.__directions   = defaultdict(
            lambda: self.continueDirection,
            {
                self.__leftKey  : self.goLeft,
                self.__rightKey : self.goRight,
                self.__upKey    : self.goUp,
                self.__downKey  : self.goDown
            }
        )

    def move(self, currentPosition, keyPressed):
        return self.__directions[keyPressed](currentPosition)


class AIInput(Basic):

    def __init__(self):
        Basic.__init__()

    def move(self, currentPosition):
        print("ai move")