import pygame

from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait


class Koopa(EntityBase):
    '''
    보스인 쿠파 엔티티에 관한 클래스
    '''
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(Koopa, self).__init__(y - 1, x, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("koopa-1").image,
                self.spriteCollection.get("koopa-2").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.timer = 0
        self.timeAfterDeath = 35
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound

    def update(self, camera):
        '''
        쿠파의 모습을 업데이트하는 함수
        :param camera:카메라 클래스
        '''
        if self.alive and self.active:
            self.updateAlive(camera)
            self.checkEntityCollision()
        elif self.alive and not self.active and not self.bouncing:
            self.sleepingInShell(camera)
            self.checkEntityCollision()
        elif self.bouncing:
            self.shellBouncing(camera)

    def drawKoopa(self, camera):
        if self.leftrightTrait.direction == -1:
            self.screen.blit(
                self.animation.image, (self.rect.x + camera.x, self.rect.y - 32)
            )
        else:
            self.screen.blit(
                pygame.transform.flip(self.animation.image, True, False),
                (self.rect.x + camera.x, self.rect.y - 32),
            )

    def shellBouncing(self, camera):
        self.leftrightTrait.speed = 4
        self.applyGravity()
        self.animation.image = self.spriteCollection.get("koopa-hiding").image
        self.drawKoopa(camera)
        self.leftrightTrait.update()

    def sleepingInShell(self, camera):
        if self.timer < self.timeAfterDeath:
            self.screen.blit(
                self.spriteCollection.get("koopa-hiding").image,
                (self.rect.x + camera.x, self.rect.y - 32),
            )
        else:
            self.alive = True
            self.active = True
            self.bouncing = False
            self.timer = 0
        self.timer += 0.1

    def updateAlive(self, camera):
        self.applyGravity()
        self.drawKoopa(camera)
        self.animation.update()
        self.leftrightTrait.update()

    def checkEntityCollision(self):
        '''
        쿠파와 엔티티의 충돌 여부를 체크하는 함수
        '''
        for ent in self.levelObj.entityList:
            if ent is not self:
                collisionState = self.EntityCollider.check(ent)
                if collisionState.isColliding:
                    if ent.type == "Mob":
                        self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithMob(self, mob, collisionState):
        '''
        몹과 충돌했을때 관여하는 함수
        :param mob: 충돌한 몹 이름
        :param collisionState: 충돌 상태 판별(등딱지에 숨은 거북/아닌 거북 등)
        '''
        if collisionState.isColliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
