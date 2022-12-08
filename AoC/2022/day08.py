import math

data = """"""

hor = [[*map(int, list(i))] for i in data.split("\n")]
ver = [*zip(*hor)]

# Part 1
dump = {}
[[dump.__setitem__((x, y), ele) for x, ele in enumerate(line[1:-1], 1) if max(line[:x]) >= ele <= max(line[x + 1:])] for y, line in enumerate(hor[1:-1], 1)]
print(len(hor[0]) * len(ver[0]) - sum([1 for coord, ele in dump.items() if max(ver[coord[0]][:coord[1]]) >= ele <= max(ver[coord[0]][coord[1] + 1:])]))

# Part 2
print(max([max([math.prod(map(lambda x: next((a for a, b in enumerate(x[0], 1) if b >= x[1]), len(x[0])), (([*reversed(line[:x])], ele), (line[x + 1:], ele), ([*reversed(ver[x][:y])], ele), (ver[x][y + 1:], ele)))) for x, ele in enumerate(line[1:-1], 1)]) for y, line in enumerate(hor[1:-1], 1)]))
