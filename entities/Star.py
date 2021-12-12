from copy import copy

from entities.EntityBase import EntityBase


class Star(EntityBase):
    '''
    승리 조건인 스타를 그리는 함수
    '''
    def __init__(self, screen, spriteCollection, x, y, gravity=0):
        super(Star, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("star").animation)
        self.type = "Star"

    def update(self, cam):
        '''
        스타의 모습을 업데이트 하는 함수
        '''
        if self.alive:
            self.animation.update()
            self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y))
