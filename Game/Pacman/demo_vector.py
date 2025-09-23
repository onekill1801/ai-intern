game = PacmanGame(render_mode=None)
game.reset()
for _ in range(10):
    state, reward, done = game.step(3)  # đi sang phải
    print(state, reward, done)
