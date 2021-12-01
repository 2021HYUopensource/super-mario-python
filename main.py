import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario


windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()

    while not mario.over:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            if mario.win:
                mario.winObj.update()
                if mario.restart:
                    restart_name = level.name
                    level = Level(screen, sound, dashboard)
                    menu = Menu(screen, dashboard, level, sound)
                    menu.inChoosingLevel = False
                    menu.dashboard.state = "start"
                    menu.dashboard.time = 0
                    menu.level.loadLevel(restart_name)
                    menu.dashboard.levelName = restart_name
                    menu.start = True
                    mario = Mario(0, 0, level, screen, dashboard, sound)
                    clock = pygame.time.Clock()
            else:
                mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
