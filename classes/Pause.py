import pygame
import sys

from classes.Spritesheet import Spritesheet
from classes.GaussianBlur import GaussianBlur

class Pause:
    '''
    정지 화면에 관여하는 클래스
    '''
    def __init__(self, screen, entity, dashboard):
        self.screen = screen
        self.entity = entity
        self.dashboard = dashboard
        self.state = 0
        self.spritesheet = Spritesheet("./img/title_screen.png")
        self.pause_srfc = GaussianBlur().filter(self.screen, 0, 0, 640, 480)
        self.dot = self.spritesheet.image_at(
            0, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.gray_dot = self.spritesheet.image_at(
            20, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )

    def update(self):
        '''
        정지 화면 업데이트 함수
        '''
        self.screen.blit(self.pause_srfc, (0, 0))
        self.dashboard.drawText("PAUSED", 120, 160, 68)
        self.dashboard.drawText("CONTINUE", 150, 280, 32)
        self.dashboard.drawText("BACK TO MENU", 150, 320, 32)
        self.drawDot()
        pygame.display.update()
        self.checkInput()

    def drawDot(self):
        '''
        정지 화면에서 선택지를 보여주는 함수
        '''
        if self.state == 0:
            self.screen.blit(self.dot, (100, 275))
            self.screen.blit(self.gray_dot, (100, 315))
        elif self.state == 1:
            self.screen.blit(self.dot, (100, 315))
            self.screen.blit(self.gray_dot, (100, 275))

    def checkInput(self):
        '''
        정지 화면에서의 키 입력에 관여하는 함수
        '''
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state == 0:
                        self.entity.pause = False
                    elif self.state == 1:
                        self.entity.restart = True
                elif event.key == pygame.K_UP:
                    if self.state > 0:
                        self.state -= 1
                elif event.key == pygame.K_DOWN:
                    if self.state < 1:
                        self.state += 1

    def createBackgroundBlur(self):
        '''
        배경 가우시안 블러 효과를 적용하는 함수
        '''
        self.pause_srfc = GaussianBlur().filter(self.screen, 0, 0, 640, 480)
