#import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

import math
import random
import ninja
from ninja import *
import level
import os
import sys
import sounds
import menus
import options
import data_manager

if getattr(sys, 'frozen', False):
	Current_Path = sys._MEIPASS
else:
	Current_Path = str(os.path.dirname(__file__)) + str('/GameData/')



pygame.font.init()
font_12=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 12)
font_16=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 16)
font_20=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 20)
font_30=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 30)
font_80=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 80)
font_120=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 120)

BLACK = (0,0,0)
WHITE = (255,255,255)

sprite_sheet_location = 'spritesheet.png'

def set_default_ninjas():
	
	sprites.player1.color = options.GREEN_LIST
	sprites.player1.change_color(None, None, color_tuple = options.GREEN_LIST, change_bandana = False)
	sprites.player1.avatar = 'Mutant'
	sprites.player1.set_avatar('Mutant')
	sprites.player1.bandana_color = options.ORANGE_LIST
	sprites.player1.bandana.kill()
	sprites.player1.bandana = rope_physics.Bandana_Knot(sprites.player1, sprites.player1.bandana_color)

	sprites.player2.color = options.PURPLE_LIST
	sprites.player2.change_color(None, None, color_tuple = options.PURPLE_LIST, change_bandana = False)
	sprites.player2.avatar = 'Ninja'
	sprites.player2.set_avatar('Ninja')
	sprites.player2.bandana_color = options.RED_LIST
	sprites.player2.bandana.kill()
	sprites.player2.bandana = rope_physics.Bandana_Knot(sprites.player2, sprites.player2.bandana_color)

	sprites.player3.color = options.RED_LIST
	sprites.player3.change_color(None, None, color_tuple = options.RED_LIST, change_bandana = False)
	sprites.player3.avatar = 'Cyborg'
	sprites.player3.set_avatar('Cyborg')
	sprites.player3.bandana_color = options.BLUE_LIST
	sprites.player3.bandana.kill()
	sprites.player3.bandana = rope_physics.Bandana_Knot(sprites.player3, sprites.player3.bandana_color)

	sprites.player4.color = options.BLUE_LIST
	sprites.player4.change_color(None, None, color_tuple = options.BLUE_LIST, change_bandana = False)
	sprites.player4.avatar = 'Robot'
	sprites.player4.set_avatar('Robot')
	sprites.player4.bandana_color = options.PURPLE_LIST
	sprites.player4.bandana.kill()
	sprites.player4.bandana = rope_physics.Bandana_Knot(sprites.player4, sprites.player4.bandana_color)

class Replay_Handler():
	def __init__(self):
		self.counter = 0
		self.cap_counter = 0
		self.target = None

		#screen_objects.add(self)

		self.small_screen = pygame.Surface((320,180))

		self.target_ninja = None
		self.focal_x = 0
		self.focal_y = 0
		self.max_x_speed = 5
		self.max_y_speed = 9 
		self.dead_x = 48
		self.dead_y = 24

	def update(self):
		if self.cap_counter > 0:
			self.cap_counter -= 1
			self.capture()

		self.image = pygame.Surface((30,48))

	def capture(self, timer = 0, target = None, target_ninja = None):

		if target != None:
			self.target = target

		if target_ninja != None:
			self.target_ninja = target_ninja
			self.focal_x = self.target_ninja.rect.centerx
			self.focal_y = self.target_ninja.rect.centery
		#self.image.blit(screen, (0,0), area = (player1.rect.centerx - 15, player1.rect.top, 30, 48))
		#pygame.image.save(self.image,'test' + str(self.counter) + '.png')

		if self.target == 'full':
			pygame.image.save(screen,'test' + str(self.counter) + '.png')
		elif self.target == 'top left':
			self.small_screen.blit(screen, (0,0), area = (0, 0, 320, 180))
			pygame.image.save(self.small_screen,'test' + str(self.counter) + '.png')


		if self.target_ninja != None:
			#First adjust focus, x direction
			if abs(self.target_ninja.rect.centerx - self.focal_x) > self.dead_x:
				x_speed = round((abs(self.target_ninja.rect.centerx - self.focal_x) - self.dead_x) / 2)
				if x_speed > self.max_x_speed:
					x_speed = self.max_x_speed

				if self.target_ninja.rect.centerx > self.focal_x:
					self.focal_x += x_speed
					
				else:
					self.focal_x -= x_speed

			if self.focal_x + 160 > 640:
				self.focal_x = 640 - 160
			if self.focal_x - 160 < 0:
				self.focal_x = 160

			#second adjust focus, y direction
			if abs(self.target_ninja.rect.centery - self.focal_y) > self.dead_y:
					#if self.target_ninja.status != 'jump' or (abs(self.target_ninja.rect.centery - self.focal_y) > self.dead_y * 2):
					y_speed = round((abs(self.target_ninja.rect.centery - self.focal_y) - self.dead_y) / 2)
					if y_speed > self.max_y_speed:
						y_speed = self.max_y_speed

					if self.target_ninja.rect.centery > self.focal_y:
						self.focal_y += y_speed
						
					else:
						self.focal_y -= y_speed

			if self.focal_y + 90 > 360:
				self.focal_y = 360 - 90
			if self.focal_y - 90 < 0:
				self.focal_y = 90

			#third take screen
			self.small_screen.blit(screen, (0,0), area = (self.focal_x - 160, self.focal_y - 90, 320, 180))
			pygame.image.save(self.small_screen,'test' + str(self.counter) + '.png')




		


		self.counter += 1

		if timer > 0:
			self.cap_counter = timer - 1

replay_handler = Replay_Handler()




class Screenshot_Handler():
	def __init__(self):
		self.counter = 0
		self.cap_counter = 0
		self.target = None

		#screen_objects.add(self)

		self.small_screen = pygame.Surface((320,180))

		self.target_ninja = None
		self.focal_x = 0
		self.focal_y = 0
		self.max_x_speed = 5
		self.max_y_speed = 9 
		self.dead_x = 48
		self.dead_y = 24

	def update(self):
		if self.cap_counter > 0:
			self.cap_counter -= 1
			self.capture()

		self.image = pygame.Surface((30,48))

	def capture(self, timer = 0, target = None, target_ninja = None):

		if target != None:
			self.target = target

		if target_ninja != None:
			self.target_ninja = target_ninja
			self.focal_x = self.target_ninja.rect.centerx
			self.focal_y = self.target_ninja.rect.centery
		#self.image.blit(screen, (0,0), area = (player1.rect.centerx - 15, player1.rect.top, 30, 48))
		#pygame.image.save(self.image,'test' + str(self.counter) + '.png')

		if self.target == 'full':
			pygame.image.save(screen,'test' + str(self.counter) + '.png')
		elif self.target == 'top left':
			self.small_screen.blit(screen, (0,0), area = (0, 0, 320, 180))
			pygame.image.save(self.small_screen,'test' + str(self.counter) + '.png')


		if self.target_ninja != None:
			#First adjust focus, x direction
			if abs(self.target_ninja.rect.centerx - self.focal_x) > self.dead_x:
				x_speed = round((abs(self.target_ninja.rect.centerx - self.focal_x) - self.dead_x) / 2)
				if x_speed > self.max_x_speed:
					x_speed = self.max_x_speed

				if self.target_ninja.rect.centerx > self.focal_x:
					self.focal_x += x_speed
					
				else:
					self.focal_x -= x_speed

			if self.focal_x + 160 > 640:
				self.focal_x = 640 - 160
			if self.focal_x - 160 < 0:
				self.focal_x = 160

			#second adjust focus, y direction
			if abs(self.target_ninja.rect.centery - self.focal_y) > self.dead_y:
					#if self.target_ninja.status != 'jump' or (abs(self.target_ninja.rect.centery - self.focal_y) > self.dead_y * 2):
					y_speed = round((abs(self.target_ninja.rect.centery - self.focal_y) - self.dead_y) / 2)
					if y_speed > self.max_y_speed:
						y_speed = self.max_y_speed

					if self.target_ninja.rect.centery > self.focal_y:
						self.focal_y += y_speed
						
					else:
						self.focal_y -= y_speed

			if self.focal_y + 90 > 360:
				self.focal_y = 360 - 90
			if self.focal_y - 90 < 0:
				self.focal_y = 90

			#third take screen
			self.small_screen.blit(screen, (0,0), area = (self.focal_x - 160, self.focal_y - 90, 320, 180))
			pygame.image.save(self.small_screen,'test' + str(self.counter) + '.png')




		


		self.counter += 1

		if timer > 0:
			self.cap_counter = timer - 1

screenshot_handler = Screenshot_Handler()

class Shake_Handler():
	def __init__(self):
		self.current_shake = 0
		self.shake_x = 0
		self.shake_y = 0
		self.shake_growth = 1

		self.max_shake = 10 #in pixels!!! need to convert

	def update_shake(self):

		#if self.current_shake > self.max_shake:
		#	self.current_shake = self.max_shake

		#self.shake_x = self.max_shake * self.current_shake^2 * random.randrange(-20,20,1) / 20
		#self.shake_y = self.max_shake * self.current_shake^2 * random.randrange(-20,20,1) / 20

		self.shake_x = self.max_shake + 1
		self.shake_y = self.max_shake + 1
		while abs(self.shake_x) > self.max_shake or abs(self.shake_y) > self.max_shake:
			self.shake_x = self.current_shake**2 * random.randrange(-20,20,1) / 20
			self.shake_y = self.current_shake**2 * random.randrange(-20,20,1) / 20

			if self.current_shake > 0:
				self.current_shake -= 0.06
			else:
				self.current_shake = 0

		return((self.shake_x, self.shake_y))

shake_handler = Shake_Handler()

class Effects_Screen(pygame.sprite.DirtySprite):

	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.Surface((640,360))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

		self.timer = 0
		self.frame_counter = 0

		self.status = 'idle'
		self.shift_list = []

		self.base_image = None

		self.source = None

		active_sprite_list.add(self)
		#screen_objects.add(self)
		visual_effects.add(self)
		active_sprite_list.change_layer(self, 85)

		self.gravity_circle_list = []
		self.gravity_line_list = []
		i = 0
		while i < 40:
			line = Gravity_Line(self)
			self.gravity_line_list.append(line)
			i += 1
		self.gravity_line_1 = pygame.Surface((1,10))
		self.gravity_line_1.fill(options.WHITE)
		self.gravity_line_2 = pygame.Surface((1,12))
		self.gravity_line_2.fill(options.WHITE)
		self.gravity_line_3 = pygame.Surface((1,14))
		self.gravity_line_3.fill(options.WHITE)
		self.gravity_line_4 = pygame.Surface((1,16))
		self.gravity_line_4.fill(options.WHITE)
		self.gravity_line_5 = pygame.Surface((1,20))
		self.gravity_line_5.fill(options.WHITE)
		self.gravity_line_6 = pygame.Surface((1,24))
		self.gravity_line_6.fill(options.WHITE)
		self.gravity_line_7 = pygame.Surface((1,28))
		self.gravity_line_7.fill(options.WHITE)
		self.gravity_line_8 = pygame.Surface((1,32))
		self.gravity_line_8.fill(options.WHITE)
		self.gravity_line_9 = pygame.Surface((1,36))
		self.gravity_line_9.fill(options.WHITE)
		self.gravity_line_10 = pygame.Surface((1,40))
		self.gravity_line_10.fill(options.WHITE)


		self.dirty = 0
		self.visible = 0

	def update(self):
		if self.status == 'solar flare':
			self.timer += 1 #* options.DT
			if self.timer >= 6:
				self.visible = 0
				self.dirty = 1
				self.status = 'idle'
				

		elif self.status == 'gravity':
			if self.frame_counter == 0 and self.timer <= 80:
				particle_generator.gravity_circles(self.source.rect.center, self.gravity_circle_list)

			self.frame_counter += 1
			if self.frame_counter > 20:
				self.frame_counter = 0


			self.timer += 1
			if self.timer > 100:
				self.visible = 0
				self.dirty = 1
				self.status = 'idle'
				for line in self.gravity_line_list:
					line.reset()
				level.flip_gravity()

			for line in self.gravity_line_list:
					line.update()

			for circle in self.gravity_circle_list:
				circle.update()
				#if circle in circle.generator.idle_particles:
				#	self.gravity_circle_list.remove(self)

		if self.status == 'glitch screen':
			self.timer -= 1
			self.dirty = 1
			if self.timer > 25:
				self.image = sprites.screen.copy()
				menus.shift_glitch(self.image, 'left')
			elif self.timer > 20:
				self.image = sprites.screen.copy()
				menus.vertical_glitch(self.image)
			elif self.timer > 10:
				if self.timer in (11,12,15,16,19,20): 
					self.image.blit(menus.intro_handler.static_image1,(0,0))
				else:
					self.image.blit(menus.intro_handler.static_image2,(0,0))
				
				#if self.timer % 2 == 0: #even number
				#	self.image.blit(menus.intro_handler.static_image1,(0,0))
				#else:
				#	self.image.blit(menus.intro_handler.static_image2,(0,0))
			elif self.timer == 10:
				self.visible = 0
			else:
				self.visible = 1
				self.image = sprites.screen.copy()
				menus.shift_glitch(self.image, 'right') 


			if self.timer == 0:
				self.reset()

	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.status = 'idle'
		for line in self.gravity_line_list:
			line.reset()
	
	def solar_flare(self, source_ninja):
		self.visible = 1
		self.dirty = 1
		self.timer = 0
		self.image.fill(options.WHITE)
		self.status = 'solar flare'

		for ninja in ninja_list:
			if ninja != source_ninja:
				if ninja.color != source_ninja.color:
					ninja.confused = True
					ninja.confused_timer = 360
					if ninja.status == 'left':
						ninja.left_release()
					elif ninja.status == 'right':
						ninja.right_release()

	def gravity(self, source):
		self.visible = 1
		self.dirty = 1
		self.timer = 0
		self.frame_counter = 0
		self.image.fill(options.BLACK)
		#self.image.set_alpha(160)
		self.image.set_alpha(80)
		self.status = 'gravity'
		for line in self.gravity_line_list:
			line.activate()
		self.source = source
		self.gravity_circle_list = []

	def glitch_screen(self):
		self.timer = 30
		self.visible = 1
		self.status = 'glitch screen'


class Unlock_Sprite(pygame.sprite.DirtySprite):

	def __init__(self, unlock, unlock_type = 'avatar'):
		pygame.sprite.DirtySprite.__init__(self)

		self.unlock = unlock

		dark_color = (43,33,65)
		light_color = (38,37,41)

		self.image = pygame.Surface((400,50))
		self.rect = self.image.get_rect()
		self.image.fill(dark_color)
		self.image.set_colorkey(options.GREEN)

		self.image = menus.Build_Menu_Perimeter(self.image)

		self.rect.centerx = 320
		self.rect.y = 360

		self.change_y = -2

		self.frame_counter = 0

		active_sprite_list.add(self)
		screen_objects.add(self)
		active_sprite_list.change_layer(self, 1000) #Above EVERYTHING!

		self.text = ''

		
		if unlock_type == 'avatar':
			if self.unlock not in data_manager.data_handler.base_profile['Avatar']:
				data_manager.data_handler.base_profile['Avatar'].append(self.unlock)

			for key in data_manager.data_handler.user_profile_dict.keys():
				if self.unlock not in data_manager.data_handler.user_profile_dict[key]['Avatar']:
					data_manager.data_handler.user_profile_dict[key]['Avatar'].append(self.unlock)

			data_manager.data_handler.save_data()

			self.text = 'NEW UNLOCK: The Dummy Ninja!'

		elif unlock_type == 'color':
			#color already added before unlock_sprite call.
			self.text = 'NEW UNLOCK: The Purple Avatar Color!'
			data_manager.data_handler.save_data()

		text = font_16.render(self.text, 0, options.LIGHT_PURPLE)

		self.image.blit(text, ((self.rect.width / 2) - (text.get_width() / 2), (self.rect.height / 2) - (text.get_height() / 2)))




		self.visible = 1
		self.dirty = 1

	def update(self):
		if self.change_y != 0:
			self.dirty = 1
			self.rect.y += self.change_y
			if self.change_y < 0 and self.rect.bottom <= 350:
				self.change_y = 0
				self.rect.bottom = 350

			if self.change_y > 0 and self.rect.top > 360:
				self.reset()

		if self.change_y == 0:
			self.frame_counter += 1
			if self.frame_counter >= 60 * 5:
				self.change_y = 2

	def reset(self):
		self.kill()


class Gravity_Line(pygame.sprite.DirtySprite):

	def __init__(self, source):
		pygame.sprite.DirtySprite.__init__(self)

		#other images stored in screen effects - source
		self.source = source
		self.image = pygame.Surface((1,10))
		self.rect = self.image.get_rect()
		self.image.fill(options.WHITE)
		self.image.set_colorkey(options.GREEN)
		self.rect.x = 0
		self.rect.y = 0

		self.change_y = 10
		self.base_y_speed = 10
		self.frame_counter = random.randrange(0,5,1)
		self.inverted_g = False

		active_sprite_list.add(self)
		screen_objects.add(self)
		active_sprite_list.change_layer(self, 86) #One above effects screen

		self.top = 0
		self.bottom = 360

		self.visible = 0
		self.dirty = 1

		self.last_y_speed = 10

	def update(self):
		if self.visible == 1:
			self.dirty = 1
			self.rect.y += self.change_y
			self.frame_counter += 1

			if self.frame_counter >= 5:
				self.frame_counter = 0
				if self.inverted_g is False:
					if self.change_y > -10:
						self.change_y -= 1
				else:
					if self.change_y < 10:
						self.change_y += 1
				#update ninja flip!

				'''
				if self.change_y == 0:
					for ninja in player_list:
						ninja.update_image(ninja.status, ninja.direction)
						ninja.dirty = 1
						#ninja.bandana.new_position()
						ninja.bandana.update()
						ninja.bandana.headband.update()
						ninja.bandana.rope1.update()
						ninja.bandana.rope2.update()
						ninja.frame_counter -= 1
				'''

			if self.change_y > 0:
				if self.rect.top > self.bottom:
					self.rect.bottom = self.top
					self.update_image()
					self.update_x_position()
					if self.top > 0 and self.top < 360:
						self.rect.top = self.top
				
			elif self.change_y < 0:
				if self.rect.bottom < self.top:
					self.rect.top = self.bottom
					self.update_image()
					self.update_x_position()
					if self.bottom > 0 and self.bottom < 360:
						self.rect.bottom = self.bottom
				
			

		if self.last_y_speed != self.change_y:
			self.update_image()
		self.last_y_speed = self.change_y

		if self.rect.bottom > self.bottom:
			dist = self.rect.bottom - self.bottom
			pygame.draw.rect(self.image, options.GREEN, (0, self.rect.height - dist, 1, dist), 0)
		elif self.rect.top < self.top:
			dist = self.top - self.rect.top
			pygame.draw.rect(self.image, options.GREEN, (0, 0, 1, dist), 0)
			
	
	def update_x_position(self):
		if self.barrier != None:
			if self.barrier.orientation == 'rect':
				self.rect.centerx = random.randrange(self.barrier.rect.left, self.barrier.rect.right, 1)

	def update_image(self):
		centerx = self.rect.centerx
		centery = self.rect.centery

		if self.change_y in (10,-10):
			self.image = self.source.gravity_line_10.copy()
		elif self.change_y in (9,-9):
			self.image = self.source.gravity_line_9.copy()
		elif self.change_y in (8,-8):
			self.image = self.source.gravity_line_8.copy()
		elif self.change_y in (7,-7):
			self.image = self.source.gravity_line_7.copy()
		elif self.change_y in (6,-6):
			self.image = self.source.gravity_line_6.copy()
		elif self.change_y in (5,-5):
			self.image = self.source.gravity_line_5.copy()
		elif self.change_y in (4,-4):
			self.image = self.source.gravity_line_4.copy()
		elif self.change_y in (3,-3):
			self.image = self.source.gravity_line_3.copy()
		elif self.change_y in (2,-2):
			self.image = self.source.gravity_line_2.copy()
		else:
			self.image = self.source.gravity_line_1.copy()

		self.image.set_colorkey(options.GREEN)

		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery


	def activate(self):
		self.rect.centerx = random.randrange(0,640,1)
		self.rect.centery = random.randrange(0,360,1)
		self.visible = 1
		self.dirty = 1
		self.change_y = self.base_y_speed
		self.frame_counter = random.randrange(0,5,1)
		self.top = 0
		self.bottom = 360
		self.barrier = None
		if len(sprites.gravity_objects) > 0:
			for barrier in sprites.gravity_objects:
				inverted_g = barrier.return_gravity_point((self.rect.centerx, self.rect.centery))
				if inverted_g is True:
					self.change_y *= -1
					self.inverted_g = True
				else:
					self.inverted_g = False
				

				if barrier.orientation == 'horizontal':
					if self.rect.centery < barrier.rect.centery:
						self.top = 0
						self.bottom = barrier.rect.centery
					else:
						self.top = barrier.rect.centery
						self.bottom = 360
				elif barrier.orientation == 'rect':
					if self.rect.left >= barrier.rect.left and self.rect.right <= barrier.rect.right:
						if self.rect.centery < barrier.rect.top:
							self.top = 0
							self.bottom = barrier.rect.top
							self.barrier = barrier
						elif self.rect.centery > barrier.rect.bottom:
							self.bottom = 360
							self.top = barrier.rect.bottom
							self.barrier = barrier
						else:
							self.top = barrier.rect.top
							self.bottom = barrier.rect.bottom
							self.barrier = barrier
		else:
			self.inverted_g = options.inverted_g
			if self.inverted_g is True:
				self.change_y *= -1

		self.last_y_speed = self.change_y


	def reset(self):
		self.dirty = 1
		self.visible = 0
		self.change_y = self.base_y_speed
		self.frame_counter = 0

