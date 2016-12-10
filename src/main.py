#!/usr/bin/env python

#   main.py
#
#   Sam Heilbron
#   Rachel Marison
#   Last Updated: December 7, 2016
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
	""" Print a welcome message with directions about how to play """

	os.system('clear')

	welcomeScreen = "Welcome to the game of tag!. \n\n\
	The rules are as follows: \n\
		1. You control the red player, which starts in the top left corner \n\
		2. If you collide with another player, \n\
			the larger one eats the smaller one \n\
		3. The larger you are, the slower you move \n\
		4. If you eat all the opponents you win \n\
		5. You have 30 seconds before the game is over and you lose \n\n\
	You will find the following opponents on the board: \n\
		BLACK - These are food sources and Can't move \n\
		GREEN - These are AI's that will move in a random pattern \n\
		BLUE - These are AI's that will move towards you \n\n\
	GOOD LUCK!\n"

	sys.stdout.write("{:<7}\n".format(welcomeScreen))

	print("press any key to continue...")
	getch.getch()

def getUserInput():
	""" Prompt user to choose between keys and mouse as input """

	c = None

	""" Loop on invalid inputs """
	while(c != 'k' and c != 'm'): 
		os.system('clear')
		keyboardOptionScreen = "Select your input type: \n\
		Keyboard: Use the arrow keys to control your movement. \n\
			press k to select \n\
		Mouse: Use the mouse to control your movement\n\
			press m to select \n "
		sys.stdout.write("{:<7}\n".format(keyboardOptionScreen))
		c = getch.getch()
	print("The game will begin shortly...\n")

	if c == 'k':
		return Human((10,10), KeyInput())
	return Human((10,10), MouseInput())

def createAndStartGame(user):
	""" Create a game and start playing """

	game = Game(
			humanUser 				= user,
			initialFoodCount 		= 20,
			initialSmartAiCount 	= 1,
			initialRandomAiCount	= 5)
	game.start()


if __name__ == '__main__':
	main(sys.argv)
