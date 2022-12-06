import itertools
import string

data = """"""


chars = string.ascii_letters


def split_every(iterable, n):
    """Return a list of lists n long from iterable"""
    i = iter(iterable)
    slice = list(itertools.islice(i, n))
    while slice:
        yield slice
        slice = list(itertools.islice(i, n))


result = 0
for i in split_every(data.split("\n"), 3):
    result += chars.find(set.intersection(*map(set, i)).pop()) + 1

print(result)
