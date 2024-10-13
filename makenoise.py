import pygame
pygame.init()
pygame.mixer.init()
async def dog_bark(sound_file: int ):
    sound = pygame.mixer.Sound(sound_file)
    sound.set_volume(-1)
    sound.play() 