import pygame, random

from constants import *


# This module is for general classes and functions which I like to use


# Function which rotates an image about its center by given angle
def rotCenter(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect  = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


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

# Get a random x and y for enemy to spawn
def randomHoriz(enemy_width):
    return random.randint((0 - enemy_width), WINDOWWIDTH)

def randomVert(enemy_height):
    return random.randint(0 - enemy_height, WINDOWHEIGHT)


def randSpawnPos(enemy_width, enemy_height):
    rand1 = random.randint(0, 100)
    rand2 = random.randint(0, 100)
    if rand1 >= 50:
        y = randomVert(enemy_height)
        if rand2 >= 50:
            x = 0 - enemy_width
        elif rand2 < 50:
            x = WINDOWWIDTH
    elif rand1 < 50:
        x = randomHoriz(enemy_width)
        if rand2 >= 50:
            y = 0 - enemy_height
        elif rand2 < 50:
            y = WINDOWHEIGHT
    return x, y

def playExplosion(sound, animation):
    sound.play()
    animation.play()

# Set health to zero and remove groups from screen
def clearGroups(group1, group2, group3, blank_enemy):

    # Remove the rest of the enemies
    for obj in group1:
        obj.image = blank_enemy
    group1.empty()

    for obj in group2:
        obj.image = blank_enemy
    group2.empty()

    for obj in group3:
        obj.image = blank_enemy
    group3.empty()
