#!/usr/bin/env python

#   games.py
#
#   Sam Heilbron, Rachel Marison
#   Last Updated: December 9, 2016
#
#   List of game classes:
#       Game

import threading
import pygame
from random import randint
from time import sleep
import time
from boards import SyncGameBoard
from users import Food, AISmart, AIRandom
from enums import Timeout

## Number of seconds between when screen is 
## shown to the user and movement begins
COUNTDOWN_DELAY = 3

###############################################################################
##
##                              Game class
##
###############################################################################
class Game(object):
    """A Game. Base class for all games.

    Attributes:
        userList: the list of users participating
        gameboard: the board that is being played on
        endTime: The time at which the gameOverTimeout will be set
        gameTimeSeconds: The number of seconds the game will last
        gameOverFlag: a flag that is set when the game finishes
        gameOverTimeout: a flag that is set when the game runs out of time
    """

    def __init__(   self,
                    humanUser,
                    initialFoodCount        = 4,
                    initialSmartAiCount     = 0,
                    initialRandomAiCount    = 0,
                    gameTimeSeconds         = 30,
                    boardType               = SyncGameBoard()):
        self.__userList         = []
        self.__gameboard        = boardType
        self.__endTime          = None
        self.__gameTimeSeconds  = gameTimeSeconds
        self.__gameOverFlag     = threading.Event()
        self.__gameOverTimeout  = threading.Event()

        self.createUsers(
            initialFoodCount, 
            initialSmartAiCount, 
            initialRandomAiCount,
            humanUser)

    def createUsers(self, foodCount, smartAiCount, randomAiCount, human):
        """ Create the oppponents and add them to the player list """
        maxWidth, maxHeight = self.__gameboard.getDimensions()

        wMin, wMax = (20, maxWidth - 20)
        hMin, hMax = (20, maxHeight - 20)

        for f in range(1, foodCount + 1):
            self.__userList.append(
                Food( 
                    id_ = "food_" + str(f),
                    initialCenter = (randint(wMin, wMax), 
                                     randint(hMin, hMax))))

        for a in range(1, smartAiCount + 1):
            """ Ensure that smart AI's start on the other half of the board """
            self.__userList.append(
                AISmart( 
                    id_ = "smart_ai_" + str(a),
                    initialCenter = (randint(wMin, wMax), 
                                     randint(int(hMax/2), hMax))))

        for a in range(1, randomAiCount + 1):
            self.__userList.append(
                AIRandom( 
                    id_ = "random_ai_" + str(a),
                    initialCenter = (randint(wMin, wMax), 
                                     randint(hMin, hMax))))

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
        """ raises StopIteration if userID not found """
        u = next(user for user in self.__userList if user.getID() == userID)
        return u

    def getHumanUser(self):
        return self.getUserFromID("human")

    def _getRemainingTime(self):
        return int(self.__endTime - time.time())

    ##########################   SETTERS   ##########################

    def killUserWithID(self, userID):
        try:
            u = self.getUserFromID(userID)
            u.quit()
            self.__userList.remove(u)

            if len(self.__userList) == 1:
                """ Only human remains """
                self.__gameOverFlag.set()
                self._win()

        except StopIteration:
            """ userID not in game currently """
            pass

    def pullUserFromBoard(self, position):
        self.__gameboard.pullUserFromBoard(position)

    def _setRemainingTime(self, remainingTime):
        self.__endTime = time.time() + remainingTime

    ########################   START GAME   #########################

    def start(self):
        pygame.init()
        self.__gameboard.initialize()

        self._startDrawing()
        self._startUsers()

    def _startUsers(self):
        """ Place all the users on the board """
        for user in self.__userList:
            self._placeUserOnBoard(user)

        """ Delay start so user has time to see board and make plan """
        sleep(COUNTDOWN_DELAY)

        """ Set game clock and prepare game over threads """
        self._setRemainingTime(self.__gameTimeSeconds)
        self._startGameOverListener()

        """ Start user movement """
        for user in self.__userList:
            user.start(self)

    def _placeUserOnBoard(self, user):
        self.__gameboard.placeUserOnBoard(user.getCenter(), user.getID())


    #########################   END GAME   ##########################

    def _startGameOverListener(self):
        """ Listen for end of game """
        gameListenerThread = threading.Thread(
                                target = self._waitForGameOverSignal,
                                args = [])
        gameTimeoutThread = threading.Thread(
                                target = self._waitForGameOverTimeout,
                                args = [])

        gameListenerThread.start()
        gameTimeoutThread.start()

    def _waitForGameOverSignal(self):
        """ Wait for game over flag from a collision """
        self.__gameOverFlag.wait()
        self.__gameOverTimeout.set()
        self._gameOver()

    def _waitForGameOverTimeout(self):
        """ Wait for game clock to run out """
        while not self.__gameOverTimeout.wait(timeout = .5):
            if self._getRemainingTime() <= 0:
                self.__gameOverTimeout.set()
                self._outOfTimeMessage()
        self.__gameOverFlag.set()

    def _gameOver(self):
        """ Quit all user threads """
        for user in self.__userList:
            user.quit()

    def _outOfTimeMessage(self):
        """ Print a message to the user if they run out of time """
        print("\n\nYou ran out of time.")
        print("FINAL SCORE: %s" % self.getHumanUser().getRadius())

    def _win(self):
        """ Notify the user that they won """
        print("CONGATULATIONS! YOU WON THE GAME")


    ########################   DRAW BOARD   #########################

    def _startDrawing(self):
        """ Spawn a drawing thread """
        drawingThread = threading.Thread(
                            target = self._drawAtInterval,
                            args = [])
        drawingThread.start()

    def _drawAtInterval(self):
        """ Draw the gameboard rapidly to account for position changes """
        self._setRemainingTime(COUNTDOWN_DELAY)

        while not self.__gameOverFlag.wait(timeout=Timeout.GAMEOVER):
            self._draw()

    def _draw(self):
        """ Draw the gameboard with all active users and time remaining """
        self.__gameboard.updateBackground()
        self.__gameboard.updateTimeClock(self._getRemainingTime())

        for user in self.__userList:
            user.draw()
        
        self.__gameboard.updateDisplay()