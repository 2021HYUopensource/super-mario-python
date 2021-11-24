from classes.Spritesheet import Spritesheet
import pygame


class Font(Spritesheet):
    '''
    Font를 로딩하는 클래스. :class:`Spritesheet` 의 하위클래스.

    :ivar filePath: 텍스트 파일 경로
    :ivar size: 텍스트 size (안 쓰이는 파라미터)
    '''
    def __init__(self, filePath:str,
                 size:int):
        Spritesheet.__init__(self, filename=filePath)
        self.chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        self.charSprites = self.loadFont()

    def loadFont(self):
        '''
        폰트를 로딩하는 함수.

        :return: 폰트 스프라이트 리턴
        '''
        font = {}
        row = 0
        charAt = 0

        for char in self.chars:
            if charAt == 16:
                charAt = 0
                row += 1
            font.update(
                {
                    char: self.image_at(
                        charAt,
                        row,
                        2,
                        colorkey=pygame.color.Color(0, 0, 0),
                        xTileSize=8,
                        yTileSize=8
                    )
                }
            )
            charAt += 1
        return font
