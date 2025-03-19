import pybullet as p
import pybullet_data
import time
import numpy as np


# Connect to PyBullet in GUI mode
p.connect(p.GUI)

# Set the additional search path for built-in models
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the plane (ground)
plane_id = p.loadURDF("plane.urdf")

# Load the KUKA iiwa robot
robot_id = p.loadURDF("kuka_iiwa/model.urdf", basePosition=[0, 0, 0])

# Get the number of joints in the robot
num_joints = p.getNumJoints(robot_id)

# Find the **end-effector** index (last joint)
end_effector_index = num_joints - 1  # Usually the last joint

# Define the **target positions** for up and down movement
target_position_up = [0.7, 0, 0]  # Move up
target_position_down = [0.5, 0, 0.3]  # Move down
target_orientation = p.getQuaternionFromEuler([0, np.pi/2, 0])  # Fixed orientation

# Simulation settings
switch_time = 2.0  # Switch movement every 2 seconds
last_switch = time.time()  # Track last switch time
moving_up = True  # Start by moving up

# Run the simulation
while True:
    # Check if it's time to switch position
    current_time = time.time()
    if current_time - last_switch > switch_time:
        moving_up = not moving_up  # Toggle direction
        last_switch = current_time  # Reset timer
        
        # Print effector possition
        link_state = p.getLinkState(robot_id, end_effector_index)
        effector_pos = link_state[4]  # World position of the link CoM
        print(f"End-effector position: {effector_pos}")

    # Select the target position based on direction
    target_position = target_position_up if moving_up else target_position_down

    # Compute Inverse Kinematics (IK) to get the required joint angles
    joint_angles = p.calculateInverseKinematics(robot_id, end_effector_index, target_position, target_orientation)

    # Apply the computed joint angles to move the robot
    for i in range(num_joints):
        p.setJointMotorControl2(robot_id, i, p.POSITION_CONTROL, joint_angles[i])


    # Step simulation
    p.stepSimulation()
    time.sleep(1./240.)  # Run at 240Hz
