#!/usr/bin/env python

#   main.py
#
#   Sam Heilbron
#   Last Updated: November 21, 2016
#
#   starts the game

import sys
from users import Food, Human
from boards import SyncGameBoard
from decisions import KeyInput, MouseInput
from games import Game
from enums import Color

import pygame
import pyautogui

def main(argv):
	pygame.init()
	
	board = SyncGameBoard()
	board.initialize()

	keyInput = KeyInput()
	mouseInput = MouseInput()

	human = Human(1, (100,200), mouseInput)
	human.start(board)

	"""
	print("reached here\n\n\n\n\n")
	while 1:
		print("DISPLAY BOARD")
		board.updateBackground()
		human.draw()
		board.updateDisplay()
		sleep(1000)

	#game = Game([human], board)
	#game.start()

	"""

	return


if __name__ == '__main__':
	main(sys.argv)


