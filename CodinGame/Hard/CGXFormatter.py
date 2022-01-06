class CGXFormatter:
    open = ('(', '{', '[')
    close = (')', '}', ']')
    capture_string = False
    exclude = (' ', '\n', '\r', '	')

    def __init__(self):
        self.main = ''
        self.buffer_len = 0

    @property
    def buffer(self):
        return '    ' * self.buffer_len

    def buff(self):
        self.newline()
        self.main += self.buffer

    def nest(self):
        self.buffer_len += 1
        self.buff()

    def unnest(self):
        self.buffer_len -= 1
        self.buff()

    def newline(self):
        if self.main:
            self.main += '\n'

    def clear_empty_lines(self):
        self.main = self.main.replace(f'\n{self.buffer}\n', '\n')
        self.main = self.main.replace(f'\n{self.buffer}    \n', '\n')

    def add(self, other):
        if other == '\'':
            self.capture_string = not self.capture_string
            self.main += other
        elif self.capture_string:
            self.main += other
        elif other in self.open:
            self.buff()
            self.main += other
            self.nest()
        elif other in self.close:
            self.unnest()
            self.main += other
        elif other == ';':
            self.main += other
            self.buff()
        elif other not in self.exclude:
            self.main += other
        self.clear_empty_lines()

    __add__ = add

    @classmethod
    def from_str(cls, str):
        self = cls()
        for i in str:
            self + i
        return self

    def add_line(self, string):
        [*map(self.add, string)]

    def print(self):
        [print(i) for i in self.main.split('\n')]


if __name__ == '__main__':
    formatter = CGXFormatter()
    n = int(input())
    for i in range(n):
        formatter.add_line(input())
    formatter.print()
