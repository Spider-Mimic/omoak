import numpy as np


EMPTY = 0
BLACK = 1
WHITE = 2


class OmokEngine:

    # 초기 설정
    def __init__(self, board_size=20):

        self.board_size = board_size

        self.reset()

    # 게임 초기화
    def reset(self):

        self.board = np.zeros(
            (self.board_size, self.board_size),
            dtype=int
        )

        self.current_player = BLACK

        self.is_over = False

        self.winner = None

    # 범위 검사
    def in_range(self, r, c):

        return (
            0 <= r < self.board_size and
            0 <= c < self.board_size
        )

    # 무승부 검사
    def is_board_full(self):

        return not np.any(self.board == EMPTY)

    # 착수 가능 여부
    def can_place(self, row, col):

        # 범위 밖
        if not self.in_range(row, col):
            return False

        # 이미 돌 존재
        if self.board[row][col] != EMPTY:
            return False

        # 게임 종료
        if self.is_over:
            return False

        # 흑돌만 금수 적용
        if self.current_player == BLACK:

            # 임시 착수
            self.board[row][col] = BLACK

            # 33 검사
            if self.is_double_three(row, col):

                self.board[row][col] = EMPTY

                return False

            # 장목 검사
            if self.is_overline(row, col):

                self.board[row][col] = EMPTY

                return False

            # 원상복구
            self.board[row][col] = EMPTY

        return True

    # 돌 놓기
    def make_move(self, row, col):

        # 착수 불가능
        if not self.can_place(row, col):
            return False

        # 돌 배치
        self.board[row][col] = self.current_player

        # 승리 검사
        if self.check_win(row, col):

            self.is_over = True

            self.winner = self.current_player

        # 무승부
        elif self.is_board_full():

            self.is_over = True

            self.winner = 0

        else:

            # 턴 교체
            if self.current_player == BLACK:
                self.current_player = WHITE
            else:
                self.current_player = BLACK

        return True

    # 승리 검사
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

            # 정방향
            r = row + dr
            c = col + dc

            while (
                self.in_range(r, c) and
                self.board[r][c] == player
            ):

                count += 1

                r += dr
                c += dc

            # 역방향
            r = row - dr
            c = col - dc

            while (
                self.in_range(r, c) and
                self.board[r][c] == player
            ):

                count += 1

                r -= dr
                c -= dc

            # 흑은 정확히 5목만
            if player == BLACK:

                if count == 5:
                    return True

            # 백은 5목 이상 가능
            else:

                if count >= 5:
                    return True

        return False

    # 장목 검사
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

            # 정방향
            r = row + dr
            c = col + dc

            while (
                self.in_range(r, c) and
                self.board[r][c] == player
            ):

                count += 1

                r += dr
                c += dc

            # 역방향
            r = row - dr
            c = col - dc

            while (
                self.in_range(r, c) and
                self.board[r][c] == player
            ):

                count += 1

                r -= dr
                c -= dc

            # 6목 이상
            if count >= 6:
                return True

        return False

    # 33 검사
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

    # 열린3 검사
    def is_open_three(self, row, col, dr, dc):

        line = ""

        # 중심 기준 9칸 검사
        for i in range(-4, 5):

            nr = row + dr * i
            nc = col + dc * i

            # 벽
            if not self.in_range(nr, nc):

                line += "X"

            else:

                value = self.board[nr][nc]

                # 빈칸
                if value == EMPTY:
                    line += "."

                # 흑돌
                elif value == BLACK:
                    line += "O"

                # 백돌
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