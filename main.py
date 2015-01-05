import sys, pygame
from pygame.locals import *
from enemies import *
from weapon import *
from player import *
from playerMenu import *
from loot import *
from environment import *
from prepare import *
from enemyControl import *


def enemyWeaponCollide(weapon_group, enemytype_group):
    if len(weapon_group.sprites()) != 0:     
        for enemy in enemytype_group:
            if pygame.sprite.spritecollideany(enemy, weapon_group):
                if pygame.sprite.groupcollide(weapon_group, enemytype_group, True, True):
                    return True


class Control:
    def __init__(self):
        # Bool for fps switch
        self.fps_toggle = False

    #    # Bools for where to blit explosions upon deaths
    #    self.enemy_explo  = False

        # Bool used to switch player menu on and off
        self.plyr_menu_toggle = False

        self.environment = Environment()

        self.enemyControl = EnemyControl()

        # Create the player
        self.player = Player(800, 450, PLAYERRECT)
        player_group.add(self.player)

        # Create crosshair object
        self.crosshair = Crosshair(CROSSHAIR, pygame.mouse.get_pos())
        cursor_group.add(self.crosshair)

        # Call and create a player menu to toggled
        self.playermenu = PlayerMenu(PLAYERMENU, self.player.rect.x + PLAYERWIDTH, self.player.rect.y + PLAYERHEIGHT)

        # Groups to minimize what is updated. One location updated at a time
        home_sprites.add(player_group, planet_group, cursor_group, hud_group)
        arena_sprites.add(player_group, cursor_group, hud_group)

        # Move player to front of layers
        home_sprites.move_to_front(self.player)
        arena_sprites.move_to_front(self.player)

        # Update so background appears
        screen.blit(SPACEIMAGE, (0, 0))
        pygame.display.update()

    def mainGameLoop(self):

        # Main game loop
        while True:
            self.eventLoop()

            if not self.environment.game_over:
                self.player.update()

                # Switch location of player upon collision of arena planet
                if pygame.sprite.collide_rect(self.player, arena_planet):
                    self.environment.planet_collision = True
                    self.environment.handleLocation(self.player.initial_time)
                    self.player.rect.x = 800
                    self.player.rect.y = 450

            if self.environment.go_arena and not self.environment.game_over:
                self.enemyControl.spawnEnemies()

            # Collect loot when player collides
            self.player.collectLoot()

            # Do damage to player with enemies
            self.player.damagePlayer()

            # Check and allow enemies to kill player
            if self.player.killPlayer():
                self.environment.player_explo = True
                self.environment.game_over    = True

            # Handle collisions between enemies and player weapon(kill enemies)
            self.player.killEnemy()

            # Handle the current position of the player's menu, based on wall collisions
            self.playermenu.handlePlayerMenuPos(right_wall, left_wall, top_wall, bottom_wall)

            # Handle cursor display
            self.crosshair.rect.center = pygame.mouse.get_pos()

            # Make fps label
            fps_label = FPSFONT.render('fps: ' + str(clock.get_fps()), 1, (255, 255, 255))
            fps_box = customRect(screen, 1500, 10, 100, 20)

            # Make name label
            name_label = NAMEFONT.render('Ship Name', 1, (255, 255, 255))
            name_box = customRect(screen, 10, 20, 110, 20)

            # Make CashMoney label
            money_label = HUDFONT.render('CashMoney: $' + str(self.player.money), 1, (255, 255, 255))
            money_box = customRect(screen, 10, 70, 150, 30)


            dirty_rects = [fps_box, name_box, money_box]

            # Handle home display
            if self.environment.go_home:

                home_sprites.clear(screen, SPACEIMAGE)
                dirty_groups = home_sprites.draw(screen)
                screen.blit(rotCenter(self.player.active_plyr_img, self.angle_between), (self.player.rect.x, self.player.rect.y))

                # Update position of floating player menu
                self.playermenu.update(self.player.rect.x + PLAYERWIDTH, self.player.rect.y + PLAYERHEIGHT)

                # Display fps label
                if self.fps_toggle:
                    screen.blit(fps_label, (1500, 10))

                screen.blit(name_label, (10, 20))
                screen.blit(money_label, (10, 70))

            # Handle arena display
            elif self.environment.go_arena:
                screen.fill(BGCOLOR)

                kamikaze_group.update(self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2))
                star_group.update(enemy_weap_group, arena_sprites, LASERSOUND, LASERIMAGE, self.enemyControl.spawn_ctr)
                screen.blit(rotCenter(self.player.active_plyr_img, self.angle_between), (self.player.rect.x, self.player.rect.y))

                # Update position of floating player menu
                self.playermenu.update(self.player.rect.x + PLAYERWIDTH, self.player.rect.y + PLAYERHEIGHT)

                # Update the shots fired
                if len(plyr_weap_group.sprites()) != 0:
                    for obj in plyr_weap_group:
                        obj.update(obj.target_vector)

                if len(enemy_weap_group.sprites()) != 0:
                    for obj in enemy_weap_group:
                        obj.update(obj.target_vector)

                # Blit explosion on player when dead
                if self.environment.player_explo:
                    EXPLOANIM1.blit(screen, (self.player.rect.x, self.player.rect.y - 78))
                    if self.environment.handleLocation(self.player.initial_time):

                        home_sprites.add(self.player)
                        arena_sprites.add(self.player)
                        player_group.add(self.player)
                        self.player.active_plyr_img = BLUESHIP
                        self.player.rect.x = 800
                        self.player.rect.y = 450
                        self.player.health = 10
                        self.player.healthbar.image = HEALTHBARS[10]

                        # Update screen to show home background
                        screen.blit(SPACEIMAGE, (0, 0))
                        pygame.display.update()

                # Blit list of explosions to screen
                if self.player.enemy_explo:
                    self.player.current_explo.blit(screen, (self.player.collision_x, self.player.collision_y - 78))

                EXPLOANIM2.blit(screen, (self.player.rect.x, self.player.rect.y))

                # Display coins
                for obj in loot_group:
                    obj.COINANIM.blit(screen, (obj.rect.x, obj.rect.y))

                # Display fps label
                if self.fps_toggle:
                    screen.blit(fps_label, (1500, 10))

                screen.blit(name_label, (10, 20))
                screen.blit(money_label, (10, 70))

                dirty_groups = arena_sprites.draw(screen)

            # Update groups of sprites
            pygame.display.update(dirty_groups)

            # Update rects
            pygame.display.update(dirty_rects)

            clock.tick(FPS)

    def eventLoop(self):
        events = pygame.event.get()
        for event in events:

            # Handle quitting
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Handle player controls

            # Vector from player to cursor
            moveVect = normalize(sub(pygame.mouse.get_pos(), (self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2))))

            # Unit vector pointing east
            currentVect = (1, 0)

            # Get angle of rotation and give it to the player
            self.angle_between = 180 * angle(moveVect, currentVect) / math.pi

            # Change player to new angle
            if moveVect != None:
                if moveVect[1] > 0:
                    self.angle_between *= -1
                self.player.angle = self.angle_between

            # Fire when mouse is clicked
            if self.environment.game_over == False:
                if event.type == pygame.MOUSEBUTTONDOWN and self.environment.go_arena:
                    LASERSOUND.play()
                    target_vector = normalize(sub(event.pos, (self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2))))
                    weapon = Weapon(LASERIMAGE, self.player.rect.x + (PLAYERWIDTH/2), self.player.rect.y + (PLAYERHEIGHT/2), self.player.angle, target_vector)
                    plyr_weap_group.add(weapon)
                    arena_sprites.add(weapon)
                    arena_sprites.move_to_back(weapon)

            # Switch bools upon WASD key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.pressed_w = True
                elif event.key == pygame.K_s:
                    self.player.pressed_s = True
                elif event.key == pygame.K_d:
                    self.player.pressed_d = True
                elif event.key == pygame.K_a:
                    self.player.pressed_a = True

                # Toggle fps
                elif event.key == pygame.K_f:
                    if self.fps_toggle == False:
                        self.fps_toggle = True
                    elif self.fps_toggle == True:
                        self.fps_toggle = False

                # Toggle player menu
                elif event.key == pygame.K_c:
                    if self.plyr_menu_toggle == False:
                        self.plyr_menu_toggle = True
                        hud_group.add(self.playermenu)
                        home_sprites.add(self.playermenu)
                        arena_sprites.add(self.playermenu)
                    elif self.plyr_menu_toggle == True:
                        self.plyr_menu_toggle = False
                        hud_group.remove(self.playermenu)
                        home_sprites.remove(self.playermenu)
                        arena_sprites.remove(self.playermenu)

            # Switch bools when WASD keys are released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.pressed_w = False
                elif event.key == pygame.K_s:
                    self.player.pressed_s = False
                elif event.key == pygame.K_d:
                    self.player.pressed_d = False
                elif event.key == pygame.K_a:
                    self.player.pressed_a = False


    def update(self):
        pass
        # Call update methods on objects



    def draw(self):
        # Call draw methods on objects
        pass



app = Control()
app.mainGameLoop()




