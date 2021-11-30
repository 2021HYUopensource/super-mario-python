from classes.Maths import Vec2D


class Camera:
    '''
    화면을 캐릭터에 따라 움직여주는 카메라 클래스
    '''
    def __init__(self, pos, entity, length):
        self.pos = Vec2D(pos.x, pos.y)
        self.entity = entity
        self.x = self.pos.x * 32
        self.y = self.pos.y * 32
        self.length = length

    def move(self):
        '''
        카메라를 케릭터에 맞게 움직여주는 함수
        '''
        xPosFloat = self.entity.getPosIndexAsFloat().x
        if 10 < xPosFloat < self.length - 10:
            self.pos.x = -xPosFloat + 10
        self.x = self.pos.x * 32
        self.y = self.pos.y * 32