class Transition_Screen(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, countdown_timer):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)


		self.channel = None

		self.countdown_timer = countdown_timer

		self.image = pygame.Surface((640,360))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

		self.circle_timer = 0
		self.circle_mod = 0.75
		self.circle_switch_timer = 0
		self.circle_switch = False

		active_sprite_list.add(self)
		screen_objects.add(self)
		active_sprite_list.change_layer(self, 88) #One below pause screen for 'questions'

		self.dirty = 1
		self.visible = 0
		self.done = False
		self.status = 'idle'

		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)
		self.GREEN = (0,255,0)

		self.DARK_PURPLE = (143,75,236)
		self.WHITE_PURPLE = (242,237,255)
		self.PURPLE = (210,145,255)
		self.image.set_colorkey(self.GREEN)

		self.frame_counter = 0
		self.text_counter = 0 #counts frames for text display purposes.
		self.build_switch = False #False means it goes across screen without building the level... True will reveal the level.
		self.center = (self.rect.centerx, self.rect.centery)
		self.top_center = (self.rect.centerx, self.rect.centery + 2)
		self.bottom_center = (self.rect.centerx, self.rect.centery - 2)
		self.text = None
		self.old_screen = None #holds copy of old screen
		self.old_1 = None #holds part of old image as needed
		self.old_2 = None
		self.old_3 = None
		self.old_4 = None 
		self.fade_type = None #holds the type of fade that will be done
		self.intro_switch = False #true for intro. Scans player both ways.
		self.single_fade = False #true if just using single fade. False if want 'the whole packaged' ie. when loading levels.
		self.fade_color = (0,0,0) #Holds the color of the 'fade backdrop.' Use GREEN for transparent, to show layer below.

		self.loaded = False

		#self.fade_cheat_switch = False #used to force a particular image into the fade. When menu order doesn't cooperate.

		self.ad_list = ("ad_IWO.png",
						"ad_IWOCon.png",
						"ad_Ancalabro.png",
						"ad_Ancalabro.png",
						"ad_IGL.png",
						"ad_HOUR.png",
						"ad_DISCORD.png",
						"ad_SKULL.png",
						"ProTip_1.png",
						"ProTip_2.png",
						"ProTip_3.png",
						"ProTip_4.png",
						"ProTip_5.png",
						"ProTip_6.png",
						"ProTip_7.png",
						"ProTip_8.png",
						"ProTip_9.png",
						"ProTip_10.png",
						"ProTip_11.png",
						"ProTip_12.png",
						"ProTip_13.png",
						"ProTip_14.png",
						"ProTip_15.png"
						)

		#self.ad_list = ("ProTip_15.png",
		#				"ProTip_15.png"
		#				)

		self.ad = None
		self.ad_y = 0

	def update(self):
		if self.loaded is False: #one frame delay to help load things.
			self.loaded = True
			#options.DT = 0
		else:
			if self.status == 'idle':
				pass

			elif self.status == 'fade':
				#self.image.fill(self.fade_color)
				self.dirty = 1

				if self.fade_type == 'vertical_rects':
					if self.frame_counter < self.rect.height:
						pygame.draw.rect(self.image, self.BLACK, (0, 0, self.rect.width / 4, self.frame_counter), 0)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width / 4 * 2, 0, self.rect.width / 4, self.frame_counter), 0)

						pygame.draw.rect(self.image, self.BLACK, (self.rect.width / 4, self.rect.height - self.frame_counter, self.rect.width / 4, self.frame_counter), 0)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width / 4 * 3, self.rect.height - self.frame_counter, self.rect.width / 4, self.frame_counter), 0)
					else:
						self.image = menus.Build_CPU_Screen(self.image)
						for bar in menus.intro_handler.matrix_bar_list:
							bar.update()
							#bar.image.fill(options.GREEN)
							for digit in bar.digit_list:
								digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
								#bar.image.blit(digit.image,(0,digit.rect.y))
							#self.image.blit(bar.image, (bar.rect.x, bar.rect.y))
						#self.image =  menus.Build_Menu_Perimeter(self.image)

						pygame.draw.rect(self.image, self.BLACK, (0, 360 - (720 - self.frame_counter), self.rect.width / 4, 720 - self.frame_counter), 0)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width / 4 * 2,  360 - (720 - self.frame_counter), self.rect.width / 4, 720 - self.frame_counter), 0)

						pygame.draw.rect(self.image, self.BLACK, (self.rect.width / 4, 0, self.rect.width / 4, 720 - self.frame_counter), 0)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width / 4 * 3, 0, self.rect.width / 4, 720 - self.frame_counter), 0)


					self.frame_counter += 10 # * options.DT

					if self.frame_counter > self.rect.height * 2:
						self.status = 'load_text'
						self.frame_counter = 0
						self.text_counter = 0

				elif self.fade_type == 'horizontal_rects':
					if self.frame_counter < self.rect.width:
						self.image.blit(self.old_screen,(0,0))
						pygame.draw.rect(self.image, self.BLACK, (0, 0, self.frame_counter, self.rect.height / 4), 0)
						pygame.draw.rect(self.image, self.BLACK, (0, self.rect.height / 4 * 2, self.frame_counter, self.rect.height / 4), 0)

						pygame.draw.rect(self.image, self.BLACK, (self.rect.width - self.frame_counter, self.rect.height / 4, self.frame_counter, self.rect.height / 4), 0)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width - self.frame_counter, self.rect.height / 4 * 3,  self.frame_counter, self.rect.height / 4), 0)
					else:
						self.image = menus.Build_CPU_Screen(self.image)
						for bar in menus.intro_handler.matrix_bar_list:
							bar.update()
							#bar.image.fill(options.GREEN)
							for digit in bar.digit_list:
								digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
								#bar.image.blit(digit.image,(0,digit.rect.y))
							#self.image.blit(bar.image, (bar.rect.x, bar.rect.y))
						#self.image =  menus.Build_Menu_Perimeter(self.image)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width - (1280 - self.frame_counter), 0, 1280 - self.frame_counter, self.rect.height / 4), 0)
						pygame.draw.rect(self.image, self.BLACK, (self.rect.width - (1280 - self.frame_counter), self.rect.height / 4 * 2, 1280 - self.frame_counter, self.rect.height / 4), 0)

						pygame.draw.rect(self.image, self.BLACK, (0, self.rect.height / 4, 1280 - self.frame_counter, self.rect.height / 4), 0)
						pygame.draw.rect(self.image, self.BLACK, (0, self.rect.height / 4 * 3,  1280 - self.frame_counter, self.rect.height / 4), 0)
					


					self.frame_counter += 10 #* options.DT

					if self.frame_counter > (self.rect.width * 2):
						
						self.status = 'load_text'
						self.frame_counter = 0
						self.text_counter = 0

				elif self.fade_type == 'swipe_down':
					self.frame_counter += 1 #* options.DT # makes swipe faster
					self.image.fill(self.fade_color)

					if options.game_state == 'level':
						self.image = menus.Build_CPU_Screen(self.image)
						for bar in menus.intro_handler.matrix_bar_list:
							bar.update()
							#bar.image.fill(options.GREEN)
							for digit in bar.digit_list:
								digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
								#bar.image.blit(digit.image,(0,digit.rect.y))
							#self.image.blit(bar.image, (bar.rect.x, bar.rect.y))

						#self.image =  menus.Build_Menu_Perimeter(self.image)

					self.image.blit(self.old_screen,(0,self.frame_counter))


					self.frame_counter += 10 #* options.DT

					if self.frame_counter > self.rect.height:
						self.status = 'load_text'
						self.frame_counter = 0
						self.text_counter = 0

				elif self.fade_type == 'explode_fade':
					particle_generator.explode_fade()
					self.status = 'load_text'
					self.frame_counter = 0
					self.text_counter = 0


				''' TOO SLOW!!!
				elif self.fade_type == 'invisibility_fade':
					self.frame_counter += 1

					i = self.old_screen.copy()
					array = pygame.PixelArray(i)
					x = 0
					y = 0
					while y <= i.get_height() - 1:
						x = 0
						while x <= i.get_width() - 1:
							color = self.image.unmap_rgb(array[x,y])
							if color != (0,255,0):
								if self.frame_counter <= 3:
									visible = random.choice((True,False,False,False))
								elif self.frame_counter <= 6:
									visible = random.choice((True,True,False,False))
								else:
									visible = random.choice((True,True,True,False))
								
								if visible is False:
									array[x,y] = (0,255,0)
							x += 1
						y += 1
				self.image = i

				if self.frame_counter >= 10:
					self.status = 'load_text'
					self.frame_counter = 0
					self.text_counter = 0
				'''




				if self.status == 'load_text': #reset self if not meant to load level.
					if self.single_fade is True:
						self.reset()

			elif self.status == 'load_text':
				self.dirty = 1
				self.image = menus.Build_CPU_Screen(self.image)
				for bar in menus.intro_handler.matrix_bar_list:
					bar.update()
					#bar.image.fill(options.GREEN)
					if bar.rect.colliderect(self.rect):
						for digit in bar.digit_list:
							digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
							#bar.image.blit(digit.image,(0,digit.rect.y))
					#self.image.blit(bar.image, (bar.rect.x, bar.rect.y))
				#self.image =  menus.Build_Menu_Perimeter(self.image)
				
				i = self.get_text()
				build_text = font_20.render(i, 0,(WHITE))
				self.image.blit(build_text,((self.rect.width / 2) - (build_text.get_width() / 2),(self.rect.height / 2) - (build_text.get_height() / 2)))

				#versus_text = 'Match to ' + str(options.versus_VP_required) + ' Points'
				#text = font_16.render(versus_text, 0,(WHITE))
				#self.image.blit(text,((self.rect.width / 2) - (text.get_width() / 2),5))

				if options.game_state != 'intro':	
					if self.ad_y < 0:
						self.ad_y += 2
					self.image.blit(self.ad, (320 - int(self.ad.get_width() / 2), self.ad_y))


				if self.frame_counter < 60:
					percent = 0
				else:
					percent = int((self.frame_counter-60) / 60 * 100)
				if percent > 100:
					percent = 100

				percent_text = font_20.render(str(percent) + '%', 0, (WHITE))
				self.image.blit(percent_text,((self.rect.width / 2) - (percent_text.get_width() / 2),self.rect.height - 5 - percent_text.get_height()))


				self.frame_counter += 1 #* options.DT
				if self.frame_counter >= 180:
						self.activate()
						for tile in tile_list:
							if tile.type == 'platform' and tile.subtype == 'moving platform':
								tile.start = True

						for ninja in ninja_list:
							if ninja.rect.centerx < 320:
								ninja.direction = 'right'
							else:
								ninja.direction = 'left'



			elif self.status == 'active':
				self.dirty = 1
				self.image = menus.Build_CPU_Screen(self.image)

				for bar in menus.intro_handler.matrix_bar_list:
					bar.update()
					if bar.rect.colliderect(self.rect):
						for digit in bar.digit_list:
							digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.

				#self.image =  menus.Build_Menu_Perimeter(self.image)

				if options.game_state != 'intro':
					if self.ad_y < 0:
						self.ad_y += 1
					self.image.blit(self.ad, (320 - int(self.ad.get_width() / 2), self.ad_y))

				if self.circle_switch is False:

					pygame.draw.circle(self.image, options.DARK_PURPLE,(320,180),2 + round(self.circle_switch_timer))
					pygame.draw.circle(self.image, options.PURPLE,(320,180),0 + round(self.circle_switch_timer))

					self.circle_switch_timer += 3 #* options.DT
					if self.circle_switch_timer >= 6:
						self.circle_switch = True
						self.channel = sounds.mixer.scan.play(loops=-1)

				else:
					if self.build_switch is True and options.game_state == 'level':
						pygame.draw.rect(self.image, self.GREEN, (0, 0, self.frame_counter, self.rect.height), 0)

					
					#mod is used to make lines 'thicker' when close to middle of scan. Like it is scanning outwards.
					mod = round((1 - abs((self.frame_counter - 320) / 320)) * 10) * 1.5
					mod2 = round(mod / 4)
					if mod2 < 0:
						mod2 = 0

					self.circle_timer += self.circle_mod #* options.DT
					circle_timer = round(self.circle_timer)
					if circle_timer > 3:
						self.circle_mod *= -1
					elif circle_timer < 0:
						self.circle_mod *= -1
						cirlce_timer = 0

					if self.build_switch is False or (self.build_switch is True and self.frame_counter <= self.rect.width / 2) or self.intro_switch is True:
						pygame.draw.circle(self.image, options.DARK_PURPLE,(320,180),7 + circle_timer)
						pygame.draw.circle(self.image, options.PURPLE,(320,180),5 + circle_timer)
						

						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,self.rect.height + mod),(self.frame_counter,self.rect.height - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,0 + mod),(self.frame_counter,0 - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 8) + mod),(self.frame_counter,(self.rect.height / 9 * 8) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 7) + mod),(self.frame_counter,(self.rect.height / 9 * 7) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 6) + mod),(self.frame_counter,(self.rect.height / 9 * 6) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 5) + mod),(self.frame_counter,(self.rect.height / 9 * 5) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 4) + mod),(self.frame_counter,(self.rect.height / 9 * 4) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 3) + mod),(self.frame_counter,(self.rect.height / 9 * 3) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 2) + mod),(self.frame_counter,(self.rect.height / 9 * 2) - mod)], 0)
						pygame.draw.polygon(self.image, self.DARK_PURPLE, [self.center,(self.frame_counter,(self.rect.height / 9 * 1) + mod),(self.frame_counter,(self.rect.height / 9 * 1) - mod)], 0)



					pygame.draw.line(self.image, self.DARK_PURPLE, (self.frame_counter, 0), (self.frame_counter, self.rect.height), 15)
					pygame.draw.line(self.image, self.PURPLE, (self.frame_counter, 0), (self.frame_counter, self.rect.height), 10)

					if self.build_switch is False:
						self.frame_counter -= 12 #* options.DT
					else:
						self.frame_counter += 12 #* options.DT

					if self.frame_counter < 0:
						self.frame_counter = 0
						self.build_switch = True
					elif self.frame_counter > self.rect.width:
						self.channel.stop()
						self.countdown_timer.activate()
						self.reset()

	def activate(self):
		self.visible = 1
		self.dirty = 1
		self.frame_counter = 640
		#The following should not be needed.
		#self.image = menus.Build_CPU_Screen(self.image)
		#self.image =  menus.Build_Menu_Perimeter(self.image)
		self.status = 'active'
		self.build_switch = False

		#self.countdown_timer.reset()
		#self.countdown_timer.level_go = False
		#self.countdown_timer.done = False

	#def fade_image_cheat(self):
	#	self.image.blit(screen,(0,0))
	#	self.old_screen = self.image.copy()
	#	self.fade_cheat_switch = True

	def fade(self, fade_type, single_fade, fade_color, layer = 250, timer = False):
		active_sprite_list.change_layer(self, layer) #88 is one below pause screen for 'questions'. Otherwise 'on top!'

		self.visible = 1
		self.dirty = 1
		self.frame_counter = 0
		

		#if self.fade_cheat_switch is False:
		self.image.blit(screen,(0,0))
		self.old_screen = self.image.copy() #some fades need copy of old screen

		#self.fade_cheat_switch = False

			
		
		self.status = 'fade'
		if fade_type == None:
			self.fade_type = random.choice(('vertical_rects', 'horizontal_rects', 'swipe_down'))
			#self.fade_type = 'horizontal_rects'
		else:
			self.fade_type = fade_type
		#self.fade_type = 'vertical_rects'
		#self.fade_type = 'horizontal_rects'
		#self.fade_type = 'swipe_down'
		if timer is True:
			self.countdown_timer.reset()
			self.countdown_timer.level_go = False
			self.countdown_timer.done = False
		self.single_fade = single_fade #True if just using fade effects. False if wanting to load level.
		self.fade_color = fade_color #the color of the background while fading. Uses GREEN if you just want to see the layer behind.
		#Now reset position of all matrix bars. Allows them to 'start from top again'
		for bar in menus.intro_handler.matrix_bar_list:
			bar.reset()
	def reset(self):
		ad_name = random.choice(self.ad_list)
		self.ad = pygame.image.load(os.path.join(Current_Path, ad_name)).convert()
		self.ad.set_colorkey(options.GREEN)
		self.ad_y = -self.ad.get_height()

		self.loaded = False
		self.status = 'idle'
		self.dirty = 1
		self.visible = 0
		self.intro_switch = False
		self.single_fade = False
		self.fade_type = None
		self.fade_color = None
		self.circle_switch_timer = 0
		self.circle_switch = False

	def get_text(self):
		if self.frame_counter < 60:
			self.text = 'Preparing Combat Simulation.'

		elif self.frame_counter < 120:
			if self.text_counter == 0:

				text_list = ['Plotting World Domination.',
							'Inputing Custom Biometrics.',
							'Loading Level Weapons.',
							'Fine Tuning Level Hazards.',
							'Synthesizing Combat Music.',
							'Randomizing Simulation Content.',
							'Union Required Coffee Break.',
							'Deadly-ifying Simulation.',
							'Perfecting Mallow Physics.',
							'Relaying Combat Data.',
							'Predicting Combat Outcome.',
							'Pretending to Load Things.',
							'Waiting for 100%.',
							'Applying Gravity Settings.',
							'Applying Difficulty Algorithm.',
							'Selecting Starting Locations',
							'Connecting to Human Brainwaves.',
							'Selecting Level Tile Pattern.',
							'Searching for Nigel',
							'Searching for Llewelyn.',
							'Sending $15 to 52 Morgan Rd.',
							'Skipping Anti-Aliasing.',
							'Loading Texture Files.',
							'Resisting Anti-Aliasing.',
								]
								
				self.text = random.choice(text_list)
			self.text_counter += 1 #* options.DT
			if self.text_counter > 8:
				self.text_counter = 0

		else:
			self.text = 'VR Simulation Ready.'

		return(self.text)

