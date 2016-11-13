#!/usr/bin/env python

#   main.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   starts the game

import sys
from users import SyncFood

import SyncGameBoard

BOARD_WIDTH = 7
BOARD_HEIGHT = 5

def main(argv):
	#syncGameBoard = SyncGameBoard(BOARD_WIDTH, BOARD_HEIGHT)
	#print(syncGameBoard)

	syncFood = SyncFood(5)
	syncFood.expose()

	return



if __name__ == '__main__':
  main(sys.argv)


