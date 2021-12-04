from PPO.agent import PPO_Agent
import time
import numpy as np
import datetime
import os
import sys
from utils.img_preprocessing import make_stack,prep
from tensorboardX import SummaryWriter
from collections import deque

ppo_def_param = {
    "learning_rate": 0.003,
    "loss_clipping": 0.2,
    "entropy_loss": 0.001,
    "epoch": 10,
    "gamma": 0.99,
    "lmbda": 0.95,
    "batch_size": 1000
}


def create_ppo_main_sys(env,state_shape, action_size,verbose,param):
    '''

    :param env: 학습에 사용할 환경 오브젝트
    :param state_shape: observation shape (3D)
    :param action_size: action space size (1D)
    :param verbose: 로그를 표시할 지 여부 (bool)
    :param param: 모델 하이퍼 파라미터(dict)
    :return: (object) ppo_main_system
    '''
    for key in ppo_def_param.keys():
        if not key in param:
            param[key] = ppo_def_param[key]

    main_sys = PPO_main_system(env,state_shape,action_size,verbose,param)

    return main_sys


class PPO_main_system:

    def __init__(self, env, state_shape, action_size,verbose,param):
        self.env = env
        self.state_shape = state_shape
        self.action_size = action_size
        self.Agent = PPO_Agent(state_shape, action_size,verbose,param)
        self.verbose = verbose

    def _action_one_hot(self,action):
        onehot = np.zeros(self.action_size)
        onehot[action] = 1

        return onehot

    def train(self,max_epi,load_model = False):

        summary = SummaryWriter()

        if(load_model):
            self.Agent.load_model()

        for epi in range(max_epi):
            done = False
            state = self.env.reset()
            state = prep(state)
            self.env.render()
            tot_reward = 0

            while not done:
                self.env.render()
                action,action_onehot,act_prob = self.Agent.get_act(state)
                next_state, reward, done, _ = self.env.step(action)
                next_state = prep(next_state)
                tot_reward += reward
                self.Agent.add_buffer(state, action_onehot, reward, next_state, act_prob,done)
                self.Agent.train()
                state = next_state



            if(self.verbose):
                print(f"log >> {epi} epi fin.   score : {tot_reward}")

            summary.add_scalar('reward', tot_reward, epi)


    def test(self,max_epi,load_model = True):


        if(load_model):
            self.Agent.load_model()

        rewards = []
        for epi in range(max_epi):

            done = False
            state = self.env.reset()
            state = prep(state)
            self.env.render()
            tot_reward = 0

            while not done:
                self.env.render()
                action,action_onehot,act_prob = self.Agent.evaluate_get_act_(state)
                next_state, reward, done, _ = self.env.step(action)
                next_state = prep(next_state)
                tot_reward += reward
                state = next_state

            rewards.append(tot_reward)

            if(self.verbose):
                print(f"log >> {epi} epi fin.   score : {tot_reward}")

        print(f"average score :{sum(rewards)/max_epi}")



