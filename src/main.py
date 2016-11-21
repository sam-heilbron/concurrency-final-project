#!/usr/bin/env python

#   main.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   starts the game

import sys
from users import Food, Human
from decisions import KeyInput, Stationary
from movements import Sphere


BOARD_WIDTH = 7
BOARD_HEIGHT = 5

def main(argv):

	human = Human(1, [(1,2), (1,3)])
	human.expose()

	human.move("a")
	human.move("j")
	human.expose()
	human.move("a")
	human.expose()
	human.move("a")
	human.expose()


	return



if __name__ == '__main__':
  main(sys.argv)


