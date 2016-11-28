#!/usr/bin/env python

#   main.py
#
#   Sam Heilbron
#   Last Updated: November 21, 2016
#
#   starts the game

import os, sys
import getch

from games import Game
from users import Human
from decisions import KeyInput, MouseInput


def main(argv):

	openingMessage()

	user = getUserInput()
	createAndStartGame(user)

	return

def openingMessage():
	os.system('clear')
	print("Welcome to the game of tag. \n\
	Your goal is to move your red player around the board. \n\
	If you collide with another player, the larger one eats the other \n\
		and the smaller one loses. \n\
	As you eat other players, your move more slowly \n\
	Food sources will generate and don't move \n\
	Opponents can be other humans or robots \n\
	GOOD LUCK!! \n")

	print("press any key to continue...")
	getch.getch()

def getUserInput():
	c = None
	while(c != 'k' and c != 'm'):
		os.system('clear')
		print("Select your input type by typing a key: \n\
			k: keyboard input (arrow keys) \n\
			m: mouse input \n ")
		c = getch.getch()
		
	print("The game will begin shortly...\n")

	if c == 'k':
		return Human(1, (100,200), KeyInput())
	elif c == 'm':
		return Human(1, (100,200), MouseInput())
	else:
		print("An error occurred.")


def createAndStartGame(user):
	game = Game(
			humanUser 			= user,
			initialFoodCount 	= 4,
			initialAiCount 		= 0)

	game.start()


if __name__ == '__main__':
	main(sys.argv)


