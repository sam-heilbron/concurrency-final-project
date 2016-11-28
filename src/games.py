#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 25, 2016
#
#   List of game classes

import pygame
import threading
from boards import SyncGameBoard
from users import Food

class Game(object):
    """A Game. Base class for all games.

    Attributes:

    """

    def __init__(   self,
                    humanUser,
                    initialFoodCount    = 4,
                    initialAiCount      = 0,
                    boardType = SyncGameBoard()):
        self.__userList     = []
        self.__gameboard    = boardType
        self.__gameOverFlag = threading.Event()

        self.createUsers(initialFoodCount, initialAiCount, humanUser)

    def createUsers(self, foodCount, aiCount, human):
        for f in range(1, foodCount):
            self.__userList.append(
                Food( (int(100*f), int(400/f)) ))

        for a in range(1, aiCount):
            print("add ai user")

        ## Append human last so that when all users are started,
        ## The call to start the human happens last. This is because
        ## The human has their decision thread run in the main thread
        ## So if you start it before the others, the infinite loop will
        ## run and no other users will be created
        self.__userList.append(human)

    def isGameOver(self):
        return self.__gameOverFlag

    def initialize(self):
        pygame.init()
        self.__gameboard.initialize()

    def start(self):
        self.initialize()
        self.DrawEveryNSeconds(.001)

        """ Start all players """
        for user in self.__userList:
            user.start(self.__gameboard, self.__gameOverFlag)

    def DrawEveryNSeconds(self, nSeconds):
        drawingThread = threading.Thread(
                            target = self.drawAtInterval,
                            args = [nSeconds])
        drawingThread.start()

    def drawAtInterval(self, interval):
        while not self.__gameOverFlag.wait(timeout=interval):
            self.draw()

    def draw(self):
        self.__gameboard.updateBackground()
        
        for user in self.__userList:
            user.draw()
        
        self.__gameboard.updateDisplay()