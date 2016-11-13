#!/usr/bin/env python

#   movement.py
#
#   Sam Heilbron
#   Last Updated: November 12, 2016
#
#   List of movement classes


## Represents the canvas that a group of artists could work on
class Stationary(object):

    def __init__(self):
        self.__name = "stationary"

    def move(self):
        print(self.__name)


class Human(object):

    def __init__(self):
        self.__name = "human"

    def move(self):
        print(self.__name)