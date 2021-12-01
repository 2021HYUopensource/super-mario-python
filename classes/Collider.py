class Collider:
    '''
    맵 오브젝트 충돌 판정에 관여하는 클래스
    '''
    def __init__(self, entity, level):
        self.entity = entity
        self.level = level.level
        self.level_ = level
        self.levelObj = level
        self.result = []

    def checkX(self):
        '''
        가로 충돌 여부 체크 함수

        :raise Exception: level 인덱스 범위를 넘길때 예외 발생
        '''
        if self.leftLevelBorderReached() or self.rightLevelBorderReached():
            return
        try:
            rows = [
                self.level[self.entity.getPosIndex().y],
                self.level[self.entity.getPosIndex().y + 1],
                self.level[self.entity.getPosIndex().y + 2],
            ]
        except Exception:
            return
        for row in rows:
            tiles = row[self.entity.getPosIndex().x : self.entity.getPosIndex().x + 2]
            for tile in tiles:
                if tile.rect is not None:
                    if self.entity.rect.colliderect(tile.rect):
                        if self.entity.vel.x > 0:
                            self.entity.rect.right = tile.rect.left
                            self.entity.vel.x = 0
                        if self.entity.vel.x < 0:
                            self.entity.rect.left = tile.rect.right
                            self.entity.vel.x = 0

    def checkY(self):
        '''
        세로 충돌 여부 체크 험수

        :raise Exception: level 인덱스 범위를 넘길때/게임 오버 될 때 예외 발생
        '''
        self.entity.onGround = False
        
        try:
            rows = [
                self.level[self.entity.getPosIndex().y],
                self.level[self.entity.getPosIndex().y + 1],
                self.level[self.entity.getPosIndex().y + 2],
            ]
        except Exception:
            try:
                self.entity.gameOver()
            except Exception:
                self.entity.alive = None
            return
        for row in rows:
            tiles = row[self.entity.getPosIndex().x : self.entity.getPosIndex().x + 2]
            for tile in tiles:
                if tile.rect is not None:
                    if self.entity.rect.colliderect(tile.rect):
                        if self.entity.vel.y > 0:
                            self.entity.onGround = True
                            self.entity.rect.bottom = tile.rect.top
                            self.entity.vel.y = 0
                            # reset jump on bottom
                            if self.entity.traits is not None:
                                if "JumpTrait" in self.entity.traits:
                                    self.entity.traits["JumpTrait"].reset()
                                if "bounceTrait" in self.entity.traits:
                                    self.entity.traits["bounceTrait"].reset()
                        if self.entity.vel.y < 0:
                            self.entity.rect.top = tile.rect.bottom
                            self.entity.vel.y = 0

    def rightLevelBorderReached(self):
        '''
        맵 오른쪽 끝에 닿았는지 여부 체크

        :return: 맵 오른쪽 끝 충돌 여부
        :rtype: bool
        '''
        if self.entity.getPosIndexAsFloat().x > self.levelObj.levelLength - 1:
            self.entity.rect.x = (self.levelObj.levelLength - 1) * 32
            self.entity.vel.x = 0
            return True

    def leftLevelBorderReached(self):
        '''
        맵 왼쪽 끝에 닿았는지 여부 체크

        :return: 맵 왼쪽 끝 충돌 여부
        :rtype: bool
        '''
        if self.entity.rect.x < 0:
            self.entity.rect.x = 0
            self.entity.vel.x = 0
            return True
