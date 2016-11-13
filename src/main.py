#!/usr/bin/env python

#   main.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   starts the game

import sys
from users import Food, Human
from movement import KeyInput, Stationary

import SyncGameBoard

BOARD_WIDTH = 7
BOARD_HEIGHT = 5

def main(argv):
	#syncGameBoard = SyncGameBoard(BOARD_WIDTH, BOARD_HEIGHT)
	#print(syncGameBoard)

	syncFood = Food(5)
	syncFood.expose()

	syncHuman = Human((3,4), KeyInput(	leftKey 	= "a", 
										rightKey 	= "d", 
										upKey 		= "w",
										downKey 	= "s"))
	syncHuman.expose()
	syncHuman.move("a")
	syncHuman.move("a")
	syncHuman.move("w")

	return



if __name__ == '__main__':
  main(sys.argv)


