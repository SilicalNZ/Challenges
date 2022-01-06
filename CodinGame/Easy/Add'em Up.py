"""Add'em Up

    Goal
Given a list of integers, add them up.
Wait... it will not be that easy.

Now there is an extra property to the operator ADD.
When you add a and b, it involves a cost of a+b.

If the list of numbers is 1, 2, 3
you can add them up in several ways.

Approach 1
1 + 2 = 3 (cost = 3)
3 + 3 = 6 (cost = 6)
Total cost = 9

Approach 2
1 + 3 = 4 (cost = 4)
4 + 2 = 6 (cost = 6)
Total cost = 10

Approach 3
2 + 3 = 5 (cost = 5)
5 + 1 = 6 (cost = 6)
Total cost = 11

Find the lowest cost to finish the addition.
"""
import sys


def smallest_add(lst: list):
    cost = 0
    while len(lst) > 1:
        print(lst, file=sys.stderr)

        x = min(lst)
        lst.remove(x)
        y = min(lst)
        lst.remove(y)
        z = x + y

        lst.append(z)
        cost += z
    return cost


n = int(input())
print(smallest_add([int(i) for i in input().split()]))
