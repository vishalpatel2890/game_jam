import pygame

from player import player
from projectiles.projectile  import projectile
from enemy import enemy

pygame.init()

screenWidth = 500
screenHeight = 500
win = pygame.display.set_mode((screenWidth,screenHeight))

pygame.display.set_caption("First Game")

# This goes outside the while loop, near the top of the program
bg = pygame.image.load('Game/bulkhead-walls.png')
char = pygame.image.load('Game/standing.png')

clock = pygame.time.Clock()

def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

#mainloop
man = player(200, 330, 64, 64)
goblin = enemy(100, 330, 64, 64, 300)
shootLoop = 0
bullets = []
run = True

while run:
    clock.tick(27)

    keys = pygame.key.get_pressed()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 6:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 7:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), facing))
        shootLoop = 1


    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
