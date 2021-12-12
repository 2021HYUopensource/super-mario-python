from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait


class Goomba(EntityBase):
    '''
    굼바 엔티티에 관여하는 클래스
    '''
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(Goomba, self).__init__(y, x - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("goomba-1").image,
                self.spriteCollection.get("goomba-2").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound
        self.textPos = Vec2D(0, 0)

    def update(self, camera):
        '''
        굼바 엔티티의 상태를 업데이트 하는 함수
        '''
        if self.alive:
            self.applyGravity()
            self.drawGoomba(camera)
            self.leftrightTrait.update()
            self.checkEntityCollision()
        else:
            self.onDead(camera)

    def drawGoomba(self, camera):
        '''
        굼바 엔티티를 그리는 함수
        '''
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y))
        self.animation.update()

    def onDead(self, camera):
        '''
        굼바 엔티티가 밟혀 사망했을 때 작용하는 함수
        '''
        if self.timer == 0:
            self.setPointsTextStartPosition(self.rect.x + 3, self.rect.y)
        if self.timer < self.timeAfterDeath:
            self.movePointsTextUpAndDraw(camera)
            self.drawFlatGoomba(camera)
        else:
            self.alive = None
        self.timer += 0.1

    def drawFlatGoomba(self, camera):
        '''
        밟혀서 사망한 굼바 엔티티를 그리는 함수
        '''
        self.screen.blit(
            self.spriteCollection.get("goomba-flat").image,
            (self.rect.x + camera.x, self.rect.y),
        )

    def setPointsTextStartPosition(self, x, y):
        self.textPos = Vec2D(x, y)

    def movePointsTextUpAndDraw(self, camera):
        self.textPos.y += -0.5
        self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8)
    
    def checkEntityCollision(self):
        '''
        다른 엔티티와 충돌했는지 판정하는 함수
        '''
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithMob(self, mob, collisionState):
        '''
        다른 몹과 충돌했을때 관여하는 함수

        :param mob: 충돌한 몹 이름
        :param collisionState: 충돌 상태 상태 판별(등딱지에 숨은 거북/아닌 거북 등)
        '''
        if collisionState.isColliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
