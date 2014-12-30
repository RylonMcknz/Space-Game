from prepare import *
from vectorMath import *

# Make weapon sprites
class Weapon(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, target_vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, angle)
        self.image = rot_image
        self.rect.x = x
        self.rect.y = y
        self.target_vector = target_vector

    # Fire weapon in direction of my mouse
    def update(self, target_vector):
        self.speed = LASERSPEED

        # Only update if fired shot is within 500 pixels of display
        if self.rect.x >= -500 and self.rect.x <= WINDOWWIDTH + 500 and self.rect.y >= -500 and self.rect.y <= WINDOWHEIGHT + 500:
            if self.speed != 0:
                move_vector = [c * self.speed for c in normalize(target_vector)]
                self.rect.x, self.rect.y = add((self.rect.x, self.rect.y), move_vector)
