#!/usr/bin/env python

#   SyncGameBoard.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   SyncGameBoard class

import threading

## Represents the canvas that a group of artists could work on
class SyncGameBoard(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height  
        self.locks = self.initGameBoard(threading.Lock(), width, height)

    # Initialize the GameBoard with a value in each position
    def initGameBoard(self, val, width, height):
        return [[val for r in range(width)] for c in range(height)]
        
    # Paint a color at a location, if that pixel has not been painted on yet
    #def move(self, row, col, color):
    #    with self.locks[row][col]:
    #        #Do this
