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

###############################################################################
##
##                              SyncGameBoard class
##
###############################################################################
class SyncGameBoard(object):
    def __init__(self, width = 800, height = 700):
        self.__width        = width
        self.__height       = height  
        self.__locks        = self.initGameBoardLocks()
        self.__players      = self.initGameBoardPlayers() 
        self.__display      = None
        self.__background   = None


    #######################   INITIALIZERS   ########################

    def initialize(self):
        self._initializeDisplay()
        self._initializeBackground()
        self._initializeTitle()

        self.updateBackground()
        self.updateDisplay()

    def _initializeDisplay(self):
        self.__display = pygame.display.set_mode(
                            (self.__width, self.__height), 
                            pygame.FULLSCREEN)

    def _initializeBackground(self):
        background = pygame.Surface(
                        self.__display.get_size())
        self.__background = background.convert()
        self.__background.fill(Color.WHITE)


    def _initializeTitle(self):
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

    def initGameBoardLocks(self):
        """ Init the board with a value in each position """
        return [[threading.Lock() for r in range(self.__width)] 
                    for c in range(self.__height)]
        
    def initGameBoardPlayers(self):
        """ This board holds players at their positions.
            Board is initialized to None. """
        return [[None for r in range(self.__width)] 
                    for c in range(self.__height)]

    ##########################   GETTERS   ##########################          

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

    def getLockAtCenter(self, centerPosition):
        (col, row) = centerPosition
        return self.__locks[row][col]

    def getPlayerAtPosition(self, centerPosition):
        (col, row) = centerPosition
        return self.__players[row][col]

    ##########################   SETTERS   ##########################

    def updateDisplay(self):
        pygame.display.flip()

    def updateBackground(self):
        self.__display.blit(self.__background, (0, 0))

    def setPlayerAtPosition(self, centerPosition, userID):
        """ 
            @TODO: Perhaps add check for self.__players boundaires
            (though we know it will never go out of bounds since 
                we're controlling it)
        """
        (col, row) = centerPosition
        self.__players[row][col] = userID