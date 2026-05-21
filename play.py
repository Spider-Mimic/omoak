import pygame
import sys
import torch
import numpy as np

from omok_engine import *
from tactical_ai import TacticalAI
from ppo_agent import PPOAgent

from config import *


pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "오목 Hybrid AI"
)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "malgungothic",
    40
)

engine = OmokEngine()

tactical_ai = TacticalAI(engine)

ai = PPOAgent()

try:

    ai.policy.load_state_dict(
        torch.load("ppo_omok.pth")
    )

    ai.policy_old.load_state_dict(
        ai.policy.state_dict()
    )

    print("AI 모델 로드 완료")

except:

    print("학습 모델 없음")

ai.policy.eval()


def get_valid_moves():

    moves = []

    for r in range(engine.board_size):
        for c in range(engine.board_size):

            if engine.can_place(r, c):
                moves.append((r, c))

    return moves


def get_ai_move():

    valid_moves = get_valid_moves()

    # =========================
    # TacticalAI 우선
    # =========================

    tactical_move = tactical_ai.get_move()

    # 전술 점수가 충분히 높으면 사용
    score = tactical_ai.evaluate_move(
        tactical_move[0],
        tactical_move[1]
    )

    if score >= 5000:

        return tactical_move

    # =========================
    # PPO 판단
    # =========================

    state = (
        engine.board
        .copy()
        .astype(np.float32)
    )

    state = np.expand_dims(
        state,
        axis=0
    )

    state = torch.FloatTensor(
        state
    ).unsqueeze(0)

    probs, _ = ai.policy(state)

    probs = (
        probs
        .detach()
        .numpy()
        .flatten()
    )

    mask = np.zeros(
        BOARD_SIZE * BOARD_SIZE
    )

    for r, c in valid_moves:

        mask[
            r * BOARD_SIZE + c
        ] = 1

    probs = probs * mask

    if probs.sum() == 0:

        return tactical_move

    probs = probs / probs.sum()

    action = np.argmax(probs)

    row = action // BOARD_SIZE
    col = action % BOARD_SIZE

    return row, col


def draw_board():

    screen.fill(COLOR_BOARD)

    for i in range(BOARD_SIZE):

        pygame.draw.line(
            screen,
            COLOR_GRID,

            (PADDING, PADDING + i * CELL_SIZE),

            (
                PADDING + (BOARD_SIZE - 1)
                * CELL_SIZE,

                PADDING + i * CELL_SIZE
            ),

            2
        )

        pygame.draw.line(
            screen,
            COLOR_GRID,

            (
                PADDING + i * CELL_SIZE,
                PADDING
            ),

            (
                PADDING + i * CELL_SIZE,

                PADDING
                + (BOARD_SIZE - 1)
                * CELL_SIZE
            ),

            2
        )


def draw_stones():

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            x = PADDING + c * CELL_SIZE
            y = PADDING + r * CELL_SIZE

            if engine.board[r][c] == BLACK:

                pygame.draw.circle(
                    screen,
                    COLOR_BLACK,
                    (x, y),
                    CELL_SIZE // 2 - 2
                )

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


def draw_result():

    if not engine.is_over:
        return

    if engine.winner == BLACK:

        text = "플레이어 승리"

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


while True:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and
            not engine.is_over
            and
            engine.current_player
            == BLACK
        ):

            mouse_x, mouse_y = (
                pygame.mouse.get_pos()
            )

            col = round(
                (mouse_x - PADDING)
                / CELL_SIZE
            )

            row = round(
                (mouse_y - PADDING)
                / CELL_SIZE
            )

            moved = engine.make_move(
                row,
                col
            )

            if moved and not engine.is_over:

                ai_row, ai_col = (
                    get_ai_move()
                )

                engine.make_move(
                    ai_row,
                    ai_col
                )

    draw_board()

    draw_stones()

    draw_result()

    pygame.display.update()