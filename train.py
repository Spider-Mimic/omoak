import numpy as np
import torch

from omok_engine import OmokEngine
from tactical_ai import TacticalAI

from ppo_agent import (
    PPOAgent,
    Memory
)

from config import *


UPDATE_STEP = 2000


def get_valid_moves(env):

    moves = []

    for r in range(env.board_size):
        for c in range(env.board_size):

            if env.can_place(r, c):
                moves.append((r, c))

    return moves


def train():

    env = OmokEngine()

    enemy_ai = TacticalAI(env)

    agent = PPOAgent()

    memory = Memory()

    step = 0

    for episode in range(1, 100000):

        env.reset()

        while not env.is_over:

            if env.current_player == BLACK:

                state = (
                    env.board
                    .copy()
                    .astype(np.float32)
                )

                state = np.expand_dims(
                    state,
                    axis=0
                )

                valid_moves = (
                    get_valid_moves(env)
                )

                action = agent.select_action(
                    state,
                    valid_moves,
                    memory
                )

                row = action // BOARD_SIZE

                col = action % BOARD_SIZE

                moved = env.make_move(
                    row,
                    col
                )

                if not moved:

                    memory.rewards.append(-1)

                    memory.is_terminals.append(
                        True
                    )

                    break

                if env.is_over:

                    if env.winner == BLACK:
                        reward = 1

                    else:
                        reward = -1

                else:
                    reward = 0

                memory.rewards.append(
                    reward
                )

                memory.is_terminals.append(
                    env.is_over
                )

            else:

                ai_row, ai_col = (
                    enemy_ai.get_move()
                )

                env.make_move(
                    ai_row,
                    ai_col
                )

            step += 1

            if step % UPDATE_STEP == 0:

                agent.update(memory)

        if episode % 100 == 0:

            print(
                f"Episode {episode}"
            )

        if episode % 1000 == 0:

            torch.save(
                agent.policy.state_dict(),
                "ppo_omok.pth"
            )

            print("모델 저장 완료")


if __name__ == "__main__":

    train()