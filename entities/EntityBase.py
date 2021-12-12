import pygame

from classes.Maths import Vec2D


class EntityBase(object):
    '''
    다른 엔티티의 속성들(attributes)을 정의하는 EntityBase에 대한 함수

    :ivar x: 엔티티의 x 좌표
    :ivar y: 엔티티의 y 좌표
    :ivar gravity: 엔티티에 적용된 중력 값
    '''
    def __init__(self, x, y, gravity):
        self.vel = Vec2D()
        self.rect = pygame.Rect(x * 32, y * 32, 32, 32)
        self.gravity = gravity
        self.traits = None
        self.alive = True
        self.active = True
        self.already = False
        self.bouncing = False
        self.timeAfterDeath = 5
        self.timer = 0
        self.type = ""
        self.onGround = False
        self.obeyGravity = True
        
    def applyGravity(self):
        '''
        엔티티의 y방향 속력을 변화시키는 중력을 적용하는 함수
        '''
        if self.obeyGravity:
            self.vel.y += self.gravity

    def updateTraits(self):
        '''
        엔티티의 속성 값을 업데이트 하는 함수
        '''
        for trait in self.traits.values():
            try:
                trait.update()
            except AttributeError:
                pass

    def getPosIndex(self):
        '''
        엔티티의 좌표를 정수형으로 반환하는 함수

        :return:엔티티의 좌표
        :rtype:Vec2D
        '''
        return Vec2D(self.rect.x // 32, self.rect.y // 32)

    def getPosIndexAsFloat(self):
        '''
        엔티티의 좌표를 받아서 실수 형태로 반환하는 함수

        :return:엔티티의 실수 좌표
        :rtype:Vec2D
        '''
        return Vec2D(self.rect.x / 32.0, self.rect.y / 32.0)
