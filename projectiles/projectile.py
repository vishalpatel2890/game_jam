import pygame

# green_flask = [pygame.image.load('projectiles/images/erl_flask_GREEN1.png'), pygame.image.load('projectiles/images/erl_flask_GREEN2.png'), pygame.image.load('projectiles/images/erl_flask_GREEN3.png'), pygame.image.load('projectiles/images/erl_flask_GREEN4.png'), pygame.image.load('projectiles/images/erl_flask_GREEN5.png'), pygame.image.load('projectiles/images/erl_flask_GREEN6.png'), pygame.image.load('projectiles/images/erl_flask_GREEN7.png'), pygame.image.load('projectiles/images/erl_flask_GREEN8.png'), pygame.image.load('projectiles/images/erl_flask_GREEN9.png'), pygame.image.load('projectiles/images/erl_flask_GREEN10.png')]

green_flask = [pygame.image.load('projectiles/images/erl_flask_GREEN11.png'), pygame.image.load('projectiles/images/erl_flask_GREEN12.png'), pygame.image.load('projectiles/images/erl_flask_GREEN13.png'), pygame.image.load('projectiles/images/erl_flask_GREEN14.png'), pygame.image.load('projectiles/images/erl_flask_GREEN15.png'), pygame.image.load('projectiles/images/erl_flask_GREEN16.png'), pygame.image.load('projectiles/images/erl_flask_GREEN17.png'), pygame.image.load('projectiles/images/erl_flask_GREEN18.png'), pygame.image.load('projectiles/images/erl_flask_GREEN19.png'), pygame.image.load('projectiles/images/erl_flask_GREEN20.png'),pygame.image.load('projectiles/images/erl_flask_GREEN21.png'), pygame.image.load('projectiles/images/erl_flask_GREEN22.png'), pygame.image.load('projectiles/images/erl_flask_GREEN23.png'), pygame.image.load('projectiles/images/erl_flask_GREEN24.png'), pygame.image.load('projectiles/images/erl_flask_GREEN25.png'), pygame.image.load('projectiles/images/erl_flask_GREEN26.png'), pygame.image.load('projectiles/images/erl_flask_GREEN27.png'), pygame.image.load('projectiles/images/erl_flask_GREEN28.png'), pygame.image.load('projectiles/images/erl_flask_GREEN29.png'), pygame.image.load('projectiles/images/erl_flask_GREEN30.png')]

red_flask = [pygame.image.load('projectiles/images/erl_flask_RED1.png'), pygame.image.load('projectiles/images/erl_flask_RED2.png'), pygame.image.load('projectiles/images/erl_flask_RED3.png'), pygame.image.load('projectiles/images/erl_flask_RED4.png'), pygame.image.load('projectiles/images/erl_flask_RED5.png'), pygame.image.load('projectiles/images/erl_flask_RED6.png'), pygame.image.load('projectiles/images/erl_flask_RED7.png'), pygame.image.load('projectiles/images/erl_flask_RED8.png'), pygame.image.load('projectiles/images/erl_flask_RED9.png'), pygame.image.load('projectiles/images/erl_flask_RED10.png')]
#
purple_flask_ = [pygame.image.load('projectiles/images/erl_flask_PURP1.png'), pygame.image.load('projectiles/images/erl_flask_PURP2.png'), pygame.image.load('projectiles/images/erl_flask_PURP3.png'), pygame.image.load('projectiles/images/erl_flask_PURP4.png'), pygame.image.load('projectiles/images/erl_flask_PURP5.png'), pygame.image.load('projectiles/images/erl_flask_PURP6.png'), pygame.image.load('projectiles/images/erl_flask_PURP7.png'), pygame.image.load('projectiles/images/erl_flask_PURP8.png'), pygame.image.load('projectiles/images/erl_flask_PURP9.png'), pygame.image.load('projectiles/images/erl_flask_PURP10.png')]



class projectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing
        self.flask_bubbles = 0


    def draw(self, win):
        """Blit the erl_flask to the window."""
        if self.flask_bubbles + 1 >= 60:
            self.flask_bubbles = 0
        win.blit(pygame.transform.scale(green_flask[self.flask_bubbles//3], (32,32)), (self.x,self.y-12))
        self.flask_bubbles += 1






















#
