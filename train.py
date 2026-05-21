import numpy as np
import torch

from omok_engine import OmokEngine, BLACK, WHITE
from ppo_agent import PPOAgent, Memory


BOARD_SIZE = 20


def get_valid_moves(env):
    moves = []
    for r in range(env.board_size):
        for c in range(env.board_size):
            if env.can_place(r, c):
                moves.append((r, c))
    return moves


def train():

    env = OmokEngine()
    agent = PPOAgent(BOARD_SIZE)
    memory = Memory()

    # 기존 저장된 모델 불러오기
    try:
        agent.policy.load_state_dict(torch.load("ppo_omok.pth"))
        print("Loaded existing model weights from ppo_omok.pth")
    except FileNotFoundError:
        print("No saved model found, starting fresh.")

    update_step = 2000
    step = 0

    for episode in range(1, 100000):

        env.reset()
        state = env.board.copy().reshape(1, 20, 20).astype(np.float32)

        while not env.is_over:

            step += 1
            valid = get_valid_moves(env)
            action = agent.select_action(state, valid, memory)

            r = action // 20
            c = action % 20

            moved = env.make_move(r, c)

            if not moved:
                memory.rewards.append(-10)
                memory.is_terminals.append(True)
                break

            if env.is_over:
                if env.winner == BLACK:
                    reward = 1
                elif env.winner == WHITE:
                    reward = -1
                else:
                    reward = 0
            else:
                reward = 0

            memory.rewards.append(reward)
            memory.is_terminals.append(env.is_over)

            state = env.board.copy().reshape(1, 20, 20).astype(np.float32)

            if step % update_step == 0:
                agent.update(memory)

        if episode % 100 == 0:
            print(f"Episode {episode}")

        if episode % 1000 == 0:
            torch.save(agent.policy.state_dict(), "ppo_omok.pth")
            print("model saved")


if __name__ == "__main__":
    train()
