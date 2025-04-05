import numpy as np
import os

class QTable:
    def __init__(self, x_coords, y_coords, z_coords, num_actions, load_path=None):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.z_coords = z_coords
        self.num_actions = num_actions

        self.x_idx_map = {x: i for i, x in enumerate(self.x_coords)}
        self.y_idx_map = {y: i for i, y in enumerate(self.y_coords)}
        self.z_idx_map = {z: i for i, z in enumerate(self.z_coords)}

        self.shape = (len(x_coords), len(y_coords), len(z_coords), num_actions)

        if load_path and os.path.exists(load_path):
            self.q_table = np.load(load_path)
            print(f"✅ Loaded Q-table from {load_path}")
        else:
            self.q_table = np.random.uniform(low=-1, high=0, size=self.shape)

    def coord_to_idx(self, coord):
        """Map real-valued (x, y, z) to Q-table indices."""
        x, y, z = coord
        return (
            self.x_idx_map.get(x),
            self.y_idx_map.get(y),
            self.z_idx_map.get(z)
        )

    def get_qs(self, coord):
        """Return Q-values for a given state (x, y, z)."""
        x, y, z = self.coord_to_idx(coord)
        if x is None or y is None or z is None:
            raise KeyError(f"State {coord} is out of bounds")
        return self.q_table[x, y, z]

    def update_q(self, coord, action, new_q):
        """Update Q-value for given state and action."""
        x, y, z = self.coord_to_idx(coord)
        self.q_table[x, y, z, action] = new_q

    def save(self, path):
        np.save(path, self.q_table)
        print(f"💾 Q-table saved to {path}")

    def load(self, path):
        self.q_table = np.load(path)
        print(f"✅ Q-table loaded from {path}")

if __name__ == '__main__':

    # Define dummy discrete state space
    x_coords = [-0.2, -0.1, 0.0, 0.1, 0.2]
    y_coords = [-0.2, -0.1, 0.0, 0.1, 0.2]
    z_coords = [0.0, 0.1, 0.2, 0.3]
    num_actions = 4

    print("🔧 Initializing QTable...")
    qt = QTable(x_coords, y_coords, z_coords, num_actions)

    # Pick a test coordinate
    state = (0.1, -0.2, 0.2)
    action = 2

    print("\n📦 Q-values at state:", state)
    qs = qt.get_qs(state)
    print("Q-values:", qs)

    print("\n✏️ Updating Q-value...")
    qt.update_q(state, action, 42.0)

    qs_updated = qt.get_qs(state)
    assert qs_updated[action] == 42.0, "Q-value update failed!"
    print("✅ Q-value updated correctly.")

    # Save to file
    path = "test_qtable.npy"
    qt.save(path)
    assert os.path.exists(path), "Save failed!"
    print("✅ Q-table saved.")

    # Load and verify
    qt2 = QTable(x_coords, y_coords, z_coords, num_actions, load_path=path)
    qs_loaded = qt2.get_qs(state)

    assert np.allclose(qs_loaded[action], 42.0), "Loaded Q-value doesn't match saved!"
    print("✅ Q-table loaded and values match.")

    # Clean up
    os.remove(path)
    print("\n🧪 QTable test passed!")
