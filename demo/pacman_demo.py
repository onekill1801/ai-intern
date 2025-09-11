import gymnasium as gym

# tạo môi trường CartPole
env = gym.make("CartPole-v1", render_mode="human")

# khởi tạo state ban đầu
state, info = env.reset()  # Gymnasium trả về (state, info)

done = False
total_reward = 0

while not done:
    # chọn hành động ngẫu nhiên (AI chưa học gì)
    action = env.action_space.sample()
    
    # step trả về 5 giá trị thay vì 4
    state, reward, done, truncated, info = env.step(action)
    total_reward += reward

    # nếu game kết thúc do done hoặc truncated
    if done or truncated:
        break

print("Tổng điểm:", total_reward)
env.close()
