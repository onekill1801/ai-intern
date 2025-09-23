import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from main import init, update, pacman, ghosts, checkFood, checkGhostCollisionFrighten, draw, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock, FPS

class PacmanEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode

        # Action space: 0 lên, 1 xuống, 2 trái, 3 phải
        self.action_space = spaces.Discrete(4)

        # Quan sát: ảnh màn hình
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8
        )

        self.running = True

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        init()
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        # Map action → input Pacman
        from main import k_up, k_down, k_left, k_right
        k_up.toggle(False)
        k_down.toggle(False)
        k_left.toggle(False)
        k_right.toggle(False)

        if action == 0: k_up.toggle(True)
        elif action == 1: k_down.toggle(True)
        elif action == 2: k_left.toggle(True)
        elif action == 3: k_right.toggle(True)

        # Update game 1 frame
        update()
        checkFood()
        checkGhostCollisionFrighten()

        obs = self._get_obs()
        reward = self._get_reward()
        terminated = self._is_done()
        truncated = False
        info = {}

        return obs, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            pygame.display.flip()
        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(screen)), (1, 0, 2)
            )

    def close(self):
        pygame.quit()

    def _get_obs(self):
        return np.transpose(np.array(pygame.surfarray.pixels3d(screen)), (1, 0, 2))

    def _get_reward(self):
        from main import score, gameOver
        if gameOver:
            return -1000
        return score

    def _is_done(self):
        from main import gameOver, win
        return gameOver or win
