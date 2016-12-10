#!/usr/bin/env python

#   decisions.py
#
#   Sam Heilbron, Rachel Marison
#   Last Updated: December 9, 2016
#
#   List of decision classes:
#       Stationary
#       KeyInput
#       MouseInput
#       AISmartInput
#       AIRandomInput

import pygame
from collections import defaultdict
from random import randint
from enums import Direction, Timeout


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

    def waitForDecision(self, user, game):
        """ DEFAULT: Wait for user to die 
            Theoretically you could just return, but it's more realistic to 
            have a thread alive as long as the user is alive since the user
            is actively making a decision (to stay stationary)
        """
        user.isDead().wait()


    #------------------------- END PAGE 1 --------------------------#
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
        """ Handle keyboard presses """
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
        """ Turn the user depending on the pressed key """
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
                Ex: (1,0) results in a left turn because that means that 
                the column difference is larger than the row difference and
                the difference is negative. Therefore the mouse is to the left
    """


    #------------------------- END PAGE 2 --------------------------#
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
        """ Handle mouse motion """
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
        """ Change the user direction based on the mouse position """
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
##                              AISmart class
##
###############################################################################
class AISmartInput(Basic):
    """ Decision class for AI that moves towards human 

    Attributes:
        directions: Map of tuples to decision methods
            (colIsLarger, isPositive) is the pattern
                Ex: (1,0) results in a left turn because that means that 
                the column difference is larger than the row difference and
                the difference is negative. Therefore the mouse is to the left
    """ 

    







    #------------------------- END PAGE 3 --------------------------#
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
        while not user.isDead().wait(timeout = Timeout.SLOWDECISION):
            self.turn(user.getMovement(), game)    

    def turn(self, movement, game):
        (col, row) = movement.getCenter()
        try:
            (humanCol, humanRow) = game.getHumanUser().getCenter() 
        except StopIteration:
            """ Human has been killed but not registered """
            return

        colDifference = humanCol - col
        rowDifference = humanRow - row

        colDifferenceLarger = (abs(colDifference)) > (abs(rowDifference))
        if colDifferenceLarger:
            return self.__directions[(1, colDifference > 0)](movement)

        return self.__directions[(0, rowDifference > 0)](movement)


###############################################################################
##
##                              AIRandom class
##
###############################################################################
class AIRandomInput(Basic):
    """ Decision class for AI to move randomly 

    Attributes:
        directions: Map of numbers to directions
    """
    def __init__(self):

        self.__directions   = dict(
            {
                0 : self.noTurn,
                1 : self.turnLeft,
                2 : self.turnRight,
                3 : self.turnUp,
                4 : self.turnDown
            }
        )

    def waitForDecision(self, user, game):
        while not user.isDead().wait(timeout = Timeout.SLOWDECISION):
            self.turn(user.getMovement())    

    def turn(self, movement):
        return self.__directions[randint(0, 4)](movement)