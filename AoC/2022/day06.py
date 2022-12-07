data = """"""

print([next(j + 4 for j in range(len(i) - 4) if len(set(i[j:j+4])) == 4) for i in data.split("\n")][0])
print([next(j + 14 for j in range(len(i) - 14) if len(set(i[j:j+14])) == 14) for i in data.split("\n")][0])
