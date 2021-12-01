import numpy as np
import cv2

class SuperMarioEnv():
    def __init__(self):
        self.action_space = {['NOOP']: [1,0,0,0,0,0,0], ['right']: [0,1,0,0,0,0,0], ['right', 'A']: [0,0,1,0,0,0,0],
                             ['right', 'B']: [0,0,0,1,0,0,0], ['right', 'A', 'B']: [0,0,0,0,1,0,0],
                             ['A']: [0,0,0,0,0,1,0], ['left']: [0,0,0,0,0,0,1]}
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

class SuperMario():
    def make(self):
        return SuperMarioEnv()