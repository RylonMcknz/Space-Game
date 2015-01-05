import pyganim
from generics import *

loot_group = pygame.sprite.RenderUpdates()

# Create coin sprite for looting and such
class Coin(pygame.sprite.Sprite):
    def __init__(loot, sprite_sheet, x, y):
        pygame.sprite.Sprite.__init__(loot)
        coin_sprites = cutSpriteSheet(32, 32, 9, 32, sprite_sheet, 9)

        loot.COINANIM = pyganim.PygAnimation(
            [(coin_sprites[0], 0.05), (coin_sprites[1], 0.05), (coin_sprites[2], 0.05),
             (coin_sprites[3], 0.05), (coin_sprites[4], 0.05), (coin_sprites[5], 0.05),
             (coin_sprites[6], 0.05), (coin_sprites[7], 0.05)], loop = True)

        loot.image  = coin_sprites[8]
        loot.rect   = loot.image.get_rect()
        loot.rect.x = x
        loot.rect.y = y

    def update(loot, loot_group):
        for obj in loot_group:
            loot.COINANIM.blit(screen, (loot.rect.x, loot.rect.y))
