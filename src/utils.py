import numpy as np
import logging
import matplotlib.pyplot as plt
import os

# ========== 1. Snap to nearest coordinate ==========
def snap_to_grid(val, coord_list):
    """Snap a continuous value to the nearest discrete grid point."""
    return min(coord_list, key=lambda x: abs(x - val))


# ========== 2. Setup basic logger ==========
def setup_logger(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )


# ========== 3. Plot moving average ==========
def plot_moving_average(rewards, window=100, save_path=None):
    if len(rewards) < window:
        print("Not enough rewards to plot moving average.")
        return

    moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
    plt.figure()
    plt.plot(moving_avg)
    plt.title(f"Moving Average Reward ({window}-episode window)")
    plt.xlabel("Episode")
    plt.ylabel("Avg Reward")
    if save_path:
        plt.savefig(save_path)
        print(f"📈 Saved reward plot to {save_path}")
    else:
        plt.show()


# ========== 4. Ensure directory exists ==========
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
