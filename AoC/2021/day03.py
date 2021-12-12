from __future__ import annotations

from typing import List, Tuple
import pprint


data = ""
numbers = ""


class Mark:
    def __str__(self):
        return 'x'

    __repr__ = __str__


base_mark = Mark()


class Board:
    def __init__(self, board: List[List[int]]):
        self.board = board

    def win_condition(self) -> bool:
        return (
            any(all(j == base_mark for j in i) for i in self.board)
            or any(all(j == base_mark for j in i) for i in zip(*self.board))
        )

    def mark(self, number: int):
        for y, j in enumerate(self.board):
            for x, i in enumerate(j):
                if i == number:
                    self.board[y][x] = base_mark

    def stupid_score(self) -> int:
        result = 0
        for j in self.board:
            for i in j:
                if i != base_mark:
                    result += i
        return result

    @classmethod
    def from_individual_board_string(cls, text: str) -> Board:
        board = []
        for row in text.split("\n"):
            board.append([*map(int, filter(lambda x: x, row.split(" ")))])
        return cls(board)

    def __str__(self):
        return pprint.pformat(self.board)

    __repr__ = __str__


class BoardAggregator:
    def __init__(self, boards: List[Board]):
        self.boards = boards
        self.win_conditions = []

    def mark(self, number):
        for board in self.boards:
            board.mark(number)

    def win_condition_occurred(self) -> Tuple[Board, int]:
        for x, board in enumerate(self.boards):
            if board.win_condition():
                yield board, x

    def mark_from_strings_until_win(self, text: str) -> int:
        for number in map(int, text.split(",")):
            self.mark(number)

            for result in self.win_condition_occurred():
                return result[0].stupid_score(), number

    def find_last_win_condition(self, text: str) -> int:
        for number in map(int, text.split(",")):
            self.mark(number)

            for result in self.win_condition_occurred():
                self.win_conditions.append((number, result[0]))
                self.boards.pop(result[1])

    @classmethod
    def from_multiple_board_strings(cls, text: str) -> BoardAggregator:
        result = []
        for board in text.split("\n\n"):
            result.append(Board.from_individual_board_string(board))
        return cls(result)

    def __str__(self):
        return pprint.pformat(self.boards)

    __repr__ = __str__


aggre = BoardAggregator.from_multiple_board_strings(data)
x, y = aggre.mark_from_strings_until_win(numbers)
print(x * y)


result = aggre.find_last_win_condition(numbers)
x, y = aggre.win_conditions[-1]
print(aggre.win_conditions)
print(x, y)
#print(aggre.boards)
print(x * y.stupid_score())