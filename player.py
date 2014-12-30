from prepare import *
from generics import *

# Create player to be added to group
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.health = 10
        self.money  = 100
        self.image  = image
        self.angle  = 0
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Change speeds depending on input
    def goRight(self):
        self.rect.x += PLAYERSPEED

    def goLeft(self):
        self.rect.x -= PLAYERSPEED

    def goUp(self):
        self.rect.y -= PLAYERSPEED

    def goDown(self):
        self.rect.y += PLAYERSPEED

    def visible(self, player_image):
        self.image = player_image

    def invisible(self, blank_image):
        self.image = blank_image

    def damagePlayer(self, player_group, enemy_group, healthbar, HEALTHBARS):
        if pygame.sprite.groupcollide(player_group, enemy_group, False, False) and self.health > 1:
            pygame.sprite.groupcollide(player_group, enemy_group, False, True)
            self.health -= 1
            healthbar.image = HEALTHBARS[self.health]
            return True

    def killPlayer(self, player_group, enemy_group, healthbar, HEALTHBARS, arena_sprites):
        if pygame.sprite.groupcollide(player_group, enemy_group, True, True) and self.health == 1:
            healthbar.image = HEALTHBARS[0]

            # Lower explosion by 78 pixels so that it appears over player
            explosion = GenericSprite(EXPLOSIONRECT, self.rect.x, self.rect.y - 78)
            arena_sprites.add(explosion)
            return True

