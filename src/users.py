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
from enums import InitialUserRadius, Color


class Blob(object):
    """A blob. Base class for all users.

    Attributes:
        decision: The class defining IN WHICH DIRECTION a blob moves
        movement: The class defining HOW a blob moves
        color: The color of the blob (drawn on screen)
        isDead: Semaphore representing life of blob
    """

    def __init__(   self,
                    color,
                    decisionClass,
                    movementClass):
        self.__decision = decisionClass
        self.__movement = movementClass
        self.__color    = color
        self.__isDead   = threading.Event()

    def getMovement(self):
        return self.__movement

    def getDecision(self):
        return self.__decision

    def draw(self):
        self.__movement.draw(self.__color)

    def isDead(self):
        return self.__isDead

    def quit(self):
        self.__isDead.set()

    def start(self, gameboard, gameOverFlag):
        """ Spin up threads for making decisions and moving """
        decisionThread = threading.Thread(
                            target = self.__decision.waitForDecision,
                            args = [self.__movement, gameOverFlag])
        movementThread = threading.Thread(
                            target = self.moveAtInterval,
                            args = [gameboard])
        decisionThread.start()
        movementThread.start()

    def moveAtInterval(self, gameboard):
        """ Move a food item based on decision class """
        while not self.__isDead.wait(timeout=1):
            self.__movement.move(gameboard)


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
                        color           = Color.BLACK,
                        decisionClass   = Stationary(),
                        movementClass   = _Circle(
                                            initialCenter, 
                                            InitialUserRadius.FOOD))


class Human(Blob):
    """A Human player.

    Attributes:
        decision: KeyInput class
        movement: Sphere class

        isAlive: Semaphore representing life of blob
        lock: Mutex to force atomic access
    """

    def __init__(self, initialCenter, inputClass = KeyInput()):
        """ Create a Human player """
        Blob.__init__(  self, 
                        color           = Color.RED,
                        decisionClass   = inputClass,
                        movementClass   = _Circle(
                                            initialCenter, 
                                            InitialUserRadius.HUMAN))

    def start(self, gameboard, gameOverFlag):
        """ Spin up a thread for moving """
        movementThread = threading.Thread(
                            target = self.moveAtInterval,
                            args = [gameboard])
        movementThread.start()

        """ Any user requiring IO should run the IO in the main thread """
        self.getDecision().waitForDecision(
                            self.getMovement(), gameOverFlag)


    def moveAtInterval(self, gameboard):
        """ Move a Human player """
        """ @TODO: make tiemout interval a variable """
        while not self.isDead().wait(timeout=.01):
            self.getMovement().move(gameboard)
            

