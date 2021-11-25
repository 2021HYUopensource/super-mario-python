import pygame
from scipy.ndimage.filters import *


class GaussianBlur:
    '''
    화면에 가우시안 블러 효과를 넣는 클래스
    '''
    def __init__(self, kernelsize=7):
        self.kernel_size = kernelsize

    def filter(self, srfc, xpos, ypos, width, height):
        '''
        가우시안 블러를 만드는 함수

        :param srfc: 가우시안 블러 효과를 적용 할 화면
        :type srfc: pygame.Surface
        :param xpos: 필터 가로 시작 위치
        :type xpos: int
        :param ypos: 필터 세로 시작 위치
        :type ypos: int
        :param width: 필터 너비
        :type width: int
        :param height: 필터 높이
        :type height: int
        :return: 가우시안 블러
        :rtype: pygame.Surface
        '''
        nSrfc = pygame.Surface((width, height))
        pxa = pygame.surfarray.array3d(srfc)
        blurred = gaussian_filter(pxa, sigma=(self.kernel_size, self.kernel_size, 0))
        pygame.surfarray.blit_array(nSrfc, blurred)
        del pxa
        return nSrfc
