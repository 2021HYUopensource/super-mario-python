import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario

from RL_Agent.Agents.creator import create_agent_main_sys
from classes.LearningEnv import SuperMario
import cv2

windowSize = 640, 480
rl_repeat_time = 2
max_frame_rate = 60
action_size = 4


def game_rl_mode(screen, menu, sound, level, dashboard):
    sound.rl_mode = True
    env = SuperMario().make(action_size)
    ppo = create_agent_main_sys("PPO", env, env.state_shape(), action_size, True)
    ppo.train(10000, 10000000, screen, menu, sound, level, dashboard)
    return 'restart'

def game_player_mode(screen, menu, sound, level, dashboard):
    mario = Mario(0, 12, level, screen, dashboard, sound, menu.rl_mode)
    clock = pygame.time.Clock()

    count = 1
    while True:
        if mario.over:
            break
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            if mario.win:
                mario.winObj.update()
                if mario.restart:
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
                    clock = pygame.time.Clock()
                    count += 1
            else:
                mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        pygame.display.update()
        clock.tick_busy_loop(max_frame_rate)
    return 'restart'

def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound(False)
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    if menu.rl_mode:
        return game_rl_mode(screen, menu, sound, level, dashboard)
    else:
        return game_player_mode(screen, menu, sound, level, dashboard)

if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
