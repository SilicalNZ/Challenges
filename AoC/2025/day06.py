import math
from itertools import zip_longest

data = """"""

print(sum([math.prod(i[:-1]) if i[-1] == "*" else sum(i[:-1]) for i in [[ "".join(j).strip() if n == len(i) else int("".join(j).strip()) for n, j in enumerate(i, 1)] for i in [*zip(*[[j for j in i.split(" ") if j] for i in data.split("\n")])]]]))
grouping = [[]]
[grouping[-1].append(int("".join(i[:-1]).replace(" ", ""))) for i in zip(*data.split("\n")) if (i[-1] != " " and (grouping[-1].append(i[-1]) or True)) or "".join(i).replace(" ", "") != "" or (grouping.append([]) and False)]
print(sum([math.prod(i[1:]) if i[0] == "*" else sum(i[1:]) for i in grouping]))
