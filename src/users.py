#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of user classes

import threading
from movement import Stationary, KeyInput


class Blob(object):

    """A blob. Base class for all users.

    Attributes:
        pos: A tuple representing the (x,y) coordinates.
        size: The size of the blob.
        movement: The class defining how a blob moves.
        canGrow: Whether or not a blob can grow.
        isAlive: Semaphore representing life of blob.
        lock: Mutex to force atomic access.
    """

    ###@TODO: Add list of pixels that user "owns"
    def __init__(   self, 
                    initialPos,
                    initialSize     = 1, 
                    movementClass   = Stationary, 
                    canGrow         = False):
        self.__pos      = initialPos
        self.__size     = initialSize
        self.__movement = movementClass

        self.__canGrow  = canGrow
        self.__isAlive  = threading.Semaphore(1)
        self.__lock     = threading.Lock()

    def getSize(self):
        return self.__size

    def getPos(self):
        return self.__pos

    def getMovement(self):
        return self.__movement

    def getCanGrow(self):
        return self.__canGrow

    def setPos(self, newPos):
        self.__pos = newPos

    def expose(self):
        print("Size: %s \nPos: %s \nMovement: %s\n" % \
         (self.__size, self.__pos, self.__movement))


class Food(Blob):
    """A Food item.

    Attributes:
        pos: A tuple representing the (x,y) coordinates.
        size: The size of the blob.
        movement: movement is Stationary.
        canGrow: Food CANNOT grow.
        isAlive: Semaphore representing life of the food.
        lock: Mutex to force atomic access.
    """

    def __init__(self, initialPos):
        """ Create a Food item """
        Blob.__init__(  self, 
                        initialPos = initialPos)


class Human(Blob):
    """A Human player.

    Attributes:
        pos: A tuple representing the (x,y) coordinates.
        size: The size of the human.
        movement: movement is Human.
        canGrow: Human CAN grow.
        isAlive: Semaphore representing life of the human.
        lock: Mutex to force atomic access.
    """

    def __init__(self, initialPos, movementClass):
        """ Create a Human player """
        Blob.__init__(  self, 
                        initialPos      = initialPos, 
                        initialSize     = 4,
                        movementClass   = movementClass,
                        canGrow         = True)

    def move(self, keyPressed):
        self.setPos(
            self.getMovement().move(*self.getPos(), keyPressed))
        print(str(self.getPos()))
