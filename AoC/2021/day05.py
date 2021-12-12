from collections import Counter

data = ""

c = Counter(map(int, data.split(",")))

items = [0] * 9
for key, value in c.items():
    items[key] = value

print(items)


for day in range(256):
    new_items = [0] * 9

    new_items[6] += items[0]
    new_items[8] += items[0]
    items[0] = 0
    for x, item in enumerate(items[1:]):
        new_items[x] += item

    items = new_items
    print(items, new_items)

print(sum(items))
