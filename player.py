from environment import *
from prepare import *
from generics import *
from enemyControl import *
from loot import *

player_group    = pygame.sprite.RenderUpdates()
plyr_weap_group = pygame.sprite.RenderUpdates()
hud_group       = pygame.sprite.RenderUpdates()

# Sprite groups are made to handle collisions. Render updates are used for dirty rects
cursor_group = pygame.sprite.RenderUpdates()


# Create crosshair sprite to put in group
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)

# Create player to be added to group
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        # Define a starting time
        self.initial_time = time.time()

        # Bools for motion upon key press
        self.pressed_w = False
        self.pressed_s = False
        self.pressed_d = False
        self.pressed_a = False

        # Bools for where to blit explosions upon deaths
        self.enemy_explo = False
        self.current_explo = EXPLOANIM1.getCopy()


        self.health = 10
        self.money  = 100
        self.image  = image
        self.active_plyr_img = BLUESHIP
        self.angle  = 0
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.collision_x = 0
        self.collision_y = 0

        # Create the healthbar
        self.healthbar = GenericSprite(HEALTHBARS[10], 10, 50)
        hud_group.add(self.healthbar)

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

    def update(self):
        # Check for border collision and change player speed
        if self.pressed_w:
            if not pygame.sprite.collide_rect(self, top_wall):
                self.goUp()
        if self.pressed_s:
            if not pygame.sprite.collide_rect(self, bottom_wall):
                self.goDown()
        if self.pressed_d:
            if not pygame.sprite.collide_rect(self, right_wall):
                self.goRight()
        if self.pressed_a:
            if not pygame.sprite.collide_rect(self, left_wall):
                self.goLeft()

    def damagePlayer(self):
        if pygame.sprite.groupcollide(player_group, enemy_attackers, False, False) and self.health > 1:
            pygame.sprite.groupcollide(player_group, enemy_attackers, False, True)
            self.health -= 1
            self.healthbar.image = HEALTHBARS[self.health]
            playExplosion(EXPLOSIONSOUND, EXPLOANIM2)

    def killPlayer(self):
        if pygame.sprite.groupcollide(player_group, enemy_attackers, True, True) and self.health == 1:
            self.healthbar.image = HEALTHBARS[0]

            # Lower explosion by 78 pixels so that it appears over player
            explosion = GenericSprite(EXPLOSIONRECT, self.rect.x, self.rect.y - 78)
            arena_sprites.add(explosion)
            playExplosion(EXPLOSIONSOUND, EXPLOANIM1)
            self.active_plyr_img = PLAYERRECT
            clearGroups(kamikaze_group, star_group, loot_group, BLANKENEMY)
            self.initial_time = time.time()
            return True

    def collectLoot(self):
        if pygame.sprite.groupcollide(player_group, loot_group, False, True):
            COLLECTCOIN.play()
            self.money += 10

    def killEnemy(self):
        if len(plyr_weap_group.sprites()) != 0:
                for enemy in enemy_attackables:
                    if pygame.sprite.spritecollideany(enemy, plyr_weap_group):
                        if pygame.sprite.groupcollide(plyr_weap_group, enemy_attackables, True, True):
                            self.collision_x = enemy.rect.x
                            self.collision_y = enemy.rect.y

                            explosion = GenericSprite(EXPLOSIONRECT, self.collision_x, self.collision_y - 78)
                            arena_sprites.add(explosion)

                            EXPLOSIONSOUND.play()
                            self.current_explo.play()

                            self.enemy_explo = True

                            coin = Coin(COINSHEET, self.collision_x, self.collision_y)
                            coin.COINANIM.play()

                            loot_group.add(coin)
                            arena_sprites.add(coin)

