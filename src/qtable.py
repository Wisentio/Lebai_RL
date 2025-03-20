import numpy as np
from constants import info


class QTable:
    """Creates a qtable used to define the strategy for q-learning"""

    def __init__(self, x_coords, y_coords, z_coords, num_actions=8, load_path=None):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.z_coords = z_coords
        self.num_actions = num_actions
        
        # Build mappings for fast index lookup
        self.x_idx_map = {v: i for i, v in enumerate(x_coords)}
        self.y_idx_map = {v: i for i, v in enumerate(y_coords)}
        self.z_idx_map = {v: i for i, v in enumerate(z_coords)}
        
        shape = (len(x_coords), len(y_coords), len(z_coords), num_actions)
        
        if load_path:
            self.q_table = np.load(load_path)
            info(f"Loaded Q-table from {load_path}")
        else:
            self.q_table = np.random.uniform(-5, 0, shape)
            info(f"Initialized new Q-table with shape {self.q_table.shape}")
    
    def coord_to_idx(self, obs):
        """Converts (x, y, z) tuple to (i, j, k) indices"""
        return (self.x_idx_map[obs[0]],
                self.y_idx_map[obs[1]],
                self.z_idx_map[obs[2]])
    
    def get_qs(self, obs):
        # Safe snap before coord_to_idx
        safe_obs = (
            self.snap_to_grid(obs[0], self.x_coords),
            self.snap_to_grid(obs[1], self.y_coords),
            self.snap_to_grid(obs[2], self.z_coords)
        )
        x, y, z = self.coord_to_idx(safe_obs)
        return self.q_table[x, y, z]
    
    def update_q(self, obs, action, new_q):
        """Updates Q-value for a given state-action pair"""
        x, y, z = self.coord_to_idx(obs)
        self.q_table[x, y, z, action] = new_q
    
    def save(self, path):
        np.save(path, self.q_table)
        info(f"Saved Q-table to {path}")

    def snap_to_grid(self, val, coord_list):
        """Snap a coordinate value to the closest valid grid coordinate."""
        return min(coord_list, key=lambda x: abs(x - val))