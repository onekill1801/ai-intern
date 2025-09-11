import numpy as np
import gymnasium as gym

env = gym.make("CartPole-v1")

n_actions = env.action_space.n
n_states = 20   # discretize state cho đơn giản
q_table = np.zeros((n_states, n_actions))

def discretize(state):
    # đơn giản hóa state liên tục thành số nguyên
    return int(min(n_states - 1, max(0, state[0] * n_states / 4 + n_states/2)))

alpha = 0.1      # learning rate
gamma = 0.99     # discount factor
epsilon = 0.1    # exploration rate

for episode in range(1000):
    state, _ = env.reset()
    state = discretize(state)
    done = False

    while not done:
        # chọn action (epsilon-greedy)
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state])

        # thực hiện action
        next_state, reward, done, truncated, _ = env.step(action)
        next_state = discretize(next_state)

        # cập nhật Q-table
        q_table[state, action] += alpha * (
            reward + gamma * np.max(q_table[next_state]) - q_table[state, action]
        )

        state = next_state
        if done or truncated:
            break

print("Training hoàn tất!")
