#!/usr/bin/env python

#   decisions.py
#
#   Sam Heilbron
#   Last Updated: November 21, 2016
#
#   List of decision classes
#

from collections import defaultdict
from enums import Direction, FPS
import pygame
import sys

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
        pygame.quit()
        sys.exit()


###############################################################################
##
##                              Stationary class
##
###############################################################################
class Stationary(Basic):
    """ Decision class for a Stationary player """

    ## Theoretically you could just return, but it's more realistic to 
    ## have a thread alive as long as the user is alive
    def waitForDecision(self, user, gameOverFlag):
        """ DEFAULT: Loop on nothing """
        clock = pygame.time.Clock()
        while not user.isDead():
            clock.tick(FPS.DECISION)


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

    def waitForDecision(self, user, gameOverFlag):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitGame(gameOverFlag)
                    else:
                        self.turn(user.getMovement(), event.key)
                elif event.type == pygame.QUIT:
                    self.quitGame(gameOverFlag)
            """ 20 frames per second """
            clock.tick(FPS.DECISION)      

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

    def waitForDecision(self, user, gameOverFlag):
        """ @TODO: would like to switch while 1 --> while not user.isDead ()
            but that was causing issues. will look into
        """
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.turn(user.getMovement(), event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitGame(gameOverFlag)
                elif event.type == pygame.QUIT:
                    self.quitGame(gameOverFlag)
            """ 20 frames per second """
            clock.tick(FPS.DECISION)
     

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
class AIInput(Basic):
    """ Decision class for AI input (auto-move) 

    @TODO: create decision algorithm for ai to move on its own
    """

    def turn(self, movement):
        print("ai move")