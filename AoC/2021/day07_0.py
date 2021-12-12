data = ""
check = (2, 3, 4, 7)
counter = 0

for _, y in data:
    for i in y:
        if len(i) in check:
            counter += 1
print(counter)
