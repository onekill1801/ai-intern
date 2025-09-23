import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

from main import init, update, pacman, ghosts, checkFood, checkGhostCollisionFrighten


class PacmanEnvVector(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode

        # Action space: 0 lên, 1 xuống, 2 trái, 3 phải
        self.action_space = spaces.Discrete(4)

        # Observation: vector 16 chiều
        self.observation_space = spaces.Box(
            low=0, high=10000, shape=(16,), dtype=np.float32
        )
        self.prev_score = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        init()
        from main import score
        self.prev_score = score  # <--- thêm dòng này
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        from main import k_up, k_down, k_left, k_right

        total_reward = 0.0
        terminated = False
        truncated = False

        # Lặp 15 frame cho cùng 1 action
        for _ in range(15):
            # Reset phím
            k_up.toggle(False)
            k_down.toggle(False)
            k_left.toggle(False)
            k_right.toggle(False)

            if action == 0: k_up.toggle(True)
            elif action == 1: k_down.toggle(True)
            elif action == 2: k_left.toggle(True)
            elif action == 3: k_right.toggle(True)

            # Update game logic
            update()
            checkFood()
            checkGhostCollisionFrighten()

            # Reward theo delta_score
            reward = self._get_reward()
            total_reward += reward

            # Check game end
            if self._is_done():
                terminated = True
                break

        obs = self._get_obs()
        info = {}
        return obs, total_reward, terminated, truncated, info


    def render(self):
        if self.render_mode == "human":
            pygame.display.flip()

    def close(self):
        pygame.quit()

    def _get_obs(self):
        from main import pacman, ghosts, score

        obs = [
            pacman.getXPos(), pacman.getYPos(),
        ]

        for g in ghosts:
            obs.extend([g.getXPos(), g.getYPos(), self._encode_state(g)])

        obs.extend([score, pacman.lives])
        return np.array(obs, dtype=np.float32)

    def _encode_state(self, ghost):
        from main import ChaseMode, ScatterMode, FrightenedMode, EatenMode, HouseMode
        if isinstance(ghost.state, ChaseMode) or isinstance(ghost.state, ScatterMode):
            return 0
        elif isinstance(ghost.state, FrightenedMode):
            return 1
        elif isinstance(ghost.state, EatenMode):
            return 2
        elif isinstance(ghost.state, HouseMode):
            return 3
        return -1

    def _get_reward(self):
        from main import score, gameOver
        reward = score - self.prev_score
        self.prev_score = score
        if gameOver:
            return -500.0
        return float(reward)

    def _is_done(self):
        from main import gameOver, win
        return gameOver or win
