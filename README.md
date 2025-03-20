# Lebai_RL

This code is divided into learning.py script - which creates/modifies a file (on default - qtable.npy) that stores the qtable

On the other hand - there is the sim.py script, which creates a simulation of a robot with 6 dof (predefined model of kuka_iiwa from pybullet is used) 

To run the script, run the sim.py code.

Make sure about the requirements

Python version used is 3.8.0


Steps to follow:

## 📥 Clone this repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/Wisentio/Lebai_RL.git
cd Lebai_RL

Download python 3.8
Create a virtual environment : python3.8 -m venv <name_of_venv>
Activate it :   Linux/macOS: source myenv/bin/activate
                Windows (cmd): myenv\Scripts\activate.bat
                Windows (PowerShell): myenv\Scripts\Activate.ps1

Install requirements: pip install -r requirements.txt
Run simulation: python3.8 sim.py
