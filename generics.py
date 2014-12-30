import pygame


# This module is for general classes and functions which I like to use
# Create a generic sprite to use in groups and collisions
class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Cut out pieces of sprite sheet to get individual sprites. Gets them in order, left to right, and bottom to top
def cutSpriteSheet(sprite_width, sprite_height, horiz_count, sheet_height, sheet_img, sprite_count):
    sprite_list = []
    i = 0
    x = 0
    y = sheet_height - sprite_height
    height = sprite_height
    width  = sprite_width
    while i <= sprite_count:
        sheet_img.set_clip(pygame.Rect(x, y, width, height))
        sprite_list.append(sheet_img.subsurface(sheet_img.get_clip()))
        x += sprite_width
        i += 1
        if i % horiz_count == 0:
            y -= sprite_height
            x = 0

    return sprite_list

# Make a rect to be added to dirty rect list--for showing things on the screen
def customRect(screen, x, y, width, height):
    return pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))