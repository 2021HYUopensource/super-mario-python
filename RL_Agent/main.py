from Agents.creator import create_agent_main_sys
import gym
import numpy as np
from utils.img_preprocessing import make_stack
import cv2

env = gym.make('CarRacing-v0')

#https://github.com/andywu0913/OpenAI-GYM-CarRacing-DQN/blob/master/CarRacingDQNAgent.py
env = gym.make('BreakoutDeterministic-v4')

state = env.reset()
env.render()
state = [state for _ in range(3)]
state = make_stack(np.asarray(state))

dqn = create_agent_main_sys("PPO",env,state.shape,4,True)

dqn.train(10000,30)