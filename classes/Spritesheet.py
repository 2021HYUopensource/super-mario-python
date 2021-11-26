import pygame


class Spritesheet(object):
    '''
    스프라이트를 로딩하는 클래스

    :ivar filePath: 텍스트 파일 경로
    '''
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    def image_at(self, x, y, scalingfactor, colorkey=None, ignoreTileSize=False,
                 xTileSize=16, yTileSize=16):
        '''
        스프라이트 이미지를 하나씩 잘라서 리턴하는 함수

        :param x: 가져올 스프라이트 가로 픽셀 위치
        :type x: int
        :param y: 가져올 스프라이트 세로 픽셀 위치
        :type y: int
        :param scalingfactor: 이미지 스케일 변경 배수
        :type scalingfactor: int
        :param colorkey: 투명하게 만들 뒷 배경 컬러
        :type colorkey: pygame.color.Color | list[int]
        :param ignoreTileSize: 타이틀 무시 여부
        :type ignoreTileSize: bool
        :param xTileSize: 타이틀 가로 사이즈. ignoreTileSize=True일 경우, backround에서 사용 될 스프라이트의 반봇 횟수로도 쓰임
        :param yTileSize: 타이틀 세로 사이즈. ignoreTileSize=True일 경우, backround에서 사용 될 스프라이트의 반봇 횟수로도 쓰임
        :return: scale된 이미지 리턴
        :rtype: pygame.Surface
        '''
        if ignoreTileSize:
            rect = pygame.Rect((x, y, xTileSize, yTileSize))
        else:
            rect = pygame.Rect((x * xTileSize, y * yTileSize, xTileSize, yTileSize))
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        )
