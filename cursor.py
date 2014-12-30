import pygame

# Create crosshair sprite to put in group
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)
