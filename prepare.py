import pyganim

from generics import *


# Constants
FPS          = 100

WINDOWWIDTH  = 1600
WINDOWHEIGHT = 900

ENEMYSPEED   = 4
ENEMYWIDTH   = 50
ENEMYHEIGHT  = 50

PLAYERSPEED  = 10
PLAYERHEALTH = 100
PLAYERARMOR  = 100
PLAYERWIDTH  = 100
PLAYERHEIGHT = 100

MENUWIDTH  = 400
MENUHEIGHT = 300

LASERWIDTH   = 30
LASERHEIGHT  = 5
LASERSPEED   = 16

# Color palette
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

BGCOLOR  = ( 28,  28,  28)


pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock  = pygame.time.Clock()
pygame.display.set_caption('Project Super Awesome Fun Time')
pygame.mouse.set_visible(False)

# Fonts
FPSFONT  = pygame.font.SysFont('monospace', 15)
HUDFONT  = pygame.font.SysFont('monospace', 17)
NAMEFONT = pygame.font.SysFont('monospace', 20, bold = True)

# Graphics converted to save memory

# HUD
HEALTHSHEET = pygame.image.load('images/healthbars.png').convert_alpha()
HEALTHBARS = cutSpriteSheet(200, 10, 5, 30, HEALTHSHEET, 11)

PLAYERMENU = pygame.image.load('images/player menu.png').convert_alpha()

# Loots
COINSHEET = pygame.image.load('images/spinning gold coin.png').convert_alpha()

# Explosions
EXPLOSIONRECT = pygame.image.load('explosion rect.png')
EXPLOSHEET1 = pygame.image.load('images/explo1.png').convert_alpha()
EXPLOSHEET2 = pygame.image.load('images/explo2.png').convert_alpha()

# Enemy
EYEBALLIMAGE = pygame.image.load('images/eyeball.png').convert_alpha()
ENEMYIMAGE   = pygame.image.load('images/enemy.png').convert_alpha()
BLANKENEMY   = pygame.image.load('images/blank enemy.png').convert_alpha()

# Cursor
CROSSHAIR = pygame.image.load('images/crosshair.png').convert_alpha()

# Player
BLUESHIP   = pygame.image.load('images/blueship.png').convert_alpha()

# Weapon
LASERIMAGE = pygame.image.load('images/laser horiz.png').convert_alpha()

# Border
RIGHTWALL  = pygame.image.load('images/right wall.png').convert_alpha()
LEFTWALL   = pygame.image.load('images/left wall.png').convert_alpha()
TOPWALL    = pygame.image.load('images/top wall.png').convert_alpha()
BOTTOMWALL = pygame.image.load('images/bottom wall.png').convert_alpha()

# Background
SPACEIMAGE = pygame.image.load('images/space.png').convert_alpha()

# Planets
PLANET1 = pygame.image.load('images/planet1.png').convert_alpha()
PLANET2 = pygame.image.load('images/planet2.png').convert_alpha()
PLANET3 = pygame.image.load('images/planet3.png').convert_alpha()
PLANET4 = pygame.image.load('images/planet4.png').convert_alpha()

# Explosion animations
explo_sprites_1 = cutSpriteSheet(50, 128, 18, 128, EXPLOSHEET1, 18)

EXPLOANIM1 = pyganim.PygAnimation(
    [(explo_sprites_1[0], 0.05), (explo_sprites_1[1], 0.05), (explo_sprites_1[2], 0.05),
     (explo_sprites_1[3], 0.05), (explo_sprites_1[4], 0.05), (explo_sprites_1[5], 0.05),
     (explo_sprites_1[6], 0.05), (explo_sprites_1[7], 0.05), (explo_sprites_1[8], 0.05),
     (explo_sprites_1[9], 0.05), (explo_sprites_1[10], 0.05), (explo_sprites_1[11], 0.05),
     (explo_sprites_1[12], 0.05), (explo_sprites_1[13], 0.05), (explo_sprites_1[14], 0.05),
     (explo_sprites_1[15], 0.05), (explo_sprites_1[16], 0.05), (explo_sprites_1[17], 0.05)],
    loop = False)

explo_sprites_2 = cutSpriteSheet(64, 64, 8, 512, EXPLOSHEET2, 36)

EXPLOANIM2 = pyganim.PygAnimation(
    [(explo_sprites_2[0], 0.05), (explo_sprites_2[1], 0.05), (explo_sprites_2[2], 0.05),
     (explo_sprites_2[3], 0.05), (explo_sprites_2[4], 0.05), (explo_sprites_2[5], 0.05),
     (explo_sprites_2[6], 0.05), (explo_sprites_2[7], 0.05), (explo_sprites_2[8], 0.05),
     (explo_sprites_2[9], 0.05), (explo_sprites_2[10], 0.05), (explo_sprites_2[11], 0.05),
     (explo_sprites_2[12], 0.05), (explo_sprites_2[13], 0.05), (explo_sprites_2[14], 0.05),
     (explo_sprites_2[15], 0.05), (explo_sprites_2[16], 0.05), (explo_sprites_2[17], 0.05),
     (explo_sprites_2[18], 0.05), (explo_sprites_2[19], 0.05), (explo_sprites_2[20], 0.05),
     (explo_sprites_2[21], 0.05), (explo_sprites_2[22], 0.05), (explo_sprites_2[23], 0.05),
     (explo_sprites_2[24], 0.05), (explo_sprites_2[25], 0.05), (explo_sprites_2[26], 0.05),
     (explo_sprites_2[27], 0.05), (explo_sprites_2[28], 0.05), (explo_sprites_2[29], 0.05),
     (explo_sprites_2[30], 0.05), (explo_sprites_2[31], 0.05), (explo_sprites_2[32], 0.05),
     (explo_sprites_2[33], 0.05), (explo_sprites_2[34], 0.05), (explo_sprites_2[35], 0.05)],
    loop = False)

# Sounds
LASERSOUND     = pygame.mixer.Sound('sounds/laser.wav')
EXPLOSIONSOUND = pygame.mixer.Sound('sounds/explosion.wav')
COLLECTCOIN    = pygame.mixer.Sound('sounds/collect coin.wav')

