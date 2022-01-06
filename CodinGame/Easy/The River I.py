"""The River I.

    Goal
A digital river is a sequence of numbers where every number is followed by the same number plus the sum of its digits. In such a sequence 123 is followed by 129 (since 1 + 2 + 3 = 6), which again is followed by 141.

We call a digital river river K, if it starts with the value K.

For example, river 7 is the sequence beginning with {7, 14, 19, 29, 40, 44, 52, ... } and river 471 is the sequence beginning with {471, 483, 498, 519, ... }.

Digital rivers can meet. This happens when two digital rivers share the same values. River 32 meets river 47 at 47, while river 471 meets river 480 at 519.

Given two meeting digital rivers print out the meeting point.

(Idea : BIO'99)
"""
import sys


a = int(input())
b = int(input())
data = {'a': a, 'b': b}

while data['a'] != data['b']:
    x = min(data, key=data.get)
    values = [int(i) for i in list(str(data[x]))]
    data[x] += sum(values)
    print(data, file=sys.stderr)

print(data['a'])
