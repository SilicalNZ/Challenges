import sys


class RPCLS:
    order = {'C': ('P', 'L'),
            'P': ('R', 'S'),
            'R': ('L', 'C'),
            'L': ('S', 'P'),
            'S': ('C', 'R')
            }

    @classmethod
    def beat(cls, one, two):
        return two in cls.order[one]


class Player:
    def __init__(self, id, choice):
        self.id = id
        self.choice = choice
        self.beaten = []

    @property
    def beaten_id(self):
        return ' '.join([str(i.id) for i in self.beaten])

    def battle(self, other):
        result = RPCLS.beat(self.choice, other.choice) or self.choice == other.choice and self.id < other.id
        self.beaten.append(other) if result else other.beaten.append(self)
        return result

    @classmethod
    def from_str(cls, string):
        id, choice = string.split()
        id = int(id)
        return cls(id, choice)

    def __repr__(self):
        return f'{self.id} {self.choice}'


class Tournament:
    def __init__(self, n):
        self.n = n
        self.child = None

    def compete(self):
        return self.battles(*[Player.from_str(input()) for i in range(self.n)])

    def battles(self, *players):
        if len(players) == 1:
            return players[0]
        battles = [players[x:x + 2] for x in range(0, len(players), 2)]
        x = [p1 if p1.battle(p2) else p2 for p1, p2 in battles]
        print(x, file=sys.stderr)
        return self.battles(*x)


winner = Tournament(int(input())).compete()
print(winner.id)
print(winner.beaten_id)