import random

from classes.Collider import Collider


class LeftRightWalkTrait:
    def __init__(self, entity, level):
        self.direction = random.choice([-1, 1])
        self.entity = entity
        self.level = level
        self.collDetection = Collider(self.entity, level)
        self.speed = 1
        self.entity.vel.x = self.speed * self.direction

    def update(self):
        if self.entity.vel.x == 0:
            self.direction *= -1
        self.entity.vel.x = self.speed * self.direction
        self.moveEntity()

    def check_sky(self):
        if self.entity.__class__.__name__ == 'Goomba':
            if self.direction == -1:
                if self.entity.getPosIndexAsFloat().x * 10 % 10 < 0.5:
                    y = self.entity.getPosIndex().x + self.direction
                else:
                    y = self.entity.getPosIndex().x
            else:
                y = self.entity.getPosIndex().x + self.direction
            tiles = self.level.level[self.entity.getPosIndex().y + 1][y]
            if tiles.id == 'sky':
                self.direction *= -1
                self.entity.vel.x = self.speed * self.direction
        elif self.entity.__class__.__name__ == 'Koopa':
            if self.direction == -1:
                if self.entity.getPosIndexAsFloat().x * 10 % 10 < 0.5:
                    y = self.entity.getPosIndex().x + self.direction
                else:
                    y = self.entity.getPosIndex().x
            else:
                y = self.entity.getPosIndex().x + self.direction
            tiles = self.level.level[self.entity.getPosIndex().y + 1][y]
            if tiles.id == 'sky' and self.entity.active:
                self.direction *= -1
                self.entity.vel.x = self.speed * self.direction

    def moveEntity(self):
        self.entity.rect.y += self.entity.vel.y
        self.collDetection.checkY()
        self.entity.rect.x += self.entity.vel.x
        self.collDetection.checkX()
        if self.entity.__class__.__name__ in ['Goomba', 'Koopa']:
            self.check_sky()
