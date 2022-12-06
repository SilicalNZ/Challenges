data = """"""

print([[j + 4 for j in range(len(i) - 4) if len(set(i[j:j+4])) == 4][0] for i in data.split("\n")][0])
print([[j + 14 for j in range(len(i) - 14) if len(set(i[j:j+14])) == 14][0] for i in data.split("\n")][0])
