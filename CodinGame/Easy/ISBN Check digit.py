"""ISBN Check digit

    Goal
International Standard Book Number (ISBN) is a unique numeric commercial book identifier.

Before year 2007 ISBNs were 10-digit long. After that year ISBNs extended to 13 digits. In both ISBN-10 and ISBN-13 standards, the last digit is the check digit, for error detection.

ISBN-10 check digit is calculated by Modulus 11 with decreasing weights on the first 9 digits.
Example: 030640615?
0×10 + 3×9 + 0×8 + 6×7 + 4×6 + 0×5 + 6×4 + 1×3 + 5×2 = 130.
130 / 11 = 11 remainder 9.
Check digit is the value needed to add to the sum to make it dividable by 11. In this case it is 2.
So the valid ISBN is 0306406152.
In case 10 being the value needed to add to the sum, we use X as the check digit instead of 10.

ISBN-13 check digit is calculated by Modulus 10 with alternate weights of 1 and 3 on the first 12 digits.
Example: 978030640615?
9×1 + 7×3 + 8×1 + 0×3 + 3×1 + 0×3 + 6×1 + 4×3 + 0×1 + 6×3 + 1×1 + 5×3 = 93.
93 / 10 = 9 remainder 3.
Check digit is the value needed to add to the sum to make it dividable by 10. So the check digit is 7. The valid ISBN is 9780306406157.

Your task is to validate a list of ISBNs.

A valid ISBN should contain the digits 0 to 9 only, except for the check digit which is determined as explained above. X or other improper characters appearing in the wrong place will render an ISBN invalid.
"""
import sys
import math


def isnumber(num):
    try:
        return int(num)
    except ValueError:
        return False


def int_split(num: int):
    return [int(i) for i in str(num)]


class ISBN:
    """ISBN 10 & 13 Validator"""
    version = '0.1'
    valid = (10, 13)

    def __init__(self, num: str):
        if len(num) not in self.valid:
            raise Exception(f"length of {num} = {len(num)} and not in {self.valid}")

        # check_digit is a valid int
        if num[-1] == 'X' and len(num) == 10:
            self.check_digit = 10
        elif isnumber(num[-1]):
            self.check_digit = int(num[-1])
        elif num[-1] == '0':
            self.check_digit = 0
        else:
            raise Exception("check_digit is not valid")
        num = num[:-1]

        # digits are a valid int
        self.digits = [int(i) for i in num]

    def check(self):
        if len(self.digits) == 12:
            return self.is_standard(10)
        elif len(self.digits) == 9:
            return self.is_standard(11)

    def is_standard(self, func):
        res = getattr(ISBN, f"modulus_{func}")(self.digits)
        res = list(res)
        calc = sum(res) % func
        if calc == 0:
            calc = func
        res = func - calc
        return int(self.check_digit) == res

    @staticmethod
    def modulus_11(num):
        return (i * x for i, x in zip(num, range(10, 1, -1)))

    @staticmethod
    def modulus_10(num, weight1: int = 1, weight2: int = 3):
        return (i * weight1 if x % 2 == 0 else i * weight2 for x, i in enumerate(num))


results = []
for i in range(int(input())):
    num = input()
    print(num, file=sys.stderr)
    try:
        [] if ISBN(num).check() else results.append(num)
    except:
        results.append(num)
print(f"{len(results)} invalid:")
[print(i) for i in results]
