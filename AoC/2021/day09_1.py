data = ""
data = data.split("\n")

close = {'(': ')', '{': '}', '[': ']', '<': '>'}
open = {value: key for key, value in close.items()}

other_points = {')': 1, ']': 2, '}': 3, '>': 4}


def extractor(row):
    pre = []
    for x, j in enumerate(row):
        for char in j:
            if char in open and close[pre[-1]] == char:
                pre.pop(-1)
            elif char in close:
                pre.append(char)
            else:
                return None
    return reversed([close[i] for i in pre]) or None


results = [j for j in [extractor(i) for i in data] if j is not None]
numbers = []
for i in results:
    tot = 0
    for j in i:
        tot = tot * 5 + other_points[j]
    numbers.append(tot)

print(results)
print(sorted(numbers)[len(numbers)//2])
