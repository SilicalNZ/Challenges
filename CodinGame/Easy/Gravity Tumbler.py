"""Gravity Tumbler
    Goal
The program must output the result of tumbling a landscape a certain number of times.

Tumbling entails:
- rotating the landscape counterclockwise by 90°
- letting the hash bits # fall down

The map is composed of . and #.

(This puzzle is a twist (hah!) on classic community puzzle “Gravity”. You may want to solve that one first.)"""
import sys


width, height = [int(i) for i in input().split()]
print(width, height, file=sys.stderr)
count = int(input())
print(count, file=sys.stderr)
raster = [list(input()) for i in range(height)]
[print(''.join(i), file=sys.stderr) for i in raster]
rotated = raster

for i in range(count):
    new_raster = []
    for line in rotated:
        line = ''.join(line)
        a = line.count('#')
        b = len(line) - line.count('#')
        new_raster.append(list('.' * b + '#' * a))

    rotated = list(zip(*new_raster))

[print(''.join(i)) for i in rotated]
