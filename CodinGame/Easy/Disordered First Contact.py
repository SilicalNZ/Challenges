"""Disordered First Contact

    Goal
Finally, we have received the first messages from aliens! Unfortunately we cannot understand them because they have a very unique way of speaking.

Here is how their messages are encoded:
abcdefghi
becomes
ghibcadef

First you take the first 1 character :
a

Then you take the following 2 characters and place it in the front of the string:
bc -> a

Then you take the following 3 characters and place it in the end of the string:
bca <- def

Repeat by taking more and more characters then complete with what remains:
ghi -> bcadef


Some messages have been transformed using the above method more than once.

Your job here is to decode or encode the messages to discuss with aliens.
"""
import sys
import math


class AlienLanguage(object):
    def __init__(self, message):
        self.message = message
        self.stages = self.seperate(message)

    @staticmethod
    def seperate(message: str):
        result, ct = [], 0
        while message:
            ct += 1
            if len(message) < ct:
                result.append(len(message))
                break
            else:
                result.append(ct)
                message = message[ct:]
        return result

    def encode(self):
        obj = self.message
        result = ""
        for x, i in enumerate(self.stages, 0):
            if x % 2 == 0:
                result += obj[:i]
            else:
                result = obj[:i] + result
            obj = obj[i:]
        self.message = result

    def decode(self):
        obj = self.message
        result = ""

        if len(self.stages) % 2 == 0:
            even = 0
        else:
            even = 1

        for x, i in enumerate(reversed(self.stages), even):
            if x % 2 == 0:
                result = obj[:i] + result
                obj = obj[i:]
            else:
                result = obj[-i:] + result
                obj = obj[:-i]
        self.message = result

n = int(input())
this = AlienLanguage(input())
print(this.message, file=sys.stderr)

for _ in range(abs(n)):
    if n > 0:
        this.decode()
    if n < 0:
        this.encode()
print(this.message)
