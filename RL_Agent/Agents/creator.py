from ..PPO.PPO_main_sys import create_ppo_main_sys

def create_agent_main_sys(model,env,state_shape, action_size,verbose):
    if (model == "PPO"):
        main_sys = create_ppo_main_sys(env, state_shape, action_size,verbose)
        return main_sys