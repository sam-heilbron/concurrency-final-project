#!/usr/bin/env python

#   games.py
#
#   Sam Heilbron
#   Last Updated: November 30, 2016
#
#   List of game classes

import pygame
import threading
from boards import SyncGameBoard
from users import Food
from random import randint

class Game(object):
    """A Game. Base class for all games.

    Attributes:
        userList: the list of users participating
        gameboard: the board that is being played on
        gameOverFlag: a flag that is set when the game finishes
    """

    def __init__(   self,
                    humanUser,
                    initialFoodCount    = 4,
                    initialAiCount      = 0,
                    boardType           = SyncGameBoard()):
        self.__userList     = []
        self.__gameboard    = boardType
        self.__gameOverFlag = threading.Event()

        self.createUsers(initialFoodCount, initialAiCount, humanUser)

    def createUsers(self, foodCount, aiCount, human):
        maxWidth, maxHeight = self.__gameboard.getDimensions()
        for f in range(1, foodCount + 1):
            self.__userList.append(
                Food( 
                    id_ = "food_" + str(f),
                    initialCenter = (randint(0,maxWidth - 20), 
                                     randint(0,maxHeight - 20))))

        ##for a in range(1, aiCount):
        ##    print("add ai user")

        """
            Append human last so that when all users are started,
        the call to start the human happens last. This is because
        the human has their decision thread run in the main thread
        so if you start it before the others, the infinite loop will
        run and no other users will be created
        """
        self.__userList.append(human)

    def getGameboard(self):
        return self.__gameboard

    def getGameOverFlag(self):
        return self.__gameOverFlag

    def start(self):
        pygame.init()
        self.__gameboard.initialize()

        self.startGameOverListener()
        self.startDrawing()
        self.startUsers()


    def startUsers(self):
        for user in self.__userList:
            user.start(self)

    def startGameOverListener(self):
        gameListenerThread = threading.Thread(
                                target = self.waitForGameOver,
                                args = [])
        gameListenerThread.start()

    def waitForGameOver(self):
        """ Wait for flag to be set, then trigger game over """
        self.__gameOverFlag.wait()
        self.gameOver()

    def gameOver(self):
        print("Trigger Game over.")
        for user in self.__userList:
            user.quit()

    def killUserWithID(self, userID):
        try:
            u = next(user for user in self.__userList if user.getID() == userID)
            u.quit()
            self.__userList.remove(u)
        except StopIteration:
            """ userID not in game currently """
            pass
        
    def getUserFromID(self, userID):
        try:
            u = next(user for user in self.__userList if user.getID() == userID)
            return u
        except StopIteration:
            """ userID not in game currently """
            pass


    def startDrawing(self):
        """ Spawn drawing in another thread """
        drawingThread = threading.Thread(
                            target = self.drawAtInterval,
                            args = [])
        drawingThread.start()

    def drawAtInterval(self, interval = .001):
        while not self.__gameOverFlag.wait(timeout=interval):
            self.draw()

    def draw(self):
        self.__gameboard.updateBackground()
        
        for user in self.__userList:
            user.draw()
        
        self.__gameboard.updateDisplay()
