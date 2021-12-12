data = ""
data = data.split("\n")

close = {'(': ')', '{': '}', '[': ']', '<': '>'}
open = {value: key for key, value in close.items()}

points = {')': 3, ']': 57, '}': 1197,'>': 25137}


def extractor(row):
    pre = []
    for x, j in enumerate(row):
        for char in j:
            if char in open and close[pre[-1]] == char:
                pre.pop(-1)
            elif char in close:
                pre.append(char)
            else:
                return char


results = [j for j in [extractor(i) for i in data] if j is not None]
print(results)
