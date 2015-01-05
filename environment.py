from prepare import *


border_group = pygame.sprite.RenderUpdates()
planet_group = pygame.sprite.RenderUpdates()


left_wall   = GenericSprite(LEFTWALL, (0 - 50), 0)
right_wall  = GenericSprite(RIGHTWALL, WINDOWWIDTH, 0)
top_wall    = GenericSprite(TOPWALL, 0, (0 - 50))
bottom_wall = GenericSprite(BOTTOMWALL, 0, WINDOWHEIGHT)
border_group.add(left_wall, right_wall, top_wall, bottom_wall)


store_planet    = GenericSprite(PLANET1, 100, 100)
training_planet = GenericSprite(PLANET2, 700, 50)
armory_planet   = GenericSprite(PLANET3, 200, 600)
arena_planet    = GenericSprite(PLANET4, 1450, 750)
planet_group.add(store_planet, training_planet, armory_planet, arena_planet)


home_sprites = pygame.sprite.LayeredUpdates()
arena_sprites = pygame.sprite.LayeredUpdates()


class Environment:
    def __init__(self):
        # Bool used to stop player movement when player is killed
        self.game_over = False

        self.player_explo = False

        # Bools to determine location of player
        self.go_arena = False
        self.go_home  = True

        self.planet_collision = False

    def handleLocation(self, initial_time):

        # Go to arena
        if self.go_home == True:
            if self.planet_collision:
                screen.fill(BGCOLOR)
                pygame.display.update()
                self.go_arena = True
                self.go_home = False

        # Go home
        elif self.go_arena == True and self.player_explo == True:

            if (time.time() - initial_time) >= 1.8:
                self.go_home   = True
                self.go_arena  = False
                self.game_over = False
                self.player_explo = False
                return True

    def clearSprites(self):
        pass

