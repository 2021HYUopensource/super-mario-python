import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Input
from tensorflow.keras.optimizers import Adam
from collections import deque
import random
import os

tf.compat.v1.disable_eager_execution()
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

class DQNAgent:

    def __init__(self, state_shape, action_size,verbose,param):

        self.state_shape = state_shape
        self.action_size = action_size
        self.steps = 0

        self.save_model_dir = param['save_model_dir']
        self.brain_name = param['brain_name']
        self.target_brain_name = param['target_brain_name']
        self.train_step = param['train_step']
        self.learning_rate = param['learning_rate']
        self.gamma = param['gamma']
        self.epsilon = param['epsilon']
        self.epsilon_min = param['epsilon_min']
        self.epsilon_decay = param['epsilon_decay']
        self.batch_size = param['batch_size']
        self.train_start_memory_size = param["train_start_memory_size"]

        self.verbose = verbose
        self.brain = self.build_model()
        self.target_brain = self.build_model()
        self.update_target_brain()

        self.memory = deque()
        self.memory_size = param['memory_size']

        if not os.path.exists(self.save_model_dir):
            os.mkdir(self.save_model_dir)

        if not os.path.exists(os.path.join(self.save_model_dir, self.brain_name)):
            os.mkdir(os.path.join(self.save_model_dir, self.brain_name))

        if not os.path.exists(os.path.join(self.save_model_dir, self.target_brain_name)):
            os.mkdir(os.path.join(self.save_model_dir, self.target_brain_name))

    def build_model(self):
        input_x = Input(self.state_shape)
        conv1 = Conv2D(16, (8, 8), strides=4, activation='relu')(input_x)
        conv2 = Conv2D(32, (4, 4), strides=2, activation='relu')(conv1)
        flatten = Flatten()(conv2)
        fc1 = Dense(256, activation='relu')(flatten)
        output = Dense(self.action_size)(fc1)

        model = Model(input_x, output)
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_brain(self):
        self.target_brain.set_weights(self.brain.get_weights())

    def get_act(self, state):

        if np.random.rand() <= self.epsilon:
            rand_axis = random.randrange(self.action_size)
            return rand_axis

        state = state[np.newaxis]

        action_predict = self.brain.predict(np.asarray(state))
        model_action = np.argmax(action_predict[0])

        return model_action

    def get_test_act_(self, state):

        state = state[np.newaxis]
        action_predict = self.brain.predict(np.asarray(state))
        model_action = np.argmax(action_predict[0])

        return model_action

    def add_memory(self, state, action, reward, next_state, done):

        self.memory.append((state, action, reward, next_state, done))
        if (len(self.memory) > self.memory_size):
            self.memory.popleft()

    def train(self):

        if (len(self.memory) >= self.batch_size and self.steps >= self.train_step):

            sample = random.sample(self.memory, self.batch_size)
            states = np.asarray([idx[0] for idx in sample])
            next_states = np.asarray([idx[3] for idx in sample])
            next_q_values = self.target_brain.predict_on_batch(next_states)
            current_q_values = self.brain.predict_on_batch(states)

            for i in range(self.batch_size):
                _, action, reward, _, done = sample[i]

                if not done:
                    next_q_value = reward + self.gamma * np.amax(next_q_values[i])
                else:
                    next_q_value = reward

                current_q_values[i, action] = next_q_value

            self.brain.fit(states, current_q_values, batch_size=self.batch_size, epochs=1, verbose=0, shuffle=False)
            self.save_model()
            self.steps = 0

            if(self.verbose):
                print("log >> model train")

        elif(self.steps < self.train_step):
            self.steps += 1

    def epsilon_update(self):
        if self.epsilon > self.epsilon_min:
            pre = self.epsilon
            self.epsilon *= self.epsilon_decay
            if (self.verbose):
                print(f"log >> epsilon_update {pre} -> {self.epsilon}")

    def save_model(self):

        self.brain.save_weights(os.path.join(self.save_model_dir, self.brain_name))
        self.target_brain.save(os.path.join(self.save_model_dir, self.target_brain_name))

    def load_model(self):
        self.brain.load_weights(os.path.join(self.save_model_dir, self.brain_name))
        self.target_brain.load_weights(os.path.join(self.save_model_dir, self.brain_name))

    def get_test_act(self, state):
        pass