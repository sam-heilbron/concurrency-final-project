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


class Basic(object):
    """ Base class for all decision classes """

    def turnLeft(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.LEFT)

    def turnRight(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.RIGHT)

    def turnUp(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.UP)

    def turnDown(self, currentPosition):
        currentPosition.setCurrentDirection(Direction.DOWN)

    def noTurn(self, currentPosition):
        """ No turn associated with that decision """
        return

    def waitForDecision(self, currentPosition, gameOverFlag):
        """ DEFAULT: Do nothing """
        return

    def quitGame(self, gameOverFlag):
        gameOverFlag.set()
        pygame.quit()
        sys.exit()


class Stationary(Basic):
    """ Decision class for a Stationary player """

    def turn(self, currentPosition, gameOverFlag):
        return



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

    def waitForDecision(self, currentPosition, gameOverFlag):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitGame(gameOverFlag)
                    else:
                        self.turn(currentPosition, event.key)
                elif event.type == pygame.QUIT:
                    self.quitGame(gameOverFlag)
            """ 20 frames per second """
            clock.tick(FPS.DECISION)
                

    def turn(self, currentPosition, keyPressed):
        return self.__directions[keyPressed](currentPosition)


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

    def waitForDecision(self, currentPosition, gameOverFlag):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.turn(currentPosition, event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitGame(gameOverFlag)
                elif event.type == pygame.QUIT:
                    self.quitGame(gameOverFlag)
            """ 20 frames per second """
            clock.tick(FPS.DECISION)       

    def turn(self, currentPosition, mousePosition):
        (col, row) = currentPosition.getCenter()
        (mouseCol, mouseRow) = mousePosition

        colDifference = mouseCol - col
        rowDifference = mouseRow - row

        colDifferenceLarger = (abs(colDifference)) > (abs(rowDifference))
        if colDifferenceLarger:
            return self.__directions[(1, colDifference > 0)](currentPosition)

        return self.__directions[(0, rowDifference > 0)](currentPosition)




class AIInput(Basic):
    """ Decision class for AI input (auto-move) 

    @TODO: create decision algorithm for ai to move on its own
    """

    def turn(self, currentPosition):
        print("ai move")