import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# =========================
# Memory
# =========================
class Memory:
    def __init__(self):
        self.states = []
        self.actions = []
        self.logprobs = []
        self.rewards = []
        self.is_terminals = []


# =========================
# PPO Network (간단 버전)
# =========================
class ActorCritic(nn.Module):
    def __init__(self, board_size):
        super().__init__()

        self.board_size = board_size
        input_size = board_size * board_size

        self.actor = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, input_size)
        )

        self.critic = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)

        logits = self.actor(x)
        value = self.critic(x)

        probs = torch.softmax(logits, dim=-1)

        return probs, value


# =========================
# PPO Agent
# =========================
class PPOAgent:
    def __init__(self, board_size=20):

        self.board_size = board_size

        self.policy = ActorCritic(board_size)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=0.001)

        self.policy_old = ActorCritic(board_size)
        self.policy_old.load_state_dict(self.policy.state_dict())

        self.mse = nn.MSELoss()

        self.gamma = 0.99

    def select_action(self, state, valid_moves, memory):

        state = torch.FloatTensor(state).unsqueeze(0)

        probs, _ = self.policy_old(state)
        probs = probs.detach().cpu().numpy().flatten()

        mask = np.zeros(self.board_size * self.board_size)

        for r, c in valid_moves:
            mask[r * self.board_size + c] = 1

        probs = probs * mask

        if probs.sum() == 0:
            probs = mask

        probs = probs / probs.sum()

        action = np.random.choice(len(probs), p=probs)

        memory.states.append(state)
        memory.actions.append(action)
        memory.logprobs.append(probs[action])

        return action

    def update(self, memory):

        rewards = []

        discounted = 0

        for r, done in zip(reversed(memory.rewards), reversed(memory.is_terminals)):
            if done:
                discounted = 0
            discounted = r + self.gamma * discounted
            rewards.insert(0, discounted)

        rewards = torch.tensor(rewards, dtype=torch.float32)

        states = torch.cat(memory.states)

        old_actions = torch.tensor(memory.actions)

        probs, values = self.policy(states)
        values = values.squeeze()

        advantage = rewards - values.detach()

        loss = (values - rewards).pow(2).mean()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.policy_old.load_state_dict(self.policy.state_dict())

        memory.states = []
        memory.actions = []
        memory.rewards = []
        memory.is_terminals = []
        memory.logprobs = []