data = """"""

nav = {}
depth = []
[(depth.pop() if j.split(" ")[2] == ".." else depth.append(j.split(" ")[2]) or nav.__setitem__("/".join(depth)[1:], 0)) if j.startswith("$ cd") else nav.__setitem__("/".join(depth)[1:], nav.get("/".join(depth)[1:], 0) + int(j.split(" ")[0])) for j in (i for i in data.split("\n") if not (i.startswith("$ ls") or i.startswith("dir")))]

# Part 1
print(sum(i for i in ((sum(value1 for key1, value1 in ((x, y) for x, y in nav.items() if x.startswith(f"{key0}/"))) + value0) for key0, value0 in nav.items()) if i <= 100000))

# Part 2
result = {key0: (sum(value1 for key1, value1 in ((x, y) for x, y in nav.items() if x.startswith(f"{key0}/"))) + value0) for key0, value0 in nav.items()}
print(next(value for key, value in sorted(result.items(), key=lambda x: x[1]) if value >= 30000000 - (70000000 - result[""])))
