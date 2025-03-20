import matplotlib.pyplot as plt
from constants import *
from player import Player
from qtable import QTable


start_q_table = "qtable.npy"  # if we have a pickled Q table, we'll put the filename of it here.

episode_rewards = []

q_table = QTable(x_coordinates, y_coordinates, z_coordinates, num_actions=8, load_path=start_q_table)

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
            if np.random.random() > epsilon:
                
                action = np.argmax(q_table.get_qs(obs))
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
            if reward == FOOD_REWARD:
                new_q = FOOD_REWARD
            else:
                max_future_q = np.max(q_table.get_qs(new_obs))

                current_q = q_table.get_qs(obs)[action]

                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            
            q_table.update_q(obs, action, new_q)
            
            episode_reward += reward

            if reward == FOOD_REWARD:
                break
        
        episode_rewards.append(episode_reward)
        epsilon *= EPS_DECAY

except KeyboardInterrupt:
    info('Training interrupted manually')

finally:
    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.show()

    q_table.save("qtable.npy")