class Menu_Arrow(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, centerxy, direction, ninja, menu=None):

		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'menu arrow'
		self.ninja = ninja

		self.direction = direction

		self.menu = menu #just used to store what menu each arrow belongs to

		self.image_list = []
		direct_dict = {'left' : (36,228), 'right' : (36,246), 'down': (36, 264) , 'up': (36,282) }
		image = sprites.level_sheet.getImage(direct_dict[direction][0], direct_dict[direction][1], 17, 17)
		image.set_colorkey(options.GREEN)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(direct_dict[direction][0] + 18, direct_dict[direction][1], 17, 17)
		image.set_colorkey(options.GREEN)
		self.image_list.append(image)
		
		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		self.rect.centerx = centerxy[0]
		self.rect.centery = centerxy[1]

		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 90) #Exist ABOVE menu text screen (10)

		self.active = False
		self.visible = 0
		self.frame_counter = 0
		self.image_number = 0
		self.dirty = 1

	def update(self):
		if self.active is True:
			self.frame_counter += 1
			if self.frame_counter >= 30:
				self.image_number += 1
				if self.image_number > len(self.image_list) - 1:
					self.image_number = 0
				self.image = self.image_list[self.image_number]
				self.frame_counter = 0
				self.dirty = 1

	def activate(self, centerxy = None):
		self.active = True
		self.visible = 1
		self.frame_counter = 0
		self.image_number = 0
		self.dirty = 1

		if centerxy != None:
			self.rect.centerx = centerxy[0]
			self.rect.centery = centerxy[1]
		

	def reset(self):
		self.active = False
		self.visible = 0
		self.frame_counter = 0
		self.dirty = 1

class Countdown_Timer(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, score_sprite):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.image_list = []

		self.score_sprite = score_sprite


		image = pygame.Surface((0,0))
		#image = menus.outline_text(image, options.WHITE, options.BLACK)
		self.image_list.append(image)
		image = font_120.render("3", 0,(options.LIGHT_PURPLE))
		image = menus.outline_text(image, options.LIGHT_PURPLE, options.DARK_PURPLE)
		self.image_list.append(image)
		image = font_120.render("2", 0,(options.LIGHT_PURPLE))
		image = menus.outline_text(image, options.LIGHT_PURPLE, options.DARK_PURPLE)
		self.image_list.append(image)
		image = font_120.render("1", 0,(options.LIGHT_PURPLE))
		image = menus.outline_text(image, options.LIGHT_PURPLE, options.DARK_PURPLE)
		self.image_list.append(image)
		image = font_120.render("GO", 0,(options.LIGHT_PURPLE))
		image = menus.outline_text(image, options.LIGHT_PURPLE, options.DARK_PURPLE)
		self.image_list.append(image)

		self.image_number = 0
		self.frame_counter = 0

		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		active_sprite_list.add(self)
		active_sprite_list.change_layer(self, 10)
		screen_objects.add(self)

		self.dirty = 1

		self.done = False
		self.level_go = False
		self.status = 'idle'

	def update(self):
		if self.status == 'active':
			if self.done is False:
					self.visible = 1
					self.frame_counter += 1 #* options.DT


					if self.frame_counter > 60:
						self.dirty = 1
						self.frame_counter = 0
						self.image_number += 1

						if self.image_number > len(self.image_list) - 1:
							self.image_number = 0
							self.visible = 0
							self.dirty = 1
						
						self.image = self.image_list[self.image_number]
						self.rect = self.image.get_rect()
						self.rect.centerx = size[0] / 2
						self.rect.centery = size[1] / 2

						#if self.image_number == 1:
						#	self.score_sprite.reset()

						if self.image_number == len(self.image_list) - 1:
							sounds.mixer.countdown_go.play()
							self.level_go = True
							self.done = True
							
							#Just reset for level ai codename_mallow
							#for bar in menus.intro_handler.matrix_bar_list:
							#	bar.reset()
							
							for ninja in player_list:
								ninja.name_bar.reset()
								ninja.score_bar.reset()
								ninja.stock_bar.reset()

						else:
							sounds.mixer.countdown_beep.stop()
							sounds.mixer.countdown_beep.play()

					self.rect.centerx = size[0] / 2
					self.rect.centery = size[1] / 2
				
			else:
				self.frame_counter += 1 #* options.DT
				if self.frame_counter >= 60:
					self.reset()
					if sounds.mixer.background_music != None:
						sounds.mixer.start_song() #start_level_song

	def online_switch(self, count):
		self.dirty = 1
		self.visible = 1
		self.image_number = count
		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()
		self.rect.centerx = size[0] / 2
		self.rect.centery = size[1] / 2
		if self.image_number == len(self.image_list) - 1:
			sounds.mixer.countdown_go.play()
			self.level_go = True
			self.done = True		
		
			for ninja in player_list:
				ninja.name_bar.reset()
				ninja.score_bar.reset()
				ninja.stock_bar.reset()

		else:
			sounds.mixer.countdown_beep.stop()
			sounds.mixer.countdown_beep.play()




	def reset(self):
		self.image_number = 0
		self.frame_counter = 0
		self.visible = 0
		self.dirty = 1
		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()
		self.rect.centerx = size[0] / 2
		self.rect.centery = size[1] / 2
		self.status = 'idle'
		#self.score_sprite.reset()

	def activate(self):
		self.done = False
		self.level_go = True
		self.status = 'active'
		self.dirty = 1
		#self.score_sprite.activate()

class Versus_Match_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self):

		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		screen_objects.add(self)
		active_sprite_list.add(self) #this group actually draws the sprites
		active_sprite_list.change_layer(self, 90)

		self.visible = 0
		self.dirty = 1

		self.update_text()

	def update(self):
		pass

	def update_text(self):
		title_text = 'Versus Match' 

		if options.versus_mode == 'Points':
			versus_text = '(First to ' + str(options.versus_VP_required) + ' Points)'
		else:
			versus_text = '(First to ' + str(options.versus_wins_required) + ' Wins)'

		

		top_text = sprites.font_30.render(title_text, 0,options.LIGHT_PURPLE)
		bottom_text = sprites.font_16.render(versus_text, 0, options.LIGHT_PURPLE)

		height =  top_text.get_height() + bottom_text.get_height() + 5

		self.image = pygame.Surface((top_text.get_width(),height))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)

		self.image.blit(top_text, (0,0))
		self.image.blit(bottom_text, ((top_text.get_width() / 2) - (bottom_text.get_width() / 2), height - bottom_text.get_height()))

		self.image = menus.outline_text(self.image, options.LIGHT_PURPLE, options.DARK_PURPLE)

		self.rect = self.image.get_rect()

		self.reset()


	def activate(self):
		self.visible = 1
		self.rect.top = 5
		self.rect.centerx = 320
		

	def reset(self):
		self.visible = 0
		self.dirty = 1

class Pause_Background(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self):

		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.Surface((640,360))
		self.image.fill(options.BLACK)
		self.image.set_alpha(160)
		#self.image.set_alpha(200)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

		screen_objects.add(self)
		active_sprite_list.add(self) #this group actually draws the sprites
		active_sprite_list.change_layer(self, 89)

		self.visible = 0
		self.dirty = 1


	def update(self):
		pass


	def activate(self):
		self.visible = 1
		self.dirty = 1
		

	def reset(self):
		self.visible = 0
		self.dirty = 1



class Background_Particle(pygame.sprite.DirtySprite):

	#Replaces Particle to allow it to 'reset' and not stop level from generating more particles.
	#Allows 'mallow bits' to build forever.

	def __init__(self, image, center,tile,color):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'background_particle'

		self.image = image.copy()
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.dirty = 1
		self.size = self.rect.width

		self.collision_type = None

		self.color = color

		self.true_x = self.rect.x
		self.true_y = self.rect.y


		active_sprite_list.add(self)
		active_sprite_list.change_layer(self, -4) #layer JUST in front of tile
		background_objects.add(self)

		tile.attached_list.add(self)

		if len(particle_generator.clone_list) > options.max_sticky_particles:
			particle_generator.ordered_clones[0].reset()

		'''	
		for particle in particle_generator.clone_list:
			if self.rect.colliderect(particle.rect):
				if self.size < particle.size:
					self.reset()
				else:
					particle.reset()
		'''
			

	def update(self):
		pass

	def reset(self):
		particle_generator.ordered_clones.remove(self)
		self.kill()

