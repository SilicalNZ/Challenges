data = """"""


new_data = data.replace(" ", "").replace("(", "").replace(")", "")
instructions, nodes = new_data.split("\n\n")
instructions = [1 if i == "R" else 0 for i in instructions]

result = {}
position = "AAA"
steps = 0

p2_start_positions = []

for node in nodes.split("\n"):
    a, b = node.split("=")
    result[a] = tuple(b.split(","))

    if a.endswith("A"):
        p2_start_positions.append(a)
nodes = result

done = False
while not done:
    for instruction in instructions:
        position = nodes[position][instruction]
        steps += 1

        if position == "ZZZ":
            print(steps)
            done = True
            break

paths = [0 for i in p2_start_positions]
skip = [False for i in p2_start_positions]

counter = 0
done = False
while not done:
    for instruction in instructions:
        steps += 1
        for x, p2_start_position in enumerate(p2_start_positions):
            if skip[x]:
                continue

            p2_start_positions[x] = nodes[p2_start_position][instruction]

            paths[x] += 1

            if p2_start_positions[x].endswith("Z"):
                skip[x] = True

        if all(skip):
            done = True
            break

import math

print(math.lcm(*paths))
