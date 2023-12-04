data = """"""

res = 0
for i in data.replace("  ", " ").split("\n"):
    a, b = i.split(": ")[-1].split(" | ")
    num = len(set(a.split(" ")).intersection(set(b.split(" "))))
    if num == 0:
        continue
    res += 2**(num-1)

print(res)

res = {i+1: 1 for i in range(len(data.split("\n")))}

for x, i in enumerate(data.replace("  ", " ").split("\n"), 1):
    a, b = i.split(": ")[-1].split(" | ")
    num = len(set(a.split(" ")).intersection(set(b.split(" "))))
    for j in range(num):
        res[x+j+1] += res[x]

print(sum(res.values()))
