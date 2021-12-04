import numpy as np
import cv2
import pygame
from pygame.locals import *

class SuperMarioEnv():
    def __init__(self, img_count):
        self.action_space_list = [['NOOP'], ['right'], ['up'], ['left'], ['up', 'left'], ['up', 'right']]
        self.screen = None
        self.menu = None
        self.sound = None
        self.level = None
        self.dashboard = None
        self.mario = None
        self.img_count = img_count

    def calculate_reward(self, x_diff, good_act, is_death, is_win):
        reward = 0
        if x_diff > 0:
            reward += 0.3
        elif x_diff < 0:
            reward -= 0.2
        else:
            reward -= 0.2
        reward += good_act * 0.1
        if is_win:
            reward += 15
        elif is_death:
            reward -= 15
        reward /= 10

        if reward > 1.5:
            reward = 1.5
        elif reward < -1.5:
            reward = -1.5

        return reward

    def get_screen(self, events, is_reset):
        state_imgs = []
        reward_total = 0

        if events == None:
            event = None
        else:
            event = events[0]
        for i in range(self.img_count):
            if event != None:
                pygame.event.post(event)
                if len(events) != 1:
                    event = events[1]
            self.level.drawLevel(self.mario.camera)
            self.dashboard.update()
            self.mario.update()
            pygame.display.update()
            pygame.image.save(self.screen, f'./tmp/0.png')
            state_imgs.append(cv2.imread('./tmp/0.png'))
            pygame.time.delay(5)
            if not is_reset:
                reward_total += self.calculate_reward(self.mario.rect.x - self.prev_x, self.mario.count_good, self.mario.over, self.mario.win)
            if self.mario.over or self.mario.win:
                if i < self.img_count:
                    last_img = cv2.imread('./tmp/0.png')
                    for _ in range(self.img_count - i - 1):
                        state_imgs.append(last_img.copy())
                break
        self.prev_x = self.mario.rect.x
        self.mario.count_good = 0
        print(reward_total)
        return np.asarray(state_imgs), reward_total

    def reset(self, screen, menu, sound, level, dashboard, mario):
        self.screen = screen
        self.menu = menu
        self.sound = sound
        self.level = level
        self.dashboard = dashboard
        self.mario = mario

        state = self.get_screen(None, True)[0]

        self.prev_x = self.mario.rect.x
        mario.count_good = 0

        return state

    def step(self, action):
        newevent = []
        if action == 0:
            newevent = None
        elif action == 1:
            newevent.append(pygame.event.Event(KEYDOWN, key=K_RIGHT, mod=KMOD_NONE))
        elif action == 2:
            newevent.append( pygame.event.Event(KEYDOWN, key=K_SPACE, mod=KMOD_NONE))
        elif action == 3:
            newevent.append(pygame.event.Event(KEYDOWN, key=K_LEFT, mod=KMOD_NONE))
        elif action == 4:
            newevent.append(pygame.event.Event(KEYDOWN, key=K_SPACE, mod=KMOD_NONE))
            newevent.append(pygame.event.Event(KEYDOWN, key=K_LEFT, mod=KMOD_NONE))
        elif action == 5:
            newevent.append(pygame.event.Event(KEYDOWN, key=K_SPACE, mod=KMOD_NONE))
            newevent.append(pygame.event.Event(KEYDOWN, key=K_RIGHT, mod=KMOD_NONE))

        state_imgs, reward_total = self.get_screen(newevent, False)

        done = False
        if self.mario.win or self.mario.over:
            done = True

        return state_imgs, reward_total, done

    def state_shape(self):
        return (84, 84, 4)

    def action_spcae(self):
        return len(self.action_space_list)

    def action_space_meaning(self):
        return self.action_space_list

class SuperMario():
    def make(self, img_count):
        return SuperMarioEnv(img_count)