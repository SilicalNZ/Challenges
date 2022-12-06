data = """"""

stacks, moves = [i for i in data.split("\n\n")]
stacks = [*zip(*(i[1::4] for i in stacks.split("\n")[:-1]))]
stacks = [[i for i in reversed(stack) if i != ' '] for stack in stacks]
moves = [*([*map(int, (j[1], j[3], j[5]))] for j in (i.split(" ") for i in moves.split("\n")))]

# First solution
[[stacks[c - 1].append(stacks[b - 1].pop()) for x in range(a)] for a, b, c in moves]
[print(i[-1], end="") for i in stacks]

# Second solution
[stacks[c - 1].extend(stacks[b - 1][-a:]) or stacks.__setitem__(b - 1, stacks[b - 1][:-a]) for a, b, c in moves]
[print(i[-1], end="") for i in stacks]





