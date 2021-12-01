import json
import pygame

from classes.Sprites import Sprites
from classes.Tile import Tile
from entities.Coin import Coin
from entities.Star import Star
from entities.CoinBrick import CoinBrick
from entities.Goomba import Goomba
from entities.Mushroom import RedMushroom
from entities.Koopa import Koopa
from entities.CoinBox import CoinBox
from entities.RandomBox import RandomBox


class Level:
    '''
    레벨 파일에서 가져온 데이터로 플레이 할 스테이지를 화면에 출력하는 클래스
    '''
    def __init__(self, screen, sound, dashboard):
        self.sprites = Sprites()
        self.dashboard = dashboard
        self.sound = sound
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = []
        self.name = ''

    def loadLevel(self, levelname):
        '''
        레벨 json 파일을 읽어와 구성요소를 파싱하는 함수

        :param levelname: 로딩할 레벨 이름
        :type levelname: str
        '''
        with open("./levels/{}.json".format(levelname)) as jsonData:
            data = json.load(jsonData)
            self.loadLayers(data)
            self.loadObjects(data)
            self.loadEntities(data)
            self.levelLength = data["length"]
            self.name = levelname

    def loadEntities(self, data):
        '''
        맵 json 데이터에서 엔티티(CoinBox, Goomba, Koopa, Coin, coinBrick, RandomBox) 추출하는 함수

        :param data: 맵 json 데이터
        :type data: dict
        :raise Exception: 엔티티가 레벨 안에 없을때 발생
        '''
        try:
            [self.addCoinBox(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            [self.addStar(x, y) for x, y in data["level"]["entities"]["star"]]
            [self.addCoinBrick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            [self.addRandomBox(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
        except:
            # if no entities in Level
            pass

    def loadLayers(self, data):
        '''
        맵 json 데이터에서 레이어(sky, gorund) 추출하는 함수

        :param data: 맵 json 데이터
        :type data: dict
        '''
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                        [
                            Tile(self.sprites.spriteCollection.get("sky"), None, 'sky')
                            for y in range(*data["level"]["layers"]["sky"]["y"])
                        ]
                        + [
                            Tile(
                                self.sprites.spriteCollection.get("ground"),
                                pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                                'ground'
                            )
                            for y in range(*data["level"]["layers"]["ground"]["y"])
                        ]
                )
            )
        self.level = list(map(list, zip(*layers)))

    def loadObjects(self, data):
        '''
        맵 json 데이터에서 오브젝트(bush, cloud, pipe, sky, ground) 추출하는 함수

        :param data: 맵 json 데이터
        :type data: dict
        '''
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        for x, y, z in data["level"]["objects"]["pipe"]:
            self.addPipeSprite(x, y, z)
        for x, y in data["level"]["objects"]["sky"]:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None, 'sky')
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
                'ground'
            )

    def updateEntities(self, cam):
        '''
        엔티티 목록 업데이트 함수

        :param cam: 화면을 보이는 카메라
        :type cam: classes.Camera.Camera
        '''
        for entity in self.entityList:
            entity.update(cam)
            if entity.alive is None:
                self.entityList.remove(entity)

    def drawLevel(self, camera):
        '''
        카메라에 맞게 배경을 업데이트 해주는 함수

        :param camera: 화면을 보여주는 카메라
        :type camera: classes.Camera.Camera
        :raise IndexError: level 인덱스 범위를 넘길때 예외 발생
        '''
        try:
            for y in range(0, 15):
                for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redrawBackground:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y * 32),
                            )
                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
            self.updateEntities(camera)
        except IndexError:
            return

    def addCloudSprite(self, x, y):
        '''
        구름 스프라이트 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        :raise IndexError: level 인덱스 범위를 넘길때 예외 발생
        '''
        try:
            for yOff in range(0, 2):
                for xOff in range(0, 3):
                    self.level[y + yOff][x + xOff] = Tile(
                        self.sprites.spriteCollection.get("cloud{}_{}".format(yOff + 1, xOff + 1)), None, 'cloud')
        except IndexError:
            return

    def addPipeSprite(self, x, y, length=2):
        '''
        파이프 스프라이트 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        :param length: 모르겠음
        :type length: int
        :raise IndexError: level 인덱스 범위를 넘길때 예외 발생
        '''
        try:
            # add pipe head
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x * 32, y * 32, 32, 32),
                'pipel'
            )
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x + 1) * 32, y * 32, 32, 32),
                'piper'
            )
            # add pipe body
            for i in range(1, length + 20):
                self.level[y + i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x * 32, (y + i) * 32, 32, 32),
                    'pipe2l'
                )
                self.level[y + i][x + 1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
                    'pipe2r'
                )
        except IndexError:
            return

    def addBushSprite(self, x, y):
        '''
        부쉬 스프라이트 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        :raise IndexError: level 인덱스 범위를 넘길때 예외 발생
        '''
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None, 'bush1')
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None, 'bush2'
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None, 'bush3'
            )
        except IndexError:
            return

    def addCoinBox(self, x, y):
        '''
        코인박스 추가

        :param x: 보여줄 가로 위치
        :type x:int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32), 'coinbox')
        self.entityList.append(
            CoinBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard,
            )
        )

    def addRandomBox(self, x, y, item):
        '''
        랜덤박스 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        :param item: 나오는 아이템 종류
        :type item: str
        '''
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32), 'randombox')
        self.entityList.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                item,
                self.sound,
                self.dashboard,
                self
            )
        )

    def addCoin(self, x, y):
        '''
        코인 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.entityList.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    def addStar(self, x, y):
        '''
        스타 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.entityList.append(Star(self.screen, self.sprites.spriteCollection, x, y))

    def addCoinBrick(self, x, y):
        '''
        코인 벽돌 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32), 'coinbrick')
        self.entityList.append(
            CoinBrick(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard
            )
        )

    def addGoomba(self, x, y):
        '''
        굼바 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.entityList.append(
            Goomba(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    def addKoopa(self, x, y):
        '''
        쿠파 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.entityList.append(
            Koopa(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    def addRedMushroom(self, x, y):
        '''
        빨간버석 추가

        :param x: 보여줄 가로 위치
        :type x: int
        :param y: 보여줄 세로 위치
        :type y: int
        '''
        self.entityList.append(
            RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )
