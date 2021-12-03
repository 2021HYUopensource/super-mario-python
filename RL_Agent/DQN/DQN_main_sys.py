from DQN import agent
import numpy as np
from utils.img_preprocessing import make_stack
from tensorboardX import SummaryWriter
from collections import deque

def create_dqn_main_sys(env,state_shape, action_size,action_space,verbose,param):

    main_sys = DQN_main_system(env,state_shape,action_size,action_space,verbose,param)

    return main_sys


class DQN_main_system:

    def __init__(self, env, state_shape, action_size,action_space,verbose,param):
        self.env = env
        self.state_shape = state_shape
        self.action_size = action_size
        self.action_space = action_space
        self.Agent = agent.DQNAgent(state_shape, action_size,verbose,param)
        self.verbose = verbose
        self.update_counter = 5

    def _action_one_hot(self,action):
        onehot = np.zeros(self.action_size)
        onehot[action] = 1

        return onehot

    def train(self,max_epi,target_score,load_model=False):

        summary = SummaryWriter()

        if(load_model):
            self.Agent.load_model()

        break_counter = 0
        for epi in range(max_epi):

            s = self.env.reset()
            self.env.render()

            state_stack = deque([s for _ in range(4)],maxlen=4)

            state = make_stack(np.asarray(state_stack))

            next_state = None
            tot_reward = 0
            negative_score_counter = 0
            done = False
            action_count = 0

            while not done:
                reward = 0
                self.env.render()
                action = self.Agent.get_act(state)
                onehot_action = self.action_space[action]


                for i in range(3):
                    self.env.render()
                    next_state, r, done, _ = self.env.step(onehot_action)
                    print(r)
                    reward += r
                state_stack.append(next_state)
                next_state = make_stack(np.asarray(state_stack))
                tot_reward += reward
                print(f"score : {reward}")

                self.Agent.add_memory(state, action, reward, next_state, done)
                # self.Agent.train()
                state = next_state

                # if (reward < 0):
                #     negative_score_counter += 1
                #     if(negative_score_counter >= 15):
                #         break
                # else:
                #     negative_score_counter = 0

                action_count += 1


            if(self.verbose):
                print(f"log >> {epi} epi fin.   score : {tot_reward}  action : {action_count}")
            summary.add_scalar('reward', tot_reward, epi)
            self.Agent.epsilon_update()
            if(epi % self.update_counter):
                self.Agent.update_target_brain()

            if(tot_reward >= target_score):

                break_counter += 1

                if(break_counter >= 5):
                    if(self.verbose):
                        print("log >> train fin.")
                    break

            else:
                break_counter = 0

        if(self.verbose):
            print("log >> train fin. but failed to reach target score")

    def test(self,max_epi,load_model=True):
        sum_reward = 0
        if(load_model):
            self.Agent.load_model()

        for epi in range(max_epi):
            done = False
            state = self.env.reset()
            state = [state for _ in range(3)]
            state = make_stack(np.asarray(state))
            tot_reward = 0
            while not done:

                self.env.render()
                reward = 0
                action = self.Agent.get_test_act_(state)
                print(action)
                onehot_action = self.action_space[action]

                next_state_arr = []

                for i in range(3):
                    self.env.render()
                    next_state, r, done, _ = self.env.step(onehot_action)
                    next_state_arr.append(next_state)
                    reward += r

                next_state = make_stack(np.asarray(next_state_arr))
                tot_reward += reward

                state = next_state

            if(self.verbose):
                print(f"log >> {epi} epi fin.   score : {tot_reward}")

            sum_reward += tot_reward

        if (self.verbose):
            print(f"log >> mean score : {sum_reward/max_epi}")


