from classes.Pause import Pause
import pygame
import sys

class Win(Pause):

    def __init__(self, screen, entity, dashboard, level):
        super(Win, self).__init__(screen, entity, dashboard)
        self.level = level

    def update(self):
        '''
        이긴 화면 업데이트 함수
        '''
        self.screen.blit(self.pause_srfc, (0, 0))
        self.dashboard.drawText("You Win!", 80, 160, 68)
        self.dashboard.drawText("RETRY", 150, 280, 32)
        self.dashboard.drawText("BACK TO MENU", 150, 320, 32)
        self.drawDot()
        pygame.display.update()
        self.checkInput()

    def checkInput(self):
        '''
        이긴 화면에서의 키 입력에 관여하는 함수
        '''
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state == 0:
                        self.entity.restart = True
                    elif self.state == 1:
                        self.entity.over = True
                elif event.key == pygame.K_UP:
                    if self.state > 0:
                        self.state -= 1
                elif event.key == pygame.K_DOWN:
                    if self.state < 1:
                        self.state += 1