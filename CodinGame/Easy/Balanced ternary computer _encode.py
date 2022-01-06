"""Balanced ternary computer: encode

    Goal
Balanced ternary(3 base) is a non-standard positional numeral system. In the standard (unbalanced) ternary system, digits have values 0, 1 and 2. The digits in the balanced ternary system have values −1, 0, and 1. We use letter T to represent -1, so the digits are (T, 0, 1).

E.g.: 1T0 = 1 * (3**2) + (-1)*(3**1) + 0*(3**0) = 9 - 3 + 0 = 6

You must convert input integer (decimal) number to its balanced ternary representation.
"""
import sys


class Ternary(object):
    digits = (-1, 0, 1)
    track = [0]
    user_dont_touch_max = 1

    def formula(self, sequence):
        return sum([i * (3 ** x) for x, i in enumerate(reversed(sequence))])

    def find(self, number: int, user_dont_touch=1):
        self.user_dont_touch_max = max(self.user_dont_touch_max, user_dont_touch)

        if len(self.track) != self.user_dont_touch_max:
            self.track.append(0)

        for i in self.digits:
            self.track[-user_dont_touch] = i
            if user_dont_touch == 1:
                x = self.formula(self.track)
                if x == number:
                    return self.track
            else:
                if self.find(number, user_dont_touch - 1):
                    return self.track
        if self.user_dont_touch_max == user_dont_touch:
            if self.find(number, user_dont_touch + 1):
                return self.track

    def convert(self, sequence=None):
        if sequence is None:
            sequence = self.track
        return ''.join(['T' if i == -1 else str(i) for i in sequence])

x = Ternary()
x.find(int(input()))
print(x.convert())
