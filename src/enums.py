#!/usr/bin/env python

#   enums.py
#
#   Sam Heilbron
#   Last Updated: November 28, 2016
#
#   List of enums 
#

def enum(**named_values):
	return type('Enum', (), named_values)

Direction = enum(
    UP      = 1,
    DOWN    = 2,
    LEFT    = 3,
    RIGHT   = 4,
    STAY    = 5)

Color = enum(
	BLACK 	= (0, 0, 0),
	WHITE 	= (255, 255, 255),
	BLUE 	= (0, 0, 255),
	GREEN 	= (0, 255, 0),
	RED 	= (255, 0, 0))

InitialUserRadius = enum(
	FOOD	= 5,
	AI		= 15,
	HUMAN	= 10)

Timeout = enum(
	MOVEMENT = .001,
	DECISION = .05,
	GAMEOVER = .0001)

# Frames per Second
FPS = enum(
	DECISION 		= 20,
	SLOWDECISION 	= 5)