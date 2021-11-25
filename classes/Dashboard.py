import pygame

from classes.Font import Font


class Dashboard(Font):
    '''
    전체적인 화면 출력에 관여하는 클래스. :class:`Font` 의 하위 클래스

    :ivar filePath: 텍스트 파일 경로
    :ivar size: 텍스트 size (안 쓰이는 파라미터)
    :ivar screen: 출력할 화면
    '''
    def __init__(self, filePath:str,
                 size:int,
                 screen:pygame.Surface):
        Font.__init__(self, filePath, size)
        self.state = "menu"
        self.screen = screen
        self.levelName = ""
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0

    def update(self):
        '''
        화면을 업데이트 하는 함수
        '''
        self.drawText("MARIO", 50, 20, 15)
        self.drawText(self.pointString(), 50, 37, 15)

        self.drawText("@x{}".format(self.coinString()), 225, 37, 15)

        self.drawText("WORLD", 380, 20, 15)
        self.drawText(str(self.levelName), 395, 37, 15)

        self.drawText("TIME", 520, 20, 15)
        if self.state != "menu":
            self.drawText(self.timeString(), 535, 37, 15)

        # update Time
        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def drawText(self, text, x, y, size):
        '''
        화면에 글자를 그리는 함수

        :param text: 출력할 텍스트
        :type text: str
        :param x: 출력할 가로 위치
        :type x: int
        :param y: 출력할 세로 위치
        :type y: int
        :param size: 출력할 텍스트 크기
        :type size: int
        '''
        for char in text:
            charSprite = pygame.transform.scale(self.charSprites[char], (size, size))
            self.screen.blit(charSprite, (x, y))
            if char == " ":
                x += size//2
            else:
                x += size

    def coinString(self):
        '''
        :return: 코인 출력 포멧
        :rtype: str
        '''
        return "{:02d}".format(self.coins)

    def pointString(self):
        '''
        :return: 점수 출력 포멧
        :rtype: str
        '''
        return "{:06d}".format(self.points)

    def timeString(self):
        '''
        :return: 남은 시간 출력 포멧
        :rtype: str
        '''
        return "{:03d}".format(self.time)
