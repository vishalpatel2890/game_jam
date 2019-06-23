"""
Basic moving platforms using only rectangle collision.
-Written by Sean J. McKiernan 'Mekire'
"""

import os
import sys
import pygame as pg
import time
import random

walkRight = [pg.transform.scale(pg.image.load(f"images/hero_walk_{f'{x:02d}'}.png"), (32,32)) for x in range(1,21)]
walkLeft = [pg.transform.flip(pg.transform.scale(pg.image.load(f"images/hero_walk_{f'{x:02d}'}.png"), (32,32)), True, False) for x in range(1,21)]
idleRight = pg.transform.scale(pg.image.load("images/hero_idle.png"), (32,32))
idleLeft = pg.transform.flip(pg.transform.scale(pg.image.load("images/hero_idle.png"), (32,32)), True, False)

clock = pg.time.Clock()
introImg = pg.image.load('introScreen.png')


CAPTION = "Moving Platforms"
SCREEN_SIZE = (1200,700)


class _Physics(object):
	"""A simplified physics class. Psuedo-gravity is often good enough."""
	def __init__(self):
		"""You can experiment with different gravity here."""
		self.x_vel = self.y_vel = 0
		self.grav = 0.4
		self.fall = False

	def physics_update(self):
		"""If the player is falling, add gravity to the current y velocity."""
		if self.fall:
			self.y_vel += self.grav
		else:
			self.y_vel = 0

class background(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location            

class Player(_Physics, pg.sprite.Sprite):
	"""Class representing our player."""
	def __init__(self,location,speed):
		"""
		The location is an (x,y) coordinate pair, and speed is the player's
		speed in pixels per frame. Speed should be an integer.
		"""
		_Physics.__init__(self)
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((20,30)).convert()
		self.image.fill(pg.Color("red"))
		self.rect = self.image.get_rect(topleft=(location[0],location[1]+2))
		self.speed = speed
		self.jump_power = -9.0
		self.jump_cut_magnitude = -3.0
		self.on_moving = False
		self.collide_below = False
		#Add death variable
		self.alive=True
		self.left = False
		self.right = True
		self.walkCount = 0
		self.standing = True

	def check_keys(self, keys):
		"""Find the player's self.x_vel based on currently held keys."""
		self.x_vel = 0
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.x_vel -= self.speed
			self.left = True
			self.right = False
			self.standing = False
		elif keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.x_vel += self.speed
			self.left = False
			self.right = True
			self.standing = False
		else:
			self.standing = True
			self.walkCount = 0

	def get_position(self, obstacles):
		"""Calculate the player's position this frame, including collisions."""
		if not self.fall:
			self.check_falling(obstacles)
		else:
			self.fall = self.check_collisions((0,self.y_vel), 1, obstacles)
		if self.x_vel:
			self.check_collisions((self.x_vel,0), 0, obstacles)

	def check_falling(self, obstacles):
		"""If player is not contacting the ground, enter fall state."""
		if not self.collide_below:
			self.fall = True
			self.on_moving = False

	def check_moving(self,obstacles):
		"""
		Check if the player is standing on a moving platform.
		If the player is in contact with multiple platforms, the prevously
		detected platform will take presidence.
		"""
		if not self.fall:
			now_moving = self.on_moving
			any_moving, any_non_moving = [], []
			for collide in self.collide_below:
				# Added condition for standing on top of "Kyoobs"
				if collide.type == "moving" or collide.type =="enemy":
					self.on_moving = collide
					any_moving.append(collide)
				else:
					any_non_moving.append(collide)
			if not any_moving:
				self.on_moving = False
			elif any_non_moving or now_moving in any_moving:
				self.on_moving = now_moving

	def check_collisions(self, offset, index, obstacles):
		"""
		This function checks if a collision would occur after moving offset
		pixels. If a collision is detected, the position is decremented by one
		pixel and retested. This continues until we find exactly how far we can
		safely move, or we decide we can't move.
		"""
		unaltered = True
		self.rect[index] += offset[index]
		while pg.sprite.spritecollideany(self, obstacles):
			self.rect[index] += (1 if offset[index]<0 else -1)
			unaltered = False
		return unaltered

	def check_above(self, obstacles):
		"""When jumping, don't enter fall state if there is no room to jump."""
		self.rect.move_ip(0, -1)
		collide = pg.sprite.spritecollideany(self, obstacles)
		self.rect.move_ip(0, 1)
		return collide

	def check_below(self, obstacles):
		"""Check to see if the player is contacting the ground."""
		self.rect.move_ip((0,1))
		collide = pg.sprite.spritecollide(self, obstacles, False)
		self.rect.move_ip((0,-1))
		return collide

	def jump(self, obstacles):
		"""Called when the user presses the jump button."""
		if not self.fall and not self.check_above(obstacles):
			self.y_vel = self.jump_power
			self.fall = True
			self.on_moving = False

	def jump_cut(self):
		"""Called if player releases the jump key before maximum height."""
		if self.fall:
			if self.y_vel < self.jump_cut_magnitude:
				self.y_vel = self.jump_cut_magnitude

	def pre_update(self, obstacles):
		"""Ran before platforms are updated."""
		self.collide_below = self.check_below(obstacles)
		self.check_moving(obstacles)

	def update(self, obstacles, keys):
		"""Everything we need to stay updated; ran after platforms update."""
		self.check_keys(keys)
		self.get_position(obstacles)
		self.physics_update()

	def draw(self, win):
	# 	"""Blit the player to the target surface."""
		# win.blit(self.image, self.rect) # drawing hitbox for testing
		if self.walkCount + 1 >= 40:
			self.walkCount = 0

		# the blits were offset manually to draw the character inside of the character box. Surely there's a better way to do this.
		if not(self.standing) and not self.fall:
			if self.left:
				win.blit(walkLeft[self.walkCount//2], (self.rect[0]-3,self.rect[1]-2))
				self.walkCount += 1
			elif self.right:
				win.blit(walkRight[self.walkCount//2], (self.rect[0]-8,self.rect[1]-2))
				self.walkCount +=1
		else:
			if self.right:
				win.blit(idleRight, (self.rect[0]-8,self.rect[1]-2))
			else:
				win.blit(idleLeft, (self.rect[0]-3,self.rect[1]-2))

class Block(pg.sprite.Sprite):
	"""A class representing solid obstacles."""
	def __init__(self, color, rect):
		"""The color is an (r,g,b) tuple; rect is a rect-style argument."""
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect(rect)
		self.image = pg.Surface(self.rect.size).convert()
		self.image.fill(color)
		self.type = "normal"

class imgBlock(pg.sprite.Sprite):
	"""A class representing solid obstacles."""
	def __init__(self, image, rect):
		"""The color is an (r,g,b) tuple; rect is a rect-style argument."""
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface(self.rect.size).convert()
		self.image.fill(color)

# 		self.image = pg.image.load('plat_narrow.png')
		self.rect = pg.Rect(rect)

# 		self.image.fill(color)
		self.type = "normal"

class imgMovingBlock(imgBlock):
	"""A class to represent horizontally and vertically moving blocks."""
	def __init__(self, image, rect, end, axis, delay=500, speed=2, start=None):
		"""
		The moving block will travel in the direction of axis (0 or 1)
		between rect.topleft and end. The delay argument is the amount of time
		(in miliseconds) to pause when reaching an endpoint; speed is the
		platforms speed in pixels/frame; if specified start is the place
		within the blocks path to start (defaulting to rect.topleft).
		"""
		Block.__init__(self, image, rect)
		self.start = self.rect[axis]
		if start:
			self.rect[axis] = start
		self.axis = axis
		self.end = end
		self.timer = 0.0
		self.delay = delay
		self.speed = speed
		self.waiting = False
		self.type = "moving"

	def update(self, player, obstacles):
		"""Update position. This should be done before moving any actors."""
		obstacles = obstacles.copy()
		obstacles.remove(self)
		now = pg.time.get_ticks()
		if not self.waiting:
			speed = self.speed
			start_passed = self.start >= self.rect[self.axis]+speed
			end_passed = self.end <= self.rect[self.axis]+speed
			if start_passed or end_passed:
				if start_passed:
					speed = self.start-self.rect[self.axis]
				else:
					speed = self.end-self.rect[self.axis]
				self.change_direction(now)
			self.rect[self.axis] += speed
			self.move_player(now, player, obstacles, speed)
		elif now-self.timer > self.delay:
			self.waiting = False

	def move_player(self, now, player, obstacles, speed):
		"""
		Moves the player both when on top of, or bumped by the platform.
		Collision checks are in place to prevent the block pushing the player
		through a wall.
		"""
		if player.on_moving is self or pg.sprite.collide_rect(self,player):
			axis = self.axis
			offset = (speed, speed)
			player.check_collisions(offset, axis, obstacles)
			if pg.sprite.collide_rect(self, player):
				if self.speed > 0:
					self.rect[axis] = player.rect[axis]-self.rect.size[axis]
				else:
					self.rect[axis] = player.rect[axis]+player.rect.size[axis]
				self.change_direction(now)

	def change_direction(self, now):
		"""Called when the platform reaches an endpoint or has no more room."""
		self.waiting = True
		self.timer = now
		self.speed *= -1

        
class imgCube(imgMovingBlock):

	def __init__(self,image,rect,end,axis, delay=100, speed=3, start=None):
		"""Use type on collision checks"""
		MovingBlock.__init__(self, image, rect, end, axis, delay=500, speed=2, start=None)
		self.type = "enemy"
	
	def move_player(self, now, player, obstacles, speed):
		"""
		Moves the player when on top of, or destroys if bumped by the cube.
		"""
		if player.on_moving is self:
			axis = self.axis
			offset = (speed, speed)
			player.check_collisions(offset, axis, obstacles)
			if pg.sprite.collide_rect(self, player):
				if self.speed > 0:
					self.rect[axis] = player.rect[axis]-self.rect.size[axis]
				else:
					self.rect[axis] = player.rect[axis]+player.rect.size[axis]
				self.change_direction(now)
		elif pg.sprite.collide_rect(self,player):
			player.alive = False
        
        

class MovingBlock(Block):
	"""A class to represent horizontally and vertically moving blocks."""
	def __init__(self, color, rect, end, axis, delay=500, speed=2, start=None):
		"""
		The moving block will travel in the direction of axis (0 or 1)
		between rect.topleft and end. The delay argument is the amount of time
		(in miliseconds) to pause when reaching an endpoint; speed is the
		platforms speed in pixels/frame; if specified start is the place
		within the blocks path to start (defaulting to rect.topleft).
		"""
		Block.__init__(self, color, rect)
		self.start = self.rect[axis]
		if start:
			self.rect[axis] = start
		self.axis = axis
		self.end = end
		self.timer = 0.0
		self.delay = delay
		self.speed = speed
		self.waiting = False
		self.type = "moving"

	def update(self, player, obstacles):
		"""Update position. This should be done before moving any actors."""
		obstacles = obstacles.copy()
		obstacles.remove(self)
		now = pg.time.get_ticks()
		if not self.waiting:
			speed = self.speed
			start_passed = self.start >= self.rect[self.axis]+speed
			end_passed = self.end <= self.rect[self.axis]+speed
			if start_passed or end_passed:
				if start_passed:
					speed = self.start-self.rect[self.axis]
				else:
					speed = self.end-self.rect[self.axis]
				self.change_direction(now)
			self.rect[self.axis] += speed
			self.move_player(now, player, obstacles, speed)
		elif now-self.timer > self.delay:
			self.waiting = False

	def move_player(self, now, player, obstacles, speed):
		"""
		Moves the player both when on top of, or bumped by the platform.
		Collision checks are in place to prevent the block pushing the player
		through a wall.
		"""
		if player.on_moving is self or pg.sprite.collide_rect(self,player):
			axis = self.axis
			offset = (speed, speed)
			player.check_collisions(offset, axis, obstacles)
			if pg.sprite.collide_rect(self, player):
				if self.speed > 0:
					self.rect[axis] = player.rect[axis]-self.rect.size[axis]
				else:
					self.rect[axis] = player.rect[axis]+player.rect.size[axis]
				self.change_direction(now)

	def change_direction(self, now):
		"""Called when the platform reaches an endpoint or has no more room."""
		self.waiting = True
		self.timer = now
		self.speed *= -1


class Cube(MovingBlock):

	def __init__(self,color,rect,end,axis, delay=100, speed=3, start=None):
		"""Use type on collision checks"""
		MovingBlock.__init__(self, color, rect, end, axis, delay=500, speed=2, start=None)
		self.type = "enemy"
	
	def move_player(self, now, player, obstacles, speed):
		"""
		Moves the player when on top of, or destroys if bumped by the cube.
		"""
		if player.on_moving is self:
			axis = self.axis
			offset = (speed, speed)
			player.check_collisions(offset, axis, obstacles)
			if pg.sprite.collide_rect(self, player):
				if self.speed > 0:
					self.rect[axis] = player.rect[axis]-self.rect.size[axis]
				else:
					self.rect[axis] = player.rect[axis]+player.rect.size[axis]
				self.change_direction(now)
		elif pg.sprite.collide_rect(self,player):
			player.alive = False

class Control(object):
	"""Class for managing event loop and game states."""
	def __init__(self):
		"""Initalize the display and prepare game objects."""
		self.screen = pg.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.clock = pg.time.Clock()
		self.fps = 60.0
		self.keys = pg.key.get_pressed()
		self.done = False
		self.player = Player((50,875), 4)
		self.background = background('background.png', [0,0])
		self.viewport = self.screen.get_rect()
		self.level = pg.Surface((1568,928)).convert()
		self.level_rect = self.level.get_rect()
		self.win_text,self.win_rect = self.make_text()
		self.obstacles = self.make_obstacles()

	def make_text(self, message = "Head this way!"):
		"""Renders a text object. Text is only rendered once."""

		# Added functionality for custom message and placement
		font = pg.font.Font(None, 30)
		text = font.render(message, True, (255,255,255))
		rect = text.get_rect(x=1024, y=64)
		return text, rect

	def make_obstacles(self):
		"""Adds some arbitrarily placed obstacles to a sprite.Group."""
		"""left x, y, width, depth """
		walls = [Block(pg.Color("chocolate"), (0,912,1568,16)),
				 Block(pg.Color("chocolate"), (0,0,16,1536)),
				Block(pg.Color("chocolate"), (1552,0,20,912)),
				Block(pg.Color("chocolate"), (16,752,1216,16)),
				]
		static = [
				Block(pg.Color("darkgreen"), (1024,576,32,176)),
				  Block(pg.Color("darkgreen"), (768,544,32,208)),
				  Block(pg.Color("darkgreen"), (928,480,32,224)),
				  Block(pg.Color("darkgreen"), (800,688,64,16)),
				  Block(pg.Color("darkgreen"), (832,624,64,16)),
				  Block(pg.Color("darkgreen"), (864,576,64,16)),
				  Block(pg.Color("darkgreen"), (496,304,16,480)),
				  Block(pg.Color("darkgreen"), (64,192,256,16)),
				  Block(pg.Color("darkgreen"), (448,208,112,16)),
				  Block(pg.Color("darkgreen"), (656,224,16,240)),
				  Block(pg.Color("darkgreen"), (944,208,16,256)),
				  Block(pg.Color("darkgreen"), (656,432,176,16)),
				  Block(pg.Color("darkgreen"), (864,464,272,16)),
				  Block(pg.Color("darkgreen"), (864,416,32,64)),
				  Block(pg.Color("darkgreen"), (864,416,32,64)),
				  Block(pg.Color("darkgreen"), (688,208,16,16)),
				  Block(pg.Color("darkgreen"), (816,208,16,16)),
				  Block(pg.Color("darkgreen"), (928,208,16,16)),
				  Block(pg.Color("darkgreen"), (1040,208,16,16)),
				  Block(pg.Color("darkgreen"), (1136,208,32,16)),
				  Block(pg.Color("darkgreen"), (1248,208,32,16)),
				  Block(pg.Color("darkgreen"), (1488,64,16,576)),
				  Block(pg.Color("darkgreen"), (1488,608,64,16)),
				]
		moving = [
				MovingBlock(pg.Color("olivedrab"), (1248,816,48,16), 1428, 0),
				  MovingBlock(pg.Color("olivedrab"), (1056,640,64,16), 1312, 0),
				  MovingBlock(pg.Color("olivedrab"), (640,544,32,16), 688, 1),
				  MovingBlock(pg.Color("olivedrab"), (544,256,32,16), 704, 1),
				  MovingBlock(pg.Color("olivedrab"), (32,224,32,16), 704, 1),
				  MovingBlock(pg.Color("olivedrab"), (1344,96,96,16), 1344, 0),
				  MovingBlock(pg.Color("olivedrab"), (1264,144,48,16), 1364, 0, speed=7),
				  MovingBlock(pg.Color("olivedrab"), (96,304,128,16), 352, 0, speed=3)
				]
		enemy = [
			Cube(pg.Color("red"), (160,880,32,32), 320, 0),
			Cube(pg.Color("red"), (480,880,32,32), 720, 0),
			Cube(pg.Color("red"), (1344, 64, 32, 32), 1408, 0),

# 			Cube(pg.Color("red"), (20,720,16,16), 225, 0),
# 			Cube(pg.Color("red"), (20,720,16,16), 325, 0)
					]

		return pg.sprite.Group(walls, static, moving, enemy)

	def update_viewport(self):
		"""
		The viewport will stay centered on the player unless the player
		approaches the edge of the map.
		"""
		self.viewport.center = self.player.rect.center
		self.viewport.clamp_ip(self.level_rect)

	def event_loop(self):
		"""We can always quit, and the player can sometimes jump."""
		for event in pg.event.get():
			if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
				self.done = True
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump(self.obstacles)
			elif event.type == pg.KEYUP:
				if event.key == pg.K_SPACE:
					self.player.jump_cut()

	def update(self):
		"""Update the player, obstacles, and current viewport."""
		self.keys = pg.key.get_pressed()
		self.player.pre_update(self.obstacles)
		self.obstacles.update(self.player, self.obstacles)
		self.player.update(self.obstacles, self.keys)
		self.update_viewport()

	def draw(self):
		"""
		Draw all necessary objects to the level surface, and then draw
		the viewport section of the level to the display surface.
		"""
		self.level.fill(pg.Color("lightblue"))
		self.level.blit(self.background.image, self.background.rect)
		self.obstacles.draw(self.level)
		self.level.blit(self.win_text, self.win_rect)
		self.player.draw(self.level)
		self.screen.blit(self.level, (0,0), self.viewport)

	def display_fps(self):
		"""Show the programs FPS in the window handle."""
		caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
		pg.display.set_caption(caption)

	def main_loop(self):
		"""As simple as it gets."""
		while not self.done:
			self.event_loop()
			self.update()
			self.draw()
			pg.display.update()
			self.clock.tick(self.fps)
			self.display_fps()
			if not self.player.alive:
				self.done = True
#		if self.player.alive:
			# add victory screen or high score
#        elif self.player.alive:
			# add code to print death message
			# add code to ask player if they'd like to play again
        
# -------------------------------------------
#        INTRO / DEATH SCREEN CODE
# -------------------------------------------
        
# 	def game_intro(self):
# 		intro = True
# 		while intro:
# 			for event in pg.event.get():
# 				#print(event)
# 				if event.type == pg.QUIT:
# 					pg.quit()
# 					quit()

# # Image to display, we can also put text over it with score / press _____ to start                    
                    
# 			self.display.blit(introImg,(0,0))
# 			if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
# 				quitgame
# 			pg.display.update()
# 			clock.tick(15)

if __name__ == "__main__":
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pg.init()
	pg.display.set_caption(CAPTION)
	pg.display.set_mode(SCREEN_SIZE)
	run_it = Control()
# 	run_it.game_intro()
	run_it.main_loop()
	pg.quit()
sys.exit()