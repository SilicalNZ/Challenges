"""Hidden word

    Goal
You are given a grid of letters and a list of words.
Strike the words in the grid. They can be written horizontally, vertically or diagonally, possibly reversed (in any direction) but always in a straight line. Each word is found only once in the grid, although they may overlap.
A few letters will remain unstruck. Write them down, from left to right, top to bottom, and find the secret word.
"""
import sys


class Character(object):
    def __init__(self, letter, x, y):
        self.item = (letter, (x, y))

    def show(self):
        return self.item


class WordSearch(object):
    def __init__(self, grid, words):
        self.grid = grid
        self.words = words
        print(grid, file=sys.stderr)
        print(words, file=sys.stderr)

        self._length = grid.index('\n') + 1

        self.find_words_in(self.alternate_directions(self.categorize()))

    def categorize(self):
        hashed_grid = []
        for index, letter in enumerate(self.grid):
            result = Character(letter, *divmod(index, self._length))
            hashed_grid.append(result)
        return hashed_grid

    def alternate_directions(self, items):
        directions = {'↓': 0, '↘': 1, '↙': -1}
        for direction, val in directions.items():
            new_grid = []
            for x in range(self._length):
                for i in range(x, len(items), self._length + val):
                    new_grid.append(items[i])
                new_grid.append('\n')
            directions[direction] = new_grid

        directions['→'] = items
        directions['←'] = list(reversed(items))
        directions['↑'] = list(reversed(directions['↓']))
        directions['↖'] = list(reversed(directions['↘']))
        directions['↗'] = list(reversed(directions['↙']))

        return directions

    def find_words_in(self, directions):
        scan_obj = list(directions['→'])
        find_words = set(self.words)
        found_words = []
        for direction, items in directions.keys():
            print(direction, file=sys.stderr)
            # Some weird bug, assigning to list fixes it.
            x = [i for i in items]
            string = ''.join([(i.show()[0] if i != '\n' else i) for i in items])
            find_words -= set(found_words)
            found_words = []
            for word in find_words:
                if word in string:
                    print(word, file=sys.stderr)
                    found_words.append(word)
                    location = string.index(word)
                    for i in range(location, location + len(word)):
                        try:
                            scan_obj.remove(x[i])
                        except ValueError:
                            continue

        scan_obj = [i.show()[0] for i in scan_obj]
        print(''.join([i for i in scan_obj if i != '\n']))


# Words to find
n = int(input())
words = [input() for i in range(n)]

# Height and width of word search grid
h, w = [int(i) for i in input().split()]

# Assembles \n seperated string
grid = ''
for i in range(h):
    grid += '{}\n'.format(input())

WordSearch(grid, words)
