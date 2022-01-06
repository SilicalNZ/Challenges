"""Rugby score

    Goal
Given a rugby score, your program must compute the different scoring combinations that lead to that particular score.
As a reminder:
- a try is worth 5 points
- after a try, a transformation kick is played and is worth 2 extra points if successful
- penalty kicks and drops are worth 3 points
"""
import sys


def score_finder(n: int):
    quick_sort = n//3 + 1
    for x in range(0, quick_sort):
        for y in range(0, quick_sort):
            for z in range(0, quick_sort):
                scores = [x*5, y*2, z*3]
                if sum(scores) == n and x >= y:
                    print(' '.join([str(i) for i in [x, y, z]]))


score_finder(int(input()))
