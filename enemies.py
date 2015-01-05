from weapon import *


enemy_attackers = pygame.sprite.RenderUpdates()


# Make enemy sprite to be put in groups
class KamikazeEnemy(pygame.sprite.Sprite):
    def __init__(enemy, x, y, image):
        pygame.sprite.Sprite.__init__(enemy)
        enemy.image  = image
        enemy.rect   = enemy.image.get_rect()
        enemy.rect.x = x
        enemy.rect.y = y

    # Particular enemy movement style (chase and then kamikaze into player)
    def update(enemy, victim_x, victim_y):
        enemy.victim_x = victim_x
        enemy.victim_y = victim_y
        if enemy.rect.x > enemy.victim_x:
            enemy.rect.x -= ENEMYSPEED
        if enemy.rect.x < enemy.victim_x:
            enemy.rect.x += ENEMYSPEED
        if enemy.rect.y < enemy.victim_y:
            enemy.rect.y += ENEMYSPEED
        if enemy.rect.y > enemy.victim_y:
            enemy.rect.y -= ENEMYSPEED

# Maybe do asteroid too
class DroneEnemy(pygame.sprite.Sprite):
    def __init__(enemy, x, y, image):
        pygame.sprite.Sprite.__init__(enemy)
        enemy.image  = image
        enemy.rect   = enemy.image.get_rect()
        enemy.rect.x = x
        enemy.rect.y = y

#    def update(enemy):


class StarEnemy(pygame.sprite.Sprite):
    def __init__(enemy, x, y, image):
        pygame.sprite.Sprite.__init__(enemy)
        enemy.image  = image
        enemy.rect   = enemy.image.get_rect()
        enemy.rect.x = x
        enemy.rect.y = y
        enemy.dest_x = random.randint(0, WINDOWWIDTH - ENEMYWIDTH)
        enemy.dest_y = random.randint(0, WINDOWHEIGHT - ENEMYHEIGHT)

    def update(enemy, enemy_weap_group, arena_sprites, LASERSOUND, LASERIMAGE, spawn_ctr):
        if abs(enemy.rect.x - enemy.dest_x) > ENEMYSPEED or abs(enemy.rect.y - enemy.dest_y) > ENEMYSPEED:
            if enemy.rect.x > enemy.dest_x:
                enemy.rect.x -= ENEMYSPEED
            if enemy.rect.x < enemy.dest_x:
                enemy.rect.x += ENEMYSPEED
            if enemy.rect.y < enemy.dest_y:
                enemy.rect.y += ENEMYSPEED
            if enemy.rect.y > enemy.dest_y:
                enemy.rect.y -= ENEMYSPEED
        else:
            if spawn_ctr % 50 == 0:
                # Lists configured for weapon starting coords, to prevent weapon and enemy collision upon enemy firing
                coords_x = [0, 0, (ENEMYWIDTH), -(ENEMYWIDTH)]
                coords_y = [-(ENEMYHEIGHT), (ENEMYHEIGHT), 0, 0]

                LASERSOUND.play()
                enemy_center_x = enemy.rect.x + (ENEMYWIDTH/2)
                enemy_center_y = enemy.rect.y + (ENEMYHEIGHT/2)
                north_vector = normalize(sub((enemy_center_x, enemy_center_y - 1), (enemy_center_x, enemy_center_y)))
                south_vector = normalize(sub((enemy_center_x, enemy_center_y + 1), (enemy_center_x, enemy_center_y)))
                east_vector  = normalize(sub((enemy_center_x + 1, enemy_center_y), (enemy_center_x, enemy_center_y)))
                west_vector  = normalize(sub((enemy_center_x - 1, enemy_center_y), (enemy_center_x, enemy_center_y)))
                ortho_vects = [north_vector, south_vector, east_vector, west_vector]
                i = 0
                while i < len(ortho_vects):
                    if i == 0 or i == 1:
                        shot_angle = 90

                    elif i == 2 or i == 3:
                        shot_angle = 0

                    weapon = Weapon(LASERIMAGE, enemy_center_x + coords_x[i], enemy_center_y + coords_y[i], shot_angle, ortho_vects[i])
                    enemy_weap_group.add(weapon)
                    arena_sprites.add(weapon)
                    enemy_attackers.add(weapon)
                    arena_sprites.move_to_back(weapon)
                    i += 1