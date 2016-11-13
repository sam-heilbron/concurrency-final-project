#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of user classes

import threading
from movement import Stationary, Human

## Represents the canvas that a group of artists could work on
class SyncBlob(object):
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

    def expose(self):
        print("Size: %s \nPos: %s \nMovement: %s\n" % \
         (self.__size, self.__pos, self.__movement))


class SyncFood(SyncBlob):

    def __init__(self, initialPos):
        SyncBlob.__init__(  self, 
                            initialPos = initialPos)


class SyncHuman(SyncBlob):

    def __init__(self, initialPos):
        SyncBlob.__init__(  self, 
                            initialPos      = initialPos, 
                            initialSize     = 4,
                            movementClass   = Human,
                            canGrow         = True)
