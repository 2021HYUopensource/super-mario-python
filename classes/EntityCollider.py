class EntityCollider:
    '''
    맵 엔티티 충돌 판정에 관여하는 클래스
    '''
    def __init__(self, entity):
        self.entity = entity

    def check(self, target):
        '''
        엔티티끼리 충돌 여부를 판별하는 함수

        :param target: 자신과 충돌 여부를 판별할 대상
        :type target: entities.EntityBase.EntityBase
        :return: CollisionState(bool, bool) 반환
        :rtype: CollisionState
        '''
        if self.entity.rect.colliderect(target.rect):
            return self.determineSide(target.rect, self.entity.rect)
        return CollisionState(False, False)

    def determineSide(self, rect1, rect2):
        '''
        두 엔티티의 충돌 상태를 판별하는 함수

        :param rect1: 충돌 여부를 판별할 대상
        :type rect1: pygame.Rect
        :param rect2: 자기 자신
        :type rect2: pygame.Rect
        :return: CollisionState(bool, bool) 반환
        :rtype: CollisionState
        '''
        if (
            rect1.collidepoint(rect2.bottomleft)
            or rect1.collidepoint(rect2.bottomright)
            or rect1.collidepoint(rect2.midbottom)
        ):
            if rect2.collidepoint(
                (rect1.midleft[0] / 2, rect1.midleft[1] / 2)
            ) or rect2.collidepoint((rect1.midright[0] / 2, rect1.midright[1] / 2)):
                return CollisionState(True, False)
            else:
                if self.entity.vel.y > 0:
                    return CollisionState(True, True)
        return CollisionState(True, False)


class CollisionState:
    '''
    충돌 상태를 나타내는 클래스

    isColliding: 충돌중인지 판별\n
    _isTop: 위에서 밟았는지 판별
    '''
    def __init__(self, _isColliding, _isTop):
        self.isColliding = _isColliding
        self.isTop = _isTop
