import pybullet as p
import pybullet_data
import time
from config import *
from agent import QTable
from kuka_agent import KukaAgent
import random


p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetSimulation()
p.setGravity(0, 0, -9.81)

planeId = p.loadURDF("plane.urdf")
kukaId = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

# Target (visual only)
target_visual = p.createVisualShape(p.GEOM_SPHERE, radius=0.05, rgbaColor=[1,0,0,1])
target_id = p.createMultiBody(baseVisualShapeIndex=target_visual)

# -------------------------------
# Target Randomization Function
# -------------------------------

def random_coordinate():
    while True:
        coordinate = round(random.uniform(-0.6, 0.6), 1)
        if coordinate <= -0.3 or coordinate >= 0.3:
            return coordinate

def randomize_target():
    x = random_coordinate()
    y = random_coordinate()
    z = round(random.uniform(0.1, 0.6), 1)
    p.resetBasePositionAndOrientation(target_id, [x, y, z], [0, 0, 0, 1])
    return [x, y, z]

def defined_target():
    x = 1
    y = 1
    z = 1
    p.resetBasePositionAndOrientation(target_id, [x, y, z], [0, 0, 0, 1])
    return [x, y, z]

# -------------------------------
# Load Q-table & Start Agent
# -------------------------------
q_table = QTable(x_coordinates, y_coordinates, z_coordinates, 0.5, num_actions=8, load_path="qtable.npy")
agent = KukaAgent(q_table, kukaId, target_id)

# -------------------------------
# Main Simulation Loop
# -------------------------------

initial_joint_positions = [0, -0.6, 0, 1.2, 0, -0.6, 0]

for joint_index in range(p.getNumJoints(kukaId)):
    p.resetJointState(kukaId, joint_index, initial_joint_positions[joint_index])

paused = False

for episode in range(1500):

    logging.info(f"=== Episode {episode+1} ===")

    target = randomize_target()
    time_start = time.time()

    for step in range(500):
        keys = p.getKeyboardEvents()

        # Toggle pause with SPACEBAR
        if ord(' ') in keys and keys[ord(' ')] & p.KEY_WAS_TRIGGERED:
            paused = not paused
            if paused:
                logging.info("== Paused ==")
            else:
                logging.info("== Unpaused ==")

        if not paused:
            if step % DISPLAY_EVERY == 0:
                agent.step(True)
            else:
                agent.step()
            p.stepSimulation()

        time.sleep(0.0002)

        if not paused and agent.reached_target():
            logging.info(f'=== Target Reached! in {round(time.time() - time_start, 3)} s ===')
            break
    # logging.info(f"=== Episode {episode+1} ===")

    # target = randomize_target()
    # time_start = time.time()

    # for step in range(500):
    #     if step % DISPLAY_EVERY == 0:
    #         agent.step(True)
    #     else:
    #         agent.step()
    #     p.stepSimulation()
    #     time.sleep(0.0002)

    #     if agent.reached_target():
    #         logging.info(f'=== Target Reached! in {round(time.time() - time_start, 3)} s ===')
    #         break

p.disconnect()
