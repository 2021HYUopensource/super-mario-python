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

def create_ppo_main_sys(env,state_shape, action_size,verbose):
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
        self.Agent = PPO_Agent(state_shape, action_size,verbose)
        self.verbose = verbose

    def _action_one_hot(self,action):
        onehot = np.zeros(self.action_size)
        onehot[action] = 1

        return onehot

    def train(self,max_epi,target_score):
        '''
        학습 시작

        :param max_epi: 반복 횟수
        :type max_epi: int
        :param target_score: 목표 점수
        :type target_score: int
        '''
        summary = SummaryWriter()

        break_counter = 0
        for epi in range(max_epi):
            frame_counter = 0
            done = False
            state = self.env.reset()
            state = [state for _ in range(3)]
            state = make_stack(np.asarray(state)) # TODO: 전처리만 뜯어 쓰기
            tot_reward = 0

            while not done:
                reward = 0
                action,action_onehot,act_prob = self.Agent.get_act(state)
                next_state_list = []
                # TODO: step만 사용
                next_state, reward, done = self.env.step(action)

                tot_reward += reward
                self.Agent.add_buffer(state, action_onehot, reward, next_state, act_prob,done)
                self.Agent.train()
                state = next_state
                frame_counter += 1

            if(self.verbose):
                print(f"log >> {epi} epi fin.   score : {tot_reward}")

            summary.add_scalar('reward', tot_reward, epi)
            if(tot_reward >= target_score):
                break_counter += 1
                if(break_counter >= 5):
                    if(self.verbose):
                        print("log >> train fin.")
                    break
            else:
                break_counter = 0



