class CGXFormatter:
    open = ('{', '[')
    close = ('}', ']')
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
    CGXFormatter.from_str("""[['dat', 'data-tracking="categories-top-in">in:'], 'Mods, HullAbsorptionEdit', ['li', 'Edit source', 'History', 'Talk (0)'], ['dat', 'Comments'], ['dat', 'Share'], ['p', 'Mods\\xe2\\x97\\x86Absorption\n', ['h2', 'Absorption(click on the icons to navigate)'], ['url', 'https://static.wikia.nocookie.net/nova-drift/images/d/db/Absorption.png/revision/latest/scale-to-width-down/100?cb=20191011021253'], ['url', 'https://static.wikia.nocookie.net/nova-drift/images/1/19/Emp.png/revision/latest/scale-to-width-down/80?cb=20200117130753'], ['url', 'https://static.wikia.nocookie.net/nova-drift/images/0/07/Juggernaut.png/revision/latest/scale-to-width-down/100?cb=20191011023057'], ['url', 'https://static.wikia.nocookie.net/nova-drift/images/8/8d/ArBotL.png/revision/latest/scale-to-width-down/80?cb=20200117155549'], ['url', 'https://static.wikia.nocookie.net/nova-drift/images/d/de/Force_Armor.png/revision/latest/scale-to-width-down/100?cb=20191011022520'], ['url', 'https://static.wikia.nocookie.net/nova-drift/images/c/cc/ArBotR.png/revision/latest/scale-to-width-down/80?cb=20200117155459'], ['dat', 'Last Update - Patch'], ['dat', 'V0.30.5'], ['dat', 'Stats / Tags'], ['dat', 'Edit']], ['h2', 'Contents'], ['li', '1Stats', '2Unlocked From', '3Unlocks', '4Tags'], ['h2', 'Stats[edit | edit source]'], ['li', '+3 plating', 'Plating reduces hull damage taken by a flat value, providing protection against rapid light damage', 'Plating cannot reduce burn damage or self-damage, and it cannot reduce damage below 1'], ['h2', 'Unlocked From[edit | edit source]'], ['li', 'Hull Strength'], ['h2', 'Unlocks[edit | edit source]'], ['li', 'Force Armor', 'Super Mod: Rancor (with Charged Shot)'], ['h2', 'Tags[edit | edit source]'], ['li', 'Hull']]
""").print()