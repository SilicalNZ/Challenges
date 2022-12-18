data = """"""


class Monkey:
    def __init__(self, id, items, operation, test, if_true, if_false):
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspects = 0

    @classmethod
    def grasp(cls, text):
        monkey, items, operation, test, if_true, if_false = text.split("\n")

        id = monkey.split(" ")[-1][:-1]
        items = [*map(int, items.split(": ")[-1].split(", "))]
        operation = operation.split(": ")[-1].split(" ")[2:]
        test = int(test.split(": ")[-1].split(" ")[-1])
        if_true = int(if_true.split(": ")[-1].split(" ")[-1])
        if_false = int(if_false.split(": ")[-1].split(" ")[-1])

        f0, opr, f1 = operation

        if opr == "*":
            opr = lambda x, y: x * y
        elif opr == "+":
            opr = lambda x, y: x + y
        elif opr == "+":
            opr = lambda x, y: x / y
        elif opr == "-":
            opr = lambda x, y: x - y
        else:
            raise AssertionError("unknown operator")

        if f0 == 'old' and f1 == 'old':
            operation = lambda x: opr(x, x)
        elif f0 == 'old' and f1.isdigit():
            y = int(f1)
            operation = lambda x: opr(x, y)
        elif f0.isdigit() and f1 == 'old':
            y = int(f0)
            operation = lambda x: opr(y, x)

        return cls(id, items, operation, test, if_true, if_false)

    @classmethod
    def grasp_all(cls, text):
        return [*map(cls.grasp, text.split("\n\n"))]

    def turn(self, monkeys, part1, stupid_math_thingy):
        for item in self.items:
            self.inspects += 1

            item = self.operation(item)

            if part1:
                item //= 3

            if item % self.test == 0:
                monkeys[self.if_true].items.append(item % stupid_math_thingy)
            else:
                monkeys[self.if_false].items.append(item % stupid_math_thingy)
        self.items = []


monkeys = Monkey.grasp_all(data)

stupid_math_thingy = 1
for monkey in monkeys:
    stupid_math_thingy *= monkey.test

for i in range(10000):
    for monkey in monkeys:
        monkey.turn(monkeys, False, stupid_math_thingy)

inspects = [monkey.inspects for monkey in monkeys]
inspects.sort()
print(inspects[-1] * inspects[-2])
