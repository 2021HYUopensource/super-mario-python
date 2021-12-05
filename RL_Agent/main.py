from Agents.creator import create_agent_main_sys
import numpy as np
from utils.img_preprocessing import make_stack
from ..classes.LearningEnv import SuperMario

env = SuperMario.make()

# TODO: state size = 84 * 84 * 4

# TODO: 내가 만든 환경 적용 - env
ppo = create_agent_main_sys("PPO",env,env.state_shape(),4,True)

ppo.train(10000, 10000000)