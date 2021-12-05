import gym
import cv2
import numpy as np
from collections import deque
#https://github.com/rjalnev/DDDQN/blob/master/wrappers.py

class Rgb2Gray(gym.ObservationWrapper):
    def __init__(self, env):
        gym.ObservationWrapper.__init__(self, env)
        (oldh, oldw, _oldc) = env.observation_space.shape
        self.observation_space = gym.spaces.Box(low=0, high=255,
                                                shape=(oldh, oldw, 1),
                                                dtype=np.uint8)

    def observation(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame[:, :, None]


class SkipFrames(gym.Wrapper):
    def __init__(self, env, n=4):
        gym.Wrapper.__init__(self, env)
        self.n = n

    def step(self, action):
        done = False
        totalReward = 0.0
        for _ in range(self.n):
            obs, reward, done, info = self.env.step(action)
            totalReward += reward
            if done:
                break
        return obs, totalReward, done, info


class FrameStack(gym.Wrapper):
    def __init__(self, env, k):
        gym.Wrapper.__init__(self, env)
        (oldh, oldw, _oldc) = env.observation_space.shape
        newStackShape = (oldh, oldw, k)
        self.observation_space = gym.spaces.Box(low=0, high=255,
                                                shape=newStackShape,
                                                dtype=np.uint8)
        self.k = k
        self.frames = deque([], maxlen=k)

    def reset(self):
        obs = self.env.reset()
        for _ in range(self.k):
            self.frames.append(obs)
        return self._get_obs()

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self.frames.append(obs)
        return self._get_obs(), reward, done, info

    def _get_obs(self):
        assert len(self.frames) == self.k
        return np.concatenate(self.frames, axis=2)


class ScaledFloatFrame(gym.ObservationWrapper):
    def __init__(self, env):
        gym.ObservationWrapper.__init__(self, env)
        self.observation_space = gym.spaces.Box(low=np.float32(0), high=np.float32(1),
                                                shape=env.observation_space.shape,
                                                dtype=np.float32)

    def observation(self, observation):
        return np.array(observation).astype(np.float32) / 255.0