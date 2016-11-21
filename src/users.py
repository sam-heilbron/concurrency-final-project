#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of user classes

import threading
from decisions import Stationary, KeyInput
from movements import Sphere


class Blob(object):
    """A blob. Base class for all users.

    Attributes:
        decision: The class defining IN WHICH DIRECTION a blob moves
        movement: The class defining HOW a blob moves

        isAlive: Semaphore representing life of blob
        lock: Mutex to force atomic access
    """

    def __init__(   self,
                    decisionClass,
                    movementClass):
        self.__decision = decisionClass
        self.__movement = movementClass

        self.__isAlive  = threading.Semaphore(1)
        self.__lock     = threading.Lock()

    def getSize(self):
        return self.__movement.getSize()

    def getPos(self):
        return self.__movement.getPos()

    def getMovement(self):
        return self.__movement

    def getDecision(self):
        return self.__decision

    def setPos(self, newPos):
        self.__pos = newPos

    def expose(self):
        print("Size: %s \nPos: %s \nMovement: %s\n" % \
         (self.getSize(), self.getPos(), self.getMovement()))


class Food(Blob):
    """A Food item.

    Attributes:
        pos: A tuple representing the (x,y) coordinates.
        size: The size of the blob.
        movement: movement is Stationary.
        isAlive: Semaphore representing life of the food.
        lock: Mutex to force atomic access.
    """

    def __init__(self, initialPositionList):
        """ Create a Food item """
        Blob.__init__(  self, 
                        decisionClass   = Stationary(),
                        movementClass   = Sphere(initialPositionList))


class Human(Blob):
    """A Human player.

    Attributes:
        pos: A tuple representing the (x,y) coordinates.
        size: The size of the human.
        movement: movement is Human.
        isAlive: Semaphore representing life of the human.
        lock: Mutex to force atomic access.
    """

    def __init__(self, ID, initialPositionList):
        """ Create a Human player """
        Blob.__init__(  self, 
                        decisionClass   = KeyInput(
                                            leftKey  = "a",
                                            rightKey = "d",
                                            upKey    = "w",
                                            downKey  = "s"),
                        movementClass   = Sphere(
                                            initialPositionList))
        self.__id = ID

    def move(self, keyPressed):
        """@TODO: update how to set and change user position
        """
        self.getDecision().move(self.getMovement(), keyPressed)
