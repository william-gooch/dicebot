"""This module contains the tools for representing and executing dice rolls.
"""
from random import randint


class Roll:
    def __init__(self,
                 sides: int,
                 num: int):
        self.sides = sides
        self.num = num
        self.mod = 0
        self.rolls = []
        self.roll()

    def roll(self):
        self.rolls = [randint(1, self.sides) for _ in range(0, self.num)]
        self.rolls.sort()

    def result(self):
        return sum(self.rolls) + self.mod

    def add_mod(self, n):
        self.mod += n

    def sub_mod(self, n):
        self.mod -= n

    def keep_highest(self, n):
        self.rolls = self.rolls[self.num-n:]

    def keep_lowest(self, n):
        self.rolls = self.rolls[:n]

    def drop_highest(self, n):
        self.rolls = self.rolls[:self.num-n]

    def drop_lowest(self, n):
        self.rolls = self.rolls[n:]
