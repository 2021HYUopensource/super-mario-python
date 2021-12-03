import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario

from RL_Agent.Agents.creator import create_agent_main_sys
from classes.LearningEnv import SuperMario


windowSize = 640, 480
rl_repeat_time = 2


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound(False)
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    if menu.rl_mode:
        max_frame_rate = 4
        sound.rl_mode = True

    mario = Mario(0, 12, level, screen, dashboard, sound, menu.rl_mode)
    clock = pygame.time.Clock()

    count = 1
    a = 0
    while True:
        if mario.over:
            if menu.rl_mode and mario.rl_mode:
                if count == rl_repeat_time:
                    break
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
        if menu.rl_mode:
            pygame.time.delay(10)
        else:
            clock.tick_busy_loop(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
