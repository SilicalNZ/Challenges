from functools import wraps

def string_assertion(func):
    wraps(func)
    def wrapper(*args, string_assert=True, **kwargs):
        if string_assert:
            return 'true' if func(*args, **kwargs) else 'false'
        else:
            return func(*args, **kwargs)
    return wrapper


class ValidBrackets:
    pairs = {'{': '}', '[': ']', '(': ')'}
    pairs_items = sum(tuple(pairs.items()), ())
    open, closed = zip(*pairs.items())

    def __init__(self, expression: str):    
        self.org_expression = expression
        self.expression = [*expression]
        self._clean_content()

    def _clean_content(self):
        self.expression = [i for i in self.expression if i in self.pairs_items]

    def check(self):
        scanned = []
        for i in self.expression:
            if i in self.open:
                scanned.append(i)
            elif scanned \
              and self.pairs[scanned[-1]] == i:
                scanned.pop()
            else:
                return False
        return len(scanned) == 0


def valid_brackets(expression: str):
    return ValidBrackets(expression).check()


if __name__ == '__main__':
    print(valid_brackets(input()))

