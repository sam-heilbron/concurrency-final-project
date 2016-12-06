#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 30, 2016
#
#   List of user classes

import threading
from decisions import Stationary, KeyInput, AIRandom
from movements import Circle_
from enums import InitialUserRadius, Color, Timeout

###############################################################################
##
##                              Blob class
##
###############################################################################
class Blob(object):
    """A blob. Base class for all users.

    Attributes:
        id: The unique tag associated with each blob
        color: The color of the blob (drawn on screen)
        decision: The class defining IN WHICH DIRECTION a blob moves
        movement: The class defining the shape and movement of a blob
        isDead: Event representing life of blob. Triggered on death.
    """

    def __init__(   self,
                    id_,
                    color,
                    decisionClass,
                    movementClass):
        self.__id       = id_
        self.__color    = color
        self.__decision = decisionClass
        self.__movement = movementClass
        self.__isDead   = threading.Event()

    ##########################   GETTERS   ##########################

    def getMovement(self):
        return self.__movement

    def getDecision(self):
        return self.__decision

    def getID(self):
        return self.__id

    def isDead(self):
        return self.__isDead

    def getCenter(self):
        return self.__movement.getCenter()

    def getRadius(self):
        return self.__movement.getRadius()

    ##########################   SETTERS   ##########################

    def setCenter(self, newCenter):
        self.__movement.setCenter(newCenter)

    def increaseRadiusByN(self, radiusIncrease):
        self.__movement.increaseRadiusByN(radiusIncrease)

    def holdPosition(self):
        return self.__movement.holdPosition()

    def releasePosition(self):
        self.__movement.releasePosition()
    
    def draw(self):
        self.__movement.draw(self.__color)

    def quit(self):
        print("Prepare to kill user: %s" % self.__id)
        self.__isDead.set()

    #########################   PROTECTED   #########################

    def _getMovementInterval(self):
        """ Timeout between moves """
        return Timeout.MOVEMENT * (self.__movement.getRadius() / 4)

    def _moveAtInterval(self, game):
        """ Move a food item based on decision class """
        while not self.__isDead.wait(timeout=self._getMovementInterval()):
            self.__movement.move(game, self)

        game.pullUserFromBoard(self.getCenter())

    def _waitForDecision(self, gameOverFlag):
        self.__decision.waitForDecision(self, gameOverFlag)


###############################################################################
##
##                              Food class
##
###############################################################################
class Food(Blob):
    """A Food item.

    Attributes:
        id: The unique tag associated with each food (food_{count})
        color: Black
        decision: Stationary
        movement: Circle_
        isDead: Event representing life of food. Triggered when eaten.
    """

    def __init__(self, id_, initialCenter):
        """ Create a Food item """
        Blob.__init__(  self, 
                        id_             = id_,
                        color           = Color.BLACK,
                        decisionClass   = Stationary(),
                        movementClass   = Circle_(
                                            initialCenter, 
                                            InitialUserRadius.FOOD))

    def start(self, game):
        """ Spin up threads for making decisions and moving """
        decisionThread = threading.Thread(
                            target = self._waitForDecision,
                            args = [game.getGameOverFlag()])
        movementThread = threading.Thread(
                            target = self._moveAtInterval,
                            args = [game])
        decisionThread.start()
        movementThread.start()


###############################################################################
##
##                              Human class
##
###############################################################################
class Human(Blob):
    """A Human player.

    Attributes:
        id: The unique tag associated with human (human)
        color: Red
        decision: Either KeyInput or MouseInput
        movement: Circle_
        isDead: Event representing life of human. Triggered when eaten.
    """

    def __init__(self, initialCenter, decisionClass = KeyInput()):
        """ Create a Human player """
        Blob.__init__(  self, 
                        id_             = "human",
                        color           = Color.RED,
                        decisionClass   = decisionClass,
                        movementClass   = Circle_(
                                            initialCenter, 
                                            InitialUserRadius.HUMAN))

    def start(self, game):
        """ Spin up a thread for moving """
        movementThread = threading.Thread(
                            target = self._moveAtInterval,
                            args = [game])
        movementThread.start()

        """ Pygame requires keyboard events to run in the main thread """
        self._waitForDecision(game.getGameOverFlag())


###############################################################################
##
##                              AI class
##
###############################################################################
class AI(Blob):
    """An AI item.

    Attributes:
        id: The unique tag associated with each ai (ai_{count})
        color: Black
        decision: AIInput
        movement: Circle_
        isDead: Event representing life of AI. Triggered when eaten.
    """

    def __init__(self, id_, initialCenter):
        """ Create an AI item """
        Blob.__init__(  self, 
                        id_             = id_,
                        color           = Color.GREEN,
                        decisionClass   = AIRandom(),
                        movementClass   = Circle_(
                                            initialCenter, 
                                            InitialUserRadius.AI))

    def start(self, game):
        """ Spin up threads for making decisions and moving """
        decisionThread = threading.Thread(
                            target = self._waitForDecision,
                            args = [game.getGameOverFlag()])
        movementThread = threading.Thread(
                            target = self._moveAtInterval,
                            args = [game])
        decisionThread.start()
        movementThread.start()