"""During World War II, the Germans were using an encryption code called Enigma – which was basically an encryption machine that encrypted messages for transmission. The Enigma code went many years unbroken. Here How Basic Machine works:

First Caesar shift is applied using an incrementing number.
If AAA and starting number is 4 then output will be EFG.
A + 4 = E
A + 4 + 1 = F
A + 4 + 1+ 1 = G
Now EFG from 1st Motor such as "ABCDEFGHIJKLMNOPQRSTUVWXYZ" --> "BDFHJLCPRTXVZNYEIWGAKMUSQO"
so EFG become "JLC". Then it is passed through 2 more rotors to get final value.
If the second ROTOR is "AJDKSIRUXBLHWTMCQGZNPYFVOE", we apply the substitution step again thus:
ABCDEFGHIJKLMNOPQRSTUVWXYZ
AJDKSIRUXBLHWTMCQGZNPYFVOE
So "JLC" becomes "BHD".

If the third ROTOR is "EKMFLGDQVZNTOWYHXUSPAIBRCJ", then the final substitution is "BHD" becoming "KQF".
Final Output is sent via Radio Transmitter.
"""
import sys
import math
import random

VERSION = '0.0.1'


class Shifts:

    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, message):
        self.original = message
        self.message = message

    def caesar(self, num: int, reverse=False):
        num = -num if reverse else num
        res = []
        for x, letter in enumerate(self.message, 0):
            if reverse:
                x = -x
            new_letter = self.ALPHABET.index(letter) + x + num
            new_letter = new_letter % len(self.ALPHABET)
            new_letter = self.ALPHABET[new_letter]
            res.append(new_letter)
        self.message = ''.join(res)


        return self.message

    def motor(self, rotor, reverse=False):
        res = []
        for letter in self.message:
            if not reverse:
                idx = self.ALPHABET.index(letter)
                res.append(rotor[idx])
            else:
                idx = rotor.index(letter)
                res.append(self.ALPHABET[idx])

        self.message = ''.join(res)
        return self.message


class Enigma(Shifts):
    def __init__(self, message, pseudo_random_number=None):
        Shifts.__init__(self, message)
        self.rotors = []
        self.pseudo_random_number = random.randint(0, 10) if pseudo_random_number is None else pseudo_random_number

    def add_rotor(self, rotor):
        self.rotors.append(rotor)

    def encode(self):
        self.caesar(self.pseudo_random_number)
        [self.motor(i) for i in self.rotors]
        return self.message

    def decode(self):
        [self.motor(i, True) for i in reversed(self.rotors)]
        self.caesar(self.pseudo_random_number, True)
        return self.message

    DECODE = decode
    ENCODE = encode


if __name__ == '__main__':
    operation = input()
    pseudo_random_number = int(input())


    # Builds operable message
    this = Enigma(None, pseudo_random_number)
    [this.add_rotor(input()) for _ in range(3)]
    this.message = input()

    print(getattr(this, operation)())
