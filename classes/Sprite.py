class Sprite:
    '''
    스프라이트를 그리는 클래스
    '''
    def __init__(self, image, colliding, animation=None, redrawBackground=False):
        self.image = image
        self.colliding = colliding
        self.animation = animation
        self.redrawBackground = redrawBackground

    def drawSprite(self, x, y, screen):
        '''
        스프라이트를 그리는 함수

        :param x: 그릴 가로 위치
        :type x: int
        :param y: 그릴 세로 위치
        :type y: int
        :param screen: 그릴 스크린
        :type screen: pygame.Surface
        '''
        dimensions = (x * 32, y * 32)
        if self.animation is None:
            screen.blit(self.image, dimensions)
        else:
            self.animation.update()
            screen.blit(self.animation.image, dimensions)
