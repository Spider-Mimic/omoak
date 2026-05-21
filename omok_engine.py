import numpy as np

from config import *


class OmokEngine:

    def __init__(self):

        self.board_size = BOARD_SIZE

        self.reset()

    def reset(self):

        self.board = np.zeros(
            (self.board_size, self.board_size),
            dtype=int
        )

        self.current_player = BLACK

        self.is_over = False

        self.winner = None

    def in_range(self, r, c):

        return (
            0 <= r < self.board_size
            and
            0 <= c < self.board_size
        )

    def is_board_full(self):

        return not np.any(self.board == EMPTY)

    def can_place(self, row, col):

        if not self.in_range(row, col):
            return False

        if self.board[row][col] != EMPTY:
            return False

        if self.is_over:
            return False

        if self.current_player == BLACK:

            self.board[row][col] = BLACK

            if self.is_double_three(row, col):

                self.board[row][col] = EMPTY

                return False

            if self.is_overline(row, col):

                self.board[row][col] = EMPTY

                return False

            self.board[row][col] = EMPTY

        return True

    def make_move(self, row, col):

        if not self.can_place(row, col):
            return False

        self.board[row][col] = self.current_player

        if self.check_win(row, col):

            self.is_over = True

            self.winner = self.current_player

        elif self.is_board_full():

            self.is_over = True

            self.winner = 0

        else:

            self.current_player = (
                WHITE
                if self.current_player == BLACK
                else BLACK
            )

        return True

    def check_win(self, row, col):

        player = self.board[row][col]

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dr, dc in directions:

            count = 1

            r = row + dr
            c = col + dc

            while (
                self.in_range(r, c)
                and
                self.board[r][c] == player
            ):

                count += 1

                r += dr
                c += dc

            r = row - dr
            c = col - dc

            while (
                self.in_range(r, c)
                and
                self.board[r][c] == player
            ):

                count += 1

                r -= dr
                c -= dc

            if player == BLACK:

                if count == 5:
                    return True

            else:

                if count >= 5:
                    return True

        return False

    def is_overline(self, row, col):

        player = self.board[row][col]

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dr, dc in directions:

            count = 1

            r = row + dr
            c = col + dc

            while (
                self.in_range(r, c)
                and
                self.board[r][c] == player
            ):

                count += 1

                r += dr
                c += dc

            r = row - dr
            c = col - dc

            while (
                self.in_range(r, c)
                and
                self.board[r][c] == player
            ):

                count += 1

                r -= dr
                c -= dc

            if count >= 6:
                return True

        return False

    def is_double_three(self, row, col):

        open_three_count = 0

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dr, dc in directions:

            if self.is_open_three(row, col, dr, dc):

                open_three_count += 1

        return open_three_count >= 2

    def is_open_three(self, row, col, dr, dc):

        line = ""

        for i in range(-4, 5):

            nr = row + dr * i
            nc = col + dc * i

            if not self.in_range(nr, nc):

                line += "X"

            else:

                value = self.board[nr][nc]

                if value == EMPTY:
                    line += "."

                elif value == BLACK:
                    line += "O"

                else:
                    line += "X"

        patterns = [
            ".OOO.",
            ".OO.O.",
            ".O.OO."
        ]

        for pattern in patterns:

            if pattern in line:
                return True

        return False