from pacman_env_vector import PacmanEnvVector

env = PacmanEnvVector(render_mode="human")
obs, info = env.reset()

for step in range(200):
    action = env.action_space.sample()  # agent chọn ngẫu nhiên
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Step {step}: Obs={obs}, Reward={reward}")
    if terminated or truncated:
        obs, info = env.reset()

env.close()
