from player import Player

class Environment:


    def __init__(self):
        self.effector = Player()
        self.target = Player()

    def step(self, action):
        """Effector takes an action, target moves randomly"""

        self.effector.action(action)
        self.target.move()
        obs = (self.effector - self.target)

        

    def reset(self):
        """Reset effector and target position, return observation"""

        self.effector = Player()
        self.target = Player()

        return (self.effector - self.target)
