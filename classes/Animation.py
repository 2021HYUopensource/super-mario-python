class Animation:
    '''
    엔티티 상태에 따른 스프라이트를 관여하는 클래스
    '''
    def __init__(self, images, idleSprite=None, airSprite=None, deltaTime=7):
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = self.images[self.index]
        self.idleSprite = idleSprite
        self.airSprite = airSprite
        self.deltaTime = deltaTime

    def update(self):
        '''
        엔티티 상태에 따라 스프라이트를 업데이트 하는 함수
        '''
        self.timer += 1
        if self.timer % self.deltaTime == 0:
            if self.index < len(self.images) - 1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.images[self.index]

    def idle(self):
        '''
        공중에 뜨지 않았을때 스프라이트로 변경
        '''
        self.image = self.idleSprite

    def inAir(self):
        '''
        공중에 떴을때 스프라이트로 변경
        '''
        self.image = self.airSprite
