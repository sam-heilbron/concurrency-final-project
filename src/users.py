#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 21, 2016
#
#   List of user classes

import threading
from decisions import Stationary, KeyInput
from movements import _Circle
from enums import InitialUserRadius


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

        self.__color    = Color.BLACK
        self.__isAlive  = threading.Semaphore(1) ### Not used yet. @TODO
        self.__lock     = threading.Lock()

    def getSize(self):
        return self.__movement.getSize()

    def getPos(self):
        return self.__movement.getPos()

    def getMovement(self):
        return self.__movement

    def getDecision(self):
        return self.__decision

    def draw(self):
        self.__movement.draw(self.__color)

    def expose(self):
        print("Size: %s \nPos: %s \nMovement: %s\n" % \
         (self.getSize(), self.getPos(), self.getMovement()))


class Food(Blob):
    """A Food item.

    Attributes:
        decision: Stationary class
        movement: Sphere class

        isAlive: Semaphore representing life of blob
        lock: Mutex to force atomic access
    """

    def __init__(self, initialCenter):
        """ Create a Food item """
        Blob.__init__(  self, 
                        decisionClass   = Stationary(),
                        movementClass   = _Circle(
                                            initialCenter, 
                                            InitialUserRadius.FOOD))

    def start(self, gameboard):
        """ Spin up threads for making decisions and moving """
        decisionThread = threading.Thread(
                            target = self.getDecision().waitForDecision,
                            args = [self.getMovement()])
        movementThread = threading.Thread(
                            target = self.moveAtInterval,
                            args = [gameboard])
        decisionThread.start()
        movementThread.start()


    def moveAtInterval(self, gameboard):
        """ Move a food item based on decision class (Stationary) """
        self.getMovement().move()


class Human(Blob):
    """A Human player.

    Attributes:
        decision: KeyInput class
        movement: Sphere class
        id: The ID of the user

        isAlive: Semaphore representing life of blob
        lock: Mutex to force atomic access
    """

    def __init__(self, ID, initialCenter, inputClass = KeyInput()):
        """ Create a Human player """
        Blob.__init__(  self, 
                        decisionClass   = inputClass,
                        movementClass   = _Circle(
                                            initialCenter, 
                                            InitialUserRadius.HUMAN))
        self.__id = ID

    def start(self, gameboard):
        """ Spin up a thread for moving """
        movementThread = threading.Thread(
                            target = self.moveAtInterval,
                            args = [gameboard])
        movementThread.start()

        """ Any user requiring IO should run the IO in the main thread """
        self.getDecision().waitForDecision(self.getMovement())


    def moveAtInterval(self, gameboard):
        """ Move a Human player """

        exit_flag = threading.Event()
        while not exit_flag.wait(timeout=.01):
            self.getMovement().move(gameboard)
            
            gameboard.updateBackground()
            self.draw()
            gameboard.updateDisplay()
