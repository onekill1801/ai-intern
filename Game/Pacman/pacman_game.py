import pygame
import csv
from main import Pacman, BlinkyGhost, InkyGhost, PinkyGhost, ClydeGhost
from main import PacGum, SuperPacGum, Wall, GhostDoor
from main import checkFood, checkGhostCollisionFrighten, update, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock, FPS

class PacmanGame:
    def __init__(self, render_mode=None):
        self.render_mode = render_mode
        self.score = 0
        self.lives = 3
        self.done = False
        self.win = False
        self.entities = []
        self.ghosts = []
        self.walls = []
        self.pacman = None
        self.prev_score = 0

    def reset(self):
        # Reset biến
        self.score = 0
        self.lives = 3
        self.done = False
        self.win = False
        self.entities = []
        self.ghosts = []
        self.walls = []
        self.prev_score = 0

        # Load level
        file = open("res/level/level.csv", "r")
        level = list(csv.reader(file, delimiter=";"))
        file.close()

        size = 8
        blinkGhost = inkyGhost = pinkyGhost = clydeGhost = None

        for i in range(len(level)):
            for j in range(len(level[i])):
                x, y = j * size, i * size
                if level[i][j] == ".":
                    self.entities.append(PacGum(x, y))
                elif level[i][j] == "o":
                    self.entities.append(SuperPacGum(x, y))
                elif level[i][j] == "x":
                    wall = Wall(x, y)
                    self.entities.append(wall)
                    self.walls.append(wall)
                elif level[i][j] == "-":
                    self.entities.append(GhostDoor(x, y))
                elif level[i][j] == "P":
                    self.pacman = Pacman(x, y)
                elif level[i][j] == "b":
                    blinkGhost = BlinkyGhost(x, y)
                elif level[i][j] == "i":
                    inkyGhost = InkyGhost(x, y, blinkGhost)
                elif level[i][j] == "p":
                    pinkyGhost = PinkyGhost(x, y)
                elif level[i][j] == "c":
                    clydeGhost = ClydeGhost(x, y)

        self.entities.extend([self.pacman, blinkGhost, inkyGhost, pinkyGhost, clydeGhost])
        self.ghosts.extend([blinkGhost, inkyGhost, pinkyGhost, clydeGhost])

    def step(self, action):
        """action: 0=up, 1=down, 2=left, 3=right"""
        from main import k_up, k_down, k_left, k_right

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

        # Tính reward
        reward = self.get_reward()
        self.prev_score = self.score

        return self.get_state(), reward, self.is_done()

    def get_state(self):
        """Observation vector"""
        obs = [self.pacman.getXPos(), self.pacman.getYPos()]
        for g in self.ghosts:
            obs.extend([g.getXPos(), g.getYPos()])
        obs.extend([self.score, self.lives])
        return obs

    def get_reward(self):
        from main import score, gameOver
        reward = score - self.prev_score
        self.score = score
        if gameOver:
            self.done = True
            return -500
        return reward

    def is_done(self):
        from main import gameOver, win
        return gameOver or win

    def render(self):
        if self.render_mode == "human":
            pygame.display.flip()

    def close(self):
        pygame.quit()
