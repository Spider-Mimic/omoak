import torch
import torch.nn as nn
import torch.nn.functional as F


class PPOModel(nn.Module):

    # =========================
    # 초기 설정
    # =========================

    def __init__(self, board_size=20):

        super(PPOModel, self).__init__()

        self.board_size = board_size

        # =========================
        # CNN 블록
        # =========================

        self.conv_block = nn.Sequential(

            # 1 x 20 x 20
            nn.Conv2d(
                in_channels=1,
                out_channels=64,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            # 64 x 20 x 20
            nn.Conv2d(
                in_channels=64,
                out_channels=128,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            # 128 x 20 x 20
            nn.Conv2d(
                in_channels=128,
                out_channels=128,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU()
        )

        # =========================
        # Flatten 크기
        # =========================

        self.flatten_size = (
            128
            * board_size
            * board_size
        )

        # =========================
        # Actor
        # =========================

        self.actor = nn.Sequential(

            nn.Linear(
                self.flatten_size,
                512
            ),

            nn.ReLU(),

            nn.Linear(
                512,
                board_size * board_size
            )
        )

        # =========================
        # Critic
        # =========================

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

    # =========================
    # 순전파
    # =========================

    def forward(self, x):

        # CNN 통과
        x = self.conv_block(x)

        # Flatten
        x = x.view(x.size(0), -1)

        # Actor
        logits = self.actor(x)

        probs = F.softmax(
            logits,
            dim=-1
        )

        # Critic
        value = self.critic(x)

        return probs, value