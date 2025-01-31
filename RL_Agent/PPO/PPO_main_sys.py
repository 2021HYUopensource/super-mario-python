import classes.LearningEnv
from ..PPO.agent import PPO_Agent
import time
import numpy as np
import datetime
import os
import sys
from ..utils.img_preprocessing import make_stack
from tensorboardX import SummaryWriter
from collections import deque
import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
import cv2

ppo_def_param = {
    "learning_rate": 0.001,
    "loss_clipping": 0.2,
    "entropy_loss": 0.001,
    "epoch": 8,
    "gamma": 0.98,
    "lmbda": 0.95,
    "batch_size": 512
}


def create_ppo_main_sys(env,state_shape, action_size,verbose):
    '''

    :param env: 학습에 사용할 환경 오브젝트
    :param state_shape: observation shape (3D)
    :param action_size: action space size (1D)
    :param verbose: 로그를 표시할 지 여부 (bool)
    :param param: 모델 하이퍼 파라미터(dict)
    :return: (object) ppo_main_system
    '''
    # for key in ppo_def_param.keys():
    #     if not key in param:
    #         param[key] = ppo_def_param[key]

    main_sys = PPO_main_system(env,state_shape,action_size,verbose)

    return main_sys


class PPO_main_system:
    def __init__(self, env:classes.LearningEnv.SuperMarioEnv,
                 state_shape:tuple,
                 action_size:int,
                 verbose:bool):
        self.env = env
        self.state_shape = state_shape
        self.action_size = action_size
        self.Agent = PPO_Agent(state_shape, action_size, verbose, ppo_def_param)
        self.verbose = verbose

    def _action_one_hot(self,action):
        onehot = np.zeros(self.action_size)
        onehot[action] = 1
        return onehot

    def __restart(self, screen, menu, sound, level, dashboard, mario):
        restart_name = level.name
        rl_mode = menu.rl_mode
        dashboard = Dashboard("./img/font.png", 8, screen)
        sound = Sound(rl_mode)
        level = Level(screen, sound, dashboard)
        menu = Menu(screen, dashboard, level, sound)
        menu.inChoosingLevel = False
        menu.rl_mode = rl_mode
        menu.dashboard.state = "start"
        menu.dashboard.time = 0
        menu.level.loadLevel(restart_name)
        menu.dashboard.levelName = restart_name
        menu.start = True
        mario = Mario(0, 12, level, screen, dashboard, sound, menu.rl_mode)
        return screen, menu, sound, level, dashboard, mario

    def train(self,max_epi,target_score, screen, menu, sound, level, dashboard, load_model = False):
        '''
        학습 시작

        :param max_epi: 반복 횟수
        :type max_epi: int
        :param target_score: 목표 점수
        :type target_score: int
        '''

        mario = Mario(0, 12, level, screen, dashboard, sound, menu.rl_mode)

        summary = SummaryWriter()

        if(load_model):
            self.Agent.load_model()

        for epi in range(max_epi):
            done = False

            screen, menu, sound, level, dashboard, mario = self.__restart(screen, menu, sound, level, dashboard, mario)
            state = self.env.reset(screen, menu, sound, level, dashboard, mario)
            state = make_stack(np.asarray(state))

            tot_reward = 0
            time = 0
            while not done:
                action, action_onehot, act_prob = self.Agent.get_act(state)
                next_state, reward, done,time = self.env.step(action)
                if(time >= 300):
                    print("time over!");
                    break;
                next_state = make_stack(np.asarray(next_state))

                tot_reward += reward
                self.Agent.add_buffer(state, action_onehot, reward, next_state, act_prob, done)
                self.Agent.train()
                state = next_state

            if self.verbose:
                print(f"log >> {epi} epi fin.   score : {tot_reward}")

            summary.add_scalar('reward', tot_reward, epi)

            if tot_reward >= target_score:
                break_counter += 1
                if break_counter >= 5:
                    if self.verbose:
                        print("log >> train fin.")
                    break
            else:
                break_counter = 0
