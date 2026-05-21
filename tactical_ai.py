from config import *

import random


class TacticalAI:

    def __init__(self, engine):

        self.engine = engine

    def get_move(self):

        valid_moves = self.get_valid_moves()

        best_score = -999999

        best_move = random.choice(valid_moves)

        for r, c in valid_moves:

            score = self.evaluate_move(r, c)

            if score > best_score:

                best_score = score

                best_move = (r, c)

        return best_move

    def get_valid_moves(self):

        moves = []

        for r in range(self.engine.board_size):
            for c in range(self.engine.board_size):

                if self.engine.can_place(r, c):

                    moves.append((r, c))

        return moves

    def evaluate_move(self, row, col):

        score = 0

        center = self.engine.board_size // 2

        # 중앙 선호
        score += (
            20
            - (
                abs(row - center)
                + abs(col - center)
            )
        )

        # =========================
        # 공격 점수
        # =========================

        self.engine.board[row][col] = WHITE

        attack = self.evaluate_patterns(
            row,
            col,
            WHITE
        )

        self.engine.board[row][col] = EMPTY

        # =========================
        # 수비 점수
        # =========================

        self.engine.board[row][col] = BLACK

        defense = self.evaluate_patterns(
            row,
            col,
            BLACK
        )

        self.engine.board[row][col] = EMPTY

        score += attack * 1.2
        score += defense * 1.5

        return score

    def evaluate_patterns(
        self,
        row,
        col,
        player
    ):

        total = 0

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dr, dc in directions:

            count, open_ends = (
                self.count_line(
                    row,
                    col,
                    dr,
                    dc,
                    player
                )
            )

            # 5목
            if count >= 5:

                total += 100000

            # 열린 4
            elif count == 4 and open_ends == 2:

                total += 20000

            # 막힌 4
            elif count == 4 and open_ends == 1:

                total += 10000

            # 열린 3
            elif count == 3 and open_ends == 2:

                total += 5000

            # 막힌 3
            elif count == 3 and open_ends == 1:

                total += 1000

            # 열린 2
            elif count == 2 and open_ends == 2:

                total += 300

        return total

    def count_line(
        self,
        row,
        col,
        dr,
        dc,
        player
    ):

        count = 1

        open_ends = 0

        r = row + dr
        c = col + dc

        while (
            self.engine.in_range(r, c)
            and
            self.engine.board[r][c] == player
        ):

            count += 1

            r += dr
            c += dc

        if (
            self.engine.in_range(r, c)
            and
            self.engine.board[r][c] == EMPTY
        ):

            open_ends += 1

        r = row - dr
        c = col - dc

        while (
            self.engine.in_range(r, c)
            and
            self.engine.board[r][c] == player
        ):

            count += 1

            r -= dr
            c -= dc

        if (
            self.engine.in_range(r, c)
            and
            self.engine.board[r][c] == EMPTY
        ):

            open_ends += 1

        return count, open_ends