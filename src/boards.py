#!/usr/bin/env python

#   boards.py
#
#   Sam Heilbron, Rachel Marison
#   Last Updated: December 9, 2016
#
#   List of board classes:
#       SyncGameBoard

import threading
import pygame
from enums import Color

###############################################################################
##
##                              SyncGameBoard class
##
###############################################################################
class SyncGameBoard(object):
    """A thread-safe game board that works with pygame.

    Attributes:
        width: The width of the board
        height: The height of the board
        players: Board containing the center postion of all active players
        locks: Locks restricting atomic access to players board 
        display: pygame display
        background: pygame background
    """

    def __init__(self, width = 700, height = 700):
        self.__width        = width
        self.__height       = height 
        self.__players      = self.initGameBoardPlayers()  
        self.__locks        = self.initGameBoardLocks()
        self.__display      = None
        self.__background   = None

    #######################   INITIALIZERS   ########################

    def initialize(self):
        """ Initialize the gameboard """
        self._initializeDisplay()
        self._initializeBackground()
        self._initializeTitle()

        self.updateBackground()
        self.updateDisplay()

    def _initializeDisplay(self):
        """ Create the pygame display """
        self.__display = pygame.display.set_mode(
                            (self.__width, self.__height), 
                            pygame.FULLSCREEN,
                            32)

    def _initializeBackground(self):
        """ Create the background for the game """
        background = pygame.Surface(self.__display.get_size())
        self.__background = background.convert()
        self.__background.fill(Color.WHITE)


    
    #------------------------- END PAGE 1 --------------------------#
    def _initializeTitle(self):
        """ Initialize the title to the display """
        titleFont = pygame.font.Font(None, 50)
        titleText = titleFont.render("TAG", 1, Color.BLACK)
        titleTextpos = titleText.get_rect(
                            centerx = self.__background.get_width()/2)
        helpFont = pygame.font.Font(None, 25)
        helpText = helpFont.render("Press q to quit", 1, Color.RED)
        helpTextpos = helpText.get_rect(
                            right = self.__background.get_width() - 10)
        self.__background.blit(titleText, titleTextpos)
        self.__background.blit(helpText, helpTextpos)

    def initGameBoardLocks(self):
        """ Initialize the board with a lock in each position """
        return [[threading.Lock() for r in range(self.__width + 1)] 
                    for c in range(self.__height + 1)]
        
    def initGameBoardPlayers(self):
        """ This board holds the players center position. """
        return [[None for r in range(self.__width + 1)] 
                    for c in range(self.__height + 1)]

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

    def getLockAtPosition(self, centerPosition):
        try:
            (col, row) = centerPosition
            return self.__locks[row][col]
        except IndexError:
            """ See the README for information about this error """
            print("There was an error when trying to acquire lock at r:%s, c: %s" \
                % (row, col))
            pass

    def getPlayerAtPosition(self, centerPosition):
        (col, row) = centerPosition
        return self.__players[row][col]

    ##########################   SETTERS   ##########################

    def updateDisplay(self):
        pygame.display.flip()

    def updateBackground(self):
        self.__display.blit(self.__background, (0, 0))

    


    #------------------------- END PAGE 2 --------------------------#
    def updateTimeClock(self, timeRemaining):
        """ Update the time that is visible to the user """
        timeFont = pygame.font.Font(None, 36)
        timeText = timeFont.render(str(timeRemaining), 1, Color.RED)
        timeTextpos = timeText.get_rect(left = 30)
        self.__display.blit(timeText, timeTextpos)

    def placeUserOnBoard(self, centerPosition, userID):
        """ Place a player on the board """
        self.getLockAtPosition(centerPosition).acquire()
        self._setPlayerAtPosition(centerPosition, userID)

    def pullUserFromBoard(self, centerPosition):
        """ Remove a player from its place on the board """
        self._setPlayerAtPosition(centerPosition, None)
        self.getLockAtPosition(centerPosition).release()

    def moveUser(self, oldPosition, newPosition, user):
        """ Move a user from one place to another """
        user.setCenter(newPosition)
        self.pullUserFromBoard(oldPosition)
        self.placeUserOnBoard(newPosition, user.getID())

    ########################   PROTECTED   ##########################

    def _setPlayerAtPosition(self, centerPosition, userID):
        """ Set a user id on the player board at a position """
        (col, row) = centerPosition
        self.__players[row][col] = userID