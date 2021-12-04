import numpy as np
import cv2
import pygame

class SuperMarioEnv():
    def __init__(self, action_size):
        self.action_space_list = [['NOOP'], ['right'], ['up'], ['left'], ['up', 'left'], ['up', 'right']]
        self.screen = None
        self.menu = None
        self.sound = None
        self.level = None
        self.dashboard = None
        self.mario = None
        self.action_size = action_size

    def reset(self, screen, menu, sound, level, dashboard, mario):
        self.screen = screen
        self.menu = menu
        self.sound = sound
        self.level = level
        self.dashboard = dashboard
        self.mario = mario

        self.state_imgs = []

        for _ in range(self.action_size):
            level.drawLevel(self.mario.camera)
            dashboard.update()
            self.mario.update()
            pygame.display.update()
            pygame.image.save(screen, f'./tmp/0.png')
            self.state_imgs.append(cv2.imread('./tmp/0.png'))
            pygame.time.delay(10)

        return np.asarray(self.state_imgs)

    def state(self):
       pass

    def step(self, action):
        done = False
        if self.mario.win or self.mario.over:
            done = True

    def state_shape(self):
        return (84, 84, 4)

    def action_spcae(self):
        return len(self.action_space_list)

    def action_space_meaning(self):
        return self.action_space_list

class SuperMario():
    def make(self, action_size):
        return SuperMarioEnv(action_size)