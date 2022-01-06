"""The River II.

    Goal
A digital river is a sequence of numbers where every number is followed by the same number plus the sum of its digits. In such a sequence 123 is followed by 129 (since 1 + 2 + 3 = 6), which again is followed by 141.

We call a digital river river K, if it starts with the value K.

For example, river 7 is the sequence beginning with {7, 14, 19, 29, 40, 44, 52, ... } and river 471 is the sequence beginning with {471, 483, 498, 519, ... }.

Digital rivers can meet. This happens when two digital rivers share the same values. River 32 meets river 47 at 47, while river 471 meets river 480 at 519.

Given a number decide, whether it can be a meeting point of two or more digital rivers. For example, it is easy to check that only river 20 contains the number 20 in its sequence (as a starting point).

(Idea : BIO'99)
"""
import sys


class River(object):
    track = 0

    def expression(self, number: int):
        value = [int(i) for i in str(number)]
        return number + sum(value)

    def execute(self, rivers, value):
        print(value, file=sys.stderr)
        for i in range(1, 99):
            check = value - i
            if check > 0:
                print(check, file=sys.stderr)
                if self.expression(check) == value:
                    print('True', file=sys.stderr)
                    self.track += 1
                    # A river might be able to be made from the current river
                    if self.execute(rivers, check):
                        break
            else:
                break
        return True if self.track >= rivers else False


print('YES') if River().execute(2, int(input())) else print('NO')
