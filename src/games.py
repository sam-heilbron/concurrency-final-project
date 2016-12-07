#!/usr/bin/env python

#   games.py
#
#   Sam Heilbron
#   Rachel Marison
#   Last Updated: December 7, 2016
#
#   List of game classes

import pygame
import threading
from boards import SyncGameBoard
from users import Food, AI
from random import randint
from enums import Timeout

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
                    initialCenter = (randint(20, maxWidth - 20), 
                                     randint(20, maxHeight - 20))))

        for a in range(1, aiCount + 1):
            self.__userList.append(
                AI( 
                    id_ = "ai_" + str(a),
                    initialCenter = (randint(20, maxWidth - 20), 
                                     randint(20, maxHeight - 20))))

        """
            Append human last so that when all users are started,
        the call to start the human happens last. This is because
        the human has their decision thread run in the main thread
        so if you start it before the others, the infinite loop will
        run and no other users will be created
        """
        self.__userList.append(human)

    ##########################   GETTERS   ##########################

    def getGameboard(self):
        return self.__gameboard

    def getGameOverFlag(self):
        return self.__gameOverFlag

    def getUserFromID(self, userID):
        try:
            u = next(user for user in self.__userList if user.getID() == userID)
            return u
        except StopIteration:
            """ userID not in game currently """
            print("user: -%s- not in game currently" % userID)
            pass

    def getHumanUser(self):
        try:
            u = next(user for user in self.__userList if user.getID() == "human")
            return u
        except StopIteration:
            """ userID not in game currently """
            pass

    ##########################   SETTERS   ##########################

    def killUserWithID(self, userID):
        try:
            u = next(user for user in self.__userList if user.getID() == userID)
            u.quit()
            self.__userList.remove(u)
        except StopIteration:
            """ userID not in game currently """
            pass

    def pullUserFromBoard(self, position):
        self.__gameboard.pullUserFromBoard(position)

    ########################   START GAME   #########################

    def start(self):
        pygame.init()
        self.__gameboard.initialize()

        self._startGameOverListener()
        self._startDrawing()
        self._startUsers()

    def _startUsers(self):
        for user in self.__userList:
            self._placeUserOnBoard(user)
            user.start(self)

    def _placeUserOnBoard(self, user):
        self.__gameboard.placeUserOnBoard(user.getCenter(), user.getID())


    #########################   END GAME   ##########################

    def _startGameOverListener(self):
        gameListenerThread = threading.Thread(
                                target = self._waitForGameOver,
                                args = [])
        gameListenerThread.start()

    def _waitForGameOver(self):
        """ Wait for flag to be set, then trigger game over """
        self.__gameOverFlag.wait()
        self._gameOver()

    def _gameOver(self):
        print("Trigger Game over.")
        # pygame.quit() Seems this is unnecessary
        for user in self.__userList:
            user.quit()


    ########################   DRAW BOARD   #########################

    def _startDrawing(self):
        """ Spawn drawing in another thread """
        drawingThread = threading.Thread(
                            target = self._drawAtInterval,
                            args = [])
        drawingThread.start()

    def _drawAtInterval(self):
        while not self.__gameOverFlag.wait(timeout=Timeout.GAMEOVER):
            self._draw()

    def _draw(self):
        self.__gameboard.updateBackground()
        
        for user in self.__userList:
            user.draw()
        
        self.__gameboard.updateDisplay()
