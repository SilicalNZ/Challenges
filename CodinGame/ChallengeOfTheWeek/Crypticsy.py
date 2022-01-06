class Elements:
    def __init__(self, seed):
        self.elements = [seed]

    def __contains__(self, item):
        f = filter(lambda x: x == item, self.elements)
        try:
            next(f)
            next(f)
        except StopIteration:
            return False
        else:
            return True

    @property
    def element(self):
        return self.elements[-1]

    def distance(self):
        elements = self.elements[:-1]
        elements.reverse()
        return elements.index(self.element) + 1

    def __iter__(self):
        while True:
            if self.element in self:
                 self.elements.append(self.distance())
            else:
                self.elements.append(0)
            yield self.element


e = Elements(10)
e = iter(e)

print([next(e) for _ in range(0, int(5692))])