from prepare import *

# Create player menu sprite
class PlayerMenu(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bot_right = True
        self.bot_left  = False
        self.top_right = False
        self.top_left  = False


    def update(self, menu_origin_x, menu_origin_y):
        if self.bot_right == True:
            self.rect.x = menu_origin_x
            self.rect.y = menu_origin_y
        elif self.bot_left == True:
            self.rect.x = menu_origin_x - (PLAYERWIDTH + MENUWIDTH)
            self.rect.y = menu_origin_y
        elif self.top_right == True:
            self.rect.x = menu_origin_x
            self.rect.y = menu_origin_y - (PLAYERHEIGHT + MENUHEIGHT)
        elif self.top_left == True:
            self.rect.x = menu_origin_x - (PLAYERWIDTH + MENUWIDTH)
            self.rect.y = menu_origin_y - (PLAYERHEIGHT + MENUHEIGHT)

    # Change position of floating player menu when is collides with borders
    def handlePlayerMenuPos(self, right_wall, left_wall, top_wall, bottom_wall):
        if pygame.sprite.collide_rect(self, right_wall):
            if self.bot_right == True:
                self.bot_right = False
                self.bot_left  = True
            elif self.top_right == True:
                self.top_right = False
                self.top_left = True
        elif pygame.sprite.collide_rect(self, left_wall):
            if self.bot_left == True:
                self.bot_left = False
                self.bot_right = True
            elif self.top_left == True:
                self.top_left = False
                self.top_right = True
        elif pygame.sprite.collide_rect(self, top_wall):
            if self.top_right == True:
                self.top_right = False
                self.bot_right = True
            elif self.top_left == True:
                self.top_left = False
                self.bot_left = True
        elif pygame.sprite.collide_rect(self, bottom_wall):
            if self.bot_right == True:
                self.bot_right = False
                self.top_right = True
            elif self.bot_left == True:
                self.bot_left = False
                self.top_left = True
