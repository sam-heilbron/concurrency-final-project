#!/usr/bin/env python

#   boards.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of board classes

import threading
import pygame
from enums import Color

## Represents the board that a group of users share
class SyncGameBoard(object):
    def __init__(self, width = 700, height = 700):
        self.__width        = width
        self.__height       = height  
        #self.__locks       = self.initGameBoard(threading.Lock())
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
        font = pygame.font.Font(None, 36)
        text = font.render("TAG", 1, Color.BLACK)
        textpos = text.get_rect(centerx = self.__background.get_width()/2)
        self.__background.blit(text, textpos)


    def updateDisplay(self):
        pygame.display.flip()

    def updateBackground(self):
        self.__display.blit(self.__background, (0, 0))

    def getDisplay(self):
        return self.__display

    def getBackground(self):
        return self.__background


    # Initialize the GameBoard with a value in each position
    def initGameBoard(self, val):
        return [[val for r in range(self.__width)] 
                    for c in range(self.__height)]
        
    # Paint a color at a location, if that pixel has not been painted on yet
    #def move(self, row, col, color):
    #    with self.locks[row][col]:
    #        #Do this