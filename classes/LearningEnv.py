import numpy as np
import cv2

class SuperMarioEnv():
    def __init__(self):
        self.action_space_list = [['NOOP'], ['right'], ['up'], ['left'], ['up', 'left'], ['up', 'right']]
        self.isInit = True

    def reset(self):
        self.isInit = True

    def state(self):
        if self.isInit:
            pass
        else:
            pass

    def step(self, action):
        pass

    def state_shape(self):
        return (84, 84, 4)

    def action_spcae(self):
        return len(self.action_space_list)

    def action_space_meaning(self):
        return self.action_space_list

class SuperMario():
    def make(self):
        return SuperMarioEnv()