class Particle(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, generator):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.GREEN = (0,255,0)
		self.color = (255,255,255)
		self.image = pygame.Surface((1,1))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		self.true_x = 0
		self.true_y = 0
		self.dirty = 0

		self.source = None #follows center
		self.source_center = None

		self.generator = generator

		self.collisions = False
		self.collision_type = ''

		active_sprite_list.add(self)
		active_sprite_list.change_layer(self, 1)
		#screen_objects.add(self)
		visual_effects.add(self)


		self.image_number = 0
		self.frame_counter = 0


		self.splash = True
		self.change_x = 0
		self.change_y = 0
		self.start_position = 0
		self.direction = 0 #degrees, 360
		self.speed = 0
		self.speed_change = 0 #how fast it moves
		self.lifespan = 0 #how long until it dies
		self.gravity = 0
		self.inverted_g = False #not used often. Just when passing along gravity to additional particles
		self.max_g = 0
		#self.change_g = 0
		self.growth_factor = 0
		self.size = 1
		self.color_mod = (0,0,0)
		self.shape = 'rect'

		self.tile = None

		self.status = 'idle'
		self.lifespan_type = 'time'

		self.trail = False
		self.trail_type = None

		self.noise_timer = 0
		self.noise_angle = 0
		self.base_change_x = 0
		self.base_change_y = 0

		self.speed_mod = 1
		self.x_speed_mod = 1
		self.y_speed_mod = 1

		self.special = None
		self.special_number = 0
		self.dirty_switch = True

		self.type = None

		self.frozen = False

		self.update_counter = random.choice((0,1,2))

	def update(self):
		if self.status == 'active':

			#used to only update some things once every three frames.
			self.update_counter += 1
			if self.update_counter > 2:
				self.update_counter = 0

			if self.dirty_switch is True:
				self.dirty = 1
			else:
				if self.change_x != 0 or self.change_y != 0:
					self.dirty_switch = True

			self.update_color()
			self.grow()
			self.apply_gravity()
			self.modify_speed()

			self.follow_source()

			self.apply_trail()
			self.apply_noise()
			
			self.true_x += self.change_x# * options.DT
			self.true_y += self.change_y# * options.DT

			

			self.rect.centerx = round(self.true_x)
			self.rect.centery = round(self.true_y)

			
			#self.rect.centerx = round(self.start_position[0] + (self.frame_counter * self.change_x))
			#self.rect.centery = round(self.start_position[1] + (self.frame_counter * self.change_y))
			


			self.frame_counter += 1# * options.DT

			self.collision_check()

			self.boundary_check()

			self.apply_special() #applies special characteristics. Custom!

			self.check_lifespan()

	def apply_trail(self):
		if self.trail is True:
			if self.trail_type == 'volt':
				particle_generator.volt_trail_particle(self.source, (self.rect.centerx,self.rect.centery), sprites.active_sprite_list.get_layer_of_sprite(self))

			if self.trail_type == 'spawn_trail':
				choice = random.choice((2,3))
				if choice != 3:
					particle_generator.spawn_vertical_trail_particles(self)
	def apply_noise(self):
		if self.noise_angle != 0:
			self.noise_timer += 1
			if self.noise_timer > 1:
				#i = random.randrange(0,3,1)
				i = 1
				if i == 1:
						self.noise_timer = 0
						temp_angle = self.angle + random.randrange(int(self.noise_angle * (3/4)), self.noise_angle, 1) * random.choice((-1,1))
						self.change_x = abs(math.sin(math.radians(temp_angle)) * self.speed) * self.x_direction
						self.change_y = abs(math.cos(math.radians(temp_angle)) * self.speed) * self.y_direction
			i = random.randrange(0,40,1)
			if i == 13:
				dist = self.dist_check(self.rect.center, self.source.rect.center)
				if dist < 20:
					particle_generator.volt_main_particle(self.source, self)


	def boundary_check(self):
		if options.loop_physics is True:
			if self.change_x < 0:
				if self.rect.right < 0:
					self.rect.left = 640
					self.true_x = round(self.rect.centerx)

			elif self.change_x > 0:
				if self.rect.left > 640:
					self.rect.right = 0
					self.true_x = round(self.rect.centerx)

			if self.change_y < 0:
				if self.rect.bottom < 0:
					self.rect.top = 360
					self.true_y = round(self.rect.centery)

			elif self.change_y > 0:
				if self.rect.top > 360:
					self.rect.bottom = 0
					self.true_y = round(self.rect.centery)

	def normal_g(self):
		self.gravity = abs(self.gravity)
		self.max_g = abs(self.max_g)
		self.inverted_g = False

		if self.collision_type == 'debris':
			if self.gravity == 0:
				self.gravity = options.change_g
				self.rect.top = self.tile.rect.bottom + ((random.randrange(1,4) + (8 - (self.size * 2))))
				self.true_y = self.rect.y
				self.frame_counter = 0
				if self.tile != None:
					self.tile.attached_list.remove(self)
					self.tile = None
				self.lifespan = random.randrange(300,360,1)
				if self.lifespan_type == None:
					self.lifespan_type = random.choice(('time', None))

	def invert_g(self):
		self.gravity = abs(self.gravity) * -1
		self.max_g = abs(self.max_g) * -1
		self.inverted_g = True

		if self.collision_type == 'debris':
			if self.gravity == 0:
				self.gravity = options.change_g * -1
				self.rect.bottom = self.tile.rect.top - ((random.randrange(1,10) + (8 - (self.size * 2))))
				self.true_y = self.rect.y
				self.frame_counter = 0
				if self.tile != None:
					self.tile.attached_list.remove(self)
					self.tile = None
				self.lifespan = random.randrange(300,360,1)
				if self.lifespan_type == None:
					self.lifespan_type = random.choice(('time', None))

	def collision_check(self):
		if self.collisions is True:
			current_tile_list = quadrant_handler.get_quadrant(self)

			for item in active_items:
				if item.type == 'portal_gun_portal':
					if item.rect.colliderect(self.rect):
						if len(item.portal_gun.active_portal_list) < 2:
							self.reset()
						else:
							for active_portal in item.portal_gun.active_portal_list:
								if active_portal != item:
									other_portal = active_portal
									break
							temp_rect = pygame.Rect(item.collision_rect[0] - 3, item.collision_rect[1] - 3, item.collision_rect[2] + 6, item.collision_rect[3] + 6)
							if temp_rect.colliderect(self.rect):
								if (item.direction == 'up' and self.change_y >= 0) or (item.direction == 'down' and self.change_y <= 0) or (item.direction == 'left' and self.change_x >= 0) or (item.direction == 'right' and self.change_x <= 0):
									if other_portal.direction == 'up':
										self.rect.bottom = other_portal.rect.centery
										self.rect.centerx = other_portal.rect.centerx
										self.true_x = self.rect.x
										self.true_y = self.rect.y
										self.change_y = abs(self.change_y) * -1

									elif other_portal.direction == 'down':
										self.rect.top = other_portal.rect.centery
										self.rect.centerx = other_portal.rect.centerx
										self.true_x = self.rect.x
										self.true_y = self.rect.y
										self.change_y = abs(self.change_y)

									elif other_portal.direction == 'left':
										self.rect.right = other_portal.rect.centerx
										self.rect.centery = other_portal.rect.centery
										self.true_x = self.rect.x
										self.true_y = self.rect.y
										self.change_x = abs(self.change_x) * -1

									elif other_portal.direction == 'right':
										self.rect.left = other_portal.rect.centerx
										self.rect.centery = other_portal.rect.centery
										self.true_x = self.rect.x
										self.true_y = self.rect.y
										self.change_x = abs(self.change_x)

							else:
								if self.change_x == 0 and self.change_y == 0:
									self.reset()
								
			if self.collision_type == 'destroy':
				for tile in current_tile_list:
					if tile.type == 'tile':
						if tile.rect.colliderect(self.rect):
							self.reset()
					elif tile.type == 'platform':
						if self.type == 'rain':
							if tile.rect.colliderect(self.rect):
								self.reset()
			
			if (self.change_x != 0 or self.change_y != 0):
				if self.collision_type == 'stick': #tile_check, stick to tile
					for tile in current_tile_list:
						if tile.type == 'tile' or tile.type == 'mallow_wall':
							if self.rect.colliderect(tile.rect):
								test_point = (self.rect.centerx - round(self.change_x / 2), self.rect.centery - round(self.change_y / 2))
								if tile.rect.collidepoint(test_point):
									self.rect.center = test_point
								self.true_x = self.rect.x
								self.true_y = self.rect.y
								self.change_x = 0
								self.change_y = 0
								self.gravity = 0
								self.tile = tile
								self.tile.attached_list.add(self)
								active_sprite_list.change_layer(self, -4) #make it JUST above tile
								break
						elif tile.type == 'platform':
							if self.rect.colliderect(tile.rect):
								if self.inverted_g is False and self.change_y > 0:
									if self.rect.bottom - self.change_y <= tile.rect.top + 1:
										test_point = (self.rect.centerx - round(self.change_x / 2), self.rect.centery - round(self.change_y / 2))
										if tile.rect.collidepoint(test_point):
											self.rect.center = test_point
										self.true_x = self.rect.x
										self.true_y = self.rect.y

										self.change_x = 0
										self.change_y = 0
										self.gravity = 0
										#if self.rect.bottom > tile.rect.top  + 1:
										#	self.rect.bottom = tile.rect.top + 1
										self.tile = tile
										self.tile.attached_list.add(self)
										active_sprite_list.change_layer(self, -4) #make it JUST above tile
										break
								elif self.inverted_g is True and self.change_y < 0:
									if self.rect.top - self.change_y >= tile.rect.bottom - 1:
										test_point = (self.rect.centerx - round(self.change_x / 2), self.rect.centery - round(self.change_y / 2))
										if tile.rect.collidepoint(test_point):
											self.rect.center = test_point
										self.true_x = self.rect.x
										self.true_y = self.rect.y

										self.change_x = 0
										self.change_y = 0
										self.gravity = 0
										#if self.rect.top < tile.rect.bottom - 1:
										#	self.rect.top = tile.rect.bottom - 1
										self.tile = tile
										self.tile.attached_list.add(self)
										active_sprite_list.change_layer(self, -4) #make it JUST above tile
										break

						elif tile.type == 'mallow':
							if self.rect.colliderect(tile.rect):
								if self.splash is True:
									self.generator.debris_FID_particles(tile, self)
									self.reset()
									break
								else:
									self.reset()
									break
									
				if self.collision_type == 'debris': #tile_check, stick to tile
					temp_list = []
					last_tile = None
					for tile in current_tile_list:
								if tile.rect.colliderect(self.rect):
									if tile.type == 'platform' or tile.type == 'tile':
										temp_list.append(tile)

									elif tile.type == 'mallow_wall':
										if tile.rect.colliderect(self.rect):
											if self.change_x > 0:
												self.rect.right = tile.rect.left
												self.true_x = self.rect.x
											elif self.change_x < 0:
												self.rect.left = tile.rect.right
												self.true_x = self.rect.x
											self.change_x *= -1

									elif tile.type == 'mallow':
										if tile.rect.colliderect(self.rect):
											self.generator.debris_FID_particles(tile, self)
											self.reset()

					debris_tile_list = []
					for tile in temp_list:
						if tile.type == 'tile':
							debris_tile_list.append(tile)
					
					if len(debris_tile_list) > 0:
							collision = True #assume collision to start
							first_tile_list = [] #make a list that whille eventually hold that first tile(s) contacted
							i = 0
							frame_division = 9
							base_position = self.rect.center
							x_change = float(self.change_x / frame_division) #float(self.change_x * options.DT / frame_division)
							y_change = float(self.change_y / frame_division) #float(self.change_y * options.DT / frame_division)
							while collision is True and i < 15:
								i += 1
								self.rect.center = base_position
								self.rect.x -= round(x_change * i)
								self.rect.y -= round(y_change * i)

								temp_tile_list = [] #temp list that will be turned into first_tile_list
								for tile in debris_tile_list:
									if self.rect.colliderect(tile.rect):
										last_tile = tile
										collision = True
										temp_tile_list.append(tile)
								if len(temp_tile_list) > 0:
									first_tile_list = temp_tile_list
								else:
									collision = False

							#now fix for all tiles in first_tile_list.
							#fix in x direction first. bomb should currently be JUST before a collision.
							if self.change_x > 0:
								for tile in first_tile_list:
									temp_rect = pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
									if tile.rect.colliderect(temp_rect):
										last_tile = tile
										self.rect.right = tile.rect.left
										self.true_x = self.rect.x
										self.change_x *= -1
										break

							elif self.change_x < 0:
								for tile in first_tile_list:
									temp_rect = pygame.Rect(self.rect.left - 1,self.rect.y,1,self.rect.height)
									if tile.rect.colliderect(temp_rect):
										last_tile = tile
										self.rect.left = tile.rect.right
										self.true_x = self.rect.x
										self.change_x *= -1
										break

							#Now fix y_direction. bomb should currently be JUST before a collision.
							if self.change_y > 0:
								for tile in first_tile_list:
									temp_rect = pygame.Rect(self.rect.x - 1,self.rect.bottom,self.rect.width + 2,1)
									if tile.rect.colliderect(temp_rect):
										last_tile = tile
										self.rect.bottom = tile.rect.top
										self.true_y = self.rect.y
										if self.inverted_g is False:
											self.change_y *= -0.4
										else:
											self.change_y *= -0.4
										if self.size > 1 and self.lifespan_type == 'time':
											self.generator.debris_crumble_particles(self.rect.center, self.color, self.inverted_g, self.frozen)
											self.reset()
										break

							elif self.change_y < 0:
								for tile in first_tile_list:
									temp_rect = pygame.Rect(self.rect.x - 1,self.rect.top - 1,self.rect.width + 2,1)
									if tile.rect.colliderect(temp_rect):
										last_tile = tile
										self.rect.top = tile.rect.bottom
										self.true_y = self.rect.y
										if self.inverted_g is True:
											self.change_y *= -0.4
										else:
											self.change_y *= -0.4
										if self.size > 1 and self.lifespan_type == 'time':
											self.generator.debris_crumble_particles(self.rect.center, self.color, self.inverted_g, self.frozen)
											self.reset()
										break

							'''
							#Attempt to keep movement fluid by adding back on the postion 'cut off' but the collision code.
							base_position = self.rect.center
							collision = True
							#i is the same i as above.
							while i > 0 and collision is True:
								self.rect.center = base_position
								self.rect.x += round(self.change_x / frame_division * i * (1/3)) #the 2/3 modifier is just to reduce the amount of distance jump. Smooths out the aesthetics of not actually 'hitting the wall'. Balanced with 'maintaining most of the physics'.
								self.rect.y += round(self.change_y / frame_division * i * (1/3))
								collision = False
								for tile in tile_list:
									if tile.type == 'tile':
										if tile.rect.colliderect(self.rect):
											collision = True
											break
								i -= 1

							self.true_x = self.rect.x
							self.true_y = self.rect.y
							'''
					#now do platforms!
					for tile in temp_list:
						if tile.type == 'platform':
							if self.inverted_g is False and tile.top_open is True: #makes sure top isn't covered by another tile
								if self.rect.colliderect(tile.top_rect) and self.change_y > 0:
									last_tile = tile
									self.rect.bottom = tile.rect.top
									self.true_y = self.rect.y
									self.change_y *= -0.4
									if self.size > 1 and self.lifespan_type == 'time':
										self.generator.debris_crumble_particles(self.rect.center, self.color, self.inverted_g, self.frozen)
										self.reset()
									break
									#bounce = True
									
							elif self.inverted_g is True and tile.bottom_open is True: #makes sure bottom of tile -inverted top- is available.
								if self.rect.colliderect(tile.bottom_rect) and self.change_y < 0:
									last_tile = tile
									self.rect.top = tile.rect.bottom
									self.true_y = self.rect.y
									self.change_y *= -0.4
									if self.size > 1 and self.lifespan_type == 'time':
										self.generator.debris_crumble_particles(self.rect.center, self.color, self.inverted_g, self.frozen)
										self.reset()
									break

					#MAKE IT BIRTH COUNTER?? M
					if self.frame_counter > 30:
						#if abs(self.change_x) < 0.2:
						#	self.change_x = 0
						#else:
						#	self.change_x *= 0.99
						if abs(self.change_y) <= abs(self.gravity) * 3:
							if last_tile != None:
								#if self.change_x == 0 and abs(self.change_y) <= abs(self.gravity) * 3:
								#if last_tile != None:		
								self.gravity = 0
								self.change_x = 0
								self.change_y = 0
								self.tile = last_tile
								self.tile.attached_list.add(self)
								#active_sprite_list.change_layer(self, -4) #make it JUST above tile




			else: #stops particle from being updated in future
				self.dirty_switch = False

			if self.collision_type == 'debris': #tile_check, stick to tile	
				if self.change_x == 0 and self.change_y == 0:
					for ninja in sprites.ninja_list:
						if abs(ninja.change_x) + abs(ninja.change_y) > options.change_g:
							if ninja.rect.colliderect(self.rect):
								if self.inverted_g is False:
									self.change_x = 1 + (abs(self.change_x) * 0.15)
									self.change_y = -1 - (abs(self.change_y) * 2)
									self.gravity = options.change_g
								else:
									self.change_x = 1 + (abs(self.change_x) * 0.15)
									self.change_y = 1 + (abs(self.change_y) * 2)
									self.gravity = options.change_g * -1
								if ninja.change_x < 0:
									self.change_x *= -1
								self.change_x *= random.choice((1.1,1.2,1.3,1.4,1.5))
								self.change_y *= random.choice((1.1,1.2,1.3,1.4,1.5))
								#if abs(self.rect.centerx - ninja.rect.centerx) > 7:
								#	self.change_x *= 1
								if self.tile != None:
									self.tile.attached_list.remove(self)
									self.tile = None
								self.lifespan = random.randrange(300,360,1)
								if self.lifespan_type == None:
									self.lifespan_type = random.choice(('time', None))
								#active_sprite_list.change_layer(self, 1)
								self.dirty_switch = True

	def follow_source(self):
		if self.source != None:
			if self.source.rect.center != self.source_center:
				x = self.source.rect.centerx - self.source_center[0]
				y = self.source.rect.centery - self.source_center[1]
				self.true_x += x
				self.true_y += y
				self.rect.centerx = round(self.true_x)
				self.rect.centery = round(self.true_y)
				self.source_center = self.source.rect.center

	def apply_special(self):
		if self.update_counter == 0:
			if self.special == 'smoke_finish':
				if self.lifespan - self.frame_counter <= 20:
					self.color = (100,100,100)
					self.color_mod = (5,5,5)

			elif self.special == 'ash_finish':
				if self.frame_counter > 45:
					self.color = (100,100,100)
					self.image.fill(self.color)

			elif self.special == 'snow_finish':
				if self.frame_counter >= self.lifespan:
					self.generator.snow_particles(self.rect, self.inverted_g, self.special_number)

			elif self.special == 'volt_finish':

				if self.source.active is False:
					self.reset()
				else:
					dist = self.dist_check(self.rect.center, self.source.rect.center)
					if dist > 23:
						self.reset()

	def modify_speed(self):
		self.change_x *= self.speed_mod * self.x_speed_mod #math.pow(self.speed_mod, options.DT)
		self.change_y *= self.speed_mod * self.y_speed_mod #math.pow(self.speed_mod, options.DT)

	def update_color(self):
		if self.update_counter == 1:
			r = self.color[0] + self.color_mod[0] #(self.color_mod[0] * options.DT)
			g = self.color[1] + self.color_mod[1] #(self.color_mod[1] * options.DT)
			b = self.color[2] + self.color_mod[1] #(self.color_mod[2] * options.DT)

			if r > 255:
				r = 255
			elif r < 0:
				r = 0

			if g > 255:
				g = 255
			elif g < 0:
				g = 0

			if b > 255:
				b = 255
			elif b < 0:
				b = 0


			self.color = (r,g,b)

	def check_lifespan(self):
		if self.update_counter == 2:
			if self.lifespan_type == 'time':
				if self.frame_counter > self.lifespan:
					if self.type == 'mallow':
						if self.change_y != 0 or self.change_x != 0:
							self.reset()
						else:
							clone = Background_Particle(self.image,self.rect.center,self.tile, self.color)
							self.generator.clone_list.add(clone)
							self.generator.ordered_clones.append(clone)
							self.reset()
					
					elif self.type == 'debris':
						if self.size > 1:
							self.generator.debris_crumble_particles(self.rect.center, self.color, self.inverted_g, self.frozen)
							self.reset()
						else:
							self.reset()
					else:
						self.reset()

			elif self.lifespan_type == 'floor':
				if self.rect.top > self.start_position[1]:
					self.reset()

			elif self.lifespan_type == 'roof':
				if self.rect.bottom < self.start_position[1]:
					self.reset()

			elif self.lifespan_type == 'distance':
				if self.dist_check(self.start_position, (self.rect.center)) > self.lifespan:
					self.reset()

			elif self.lifespan_type == 'waterfall_top_particle':
				if self.frame_counter > self.lifespan:
					self.frame_counter = 0
					if self.waterfall.inverted is False:
						self.rect.bottom = self.loopy
					else:
						self.rect.top = self.loopy
					self.rect.centerx = random.randrange(self.loopx[0], self.loopx[1], 1)
					self.true_x = self.rect.centerx
					self.true_y = self.rect.centery

					self.lifespan = random.randrange(4,7,1)
					self.change_x = random.randrange(-10,10,1) * 0.01
					self.change_y = random.randrange(-10,-5,1) * 0.05
					if self.waterfall.inverted is True:
						self.change_y *= -1

			elif self.lifespan_type == 'volt_boundaries':
				
				if self.change_y < 0 and self.rect.top < self.source.rect.top + 2:
					self.reset()

				elif self.change_y > 0 and self.rect.bottom > self.source.rect.bottom - 2:
					self.reset()

				else: #check for distance boundaries based on 'lightning sprite diameter'
					dist = self.dist_check(self.rect.center, self.source.rect.center)
					i = 0
					if dist >= 22: #greater than radius of circle
						while dist >= 22:
							self.true_x -= self.change_x / 2
							self.true_y -= self.change_y / 2
							self.rect.centerx = round(self.true_x)
							self.rect.centery = round(self.true_y)
							dist = self.dist_check(self.rect.center, self.source.rect.center)
							i += 1
							if i == 4:
								break

						self.change_x *= -1
						self.base_change_x *= -1
						self.x_direction *= -1

						old_layer = sprites.active_sprite_list.get_layer_of_sprite(self)
						source_layer = sprites.active_sprite_list.get_layer_of_sprite(self.source)
						if old_layer < source_layer:
							new_layer = source_layer
						else:
							new_layer = source_layer - 2
						sprites.active_sprite_list.change_layer(self, new_layer)

					dist = self.dist_check(self.rect.center, self.source.rect.center)
					if dist >= 22:
						self.reset()

				if self.lifespan != None:
					self.lifespan -= 1
					if self.lifespan <= 0:
						self.reset()
			'''
			if self.base_change_x > 0:
				if self.rect.centerx > self.source.rect.right:
					self.rect.centerx = self.source.rect.right
					self.true_x = self.rect.centerx
					self.change_x *= -1
					self.base_change_x *= -1
					self.x_direction *= -1

					old_layer = sprites.active_sprite_list.get_layer_of_sprite(self)
					source_layer = sprites.active_sprite_list.get_layer_of_sprite(self.source)
					if old_layer < source_layer:
						new_layer = source_layer
					else:
						new_layer = source_layer - 2
					sprites.active_sprite_list.change_layer(self, new_layer)

			elif self.base_change_x < 0:
				if self.rect.centerx < self.source.rect.left:
					self.rect.centerx = self.source.rect.left
					self.true_x = self.rect.left
					self.change_x *= -1
					self.base_change_x *= -1
					self.x_direction *= -1

					old_layer = sprites.active_sprite_list.get_layer_of_sprite(self)
					source_layer = sprites.active_sprite_list.get_layer_of_sprite(self.source)
					if old_layer < source_layer:
						new_layer = source_layer 
					else:
						new_layer = source_layer - 2
					sprites.active_sprite_list.change_layer(self, new_layer)

			'''


	def apply_gravity(self):
		if self.gravity != 0:
			if self.max_g > 0:
				
				if self.change_y > self.max_g:
					self.change_y -= self.gravity #* options.DT
					if self.change_y < self.max_g:
						self.change_y = self.max_g
				else:
					self.change_y += self.gravity #* options.DT
					if self.change_y > self.max_g:
						self.change_y = self.max_g
			else:
				if self.change_y < self.max_g:
					self.change_y -= self.gravity #* options.DT
					if self.change_y > self.max_g:
						self.change_y = self.max_g
				else:
					self.change_y += self.gravity #* options.DT
					if self.change_y < self.max_g:
						self.change_y = self.max_g


				#self.change_y += self.gravity * options.DT
				#if self.change_y < self.max_g:
				#	self.change_y = self.max_g

	def grow(self):
		if self.growth_factor != 0:
			old_center = self.rect.center
			self.size += self.growth_factor #* options.DT
			if self.size < 1:
				self.size = 1
			if round(self.size) != self.rect.width:
				if self.shape == 'rect':
					self.image = pygame.Surface((self.size,self.size))
					self.image.fill(self.color)
					self.rect = self.image.get_rect()
				elif self.shape == 'circle':
					self.image = pygame.Surface((self.size,self.size))
					self.image.fill((0,255,0))
					self.rect = self.image.get_rect()
					pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2), int(self.rect.height / 2)), int(self.size / 2), 0)
					self.image.set_colorkey((0,255,0))
				elif self.shape == 'empty_circle':
					self.image = pygame.Surface((self.size,self.size))
					self.image.fill((0,255,0))
					self.rect = self.image.get_rect()
					pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2), int(self.rect.height / 2)), int(self.size / 2), 1)
					self.image.set_colorkey((0,255,0))
					
			self.rect.center = old_center

	def dist_check(self, point1, point2):
		distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
		return distance


	def reset(self):
		self.noise_timer = 0
		self.noise_angle = 0
		self.base_change_x = 0
		self.base_change_y = 0

		self.trail = False
		self.trail_type = None
		self.splash = True
		self.frozen = False
		self.source = None #follows center
		self.source_center = None
		self.dirty = 1
		self.visible = 0
		self.status = 'idle'
		self.change_x = 0
		self.change_y = 0
		self.size = 1
		self.start_position = 0
		self.direction = 0 #degrees, 360
		self.speed = 0
		self.speed_change = 0 #how fast it moves
		self.lifespan = 0 #how long until it dies
		self.gravity = 0
		self.max_g = 0
		self.inverted_g = False
		self.type = None
		#self.change_g = 0
		self.growth_factor = 0
		self.frame_counter = 0
		self.generator.idle_particles.append(self)
		self.lifespan_type = 'time'
		self.color = (255,255,255)
		self.color_mod = (0,0,0)
		self.shape = 'rect'

		if self.tile != None:
			self.tile.attached_list.remove(self)
		self.tile = None

		self.collisions = False
		self.collision_type = ''
		self.dirty_switch = True

		self.special = None

		self.speed_mod = 1 #1 means the x and y speed stay the same. Multiplies each frame.
		self.x_speed_mod = 1
		self.y_speed_mod = 1
		self.special_number = 0

		active_particle_list.remove(self)

