import random

from omok_engine import *


class TacticalAI:

    def __init__(self, engine):
        self.engine = engine

    # =========================
    # AI 행동 결정
    # =========================

    def get_move(self):

        valid_moves = self.get_valid_moves()

        # 1. 즉시 승리 가능하면 승리
        for r, c in valid_moves:
            self.engine.board[r][c] = WHITE
            if self.engine.check_win(r, c):
                self.engine.board[r][c] = EMPTY
                return r, c
            self.engine.board[r][c] = EMPTY

        # 2. 상대 즉시 승리 방어
        for r, c in valid_moves:
            self.engine.board[r][c] = BLACK
            if self.engine.check_win(r, c):
                self.engine.board[r][c] = EMPTY
                return r, c
            self.engine.board[r][c] = EMPTY

        # 3. 가장 점수 높은 곳 선택
        best_score = -999999
        best_moves = []

        for r, c in valid_moves:
            score = self.evaluate_position(r, c)

            if score > best_score:
                best_score = score
                best_moves = [(r, c)]
            elif score == best_score:
                best_moves.append((r, c))

        # 같은 점수면 랜덤
        return random.choice(best_moves) if best_moves else None

    # 가능한 수 찾기
    def get_valid_moves(self):
        moves = []
        for r in range(self.engine.board_size):
            for c in range(self.engine.board_size):
                if self.engine.can_place(r, c):
                    moves.append((r, c))
        return moves

    # 자리 평가 
    def evaluate_position(self, row, col):
        total_score = 0
        directions = [
            (0, 1), # 가로
            (1, 0), # 세로
            (1, 1), # 대각선 오아
            (1, -1) # 대각선 왼아
        ]

        # 중앙을 선호하도록 기본 점수
        center = self.engine.board_size // 2
        dist = abs(row - center) + abs(col - center)
        total_score += (self.engine.board_size * 2 - dist)

        # 주변 돌의 위협도/공격도 계산
        for dr, dc in directions:
            # 백돌점수
            total_score += self.get_line_score(row, col, dr, dc, WHITE) * 1.1
            # 흑돌점수
            total_score += self.get_line_score(row, col, dr, dc, BLACK) * 1.0

        return total_score

    # 연결된 돌 개수 계산
    def get_line_score(self, row, col, dr, dc, player):
        count = 0
        open_ends = 0

        # 정방향 탐색
        r = row + dr
        c = col + dc
        while self.engine.in_range(r, c) and self.engine.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # 끝이 비어있는지 확인
        if self.engine.in_range(r, c) and self.engine.board[r][c] == EMPTY:
            open_ends += 1

        # 역방향 탐색
        r = row - dr
        c = col - dc
        while self.engine.in_range(r, c) and self.engine.board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
            
        # 끝이 비어있는지 확인
        if self.engine.in_range(r, c) and self.engine.board[r][c] == EMPTY:
            open_ends += 1

        # 패턴에 따른 점수
        if count >= 4:
            return 100000  
            
        elif count == 3:
            if open_ends == 2:
                return 10000 # 양쪽이 열린 3목 (제일 위험해요! 꼭 막아야 해!)
            elif open_ends == 1:
                return 1000 # 한쪽만 열린 3목
                
        elif count == 2:
            if open_ends == 2:
                return 100 # 양쪽이 열린 2목
            elif open_ends == 1:
                return 10 # 한쪽만 열린 2목
                
        elif count == 1:
            if open_ends == 2:
                return 2
            elif open_ends == 1:
                return 1

        return 0