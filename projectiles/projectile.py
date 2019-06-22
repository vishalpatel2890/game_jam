import pygame

green_flask = [pygame.image.load('projectiles/images/erl_flask_GREEN1.png'), pygame.image.load('projectiles/images/erl_flask_GREEN2.png'), pygame.image.load('projectiles/images/erl_flask_GREEN3.png'), pygame.image.load('projectiles/images/erl_flask_GREEN4.png'), pygame.image.load('projectiles/images/erl_flask_GREEN5.png'), pygame.image.load('projectiles/images/erl_flask_GREEN6.png'), pygame.image.load('projectiles/images/erl_flask_GREEN7.png'), pygame.image.load('projectiles/images/erl_flask_GREEN8.png'), pygame.image.load('projectiles/images/erl_flask_GREEN9.png'), pygame.image.load('projectiles/images/erl_flask_GREEN10.png')]

# rename to red_flask afterwards --->
red_flask = [pygame.image.load('projectiles/images/erl_flask_RED1.png'), pygame.image.load('projectiles/images/erl_flask_RED2.png'), pygame.image.load('projectiles/images/erl_flask_RED3.png'), pygame.image.load('projectiles/images/erl_flask_RED4.png'), pygame.image.load('projectiles/images/erl_flask_RED5.png'), pygame.image.load('projectiles/images/erl_flask_RED6.png'), pygame.image.load('projectiles/images/erl_flask_RED7.png'), pygame.image.load('projectiles/images/erl_flask_RED8.png'), pygame.image.load('projectiles/images/erl_flask_RED9.png'), pygame.image.load('projectiles/images/erl_flask_RED10.png')]
#
purple_flask_ = [pygame.image.load('projectiles/images/erl_flask_PURPLE1.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE2.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE3.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE4.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE5.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE6.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE7.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE8.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE9.png'), pygame.image.load('projectiles/images/erl_flask_PURPLE10.png')]



class projectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing
        self.flask_bubbles = 0


    def draw(self, win):
        """Blit the erl_flask to the window."""
        if self.flask_bubbles + 1 >= 30:
            self.flask_bubbles = 0
        win.blit(pygame.transform.scale(green_flask[self.flask_bubbles//3], (32,32)), (self.x,self.y-12))
        self.flask_bubbles += 1

        # win.blit(pygame.transform.scale(green_flask[0], (36,36)), (self.x,self.y-12))




        # if not(self.standing):
        #     if self.left:
        #         win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
        #         self.walkCount += 1
        #     elif self.right:
        #         win.blit(walkRight[self.walkCount//3], (self.x,self.y))
        #         self.walkCount +=1





















#
