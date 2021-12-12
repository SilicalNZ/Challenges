data = ""

result = []
for i in data.split("\n"):
    x, y = tuple(i.split(" "))
    result.append((x, int(y)))

aim, depth, horizontal = 0, 0, 0
for i in result:
    print(i, aim, depth, horizontal)
    if i[0] == 'forward':
        horizontal += i[1]
        depth += i[1] * aim
    elif i[0] == 'down':
        aim += i[1]
    elif i[0] == 'up':
        aim -= i[1]

print(aim, depth, horizontal)
print(horizontal * depth)
