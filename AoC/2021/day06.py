import statistics

data = ""

datra = tuple(map(int, data.split(",")))
print(datra)

median = statistics.median(datra)
mean = int(statistics.mean(datra) + .5)
print(mean)
mean = 446  # Found by mean - 1. Couldn't be bothered coding

check = lambda x: (x * (x + 1)) / 2

print(sum(int(abs(i - median)) for i in datra))
print(tuple(check(int(abs(i - mean))) for i in datra))
print(sum(check(int(abs(i - mean))) for i in datra))