class Particle_Generator():

	#place Ninja attributes here

	def __init__(self):
		
		i = 0
		self.particle_list = []
		self.idle_particles = []

		while i < 1000:
			particle = Particle(self)
			self.particle_list.append(particle)
			self.idle_particles.append(particle)
			i += 1

		#pre-loaded images:
		self.ice_diamond = level_sheet.getImage(433, 162, 10, 10)

		self.big_ice_shard_list = []
		self.big_ice_shard_1 = level_sheet.getImage(450, 162, 6, 6)
		self.big_ice_shard_list.append(self.big_ice_shard_1)
		self.big_ice_shard_2 = level_sheet.getImage(450, 169, 6, 6)
		self.big_ice_shard_list.append(self.big_ice_shard_2)
		self.big_ice_shard_3 = level_sheet.getImage(450, 176, 6, 6)
		self.big_ice_shard_list.append(self.big_ice_shard_3)
		self.big_ice_shard_4 = level_sheet.getImage(450, 183, 6, 6)
		self.big_ice_shard_list.append(self.big_ice_shard_4)

		self.small_ice_shard_list = []
		self.small_ice_shard_1 = level_sheet.getImage(444, 162, 5, 5)
		self.small_ice_shard_list.append(self.small_ice_shard_1)
		self.small_ice_shard_2 = level_sheet.getImage(444, 168, 5, 5)
		self.small_ice_shard_list.append(self.small_ice_shard_2)
		self.small_ice_shard_3 = level_sheet.getImage(444, 174, 5, 5)
		self.small_ice_shard_list.append(self.small_ice_shard_3)
		self.small_ice_shard_4 = level_sheet.getImage(444, 180, 5, 5)
		self.small_ice_shard_list.append(self.small_ice_shard_4)

		self.clone_list = pygame.sprite.LayeredDirty()
		self.ordered_clones = []

	def update(self):
		pass

	def reset(self):
		for sprite in self.clone_list:
			sprite.reset()
		self.clone_list = pygame.sprite.LayeredDirty()
		self.ordered_clones = []
		self.idle_particles = []
		for particle in self.particle_list:
			particle.reset() #adds itself back to idle_particles

	def slide_particles(self, startxy, direction, inverted_g):
		if len(self.idle_particles) != 0:
			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)

			particle.size = 2
			particle.image = pygame.Surface((particle.size,particle.size))
			particle.image.fill((255,255,255))
			particle.rect = particle.image.get_rect()			

			particle.start_position = startxy
			particle.rect.centerx = startxy[0]
			if inverted_g is False:
				particle.rect.centery = startxy[1] + random.randrange(-50,0,1) * 0.1
			else:
				particle.rect.centery = startxy[1] + random.randrange(0,50,1) * 0.1

			if direction == 'left':
				particle.change_x = -0.75
			elif direction == 'right':
				particle.change_x = 0.75

			if inverted_g is False:
				particle.change_y = random.randrange(-5,0,1) * 0.1
			else:
				particle.change_y = random.randrange(0,5,1) * 0.1

			

			particle.growth_factor = 0.1
			particle.lifespan = 20

			particle.status = 'active'
			particle.visible = 1
			particle.image.fill((255,255,255))

			particle.lifespan_type = 'time'

			active_sprite_list.change_layer(particle, 1)


			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery

	def land_particles(self, startxy, inverted_g):
		i = 0
		while i < 10:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 1
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()			

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				if inverted_g is False:
					particle.rect.centery = startxy[1]# + random.randrange(-50,0,1) * 0.1
				else:
					particle.rect.centery = startxy[1]# + random.randrange(0,50,1) * 0.1

				particle.change_x = random.choice((-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25))


				if inverted_g is False:
					particle.change_y = random.choice((-1.5,-1,-0.5,0)) * 0.1
				else:	
					particle.change_y = random.choice((0,0.5,1,1.5)) * 0.1

				

				particle.growth_factor = 0.15
				particle.lifespan = 20

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((255,255,255))

				particle.lifespan_type = 'time'

				active_sprite_list.change_layer(particle, 1)

				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def warning_spike_particles(self, startxy, inverted_g):
		i = 0
		while i < 10:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 2
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()			

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				if inverted_g is False:
					particle.rect.centery = startxy[1]# + random.randrange(-50,0,1) * 0.1
				else:
					particle.rect.centery = startxy[1]# + random.randrange(0,50,1) * 0.1

				particle.change_x = random.randrange(-20,20,1) / 120


				if inverted_g is False:
					particle.change_y = random.randrange(10,40,1) / 160
				else:	
					particle.change_y = random.randrange(-40,-10,1) / 160

				

				particle.growth_factor = 0.05
				particle.lifespan = 20

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((255,255,255))

				particle.lifespan_type = 'time'

				active_sprite_list.change_layer(particle, 1)

				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def spike_particles(self, startxy, inverted_g):
		i = 0
		while i < 10:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 2
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()			

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				if inverted_g is False:
					particle.rect.centery = startxy[1]# + random.randrange(-50,0,1) * 0.1
				else:
					particle.rect.centery = startxy[1]# + random.randrange(0,50,1) * 0.1

				particle.change_x = random.choice((-1.25,-1,-0.75,-0.5,-0.25,0.25,0.5,0.75,1,1.25))


				if inverted_g is False:
					particle.change_y = random.choice((-1.5,-1,-0.5,0)) * 0.2
				else:	
					particle.change_y = random.choice((0,0.5,1,1.5)) * 0.2

				

				particle.growth_factor = 0.05
				particle.lifespan = 15

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((255,255,255))

				particle.lifespan_type = 'time'

				active_sprite_list.change_layer(particle, 1)

				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	

	def debris_FID_particles(self, mallow, debris):
		i = 0
		#print(debris.size)
		while i < debris.size * 2:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.splash = False

				particle.type = 'mallow'

				particle.inverted_g = debris.inverted_g

				if debris.size == 1:
					particle.size = 1
				else:
					particle.size = random.choice((1,2))

				speed_mod = (5 + debris.size) / 8

				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = debris.rect.centerx
				if mallow.inverted is False:
					particle.rect.bottom = mallow.rect.top + 1
					particle.change_y = (random.randrange(-10,-7,1) * 0.5) * ((10 - particle.size) / 10) * speed_mod
				else:
					particle.rect.top = mallow.rect.bottom - 1
					particle.change_y = (random.randrange(8,11,1) * 0.5) * ((10 - particle.size) / 10) * speed_mod

				particle.start_position = (particle.rect.centerx,particle.rect.centery)

				particle.change_x = random.randrange(-4,5,1) * 0.5 * ((10 - particle.size) / 10) * speed_mod

				particle.collisions = True
				particle.collision_type = 'stick'

				if particle.inverted_g is False:
					particle.gravity = options.change_g
					particle.max_g = options.max_g
				else:
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.change_x *= abs(options.max_g)/abs(options.base_max_g)
				particle.change_y *= abs(options.max_g)/abs(options.base_max_g)

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				if particle.size > 1:
					particle.image.fill(random.choice((options.PURPLE, options.LIGHT_PURPLE)))
				else:
					particle.image.fill(options.LIGHT_PURPLE)

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def bomb_FID_particles(self, startxy, inverted_mallow, bomb, frozen, weapon_mod):
		i = 0
		while i < 15:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				#particle.inverted_g = inverted_g

				x_mod = weapon_mod * 1.5 * (random.choice((-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5)) + (random.randrange(-50,50,1) / 200))
				y_mod = weapon_mod * ((random.randrange(15,20,1) * 0.35) + (random.randrange(-50,50,1) / 200))
				particle.size = random.choice((1,1,1,1,2,2))

				particle.image = pygame.Surface((particle.size,particle.size))
				#particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = startxy[0] + x_mod
				if inverted_mallow is False:
					particle.rect.bottom = startxy[1] - 1
					particle.change_y = (-y_mod) * ((12 - (particle.size * 2)) / 12) #collision speed has a max or 1.
				else:
					particle.rect.top = startxy[1] + 1
					particle.change_y = y_mod * ((12 - (particle.size* 2)) / 12) #collision speed has a max or 1.
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.change_x = x_mod * 0.5 * (1 / particle.size)

				particle.collisions = True
				particle.collision_type = 'stick'

				particle.inverted_g = bomb.inverted_g
				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.gravity = options.change_g
					particle.max_g = options.max_g

				else:
					#particle.lifespan_type = 'roof'
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				
				particle.frozen = frozen
				if particle.frozen is True:
					particle.image.fill(options.ICE)
				else:
					if particle.size > 1:
						particle.image.fill(random.choice((options.PURPLE, options.LIGHT_PURPLE)))
					else:
						particle.image.fill(options.LIGHT_PURPLE)

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def single_dust_particles(self, startxy, color, ninja, inverted_g):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = None

				#particle.inverted_g = inverted_g
				particle.size = 1

				particle.image = pygame.Surface((particle.size,particle.size))
				#particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]
				if inverted_g is False:
					particle.change_y = 0
				else:
					particle.change_y = 0
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.change_x = random.randrange(10,20,1) * 0.025

				particle.collisions = True
				particle.collision_type = 'stick'

				particle.inverted_g = inverted_g
				particle.gravity = 0
				particle.max_g = 0
				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.change_y = random.randrange(-10,0,1) * 0.05
					#particle.gravity = -options.change_g / 3
					#particle.max_g = -options.max_g / 3

				else:
					#particle.lifespan_type = 'roof'
					particle.change_y = random.randrange(1,11,1) * 0.05
					#particle.gravity = options.change_g / 3
					#particle.max_g = options.max_g / 3

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(60,90,1)

				particle.growth_factor = 0
				particle.speed_mod = 0.98

				particle.status = 'active'
				particle.visible = 1
				particle.color = options.GREY_LIST[1]
				particle.image.fill(particle.color)

				active_sprite_list.change_layer(particle, 4)
				#active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def gravity_circles(self, startxy, particle_list):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = None

				#particle.inverted_g = inverted_g
				particle.growth_factor = 1.5

				particle.size = 20

				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill((options.GREEN))
				particle.image.set_colorkey(options.GREEN)
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]

				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.lifespan_type = 'time'
				particle.lifespan = 60


				particle.shape = 'empty_circle'
				particle.status = 'active'
				particle.visible = 1
				particle.color = options.BLACK
				pygame.draw.circle(particle.image, particle.color, (int(particle.rect.width / 2), int(particle.rect.height / 2)), int(particle.rect.width / 2), 1)

				active_sprite_list.change_layer(particle, 86)
				#active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

				particle_list.append(particle) #allows updates screen_effect_gravity_upate

	def torch_particles(self, source, style):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'fire'

				particle.rect.centery = random.randrange(source.rect.centery - 5,source.rect.centery,1)
				
				x_mod = random.randrange(-8,8,1)
				particle.rect.centerx = source.rect.centerx + x_mod
				y_mod = 10 - abs(x_mod)
				particle.rect.centery -= y_mod

				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.shape = 'circle'
				particle.inverted_g = False#source.inverted_g

				if style == 'temple':
					particle.color = random.choice((options.FIRE_RED, options.FIRE_ORANGE))
				elif style == 'dungeon':
					particle.color = random.choice(((89,145,109), (157,184,145)))
				particle.size = random.choice((1,1,1,1,1,1,1,1,1,2))

				particle.change_x = 0 #source.change_x / 2
				particle.change_y = -0.5


				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.center = particle.start_position
				particle.image.fill(particle.color)


				particle.lifespan_type = 'distance'
				particle.lifespan = random.randrange(10,15 + y_mod,1)

				if source.type == 'flame':
					particle.lifespan /= 5
					#particle.lifespan += (source.image_number * 3)
					particle.rect.centery += (3 - source.image_number) * 2
					particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1



				active_sprite_list.change_layer(particle, active_sprite_list.get_layer_of_sprite(source) + 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def fireball_finish_particles(self, source):
		i = 0
		while i < 10:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'fire'

				choice = random.choice(('left','right','top','bottom'))
				if choice == 'bottom':
					y = source.rect.bottom - random.choice((1,2,3))
					x = random.randrange(source.rect.left + 3, source.rect.right - 3,1)

				elif choice == 'top':
					y = source.rect.top + random.choice((1,2,3))
					x = random.randrange(source.rect.left + 3, source.rect.right - 3,1)

				elif choice == 'left':
					x = source.rect.left + random.choice((1,2,3))
					y = random.randrange(source.rect.top + 3, source.rect.bottom - 3,1)

				elif choice == 'right':
					x = source.rect.left + random.choice((1,2,3))
					y = random.randrange(source.rect.top + 3, source.rect.bottom - 3,1)




				particle.rect.centery = y
				particle.rect.centerx = x

				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.shape = 'circle'
				particle.inverted_g = False#source.inverted_g

				particle.color = random.choice((options.FIRE_RED, options.FIRE_ORANGE))
				particle.size = random.choice((1,1,1,1,1,1,1,1,1,2))

				particle.change_x = source.change_x * random.randrange(1,2,3) / 5
				particle.change_y = -0.5


				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.center = particle.start_position
				particle.image.fill(particle.color)


				particle.lifespan_type = 'distance'
				particle.lifespan = random.randrange(10,15,1)
				
				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1



				active_sprite_list.change_layer(particle, active_sprite_list.get_layer_of_sprite(source) + 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def fire_trap_triggered_particles(self, source):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'fire'

				y = random.randrange(source.rect.top + 5, source.rect.bottom - 5, 1)
				if source.direction == 'left':
					change_x = -0.2 + random.choice((-0.2,-0.15,-0.1,-0.05,0))
				elif source.direction == 'right':
					change_x = 0.2 + random.choice((0,0.05,0.1,0.15,0.2))

				particle.x_speed_mod = 0.95
				x = source.rect.centerx + random.choice((-1,0,1))

				particle.rect.centery = y
				particle.rect.centerx = x

				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.shape = 'circle'
				particle.inverted_g = False#source.inverted_g

				particle.color = random.choice((options.FIRE_RED, options.FIRE_ORANGE, options.FIRE_SMOKE, options.FIRE_SMOKE))
				particle.size = random.choice((1,1,1,1,1,1,1,1,1,2))

				particle.change_x = change_x
				particle.change_y = -0.25 #-0.5


				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.center = particle.start_position
				particle.image.fill(particle.color)


				particle.lifespan_type = 'distance'
				#particle.lifespan = random.randrange(10,15,1)
				particle.lifespan = random.randrange(10,15,1)
				
				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1



				active_sprite_list.change_layer(particle, active_sprite_list.get_layer_of_sprite(source) + 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def fire_slime_particles(self, source):
		i = random.choice((0,1))
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'fire'

				if source.inverted_g is False:
					y = random.randrange(source.rect.top + 1, source.rect.top + 12, 1)
					particle.change_y = -0.2
				else:
					y = random.randrange(source.rect.bottom - 7, source.rect.bottom - 3, 1)
					particle.change_y = 0.2
				

				particle.change_x = random.randrange(-10,10,1) * 0.02

				particle.x_speed_mod = 0.95
				x = random.randrange(source.rect.left+3,source.rect.right-3,1)
				
				particle.rect.centery = y
				particle.rect.centerx = x

				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.shape = 'circle'
				particle.inverted_g = False#source.inverted_g

				particle.color = random.choice((options.FIRE_RED, options.FIRE_ORANGE, options.FIRE_SMOKE, options.FIRE_SMOKE))
				particle.size = random.choice((1,1,1,1,1,1,1,1,1,2))


				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.center = particle.start_position
				particle.image.fill(particle.color)


				particle.lifespan_type = 'distance'
				#particle.lifespan = random.randrange(10,15,1)
				particle.lifespan = random.randrange(10,15,1)
				
				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1



				active_sprite_list.change_layer(particle, active_sprite_list.get_layer_of_sprite(source) + 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery


	def fire_burn_particles(self, source, base_number, x_speed):
		i = 0

		#if source.rect.height == 24:
		#	number = base_number / 2
		#else:
		#	number = base_number

		while i < base_number:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'fire'

				if source.rect.height == 48:
					if source.inverted_g is False:
						particle.rect.centery = random.randrange(source.rect.top + 24, source.rect.top + 24 + 20,1)
					else:
						particle.rect.centery = random.randrange(source.rect.bottom - 24 - 20,source.rect.bottom - 24,1)
				else:
					if source.inverted_g is False:
						particle.rect.centery = random.randrange(source.rect.top + 8, source.rect.top + 8 + 20,1)
					else:
						particle.rect.centery = random.randrange(source.rect.bottom - 8 - 20,source.rect.bottom - 8,1)


				particle.rect.centerx = random.randrange(source.rect.left,source.rect.right,1)
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.shape = 'circle'
				particle.inverted_g = source.inverted_g


				if source.inverted_g is False:
					if particle.rect.centery < source.rect.centery + 9:
						particle.size = random.choice((1,1,1,1,1,1,2))
						particle.color = options.FIRE_RED
					elif particle.rect.centery > source.rect.bottom - (source.rect.height / 3) + 5:
						particle.size = random.choice((2,2))
						if particle.rect.centerx <= source.rect.left + 2 or particle.rect.centerx >= source.rect.right - 2:
							particle.color = options.FIRE_RED
						elif particle.rect.centerx <= source.rect.left + 3 or particle.rect.centerx >= source.rect.right - 3:
							particle.color = options.FIRE_ORANGE
						else:
							particle.color = options.FIRE_YELLOW
					elif particle.rect.centery > source.rect.bottom - (source.rect.height / 3 * 2):
						particle.size = random.choice((1,1,2))
						particle.color = options.FIRE_ORANGE
					


					particle.change_x = x_speed / 3
					particle.x_speed_mod = 0.95
					particle.change_y = -1


				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.center = particle.start_position
				#if particle.size <= 2:
				particle.image.fill(particle.color)
				#else:
				#	particle.image.fill((options.GREEN))
				#	particle.image.set_colorkey((0,255,0))
				#	pygame.draw.circle(particle.image, particle.color, (round(particle.rect.width / 2), round(particle.rect.height / 2)), round(particle.size / 2), 0)



				particle.lifespan_type = 'distance'
				temp_i = source.rect.height / 3
				particle.lifespan = random.randrange(temp_i,temp_i + 20,1)

				y_mod = 12 - abs(particle.rect.centerx - source.rect.centerx)
				particle.lifespan += y_mod

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1



				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery


	def rain_particles(self, startxy, color):
		i = 0
		number = random.choice((1,2))
		while i < number:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'rain'

				#particle.inverted_g = inverted_g
				particle.size = 1

				particle.image = pygame.Surface((particle.size,particle.size))
				#particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]

				particle.inverted_g = False
				if particle.inverted_g is False:
					particle.change_y = random.randrange(5,7, 1) * -0.4
				else:
					particle.change_y = random.randrange(5,7, 1) * 0.4
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				x_mod = random.choice((-1,1))
				particle.change_x = x_mod * random.randrange(2,5,1) * 0.1

				particle.collisions = True
				particle.collision_type = 'destroy'

				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.gravity = options.change_g
					particle.max_g = options.max_g

				else:
					#particle.lifespan_type = 'roof'
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.lifespan_type = 'time'
				particle.lifespan = 360

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				particle.color = color
				particle.image.fill(color)


				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def single_mallow_particles(self, startxy, color, ninja, inverted_g, force_origin, changexy, size):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				#particle.inverted_g = inverted_g
				if size == None:
					particle.size = random.choice((1,1,1,1,2,2))
				else:
					particle.size = size

				particle.image = pygame.Surface((particle.size,particle.size))
				#particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]
				if inverted_g is False:
					particle.change_y = random.randrange(0,6, 1) * 0.1
				else:
					particle.change_y = random.randrange(-5,1, 1) * 0.1
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.change_x = x_mod * 0.5 * (1 / particle.size)

				particle.collisions = True
				particle.collision_type = 'stick'

				particle.inverted_g = inverted_g
				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.gravity = options.change_g
					particle.max_g = options.max_g

				else:
					#particle.lifespan_type = 'roof'
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				if color == None:
					if particle.size > 1:
						particle.image.fill(random.choice((options.PURPLE, options.LIGHT_PURPLE)))
					else:
						particle.image.fill(options.LIGHT_PURPLE)
				else:
					particle.color = color
					particle.image.fill(color)

				if force_origin != None:
					#speed = 3
					speed = random.randrange(20,40,1) / 10

					opp_side = particle.start_position[0] - force_origin[0] 
					adj_side = particle.start_position[1] - force_origin[1]
					try:
						angle = math.atan(opp_side / adj_side)
					except ZeroDivisionError:
						angle = math.atan(0)

					particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
					particle.change_y = math.cos(angle) * speed * random.choice((-1,1))
					particle.change_y *= 1.5

					#if particle.start_position[0] > force_origin[0]:
					#	particle.change_x = abs(particle.change_x) * -1
					#else:
					#	particle.change_x = abs(particle.change_x) * 1

					#particle.rect.centerx= force_origin[0]
					#particle.rect.centery= force_origin[1]

				if changexy != None:
					particle.change_x = changexy[0]
					particle.change_y = changexy[1]

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def FID_particles(self, startxy, inverted_mallow, ninja):
		i = 0
		while i < 15:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				#particle.inverted_g = inverted_g

				x_mod = random.choice((-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5)) + (random.randrange(-50,50,1) / 200)
				y_mod = (random.randrange(15,20,1) * 0.45) + (random.randrange(-50,50,1) / 200)
				particle.size = random.choice((1,1,1,1,2,2))

				particle.image = pygame.Surface((particle.size,particle.size))
				#particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()

				
				particle.rect.centerx = startxy[0] + x_mod
				if inverted_mallow is False:
					particle.rect.bottom = startxy[1] - 1
					particle.change_y = (-y_mod) * ((6 - particle.size) / 6) #collision speed has a max or 1.
				else:
					particle.rect.top = startxy[1] + 1
					particle.change_y = y_mod * ((6 - particle.size) / 6) #collision speed has a max or 1.
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.change_x = x_mod * 0.5 * (1 / particle.size)

				particle.collisions = True
				particle.collision_type = 'stick'

				particle.inverted_g = ninja.inverted_g
				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.gravity = options.change_g
					particle.max_g = options.max_g

				else:
					#particle.lifespan_type = 'roof'
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.change_x *= abs(ninja.change_y)/abs(options.base_max_g)
				particle.change_y *= abs(ninja.change_y)/abs(options.base_max_g)

				if inverted_mallow is True and ninja.inverted_g is False:
					particle.change_y /= 10
				elif inverted_mallow is False and ninja.inverted_g is True:
					particle.change_y /= 10

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				if particle.size > 1:
					particle.image.fill(random.choice((options.PURPLE, options.LIGHT_PURPLE)))
				else:
					particle.image.fill(options.LIGHT_PURPLE)

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def mine_death_particles(self, rect, inverted_g, ninja):
		i = 0
		while i < 30:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				particle.size = random.choice((1,1,1,1,2,2))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()

				particle.rect.centerx = random.randrange(rect.x + 4, rect.x + rect.width - 8,1)
				particle.rect.centery = random.randrange(rect.y + 4, rect.y + rect.height - 8,1)

				
				if inverted_g is False:
					particle.change_y = random.randrange(-10,-5,1) * 0.75 * ((4 - particle.size) / 4) #collision speed has a max or 1.
				else:
					particle.change_y = random.randrange(6,11,1) * 0.75 * ((4 - particle.size) / 4) #collision speed has a max or 1.

				particle.change_x = random.randrange(-5,6,1) * 0.25 * ((4 - particle.size) / 3)
				if particle.rect.centerx < ninja.rect.centerx:
					particle.change_x = abs(particle.change_x) * -1
				else:
					particle.change_x = abs(particle.change_x)

				particle.collisions = True
				particle.collision_type = 'stick'

				particle.inverted_g = ninja.inverted_g
				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.gravity = options.change_g
					particle.max_g = options.max_g

				else:
					#particle.lifespan_type = 'roof'
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				particle.color = random.choice((options.PURPLE, options.LIGHT_PURPLE, ninja.color[1]))
				particle.image.fill(particle.color)
				#if particle.size > 1:
				#	particle.image.fill(random.choice((options.PURPLE, options.LIGHT_PURPLE)))
				#else:
				#	particle.image.fill(options.LIGHT_PURPLE)

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def metal_suit_death_particles(self, rect, inverted_g, ninja):
		i = 0
		while i < 10:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				particle.size = random.choice((1,1,1,1,2,2))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()

				particle.rect.centerx = random.randrange(rect.x + 4, rect.x + rect.width - 8,1)
				if rect.height > 0:
					particle.rect.centery = random.randrange(rect.y, rect.y + rect.height,1)
				else:
					particle.rect.centery = rect.y

				
				if inverted_g is False:
					particle.change_y = random.randrange(-10,-5,1) * 0.75 * ((4 - particle.size) / 4) #collision speed has a max or 1.
				else:
					particle.change_y = random.randrange(6,11,1) * 0.75 * ((4 - particle.size) / 4) #collision speed has a max or 1.

				particle.change_x = random.randrange(-5,6,1) * 0.25 * ((4 - particle.size) / 3)
				if particle.rect.centerx < ninja.rect.centerx:
					particle.change_x = abs(particle.change_x) * -1
				else:
					particle.change_x = abs(particle.change_x)

				particle.collisions = True
				particle.collision_type = 'stick'

				particle.inverted_g = ninja.inverted_g
				if particle.inverted_g is False:
					#particle.lifespan_type = 'floor'
					particle.gravity = options.change_g
					particle.max_g = options.max_g

				else:
					#particle.lifespan_type = 'roof'
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.growth_factor = 0

				particle.status = 'active'
				particle.visible = 1
				particle.color = random.choice((options.PURPLE, options.LIGHT_PURPLE, ninja.color[1]))
				particle.image.fill(particle.color)
				#if particle.size > 1:
				#	particle.image.fill(random.choice((options.PURPLE, options.LIGHT_PURPLE)))
				#else:
				#	particle.image.fill(options.LIGHT_PURPLE)

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def color_knocked_particles(self, startxy, direction, inverted_g, delay, color_list, y_multiplier = 1, x_multiplier = 1):
		if delay == 0:
			number = 6
			big_particles = 2
		else:
			number = 2
			big_particles = 2
		i = 0
		
		#turn off based on settings
		if options.particles == 'Off':
			number = 0
			big_particles = 0
		elif options.particles == 'Low':
			number = int(number/2)
			big_particles = int(big_/2)

		while i < number:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				particle.inverted_g = inverted_g

				if direction == 'left':
					mod_x = -1
				else:
					mod_x = 1

				if i <= big_particles:
					particle.size = 2
					particle.change_x = (random.randrange(1,10,1) / 20) * mod_x * x_multiplier
					particle.change_y = random.randrange(3,5,1) * -0.5 * y_multiplier
				else:
					particle.size = 1
					particle.change_x = (random.randrange(1,10,1) / 10) * mod_x * x_multiplier
					particle.change_y = random.randrange(4,7,1) * -0.5 * y_multiplier

				particle.color = random.choice(color_list)


				if inverted_g is False:
					particle.change_y *= 1
				else:
					particle.change_y *= -1
				
				#particle.speed_mod = 0.9

				particle.collisions = True
				particle.collision_type = 'stick'

				#particle.color = random.choice(( (255,245,246),(210,145,255),(97,24,148) ))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill(particle.color)
				particle.rect = particle.image.get_rect()

				particle.start_position = startxy
				if abs(particle.change_x) >= 2.5:
					particle.rect.centerx = startxy[0]
				else:
					particle.rect.centerx = startxy[0] - int(particle.change_x * 2)
				particle.rect.centery = startxy[1]

				

				if inverted_g is False:
					particle.gravity = options.change_g
					particle.max_g = options.max_g
					#particle.change_y -= 0.25
				else:
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g
					#particle.change_y += 0.25

				particle.growth_factor = 0
				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def knocked_particles(self, startxy, direction, inverted_g, delay):
		if delay == 0:
			number = 8
			big_particles = 2
		else:
			number = 3
			big_particles = 1

		#turn off based on settings
		if options.particles == 'Off':
			number = 0
			big_particles = 0
		elif options.particles == 'Low':
			number = int(number/2)
			big_particles = int(big_particles/2)

		i = 0
		while i < number:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				particle.inverted_g = inverted_g

				if direction == 'left':
					mod_x = -1
				else:
					mod_x = 1

				if i <= big_particles:
					particle.size = 2
					particle.color = (210,145,255)
					particle.change_x = (random.randrange(1,10,1) / 20) * mod_x
					particle.change_y = random.randrange(3,5,1) * -0.5
				else:
					particle.size = 1
					particle.color = (255,245,246)
					particle.change_x = (random.randrange(1,10,1) / 10) * mod_x
					particle.change_y = random.randrange(4,7,1) * -0.5


				if inverted_g is False:
					particle.change_y *= 1
				else:
					particle.change_y *= -1
				
				#particle.speed_mod = 0.9

				particle.collisions = True
				particle.collision_type = 'stick'

				#particle.color = random.choice(( (255,245,246),(210,145,255),(97,24,148) ))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill(particle.color)
				particle.rect = particle.image.get_rect()

				particle.start_position = startxy
				if abs(particle.change_x) >= 2.5:
					particle.rect.centerx = startxy[0]
				else:
					particle.rect.centerx = startxy[0] - int(particle.change_x * 2)
				particle.rect.centery = startxy[1]

				

				if inverted_g is False:
					particle.gravity = options.change_g
					particle.max_g = options.max_g
					#particle.change_y -= 0.25
				else:
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g
					#particle.change_y += 0.25

				particle.growth_factor = 0
				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def cling_particles(self, startxy, direction, inverted_g):
		i = 0
		number = random.randrange(4,8,1)
		big_number = random.choice((1,2))
		
		#turn off based on settings
		if options.particles == 'Off':
			number = 0
			big_number = 0
		elif options.particles == 'Low':
			number = int(number/2)
			big_number = int(big_number/2)

		while i < number:
			i += 1
			if len(self.idle_particles) != 0:

				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				if direction == 'left':
					mod_x = -1
				else:
					mod_x = 1

				if i <= big_number:
					particle.size = 2
					particle.color = (210,145,255)
					particle.change_x = (random.randrange(1,10,1) / 20) * mod_x
					particle.change_y = random.randrange(2,4,1) * -0.5
				else:
					particle.size = 1
					particle.color = (255,245,246)
					particle.change_x = (random.randrange(1,10,1) / 10) * mod_x
					particle.change_y = random.randrange(3,6,1) * -0.5
				
				#particle.speed_mod = 0.9

				particle.collisions = True
				particle.collision_type = 'stick'

				#particle.color = random.choice(( (255,245,246),(210,145,255),(97,24,148) ))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill(particle.color)
				particle.rect = particle.image.get_rect()

				particle.start_position = startxy
				#if abs(particle.change_x) >= 2.5:
				#	particle.rect.centerx = startxy[0]
				#else:
				#	particle.rect.centerx = startxy[0] - int(particle.change_x * 2)
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]

				if particle.change_x > 0:
					particle.rect.x += particle.rect.width / 2
				else:
					particle.rect.x -= particle.rect.width / 2

				

				if inverted_g is False:
					particle.gravity = options.change_g
					particle.max_g = options.max_g
					particle.change_y *= 1
				else:
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g
					particle.change_y *= -1

				particle.growth_factor = 0
				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery


	def throw_item_particles(self, startxy, change_x, change_y, inverted_g, throw_type):
		i = 0
		while i < 6:
			i += 1
			if len(self.idle_particles) != 0:
				
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'mallow'

				particle.collisions = True
				particle.collision_type = 'stick'

				#x_mod = random.randrange(-5,5,1)
				#y_mod = random.randrange(10,15,1)
				if change_x < 0:
					mod_x = -1
				else:
					mod_x = 1
				if i <= 2:
					particle.size = 2
					particle.color = (210,145,255)
					particle.change_x = ((random.randrange(1,10,1) / 30) + (abs(change_x) / 2))* mod_x
					particle.change_y = random.randrange(3,5,1) * -0.5
				else:
					particle.size = 1
					particle.color = (255,245,246)
					particle.change_x = ((random.randrange(1,10,1) / 15) + (abs(change_x) / 2)) * mod_x
					particle.change_y = random.randrange(4,7,1) * -0.5


				#particle.speed_mod = 0.9

				#particle.color = random.choice(( (255,245,246),(210,145,255),(97,24,148) ))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill(particle.color)
				particle.rect = particle.image.get_rect()

				#particle.start_position = startxy
				#if abs(particle.change_x) >= 5:
				#	particle.rect.centerx = startxy[0]
				#else:
				#	particle.rect.centerx = startxy[0] - int(particle.change_x * 2)
				
				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]

				
				particle.inverted_g = inverted_g
				if inverted_g is False:
					particle.gravity = options.change_g
					particle.max_g = options.max_g
					if throw_type == 'bomb_down':
						particle.rect.centery += 12
					elif throw_type == 'mine_slow':
						particle.change_y -= 0.5
				else:
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g
					if throw_type == 'bomb_down':
						particle.rect.centery -= 12
					elif throw_type == 'mine_slow':
						particle.change_y += 0.5

				particle.growth_factor = 0
				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,360,1)

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 4)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def pole_death_particles(self, rect):
		
		i = 0
		while i < 40:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 2
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.centerx = random.randrange(rect[0], rect[0] + rect[2],1)
				particle.rect.centery = random.randrange(rect[1], rect[1] + rect[3],1)
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.lifespan_type = 'time'
				particle.lifespan = 20

				x_mod = particle.rect.centerx - (rect[0] + (rect[2] / 2))
				particle.change_x = x_mod / 18 / 2

				inverted_g = False
				if inverted_g is False:
					particle.change_y = random.choice((-0.5,-1,-1.5))
					particle.gravity = options.change_g
					particle.max_g = options.max_g
				else:
					particle.change_y = random.choice((0.5,1,1.5))
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g


				particle.color = (109,71,52)

				particle.image.fill(particle.color)



				particle.growth_factor = -0.05

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((particle.color))

				active_sprite_list.change_layer(particle, -5)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def explode_fade(self):
		
		i = 0
		while i < 150:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				if i < 75:
					particle.size = random.randrange(12,96,1)
					particle.image = pygame.Surface((particle.size, particle.size))
					particle.rect = particle.image.get_rect()
					particle.rect.centerx = random.randrange(100, 540,1)
					particle.rect.centery = random.randrange(50, 310,1)
					particle.start_position = (particle.rect.centerx, particle.rect.centery)
					particle.image.blit(transition_screen.old_screen, (0,0), area = particle.rect)

					
					choice = random.choice((1,2))
					#choice = 2
					if choice == 1:
						point_choices = [(0,0),(particle.rect.width,0),(particle.rect.width,particle.rect.height),(0,particle.rect.height)]
						point_list = []
						while len(point_list) < 3:
							temp_point = random.choice(point_choices)
							point_list.append(temp_point)
							point_choices.remove(temp_point)
							#print(temp_point)
						pygame.draw.polygon(particle.image, (0,255,0), point_list, 0)
						particle.image.set_colorkey(options.GREEN)
					elif choice == 2:
						point_choice = random.choice((1,2,))
						#point_choice = 2
						if point_choice == 1:
							triangle1 = [(0,int(particle.rect.height / 2)),(0,0),(particle.rect.width,0)] 
							triangle2 = [(0,int(particle.rect.height / 2)),(0,particle.rect.height),(particle.rect.width,particle.rect.height)]
						elif point_choice == 2:
							triangle1 = [(particle.rect.width,int(particle.rect.height / 2)),(0,0),(particle.rect.width,0)] 
							triangle2 = [(particle.rect.width,int(particle.rect.height / 2)),(0,particle.rect.height),(particle.rect.width,particle.rect.height)]
						pygame.draw.polygon(particle.image, (0,255,0), triangle1, 0)
						pygame.draw.polygon(particle.image, (0,255,0), triangle2, 0)
						particle.image.set_colorkey(options.GREEN)


					
					particle.shape = 'square'

				else:
					particle.color = random.choice(((38,37,41),(48,29,69),options.DARK_PURPLE))

					particle.size = random.choice((2,3,4,5,6,7,8,9,10))
					particle.image = pygame.Surface((particle.size,particle.size))
					#particle.image.fill((0,255,0))
					particle.rect = particle.image.get_rect()
					particle.image.fill(particle.color)
					#pygame.draw.circle(particle.image, particle.color, (round(particle.rect.width / 2), round(particle.rect.height / 2)), round(particle.size / 2), 0)
					particle.image.set_colorkey((0,255,0))
					particle.rect.centerx = random.randrange(0, 640,1)
					particle.rect.centery = random.randrange(0, 360,1)
					particle.start_position = (particle.rect.centerx, particle.rect.centery)
					particle.shape = 'square'
				

				particle.lifespan_type = 'distance'
				particle.lifespan = 360

				x_mod = particle.rect.centerx - 320
				particle.change_x = x_mod / 18 / 2

				particle.change_y = random.choice((-3.5,-4,-4.5))
				particle.gravity = 0.7
				particle.max_g = 8



				#particle.growth_factor = -0.1

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 5)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def debris_crumble_particles(self, center, color, inverted_g, frozen):
		i = 0
		while i < 3:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'debris'
				particle.size = 1
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.centerx = center[0] #+= random.choice((-1,,1))
				particle.rect.centery = center[1] #+= random.choice((-1,0,1))
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(300,600,1)

				particle.collisions = True
				particle.collision_type = 'debris'

				particle.change_x = random.randrange(-3,4,1) * 0.5

				particle.inverted_g = inverted_g
				if inverted_g is False:
					particle.change_y = random.randrange(-5,-2,1) * 0.5
					particle.gravity = options.change_g
					particle.max_g = options.max_g
				else:
					particle.change_y = random.randrange(2,6,1) * 0.5
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g


				#choose proper colors
				particle.color = color



				#particle.growth_factor = -0.05

				particle.status = 'active'
				particle.visible = 1

				particle.frozen = frozen
				if particle.frozen is True:
					particle.image.fill(options.ICE)
				else:
					particle.image.fill((particle.color))

				active_sprite_list.change_layer(particle, -5)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def enemy_death_particle(self, inverted_g, color, center, rect, particle_type):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)


				particle.size = random.choice((1,1,1,2))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.centerx = center[0]
				particle.rect.centery = center[1]
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.lifepan_type = random.choice(('time', 'time', None))
				#particle.lifespan_type = 'time'
				if particle.size == 1:
					particle.lifespan_type = 'time'
				else:
					particle.lifespan_type = random.choice(('time','time', None))
				
				particle.lifespan = random.randrange(300,360,1)

				particle.collisions = True
				if particle_type == 'debris':
					particle.type = 'debris'
					particle.collision_type = 'debris'
				elif particle_type == 'stick':
					particle.collision_type = 'stick'
					particle.type = 'mallow'


				x_mod = particle.rect.centerx - (rect[0] + (rect[2] / 2))
				particle.change_x = x_mod / 12

				particle.inverted_g = inverted_g
				if inverted_g is False:
					particle.change_y = random.randrange(-10,-4,1) * 0.5
					particle.gravity = options.change_g
					particle.max_g = options.max_g
				else:
					particle.change_y = random.randrange(4,10,1) * 0.5
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g


				particle.change_x *= abs(options.max_g)/abs(options.base_max_g)
				particle.change_y *= abs(options.max_g)/abs(options.base_max_g)

				if particle.type == 'mallow':
					particle.change_x *= 2
					particle.change_y *= 1.2


				#choose proper colors
				particle.color = color



				#particle.growth_factor = -0.05

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((particle.color))

				active_sprite_list.change_layer(particle, 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def single_debris_particle(self, inverted_g, color, center, rect, y_speed = 'explode'):
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'debris'
				particle.size = random.choice((1,2))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.centerx = center[0]
				particle.rect.centery = center[1]
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.lifepan_type = random.choice(('time', 'time', None))
				#particle.lifespan_type = 'time'
				if particle.size == 1:
					particle.lifespan_type = 'time'
				else:
					particle.lifespan_type = random.choice(('time','time', None))
				
				particle.lifespan = random.randrange(300,360,1)

				particle.collisions = True
				particle.collision_type = 'debris'

				if rect != None:
					x_mod = particle.rect.centerx - (rect[0] + (rect[2] / 2))
					particle.change_x = x_mod / 12
				else:
					particle.change_x = random.randrange(-20,20,1) / 20

				particle.inverted_g = inverted_g
				if inverted_g is False:
					particle.change_y = random.randrange(-10,-4,1) * 0.5
					particle.gravity = options.change_g
					particle.max_g = options.max_g
				else:
					particle.change_y = random.randrange(4,10,1) * 0.5
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g

				if y_speed == 0:
					particle.change_y = 0



				particle.change_x *= abs(options.max_g)/abs(options.base_max_g)
				particle.change_y *= abs(options.max_g)/abs(options.base_max_g)


				#choose proper colors
				particle.color = color



				#particle.growth_factor = -0.05

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((particle.color))

				active_sprite_list.change_layer(particle, 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def tile_death_particles(self, rect, tile_style, inverted_g, delay):
		if rect.width <= 5:
			number = 3
		elif delay == 0:
			number = 15
		elif delay == 'exploding tile':
			number = random.choice((3,4,5))
		else:
			number = 3

		i = 0
		while i < number:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.type = 'debris'
				particle.size = random.choice((1,2,3))
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.rect = particle.image.get_rect()
				particle.rect.centerx = random.randrange(rect[0], rect[0] + rect[2],1)
				particle.rect.centery = random.randrange(rect[1], rect[1] + rect[3],1)
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				#particle.lifepan_type = random.choice(('time', 'time', None))
				#particle.lifespan_type = 'time'
				if particle.size == 1:
					particle.lifespan_type = 'time'
				else:
					particle.lifespan_type = random.choice(('time','time', None))
				
				particle.lifespan = random.randrange(300,360,1)

				particle.collisions = True
				particle.collision_type = 'debris'

				x_mod = particle.rect.centerx - (rect[0] + (rect[2] / 2))
				particle.change_x = x_mod / 12

				particle.inverted_g = inverted_g
				if inverted_g is False:
					particle.change_y = random.randrange(-10,-4,1) * 0.5
					particle.gravity = options.change_g
					particle.max_g = options.max_g
				else:
					particle.change_y = random.randrange(4,10,1) * 0.5
					particle.gravity = -options.change_g
					particle.max_g = -options.max_g


				particle.change_x *= abs(options.max_g)/abs(options.base_max_g)
				particle.change_y *= abs(options.max_g)/abs(options.base_max_g)


				#choose proper colors
				if tile_style == 'ice':
					particle.color = (150,218,255)
				elif tile_style == 'space':
					particle.color = (163,146,212)
				elif tile_style == 'exploding tile':
					particle.color = (175,37,50)
				elif tile_style == 'dungeon':
					#particle.color = (167,186,0)
					particle.color = (67,86,85)
				elif tile_style == 'stone':
					particle.color = (97,84,118)
				elif tile_style == 'mystic':
					particle.color = (97,24,148)
				elif tile_style == 'temple':
					particle.color = (109,71,52)
				elif tile_style == 'burnt':
					particle.color = random.choice(((96,71,38),(66,45,24)))
				elif tile_style == 'classic':
					particle.color = (125,92,220)
				else: #classic
					particle.color = (74,70,82)



				#particle.growth_factor = -0.05

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((particle.color))

				active_sprite_list.change_layer(particle, 1)
				active_particle_list.add(particle)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def metal_pound_land_particles(self, startxy, inverted_g):
		i = 0
		while i < 50:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 1
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.image.fill((255,255,255))
				particle.rect = particle.image.get_rect()			

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				if inverted_g is False:
					particle.rect.centery = startxy[1]# + random.randrange(-50,0,1) * 0.1
				else:
					particle.rect.centery = startxy[1]# + random.randrange(0,50,1) * 0.1

				particle.change_x = random.randrange(-20,20,1) * 0.2
				particle.speed_mod = 0.9


				if inverted_g is False:
					particle.change_y = random.randrange(-20,0,1) * 0.05
				else:	
					particle.change_y = random.randrange(0,20,1) * 0.05

				

				particle.growth_factor = 0.15
				particle.lifespan = random.randrange(10,20,1) + abs(particle.change_x * 5) 

				particle.status = 'active'
				particle.visible = 1
				particle.image.fill((255,255,255))

				particle.lifespan_type = 'time'

				active_sprite_list.change_layer(particle, 1)

				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def metal_pound_particles(self, startxy, inverted_g):
		i = 0
		while i < 2:
			i += 1
			if len(self.idle_particles) != 0:
				#straight_speed = 3
				#angle_speed = math.sin(45) * self.straight_speed

				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.shape = 'circle'
				particle.size = 5
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = (170,170,170)
				particle.color_mod = (1,1,1)
				particle.image.fill(particle.color)
				particle.rect = particle.image.get_rect()			

				particle.start_position = startxy
				particle.rect.centerx = startxy[0] + random.randrange(-3,3,1)
				particle.rect.centery = startxy[1]
				

				particle.change_x = random.randrange(-3,3,1) * 0.04
				particle.change_y = random.randrange(1,5,1) * 0.04
				if inverted_g is False:
					particle.change_y *= -1

				

				particle.growth_factor = 0.025
				

				particle.status = 'active'
				particle.visible = 1

				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(40,80,1)

				active_sprite_list.change_layer(particle, 1)

				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery
		
	def rocket_particles(self, startxy, direction):
		if len(self.idle_particles) != 0:
			#straight_speed = 3
			#angle_speed = math.sin(45) * self.straight_speed

			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)

			particle.shape = 'circle'
			particle.size = 5
			particle.image = pygame.Surface((particle.size,particle.size))
			particle.image.fill((options.GREEN))
			particle.image.set_colorkey((0,255,0))
			particle.color = (170,170,170)
			particle.color_mod = (1,1,1)
			particle.rect = particle.image.get_rect()
			pygame.draw.circle(particle.image, particle.color, (round(particle.rect.width / 2), round(particle.rect.height / 2)), round(particle.size / 2), 0)


			particle.start_position = startxy
			particle.rect.centerx = startxy[0]
			particle.rect.centery = startxy[1]
			

			particle.change_x = random.randrange(-5,5,1) * 0.04
			particle.change_y = random.randrange(-5,5,1) * 0.04

			

			particle.growth_factor = 0.05
			particle.lifespan = 50

			particle.status = 'active'
			particle.visible = 1

			particle.lifespan_type = 'time'

			active_sprite_list.change_layer(particle, 1)

			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery

	def portal_gun_particles(self, startxy, color):
		i = 0
		while i < 40:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 2

				speed = 2
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = color
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]


				particle.growth_factor = 0.025
				particle.lifespan_type = 'distance'
				particle.lifespan = 10

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 0) #layer below ninja.
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def bubble_pop_particles(self, startxy):
		i = 0
		while i < 30:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 2

				speed = 2
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = (210,145,255)
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]


				particle.growth_factor = 0.025
				particle.lifespan_type = 'distance'
				particle.lifespan = 20

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def volt_main_particle(self, source, branch):
		i = 0
		while i == 0:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 1

				particle.noise_angle = 180

				particle.speed = 1.5
				particle.x_direction = random.choice((1,-1))
				particle.y_direction = random.choice((1,-1))
				particle.angle = random.choice((random.randrange(-85,-75,1),random.randrange(75,85,1)))
				particle.change_x = abs(math.sin(math.radians(particle.angle)) * particle.speed) * particle.x_direction
				#if source.inverted_g is False:
				#	particle.y_direction = -1
				#else:
				#	particle.y_direction = 1
				particle.change_y = abs(math.cos(math.radians(particle.angle)) * particle.speed) * particle.y_direction

				particle.base_change_y = particle.change_y
				particle.base_change_x = particle.change_x

				particle.shape = 'rect'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = options.WHITE
				#particle.color = options.BLACK

				particle.trail = True
				particle.trail_type = 'volt'

				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.lifespan_type = 'volt_boundaries'
				particle.lifespan = None
				particle.special = 'volt_finish'

				#if particle.source.inverted_g is False:
				#	particle.rect.centery = source.rect.bottom
				#else:
				#	particle.rect.centery = source.rect.top

				if particle.y_direction == -1:
					particle.rect.bottom = source.rect.bottom - 4
				else:
					particle.rect.top = source.rect.top + 4

				particle.rect.centerx = random.randrange(source.rect.centerx - 3, source.rect.centerx + 3, 1)
				particle.start_position = (particle.rect.centerx, particle.rect.centery)

				if branch != None:
					particle.rect.centerx = branch.rect.centerx
					particle.rect.centery = branch.rect.centery
					particle.x_direction = branch.x_direction * -1
					particle.y_direction = branch.y_direction
					particle.change_x = abs(math.sin(math.radians(particle.angle)) * particle.speed) * particle.x_direction
					particle.change_y = math.cos(math.radians(particle.angle)) * particle.speed * particle.y_direction
					particle.base_change_y = particle.change_y
					particle.base_change_x = particle.change_x
					particle.lifespan_type = 'volt_boundaries'
					particle.lifespan = random.randrange(10,20,1)
					layer = active_sprite_list.get_layer_of_sprite(branch)
				else:
					layer = random.choice((0,active_sprite_list.get_layer_of_sprite(source)))

				particle.status = 'active'
				particle.visible = 1

				
				active_sprite_list.change_layer(particle, layer)

				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery


	def volt_trail_particle(self, source, startxy, layer):
		i = 0
		while i == 0:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 1

				speed = 0
				particle.change_x = 0
				particle.change_y = 0

				particle.shape = 'rect'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = options.YELLOW
				#particle.color = options.BLACK


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.lifespan_type = 'time'
				particle.lifespan = 20
				particle.special = 'volt_finish'

				particle.start_position = startxy
				particle.rect.centery = particle.start_position[1]
				particle.rect.centerx = particle.start_position[0]
				

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, layer)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def metal_off_particles(self, startxy, source):
		i = 0
		while i < 20:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 3

				speed = 3
				particle.speed_mod = 0.9
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice(((210,204,243),(163,146,212),(97,84,118)))


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.growth_factor = -0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 30

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def metal_pound_charge_particles(self, startxy, source):
		i = 0
		while i < 2:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 2

				speed = 1.5
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice(((210,204,243),(163,146,212),(97,84,118)))


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.growth_factor = 0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 20

				particle.start_position = startxy
				particle.rect.centerx = startxy[0] + (particle.lifespan * particle.change_x)
				particle.rect.centery = startxy[1] + (particle.lifespan * particle.change_y)
				particle.change_x *= -1
				particle.change_y *= -1


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def wheel_laser_fire_particles(self, startxy, source, direction):
		i = 0
		while i < 8:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 1

				speed = 1.5

				if direction == 'left':
					direction_mod = -1
				else:
					direction_mod = 1

				angle = math.radians(random.randrange(45,90,1))
				particle.change_x = math.sin(angle) * speed * direction_mod #random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice((options.RED_LIST[3],options.RED_LIST[2]))#,options.WHITE))
				#particle.color = options.WHITE


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				#particle.growth_factor = 0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 15

				particle.start_position = startxy
				particle.rect.centerx = startxy[0] #+ (particle.lifespan * particle.change_x)
				particle.rect.centery = startxy[1] #+ (particle.lifespan * particle.change_y)
				#particle.change_x *= -1
				#particle.change_y *= -1


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 3)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery
	
	def wheel_laser_charge_particles(self, startxy, source, direction):
		i = 0
		while i < 1:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = random.choice((1,1,1,2))

				speed = 1.5

				if direction == 'left':
					direction_mod = -1
				else:
					direction_mod = 1

				angle = math.radians(random.randrange(45,90,1))
				particle.change_x = math.sin(angle) * speed * direction_mod #random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice((options.RED_LIST[3],options.RED_LIST[2]))#,options.WHITE))
				#particle.color = options.WHITE

				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				#particle.growth_factor = 0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 15

				particle.start_position = startxy
				particle.rect.centerx = startxy[0] + (particle.lifespan * particle.change_x)
				particle.rect.centery = startxy[1] + (particle.lifespan * particle.change_y)
				particle.change_x *= -1
				particle.change_y *= -1


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 3)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def metal_suit_particles(self, startxy, source):
		i = 0
		while i < 10:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 2

				speed = 3
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice(((210,204,243),(163,146,212),(97,84,118)))


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.growth_factor = 0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 30

				particle.start_position = startxy
				particle.rect.centerx = startxy[0] + (particle.lifespan * particle.change_x)
				particle.rect.centery = startxy[1] + (particle.lifespan * particle.change_y)
				particle.change_x *= -1
				particle.change_y *= -1


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def solar_flare_explode_particles(self, startxy, source):
		i = 0
		while i < 30:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 3

				speed = 4
				particle.speed_mod = 0.9
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = (255,226,44)


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.growth_factor = -0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 40

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def solar_flare_grow_particles(self, startxy, source):
		i = 0
		while i < 2:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.source = source #follows center
				particle.source_center = particle.source.rect.center

				particle.size = 2

				speed = 1.5
				angle = random.randrange(0,90,1)
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = (255,226,44)


				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.growth_factor = 0.025
				particle.lifespan_type = 'time'
				particle.lifespan = 20

				particle.start_position = startxy
				particle.rect.centerx = startxy[0] + (particle.lifespan * particle.change_x)
				particle.rect.centery = startxy[1] + (particle.lifespan * particle.change_y)
				particle.change_x *= -1
				particle.change_y *= -1


				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def radial_explosion_particles(self, startxy, inverted_g, seed, special):
		i = 0
		random.seed(seed)
		while i <= 10:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.special = special

				if inverted_g is False:
					particle.gravity = 0.025
					particle.max_g = options.max_g
				else:
					particle.gravity = -0.025
					particle.max_g = -options.max_g

				particle.size = 1

				speed = 2.5
				'''
				angle = math.radians(random.randrange(0,90,1))
				particle.change_x = math.sin(angle) * speed 
				if i in (1,2,3,4):
					particle.change_x *= -1
				particle.change_y = math.cos(angle) * speed 
				if i in (1,2,5,6):
					particle.change_y *= -1
				'''
				angle = math.radians(random.randrange(0,360,1))
				particle.change_x = math.sin(angle) * speed
				particle.change_y = math.cos(angle) * speed 
				particle.speed_mod = 0.92

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = (255,226,44)
				particle.color_mod = (
				-3,-15,0) #192,34,20
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.start_position = startxy
				particle.rect.centerx = startxy[0]
				particle.rect.centery = startxy[1]


				particle.growth_factor = 0.13
				particle.lifespan_type = 'time'
				particle.lifespan = 60

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 2)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def mine_explosion_particles(self, rect, inverted_g, seed, special):
		i = 0
		random.seed(seed)
		while i <= 50:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.special = special

				particle.size = 1

				speed = random.choice((1.5,2,2.5,3.5,4,4.5,5))
				particle.speed_mod = 0.92

				angle = math.radians(random.randrange(0,20,1)) * random.choice((1,-1))
				particle.change_x = math.sin(angle) * speed 
				particle.change_y = math.cos(angle) * speed
				#if i in (1,2,3):
				#	particle.change_x *= -1
				particle.change_y = math.cos(angle) * speed  * -1

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice(( (192,34,20), (192,34,20), (192,34,20), (255,226,44), (241,110,3), (253,164,20)))
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				if inverted_g is False:
					particle.gravity = 0.05
					particle.max_g = 4.5
					particle.start_position = rect.midbottom
					particle.rect.center = particle.start_position
					particle.lifespan_type = 'floor'
					particle.lifespan = rect.bottom
					
				else:
					particle.change_y *= -1
					particle.gravity = -0.05
					particle.max_g = -4.5
					particle.start_position = rect.midtop
					particle.rect.center = particle.start_position
					particle.lifespan_type = 'roof'
					particle.lifespan = rect.top


				

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 2)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery


	def bomb_explosion_particles(self, rect, seed, inverted_g, special):
		i = 0
		random.seed(seed)
		#while i < 10:
		while i <= 30:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.special = special

				particle.size = 1

				speed = random.choice((2,3,4))
				particle.speed_mod = 0.85

				angle = math.radians(random.randrange(0,90,1))
				particle.change_x = math.sin(angle) * speed * random.choice((-1,1)) * 1.5
				particle.change_y = math.cos(angle) * speed * random.choice((-1,1)) * 1.5



				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice(( (192,34,20), (192,34,20), (192,34,20), (255,226,44), (241,110,3), (253,164,20)))
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.start_position = rect.center
				particle.rect.center = particle.start_position
				particle.lifespan_type = 'time'
				particle.lifespan = 90

				if inverted_g is False:
					particle.gravity = 0.05
					particle.max_g = 4.5

				else:
					#particle.change_y *= -1
					particle.gravity = -0.05
					particle.max_g = -4.5
				
				


				

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 2)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	''' old ice version
	def break_ice_particles(self, rect, inverted_g, special):
		i = 0
		particle_number = (rect.width * rect.height) / 10
		while i <= particle_number:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 5

				speed = 4
				#angle = random.randrange(0,90,1)
				#particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				#particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'rect'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = (0,255,0)
				particle.image.fill((particle.color))
				particle.image.set_colorkey((0,255,0))
				particle.rect = particle.image.get_rect()

				temp_rect = pygame.Rect(0,0,5,5)
				point_list = [temp_rect.midbottom, temp_rect.midtop, temp_rect.midleft, temp_rect.midright]
				point1 = random.choice(point_list)
				point_list.remove(point1)
				point2 = random.choice(point_list)
				point_list.remove(point2)
				point3 = random.choice(point_list)

				pygame.draw.polygon(particle.image, (150,218,255), [point1,point2,point3], 0)


				x_mod = random.randrange(int(-rect.width / 4),(rect.width / 4),1)
				y_mod = random.randrange(int(-rect.height / 4),(rect.height / 4),1)
				particle.start_position = (rect.center[0] + x_mod,rect.center[1] + y_mod)
				particle.rect.centerx = particle.start_position[0]
				particle.rect.centery = particle.start_position[1]

				opp_side = particle.start_position[0] - rect.center[0] 
				adj_side = particle.start_position[1] - rect.center[1]
				try:
					collision_angle = math.atan(opp_side / adj_side)
				except ZeroDivisionError:
					collision_angle = math.atan(0)

				speed = random.choice((2,3,4))
				particle.speed_mod = 0.85

				#angle = collision_angle + (random.randrange(-4,4,1) * 0.1) #add or take away .4 radians (+ or - 22 degrees.)
				particle.change_x = math.sin(collision_angle) * speed 
				particle.change_y = math.cos(collision_angle) * speed
				if particle.start_position[1] < rect.center[1]:
					particle.change_y *= -1


				#particle.growth_factor = 0.05
				particle.lifespan_type = 'time'
				particle.lifespan = 15

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery
	'''

	def break_ice_particles(self, rect, inverted_g, special):
		i = 0
		particle_number = (rect.width * rect.height) / 40
		while i <= particle_number:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = random.choice((5,6))

				particle.special = special
				particle.special_number = 2 #how many snowflakes appear at end.

				#speed = random.choice((4,5,6))
				#angle = random.randrange(0,90,1)
				#particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
				#particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

				particle.shape = 'rect'
				if particle.size == 5:
					particle.image = random.choice(self.small_ice_shard_list)
				elif particle.size == 6:
					particle.image = random.choice(self.big_ice_shard_list)
				#particle.image = pygame.Surface((particle.size,particle.size))
				#particle.color = (0,255,0)
				#particle.image.fill((particle.color))
				#particle.image.set_colorkey((0,255,0))
				particle.rect = particle.image.get_rect()

				'''
				temp_rect = pygame.Rect(0,0,particle.size,particle.size)
				point_list = [temp_rect.midbottom, temp_rect.midtop, temp_rect.midleft, temp_rect.midright]
				point1 = random.choice(point_list)
				point_list.remove(point1)
				point2 = random.choice(point_list)
				point_list.remove(point2)
				point3 = random.choice(point_list)
				pygame.draw.polygon(particle.image, (150,218,255), [point1,point2,point3], 0)
				'''

				particle.start_position = rect.center
				particle.rect.centerx = particle.start_position[0]
				particle.rect.centery = particle.start_position[1]

				angle = math.radians(random.randrange(0,360,1))

				speed = random.choice((1,1.5,2,3))
				particle.speed_mod = 0.92

				#angle = collision_angle + (random.randrange(-4,4,1) * 0.1) #add or take away .4 radians (+ or - 22 degrees.)
				particle.change_x = math.sin(angle) * speed 
				particle.change_y = math.cos(angle) * speed

				particle.inverted_g = inverted_g

				'''
				if inverted_g is False:
					particle.gravity = 0.1
					particle.max_g = 9

				else:
					particle.gravity = -0.1
					particle.max_g = -9
				'''


				#particle.growth_factor = 0.05
				particle.lifespan_type = 'time'
				particle.lifespan = 30 + random.choice((-5,-4,-3,-2,-1,0,1,2,3,4,5))

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def ice_bomb_explosion_particles(self, rect, inverted_g, special):
		i = 0
		p = 0
		particle_number = (rect.width * rect.height) / 10
		while i <= 6:
			i += 1
			p = 0
			while p <= 3:
				p += 1
				if len(self.idle_particles) != 0:
					particle = self.idle_particles[0]
					self.idle_particles.remove(particle)

					particle.special = special
					particle.special_number = 5 #how many snowflakes appear at end.

					particle.size = 10

					#speed = random.choice((4,5,6))
					#angle = random.randrange(0,90,1)
					#particle.change_x = math.sin(angle) * speed * random.choice((-1,1))
					#particle.change_y = math.cos(angle) * speed * random.choice((-1,1))

					particle.shape = 'rect'
					particle.image = self.ice_diamond
					#particle.color = (0,255,0)
					#particle.image.fill((particle.color))
					#particle.image.set_colorkey((0,255,0))
					particle.rect = particle.image.get_rect()
					#temp_rect = pygame.Rect(0,0,particle.size,particle.size)
					#pygame.draw.polygon(particle.image, (150,218,255), [temp_rect.midbottom, temp_rect.midleft, temp_rect.midtop, temp_rect.midright], 0)


					'''
					point_list = [temp_rect.midbottom, temp_rect.midtop, temp_rect.midleft, temp_rect.midright]
					point1 = random.choice(point_list)
					point_list.remove(point1)
					point2 = random.choice(point_list)
					point_list.remove(point2)
					point3 = random.choice(point_list)
					pygame.draw.polygon(particle.image, (150,218,255), [point1,point2,point3], 0)
					'''


					particle.start_position = rect.center
					particle.rect.centerx = particle.start_position[0]
					particle.rect.centery = particle.start_position[1]

					angle = math.radians(0 + i*60)

					speed = p * 5 #link speed to p.
					particle.speed_mod = 0.8

					#angle = collision_angle + (random.randrange(-4,4,1) * 0.1) #add or take away .4 radians (+ or - 22 degrees.)
					particle.change_x = math.sin(angle) * speed 
					particle.change_y = math.cos(angle) * speed


					particle.inverted_g = inverted_g #just to pass along gravity direction to snowflaxes.
					'''
					if inverted_g is False:
						particle.gravity = 0.1
						particle.max_g = 9

					else:
						particle.gravity = -0.1
						particle.max_g = -9
					'''


					#particle.growth_factor = 0.05
					particle.lifespan_type = 'time'
					particle.lifespan = 20 + random.choice((-2,-1,0,1,2))

					particle.status = 'active'
					particle.visible = 1

					active_sprite_list.change_layer(particle, 1)
					particle.true_x = particle.rect.centerx
					particle.true_y = particle.rect.centery


	def snow_particles(self, rect, inverted_g, number):
		i = 0
		while i <= number:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 1

				particle.collisions = True
				particle.collision_type = 'destroy'

				particle.change_x = 0
				particle.change_y = 0

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = ((218,255,254))
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				x = rect.centerx#random.randrange(rect[0],rect[0] + rect[2])
				y = random.randrange(rect[1],rect[1] + rect[3])
				particle.change_x = random.randrange(-3,3,1) * 0.1

				if inverted_g is False:
					particle.change_y = random.choice((-2,-1)) * 0.5
					particle.gravity = 0.1
					particle.max_g = 4.5
					
				else:
					particle.change_y = random.choice((1,2)) * 0.5
					particle.gravity = -0.1
					particle.max_g = -4.5
				
				
				particle.start_position = (x,y)
				particle.rect.center = particle.start_position
				particle.lifespan_type = 'time'
				particle.lifespan = random.randrange(20,60,1)


				active_particle_list.add(particle) #for physics

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 2)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def laser_particles(self, centerpoint, direction, color): #direction = 'vertical' or 'horizonal'
		i = 0
		while i <= 5:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				particle.size = 2
				particle.speed_mod = 0.95
				particle.growth_factor = -0.05

				extra_speed = 5
				if direction == 'horizontal':
					if i in (0,1,2):
						particle.change_x = 0
						particle.change_y = i + extra_speed
					elif i in (3,4,5):
						particle.change_x = 0
						particle.change_y = (i-3 + extra_speed) * -1

				if direction == 'vertical':
					if i in (1,2,3):
						particle.change_x = i + extra_speed
						particle.change_y = 0
					elif i in (4,5,6):
						particle.change_x = (i-3 + extra_speed) * -1
						particle.change_y = 0
				

				particle.shape = 'rect'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = color
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				
				particle.start_position = centerpoint
				particle.rect.center = particle.start_position
				particle.rect.centerx -= particle.change_x * 1.5
				particle.rect.centery -= particle.change_y * 1.5
				particle.lifespan_type = 'time'
				particle.lifespan = 10


				

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 1)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery

	def spawn_vertical_particles(self, particlexy, inverted_g, color_list, moving_platform = None):
		if len(self.idle_particles) != 0:
			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)
			particle.size = 1

			if moving_platform != None:
				particle.source = moving_platform
				particle.source_center = moving_platform.rect.center

			particle.shape = 'square'
			particle.image = pygame.Surface((particle.size,particle.size))
			particle.color = options.WHITE #color_list[3]
			particle.image.fill((particle.color))
			particle.rect = particle.image.get_rect()
			particle.start_position = particlexy
			particle.rect.center = particle.start_position
			#particle.lifespan_type = 'distance'
			#particle.lifespan = random.randrange(50,56,1)

			particle.lifespan_type = 'time'
			particle.lifespan = 48 + random.randrange(0,10,1)

			particle.change_x = 0
			particle.change_y = -1

			if inverted_g is True:
				particle.change_y *= -1

			particle.status = 'active'
			particle.visible = 1

			active_sprite_list.change_layer(particle, 4)
			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery

			particle.trail = True
			particle.trail_type = 'spawn_trail'
			

	def spawn_vertical_trail_particles(self, source_particle):
		if len(self.idle_particles) != 0:
			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)
			particle.size = source_particle.size

			if source_particle.source != None:
				particle.source = source_particle.source
				particle.source_center = source_particle.source.rect.center

			particle.shape = source_particle.shape
			particle.image = pygame.Surface((particle.size,particle.size))
			particle.color = source_particle.color
			particle.image.fill((particle.color))
			particle.rect = particle.image.get_rect()
			particle.start_position = source_particle.rect.center
			particle.rect.center = particle.start_position
			
			#particle.lifespan_type = 'distance'
			#particle.lifespan = particle.dist_check(source_particle.start_position, (source_particle.rect.center)) + random.randrange(-3,1,1)

			particle.lifespan_type = 'time'
			particle.lifespan = 10

			particle.change_x = 0
			particle.change_y = 0

			particle.status = 'active'
			particle.visible = 1
			particle.dirty = 1

			active_sprite_list.change_layer(particle, 4)
			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery

	def spawn_bottom_particles(self, particlexy, inverted_g, color_list, moving_platform = None):
		if len(self.idle_particles) != 0:
			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)
			particle.size = random.choice((1,2))

			if moving_platform != None:
				particle.source = moving_platform
				particle.source_center = moving_platform.rect.center

			particle.shape = 'square'
			particle.image = pygame.Surface((particle.size,particle.size))
			particle.color = color_list[3]
			particle.image.fill((particle.color))
			particle.rect = particle.image.get_rect()
			particle.start_position = particlexy
			particle.rect.center = particle.start_position
			particle.lifespan_type = 'time'
			particle.lifespan = random.randrange(10,15,1)

			particle.change_x = random.randrange(-10,10,1) * 0.01
			particle.change_y = random.randrange(-10,-5,1) * 0.05 / particle.size

			if inverted_g is True:
				particle.change_y *= -1

			particle.status = 'active'
			particle.visible = 1

			active_sprite_list.change_layer(particle, 5)
			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery

	def waterfall_top_particles(self, particlexy, loopy, loopx, waterfall):
		if len(self.idle_particles) != 0:
			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)
			particle.size = 1

			particle.waterfall = waterfall
			particle.shape = 'square'
			particle.image = pygame.Surface((particle.size,particle.size))
			particle.color = options.LIGHT_PURPLE
			particle.image.fill((particle.color))
			particle.rect = particle.image.get_rect()
			particle.start_position = particlexy
			particle.rect.center = particle.start_position
			particle.lifespan_type = 'waterfall_top_particle'
			particle.lifespan = random.randrange(4,7,1)
			particle.loopy = loopy
			particle.loopx = loopx

			particle.change_x = random.randrange(-10,10,1) * 0.01
			particle.change_y = random.randrange(-10,-5,1) * 0.05

			if particle.waterfall.inverted is True:
				particle.change_y *= -1

			particle.status = 'active'
			particle.visible = 1

			active_sprite_list.change_layer(particle, -9)
			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery

	def bubble_particles(self, rect, layer, color):
		if len(self.idle_particles) != 0:
			particle = self.idle_particles[0]
			self.idle_particles.remove(particle)
			
			particle.size = random.choice((1,1,1,2,2,4))

			if particle.size == 4:
				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = color
				particle.image.fill(options.GREEN)
				particle.image.set_colorkey(options.GREEN)
				particle.rect = particle.image.get_rect()
				pygame.draw.circle(particle.image, particle.color, (int(particle.rect.width / 2), int(particle.rect.height / 2)), int(particle.size / 2), 0)
			else:
				particle.shape = 'square'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = color
				particle.image.fill(particle.color)
				particle.rect = particle.image.get_rect()

			particle.lifespan = 'time'
			particle.lifespan = (60 * 15) - (particle.size * 120) - random.randrange(0,180,1)


			

			particle.rect.centerx = random.randrange(rect[0],rect[0] + rect[2], 1)
			particle.rect.bottom = rect[1] + rect[3]
			particle.start_position = (particle.rect.centerx,particle.rect.centery)

			particle.change_x = 0
			particle.change_y = -0.25

			particle.status = 'active'
			particle.visible = 1

			active_sprite_list.change_layer(particle, layer)
			active_particle_list.add(particle)
			particle.true_x = particle.rect.centerx
			particle.true_y = particle.rect.centery


	def ninja_collision_particles(self, ninja_center, collision_center, inverted_g): #NOT IN USE. THEORETICAL.
		i = 0
		while i <= 10:
			i += 1
			if len(self.idle_particles) != 0:
				particle = self.idle_particles[0]
				self.idle_particles.remove(particle)

				opp_side = collision_center[0] - ninja_center[0] 
				adj_side = collision_center[1] - ninja_center[1]
				collision_angle = math.atan(opp_side / adj_side)

				#print(collision_angle)


				particle.size = 2

				speed = random.choice((1.5,2,3,))
				particle.speed_mod = 0.91

				angle = collision_angle + (random.randrange(-4,4,1) * 0.1) #add or take away .4 radians (+ or - 22 degrees.)
				particle.change_x = math.sin(angle) * speed 
				particle.change_y = math.cos(angle) * speed
				if collision_center[1] < ninja_center[1]:
					particle.change_y *= -1
				#if i in (1,2,3):
				#	particle.change_x *= -1
				#particle.change_y = math.cos(angle) * speed  * -1

				particle.shape = 'circle'
				particle.image = pygame.Surface((particle.size,particle.size))
				particle.color = random.choice(( (0,0,0), (0,0,0) ))
				particle.image.fill((particle.color))
				particle.rect = particle.image.get_rect()

				particle.start_position = collision_center
				particle.rect.center = particle.start_position
				particle.lifespan_type = 'time'
				particle.lifespan = 120

				
				if inverted_g is False:
					particle.gravity = 0.2
					particle.max_g = 4.5
						
				else:
					particle.gravity = -0.2
					particle.max_g = -4.5
				

				particle.status = 'active'
				particle.visible = 1

				active_sprite_list.change_layer(particle, 2)
				particle.true_x = particle.rect.centerx
				particle.true_y = particle.rect.centery


