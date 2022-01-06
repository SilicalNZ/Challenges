"""Organic Compounds 🔬

    Goal
The Problem:

Write a program to input the condensed formula of an alicylic hydrocarbon, and decide whether it is valid or not.

--------------------------------------------------- xxx ---------------------------------------------------

Condensed Formula:

The condensed formula includes units of carbon linked to one another by one or more bonds.

1 unit of carbon is represented as CHn.

The bonds are adjacent to the carbon units, either horizontally or vertically. Bonds are represented as (m).

The inputs given will have a valid representation, but the bonds might not be matching. For example, a carbon unit with n=1 should have 3 adjacent bonds, one with n=2 should have 2 adjacent bonds, etc.

--------------------------------------------------- xxx ---------------------------------------------------

Note:

To get a better understanding of organic compounds and condensed formulae, look it up on the web
"""
import sys


class HydroCarbon_Analyzer(object):
    def __init__(self):
        self.hydrocarbon = []
        self.locations = []

    def add_chain(self, arg):
        """
        Append arg to molecule structure

        :param arg:
        :return:
        """
        self.hydrocarbon.append(self.adjust(arg, True))

    def adjust(self, arg, order=None):
        # Gets locations of all CH molecules and stores them
        arg = '   ' + arg
        obj = list(map(''.join, zip(*[iter(arg)]*3)))
        y = len(self.hydrocarbon)
        for x, i in enumerate(obj):
            if 'CH' in i:
                self.locations.append((x, y))

        # Converts to simplified obj
        obj =  arg.replace('CH', '') \
                .replace('(', '|') \
                .replace(')', '|') \
                .replace('   ', '|0|') \
                .replace('||', '|')

        # Shows result or representative number array
        if order:
            return [int(i) for i in obj.split('|') if i != '']
        else:
            return obj

    def analyze(self):
        obj = self.hydrocarbon
        obj = self._balance(obj)
        obj = self._give_border(obj)
        return self._calculate(obj)

    def _balance(self, arg):
        max_length = len(max(arg, key=len))
        for x, i in enumerate(arg):
            if len(i) < max_length:
                arg[x].extend([0 for i in range(max_length - len(i))])
        return arg

    def _give_border(self, arg):
        result = []
        for i in arg:
            result.append([0] + i + [0])
        tmp = [[0 for i in range(len(result[0]))]]
        result = tmp + result + tmp
        return result

    def _calculate(self, arg):
        for x, y in self.locations:
            x, y = x + 1, y + 1
            #         above +       below +        left +       right +    middle
            z = arg[y-1][x] + arg[y+1][x] + arg[y][x-1] + arg[y][x+1] + arg[y][x]
            if z % 4 != 0:
                return False
        return True


this = HydroCarbon_Analyzer()
x = ["CH3(1)CH1(1)CH2(1)CH1(1)CH3",
    "(1)         (1)",
    "CH3         CH1(1)CH1(1)CH3",
    "            (1)",
                "CH3"]
for i in x:
    compound = i
    print(compound, file=sys.stderr)
    this.add_chain(compound)
print("VALID") if this.analyze() else print("INVALID")