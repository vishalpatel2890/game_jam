import pygame
import pygame as pg

walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]

DIRECT_DICT = {pg.K_UP   : ( 0,-1),
               pg.K_DOWN : ( 0, 1),
               pg.K_RIGHT: ( 1, 0),
               pg.K_LEFT : (-1, 0)}

class Player(object):
    """Our user controllable character."""
    def __init__(self, image, location, speed):
        """
        The location is an (x,y) coordinate; speed is in pixels per frame.
        The location of the player is with respect to the map he is in; not the
        display screen.
        """
        self.speed = speed
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=location)

    def update(self, keys, image_dim):
        """
        Check pressed keys to find initial movement vector.  Then call
        collision detection methods and adjust the vector appropriately.
        """
        move = self.check_keys(keys)
        self.move(move, image_dim)

    def check_keys(self, keys):
        """Find the players movement vector from key presses."""
        move = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                for i in (0, 1):
                    move[i] += DIRECT_DICT[key][i]*self.speed
        return move

    def move(self, move, image_dim):
        """
        Determine where to  move based on key stroke
        """
        # x_change = self.collision_detail(move, level_mask, 0)
        if self.rect[0] > self.speed and self.rect[0] < 1776 - self.speed:
            self.rect.move_ip((move[0],0))
        elif self.rect[0] <= self.speed and self.rect[0] > 0:
            self.rect.move_ip(1,0)
        elif self.rect[0] >= 1776 - self.speed :
            self.rect.move_ip(-1, 0)
        # y_change = self.collision_detail(move, level_mask, 1)
        if self.rect[1] > self.speed and self.rect[1] < 960 - self.speed :
            self.rect.move_ip((0,move[1]))
        elif self.rect[1] <= self.speed and self.rect[1] > 0:
            self.rect.move_ip(0,1)
        elif self.rect[1] >= 960 - self.speed:
            self.rect.move_ip(0,-1)

    def draw(self, surface):
        """Basic draw function."""
        surface.blit(self.image, self.rect)
