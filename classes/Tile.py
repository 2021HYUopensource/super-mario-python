import pygame


class Tile:
    '''
    배경 스프라이트 그리는 클래스
    '''
    def __init__(self, sprite, rect, id):
        self.sprite = sprite
        self.rect = rect
        self.id = id

    def drawRect(self, screen):
        '''
        배경 스프라이트 그리는 함수
        :param screen: 그릴 화면
        :type screen: pygame.Surface
        '''
        try:
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), self.rect, 1)
        except Exception:
            pass