class SpriteSheet():
	""" Class used to grab images out of a sprite sheet. """    
	# This points to our sprite sheet image
	sprite_sheet = None
	
	def __init__(self, file_name):
		""" Constructor. Pass in the file name of the sprite sheet. """
		
		# Load the sprite sheet. 
		self.sprite_sheet = pygame.image.load(os.path.join(Current_Path, file_name)).convert()    
		
				
	def getImage(self, x, y, width, height):
		""" Grab a single image out of a larger spritesheet
			Pass in the x, y location of the sprite
			and the width and height of the sprite. """
		
		# Create a new blank image
		image = pygame.Surface([width, height]).convert() 
		
		# Copy the sprite from the large sheet onto the smaller image
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height) )
		
		# Assuming black works as the transparent color
		GREEN = (0,255,0)
		image.set_colorkey(GREEN)    
		
		# Return the image
		return image

# Set the height and width of the screen 
size = [640,360]

#for regular window. LEAVE IN FOR DEBUGGING PURPOSES. Can be handy to see terminal in some cases.
background = pygame.Surface((size))
background.fill((0,0,0))
#background.fill((255,255,255))


screen = pygame.display.set_mode((size)) #sets the main window to be blitted.
screen.fill((0,0,0))
big_screen = pygame.display.set_mode((size)) #sets the main window to be blitted.
big_screen.fill((0,0,0))

