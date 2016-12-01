#!/usr/bin/env python

#   boards.py
#
#   Sam Heilbron
#   Last Updated: November 30, 2016
#
#   List of board classes

import threading
import pygame
from enums import Color

## Represents the board that a group of users share
class SyncGameBoard(object):
    def __init__(self, width = 800, height = 700):
        self.__width        = width
        self.__height       = height  
        self.__locks        = self.initGameBoardLocks()
        self.__players      = self.initGameBoardPlayers() 
        self.__display      = None
        self.__background   = None

    def initialize(self):
        self.initializeDisplay()
        self.initializeBackground()
        self.initializeTitle()

        self.updateBackground()
        self.updateDisplay()

    def initializeDisplay(self):
        self.__display = pygame.display.set_mode(
                            (self.__width, self.__height), 
                            pygame.FULLSCREEN)

    def initializeBackground(self):
        background = pygame.Surface(
                        self.__display.get_size())
        self.__background = background.convert()
        self.__background.fill(Color.WHITE)


    def initializeTitle(self):
        titleFont = pygame.font.Font(None, 50)
        titleText = titleFont.render("TAG", 1, Color.BLACK)
        titleTextpos = titleText.get_rect(
                            centerx = self.__background.get_width()/2)
        helpFont = pygame.font.Font(None, 36)
        helpText = helpFont.render("Press q to quit", 1, Color.RED)
        helpTextpos = helpText.get_rect(
                            right = self.__background.get_width() - 10)
        self.__background.blit(titleText, titleTextpos)
        self.__background.blit(helpText, helpTextpos)

    def updateDisplay(self):
        pygame.display.flip()

    def updateBackground(self):
        self.__display.blit(self.__background, (0, 0))

    def getDisplay(self):
        return self.__display

    def getBackground(self):
        return self.__background

    def getDimensions(self):
        return self.__width, self.__height

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getLocks(self):
        return self.__locks

    def getPlayers(self):
        return self.__players

    def getLockAtCenter(self, centerPosition):
        (col, row) = centerPosition
        return self.__locks[row][col]

    def getPlayerAtPosition(self, centerPosition):
        (col, row) = centerPosition
        return self.__players[row][col]

    def initGameBoardLocks(self):
        """ Init the board with a value in each position """
        return [[threading.Lock() for r in range(self.__width)] 
                    for c in range(self.__height)]
        
    def initGameBoardPlayers(self):
        """ This board holds players at their positions.
            Board is initialized to None. """
        return [[None for r in range(self.__width)] 
                    for c in range(self.__height)]

