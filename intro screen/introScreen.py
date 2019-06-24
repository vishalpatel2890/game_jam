import pygame
import time
import random
 
pygame.init()
 
display_width = 500
display_height = 500
 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)
 
car_width = 73
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('racecar.png')
introImg = pygame.image.load('introScreen.png')

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)
 
    game_loop()
    
    

def crash():
    message_display('You Crashed')
    
def quitgame():
    pygame.quit()
    quit()


def update(self):
    """Update the player, obstacles, and current viewport."""
    self.keys = pygame.key.get_pressed()
    
    
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.blit(introImg,(0,0))

#         if event.type == pygame.QUIT or self.keys[pg.K_ESCAPE]:
#             quitgame

        pygame.display.update()
        clock.tick(15)        
        
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    x_change = 0
 
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
 
    thingCount = 1
 
    dodged = 0
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(white)
 
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
 
 
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
 
        if x > display_width - car_width or x < 0:
            crash()
 
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)
 
        if y < thing_starty+thing_height:
            print('y crossover')
 
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()


# """
#  Example program to show how to do an instruction screen.
 
#  Sample Python/Pygame Programs
#  Simpson College Computer Science
#  http://programarcadegames.com/
#  http://simpson.edu/computer-science/
# """
 
# import pygame
 
# # Define some colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
 
# pygame.init()
 
# # Set the height and width of the screen
# size = [700, 500]
# screen = pygame.display.set_mode(size)
 
# pygame.display.set_caption("Instruction Screen")
 
# # Loop until the user clicks the close button.
# done = False
 
# # Used to manage how fast the screen updates
# clock = pygame.time.Clock()
 
# # Starting position of the rectangle
# rect_x = 50
# rect_y = 50
 
# # Speed and direction of rectangle
# rect_change_x = 5
# rect_change_y = 5
 
# # This is a font we use to draw text on the screen (size 36)
# font = pygame.font.Font(None, 36)
 
# display_instructions = True
# instruction_page = 1
 
# # -------- Instruction Page Loop -----------
# while not done and display_instructions:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             instruction_page += 1
#             if instruction_page == 3:
#                 display_instructions = False
 
#     # Set the screen background
#     screen.fill(BLACK)
 
#     if instruction_page == 1:
#         # Draw instructions, page 1
#         # This could also load an image created in another program.
#         # That could be both easier and more flexible.
 
#         text = font.render("PRCILLA AND THE WeKYUBE MACHINE", True, WHITE)
#         screen.blit(text, [10, 10])
 
#         text = font.render("Page 1", True, WHITE)
#         screen.blit(text, [10, 40])
 
#     if instruction_page == 2:
#         # Draw instructions, page 2
#         text = font.render("This program bounces a rectangle", True, WHITE)
#         screen.blit(text, [10, 10])
 
#         text = font.render("Page 2", True, WHITE)
#         screen.blit(text, [10, 40])
 
#     # Limit to 60 frames per second
#     clock.tick(60)
 
#     # Go ahead and update the screen with what we've drawn.
#     pygame.display.flip()
 
# # -------- Main Program Loop -----------
# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
 
#     # Set the screen background
#     screen.fill(BLACK)
 
#     # Draw the rectangle
#     pygame.draw.rect(screen, WHITE, [rect_x, rect_y, 50, 50])
 
#     # Move the rectangle starting point
#     rect_x += rect_change_x
#     rect_y += rect_change_y
 
#     # Bounce the ball if needed
#     if rect_y > 450 or rect_y < 0:
#         rect_change_y = rect_change_y * -1
#     if rect_x > 650 or rect_x < 0:
#         rect_change_x = rect_change_x * -1
 
#     # Limit to 60 frames per second
#     clock.tick(60)
 
#     # Go ahead and update the screen with what we've drawn.
#     pygame.display.flip()
 
# # Be IDLE friendly. If you forget this line, the program will 'hang'
# # on exit.
# pygame.quit()