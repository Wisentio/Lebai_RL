from constants import *
import pybullet as p

axis_flip = np.array([-1, -1, -1])

class KukaAgent:
    def __init__(self, q_table, kuka_id, target_id, debug=False):
        self.q_table = q_table
        self.kuka_id = kuka_id
        self.target_id = target_id
        self.debug = debug
        self.delta = DSIZE  # Same DSIZE as your RL grid
        self.num_actions = q_table.num_actions

        self.actions = {
            0: np.array([self.delta, self.delta, self.delta]), 
            1: np.array([-self.delta, self.delta, self.delta]),
            2: np.array([-self.delta, -self.delta, self.delta]),
            3: np.array([self.delta, -self.delta, self.delta]),
            4: np.array([self.delta, self.delta, -self.delta]),
            5: np.array([-self.delta, self.delta, -self.delta]),
            6: np.array([-self.delta, -self.delta, -self.delta]),
            7: np.array([self.delta, -self.delta, -self.delta]),
        }

    def get_effector_position(self):
        state = p.getLinkState(self.kuka_id, 6)
        return np.array([round(coord,1) for coord in np.array(state[0])])

    def get_target_position(self):
        pos, _ = p.getBasePositionAndOrientation(self.target_id)
        return np.array([round(coord,1) for coord in pos])

    def step(self):
        effector_pos = self.get_effector_position()
        target_pos = self.get_target_position()
        diff = target_pos - effector_pos

        obs = (round(diff[0], 1), round(diff[1], 1), round(diff[2], 1))
        action = np.argmax(self.q_table.get_qs(obs))
        movement = self.actions[action] * axis_flip
        next_pos = effector_pos + movement

        if self.debug:
            print(f"Effector Pos: {effector_pos}")
            print(f"Target Pos: {target_pos}")
            print(f"Obs (diff): {obs}")
            print(f"Selected Action: {action} | Movement Vector: {movement}")

        # IK Solver
        joint_positions = p.calculateInverseKinematics(self.kuka_id, 6, next_pos)
        
        if self.debug:
            info(f'Joint positions are : {joint_positions}')
        
        for j in range(7):
            p.setJointMotorControl2(self.kuka_id, j, p.POSITION_CONTROL, joint_positions[j], force=500)

    def reached_target(self, threshold=0.05):
        diff = self.get_target_position() - self.get_effector_position()
        return np.linalg.norm(diff) < threshold
    