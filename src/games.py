#!/usr/bin/env python

#   users.py
#
#   Sam Heilbron
#   Last Updated: November 25, 2016
#
#   List of game classes

import pygame

class Game(object):
    """A Game. Base class for all games.

    Attributes:

    """

    def __init__(   self,
                    userList,
                    boardType):
        self.__users = userList
        self.__board = boardType


    def start(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.__board.initializeDisplay()

        """ Start all players """
        for p in self.__users:
            p.start(self.__board)

        """ Run main game loop """
        while True:
            handleEvents()
            #drawGrid()

            self.__board.updateDisplay()
            clock.tick(30)

    def handleEvents():
        # The only event we need to handle in this program is when it terminates.
        global GAME_RUNNING

        for event in pygame.event.get(): 
            print(event)
            #if  (event.type == QUIT) or 
            #    (event.type == KEYDOWN and event.key == K_ESCAPE):
            #        GAME_RUNNING = False #
            #        pygame.quit()
            #       sys.exit()

        

    ##  Play all the musicians at the same time
    ##def play(self, bpm):
    #   threads = [threading.Thread(
    #                target = self.conductMusician,
    #                args = [musician, bpm])
    #           for musician in self.musicians]
    #   for t in threads:
    #        t.start()
    #   for t in threads:
    #       t.join()