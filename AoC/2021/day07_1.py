data = ""
data = tuple(tuple(list("".join(sorted(list(k))) for k in j.split(" ")) for j in i.split(" | ")) for i in data.split("\n"))


class NumberDisplays:
    def __init__(self, data):
        self.data = data
        self.display = [None, None, None, None, None, None, None]
        self.numbers = [None, None, None, None, None, None, None, None, None, None]

    def _find(self, number):
        for x, i in enumerate(self.data):
            if len(i) == number:
                self.data.pop(x)
                return i

    def find_zero(self):
        if self.numbers[0]:
            return self.numbers[0]

        remainders = []
        for i in self.find_four():
            if i not in self.find_one():
                remainders.append(i)

        for x, i in enumerate(self.data):
            if len(i) == 6 and remainders[0] in i and remainders[1] not in i:
                self.display[1] = remainders[0]
                self.display[3] = remainders[1]
                self.data.pop(x)
                self.numbers[0] = i
                return i
            elif len(i) == 6 and remainders[1] in i and remainders[0] not in i:
                self.display[1] = remainders[1]
                self.display[3] = remainders[0]
                self.data.pop(x)
                self.numbers[0] = i
                return i

    def find_one(self):
        if self.numbers[1]:
            return self.numbers[1]

        result = self._find(2)
        self.numbers[1] = result
        return result

    def find_two(self):
        if self.numbers[2]:
            return self.numbers[2]

        for x, i in enumerate(self.data):
            if self.find_third() in i:
                for letter in i:
                    if letter not in self.display:
                        self.display[4] = letter

                self.numbers[2] = i
                self.data.pop(x)
                return i

    def find_three(self):
        if self.numbers[3]:
            return self.numbers[3]

        self.find_nine()

        for x, i in enumerate(self.data):
            if self.find_third() in i and self.find_sixth() in i:
                self.numbers[3] = i
                self.data.pop(x)

                return i

    def find_four(self):
        if self.numbers[4]:
            return self.numbers[4]

        result = self._find(4)
        self.numbers[4] = result
        return result

    def find_five(self):
        if self.numbers[5]:
            return self.numbers[5]

        self.find_two()

        self.numbers[5] = self.data[0]
        self.data.pop(0)
        return self.numbers[5]

    def find_six(self):
        if self.numbers[6]:
            return self.numbers[6]

        for x, i in enumerate(self.data):
            if len(i) == 6 and self.find_one()[0] in i and self.find_one()[1] not in i:
                self.display[5] = self.find_one()[0]
                self.display[2] = self.find_one()[1]
                self.numbers[6] = i
                self.data.pop(x)
                return i
            elif len(i) == 6 and self.find_one()[1] in i and self.find_one()[0] not in i:
                self.display[5] = self.find_one()[1]
                self.display[2] = self.find_one()[0]
                self.numbers[6] = i
                self.data.pop(x)
                return i

    def find_seven(self):
        if self.numbers[7]:
            return self.numbers[7]

        result = self._find(3)
        self.numbers[7] = result

        for letter in result:
            if letter not in self.find_one():
                self.display[0] = letter
        return result

    def find_eight(self):
        if self.numbers[8]:
            return self.numbers[8]

        result = self._find(7)
        self.numbers[8] = result
        return result

    def find_nine(self):
        if self.numbers[9]:
            return self.numbers[9]

        self.find_sixth()

        for x, i in enumerate(self.data):
            if len(i) == 6:
                for letter in i:
                    if letter not in self.display:
                        self.display[6] = letter
                        break
                self.numbers[9] = i
                self.data.pop(x)
                return i

    def find_first(self):
        if self.display[0]:
            return self.display[0]

        for i in self.find_seven():
            if i not in self.find_one():
                self.display[0] = i
                return i

    def find_second(self):
        if self.display[1]:
            return self.display[1]

        self.find_zero()
        return self.find_second()

    def find_third(self):
        if self.display[2]:
            return self.display[2]

        self.find_six()
        return self.find_third()

    def find_fourth(self):
        if self.display[3]:
            return self.display[3]

        self.find_zero()
        return self.find_fourth()

    def find_fifth(self):
        if self.display[4]:
            return self.display[4]

        self.find_two()
        return self.find_fourth()

    def find_sixth(self):
        if self.display[5]:
            return self.display[5]

        self.find_six()
        return self.find_sixth()

    def find_seventh(self):
        if self.display[6]:
            return self.display[6]

        self.find_nine()
        return self.find_seventh()

    def parse(self):
        self.find_one()
        self.find_four()
        self.find_eight()
        self.find_seven()
        self.find_zero()
        self.find_six()
        self.find_nine()
        self.find_three()
        self.find_two()
        self.find_five()
        return self.display, self.numbers

    def display_to_dict(self):
        data = {}

        for x, i in enumerate(self.numbers):
            data[i] = x
        return data


number_displays = []

result = 0
for i, j in data:
    print(i, j)
    number_display = NumberDisplays(i)

    print(number_display.parse())
    converter = number_display.display_to_dict()

    result += int("".join([str(converter[number]) for number in j]))

print(result)