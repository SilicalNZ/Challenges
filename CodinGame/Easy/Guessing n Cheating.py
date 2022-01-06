"""Guessing n Cheating

    Goal
Alice and Bob are playing a guessing game. Alice thinks of a number between 1 and 100 (both inclusive). Bob guesses whjat it is. Alice then replies "too high", "too low" or "right on". After repeated rounds of guessing and replying, Bob should be able to hit right on the number.

After some games, Bob suspects Alice is cheating - that she changed the number in the middle of the game, or just gave a false response. To collect evidence against Alice, Bob recorded the transcripts of several games. You are invited to help Bob to determine whether Alice cheated in each game.

An example game between Bob ande Alice:

A game of 3 rounds
"""
import sys




class HoLChecker(object):
    boundary = 1, 100
    phrases = "too low", "too high", "right on", "within range"

    def question(self, num: int):
        if max(self.boundary) > num > min(self.boundary):
            return self.phrases[3]
        elif num > max(self.boundary):
            return self.phrases[1]
        elif num < min(self.boundary):
            return self.phrases[0]



this = HoLChecker()
for _ in range(int(input())):
    n, nxt1, nxt2 = input().split()
    answer = f"{nxt1} {nxt2}"

    question = this.question(int(n))
    if question == answer:
        continue
    elif question == this.phrases[3]:



