"""Simple Awalé

    Goal
Awalé is an african 2 players game consisting of moving grains in some bowls. Each player has 7 bowls indexed from 0 to 6. The last bowl is the reserve.

At each turn a player chooses one of his own bowls except the reserve, picks up all grains there and redistributes them one by one to bowls beginning just after the chosen one. If the number of grains in hand is sufficient, after adding one to his reserve the player continues the distribution in the opponent's bowls excluding his reserve and then back in his own bowls, until his hand is empty.

If the final grain is distributed to the player's reserve, he is allowed to play again.

Examples

bowls num : 0 1 2 3 4 5  6
--------------------------
opp bowls : 5 1 0 6 2 2 [3]
 my bowls : 3 4 0 3 3 2 [2]


I play bowl 0: distribute 3 grains in bowl 1, 2 and 3
bowls num : 0 1 2 3 4 5  6
--------------------------
opp bowls : 5 1 0 6 2 2 [3]
 my bowls : 0 5 1 4 3 2 [2]


I play bowl 5: distribute 2 grains (1 in my reserve and 1 in the first opponent bowl)
bowls num : 0 1 2 3 4 5  6
--------------------------
opp bowls : 6 1 0 6 2 2 [3]
 my bowls : 3 4 0 3 3 0 [3]


If I end in my reserve I can replay:
I play bowl 3:
bowls num : 0 1 2 3 4 5  6
--------------------------
opp bowls : 5 1 0 6 2 2 [3]
 my bowls : 3 4 0 0 4 3 [3]
REPLAY


Your goal is to simulate your turn of game. Given the numbers of grains in each bowl and the num of the chosen bowl your program has to display the new situation and the string REPLAY if the player has a chance to play again. Print the numbers of grains of opponent bowls separated by space, then yours. Put reserve counts between brackets.

Remember that the player always skips the opponent's reserve when distributing!
"""
import sys


class Mancala7(object):
    def __init__(self):
        self.boards = [self.create_board(), self.create_board()]

    @staticmethod
    def create_board(length: int=6, pebbles: int=4):
        return [pebbles for _ in range(length)].append(0)

    def make_move(self, board: int, pos: int, _pebbles=None):
        """lol what a mess"""
        if (board < len(self.boards)) and (pos < len(self.boards[board])):
            upper_limit = False
            if _pebbles is None:
                upper_limit = True
                next_board = abs(board - 1)
                op_points = self.boards[next_board][-1]
                self.boards[next_board] = self.boards[next_board][:-1]

                _pebbles = self.boards[board][pos]
                self.boards[board][pos] = 0
                pos += 1

            x = 0
            for x, i in enumerate(range(pos, len(self.boards[board])), 1):
                if x <= _pebbles:
                    self.boards[board][i] += 1
                else:
                    break

            remaining_pebbles = _pebbles - x
            if remaining_pebbles > 0:
                self.make_move(abs(board - 1), 0, remaining_pebbles)
            elif remaining_pebbles < 0:
                pass
            else:
                if upper_limit:
                    self.boards[next_board].append(op_points)
                return "REPLAY"

            if upper_limit:
                self.boards[next_board].append(op_points)
            return


    def show(self):
        def convert(lst):
            lst[-1] = f"[{str(lst[-1])}]"
            return [str(i) for i in lst]
        return ' '.join(convert(self.boards[0])) + '\n' + ' '.join(convert(self.boards[1]))


op_bowls = [int(i) for i in input().split(' ')]
my_bowls = [int(i) for i in input().split(' ')]
num = int(input())

this = Mancala7()
this.boards = [op_bowls, my_bowls]
result = this.make_move(1, num)
print(this.show())
if result:
    print(result)