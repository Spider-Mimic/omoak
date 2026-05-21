import torch
import torch.nn as nn
import torch.optim as optim

from torch.distributions import Categorical

from model import PPOModel

from config import *


class Memory:

    def __init__(self):

        self.states = []
        self.actions = []
        self.logprobs = []
        self.rewards = []
        self.is_terminals = []

    def clear(self):

        self.states.clear()
        self.actions.clear()
        self.logprobs.clear()
        self.rewards.clear()
        self.is_terminals.clear()


class PPOAgent:

    def __init__(self):

        self.policy = PPOModel()

        self.policy_old = PPOModel()

        self.policy_old.load_state_dict(
            self.policy.state_dict()
        )

        self.optimizer = optim.Adam(
            self.policy.parameters(),
            lr=0.0003
        )

        self.gamma = 0.99

        self.eps_clip = 0.2

        self.k_epochs = 4

        self.mse_loss = nn.MSELoss()

    def select_action(
        self,
        state,
        valid_moves,
        memory
    ):

        state = torch.FloatTensor(
            state
        ).unsqueeze(0)

        probs, _ = self.policy_old(state)

        probs = probs.squeeze(0)

        mask = torch.zeros(
            BOARD_SIZE * BOARD_SIZE
        )

        for r, c in valid_moves:

            mask[
                r * BOARD_SIZE + c
            ] = 1

        probs = probs * mask

        probs = probs / probs.sum()

        dist = Categorical(probs)

        action = dist.sample()

        memory.states.append(state)

        memory.actions.append(action)

        memory.logprobs.append(
            dist.log_prob(action)
        )

        return action.item()

    def update(self, memory):

        rewards = []

        discounted_reward = 0

        for reward, done in zip(
            reversed(memory.rewards),
            reversed(memory.is_terminals)
        ):

            if done:
                discounted_reward = 0

            discounted_reward = (
                reward
                + self.gamma
                * discounted_reward
            )

            rewards.insert(
                0,
                discounted_reward
            )

        rewards = torch.tensor(
            rewards,
            dtype=torch.float32
        )

        rewards = (
            rewards - rewards.mean()
        ) / (rewards.std() + 1e-5)

        old_states = torch.cat(
            memory.states
        )

        old_actions = torch.stack(
            memory.actions
        )

        old_logprobs = torch.stack(
            memory.logprobs
        )

        for _ in range(self.k_epochs):

            probs, state_values = (
                self.policy(old_states)
            )

            dist = Categorical(probs)

            logprobs = dist.log_prob(
                old_actions
            )

            entropy = dist.entropy()

            ratios = torch.exp(
                logprobs
                - old_logprobs.detach()
            )

            advantages = (
                rewards
                - state_values.detach().squeeze()
            )

            surr1 = ratios * advantages

            surr2 = torch.clamp(
                ratios,
                1 - self.eps_clip,
                1 + self.eps_clip
            ) * advantages

            loss = (
                -torch.min(surr1, surr2)
                + 0.5
                * self.mse_loss(
                    state_values.squeeze(),
                    rewards
                )
                - 0.01 * entropy
            )

            self.optimizer.zero_grad()

            loss.mean().backward()

            self.optimizer.step()

        self.policy_old.load_state_dict(
            self.policy.state_dict()
        )

        memory.clear()