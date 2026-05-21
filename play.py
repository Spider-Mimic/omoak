import pygame
import sys

from omok_engine import *
from tactical_ai import TacticalAI


# =========================
# 기본 설정
# =========================

BOARD_SIZE = 20

CELL_SIZE = 40

PADDING = 40

SCREEN_WIDTH = (
    (BOARD_SIZE - 1) * CELL_SIZE
    + (PADDING * 2)
)

SCREEN_HEIGHT = (
    (BOARD_SIZE - 1) * CELL_SIZE
    + (PADDING * 2)
)

FPS = 60


# =========================
# 색상
# =========================

COLOR_BOARD = (193, 154, 107)

COLOR_GRID = (40, 40, 40)

COLOR_BLACK = (35, 35, 35)

COLOR_WHITE = (245, 245, 245)

COLOR_WHITE_BORDER = (180, 180, 180)

COLOR_TEXT = (220, 30, 30)


# =========================
# pygame 시작
# =========================

pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("20x20 오목 AI")

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "malgungothic",
    40
)


# =========================
# 게임 엔진
# =========================

engine = OmokEngine()

ai = TacticalAI(engine)


# =========================
# 바둑판 그리기
# =========================

def draw_board():

    screen.fill(COLOR_BOARD)

    for i in range(BOARD_SIZE):

        # 가로줄
        pygame.draw.line(
            screen,
            COLOR_GRID,

            (PADDING, PADDING + i * CELL_SIZE),

            (
                PADDING + (BOARD_SIZE - 1) * CELL_SIZE,
                PADDING + i * CELL_SIZE
            ),

            2
        )

        # 세로줄
        pygame.draw.line(
            screen,
            COLOR_GRID,

            (PADDING + i * CELL_SIZE, PADDING),

            (
                PADDING + i * CELL_SIZE,
                PADDING + (BOARD_SIZE - 1) * CELL_SIZE
            ),

            2
        )


# =========================
# 돌 그리기
# =========================

def draw_stones():

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            x = PADDING + c * CELL_SIZE
            y = PADDING + r * CELL_SIZE

            # 흑돌
            if engine.board[r][c] == BLACK:

                pygame.draw.circle(
                    screen,
                    COLOR_BLACK,
                    (x, y),
                    CELL_SIZE // 2 - 2
                )

            # 백돌
            elif engine.board[r][c] == WHITE:

                pygame.draw.circle(
                    screen,
                    COLOR_WHITE,
                    (x, y),
                    CELL_SIZE // 2 - 2
                )

                pygame.draw.circle(
                    screen,
                    COLOR_WHITE_BORDER,
                    (x, y),
                    CELL_SIZE // 2 - 2,
                    1
                )


# =========================
# 결과 표시
# =========================

def draw_result():

    if not engine.is_over:
        return

    if engine.winner == BLACK:

        text = "흑 승리"

    elif engine.winner == WHITE:

        text = "AI 승리"

    else:

        text = "무승부"

    image = font.render(
        text,
        True,
        COLOR_TEXT
    )

    screen.blit(image, (20, 20))


# =========================
# 메인 루프
# =========================

while True:

    clock.tick(FPS)

    # =========================
    # 이벤트 처리
    # =========================

    for event in pygame.event.get():

        # 창 닫기
        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

        # =========================
        # 플레이어 턴
        # =========================

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and
            not engine.is_over
            and
            engine.current_player == BLACK
        ):

            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = round(
                (mouse_x - PADDING)
                / CELL_SIZE
            )

            row = round(
                (mouse_y - PADDING)
                / CELL_SIZE
            )

            moved = engine.make_move(row, col)

            # =========================
            # AI 턴
            # =========================

            if (
                moved
                and
                not engine.is_over
            ):

                ai_row, ai_col = ai.get_move()

                engine.make_move(
                    ai_row,
                    ai_col
                )

    # =========================
    # 화면 그리기
    # =========================

    draw_board()

    draw_stones()

    draw_result()

    pygame.display.update()