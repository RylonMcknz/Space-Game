import time, sys
from pygame.locals import *
from enemies import *
from weapon import *
from player import *
from playerMenu import *
from loot import *
from prepare import *

# Graphics, NOT converted for memory efficiency (Globally defined to shorten function parameters)

PLAYERRECT = pygame.image.load('player rect.png')





# Create crosshair sprite to put in group
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        self.image  = image
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)


# Function which rotates an image about its center by given angle
def rotCenter(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect  = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

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

def enemyWeaponCollide(weapon_group, enemytype_group, EXPLOSIONRECT, arena_sprites, EXPLOSIONSOUND, enemy_explo):
    if len(weapon_group.sprites()) != 0:     
        for enemy in enemytype_group:
            if pygame.sprite.spritecollideany(enemy, weapon_group):
                if pygame.sprite.groupcollide(weapon_group, enemytype_group, True, True):
                    return True

# Set health to zero and remove groups from screen
def handlePlayerDeath(group1, group2, blank_enemy):
    
    # Remove the rest of the enemies
    for obj in group1:
        obj.image = blank_enemy
    group1.empty()

    for obj in group2:
        obj.image = blank_enemy
    group2.empty()


def playExplosion(sound, animation):
    sound.play()
    animation.play()


# Main function starts here
def main():


    # Bools for motion upon key press
    pressed_w = False
    pressed_s = False
    pressed_d = False
    pressed_a = False

    # Bool for fps switch
    fps_toggle = False

    # Bools for where to blit explosions upon deaths
    enemy_explo  = False
    player_explo = False

    # Bools to determine location of player
    go_arena = False
    go_home  = True

    # Bool used to stop player movement when player is killed
    game_over = False

    # Bool used to switch player menu on and off
    plyr_menu_toggle = False

    # Sprite groups are made to handle collisions. Render updates are used for dirty rects
    player_group     = pygame.sprite.RenderUpdates()
    kamikaze_group   = pygame.sprite.RenderUpdates()
    star_group       = pygame.sprite.RenderUpdates()
    plyr_weap_group  = pygame.sprite.RenderUpdates()
    enemy_weap_group = pygame.sprite.RenderUpdates()
    border_group     = pygame.sprite.RenderUpdates()
    planet_group     = pygame.sprite.RenderUpdates()
    cursor_group     = pygame.sprite.RenderUpdates()
    hud_group        = pygame.sprite.RenderUpdates()
    loot_group       = pygame.sprite.RenderUpdates()


    # Create the player
    player = Player(800, 450, PLAYERRECT)
    player_group.add(player)
    active_plyr_img = BLUESHIP

    # Create the healthbar
    healthbar = GenericSprite(HEALTHBARS[10], 10, 50)
    hud_group.add(healthbar)

    # Create crosshair object
    crosshair = Crosshair(CROSSHAIR, pygame.mouse.get_pos())
    cursor_group.add(crosshair)

    # Used to hande when enemies spawn
    spawn_ctr = 0


    # Call the borders
    left_wall   = GenericSprite(LEFTWALL, (0 - 50), 0)
    right_wall  = GenericSprite(RIGHTWALL, WINDOWWIDTH, 0)
    top_wall    = GenericSprite(TOPWALL, 0, (0 - 50))
    bottom_wall = GenericSprite(BOTTOMWALL, 0, WINDOWHEIGHT)
    border_group.add(left_wall, right_wall, top_wall, bottom_wall)

    # Call the home planets
    store_planet    = GenericSprite(PLANET1, 100, 100)
    training_planet = GenericSprite(PLANET2, 700, 50)
    armory_planet   = GenericSprite(PLANET3, 200, 600)
    arena_planet    = GenericSprite(PLANET4, 1450, 750)
    planet_group.add(store_planet, training_planet, armory_planet, arena_planet)

    # Call and create a player menu to toggled
    playermenu = PlayerMenu(PLAYERMENU, player.rect.x + PLAYERWIDTH, player.rect.y + PLAYERHEIGHT)

    # Groups to minimize what is updated. One location updated at a time
    home_sprites = pygame.sprite.LayeredUpdates()
    arena_sprites = pygame.sprite.LayeredUpdates()
    home_sprites.add(player_group, planet_group, cursor_group, hud_group)
    arena_sprites.add(player_group, cursor_group, hud_group)

    # Move player to front of layers
    home_sprites.move_to_front(player)
    arena_sprites.move_to_front(player)

    # Start time before main loop
    initial_time = time.time()

    # Update so background appears
    screen.blit(SPACEIMAGE, (0, 0))
    pygame.display.update()

    # Main game loop
    while True:
        events = pygame.event.get()
        for event in events:

            # Handle quitting
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Handle player controls

            # Vector from player to cursor
            moveVect = normalize(sub(pygame.mouse.get_pos(), (player.rect.x + (PLAYERWIDTH/2), player.rect.y + (PLAYERHEIGHT/2))))

            # Unit vector pointing east
            currentVect = (1, 0)

            # Get angle of rotation and give it to the player
            angle_between = 180 * angle(moveVect, currentVect) / math.pi

            # Change player to new angle
            if moveVect != None:
                if moveVect[1] > 0:
                    angle_between *= -1
                player.angle = angle_between

            # Fire when mouse is clicked
            if game_over == False:
                if event.type == pygame.MOUSEBUTTONDOWN and go_arena:
                    LASERSOUND.play()
                    target_vector = normalize(sub(event.pos, (player.rect.x + (PLAYERWIDTH/2), player.rect.y + (PLAYERHEIGHT/2))))
                    weapon = Weapon(LASERIMAGE, player.rect.x + (PLAYERWIDTH/2), player.rect.y + (PLAYERHEIGHT/2), player.angle, target_vector)
                    plyr_weap_group.add(weapon)
                    arena_sprites.add(weapon)
                    arena_sprites.move_to_back(weapon)
                    
            # Switch bools upon WASD key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    pressed_w = True
                elif event.key == pygame.K_s:
                    pressed_s = True
                elif event.key == pygame.K_d:
                    pressed_d = True
                elif event.key == pygame.K_a:
                    pressed_a = True

                # Toggle fps
                elif event.key == pygame.K_f:
                    if fps_toggle == False:
                        fps_toggle = True
                    elif fps_toggle == True:
                        fps_toggle = False

                # Toggle player menu
                elif event.key == pygame.K_c:
                    if plyr_menu_toggle == False:
                        plyr_menu_toggle = True
                        hud_group.add(playermenu)
                        home_sprites.add(playermenu)
                        arena_sprites.add(playermenu)
                    elif plyr_menu_toggle == True:
                        plyr_menu_toggle = False
                        hud_group.remove(playermenu)
                        home_sprites.remove(playermenu)
                        arena_sprites.remove(playermenu)
                        
            # Switch bools when WASD keys are released        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    pressed_w = False
                elif event.key == pygame.K_s:
                    pressed_s = False
                elif event.key == pygame.K_d:
                    pressed_d = False
                elif event.key == pygame.K_a:
                    pressed_a = False

        # Check for border collision and change player speed
        if game_over == False:
            if pressed_w:
                if not pygame.sprite.collide_rect(player, top_wall):
                    player.goUp()
            if pressed_s:
                if not pygame.sprite.collide_rect(player, bottom_wall):
                    player.goDown()
            if pressed_d:
                if not pygame.sprite.collide_rect(player, right_wall):
                    player.goRight()
            if pressed_a:
                if not pygame.sprite.collide_rect(player, left_wall):
                    player.goLeft()



        # Switch location of player
        if go_home == True:
            if pygame.sprite.collide_rect(player, arena_planet):
                screen.fill(BGCOLOR)
                pygame.display.update()
                go_arena = True
                go_home = False
                player.rect.x = 800
                player.rect.y = 450
            
        # Handle enemy spawning
        if spawn_ctr % 100 == 0 and go_arena and not game_over:
            spawn_x, spawn_y = randSpawnPos(ENEMYWIDTH, ENEMYHEIGHT)
            rand_num = random.randint(0, 100)
            if rand_num < 50:
                enemy = StarEnemy(spawn_x, spawn_y, EYEBALLIMAGE)
                star_group.add(enemy)
                arena_sprites.add(enemy)
                arena_sprites.move_to_back(enemy) 
            elif rand_num >= 50:
                enemy = KamikazeEnemy(spawn_x, spawn_y, ENEMYIMAGE)
                kamikaze_group.add(enemy)
                arena_sprites.add(enemy)
                arena_sprites.move_to_back(enemy) 
        spawn_ctr += 1


        # Collect loot when player collides
        if pygame.sprite.groupcollide(player_group, loot_group, False, True):
            COLLECTCOIN.play()
            player.money += 10

        # Do damage to player with enemies
        if player.damagePlayer(player_group, kamikaze_group, healthbar, HEALTHBARS):
            playExplosion(EXPLOSIONSOUND, EXPLOANIM2)


        # Do damage to player with enemy weapon
        if player.damagePlayer(player_group, enemy_weap_group, healthbar, HEALTHBARS):
            playExplosion(EXPLOSIONSOUND, EXPLOANIM2)
        

        # Kill player with kamikaze enemies
        if player.killPlayer(player_group, kamikaze_group, healthbar, HEALTHBARS, arena_sprites):
            playExplosion(EXPLOSIONSOUND, EXPLOANIM1)
            player_explo = True
            game_over    = True
            active_plyr_img = PLAYERRECT
            handlePlayerDeath(kamikaze_group, star_group, BLANKENEMY)
            initial_time = current_time

        # Repeat the above so star enemies can kill player
        if player.killPlayer(player_group, enemy_weap_group, healthbar, HEALTHBARS, arena_sprites):
            playExplosion(EXPLOSIONSOUND, EXPLOANIM1)
            player_explo = True
            game_over    = True
            active_plyr_img = PLAYERRECT
            handlePlayerDeath(kamikaze_group, star_group, BLANKENEMY)
            initial_time = current_time


        # Handle collisions between enemies and player weapon
        if len(plyr_weap_group.sprites()) != 0:     
            for enemy in kamikaze_group:
                if pygame.sprite.spritecollideany(enemy, plyr_weap_group):
                    if pygame.sprite.groupcollide(plyr_weap_group, kamikaze_group, True, True):
                        collision_x = enemy.rect.x
                        collision_y = enemy.rect.y
                        
                        explosion = GenericSprite(EXPLOSIONRECT, collision_x, collision_y - 78)
                        arena_sprites.add(explosion)

                        EXPLOSIONSOUND.play()
                        current_explo = EXPLOANIM1.getCopy()
                        current_explo.play()
                        
                        enemy_explo = True

                        coin = Coin(COINSHEET, collision_x, collision_y)  
                        coin.COINANIM.play()

                        loot_group.add(coin)
                        arena_sprites.add(coin)

            for enemy in star_group:
                if pygame.sprite.spritecollideany(enemy, plyr_weap_group):
                    if pygame.sprite.groupcollide(plyr_weap_group, star_group, True, True):
                        collision_x = enemy.rect.x
                        collision_y = enemy.rect.y
                        
                        explosion = GenericSprite(EXPLOSIONRECT, collision_x, collision_y - 78)
                        arena_sprites.add(explosion)

                        EXPLOSIONSOUND.play()
                        current_explo = EXPLOANIM1.getCopy()
                        current_explo.play()
                        
                        enemy_explo = True

        # Handle the current position of the player's menu, based on wall collisions
        playermenu.handlePlayerMenuPos(right_wall, left_wall, top_wall, bottom_wall)
                        
        # Handle cursor display
        crosshair.rect.center = pygame.mouse.get_pos()

        # Make fps label
        fps_label = FPSFONT.render('fps: ' + str(clock.get_fps()), 1, (255, 255, 255))
        fps_box = customRect(screen, 1500, 10, 100, 20)
        
        # Make name label
        name_label = NAMEFONT.render('Ship Name', 1, (255, 255, 255))
        name_box = customRect(screen, 10, 20, 110, 20)

        # Make CashMoney label
        money_label = HUDFONT.render('CashMoney: $' + str(player.money), 1, (255, 255, 255))
        money_box = customRect(screen, 10, 70, 150, 30)


        dirty_rects = [fps_box, name_box, money_box]
          
        # Handle home display
        if go_home:
            
            home_sprites.clear(screen, SPACEIMAGE)
            dirty_groups = home_sprites.draw(screen)
            screen.blit(rotCenter(active_plyr_img, angle_between), (player.rect.x, player.rect.y))

            # Update position of floating player menu
            playermenu.update(player.rect.x + PLAYERWIDTH, player.rect.y + PLAYERHEIGHT)

            # Display fps label
            if fps_toggle == True:
                screen.blit(fps_label, (1500, 10))

            screen.blit(name_label, (10, 20))
            screen.blit(money_label, (10, 70))

        # Handle arena display    
        elif go_arena:
            screen.fill(BGCOLOR)

            kamikaze_group.update(player.rect.x + (PLAYERWIDTH/2), player.rect.y + (PLAYERHEIGHT/2))
            star_group.update(enemy_weap_group, arena_sprites, LASERSOUND, LASERIMAGE, spawn_ctr)
            screen.blit(rotCenter(active_plyr_img, angle_between), (player.rect.x, player.rect.y))

            # Update position of floating player menu
            playermenu.update(player.rect.x + PLAYERWIDTH, player.rect.y + PLAYERHEIGHT)

            # Update the shots fired
            if len(plyr_weap_group.sprites()) != 0:
                for obj in plyr_weap_group:
                    obj.update(obj.target_vector)

            if len(enemy_weap_group.sprites()) != 0:
                for obj in enemy_weap_group:
                    obj.update(obj.target_vector)

            

            # Current time
            current_time = time.time()
            
            # Blit explosion on player when dead
            if player_explo == True:
                EXPLOANIM1.blit(screen, (player.rect.x, player.rect.y - 78))

                # Wait for animation(time in seconds) to play, then go back home
                if (current_time - initial_time) >= 1.8:
                    go_home   = True
                    go_arena  = False
                    game_over = False

                    # Bring back player
                    player_explo = False
                    home_sprites.add(player)
                    arena_sprites.add(player)
                    player_group.add(player)
                    active_plyr_img = BLUESHIP
                    player.rect.x = 800
                    player.rect.y = 450
                    player.health = 10
                    healthbar.image = HEALTHBARS[10]

                    # Update screen to show home background
                    screen.blit(SPACEIMAGE, (0, 0))
                    pygame.display.update()
                 
            # Blit list of explosions to screen
            if enemy_explo == True:
                current_explo.blit(screen, (collision_x, collision_y - 78))

            EXPLOANIM2.blit(screen, (player.rect.x, player.rect.y))

            # Display coins
            for obj in loot_group:
                obj.COINANIM.blit(screen, (obj.rect.x, obj.rect.y))
        


            # Display fps label
            if fps_toggle == True:
                screen.blit(fps_label, (1500, 10))

            screen.blit(name_label, (10, 20))
            screen.blit(money_label, (10, 70))


            dirty_groups = arena_sprites.draw(screen)

        # Update groups of sprites
        pygame.display.update(dirty_groups)

        # Update rects
        pygame.display.update(dirty_rects)

        clock.tick(FPS)
        
main()





