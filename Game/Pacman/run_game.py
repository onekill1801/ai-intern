import pygame
from pacman_game import PacmanGame

def run_game():
    game = PacmanGame(render_mode="human")
    game.reset()

    running = True
    clock = pygame.time.Clock()

    while running:
        # bắt sự kiện phím
        action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: action = 0
                elif event.key == pygame.K_DOWN: action = 1
                elif event.key == pygame.K_LEFT: action = 2
                elif event.key == pygame.K_RIGHT: action = 3

        if action is not None:
            state, reward, done = game.step(action)
            print(f"Pacman pos: {state[0]}, {state[1]}, Reward={reward}")

        game.render()
        clock.tick(60)  # FPS

        if game.is_done():
            print("Game Over!")
            running = False

    game.close()

if __name__ == "__main__":
    run_game()
