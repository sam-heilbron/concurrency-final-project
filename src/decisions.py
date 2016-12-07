#!/usr/bin/env python

#   decisions.py
#
#   Sam Heilbron
#   Rachel Marison
#   Last Updated: December 7, 2016
#
#   List of decision classes
#

from collections import defaultdict
from enums import Direction, Timeout
import pygame
from random import randint


###############################################################################
##
##                              Basic class
##
###############################################################################
class Basic(object):
    """ Base class for all decision classes """

    def turnLeft(self, movement):
        movement.setCurrentDirection(Direction.LEFT)

    def turnRight(self, movement):
        movement.setCurrentDirection(Direction.RIGHT)

    def turnUp(self, movement):
        movement.setCurrentDirection(Direction.UP)

    def turnDown(self, movement):
        movement.setCurrentDirection(Direction.DOWN)

    def noTurn(self, movement):
        """ No turn associated with that decision """
        return

    def quitGame(self, gameOverFlag):
        gameOverFlag.set()


###############################################################################
##
##                              Stationary class
##
###############################################################################
class Stationary(Basic):
    """ Decision class for a Stationary player """

    ## Theoretically you could just return, but it's more realistic to 
    ## have a thread alive as long as the user is alive
    def waitForDecision(self, user, game):
        """ DEFAULT: Wait for user to die """
        user.isDead().wait()


###############################################################################
##
##                              KeyInput class
##
###############################################################################
class KeyInput(Basic):
    """ Decision class for keyboard inputs

    Attributes:
        directions: Map of key inputs to methods
    """

    def __init__(   self, 
                    upKey       = pygame.K_UP, 
                    downKey     = pygame.K_DOWN,
                    leftKey     = pygame.K_LEFT, 
                    rightKey    = pygame.K_RIGHT):

        self.__directions   = defaultdict(
            lambda: self.noTurn,
            {
                leftKey  : self.turnLeft,
                rightKey : self.turnRight,
                upKey    : self.turnUp,
                downKey  : self.turnDown
            }
        )

    def waitForDecision(self, user, game):
        gameOverFlag = game.getGameOverFlag()
        while not user.isDead().wait(timeout = Timeout.DECISION):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitGame(gameOverFlag)
                    else:
                        self.turn(user.getMovement(), event.key)
                elif event.type == pygame.QUIT:
                    self.quitGame(gameOverFlag)

        self.quitGame(gameOverFlag)    

    def turn(self, movement, keyPressed):
        return self.__directions[keyPressed](movement)


###############################################################################
##
##                              MouseInput class
##
###############################################################################
class MouseInput(Basic):
    """ Decision class for mouse input

     Attributes:
        directions: Map of tuples to decision methods
            (colIsLarger, isPositive) is the pattern
                Ex: Turn left if the column difference is larger 
                    AND its negative
    """

    def __init__(self):
        self.__directions   = defaultdict(
            lambda: self.noTurn,
            {
                (1, 0)  : self.turnLeft,
                (1, 1)  : self.turnRight,
                (0, 0)  : self.turnUp,
                (0, 1)  : self.turnDown
            }
        )

    def waitForDecision(self, user, game):
        gameOverFlag = game.getGameOverFlag()
        while not user.isDead().wait(timeout = Timeout.DECISION):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.turn(user.getMovement(), event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitGame(gameOverFlag)
                elif event.type == pygame.QUIT:
                    self.quitGame(gameOverFlag)

        self.quitGame(gameOverFlag)
     

    def turn(self, movement, mousePosition):
        (col, row) = movement.getCenter()
        (mouseCol, mouseRow) = mousePosition

        colDifference = mouseCol - col
        rowDifference = mouseRow - row

        colDifferenceLarger = (abs(colDifference)) > (abs(rowDifference))
        if colDifferenceLarger:
            return self.__directions[(1, colDifference > 0)](movement)

        return self.__directions[(0, rowDifference > 0)](movement)


###############################################################################
##
##                              AIInput class
##
###############################################################################
class AIRandom(Basic):
    """ Decision class for AI input (auto-move)""" 

    def __init__(self):
        self.__directions   = defaultdict(
            lambda: self.noTurn,
            {
                (1, 0)  : self.turnLeft,
                (1, 1)  : self.turnRight,
                (0, 0)  : self.turnUp,
                (0, 1)  : self.turnDown
            }
        )

    def waitForDecision(self, user, game):
        clock = pygame.time.Clock()
        while not user.isDead().wait(timeout = Timeout.SLOWDECISION):
            self.turn(user.getMovement(), game)    

    def turn(self, movement, game):
        (col, row) = movement.getCenter()
        (humanCol, humanRow) = game.getHumanUser().getCenter() 

        colDifference = humanCol - col
        rowDifference = humanRow - row

        colDifferenceLarger = (abs(colDifference)) > (abs(rowDifference))
        if colDifferenceLarger:
            return self.__directions[(1, colDifference > 0)](movement)

        return self.__directions[(0, rowDifference > 0)](movement)
