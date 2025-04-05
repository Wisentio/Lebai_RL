import matplotlib.pyplot as plt
from config import *
from player import Player
from agent import QTable

start_q_table = "qtable.npy"  # if we have a pickled Q table, we'll put the filename of it here.

episode_rewards = []

q_table = QTable(x_coordinates, y_coordinates, z_coordinates, epsilon, num_actions=8, load_path=start_q_table)


# env = Environment()

# for episode in range(HM_EPISODES):
#     obs = env.reset()
#     done = False

#     while not done:
#         if np.random.random() > epsilon:
#             action = np.argmax(agent.q_table.get_qs(obs))
#         else:
#             action = np.random.randint(0, 8)

#         new_obs, reward, done, _ = env.step(action)

#         # Learning logic here:
#         agent.learn(obs, action, reward, new_obs, done)
#         obs = new_obs

try:
    for episode in range(HM_EPISODES):
        effector = Player()
        target = Player()

        if episode % SHOW_EVERY == 0:  
            info(f'{episode} episodes')

        episode_reward = 0

        for _ in range(200):
            obs = (effector-target)

            # Get the action
            if np.random.random() > q_table.epsilon:
                
                action = np.argmax(q_table.act(obs))
            else:
                action = np.random.randint(0, 8)

            # Take the action!
            effector.action(action)

            target.move()

            new_obs = (effector-target)

            # Rewarding
            if all(abs(coordinate) < PROXIMITY_THREASHOLD for coordinate in new_obs):
                reward = FOOD_REWARD
            else:
                reward = -MOVE_PENALTY

            # Update q_table
            # if reward == FOOD_REWARD:
            #     new_q = FOOD_REWARD
            # else:
            #     max_future_q = np.max(q_table.act(new_obs))

            #     current_q = q_table.act(obs)[action]

            #     new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            # q_table.update_q(obs, action, new_q)
            q_table.learn(obs, action, reward, new_obs, True if reward == FOOD_REWARD else False)

            episode_reward += reward

            if reward == FOOD_REWARD:
                break
        
        episode_rewards.append(episode_reward)
        q_table.decay_epsilon()

except KeyboardInterrupt:
    info('Training interrupted manually')

finally:
    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.show()

    q_table.save("qtable.npy")