shake_screen = pygame.Surface((size)) #sets the main window to be blitted.
shake_screen.fill((0,0,0))
#screen.fill((255,255,255))

tile_list = pygame.sprite.LayeredDirty()
tile_list.clear(screen, background)

tile_list_Q1 = pygame.sprite.LayeredDirty()
tile_list_Q2 = pygame.sprite.LayeredDirty()
tile_list_Q3 = pygame.sprite.LayeredDirty()
tile_list_Q4 = pygame.sprite.LayeredDirty()
tile_list_Q5 = pygame.sprite.LayeredDirty()
tile_list_Q6 = pygame.sprite.LayeredDirty()
tile_list_Q7 = pygame.sprite.LayeredDirty()
tile_list_Q8 = pygame.sprite.LayeredDirty()

class Quadrant_Handler():
	def __init__(self):
		self.Q1_rect = pygame.Rect(-100,-100,296,316)
		self.Q2_rect = pygame.Rect(120,-100,240,316)
		self.Q3_rect = pygame.Rect(280,-100,240,316)
		self.Q4_rect = pygame.Rect(444,-100,296,316)

		self.Q5_rect = pygame.Rect(-100,144,296,316)
		self.Q6_rect = pygame.Rect(120,144,240,316)
		self.Q7_rect = pygame.Rect(280,144,240,316)
		self.Q8_rect = pygame.Rect(444,144,296,316)

	def get_quadrant(self, sprite):
		#returns the nearest quadrant of the sprite
		if sprite.rect.centery <= 180:
			quadrant_rect_list = [self.Q1_rect, self.Q2_rect, self.Q3_rect, self.Q4_rect]
		else:
			quadrant_rect_list = [self.Q5_rect, self.Q6_rect, self.Q7_rect, self.Q8_rect]

		temp_list = []
		for quadrant_rect in quadrant_rect_list:
			if sprite.rect.colliderect(quadrant_rect):
				temp_list.append(quadrant_rect)

		if len(temp_list) > 1:
			temp_list.sort(key=lambda x: x[0]) #sort by x (left side)

			if abs(temp_list[0].centerx  - sprite.rect.centerx) >= abs(temp_list[1].centerx - sprite.rect.centerx):
				temp_list.pop(0)
			else:
				temp_list.pop(1)

		if len(temp_list) == 0:
			i = []
			return(i)
		else:
			if temp_list[0] == self.Q1_rect:
				#print('1')
				return(tile_list_Q1)
			elif temp_list[0] == self.Q2_rect:
				#print('2')
				return(tile_list_Q2)
			elif temp_list[0] == self.Q3_rect:
				#print('3')
				return(tile_list_Q3)
			elif temp_list[0] == self.Q4_rect:
				#print('4')
				return(tile_list_Q4)
			elif temp_list[0] == self.Q5_rect:
				#print('5')
				return(tile_list_Q5)
			elif temp_list[0] == self.Q6_rect:
				#print('6')
				return(tile_list_Q6)
			elif temp_list[0] == self.Q7_rect:
				#print('7')
				return(tile_list_Q7)
			elif temp_list[0] == self.Q8_rect:
				#print('8')
				return(tile_list_Q8)
	
	def join_all_quadrants(self, tile): #puts tiles in appropriate quadrants
			tile_list_Q1.add(tile)
			tile_list_Q2.add(tile)
			tile_list_Q3.add(tile)
			tile_list_Q4.add(tile)
			tile_list_Q5.add(tile)
			tile_list_Q6.add(tile)
			tile_list_Q7.add(tile)
			tile_list_Q8.add(tile)		

	def join_quadrants(self, tile): #puts tiles in appropriate quadrants
		if tile.rect.colliderect(self.Q1_rect):
			tile_list_Q1.add(tile)
		if tile.rect.colliderect(self.Q2_rect):
			tile_list_Q2.add(tile)
		if tile.rect.colliderect(self.Q3_rect):
			tile_list_Q3.add(tile)
		if tile.rect.colliderect(self.Q4_rect):
			tile_list_Q4.add(tile)
		if tile.rect.colliderect(self.Q5_rect):
			tile_list_Q5.add(tile)
		if tile.rect.colliderect(self.Q6_rect):
			tile_list_Q6.add(tile)
		if tile.rect.colliderect(self.Q7_rect):
			tile_list_Q7.add(tile)
		if tile.rect.colliderect(self.Q8_rect):
			tile_list_Q8.add(tile)

	def leave_quadrants(self, tile): #takes tile out of all quadrants
		tile_list_Q1.remove(tile)
		tile_list_Q2.remove(tile)
		tile_list_Q3.remove(tile)
		tile_list_Q4.remove(tile)
		tile_list_Q5.remove(tile)
		tile_list_Q6.remove(tile)
		tile_list_Q7.remove(tile)
		tile_list_Q8.remove(tile)


