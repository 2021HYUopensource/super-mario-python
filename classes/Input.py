import pygame
from pygame.locals import *
import sys


class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity

    def checkForInput(self):
        '''
        모든 입력을 확인하는 함수
        '''
        events = pygame.event.get()
        self.checkForKeyboardInput()
        self.checkForMouseInput(events)
        self.checkForQuitAndRestartInputEvents(events)

    def checkForKeyboardInput(self):
        '''
        키보드 입력을 확인하는 함수
        '''
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_LEFT] or pressedKeys[K_h] and not pressedKeys[K_RIGHT]:
            self.entity.traits["goTrait"].direction = -1
        elif pressedKeys[K_RIGHT] or pressedKeys[K_l] and not pressedKeys[K_LEFT]:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits['goTrait'].direction = 0

        isJumping = pressedKeys[K_SPACE] or pressedKeys[K_UP] or pressedKeys[K_k]
        self.entity.traits['jumpTrait'].jump(isJumping)

        self.entity.traits['goTrait'].boost = pressedKeys[K_LSHIFT]

    def checkForMouseInput(self, events):
        '''
        마우스 입력을 확인하는 함수

        :param events: 이벤트 종류
        :type events: list[pygame.event.Event]
        '''
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.isRightMouseButtonPressed(events):
            self.entity.levelObj.addKoopa(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addGoomba(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addRedMushroom(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
        if self.isLeftMouseButtonPressed(events):
            self.entity.levelObj.addCoin(
                mouseX / 32 - self.entity.camera.pos.x, mouseY / 32
            )

    def checkForQuitAndRestartInputEvents(self, events):
        '''
        게임 중지 및 나가기 입력을 확인하는 함수

        :param events: 이벤트 종류
        :type events: list[pygame.event.Event]
        '''
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_ESCAPE or event.key == pygame.K_F5):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self, events):
        '''
        마우스 왼쪽 입력을 확인하는 함수

        :param events: 이벤트 종류
        :type events: list[pygame.event.Event]
        :return: 왼쪽/오른쪽 클릭 여부
        :rtype: bool
        '''
        return self.checkMouse(events, 1)

    def isRightMouseButtonPressed(self, events):
        '''
        마우스 오른쪽 입력을 확인하는 함수

        :param events: 이벤트 종류
        :type events: list[pygame.event.Event]
        :return: 왼쪽/오른쪽 클릭 여부
        :rtype: bool
        '''
        return self.checkMouse(events, 3)

    def checkMouse(self, events, button):
        '''
        마우스 입력을 확인하는 함수

        :param events: 이벤트 종류
        :type events: list[pygame.event.Event]
        :param button: 이벤트 타입
        :type button: int
        :return: 왼쪽/오른쪽 클릭 여부
        :rtype: bool
        '''
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP and e.button == button:
                return True
        return False
