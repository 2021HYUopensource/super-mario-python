from PPO.agent import PPO_Agent
import time
import numpy as np
import datetime
import os
import sys
from utils.img_preprocessing import make_stack
from tensorboardX import SummaryWriter
from collections import deque

def create_ppo_main_sys(env,state_shape, action_size,verbose):

    main_sys = PPO_main_system(env,state_shape,action_size,verbose)

    return main_sys


class PPO_main_system:

    def __init__(self, env, state_shape, action_size,verbose):
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

        summary = SummaryWriter()

        break_counter = 0
        for epi in range(max_epi):
            frame_counter = 0
            bad_status = 0
            done = False
            state = self.env.reset()
            self.env.render()
            state = [state for _ in range(3)]
            state = make_stack(np.asarray(state))
            tot_reward = 0

            while not done:
                self.env.render()
                reward = 0
                action,action_onehot,act_prob = self.Agent.get_act(state)
                next_state_list = []
                for i in range(3):
                    next_state, r, done, _ = self.env.step(action)
                    next_state_list.append(next_state)
                    reward += r

                if(frame_counter >= 30 and reward == 0):
                    bad_status += 1
                    if(bad_status >= 60):
                        print("bad status now, break")
                        break
                else:
                    bad_status = 0
                next_state = make_stack(np.asarray(next_state_list))
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



