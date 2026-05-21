import torch
import torch.nn as nn
import torch.nn.functional as F

from config import *


class PPOModel(nn.Module):

    def __init__(self):

        super().__init__()

        self.conv_block = nn.Sequential(

            nn.Conv2d(
                1,
                64,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            nn.Conv2d(
                64,
                128,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            nn.Conv2d(
                128,
                128,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU()
        )

        self.flatten_size = (
            128
            * BOARD_SIZE
            * BOARD_SIZE
        )

        self.actor = nn.Sequential(

            nn.Linear(
                self.flatten_size,
                512
            ),

            nn.ReLU(),

            nn.Linear(
                512,
                BOARD_SIZE * BOARD_SIZE
            )
        )

        self.critic = nn.Sequential(

            nn.Linear(
                self.flatten_size,
                512
            ),

            nn.ReLU(),

            nn.Linear(
                512,
                1
            )
        )

    def forward(self, x):

        x = self.conv_block(x)

        x = x.view(x.size(0), -1)

        logits = self.actor(x)

        probs = F.softmax(
            logits,
            dim=-1
        )

        value = self.critic(x)

        return probs, value