import pygame

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Sprites import Sprites
from classes.Win import Win
from entities.EntityBase import EntityBase
from entities.Mushroom import RedMushroom
from traits.bounce import bounceTrait
from traits.go import GoTrait
from traits.jump import JumpTrait
from classes.Pause import Pause

spriteCollection = Sprites().spriteCollection
smallAnimation = Animation(
    [
        spriteCollection["mario_run1"].image,
        spriteCollection["mario_run2"].image,
        spriteCollection["mario_run3"].image,
    ],
    spriteCollection["mario_idle"].image,
    spriteCollection["mario_jump"].image,
)
bigAnimation = Animation(
    [
        spriteCollection["mario_big_run1"].image,
        spriteCollection["mario_big_run2"].image,
        spriteCollection["mario_big_run3"].image,
    ],
    spriteCollection["mario_big_idle"].image,
    spriteCollection["mario_big_jump"].image,
)


class Mario(EntityBase):
    '''
    플레이어인 마리오를 그리는 함수
    '''
    def __init__(self, x, y, level, screen, dashboard, sound, rl_mode, gravity=0.8):
        super(Mario, self).__init__(x, y, gravity)
        self.camera = Camera(self.rect, self, level.levelLength)
        self.sound = sound
        self.input = Input(self)
        self.inAir = False
        self.inJump = False
        self.powerUpState = 0
        self.invincibilityFrames = 0
        self.rl_mode = rl_mode
        self.traits = {
            "jumpTrait": JumpTrait(self),
            "goTrait": GoTrait(smallAnimation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self),
        }

        self.levelObj = level
        self.collision = Collider(self, level)
        self.screen = screen
        self.EntityCollider = EntityCollider(self)
        self.dashboard = dashboard
        self.over = False
        self.restart = False
        self.pause = False
        self.win = False
        self.pauseObj = Pause(screen, self, dashboard)
        self.winObj = Win(screen, self, dashboard, level)

    def update(self):
        '''
        마리오의 모습을 업데이트 하는 함수
        '''
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
        self.updateTraits()
        self.moveMario()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.input.checkForInput()

    def moveMario(self):
        '''
        게임 안에서 마리오의 위치를 변경하는 함수
        '''
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def checkEntityCollision(self):
        '''
        마리오와 엔티티의 충돌 여부를 체크하는 함수
        '''
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)
                elif ent.type == "Star":
                    self._onCollisionWithStar(ent)

    def _onCollisionWithItem(self, item):
        '''
        아이템과 충돌했을때 관여하는 함수

        :param item: 충돌한 아이템 이름
        '''
        self.levelObj.entityList.remove(item)
        self.dashboard.points += 100
        self.dashboard.coins += 1
        self.sound.play_sfx(self.sound.coin)

    def _onCollisionWithStar(self, star):
        self.levelObj.entityList.remove(star)
        self.sound.play_sfx(self.sound.end)
        self.win = True
        self.pause = True
        if self.rl_mode:
            self.restart = True
        else:
            self.winObj.createBackgroundBlur()
            self.winObj.update()

    def _onCollisionWithBlock(self, block):
        '''
        블록과 충돌했을때 관여하는 함수

        :param block: 충돌한 불록 이름
        '''
        if not block.triggered:
            self.dashboard.coins += 1
            self.sound.play_sfx(self.sound.bump)
        block.triggered = True

    def _onCollisionWithMob(self, mob, collisionState):
        '''
        몹과 충돌했을때 관여하는 함수

        :param mob: 충돌한 몹 이름
        :param collisionState: 충돌 상태 상태 판별(등딱지에 숨은 거북/아닌 거북 등)
        :return:
        '''
        if isinstance(mob, RedMushroom) and mob.alive:
            self.powerup(1)
            self.killEntity(mob,True)
            self.sound.play_sfx(self.sound.powerup)
        elif collisionState.isTop and (mob.alive or mob.bouncing):
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            if not mob.active and not mob.bouncing:
                self.killEntity(mob, False)
            else:
                self.killEntity(mob, True)
        elif collisionState.isTop and mob.alive and not mob.active:
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            mob.timer = 0
            self.bounce()
            mob.alive = False
            print('now')
        elif collisionState.isColliding and mob.alive and not mob.active and not mob.bouncing:
            mob.bouncing = True
            if mob.rect.x < self.rect.x:
                mob.leftrightTrait.direction = -1
                mob.rect.x += -5
                self.sound.play_sfx(self.sound.kick)
            else:
                mob.rect.x += 5
                mob.leftrightTrait.direction = 1
                self.sound.play_sfx(self.sound.kick)
        elif collisionState.isColliding and mob.alive and not self.invincibilityFrames:
            if self.powerUpState == 0:
                self.gameOver()
            elif self.powerUpState == 1:
                self.powerUpState = 0
                self.traits['goTrait'].updateAnimation(smallAnimation)
                x, y = self.rect.x, self.rect.y
                self.rect = pygame.Rect(x, y + 32, 32, 32)
                self.invincibilityFrames = 60
                self.sound.play_sfx(self.sound.pipe)

    def bounce(self):
        '''
        점프 상태를 업데이트하는 함수
        '''
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent, state):
        '''
        앤티티를 죽였을때 동작하는 함수

        :param ent: 죽인 엔티티 이름
        '''
        if ent.__class__.__name__ != "Koopa":
            ent.alive = False
        else:
            ent.timer = 0
            ent.leftrightTrait.speed = 1
            ent.alive = True
            ent.active = False
            ent.bouncing = False
        if state and not ent.already:
            ent.already = True
            self.dashboard.points += 100

    def gameOver(self):
        '''
        게임 오버가 됬을때 동작하는 함수
        '''
        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.sound.music_channel.stop()
        if not self.rl_mode:
            self.sound.music_channel.play(self.sound.death)

        for i in range(500, 20, -2):
            srf.fill((0, 0, 0))
            pygame.draw.circle(
                srf,
                (255, 255, 255),
                (int(self.camera.x + self.rect.x) + 16, self.rect.y + 16),
                i,
            )
            self.screen.blit(srf, (0, 0))
            pygame.display.update()
            self.input.checkForInput()
        while self.sound.music_channel.get_busy():
            pygame.display.update()
            self.input.checkForInput()
        self.over = True

    def getPos(self):
        '''
        마리오의 위치를 가져오는 함수
        '''
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self, x, y):
        '''
        마리오의 위치를 지정하는 함수

        :param x: 마리오의 가로 위치
        :param y: 마리오의 세로 위치
        '''
        self.rect.x = x
        self.rect.y = y
        
    def powerup(self, powerupID):
        '''
        작은 마리오가 커질때 동작하는 함수

        :param powerupID: 파워 단계
        '''
        if self.powerUpState == 0:
            if powerupID == 1:
                self.powerUpState = 1
                self.traits['goTrait'].updateAnimation(bigAnimation)
                self.rect = pygame.Rect(self.rect.x, self.rect.y-32, 32, 64)
                self.invincibilityFrames = 20