quadrant_handler = Quadrant_Handler()

#breakable_tile_list = pygame.sprite.LayeredDirty() #just holds tiles that can be broken.

player_list = pygame.sprite.LayeredDirty() #holds player sprites as long as they have a player.
player_list.clear(screen, background)

#No Longer Needed!!
#select_tile_list = pygame.sprite.LayeredDirty() #holds tiles used for 'level select'. Never to be deleted.
#select_tile_list.clear(screen, background)

ninja_list = pygame.sprite.LayeredDirty()
ninja_list.clear(screen, background)

enemy_list = pygame.sprite.LayeredDirty()
enemy_list.clear(screen, background)

active_sprite_list = pygame.sprite.LayeredDirty() #this group will hold our sprite to be blitted
active_sprite_list.clear(screen, background)

active_particle_list = pygame.sprite.LayeredDirty() #holds particles that need to interact.
active_particle_list.clear(screen, background)

level_objects = pygame.sprite.LayeredDirty() #this group will hold our sprites to be blitted. Items.
level_objects.clear(screen, background)

level_ropes = pygame.sprite.LayeredDirty() #this group will hold our ropes.
level_ropes.clear(screen, background)

background_objects = pygame.sprite.LayeredDirty()
background_objects.clear(screen,background)

gravity_objects = pygame.sprite.LayeredDirty() #holds gravity bars
gravity_objects.clear(screen,background)

screen_objects = pygame.sprite.LayeredDirty() #this group will hold things like 'Countdown Timer', Transition Screens
screen_objects.clear(screen, background)

visual_effects = pygame.sprite.LayeredDirty() #this group will hold things like 'Countdown Timer', Transition Screens
visual_effects.clear(screen, background)

gravity_effects = pygame.sprite.LayeredDirty() #this group will hold random things for gravity to act on
gravity_effects.clear(screen, background)

item_effects = pygame.sprite.LayeredDirty() #holds item effects or player effects.
item_effects.clear(screen, background)
active_items = [] #holds currently active items. Used in level.py for item collisions.

menu_sprite_list = pygame.sprite.LayeredDirty() #this group will be manipulated by menuz
menu_sprite_list.clear(screen, background)

temp_menu_list = pygame.sprite.LayeredDirty() #holds sprites for menus occasionally (versus items)
temp_menu_list.clear(screen, background)

#create spritesheet to pass along to ninja init.
#ninja_sheet = SpriteSheet("ninjasheet.png")
level_sheet = SpriteSheet('levelsheet.png')
enemy_sheet = SpriteSheet('enemysheet.png')
menu_sheet = SpriteSheet('menusheet.png')

#created to hold players. But, must originate from main loop.
player1 = None
player2 = None
player3 = None
player4 = None


versus_match_sprite = Versus_Match_Sprite()
countdown_timer = Countdown_Timer(versus_match_sprite)
pause_background = Pause_Background()

transition_screen = Transition_Screen(countdown_timer)
effects_screen = Effects_Screen()

particle_generator = Particle_Generator()

def create_players():
	#starting_positions = ((100,30), (540,30), (100,290), (540,290))
	# Create the player
	player1 = ninja.Ninja((100,30),1,  SpriteSheet("ninjasheet.png")) #pass on tile_list for collision purposes
	#ninja_list.add(player1)
	#player_list.add(player1)
	#active_sprite_list.add(player1)
	#active_sprite_list.change_layer(player1, 1)
	player1.name = 'Player1'
	player1.avatar = 'Ninja'

	# Create the player
	player2 = ninja.Ninja((640 - 100,30),2, sprites.SpriteSheet("robotsheet.png")) #pass on tile_list for collision purposes
	#ninja_list.add(player2)
	#player_list.add(player2)
	#active_sprite_list.add(player2)
	#active_sprite_list.change_layer(player2, 1)
	player2.name = 'Player2'
	player2.avatar = 'Robot'

	# Create the player
	player3 = ninja.Ninja((100,290),3, sprites.SpriteSheet("mutantsheet.png")) #pass on tile_list for collision purposes
	#ninja_list.add(player3)
	#player_list.add(player3)
	#active_sprite_list.add(player3)
	#active_sprite_list.change_layer(player3, 1)
	player3.name = 'Player3'
	player3.avatar = 'Mutant'

	# Create the player
	player4 = ninja.Ninja((640 - 100,290),4, sprites.SpriteSheet("cyborgsheet.png")) #pass on tile_list for collision purposes
	#ninja_list.add(player4)
	#player_list.add(player4)
	#active_sprite_list.add(player4)
	#active_sprite_list.change_layer(player4, 1)
	player4.name = 'Player4'
	player4.avatar = 'Cyborg'
	
	return (player1, player2, player3, player4)


#create tiles for character select screen
#level.Build_Level(active_sprite_list, tile_list, size, ninja_sheet)

'''
#NO LONGER NEEDED!! create tile for character select screen
starting_positions = ((100,30), (540,30), (100,290), (540,290))
tile = level.Platform((screen.get_width() / 4) - 18, screen.get_height() / 4, 'classic')
tile.kill()
select_tile_list.add(tile)
tile = level.Platform((screen.get_width() / 4) - 18, screen.get_height() / 4 * 3, 'classic')
tile.kill()
select_tile_list.add(tile)
tile = level.Platform((screen.get_width() / 4 * 3) - 18, screen.get_height() / 4, 'classic')
tile.kill()
select_tile_list.add(tile)
tile = level.Platform((screen.get_width() / 4 * 3) - 18, screen.get_height() / 4 * 3, 'classic')
tile.kill()
select_tile_list.add(tile)
'''

def reset_sprites():
	#First reset everything:
	'''
	options.change_g = 0.3
	options.max_g = 5.1
	options.inverted_g = False

	level.level_builder.spawn_options = []
	level.level_builder.inverted_spawn_options = []
	level.level_builder.moving_platform_spawn_options = []
	'''


	active_items = []

	player1.reset()
	player2.reset()
	player3.reset()
	player4.reset()

	active_sprite_list.remove(player1)
	active_sprite_list.remove(player2)
	active_sprite_list.remove(player3)
	active_sprite_list.remove(player4)

	ninja_list.remove(player1)
	ninja_list.remove(player2)
	ninja_list.remove(player3)
	ninja_list.remove(player4)

	countdown_timer.reset()

	for sprite in enemy_list:
		sprite.pre_kill(reset_kill = True)

	'''
	for sprite in item_effects:
		try:
			if sprite.type == 'enemy ice cube':
				sprite.kill()
		except AttributeError:
			pass
	'''
		
	for sprite in tile_list:
		#sprite.remove(tile_list, active_sprite_list)
		sprite.kill()

	for sprite in level_objects:
		sprite.kill()

	for sprite in gravity_objects:
		sprite.kill()

	for sprite in level_ropes:
		sprite.kill()

	for sprite in background_objects:
		sprite.kill()

	particle_generator.reset()

	effects_screen.reset()

	for sprite in menu_sprite_list:
		active_sprite_list.remove(sprite)
		menu_sprite_list.remove(sprite)
		screen_objects.remove(sprite)

