from pygame import mixer


class Sound:
    '''
    사운드 재생에 관여하는 클래스
    '''
    def __init__(self):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)

        self.allowSFX = True

        self.soundtrack = mixer.Sound("./sfx/main_theme.ogg")
        self.coin = mixer.Sound("./sfx/coin.ogg")
        self.bump = mixer.Sound("./sfx/bump.ogg")
        self.stomp = mixer.Sound("./sfx/stomp.ogg")
        self.jump = mixer.Sound("./sfx/small_jump.ogg")
        self.death = mixer.Sound("./sfx/death.wav")
        self.kick = mixer.Sound("./sfx/kick.ogg")
        self.brick_bump = mixer.Sound("./sfx/brick-bump.ogg")
        self.powerup = mixer.Sound('./sfx/powerup.ogg')
        self.powerup_appear = mixer.Sound('./sfx/powerup_appears.ogg')
        self.pipe = mixer.Sound('./sfx/pipe.ogg')

    def play_sfx(self, sfx):
        '''
        효과음 재생하는 함수

        :param sfx: 재생할 효과음 이름
        :type sfx: mixer.Sound
        '''
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music):
        '''
        배경음악 재생하는 함수

        :param music: 재생할 배경음 이름
        :type music: mixer.Sound
        '''
        self.music_channel.play(music)
