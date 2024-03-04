#import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

import math
import random
import sprites
import ninja
import options
import menus
import os
import sys
import sounds
import enemy
import rope_physics
import controls

if getattr(sys, 'frozen', False):
	Current_Path = sys._MEIPASS
else:
	Current_Path = str(os.path.dirname(__file__)) + str('/GameData/')

def flip_gravity():
				gbarrier = False
				options.inverted_g = not options.inverted_g

				for item in sprites.gravity_objects:
					try:
						if item.type == 'gravity_barrier':
							if item.opposite is True:
								item.opposite = False
							else:
								item.opposite = True
							#item.switch_tiles()
							break
					except AttributeError:
						pass
				if gbarrier is False:
					for ninja in sprites.ninja_list:
						if ninja.inverted_g is False:
							ninja.invert_g()
						else:
							ninja.revert_g()

					for sprite in sprites.gravity_effects:
						sprite.invert_g(None)


					for ninja in sprites.player_list:
						if ninja not in sprites.ninja_list: 
							ninja.death_sprite.inverted_g = not ninja.death_sprite.inverted_g

					for enemy in sprites.enemy_list:
						enemy.inverted_g = not enemy.inverted_g
						for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g


					for tile in sprites.tile_list:
						if tile.type == 'platform' or tile.type == 'tile':
							if tile.inverted_g is True:
								tile.inverted_g = False
							else:
								tile.inverted_g = True
							tile.update()

					for rope in sprites.level_ropes:
						rope.invert_g()

					for item in sprites.active_items:
						try:
							#item.inverted_g = item.ninja.inverted_g
							if item.inverted_g is True:
								item.inverted_g = False
							else:
								item.inverted_g = True
						except AttributeError:
							pass

					for particle in sprites.active_particle_list:
						if particle.inverted_g is True:
							particle.normal_g()
						else:
							particle.invert_g()

					for sprite in sprites.level_objects:
						try:
							if sprite.type == 'cannon':
								if sprite.inverted_g is True:
									sprite.inverted_g = False
								else:
									sprite.inverted_g = True
						except AttributeError:
							pass

def get_diamond_list(x,y,radius):
				diamond_list = [] 
				diamond_list.append((x,y - radius))
				diamond_list.append((x + radius, y))
				diamond_list.append((x, y + radius))
				diamond_list.append((x - radius,y))

				return(diamond_list)

def get_square_list(x,y,radius): #build square pattern from circle radius
				square_list = [] 
				square_list.append((x - radius,y - radius))
				square_list.append((x + radius, y - radius))
				square_list.append((x + radius, y + radius))
				square_list.append((x - radius,y + radius))

				return(square_list)

def get_circle_list(xcenter,ycenter,radius): #build circle pattern from circle radius
				'''
				circle_list=[]
				
				for i in range(0, 360, 15): #create circle with 24 points
					y = ycenter + (radius*math.sin(math.radians(i)))
					x = xcenter + (radius*math.cos(math.radians(i)))
					#Create array with all the x-co and y-co of the circle
					circle_list.append((x,y))

				circle_list.sort(key=lambda point:math.atan2(point[0], point[1]))

				print(circle_list)
				return circle_list
				'''
				circle_list=[]
				i = 0
				while i < 360:
					y = ycenter + (radius*math.sin(math.radians(i)))
					x = xcenter + (radius*math.cos(math.radians(i)))
					#Create array with all the x-co and y-co of the circle
					circle_list.append((round(x),round(y)))
					i += 0.25

				#circle_list.sort(key=lambda point:math.atan2(point[0], point[1]))
				return circle_list



class Red_Light_Bar(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, point1, point2):
		#constructor functionf
		pygame.sprite.DirtySprite.__init__(self)

		#first figure out if vertical or horizontal
		if point1[0] == point2[0]: #vertical
			base_image = pygame.Surface((1,360))

		else: #horizontal
			base_image = pygame.Surface((640,1))


		color_list = 	[(0,0,0),
						(10,5,5),
						(20,10,11),
						(31,16,17),
						(41,21,23),
						(52,27,29),
						(62,32,35),
						(72,37,41),
						(83,43,47),
						(93,48,52),
						(104,54,58)
						]

		
		self.image_list = []
		self.image_number = 0
		self.frame_counter = 6
		self.image_direction = 1

		i = 0
		while i < len(color_list):
			image = base_image.copy()
			image.fill(color_list[i])
			self.image_list.append(image)
			i += 1

		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()

		self.rect.x = point1[0]
		self.rect.y = point1[1]

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, -10)
		sprites.background_objects.add(self)

		self.dirty = 1



	def update(self):
		self.frame_counter -= 1
		if self.frame_counter == 0:

			self.image_number += self.image_direction
			if self.image_number < 0:
				self.image_number = 0
				self.image_direction *= -1
			elif self.image_number >= len(self.image_list):
				self.image_number = len(self.image_list) - 1
				self.image_direction *= -1

			#if self.image_number == 0 or self.image_number == len(self.image_list) - 1:	
			if self.image_number == len(self.image_list) - 1:
				self.frame_counter = 24
			else:
				self.frame_counter = 6

			self.image = self.image_list[self.image_number]
			self.dirty = 1


class Background_Laser(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, direction, start_point):
		#constructor functionf
		pygame.sprite.DirtySprite.__init__(self)

		#the following serves some function, but mostly just replicates ninja.
		self.direction = direction

		self.type = 'background_laser'

		if self.direction == 'horizontal':
			self.image = sprites.level_sheet.getImage(241,36,11,7)
			self.change_x = 2
			self.change_y = 0

		elif self.direction == 'vertical':
			self.image = sprites.level_sheet.getImage(232,33,7,11)
			self.change_x = 0
			self.change_y = 2

		self.horizontal_start_list = [77,158,239,320]
		self.vertical_start_list = [77,158,239,320,401,482,563]
		
		self.rect = self.image.get_rect()
		self.rect.x = start_point[0]
		self.rect.y = start_point[1]

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, -9)
		sprites.background_objects.add(self)

		self.dirty = 1


	def update(self):

		self.dirty = 1
		
		self.rect.y += self.change_y
		self.rect.x += self.change_x

		self.position_check()

	def position_check(self):
		if self.change_x > 0:
			if self.rect.x > sprites.size[0]:
				self.rect.right = 0
				self.rect.y = random.choice(self.horizontal_start_list)
				self.change_x *= random.choice((1,-1))
		elif self.change_x < 0:
			if self.rect.right < 0:
				self.rect.left = sprites.size[0]
				self.rect.y = random.choice(self.horizontal_start_list)
				self.change_x *= random.choice((1,-1))

		elif self.change_y > 0:
			if self.rect.y > sprites.size[1]:
				self.rect.bottom = 0
				self.rect.centerx = random.choice(self.vertical_start_list)
				self.change_y *= random.choice((1,-1))
		elif self.change_y < 0:
			if self.rect.bottom < 0:
				self.rect.top = sprites.size[1]
				self.rect.centerx = random.choice(self.vertical_start_list)
				self.change_y *= random.choice((1,-1))



class Reflection(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rect):
		#constructor functionf
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface((rect.width,rect.height))
		self.image.fill(options.BLACK)
		self.image.set_alpha(150)
		self.rect = self.image.get_rect()

		self.rect.x = rect.x
		self.rect.y = rect.y + 1

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 10)
		sprites.background_objects.add(self)

	def update(self):
		self.dirty = 1
		self.image.blit(sprites.screen, (0,0), area = (self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height))
		self.image = pygame.transform.flip(self.image, False, True)
		#self.image.fill((60,60,60), special_flags = pygame.BLEND_RGBA_SUB)

class PicFrame(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self):
		#constructor functionf
		pygame.sprite.DirtySprite.__init__(self)
		file_name = "picframe.png"
		self.image = pygame.image.load(os.path.join(Current_Path, file_name)).convert()
		self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()

		self.rect.x = 0
		self.rect.y = 0

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 50)
		sprites.background_objects.add(self)

		self.dirty = 1

class Rainstorm(pygame.sprite.DirtySprite):
	def __init__(self, wind):
		pygame.sprite.DirtySprite.__init__(self)

		self.raindrop_list = []

		self.type = 'rainstorm'

		self.wind = wind #(-1,0,1) #left, right, or down

		self.wind = 0

		'''
		if self.wind == 1:
			self.base_image = pygame.Surface((4,12))
			self.base_image.fill(options.GREEN)
			self.base_image.set_colorkey(options.GREEN)
			pygame.draw.line(self.base_image, (0,100,100),(0,0),(4,12),1)

		elif self.wind == 0:
			self.base_image = pygame.Surface((1,12))
			self.base_image.fill((0,100,100))
		'''

		if options.background_effects == 'High':
			number = 30
		elif options.background_effects == 'Low':
			number = 15
		else:
			number = 0
		
		for i in range(number):
			raindrop = Raindrop(self, 'background')
			self.raindrop_list.append(raindrop)

		for i in range(number):
			raindrop = Raindrop(self, 'foreground')
			self.raindrop_list.append(raindrop)


		sprites.level_objects.add(self)

class Raindrop(pygame.sprite.DirtySprite):
	def __init__(self, rainstorm, depth):
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'raindrop'

		self.rainstorm = rainstorm

		if depth == 'foreground':
			height_range = (8,10)
		else:
			height_range = (6,8)
		if self.rainstorm.wind == 1:
			self.image = pygame.Surface((4,12))
			self.image.fill(options.GREEN)
			self.image.set_colorkey(options.GREEN)
			pygame.draw.line(self.base_image, (0,100,100),(0,0),(4,12),1)

		elif self.rainstorm.wind == 0:
			height = random.randrange(height_range[0],height_range[1],1)
			self.image = pygame.Surface((1,height))
			self.image.fill((255,255,255))

		self.rect = self.image.get_rect()

		self.depth = depth
		if depth == 'foreground':
			self.change_y = 4
			self.change_x = 1 * self.rainstorm.wind
			sprites.background_objects.add(self)
			sprites.active_sprite_list.add(self)
			sprites.active_sprite_list.change_layer(self, 0)
		elif depth == 'background':
			self.change_y = 3
			self.change_x = 1 * self.rainstorm.wind
			sprites.background_objects.add(self)
			sprites.active_sprite_list.add(self)
			sprites.active_sprite_list.change_layer(self, -8)

		self.rect.centerx = random.randrange(7,633,1)
		self.rect.centery = random.randrange(0,sprites.size[1],1)

		#self.travel_bottom = random.choice((True,False,False)) #False will collide with all tiles


	def update(self):
		self.dirty = 1

		self.rect.x += self.change_x
		self.rect.y += self.change_y

		if self.rect.top > 360 or self.rect.left > 640:
			self.rect.bottom = 0
			self.rect.centerx = random.randrange(7,633,1)			

		#if self.collisions == 'main':
		if self.depth == 'foreground' or self.rect.bottom > 300: #300 is just above bottom tiles
			current_tile_list = sprites.quadrant_handler.get_quadrant(self)
			for tile in current_tile_list:
				if tile.type in ('tile', 'platform'):
					if tile.rect.colliderect(self.rect):
						sprites.particle_generator.rain_particles((self.rect.centerx,tile.rect.top), (255,255,255))
						self.reset()
						break
				elif tile.type == 'mallow':
					if tile.rect.colliderect(self.rect):
						if self.rect.bottom > tile.rect.top + 5:
							#sprites.particle_generator.single_mallow_particles((self.rect.right - 1 + random.choice((-1,0,1)), 320), None, None, False, None, (0,0), 1)
							sprites.particle_generator.rain_particles((self.rect.centerx,tile.rect.top), (255,255,255))
							self.reset()
							break

			for ninja in sprites.ninja_list:
				if self.rect.colliderect(ninja.collision_rect):
					sprites.particle_generator.rain_particles((self.rect.centerx,self.rect.bottom), (255,255,255))
					self.reset()
					break

	def reset(self):
		self.rect.bottom = 0
		self.rect.centerx = random.randrange(7,633,1)
		#self.travel_bottom = random.choice((True,False,False))
						





class Snowfield(pygame.sprite.DirtySprite):
	def __init__(self, wind):
		pygame.sprite.DirtySprite.__init__(self)

		self.snowflake_list = []

		self.type = 'snowfield'

		if options.background_effects == 'High':
			number = (30,50)
		elif options.background_effects == 'Low':
			number = (20,30)
		else:
			number = (10,20)

		for i in range(number[0]):
			snowflake = Snowflake(self, 'front')
			self.snowflake_list.append(snowflake)

		for i in range(number[1]):
			snowflake = Snowflake(self, 'back')
			self.snowflake_list.append(snowflake)

		sprites.level_objects.add(self)

		self.wind = wind

		self.storm_status = 'idle'
		self.wind_speed = 0
		self.wind_max = 1.5
		self.wind_accel = 0.05
		self.wind_timer = 0

	def update(self):
		if self.wind is True:
			self.wind_timer += 1
			if self.storm_status == 'idle':
				if self.wind_timer == 600:
					self.wind_timer = 0
					self.storm_status = random.choice(('left','right'))
			elif self.storm_status != 'idle':
				if self.wind_timer == 300:
					self.wind_timer = 0
					self.storm_status = 'idle'

		if self.storm_status == 'idle':
			if self.wind_speed > -0.05 and self.wind_speed < 0.05:
				self.wind_speed = 0
			if self.wind_speed != 0:
				if self.wind_speed > 0:
					self.wind_speed -= self.wind_accel
				elif self.wind_speed < 0:
					self.wind_speed += self.wind_accel

		elif self.storm_status == 'left':
			self.wind_speed -= self.wind_accel
			if self.wind_speed < self.wind_max * -1:
				self.wind_speed = self.wind_max * -1

		elif self.storm_status == 'right':
			self.wind_speed += self.wind_accel
			if self.wind_speed > self.wind_max:
				self.wind_speed = self.wind_max

		if self.wind_speed == 0:
			for ninja in sprites.ninja_list:
					ninja.wind_speed = 0
		else:
			for snowflake in self.snowflake_list:
				x_change = (self.wind_speed / self.wind_max) * snowflake.max_change_x
				if snowflake.position == 'front' or snowflake.move_switch is True:
					snowflake.rect.x += x_change

			'''
			for ninja in sprites.ninja_list:
				if ninja.status != 'climb':
					if self.wind_speed > 0:
						ninja.change_x += self.wind_accel
					elif self.wind_speed < 0:
						ninja.change_x -= self.wind_accel
			'''

			
			for ninja in sprites.ninja_list:
				if ninja.item != 'metal suit':
					if ninja.status != 'climb' and ninja.status != 'cling' and ninja.FID is False:
						ninja.rect.x += self.wind_speed
						ninja.true_x += self.wind_speed
						ninja.wind_speed = self.wind_speed
						if ninja.rect.right < 0:
							ninja.rect.left = sprites.size[0]
							ninja.true_x = ninja.rect.x
							ninja.bandana.new_position()
						elif ninja.rect.left > sprites.size[0]:
							ninja.rect.right = 0
							ninja.true_x = ninja.rect.x
							ninja.bandana.new_position()


						if ninja.status == 'jump':
							ninja.change_x = self.wind_speed #* 2
						elif ninja.status == 'falling':
							if ninja.fall_timer >= 6:
								ninja.change_x = self.wind_speed #* 2


							
						
						'''
						if ninja.inverted_g is False:
							ninja.collision_check()
						else:
							ninja.inverted_collision_check()
						'''

						'''
						#bonus collision check - stops going through walls and causing collision errors
						for tile in sprites.tile_list: #check y first
							if tile.type == 'tile':
								#rect = (ninja.rect.x,ninja.rect.top + 10, ninja.rect.width, ninja.rect.height - 20)
								if tile.top_rect.colliderect(ninja.rect_bottom):
									ninja.rect.bottom = tile.rect.top
									break
						'''

						for tile in sprites.tile_list:
							if tile.type == 'mallow_wall' or tile.type == 'tile':
								rectR = (ninja.rect.right,ninja.rect.top +5, 2, ninja.rect.height - 10)
								rectL = (ninja.rect.left - 1,ninja.rect.top +5, 2, ninja.rect.height - 10)
								if tile.rect.colliderect(rectR):
									if ninja.status != 'right':
										if ninja.change_x > self.wind_speed * -1:
											ninja.change_x = self.wind_speed * -1
									break
								elif tile.rect.colliderect(rectL):
									if ninja.status != 'left':
										if ninja.change_x < self.wind_speed * -1:
											ninja.change_x = self.wind_speed * -1
									break

class Snowflake(pygame.sprite.DirtySprite):
	def __init__(self, snowfield,position):
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'snowflake'
		self.position = position
		self.snowfield = snowfield
		if self.position == 'front':
			layer = 5
			self.change_y = 1
			self.image = sprites.level_sheet.getImage(565, 179, 5, 5)
		elif self.position == 'back':
			layer = -8
			self.change_y = 1
			self.image = sprites.level_sheet.getImage(566, 173, 3, 3)

		self.rect = self.image.get_rect()

		self.change_x = 0
		self.max_change_x = self.change_y * 3


		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)

		self.rect.centerx = random.randrange(-640,sprites.size[0]+640,1)
		self.rect.centery = random.randrange(0,sprites.size[1],1)

		self.move_switch = True

	def update(self):
		self.dirty = 1

		if self.position == 'front':
			self.rect.y += self.change_y
		else:
			if self.move_switch is True:
				self.rect.y += self.change_y
				self.move_switch = False
			else:
				self.move_switch = True
		
		if self.rect.top > sprites.size[1]:
			self.loop_flake()

		if self.snowfield.storm_status == 'left':
			if self.rect.right < 0:
				self.rect.left = random.randrange(640, 690, 1)
		if self.snowfield.storm_status == 'right':
			if self.rect.left > 640:
				self.rect.right = random.randrange(-50, 0, 1)


	def loop_flake(self):
		self.rect.centerx = random.randrange(-180,sprites.size[0]+180,1)
		if self.rect.right < 0 or self.rect.left > sprites.size[0]:
			if self.snowfield.storm_status == 'left':
				self.rect.left = random.randrange(640,690,1)
				self.rect.centery = random.randrange(0,360,1)
			elif self.snowfield.storm_status == 'right':
				self.rect.left = random.randrange(-50,0,1)
				self.rect.centery = random.randrange(0,360,1)
		else:
			self.rect.y = random.randrange(-50,0,1)


		'''
		#self.rect.centerx = random.randrange(-640,sprites.size[0]+640,1)
		self.rect.centerx = random.randrange(-150,sprites.size[0]+150,1)
		if self.rect.centerx > sprites.size[0] or self.rect.centerx < 0:
			self.rect.centery = random.randrange(0,350,1)
		else:
			self.rect.bottom = random.randrange(-50,0,1)

		#now put flakes on the right side. Allows for fewer flaxes required.
		if self.snowfield.storm_status == 'left':
			if self.rect.centerx < 0: 
				self.rect.centerx = sprites.size[0] + abs(self.rect.centerx)
		elif self.snowfield.storm_status == 'right':
			if self.rect.centerx > sprites.size[0]:
				self.rect.centerx = 640 - self.rect.centerx
		'''





class TV_Screen(pygame.sprite.DirtySprite):
	def __init__(self, position, source_surface, target, layer):
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'tv_screen'

		self.image = pygame.Surface((100,50))
		self.temp_image = pygame.Surface((200,100))
		self.rect = self.image.get_rect()

		self.rect.x = position[0]
		self.rect.y = position[1]

		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)

		self.dirty = 1
		self.counter = 0

		self.source_surface = source_surface
		self.target = target

		self.target_list = []
		for ninja in sprites.ninja_list:
			self.target_list.append(ninja)

		self.target_timer = random.randrange(0,300)
		self.switch_timer = 0

		i = random.randrange(0,10,1)
		self.line_list = [0 + i,10 + i,20 + i,30 + i,40 + i]
		self.line_counter = 0

		self.line_image = pygame.Surface((self.rect.width,1))
		self.line_image.fill((255,255,255))
		self.line_image.set_alpha(100)

		self.static_image_1 = pygame.Surface((200,100))
		self.static_image_1.fill(options.LIGHT_PURPLE)
		x = 0
		y = 0
		while x < 200 - 1:
			while y < 100 - 1:
				color = random.choice((options.DARK_PURPLE, options.LIGHT_PURPLE))
				i = random.choice((True,False))
				if i is True:
					pygame.draw.rect(self.static_image_1, options.DARK_PURPLE, (x,y,1,1), 0)
				y += 1
			y = 0
			x += 1

		self.static_image_2 = pygame.Surface((200,100))
		self.static_image_2.fill(options.LIGHT_PURPLE)
		x = 0
		y = 0
		while x < 200 - 1:
			while y < 100 - 1:
				color = random.choice((options.DARK_PURPLE, options.LIGHT_PURPLE))
				i = random.choice((True,False))
				if i is True:
					pygame.draw.rect(self.static_image_2, options.DARK_PURPLE, (x,y,1,1), 0)
				y += 1
			y = 0
			x += 1


		self.glitch = False
		self.glitch_timer = 0

		self.camera = TV_Camera(self)

	def update(self):
		if options.background_effects != 'Off':	
			self.dirty = 1
			if self.camera != None and self.camera.frozen is False:	
				if self.target.rect.centerx - 100 < 0:
					x = 0
				elif self.target.rect.centerx + 100 > 640:
					x = 640 - 200
				else:
					x = self.target.rect.centerx - 100
				
				if self.target.rect.centery - 50 < 0:
					y = 0
				elif self.target.rect.centery + 50 > 360:
					y = 360 - 100
				else:
					y = self.target.rect.centery - 50

				if self.glitch is False:
					self.temp_image.blit(self.source_surface, (0,0), area = (x, y, 200, 100))
					
				pygame.transform.scale(self.temp_image, (100,50), self.image)


				self.image.fill((25,25,25), special_flags = pygame.BLEND_RGBA_ADD)

				self.line_counter += 1
				if self.line_counter >= 10:
					self.line_counter = 0
					for i, item in enumerate(self.line_list):
						temp_number = item
						temp_number += 1
						if temp_number > 50:
							temp_number = 0
						self.line_list[i] = temp_number


				for y_point in self.line_list:
					self.image.blit(self.line_image,(0,y_point))

				
				self.target_timer += 1
				
				if self.target.visible == 0:
					self.target_timer = 600

				if self.target_timer >= 600:
					self.target_timer = 0
					
					#reset list choices
					old_target = self.target
					self.target_list = []
					for ninja in sprites.ninja_list:
						self.target_list.append(ninja)

					if len(self.target_list) > 0:
						self.target = random.choice((self.target_list))

					if self.target != old_target:
						self.glitch = True
						self.base_temp_image = self.temp_image.copy()
						self.glitch_timer = 22
						self.camera.target = self.target
						self.camera.hover_mod = random.randrange(-5,5,1)

				if self.glitch is True:
					self.glitch_timer -= 1
					self.dirty = 1
					if self.glitch_timer > 19:
						self.temp_image = self.base_temp_image.copy()
						menus.shift_glitch(self.image, 'left')
					elif self.glitch_timer > 15:
						self.temp_image = self.base_temp_image.copy()
						menus.vertical_glitch(self.image)
					elif self.glitch_timer > 6:
						if self.glitch_timer % 2 == 0: #even number
							self.temp_image = self.static_image_1.copy()
						else:
							self.temp_image = self.static_image_2.copy()
					elif self.glitch_timer == 6:
						self.visible = 0
					else:
						self.visible = 1
						if self.target.rect.centerx - 100 < 0:
							x = 0
						elif self.target.rect.centerx + 100 > 640:
							x = 640 - 200
						else:
							x = self.target.rect.centerx - 100

						if self.target.rect.centery - 50 < 0:
							y = 0
						elif self.target.rect.centery + 50 > 360:
							y = 360 - 100
						else:
							y = self.target.rect.centery - 50
						
						self.temp_image.blit(self.source_surface, (0,0), area = (x, y, 200, 100))
						menus.shift_glitch(self.image, 'right')


					if self.glitch_timer == 0:
						self.glitch = False

			else: #static!:
				self.glitch_timer += 1
				if self.glitch_timer > 5:
					self.glitch_timer = 0
					if self.temp_image == self.static_image_1:
						self.temp_image = self.static_image_2
					else:
						self.temp_image = self.static_image_1

				pygame.transform.scale(self.temp_image, (100,50), self.image)


				self.image.fill((25,25,25), special_flags = pygame.BLEND_RGBA_ADD)

				self.line_counter += 1
				if self.line_counter >= 10:
					self.line_counter = 0
					for i, item in enumerate(self.line_list):
						temp_number = item
						temp_number += 1
						if temp_number > 50:
							temp_number = 0
						self.line_list[i] = temp_number

				for y_point in self.line_list:
					self.image.blit(self.line_image,(0,y_point))

class TV_Camera(enemy.Enemy):
	def __init__(self, TV_Screen):
		#constructor function
		enemy.Enemy.__init__(self)

		self.type = 'tv_camera'

		self.subtype = 'tv_camera'

		#pygame.sprite.DirtySprite.__init__(self)

		self.online_key = 0
		
		self.online_frame = 0 #ticks up on frame each time. Handled by HOST. Keeps things in line.


		self.tv_screen = TV_Screen

		self.right_list = []
		image = sprites.enemy_sheet.getImage(20, 388, 19, 12)
		self.right_list.append(image)
		image = sprites.enemy_sheet.getImage(40, 388, 19, 12)
		self.right_list.append(image)
		image = sprites.enemy_sheet.getImage(60, 388, 19, 12)
		self.right_list.append(image)
		image = sprites.enemy_sheet.getImage(40, 388, 19, 12)
		self.right_list.append(image)

		self.left_list = []
		image = sprites.enemy_sheet.getImage(20, 388, 19, 12)
		image = pygame.transform.flip(image, True, False)
		self.left_list.append(image)
		image = sprites.enemy_sheet.getImage(40, 388, 19, 12)
		image = pygame.transform.flip(image, True, False)
		self.left_list.append(image)
		image = sprites.enemy_sheet.getImage(60, 388, 19, 12)
		image = pygame.transform.flip(image, True, False)
		self.left_list.append(image)
		image = sprites.enemy_sheet.getImage(40, 388, 19, 12)
		image = pygame.transform.flip(image, True, False)
		self.left_list.append(image)

		self.image_list = self.left_list

		self.image_number = 0
		self.image = self.image_list[0]
		self.rect = self.image.get_rect()
		self.frame_counter = 0

		self.rect.x = self.tv_screen.rect.centerx
		self.rect.y = self.tv_screen.rect.centery

		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery

		sprites.enemy_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 1)

		self.dirty = 1

		self.hover_mod = 5
		self.hover_mod_change = -0.25
		self.target = self.tv_screen.target

		self.freezable = True
		self.frozen = False

		self.ice_cube = enemy.Ice_Cube_Sprite(self,(0,388,19,12))

		self.status = 'idle'

		self.physics = 'ghost' #'ghost', 'normal', 'stick'

		self.collision_dict = 	{'ghost' : pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2), 
								'death' : pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)

								}

		self.death_list = ['jump', 'roll', 'explosion', 'laser', 'volt', 'metal pound'] #jump, roll, metal pound, explosion, laser
		self.death_type = 'crumble' #crumble, explode
		self.dirty = 1
		
	def update(self):
		self.dirty = 1
		#self.online_frame_number += 1

		if self.frozen is False:
			self.frame_counter += 1
			if self.frame_counter >= 3:
				self.frame_counter = 0
				self.image_number +=1
				if self.image_number > 2:
					self.image_number = 0
				#if self.inverted_g is True:
				if self.inverted_g is True:
					i = self.image_list[self.image_number].copy()
					self.image = pygame.transform.flip(i, False, True)
				else:
					self.image = self.image_list[self.image_number]

		if self.frozen is False:
			self.update_hover_mod()
			self.follow_target() #gets target_true_x
		self.boundary_check() #handles 'loop physics'

		#Updates all collision rects before going to main enemy 'update' function
		self.update_collision_dict()

		#The following are handled in the Enemy Class. Gravity, Tile Collisions, movex_y
		super(TV_Camera, self).update()

	def pre_kill(self, reset_kill = False):
		self.ice_cube.kill()
		self.tv_screen.camera = None #triggers stat
		self.crumble()
		sprites.enemy_list.remove(self)
		self.kill()

 

	def update_collision_dict(self):
		self.collision_dict['ghost'] = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)
		self.collision_dict['death'] = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)
		#self.collision_dict['tile' ] = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4, self.rect.height)
	
	def boundary_check(self):
		if self.target.loop_physics is True:
			if self.rect.bottom < 0 and self.change_y < 0:
				self.rect.top = sprites.size[1]
				self.true_y = self.rect.centery

			if self.rect.top > sprites.size[1] and self.change_y > 0:
				self.rect.bottom = 0
				self.true_y = self.rect.centery

			if self.rect.right < 0 and self.change_x < 0:
				self.rect.left = sprites.size[0]
				self.true_x = self.rect.centerx

			if self.rect.left > sprites.size[0] and self.change_x > 0:
				self.rect.right = 0
				self.true_x = self.rect.centerx

	def update_hover_mod(self):
		if self.hover_mod == 5:
			self.hover_mod_change = -0.25
		elif self.hover_mod == -5:
			self.hover_mod_change = 0.25

		self.hover_mod += self.hover_mod_change

	def follow_target(self):
		if options.loop_physics is False:
			if self.rect.centerx <= self.target.rect.centerx:
				self.image_list = self.right_list
				if self.target.rect.centerx < 100:
					self.target_centerx = self.target.rect.centerx + 100
					self.target_centery = self.target.rect.top + self.hover_mod - 100
					if self.target.FID is True:
						self.target_centery -= 20
				else:
					self.target_centerx = self.target.rect.centerx - 100
					self.target_centery = self.target.rect.top + self.hover_mod
					if self.target.FID is True:
						self.target_centery -= 20
			else:
				self.image_list = self.left_list
				if self.target.rect.centerx > 640 - 100:
					self.target_centerx = self.target.rect.centerx - 100
					self.target_centery = self.target.rect.top + self.hover_mod - 100
					if self.target.FID is True:
						self.target_centery -= 20

				else:
					self.target_centerx = self.target.rect.centerx + 100
					self.target_centery = self.target.rect.top + self.hover_mod
					if self.target.FID is True:
						self.target_centery -= 20
		else:
			if abs(self.rect.centerx - self.target.rect.centerx) < sprites.size[0] / 2:
				self.target_centerx = self.target.rect.centerx
			elif self.rect.centerx < self.target.rect.centerx:
				self.target_centerx = -50
			elif self.rect.centerx > self.target.rect.centerx:
				self.target_centerx = sprites.size[0] + 50

		'''
		if self.target.loop_physics is False:
			if self.target.inverted_g is False:	
				self.target_centery = self.target.rect.top + self.hover_mod
				if self.target.FID is True:
					self.target_centery -= 20
			else:
				self.target_centery = self.target.rect.bottom + self.hover_mod
				if self.target.FID is True:
					self.target_centery += 20
		else:
			if abs(self.rect.centery - self.target.rect.centery) < sprites.size[1] / 2:
				if self.target.inverted_g is False:	
					self.target_centery = self.target.rect.top + self.hover_mod
				else:
					self.target_centery = self.target.rect.bottom + self.hover_mod
			elif self.rect.centery < self.target.rect.centery:
				self.target_centery = -50
			elif self.rect.centery > self.target.rect.centery:
				self.target_centery = sprites.size[1] + 50
		'''

		if self.target.visible == 0:
			self.target_centerx = self.rect.centerx + self.hover_mod
			self.target_centery = self.rect.centery + self.hover_mod

		self.change_y = ((self.target_centery - self.rect.centery) / 20) #+ (self.hover_mod / 10)
		if self.change_y > 2:
			self.change_y = 2
		elif self.change_y < -2:
			self.change_y = -2

		self.change_x = ((self.target_centerx - self.rect.centerx) / 20)
		if self.change_x > 3:
			self.change_x = 3
		elif self.change_x < -3:
			self.change_x = -3


class Slime_Enemy(enemy.Enemy):
	def __init__(self, center, subtype = 'green'):
		#constructor function
		enemy.Enemy.__init__(self)

		#pygame.sprite.DirtySprite.__init__(self)

		self.online_key = 0
		
		self.online_frame = 0 #ticks up on frame each time. Handled by HOST. Keeps things in line.


		
		self.big_image_list = []

		self.idle_image_list = []
		self.jump_image_list = []

		image = sprites.enemy_sheet.getImage(0, 330, 24, 24)
		self.idle_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(25, 330, 24, 24)
		self.idle_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(0, 330, 24, 24)
		self.idle_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(50, 330, 24, 24)
		self.idle_image_list.append(image)
		self.big_image_list.append(image)

		image = sprites.enemy_sheet.getImage(0, 355, 24, 24)
		self.jump_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(25, 355, 24, 24)
		self.jump_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(50, 355, 24, 24)
		self.jump_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(75, 355, 24, 24)
		self.jump_image_list.append(image)
		self.big_image_list.append(image)

		self.split_image_list = []
		image = sprites.enemy_sheet.getImage(125, 330, 24, 24)
		self.split_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(150, 330, 24, 24)
		self.split_image_list.append(image)
		self.big_image_list.append(image)
		
		self.land_image = sprites.enemy_sheet.getImage(100, 355, 24, 24)
		self.big_image_list.append(self.land_image)

		self.knocked_left_image = sprites.enemy_sheet.getImage(100, 330, 24, 24)
		self.big_image_list.append(self.knocked_left_image)
		self.knocked_right_image = sprites.enemy_sheet.getImage(75, 330, 24, 24)
		self.big_image_list.append(self.knocked_right_image)

		self.death_image_list = []
		image = sprites.enemy_sheet.getImage(125, 355, 28, 28)
		self.death_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(154, 355, 28, 28)
		self.death_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(183, 355, 32, 32)
		self.death_image_list.append(image)
		self.big_image_list.append(image)
		image = sprites.enemy_sheet.getImage(216, 355, 32, 32)
		self.death_image_list.append(image)
		self.big_image_list.append(image)

		self.subtype = subtype
		self.particle_color_list = [options.GREEN_LIST[1],options.GREEN_LIST[2],options.GREEN_LIST[0]]
		if self.subtype == 'lava':
			self.particle_color_list = [options.RED_LIST[1],options.RED_LIST[2],options.RED_LIST[0]]
			for image in self.big_image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace(options.GREEN_LIST[0],options.RED_LIST[0])
				array.replace(options.GREEN_LIST[1],options.RED_LIST[1])
				array.replace(options.GREEN_LIST[2],options.RED_LIST[2])
				array.replace(options.GREEN_LIST[3],options.RED_LIST[3])
				array.close()
				image.unlock()

		self.frame_counter = 0
		self.image_number = 0 #0,1,or2
		self.direction = random.choice(('left','right'))
		self.image = self.idle_image_list[self.image_number]

		self.rect = self.image.get_rect()
		self.rect.centerx = center[0]
		self.rect.centery = center[1]

		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery

		sprites.enemy_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 1)
		self.base_layer = 1

		self.dirty = 1

		self.target = sprites.player1
		self.target_xy = self.target.rect.center

		self.freezable = True
		self.frozen = False

		self.ice_cube = enemy.Ice_Cube_Sprite(self,(0,305,24,24))

		self.bounce_list = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,3,3,3,2,2,2,1,1,2]
		self.online_trigger = False

		self.status = 'move'

		self.physics = 'normal' #'ghost', 'normal', 'stick', 'bounce'

		self.collision_dict = 	{'normal' : pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4),
								'death' : pygame.Rect(self.rect.x + 3, self.rect.top + 3, self.rect.width - 6, self.rect.height - 6)
								}

		#self.kill_type = 'acid'

		if self.subtype == 'lava':
			self.death_list = ['explosion', 'laser', 'traps', 'volt', 'metal pound', 'freeze'] #jump, roll, metal pound, explosion, laser, 'traps'
		else:
			self.death_list = ['explosion', 'laser', 'traps', 'volt', 'metal pound']
		
		self.death_type = 'crumble' #crumble, explode
		self.particle_type = 'stick' #stick, debris
		#self.x_accel = 0.04
		#self.accel = 0.08
		self.speed = 2
		self.speed_x = 2
		#self.friction_applies = False

		self.land_mod_x = 4
		
		self.jump_timer = 0 #set to to jump, actually jump is triggered at 0.
		self.jump_force = -4.2
		self.jump_frames = 0
		self.jump_height = 0

		#self.eye = Wheel_Eye(self, variant)
		#self.subsprite_list.append(self.eye)

		self.ai_timer = random.randrange(0,15,1) #just randomize the start of the 'ai' timer to minimize ai decisions on same frame.

		self.status = 'idle'
		self.idle_timer = 0
		self.jump_timer = 0

	def update(self):
		if self.subtype == 'lava':
			sprites.particle_generator.fire_slime_particles(self)

		self.dirty = 1
		if self.status == 'idle':
			#self.change_x = 0
			self.frame_counter += 1
			if self.frame_counter > 12:
				self.frame_counter = 0
				self.image_number += 1
			if self.image_number > len(self.idle_image_list) - 1:
				self.image_number = 0

			if self.inverted_g is True:
				i = self.idle_image_list[self.image_number].copy()
				self.image = pygame.transform.flip(i, False, True)
			else:
				self.image = self.idle_image_list[self.image_number]
			self.idle_timer += 1
			if self.idle_timer >= 180:
				#pass
				
				i = random.randrange(0,10,1)
				if len(sprites.enemy_list) < 20:
					if i <= 3 and self.subtype == 'green':
						self.trigger_split()
					else:
						self.trigger_jump(11)
				else:
					self.trigger_jump(11)
				

		elif self.status == 'land':
			#self.change_x = 0
			self.frame_counter +=1
			if self.frame_counter > 8:
				self.frame_counter = 0
				self.image_number = 1
				self.status = 'idle'
				if self.inverted_g is True:
					i = self.idle_image_list[self.image_number].copy()
					self.image = pygame.transform.flip(i, False, True)
				else:
					self.image = self.idle_image_list[self.image_number]

		elif self.status == 'split':
			self.frame_counter +=1
			if self.frame_counter > 16:
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number > len(self.split_image_list) - 1:
					self.split()
				else:
					if self.inverted_g is True:
						i = self.split_image_list[self.image_number].copy()
						self.image = pygame.transform.flip(i, False, True)
					else:
						self.image = self.split_image_list[self.image_number]


		elif self.status == 'charge_jump':
			if self.inverted_g is True:
				i = self.jump_image_list[0].copy()
				self.image = pygame.transform.flip(i, False, True)
			else:
				self.image = self.jump_image_list[0]
			self.jump_timer += 1
			if self.jump_timer >= 30:
				self.jump_timer = 0
				self.jump()

		elif self.status == 'jump':
			if self.jump_frames > 0:
				self.jump_frames -= 1
				if self.inverted_g is False:
					self.change_y = self.jump_force
				else:
					self.change_y = -self.jump_force

			#self.frame_counter += 1
			#if self.frame_counter < 5:
			#	pass
			#else:
			if self.last_collision_timer <= 0:
				if len(self.bounce_list) > 0:
					i = self.bounce_list[0]
					self.bounce_list.pop(0)
					if self.inverted_g is False:
						self.image = self.jump_image_list[i]
					else:
						i = self.jump_image_list[i].copy()
						self.image = pygame.transform.flip(i, False, True)
				else:
					if self.inverted_g is False:
						self.image = self.jump_image_list[2]
					else:
						i = self.jump_image_list[2].copy()
						self.image = pygame.transform.flip(i, False, True)

			self.change_x = self.speed


		if self.frozen is False:
			self.ai_update()
			#self.follow_target() #gets target_true_x

		self.boundary_check() #handles 'loop physics'

		#Updates all collision rects before going to main enemy 'update' function
		self.update_collision_dict()

		if self.status == 'death':
			self.pre_kill()

		#The following are handled in the Enemy Class. Gravity, Tile Collisions, movex_y
		super(Slime_Enemy, self).update()
		
		
	def pre_kill(self, reset_kill = False):
		if reset_kill is True:
			self.ice_cube.kill()
			self.kill()

		else:
			if self.death_image_list != None and self.status != 'death':
				self.status = 'death'
				self.ice_cube.kill()
				self.image_number = 0
				self.frame_counter = 0
				self.image = self.death_image_list[self.image_number]
				self.dirty = 1


				self.destroyed = True

			
			if self.status == 'death':
				self.frame_counter += 1
				if self.frame_counter > 4:
					self.image_number += 1
					self.frame_counter = 0
					if options.particles != 'Off':
						if self.image_number == 1:
							self.crumble()
					if self.image_number < len(self.death_image_list):
						old_centerx = self.rect.centerx
						old_bottom = self.rect.bottom
						old_top = self.rect.top
						self.image = self.death_image_list[self.image_number]
						self.rect = self.image.get_rect()
						self.rect.centerx = old_centerx
						if self.inverted_g is True:
							self.rect.top = old_top
						else:
							self.rect.bottom = old_bottom
						self.dirty = 1
					else:
						self.kill()

					
		#self.ice_cube.kill()
		#self.kill()

	def update_collision_dict(self):
		
		if self.inverted_g is False:
			self.collision_dict['normal'] = pygame.Rect(self.rect.x + 3, self.rect.top + 3, self.rect.width - 6, self.rect.height - 6)
			self.collision_dict['death'] = pygame.Rect(self.rect.x + 3, self.rect.top + 3, self.rect.width - 6, self.rect.height - 6)
		else:
			self.collision_dict['normal'] = pygame.Rect(self.rect.x + 3, self.rect.top + 3, self.rect.width - 6, self.rect.height - 6)
			self.collision_dict['death'] = pygame.Rect(self.rect.x + 3, self.rect.top + 3, self.rect.width - 6, self.rect.height - 6)
		

		#self.collision_dict['tile' ] = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4, self.rect.height)
	
	def trigger_split(self):
			split = True

			if len(sprites.enemy_list) >= 6:
				split = False

			if split is True:
				for sprite in sprites.background_objects:
					if sprite.type == 'classic_door':
						if sprite.spawn_timer < 90: #Not spawning:
							split = False
							break

			if split is True:
				for sprite in sprites.enemy_list:
					if sprite.subtype == 'green':
						if sprite.status == 'split':
							split = False
							break


			if split is True:
				current_tile_list = sprites.quadrant_handler.get_quadrant(self)
				temp_rect = pygame.Rect(self.rect.x - 24,self.rect.top, self.rect.width + 48, self.rect.height)
				for tile in current_tile_list:
					if tile.rect.colliderect(temp_rect):
						split = False
						break

			if split is True:
				self.status = 'split'
				self.frame_counter = 0
				self.image_number = 0

				if self.inverted_g is True:
					i = self.split_image_list[self.image_number].copy()
					self.image = pygame.transform.flip(i, False, True)
				else:
					self.image = self.split_image_list[self.image_number]

			else: #if too close to tile to split, jump!
				self.trigger_jump(11)


	def split(self, source=None):
			self.image_number = 0
			self.frame_counter = 0
			self.status = 'idle'
			self.idle_timer = random.randrange(150,250,1)

			offspring = Slime_Enemy((self.rect.centerx + (self.rect.width / 2), self.rect.centery), subtype = self.subtype)
			offspring.status = 'land'
			offspring.idle_timer = 0
			offspring.frame_counter = -5
			if offspring.inverted_g is False:
				offspring.image = offspring.land_image
			else:
				i = offspring.land_image.copy()
				offspring.image = pygame.transform.flip(i, False, True)

			self.rect.centerx -= (self.rect.width / 2)
			self.true_x = self.rect.centerx
			self.status = 'land'
			self.idle_timer = 0
			self.frame_counter = -5	
			if self.inverted_g is False:
				self.image = self.land_image
			else:
				i = self.land_image.copy()
				self.image = pygame.transform.flip(i, False, True)


			centerpoint = self.rect.right

			sprites.particle_generator.color_knocked_particles((self.rect.left + 5,self.rect.centery), 'left', self.inverted_g, self.last_collision_timer, self.particle_color_list, y_multiplier = 2, x_multiplier = 2)
			sprites.particle_generator.color_knocked_particles((self.rect.right - 5,self.rect.centery), 'right', self.inverted_g, self.last_collision_timer, self.particle_color_list, y_multiplier = 2, x_multiplier = 2)


	def trigger_jump(self, jump_height):
			self.status = 'charge_jump'
			self.bounce_list = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,3,3,3,2,2,2,1,1,2]
			self.jump_height = jump_height


	def jump(self):
			self.bounce_list = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,3,3,3,2,2,2,1,1,2]
			self.status = 'jump'
			self.change_x = random.choice((-1,1))
			self.jump_frames = self.jump_height
			if self.inverted_g is False:
				self.change_y = self.jump_force
			else:
				self.change_y = -self.jump_force
			self.frame_counter = 0

			self.direction = random.choice(('left', 'right'))
			if self.direction == 'left':
				self.speed = -abs(self.speed_x)
			else:
				self.speed = abs(self.speed_x)
			self.change_x = self.speed


	def land(self, y_speed):
		#may hold enemey-specific animation stuff
		if self.status == 'jump':
			self.status = 'land'
			self.idle_timer = 0
			self.frame_counter = 0
			
			if self.inverted_g is False:
				self.image = self.land_image
			else:
				i = self.land_image.copy()
				self.image = pygame.transform.flip(i, False, True)


			'''
			if self.inverted_g is True:
				if y_speed < -4:
					i = self.land_image.copy()
					self.image = pygame.transform.flip(i, False, True)
				else:
					self.frame_counter = 4
			else:
				if y_speed > 4:
					self.image = self.land_image
				else:
					self.frame_counter = 4
			'''


		self.jump_frames = 0

	def wall_bounce(self):
		self.bounce_list = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,3,3,3,2,2,2,1,1,2]
		'''
		if self.target == None:
			if self.target_xy[0] == 0:
				self.target_xy = (640,None)
			else:
				self.target_xy = (0,None)
		'''

		self.jump_frames = 0
		self.speed = self.change_x
		#pass #may hold enemy-specific animation stuff

	def collision_bounce(self, source):
		self.collision_timer = self.collision_timer_max

		self.bounce_list = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,3,3,3,2,2,2,1,1,2]

		#if abs(self.rect.centerx - source.rect.centerx) < 18:
		if abs(source.rect.centery - self.rect.centery) >= 15:
				self.bounce_list = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,3,3,3,2,2,2,1,1,2]

		self.jump_frames = 0

		self.status = 'jump'

		self.speed = self.change_x

		#if self.slime_subtype == None:
		if self.change_x > 0:
			sprites.particle_generator.color_knocked_particles((self.rect.left + 5,self.rect.centery), 'left', self.inverted_g, self.last_collision_timer, self.particle_color_list)
		else:
			sprites.particle_generator.color_knocked_particles((self.rect.right - 5,self.rect.centery), 'right', self.inverted_g, self.last_collision_timer, self.particle_color_list)
		
		
		#self.frame_counter = 0
		if self.inverted_g is False:
			if self.change_x > 0:
				self.image = self.knocked_right_image
			else:
				self.image = self.knocked_left_image
		else:
			if self.change_x > 0:
				i = self.knocked_right_image.copy()
				self.image = pygame.transform.flip(i, False, True)
			else:
				i = self.knocked_right_image.copy()
				self.image = pygame.transform.flip(i, False, True)


		if source.type == 'Ninja':
			if self.subtype == 'lava':
				if source.shield_sprite.active is False and source.item != 'volt':
					source.set_fire()

		self.online_trigger = True

	def boundary_check(self):
		if options.loop_physics is True:
			if self.rect.bottom < 0 and self.change_y < 0:
				self.rect.top = sprites.size[1]
				self.true_y = self.rect.centery

			if self.rect.top > sprites.size[1] and self.change_y > 0:
				self.rect.bottom = 0
				self.true_y = self.rect.centery

			if self.rect.right < 0 and self.change_x < 0:
				self.rect.left = sprites.size[0]
				self.true_x = self.rect.centerx

			if self.rect.left > sprites.size[0] and self.change_x > 0:
				self.rect.right = 0
				self.true_x = self.rect.centerx

	def ai_update(self):
		'''
		self.ai_timer += 1

		if self.target != None:
			if self.target.visible == 0:
				self.target = None
				if self.direction == 'left':
					self.target_xy = (0,None)
				elif self.direction == 'right':
					self.target_xy = (640,None)

		if self.ai_timer > 10:
			self.ai_timer = 0

		if self.ai_timer == 0 and self.collision_timer <= 0:
			if self.target == None:
				pass
			else:
				temp_rect = pygame.Rect(-50,self.rect.top - 50, 740, 100 + self.rect.height)
				if temp_rect.colliderect(self.target.rect) == 0:
					self.target = None
					if self.direction == 'left':
						self.target_xy = (0,None)
					elif self.direction == 'right':
						self.target_xy = (640,None)
					#self.target_xy = (random.choice((0,640)), None)

		if self.ai_timer == 5:
			if self.change_x > 0:
				temp_rect = pygame.Rect(self.rect.right,self.rect.centery - 12, 640, 24)
			elif self.change_x < 0:
				temp_rect = pygame.Rect(self.rect.left - 640,self.rect.centery - 12, 640, 24)
			else:
				temp_rect = None
				
			if temp_rect != None:
				ninja_list = None
				for ninja in sprites.ninja_list:
					if ninja.visible == 1:
						if temp_rect.colliderect(ninja.rect):
							dist = self.dist_check(self.rect.center, ninja.rect.center)
							if ninja_list == None or dist < ninja_list[1]:
								ninja_list = (ninja, dist)
				
				if ninja_list != None:
					self.target = ninja_list[0]

		'''
		
		#Check can proceed, otherwise turn.
		self.direction = random.choice(('right','left'))
		if self.status == 'move':
			if self.current_tile != None:
				if self.direction == 'right':
					if self.current_tile.right_tile_dist == None or self.current_tile.right_tile_dist > 3:
						if self.rect.right + 4 >= self.current_tile.rect.right:
							self.status = 'idle'
							self.image_number = 0
							self.direction = 'left'
							self.speed = -self.speed_x
						
				elif self.direction == 'left':
					if  self.current_tile.left_tile_dist == None or self.current_tile.left_tile_dist > 3:
						if self.rect.left - 4 <= self.current_tile.rect.left:
							self.status = 'idle'
							self.image_number = 0
							self.direction = 'right'
							self.speed = self.speed_x


	
	def follow_target(self):
		if self.target != None:
			self.target_xy = self.target.rect.center

			
		if self.collision_timer <= 0:
			if self.direction == 'right':	
				if self.change_x < self.max_speed:
					self.change_x += self.accel
				if self.rect.centerx > self.target_xy[0] + 10:
					self.direction = 'left'
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]
					
			else:
				if self.change_x > -self.max_speed:
					self.change_x -= self.accel
				if self.rect.centerx < self.target_xy[0] - 10:
					self.direction = 'right'
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]

			if self.inverted_g is False:
				if self.direction == 'left' and self.change_x > 0:
					sprites.particle_generator.slide_particles((self.rect.right - 5, self.rect.bottom), 'right', self.inverted_g)
				elif self.direction == 'right' and self.change_x < 0:
					sprites.particle_generator.slide_particles((self.rect.left + 5, self.rect.bottom), 'left', self.inverted_g)
			else:
				if self.direction == 'left' and self.change_x > 0:
					sprites.particle_generator.slide_particles(self.rect.topright, 'right', self.inverted_g)
					#self.bounce_list.append(4)
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]
				elif self.direction == 'right' and self.change_x < 0:
					sprites.particle_generator.slide_particles(self.rect.topleft, 'left', self.inverted_g)
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]
			
			#jump into target if close
			if self.target != None and self.jump is False:
				i = 0
				if self.direction == 'left' and self.change_x < 0:
					if self.target.change_x > 0:
						i = self.target.change_x * 10
					temp_rect = pygame.Rect(self.rect.left - 50 - i, self.rect.top, 50 + i, 24)
					if self.target.rect.colliderect(temp_rect):
						self.trigger_jump(4)
				elif self.direction == 'right' and self.change_x > 0:
					if self.target.change_x < 0:
						i = self.target.change_x * 10
					temp_rect = pygame.Rect(self.rect.right, self.rect.top, 50 + i, 24)
					if self.target.rect.colliderect(temp_rect):
						self.trigger_jump(4)

class Wheel_Enemy(enemy.Enemy):
	def __init__(self, center, variant):
		#constructor function
		enemy.Enemy.__init__(self)

		#pygame.sprite.DirtySprite.__init__(self)

		#1 and 2 are vertically stretched, 3 is normal, 4 and 5 are horizonatally stretched.
		self.image_dict = {1:[],2:[],3:[],4:[],5:[]}		

		image = sprites.enemy_sheet.getImage(0, 180, 24, 24)
		self.image_dict[1].append(image)
		image = sprites.enemy_sheet.getImage(25, 180, 24, 24)
		self.image_dict[1].append(image)
		image = sprites.enemy_sheet.getImage(50, 180, 24, 24)
		self.image_dict[1].append(image)

		image = sprites.enemy_sheet.getImage(0, 205, 24, 24)
		self.image_dict[2].append(image)
		image = sprites.enemy_sheet.getImage(25, 205, 24, 24)
		self.image_dict[2].append(image)
		image = sprites.enemy_sheet.getImage(50, 205, 24, 24)
		self.image_dict[2].append(image)

		image = sprites.enemy_sheet.getImage(0, 230, 24, 24)
		self.image_dict[3].append(image)
		image = sprites.enemy_sheet.getImage(25, 230, 24, 24)
		self.image_dict[3].append(image)
		image = sprites.enemy_sheet.getImage(50, 230, 24, 24)
		self.image_dict[3].append(image)

		image = sprites.enemy_sheet.getImage(0, 255, 24, 24)
		self.image_dict[4].append(image)
		image = sprites.enemy_sheet.getImage(25, 255, 24, 24)
		self.image_dict[4].append(image)
		image = sprites.enemy_sheet.getImage(50, 255, 24, 24)
		self.image_dict[4].append(image)

		image = sprites.enemy_sheet.getImage(0, 280, 24, 24)
		self.image_dict[5].append(image)
		image = sprites.enemy_sheet.getImage(25, 280, 24, 24)
		self.image_dict[5].append(image)
		image = sprites.enemy_sheet.getImage(50, 280, 24, 24)
		self.image_dict[5].append(image)

		




		self.image_number = 0 #0,1,or2
		self.dict_number = 3 #1,2,3,4,5... 1/2 is stretched vertically, 3 is normal, 4/5 is vertically squished
		self.image = self.image_dict[self.dict_number][self.image_number]
		self.rect = self.image.get_rect()
		self.frame_counter = 0

		self.rect.centerx = center[0]
		self.rect.centery = center[1]

		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery

		sprites.enemy_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 1)
		self.base_layer = 1

		self.dirty = 1

		self.target = sprites.player1
		self.target_xy = self.target.rect.center

		self.freezable = True
		self.frozen = False

		self.ice_cube = enemy.Ice_Cube_Sprite(self,(0,305,24,24))

		self.status = 'idle'

		self.physics = 'bounce' #'ghost', 'normal', 'stick', 'bounce'

		self.collision_dict = 	{'normal' : pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2),
								'death' : pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)
								}

		self.death_list = ['explosion', 'laser', 'volt', 'metal pound', 'traps'] #jump, roll, metal pound, explosion, laser, 'traps'
		self.death_type = 'crumble' #crumble, explode

		self.x_accel = 0.04
		self.accel = 0.08
		self.max_speed = 2
		self.bounce_var = 0.6

		self.bounce_list = []

		self.direction = random.choice(('right','left'))

		self.jump = False #set to True to trigger jump
		self.jump_timer = 0 #set to to jump, actually jump is triggered at 0.
		self.jump_force = -4.2
		self.jump_frames = 0
		self.jump_height = 0

		self.eye = Wheel_Eye(self, variant)
		self.subsprite_list.append(self.eye)

		self.ai_timer = random.randrange(0,15,1) #just randomize the start of the 'ai' timer to minimize ai decisions on same frame.

		self.variant = variant

		if self.variant == 'laser':
			#self.collision_dict.keys()
			for key in self.image_dict:
				for image in self.image_dict[key]:
					image.lock()
					array = pygame.PixelArray(image)
					array.replace((74,74,74),options.RED_LIST[1])
					array.replace((50,49,57),(50,22,34))
					array.replace((158,153,205),options.RED_LIST[2])
					#array.replace((241,239,253),options.RED_LIST[3])
					array.close()
					image.unlock()

	def update(self):
		#if self.current_tile != None:
		#	print(self.current_tile.rect.centerx)
		if self.jump is True or self.target != None:
			self.max_speed = 2
		else:
			self.max_speed = 1
		
		self.dirty = 1

		if len(self.bounce_list) > 0:
			self.dict_number = self.bounce_list[0]
			self.bounce_list.pop(0)

		if self.frozen is False:
			self.frame_counter += 1 * abs(self.change_x / self.max_speed)
			if self.frame_counter >= 1:
				self.frame_counter = 0
				if self.direction == 'right':
					self.image_number +=1
				else:
					self.image_number -= 1
				if self.image_number > 2:
					self.image_number = 0
				elif self.image_number < 0:
					self.image_number = 2

				if self.inverted_g is True:
					i = self.image_dict[self.dict_number][self.image_number].copy()
					self.image = pygame.transform.flip(i, False, True)
				else:
					self.image = self.image_dict[self.dict_number][self.image_number]

		#self.image = self.image_dict[self.dict_number][self.image_number]


		if self.frozen is False:
			#self.update_hover_mod()
			self.ai_update()
			self.follow_target() #gets target_true_x
			

		self.boundary_check() #handles 'loop physics'

		#Updates all collision rects before going to main enemy 'update' function
		self.update_collision_dict()

		#testing jump triggerd
		'''
		if self.jump is False:
			i = random.randrange(0,60,1)
			if i == 30:
				self.trigger_jump()
		'''
		if self.jump is True:
			#cance if knocked or falling
			if abs(self.change_y) > 0.5: #just tested, won't occur unless jumping or falling
				self.jump = False
				self.jump_timer = 0

			self.jump_timer -= 1
			if self.jump_timer == 0:
				self.jump = False
				#asdf
				self.jump_frames = self.jump_height
				if self.inverted_g is False:
					self.change_y = self.jump_force
				else:
					self.change_y = -self.jump_force
				if self.change_x > 0:
					self.change_x = 2
				elif self.change_x < 0:
					self.change_x = -2

		if self.jump_frames > 0:
			self.jump_frames -= 1
			if self.inverted_g is False:
				self.change_y = self.jump_force
			else:
				self.change_y = -self.jump_force

		#The following are handled in the Enemy Class. Gravity, Tile Collisions, movex_y
		super(Wheel_Enemy, self).update()

	def pre_kill(self, reset_kill = False):

		self.ice_cube.kill()
		self.crumble()
		self.eye.kill()
		self.kill()

		self.destroyed = True


	def update_collision_dict(self):
		self.collision_dict['normal'] = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		self.collision_dict['death'] = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		#self.collision_dict['tile' ] = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4, self.rect.height)
	
	def trigger_jump(self, jump_height):
		self.jump = True
		self.jump_timer = 8
		self.bounce_list = [3,4,4,5,5,4,4,3,2,2,1,1,2,2,3]
		self.jump_height = jump_height

	def bounce(self):
		#may hold enemey-specific animation stuff
		if abs(self.change_y) > 1:
			self.bounce_list = [3,4,4,4,5,5,5,4,4,4,3]

		if self.jump is True:
			self.change_y = 0
			#if self.jump_timer > 1:
			#	self.jump_timer = 1

		self.jump_frames = 0

	def wall_bounce(self):
		self.bounce_list = [3,2,2,1,1,2,2,3,3,4,4,3]
		if self.target == None:
			if self.target_xy[0] == 0:
				self.target_xy = (640,None)
			else:
				self.target_xy = (0,None)

		self.jump_frames = 0
		#pass #may hold enemy-specific animation stuff

	def collision_bounce(self, source):
		self.collision_timer = self.collision_timer_max

		self.bounce_list = [3,2,2,1,1,2,2,3,3,4,4,3]

		#if abs(self.rect.centerx - source.rect.centerx) < 18:
		if abs(source.rect.centery - self.rect.centery) >= 15:
				self.bounce_list = [3,4,4,5,5,4,4,3,3,2,2,3]

		self.jump_frames = 0

		if source.type == 'Ninja':
			if self.target == None:
				self.target = source
		else:
			if self.rect.centerx <= source.rect.centerx:
				self.target_xy = (0,None)
			else:
				self.target_xy = (640,None)


	def boundary_check(self):
		if options.loop_physics is True:
			if self.rect.bottom < 0 and self.change_y < 0:
				self.rect.top = sprites.size[1]
				self.true_y = self.rect.centery

			if self.rect.top > sprites.size[1] and self.change_y > 0:
				self.rect.bottom = 0
				self.true_y = self.rect.centery

			if self.rect.right < 0 and self.change_x < 0:
				self.rect.left = sprites.size[0]
				self.true_x = self.rect.centerx

			if self.rect.left > sprites.size[0] and self.change_x > 0:
				self.rect.right = 0
				self.true_x = self.rect.centerx

	def ai_update(self):
		self.ai_timer += 1

		if self.target != None:
			if self.target.visible == 0:
				self.target = None
				if self.direction == 'left':
					self.target_xy = (0,None)
				elif self.direction == 'right':
					self.target_xy = (640,None)

		if self.ai_timer > 10:
			self.ai_timer = 0

		if self.ai_timer == 0 and self.collision_timer <= 0:
			if self.target == None:
				pass
			else:
				temp_rect = pygame.Rect(-50,self.rect.top - 50, 740, 100 + self.rect.height)
				if temp_rect.colliderect(self.target.rect) == 0:
					self.target = None
					if self.direction == 'left':
						self.target_xy = (0,None)
					elif self.direction == 'right':
						self.target_xy = (640,None)
					#self.target_xy = (random.choice((0,640)), None)

		if self.ai_timer == 5:
			if self.change_x > 0:
				temp_rect = pygame.Rect(self.rect.right,self.rect.centery - 12, 640, 24)
			elif self.change_x < 0:
				temp_rect = pygame.Rect(self.rect.left - 640,self.rect.centery - 12, 640, 24)
			else:
				temp_rect = None
				
			if temp_rect != None:
				ninja_list = None
				for ninja in sprites.ninja_list:
					if ninja.visible == 1:
						if temp_rect.colliderect(ninja.rect):
							dist = self.dist_check(self.rect.center, ninja.rect.center)
							if ninja_list == None or dist < ninja_list[1]:
								ninja_list = (ninja, dist)
				
				if ninja_list != None:
					self.target = ninja_list[0]


		#Check if jumpable gap exists, then take it!
		if self.jump is False:
			if self.current_tile != None:
				if self.max_speed == 1:
					mod = 6
					turn_mod = 8
				else:
					mod = -12
					turn_mod = -4
				if self.change_x > 0:
					if self.rect.centerx >= self.current_tile.rect.centerx + mod:
						if self.current_tile.right_tile_dist != None:
							if self.current_tile.right_tile_dist < 3:
								pass
							elif self.current_tile.right_tile_dist <= 40:
								self.trigger_jump(0)
								if self.change_y != 0:
									self.change_y = 0
							else:
								if self.rect.centerx >= self.current_tile.rect.centerx + turn_mod:
									self.target = None
									self.target_xy = (0,None)
						else:
							if self.rect.centerx >= self.current_tile.rect.centerx + turn_mod:
								self.target = None
								self.target_xy = (0,None)

				elif self.change_x < 0:
					if self.rect.centerx <= self.current_tile.rect.centerx - mod:
						if self.current_tile.left_tile_dist != None:
							if self.current_tile.left_tile_dist < 3:
								pass
							elif self.current_tile.left_tile_dist <= 40:
								self.trigger_jump(0)
								if self.change_y != 0:
									self.change_y = 0
							else:
								if self.rect.centerx <= self.current_tile.rect.centerx - turn_mod:
									self.target = None
									self.target_xy = (640,None)
						else:
							if self.rect.centerx <= self.current_tile.rect.centerx - turn_mod:
								self.target = None
								self.target_xy = (640,None)

	
	def follow_target(self):
		if self.target != None:
			self.target_xy = self.target.rect.center

			
		if self.collision_timer <= 0:
			if self.direction == 'right':	
				if self.change_x < self.max_speed:
					self.change_x += self.accel
				if self.rect.centerx > self.target_xy[0] + 10:
					self.direction = 'left'
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]
					
			else:
				if self.change_x > -self.max_speed:
					self.change_x -= self.accel
				if self.rect.centerx < self.target_xy[0] - 10:
					self.direction = 'right'
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]

			if self.inverted_g is False:
				if self.direction == 'left' and self.change_x > 0:
					sprites.particle_generator.slide_particles((self.rect.right - 5, self.rect.bottom), 'right', self.inverted_g)
				elif self.direction == 'right' and self.change_x < 0:
					sprites.particle_generator.slide_particles((self.rect.left + 5, self.rect.bottom), 'left', self.inverted_g)
			else:
				if self.direction == 'left' and self.change_x > 0:
					sprites.particle_generator.slide_particles(self.rect.topright, 'right', self.inverted_g)
					#self.bounce_list.append(4)
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]
				elif self.direction == 'right' and self.change_x < 0:
					sprites.particle_generator.slide_particles(self.rect.topleft, 'left', self.inverted_g)
					self.bounce_list = [4,4,4,5,5,5,5,5,4,4,4,4,4,3]
			
			#jump into target if close
			if self.target != None and self.jump is False:
				i = 0
				if self.direction == 'left' and self.change_x < 0:
					if self.target.change_x > 0:
						i = self.target.change_x * 10
					temp_rect = pygame.Rect(self.rect.left - 50 - i, self.rect.top, 50 + i, 24)
					if self.target.rect.colliderect(temp_rect):
						self.trigger_jump(4)
				elif self.direction == 'right' and self.change_x > 0:
					if self.target.change_x < 0:
						i = self.target.change_x * 10
					temp_rect = pygame.Rect(self.rect.right, self.rect.top, 50 + i, 24)
					if self.target.rect.colliderect(temp_rect):
						self.trigger_jump(4)


class Wheel_Eye(pygame.sprite.DirtySprite):
	def __init__(self, wheel, variant):
		pygame.sprite.DirtySprite.__init__(self)

		self.wheel = wheel
		
		self.image_list = [] #Left is 0, Right is 8, middle is 4
		image = sprites.enemy_sheet.getImage(25, 305, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(34, 305, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(43, 305, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(52, 305, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(61, 305, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(25, 314, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(34, 314, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(43, 314, 8, 8)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(52, 314, 8, 8)
		self.image_list.append(image)

		self.image_target = 4
		self.image_number = 4
		self.frame_counter = 0
		self.image = self.image_list[self.image_number]

		self.rect = self.image.get_rect()
		self.rect.centerx = self.wheel.rect.centerx
		self.rect.centery = self.wheel.rect.centery

		self.inverted_g = False

		self.variant = variant
		if self.variant == 'laser':
			for image in self.image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace((93,88,114),options.RED_LIST[1])
				array.replace((50,49,57),options.RED_LIST[0])
				#array.replace((241,239,253),options.RED_LIST[3])
				array.close()
				image.unlock()

			self.big_image_list = []
			self.laser = ninja.Projectile_Sprite(self, 0)
			for image in self.laser.image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace(options.BLUE_LIST[0], options.RED_LIST[0])
				array.replace(options.BLUE_LIST[1], options.RED_LIST[1])
				array.replace(options.BLUE_LIST[2], options.RED_LIST[2])
				array.replace(options.BLUE_LIST[3], options.RED_LIST[3])
				array.close()
				image.unlock()

			self.laser_counter = 250
			self.color = options.RED_LIST

		'''
		#the following serves some function, but mostly just replicates ninja.
		self.direction = direction
		self.status = direction
		self.big_image_list = []
		self.inverted_g = False
		self.loop_physics = False
		'''

		layer = sprites.active_sprite_list.get_layer_of_sprite(self.wheel)
		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self)
		
		sprites.active_sprite_list.change_layer(self, layer)

		self.death_type = 'crumble'

		self.status = 'idle'
		self.fire_timer = 180

	def update(self):
		if self.variant == 'laser':
			#trigger fire and lock eye
			if self.status == 'idle':
				if self.wheel.target != None:
					self.fire_timer -= 1
					if self.fire_timer <= 0:
						if self.image_number in (0,8):
							self.status = 'fire'
							self.laser_counter = 56


			if self.status == 'fire':
				self.laser_counter -= 1
				if self.laser_counter > 15 and self.laser_counter < 55:
					if self.image_number == 0:
						i = (self.rect.left,self.rect.centery)
						self.direction = 'left'
					elif self.image_number == 8:
						i = (self.rect.right,self.rect.centery)
						self.direction = 'right'
					sprites.particle_generator.wheel_laser_charge_particles(i, self, self.direction)
				if self.laser_counter == 0:
					self.loop_physics = options.loop_physics
					self.laser.fire_sensor_laser(self.direction)
					if self.image_number == 0:
						i = (self.rect.left,self.rect.centery)
					elif self.image_number == 8:
						i = (self.rect.right,self.rect.centery)
					sprites.particle_generator.wheel_laser_fire_particles(i, self, self.direction)
					self.status = 'idle'
					self.fire_timer = 180
				
		
		self.dirty = 1
		self.rect.centerx = self.wheel.rect.centerx

		if self.inverted_g is False:
			self.rect.centery = self.wheel.rect.centery + self.wheel.dict_number - 1
		else:
			self.rect.centery = self.wheel.rect.centery - self.wheel.dict_number

		if self.wheel.target_xy[0] < self.rect.centerx:
			self.image_target = 0
		else:
			self.image_target = 8

		if self.image_number != self.image_target and self.status == 'idle':
			self.frame_counter += 1
			if self.frame_counter >= 3:
				self.frame_counter = 0
				if self.image_number < self.image_target:
					self.image_number +=1
				else:
					self.image_number -= 1
				if self.inverted_g is False:
					self.image = self.image_list[self.image_number]
				else:
					self.image = pygame.transform.flip(self.image_list[self.image_number], False, True)

		else:
			self.frame_counter = 0









class Waterfall(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, layer, rect, tile_split, inverted = False, fix_edges = True):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'waterfall'

		self.tile_split = tile_split

		self.inverted = inverted
		self.fix_edges = fix_edges

		self.image_list = []
		image1 = pygame.Surface((rect[2], rect[3]))
		x = 0
		y = 00
		
		#If wanting mystic cavers to have different falls
		if tile_split is True:
			pic = sprites.level_sheet.getImage(433, 272, 24, 24)
		elif tile_split == 'classic':
			pic = sprites.level_sheet.getImage(458, 272, 24, 24)
		else:
			pic = sprites.level_sheet.getImage(540, 272, 24, 24)
		
		#pic = sprites.level_sheet.getImage(433, 272, 24, 24)
		
		while x < image1.get_width():
			while y < image1.get_height():
				image1.blit(pic, (x,y))
				y += pic.get_height()
			x += pic.get_width()
			y = 0
		self.image_list.append(image1)

		while len(self.image_list) <= 11:
			image = pygame.Surface((rect[2], rect[3]))
			x = 0
			y = 0
			temp_pic = pygame.Surface((24,24))
			temp_pic.blit(pic,(0,2),area=(0,0,24,22))
			#blit(source, dest, area=None, 
			temp_pic.blit(pic,(0,0),area=(0,22,24,2))
			pic = temp_pic
			while x < image.get_width():
				while y < image.get_height():
					image.blit(pic, (x,y))
					y += pic.get_height()
				x += pic.get_width()
				y = 0
			self.image_list.append(image)

		if self.inverted is True:
			temp_list = []
			for image in self.image_list:
				i = pygame.transform.flip(image,True,True)
				temp_list.append(i)
			self.image_list = temp_list

		self.image_number = 0
		self.frame_number = 0
		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		self.rect.x = rect[0]
		self.rect.y = rect[1]


		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		#sprites.background_objects.add(self)
		sprites.tile_list.add(self)

		self.splash1 = sprites.level_sheet.getImage(433, 297, 24, 10)
		self.splash2 = sprites.level_sheet.getImage(458, 297, 24, 10)
		self.splash3 = sprites.level_sheet.getImage(483, 297, 24, 10)
		self.splash4 = sprites.level_sheet.getImage(508, 297, 24, 10)

		if tile_split != False:
			self.mallow_splash = Waterfall_Mallow_Splash(self)

		self.dirty = 1

		self.image_number = 0
		self.frame_counter = 0

		if tile_split != False:
			self.tile_physics()
			self.top_splash()

		self.log_list = []


	def set_top_particles(self):
		if self.rect.width > 40:
			i = 0

			if options.particles == 'High':
				density = self.rect.width / 10
			elif options.particles == 'Low':
				density = self.rect.width / 20
			else:
				density = 0

			while i < density:
				if self.inverted is False:
					particlexy = (self.rect.left + random.randrange(0,self.rect.width,1),self.rect.top - random.randrange(0,10,1))
					sprites.particle_generator.waterfall_top_particles(particlexy, self.rect.top, (self.rect.left,self.rect.right), self)
				else:
					particlexy = (self.rect.left + random.randrange(0,self.rect.width,1),self.rect.bottom + random.randrange(0,10,1))
					sprites.particle_generator.waterfall_top_particles(particlexy, self.rect.bottom, (self.rect.left,self.rect.right), self)
				i += 1

	def update(self):
		self.frame_counter += 1
		if self.frame_counter >= 4:
			self.frame_counter = 0
			self.image_number += 1
			for log in self.log_list:
				log.falls_update()
			if self.image_number >= len(self.image_list):
				self.image_number = 0

			self.image = self.image_list[self.image_number]
			self.dirty = 1

	def top_splash(self):
		#NO LONGER USING TOP SPLASH
		splash_list = [self.splash1, self.splash2, self.splash3, self.splash4]
		
		if self.inverted is False:
			y = 0
		else:
			y = self.rect.height - 1
		for image in self.image_list:
			x = 0
			while x < image.get_width():
				i = random.randrange(0,5,1)
				pygame.draw.line(image, (options.LIGHT_PURPLE),(x,y),(x+i,y),1)
				i += random.randrange(1,5,1)
				x += i 

			'''
			pygame.draw.rect(image, (0,255,0), (0,0,image.get_width(),10), 0)
			image.set_colorkey((0,255,0))

			x = 0
			y = 0
			while x < image.get_width():
				pic = random.choice(splash_list)
				image.blit(pic, (x, 0))
				x += pic.get_width()
			'''

				

	def tile_physics(self):
		GREEN = (0,255,0) #transparent colorkey
		for tile in sprites.tile_list:
			if tile.type == 'tile':
				#green_rect = (tile.rect.x, tile.rect.bottom, tile.rect.width, self.rect.bottom - tile.rect.bottom)
				if self.inverted is False:
					if tile.left_open is True and tile.right_open is True:
						green_rect = (tile.rect.x + 2 - self.rect.x, tile.rect.bottom - self.rect.y - 10, tile.rect.width - 4, self.rect.bottom - tile.rect.bottom + 10)

					elif tile.left_open is True and tile.right_open is False:
						green_rect = (tile.rect.x + 2 - self.rect.x, tile.rect.bottom - self.rect.y - 10, tile.rect.width, self.rect.bottom - tile.rect.bottom + 10)

					elif tile.left_open is False and tile.right_open is True:
						green_rect = (tile.rect.x - self.rect.x, tile.rect.bottom - self.rect.y - 10, tile.rect.width - 2, self.rect.bottom - tile.rect.bottom + 10)

					elif tile.left_open is False and tile.right_open is False:
						green_rect = (tile.rect.x - self.rect.x, tile.rect.bottom - self.rect.y - 10, tile.rect.width, self.rect.bottom - tile.rect.bottom + 10)
				else:
					if tile.left_open is True and tile.right_open is True:
						green_rect = (tile.rect.x + 2 - self.rect.x, 0, tile.rect.width - 4, tile.rect.top - self.rect.top + 10)

					elif tile.left_open is True and tile.right_open is False:
						green_rect = (tile.rect.x + 2 - self.rect.x, 0, tile.rect.width, tile.rect.top - self.rect.top  + 10)

					elif tile.left_open is False and tile.right_open is True:
						green_rect = (tile.rect.x - self.rect.x, 0, tile.rect.width - 2, tile.rect.top - self.rect.top  + 10)

					elif tile.left_open is False and tile.right_open is False:
						green_rect = (tile.rect.x - self.rect.x, 0, tile.rect.width, tile.rect.top - self.rect.top  + 10)

				

				if self.rect.colliderect(tile.rect):
					splash_list = [self.splash1, self.splash2, self.splash3, self.splash4,self.splash1, self.splash2, self.splash3, self.splash4,self.splash1, self.splash2, self.splash3, self.splash4]
					for image in self.image_list:
						#if tile.inverted_g is False:
						#	green_rect = (tile.rect.x + 2, tile.rect.bottom, tile.rect.width - 4, self.rect.bottom - tile.rect.bottom)
						#else:
						#	green_rect = (tile.rect.x + 2, tile.rect.top, tile.rect.width - 4, tile.rect.top - self.rect.top)
						pygame.draw.rect(image, (GREEN), green_rect, 0)
						image.set_colorkey(GREEN)

						pic = random.choice(splash_list)
						splash_list.remove(pic)

						if self.inverted is True:
							pic = pygame.transform.flip(pic,True,True)
							image.blit(pic, (tile.rect.left - self.rect.x, tile.rect.bottom - 3 - self.rect.y))
						else:
							image.blit(pic, (tile.rect.left - self.rect.x, tile.rect.top - 6 - self.rect.y))

					for image in self.mallow_splash.image_list:
						pygame.draw.rect(image, (GREEN), (green_rect[0] + 10, 0, green_rect[2], image.get_height()), 0)
						image.set_colorkey(GREEN)

						pygame.draw.rect(image, (GREEN), (0, 0, 10, 10), 0)
						pygame.draw.rect(image, (GREEN), (image.get_width() - 10, 0, 10, 10), 0)

			if tile.type == 'mallow':
				if tile.rect.colliderect(self.rect):
					if tile.rect.top > sprites.size[1] / 2:
						splash_line = tile.rect.top + 3 #where the splash needs to start to get mallow.
						self.mallow_splash.rect.bottom = splash_line
					else:
						splash_line = tile.rect.bottom - 3 #where the splash needs to start to get mallow.
						self.mallow_splash.rect.top = splash_line

		if self.fix_edges is True:
			self.mallow_splash.fix_edges()

class Waterfall_Mallow_Splash(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, waterfall):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'waterfall mallow splash'
		self.waterfall = waterfall
		GREEN = (0,255,0)

		self.image_list = []
		image1 = pygame.Surface((self.waterfall.rect.width + 20, 10))
		image1.fill(GREEN)
		self.image_list.append(image1)
		image2 = pygame.Surface((self.waterfall.rect.width + 20, 10))
		image2.fill(GREEN)
		self.image_list.append(image2)
		image3 = pygame.Surface((self.waterfall.rect.width + 20, 10))
		image3.fill(GREEN)
		self.image_list.append(image3)
		image4 = pygame.Surface((self.waterfall.rect.width + 20, 10))
		image4.fill(GREEN)
		self.image_list.append(image4)


				
		x = 5
		while x < sprites.size[0]:
			splash_list = [self.waterfall.splash1, self.waterfall.splash2, self.waterfall.splash3, self.waterfall.splash4]
			for image in self.image_list:
				i = random.choice(splash_list)
				splash_list.remove(i)
				image.blit(i, (x,0))
				pygame.draw.rect(image, (0,255,0), (image.get_width() - 5,0,5,image.get_height()),0)
				image.set_colorkey(GREEN)

			x += i.get_width() 

		if self.waterfall.inverted is True:
			temp_list = []
			for image in self.image_list:
				i = pygame.transform.flip(image,True,True)
				temp_list.append(i)
			self.image_list = temp_list



		self.image_number = 0
		self.frame_counter = 0
		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()
		self.rect.centerx = self.waterfall.rect.centerx
		if self.waterfall.inverted is False:
			self.rect.bottom = self.waterfall.rect.bottom
		else:
			self.rect.top = self.waterfall.rect.top

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 3)
		sprites.background_objects.add(self)

		self.dirty = 1

	def update(self):
		self.frame_counter += 1
		if self.frame_counter >= 6:
			self.frame_counter = 0
			self.dirty = 1
			self.image_number += 1
			if self.image_number >= len(self.image_list):
				self.image_number = 0
			self.image = self.image_list[self.image_number]

	def fix_edges(self):
		circle_list = []
		WHITE = (241,239,253)
		GREEN = (0,255,0)

		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = round(self.rect.height / 2)
		#get circle_x
		last_color = None
		while x <= self.image.get_width() - 1:
			color = self.image.unmap_rgb(array[x,y])
			if last_color != None:
				if color != last_color:
					circle_list.append(x)
			last_color = color
			x += 1

		#take care of potential 'ends'
		x = 0
		color = self.image.unmap_rgb(array[x,y])
		if color == WHITE:
			circle_list.append(x)
		x = self.image.get_width() - 1
		color = self.image.unmap_rgb(array[x,y])
		if color == WHITE:
			circle_list.append(x)

		self.image.unlock()
		
		for x in circle_list:
			radius_mod = 0
			for image in self.image_list:
				if self.waterfall.inverted is True:
					radius = 2 + radius_mod
					pygame.draw.circle(image, WHITE, (x , self.rect.height - 5), radius, 0)
					pygame.draw.circle(image, WHITE, (x , self.rect.height - 7), radius, 0)
					pygame.draw.circle(image, WHITE, (x , self.rect.height - 9), radius, 0)
					radius_mod += 1
				else:
					radius = 2 + radius_mod
					pygame.draw.circle(image, WHITE, (x , 5), radius, 0)
					pygame.draw.circle(image, WHITE, (x , 7), radius, 0)
					pygame.draw.circle(image, WHITE, (x , 9), radius, 0)
					radius_mod += 1

		for image in self.image_list:
			if self.waterfall.tile_split != 'classic':
				pygame.draw.rect(image, options.GREEN, (0, 0, abs(self.rect.left - self.waterfall.rect.left), self.rect.height), 0)
				pygame.draw.rect(image, options.GREEN, (self.rect.width - (abs(self.rect.left - self.waterfall.rect.left)), 0, abs(self.rect.left - self.waterfall.rect.left), self.rect.height), 0)

class Window(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rect, layer, special):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'window'

		self.image_list = []
		self.image = pygame.Surface((rect[2], rect[3]))
		self.rect = self.image.get_rect()
		self.rect.x = rect[0]
		self.rect.y = rect[1]
		if special in ('classic', 'pump'):
			#self.color = (105,91,143)
			self.color = (124,107,168)
		else:
			self.color = (106,193,209)
		self.image.fill(self.color)

		while len(self.image_list) < 4:
			i = self.image.copy()
			self.image_list.append(i)

		self.image_number = 0
		self.frame_counter = 0
		self.image = self.image_list[0]

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)

		if special == 'classic':
			self.build_classic()

		if special == 'pump':
			self.build_pump()

		self.dirty = 1


	def update(self):
		if options.background_effects == 'High':
			self.frame_counter += 1
			if self.frame_counter >= 20:
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number >= len(self.image_list):
					self.image_number = 0
				self.image = self.image_list[self.image_number]
				self.dirty = 1

	def build_classic(self):
		self.build_shadow([sprites.player1.idle_right[0],sprites.player1.idle_right[1],sprites.player1.idle_right[2], sprites.player1.idle_right[1]], (45,72))
		self.build_shadow([sprites.player1.idle_right[1],sprites.player1.idle_right[2],sprites.player1.idle_right[0], sprites.player1.idle_right[2]], (15,62))

		self.build_shadow([sprites.player1.idle_right[0],sprites.player1.idle_right[1],sprites.player1.idle_right[2], sprites.player1.idle_right[1]], (self.rect.width - 69,72))
		self.build_shadow([sprites.player1.idle_right[1],sprites.player1.idle_right[2],sprites.player1.idle_right[0], sprites.player1.idle_right[2]], (self.rect.width - 39,62))

		self.build_shadow([sprites.player1.idle_right[0],sprites.player1.idle_right[1],sprites.player1.idle_right[2], sprites.player1.idle_right[1]], (127,72))
		self.build_shadow([sprites.player1.idle_right[1],sprites.player1.idle_right[2],sprites.player1.idle_right[0], sprites.player1.idle_right[2]], (157,52))
		self.build_shadow([sprites.player1.idle_right[2],sprites.player1.idle_right[0],sprites.player1.idle_right[1], sprites.player1.idle_right[0]], (187,62))

		self.build_shadow([sprites.player1.idle_right[0],sprites.player1.idle_right[1],sprites.player1.idle_right[2], sprites.player1.idle_right[1]], (self.rect.width - 24 - 127,62))
		self.build_shadow([sprites.player1.idle_right[1],sprites.player1.idle_right[2],sprites.player1.idle_right[0], sprites.player1.idle_right[2]], (self.rect.width - 24 - 157,57))
		self.build_shadow([sprites.player1.idle_right[2],sprites.player1.idle_right[0],sprites.player1.idle_right[1], sprites.player1.idle_right[0]], (self.rect.width - 24 - 187,72))

		pic = pygame.Surface((140,100))
		pic.fill((0,0,0))
		for image in self.image_list:
			image.blit(pic, ((self.rect.width / 2) - pic.get_width() / 2,0))

		#self.build_shadow([pic,pic,pic,pic], ((self.rect.width / 2) - pic.get_width() / 2,0))

	def build_pump(self):
		pic1 = sprites.enemy_sheet.getImage(0,0, 157, 59)
		pic2 = sprites.enemy_sheet.getImage(0,60, 157, 59)
		self.build_shadow([pic1,pic2,pic1,pic2], (0,0))

		#pic = pygame.Surface((140,100))
		#pic.fill((0,0,0))
		#for image in self.image_list:
		#	image.blit(pic, ((self.rect.width / 2) - pic.get_width() / 2,0))
		

	def build_shadow(self, pic_list, xy): #creates dark shadow inside window
		counter = 0
		pic_list = pic_list.copy()
		while len(pic_list) > 0:
			ninja_pic = pic_list[0].copy()
			del pic_list[0]
			ninja_pic.lock()
			array = pygame.PixelArray(ninja_pic)
			x = 0
			y = 0
			while y <= ninja_pic.get_height() - 1:
				x = 0
				while x <= ninja_pic.get_width() - 1:
					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):
						r = self.color[0] - 20
						g = self.color[1] - 30
						b = self.color[2] - 20

						
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
						

						array[x,y] = (r,g,b)

					x += 1
				y += 1

			array.close()
			ninja_pic.unlock()

			self.image_list[counter].blit(ninja_pic, (xy))
			counter += 1


class Cloud(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, layer_list, startx, starty, speed, sprite_rect, y_range):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'cloud'

		self.y_range = y_range
		self.starty = starty
		self.layer_list = layer_list

		self.image = sprites.level_sheet.getImage(sprite_rect[0], sprite_rect[1], sprite_rect[2], sprite_rect[3])
		self.rect = self.image.get_rect()
		self.rect.x = startx
		self.rect.y = starty

		self.change_x = speed

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, self.layer_list[0])
		sprites.background_objects.add(self)

		self.dirty = 1

		self.frame_counter = 0
		self.true_x = self.rect.x

	def update(self):
		self.frame_counter += 1
		#if self.frame_counter >= 3:
		self.frame_counter = 0
		self.true_x += self.change_x
		self.rect.x = round(self.true_x)
		self.dirty = 1


		if self.rect.x > sprites.size[0]:
			self.rect.right = 0
			if self.y_range != None:
				i = random.randrange(-self.y_range, self.y_range, 1)
				self.rect.centery = self.starty + i
			layer = random.choice(self.layer_list)
			sprites.active_sprite_list.change_layer(self, layer)
			self.true_x = self.rect.x


class Light_Source(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, background_surface, size, centerx, centery, style):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.surface = background_surface
		self.surface.image.set_colorkey(None)

		self.layer = sprites.active_sprite_list.get_layer_of_sprite(self.surface) + 1
		self.image_list = []
		self.frame_number = 0
		self.image_number = 0

		self.style = style

		self.type = 'light source'

		if self.style == 'dungeon':
			fire1 = sprites.level_sheet.getImage(0, 526,24,31)
			fire2 = sprites.level_sheet.getImage(25, 526,24,31)
			fire3 = sprites.level_sheet.getImage(50, 526,24,31)
			fire4 =	sprites.level_sheet.getImage(75, 526,24,31)
			fire5 =	sprites.level_sheet.getImage(100, 526,24,31)
			fire6 =	sprites.level_sheet.getImage(125, 526,24,31)

			r_mod = [20, 10, 5]
			g_mod = [30,15,8]
			b_mod = [20,10,5]


		elif self.style == 'temple':
			fire4 = sprites.level_sheet.getImage(0, 494,24,31)
			fire5 = sprites.level_sheet.getImage(25, 494,24,31)
			fire6 = sprites.level_sheet.getImage(50, 494,24,31)
			fire1 =	sprites.level_sheet.getImage(75, 494,24,31)
			fire2 =	sprites.level_sheet.getImage(100, 494,24,31)
			fire3 =	sprites.level_sheet.getImage(125, 494,24,31)

			r_mod = [40, 20, 10]
			g_mod = [30,15,8]
			b_mod = [20,10,5]
			

		#get first image:
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery


		self.big_circle = size / 2
		self.med_circle = self.big_circle - 10
		self.small_circle = self.big_circle - 20


		self.image.blit(self.surface.image, (0,0), (self.rect.x,self.rect.y,size,size))

		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.image.get_height() - 1:
			x = 0
			while x <= self.image.get_width() - 1:

				dist =  self.dist_check((size/2, size/2), (x,y))
				if dist <= self.small_circle: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):

						r = color[0] + r_mod[0]
						g = color[1] + g_mod[0]
						b = color[2] + b_mod[0]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				elif dist <= self.med_circle: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[1]
						g = color[1] + g_mod[1]
						b = color[2] + b_mod[1]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				elif dist <= self.big_circle: #calculate cicle based on rect size

					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[2]
						g = color[1] + g_mod[2]
						b = color[2] + b_mod[2]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				else:
					array[x,y] = (0,255,0)

				x += 1
			y += 1

		array.close()
		self.image.unlock()

		#self.image.set_colorkey((0,255,0))
		#self.image.blit(fire1, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 12))

		temp_image1 = self.image.copy()
		temp_image2 = self.image.copy()
		temp_image3 = self.image.copy()
		#self.image_list.append(image)


		#get second image!
		self.image.blit(self.surface.image, (0,0), (self.rect.x,self.rect.y,size,size))

		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.image.get_height() - 1:
			x = 0
			while x <= self.image.get_width() - 1:

				dist =  self.dist_check((size/2, size/2), (x,y))
				if dist <= self.small_circle - 1: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[0]
						g = color[1] + g_mod[0]
						b = color[2] + b_mod[0]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				elif dist <= self.med_circle - 1: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[1]
						g = color[1] + g_mod[1]
						b = color[2] + b_mod[1]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				elif dist <= self.big_circle - 1: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[2]
						g = color[1] + g_mod[2]
						b = color[2] + b_mod[2]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				else:
					array[x,y] = (0,255,0)

				x += 1
			y += 1

		self.image.set_colorkey((0,255,0))
		self.surface.image.set_colorkey((0,255,0))

		array.close()
		self.image.unlock()
		#self.image.blit(fire2, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 12))

		temp_image4 = self.image.copy()
		temp_image5 = self.image.copy()
		temp_image6 = self.image.copy()
		image = self.image.copy()
		
		temp_image1.set_colorkey((0,255,0))
		temp_image1.blit(fire1, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 15))
		self.image_list.append(temp_image1)

		temp_image2.set_colorkey((0,255,0))
		temp_image2.blit(fire2, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 15))
		self.image_list.append(temp_image2)

		temp_image3.set_colorkey((0,255,0))
		temp_image3.blit(fire3, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 15))
		self.image_list.append(temp_image3)

		temp_image4.set_colorkey((0,255,0))
		temp_image4.blit(fire4, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 15))
		self.image_list.append(temp_image4)

		temp_image5.set_colorkey((0,255,0))
		temp_image5.blit(fire5, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 15))
		self.image_list.append(temp_image5)

		temp_image6.set_colorkey((0,255,0))
		temp_image6.blit(fire6, ((self.rect.width / 2) - 12, (self.rect.height / 2) - 15))
		self.image_list.append(temp_image6)
		
		#self.image_list.append(image)

		#self.image = self.image_list[0]




		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, self.layer)
		sprites.background_objects.add(self)

		self.dirty = 1

		self.image_change_var = 1

		self.change_x = 0 #used for particle guide
		self.change_y = 0 #used for particle guide

	def dist_check(self, point1, point2):
		distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
		return distance

	def update(self):
		self.frame_number += 1
		if self.frame_number > 4:
			self.image_number += self.image_change_var
			if self.image_number > len(self.image_list) - 1:
				self.image_number = 0
			#if self.image_number == len(self.image_list) - 1:
			#	self.image_change_var *= -1
			#elif self.image_number == 0:
			#	self.image_change_var *= -1
			self.frame_number = 0

			self.image = self.image_list[self.image_number]
			self.dirty = 1

		i = random.choice((1,2,3,4,5,6,7,8))
		if i == 3:
			sprites.particle_generator.torch_particles(self, self.style)

class Electric_Light_Source(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, background_surface, size, centerx, centery, style, flicker = False):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.surface = background_surface
		self.surface.image.set_colorkey(None)

		self.layer = sprites.active_sprite_list.get_layer_of_sprite(self.surface) + 1
		self.image_list = []
		self.frame_number = 0
		self.image_number = 0

		self.style = style

		self.type = 'light source'

		if self.style == 'secret lab':

			image_on = sprites.level_sheet.getImage(242, 305, 24, 24)
			image_on.set_colorkey(options.GREEN)


			image_off = sprites.level_sheet.getImage(242, 330, 24, 24)
			image_off.set_colorkey(options.GREEN)

			r_mod = [20, 15, 10]
			g_mod = [15,10,5]
			b_mod = [15,10,5]

		

		#get first image:
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery


		self.big_circle = size / 2
		self.med_circle = self.big_circle - 10
		self.small_circle = self.big_circle - 20


		self.image.blit(self.surface.image, (0,0), (self.rect.x,self.rect.y,size,size))
		self.image_off = self.image.copy()

		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.image.get_height() - 1:
			x = 0
			while x <= self.image.get_width() - 1:

				dist =  self.dist_check((size/2, size/2), (x,y))
				if dist <= self.small_circle: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):

						r = color[0] + r_mod[0]
						g = color[1] + g_mod[0]
						b = color[2] + b_mod[0]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				elif dist <= self.med_circle: #calculate cicle based on rect size
					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[1]
						g = color[1] + g_mod[1]
						b = color[2] + b_mod[1]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				elif dist <= self.big_circle: #calculate cicle based on rect size

					color = self.image.unmap_rgb(array[x,y])

					if color != (0,255,0):

						r = color[0] + r_mod[2]
						g = color[1] + g_mod[2]
						b = color[2] + b_mod[2]

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)
				else:
					array[x,y] = (0,255,0)

				x += 1
			y += 1

		array.close()
		self.image.unlock()

		self.image.blit(image_on, ((self.rect.width / 2) - (image_on.get_width() / 2),(self.rect.height / 2) - (image_on.get_height() / 2)))
		self.image.set_colorkey(options.GREEN)
		self.image_on = self.image.copy()
		self.image_on.set_colorkey(options.GREEN)
		self.image_off.blit(image_off, ((self.rect.width / 2) - (image_off.get_width() / 2),(self.rect.height / 2) - (image_off.get_height() / 2)))
		self.image_off.set_colorkey(options.GREEN)

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, self.layer)
		sprites.background_objects.add(self)

		self.dirty = 1

		self.frame_counter = 0
		self.status = 'on'
		if flicker is False:
			self.status = 'always on' #skips updates

		self.change_x = 0 #used for particle guide
		self.change_y = 0 #used for particle guide

	def dist_check(self, point1, point2):
		distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
		return distance

	def update(self):
		if self.status == 'on':
			i = random.randrange(1,60 * 5,1)
			if i == 10:
				self.status = 'off'
				self.frame_counter = 0

		if self.status == 'off':
			self.frame_counter += 1
			if self.frame_counter > 20:
				i = random.randrange(0,10,1)
				if i == 5:
					self.frame_counter = 0
					self.status = 'on'
					self.image = self.image_on
					self.dirty = 1
			else:
				i = random.choice((1,2,3,4,5))
				if i in (1,2):
					self.image = self.image_off
					self.dirty = 1
				else:
					self.image = self.image_on
					self.dirty = 1
		

class Classic_Door(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, xy, layer, enemy_list):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		
		self.type = 'classic_door'

		self.image = sprites.level_sheet.getImage(131, 357, 136, 136)
		self.rect = self.image.get_rect()
		self.rect.x = xy[0]
		self.rect.y = xy[1]

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer - 1)
		sprites.background_objects.add(self)

		self.top_door = Classic_Door_Top((263,23),layer, self)
		self.bottom_door = Classic_Door_Bottom((263,73),layer, self)

		self.status = 'closed'
		self.timer = 600

		self.enemy_list = enemy_list
		self.spawn_timer = 90


	def update(self):

		if self.enemy_list != None:
			if self.status == 'spawn':
				self.spawn_timer -= 1
				if self.spawn_timer == 30:
						if len(sprites.enemy_list) < 6:
							self.spawn_enemy()
				if self.spawn_timer == 0:
					self.spawn_timer = 90
					self.timer = 600
					self.status = 'closed'
					self.top_door.direction = 'close'
					self.bottom_door.direction = 'close'

			else:
				self.timer -= 1
				if self.timer <= 0:
					self.timer = 600
					if self.status == 'closed':
						self.status = 'opened'
						self.top_door.direction = 'open'
						self.bottom_door.direction = 'open'
					elif self.status == 'opened':
						self.status = 'closed'
						self.top_door.direction = 'close'
						self.bottom_door.direction = 'close'


	def spawn_enemy(self):
		if len(self.enemy_list) == 0:
			enemy_type = self.enemy_list[0]
		else:
			enemy_type = random.choice(self.enemy_list)

		if enemy_type == 'wheel':
			self.enemy = Wheel_Enemy((self.rect.centerx,self.rect.centery), None)
			self.enemy.jump_frames = 4
			if self.enemy.direction == 'left':
				self.enemy.change_x = -1
			else:
				self.enemy.change_x = 1
			self.enemy.change_y = self.enemy.jump_force

		elif enemy_type == 'laser wheel':
			self.enemy = Wheel_Enemy((self.rect.centerx,self.rect.centery), 'laser')
			self.enemy.jump_frames = 4
			if self.enemy.direction == 'left':
				self.enemy.change_x = -1
			else:
				self.enemy.change_x = 1
			self.enemy.change_y = self.enemy.jump_force

		elif enemy_type == 'slime':
			self.enemy = Slime_Enemy((self.rect.centerx,self.rect.centery))
			self.enemy.jump()
			enemy_message = 'slm' + ',' + str(self.rect.centerx) + ',' + str(self.rect.centery) + ',' + str(self.enemy.change_x) + ',' + str(self.enemy.change_y) + ',' + self.enemy.direction + ',' + str(self.enemy.jump_frames)

		elif enemy_type == 'volcanic slime':
			self.enemy = Slime_Enemy((self.rect.centerx,self.rect.centery), subtype = 'lava')
			self.enemy.jump()
			enemy_message = 'vslm' + ',' + str(self.rect.centerx) + ',' + str(self.rect.centery) + ',' + str(self.enemy.change_x) + ',' + str(self.enemy.change_y) + ',' + self.enemy.direction + ',' + str(self.enemy.jump_frames)



class Classic_Door_Top(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, xy, layer, door):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.image = sprites.level_sheet.getImage(268, 424, 116, 69)
		
		self.type = 'classic_door_top'

		self.door = door

		self.rect = self.image.get_rect()
		self.rect.x = xy[0]
		self.rect.y = xy[1]
		self.true_y = self.rect.y

		self.closed = self.rect.bottom
		self.open = self.rect.top

		self.change_y = 0.2
		self.direction = 'idle'

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)

	def update(self):
		self.dirty = 1
		if self.direction == 'open':
			self.dirty = 1
			self.true_y -= self.change_y
			self.rect.y = round(self.true_y)
			if self.rect.bottom <= self.open:
				self.direction = 'idle'
				self.door.status = 'spawn'

		elif self.direction == 'close':
			self.dirty = 1
			self.true_y += self.change_y
			self.rect.y = round(self.true_y)
			if self.rect.bottom >= self.closed:
				self.direction = 'idle'

class Classic_Door_Bottom(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, xy, layer, door):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		
		self.type = 'classic_door_bottom'
		self.door = door

		self.image = sprites.level_sheet.getImage(14, 425, 116, 68)
		self.rect = self.image.get_rect()
		self.rect.x = xy[0]
		self.rect.y = xy[1]
		self.true_y = self.rect.y

		self.closed = self.rect.top
		self.open = self.rect.bottom

		self.change_y = 0.2
		self.direction = 'idle'

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)

	def update(self):
		if self.direction == 'open':
			self.dirty = 1
			self.true_y += self.change_y
			self.rect.y = round(self.true_y)
			if self.rect.y >= self.open:
				self.direction = 'idle'
				self.door.status = 'spawn'

		elif self.direction == 'close':
			self.dirty = 1
			self.true_y -= self.change_y
			self.rect.y = round(self.true_y)
			if self.rect.y <= self.closed:
				self.direction = 'idle'


class Mallow_Alarm(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, centerx, centery, layer, mallow, source_alarm):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.mallow = mallow
		self.source_alarm = source_alarm

		self.online_key = 0


		self.image_list = []
		self.frame_number = 0
		self.image_number = 0

		self.base_image = sprites.level_sheet.getImage(131, 242, 41, 41)
		size = 41

		#RED
		base_color = (0,0,0)
		end_color = (175,37,50)

		#PURPLE
		end_color = (125,92,220)

		
		red_multiplier = (end_color[0] - base_color[0]) / 10
		green_multiplier = (end_color[1] - base_color[1]) / 10
		blue_multiplier = (end_color[2] - base_color[2]) / 10

		i = 0
		while i < 10:
			i += 1
			image = self.base_image.copy()
			image.lock()
			array = pygame.PixelArray(image)
			x = 0
			y = 0
			while y <= image.get_height() - 1:
				x = 0
				while x <= image.get_width() - 1:
					color = image.unmap_rgb(array[x,y])
					if color == base_color:

						r = base_color[0] + (i * red_multiplier)
						g = base_color[1] + (i * green_multiplier)
						b = base_color[2] + (i * blue_multiplier)

						if r > 255:
							r = 255
						if g > 255:
							g = 255
						if b > 255:
							b = 255

						array[x,y] = (r,g,b)

					x += 1
				y += 1

			array.close()
			image.unlock()

			image.set_colorkey((0,255,0))
			self.image_list.append(image)



		#add two more of bright red:
		#self.image_list.append(image)
		#self.image_list.append(image)
		
		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)

		self.flip_mod = 1

		self.dirty = 1

		if self.mallow != None:
			self.mallow_countdown = 300
			self.status = 'idle'
			self.off_switch = False
			self.mallow.alarm = self

		self.last_image_number = -1000

	def update(self):
		if self.mallow != None:
			if sprites.countdown_timer.done is True:
				if self.status == 'idle':
						self.mallow_countdown -= 1

						if self.mallow_countdown <= 0:
							self.status = 'active'
							self.mallow_countdown = 600
							

				
				elif self.status == 'active':
					self.frame_number += 1
					if self.frame_number > 6:
						self.image_number += (1 * self.flip_mod)
						if self.image_number >= len(self.image_list):
							self.image_number = len(self.image_list) - 1
							self.flip_mod *= -1
						elif self.image_number < 0:
							self.image_number = 1
							self.flip_mod *= -1
							if self.off_switch is True:
								self.off_switch = False
								self.status = 'idle'
								self.image_number = 0
						self.frame_number = 0

						self.image = self.image_list[self.image_number]
						self.dirty = 1

		#just copies other alarm
		else:
			self.image_number = self.source_alarm.image_number
			if self.image_number != self.last_image_number:
				self.dirty = 1
				self.last_image_number = self.image_number
				self.image = self.image_list[self.image_number]


class Glass_Reflection(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rect, layer, color):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.Surface((rect[2],rect[3]))
		self.image.fill(color)
		self.image.set_alpha(150)
		self.rect = self.image.get_rect()
		self.rect.x = rect[0]
		self.rect.y = rect[1]

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)
		self.dirty = 1




class Level_Background(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, layer, image_name):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'level background'

		if isinstance(image_name,tuple):
			self.image = pygame.Surface((sprites.size[0],sprites.size[1]))
			self.image.fill(image_name)
		else:
			self.image = pygame.image.load(os.path.join(Current_Path, image_name)).convert()
		

		self.rect = self.image.get_rect()
		self.image.set_colorkey((0,255,0))

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)

		self.dirty = 1


class Animated_Background(pygame.sprite.DirtySprite): #moving platform
	#you can jump up through platforms
	def __init__(self, layer,image_list, level):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'animated background'
		self.image_list = []
		self.image_number = 0
		self.frame_counter = 2
		self.image_direction = 1
		self.level = None

		i = 0
		while i <= len(image_list) - 1:
			image = pygame.image.load(os.path.join(Current_Path, image_list[i])).convert()
			image.set_colorkey(options.GREEN)
			self.image_list.append(image)
			i += 1

		if level == 'crucible':
			image = pygame.Surface((640,360))
			image.fill(options.GREEN)
			image.set_colorkey(options.GREEN)
			self.image_list.insert(0,image)
			self.level = level

		if level == 'paradox':
			self.level = level



		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		sprites.background_objects.add(self)

		self.dirty = 1


	def update(self):
		if self.level == 'crucible':
			self.frame_counter -= 1
			if self.frame_counter == 0:

				self.image_number += self.image_direction
				if self.image_number < 0:
					self.image_number = 0
					self.image_direction *= -1
				elif self.image_number >= len(self.image_list):
					self.image_number = len(self.image_list) - 1
					self.image_direction *= -1

				if self.image_number == 0 or self.image_number == len(self.image_list) - 1:	
					self.frame_counter = 15
				else:
					self.frame_counter = 6

				self.image = self.image_list[self.image_number]
				self.dirty = 1

		elif self.level == 'paradox':
			self.frame_counter -= 1
			if self.frame_counter == 0:

				self.image_number += 1
				if self.image_number >= len(self.image_list):
					self.image_number = 0

				self.frame_counter = 10

				self.image = self.image_list[self.image_number]
				self.dirty = 1

class Barrier(pygame.sprite.DirtySprite):
	def __init__(self, rect, direction):
		pygame.sprite.DirtySprite.__init__(self)
		#orientation = 'horizontal' or 'vertical'

		self.type = 'barrier'

		self.direction = direction
		

		#self.image = pygame.Surface((rect[2], rect[3]))
		#self.image.fill(options.BLACK)
		self.rect = pygame.Rect(rect)
		self.rect.x = rect[0]
		self.rect.y = rect[1]


		sprites.level_objects.add(self) #placed here so it is active immediately (before countdown)
		#sprites.active_sprite_list.add(self)

		#self.dirty = 1

	def update(self):
		for ninja in sprites.ninja_list:
			if ninja.rect.colliderect(self.rect):
				if self.direction == 'right':
					ninja.rect.left = self.rect.right
				elif self.direction == 'left':
					ninja.rect.right = self.rect.left
				
				ninja.true_x = ninja.rect.x

		#barrier = Barrier((0,0,7,100),'right')
		#barrier = Barrier((640-7,0,7,100), 'left')

class Gravity_Barrier(pygame.sprite.DirtySprite):
	def __init__(self, orientation, xory, opposite, rect):
		pygame.sprite.DirtySprite.__init__(self)
		#orientation = 'horizontal' or 'vertical'

		self.type = 'gravity_barrier'

		self.orientation = orientation
		self.opposite = opposite #true if the opposite of standard gravity changes.
		self.image_list = []
		self.image_number = 0
		self.frame_counter = 0

		GREEN = (0,255,0)
		
		if self.orientation == 'horizontal':

			image = pygame.Surface((sprites.size[0], 5))
			image.fill(GREEN)
			image.set_colorkey(GREEN)
			image2 = pygame.Surface((sprites.size[0], 5))
			image2.fill(GREEN)
			image2.set_colorkey(GREEN)

			i = sprites.level_sheet.getImage(215, 31, 5, 32)
			i1 = pygame.transform.rotate(i, 90)

			i = sprites.level_sheet.getImage(221, 31, 5, 32)
			i2 = pygame.transform.rotate(i, 90)


			i = 0
			while i < sprites.size[0]:
				image.blit(i1, (i,0))
				image2.blit(i2, (i,0))
				i += 32

			self.image_list.append(image)
			self.image_list.append(image2)

			self.image = self.image_list[0]
			self.rect = self.image.get_rect()

			self.rect.x = 0
			self.rect.centery = xory

			for tile in sprites.tile_list:
				if self.opposite is False:
					if tile.rect.centery < self.rect.centery:
						tile.inverted_g = True
				else:
					if tile.rect.centery > self.rect.centery:
						tile.inverted_g = True

			

		if self.orientation == 'vertical':
			image = pygame.Surface((5, sprites.size[1]))
			image.fill(GREEN)
			image.set_colorkey(GREEN)
			image2 = pygame.Surface((5, sprites.size[1]))
			image2.fill(GREEN)
			image2.set_colorkey(GREEN)
			i1 = sprites.level_sheet.getImage(215, 31, 5, 32)
			i2 = sprites.level_sheet.getImage(221, 31, 5, 32)
			i = 0
			while i < sprites.size[1]:
				image.blit(i1, (0,i))
				image2.blit(i2, (0,i))
				i += 32

			self.image_list.append(image)
			self.image_list.append(image2)

			self.image = self.image_list[0]
			self.rect = self.image.get_rect()
			self.rect.centerx = xory
			self.rect.y = 0

			for tile in sprites.tile_list:
				if self.opposite is False:
					if tile.rect.centerx > self.rect.centerx:
						tile.inverted_g = True
				else:
					if tile.rect.centerx < self.rect.centerx:
						tile.inverted_g = True

		if self.orientation == 'rect':
			#build base surgaces
			image = pygame.Surface((rect[2],rect[3]))
			image.fill(options.GREEN)
			image.set_colorkey(options.GREEN)
			image2 = pygame.Surface((rect[2],rect[3]))
			image2.fill(options.GREEN)
			image2.set_colorkey(options.GREEN)

			#blit vertical vertical lines:
			i1 = sprites.level_sheet.getImage(215, 31, 5, 32)
			i2 = sprites.level_sheet.getImage(221, 31, 5, 32)
			i = 0
			while i < rect[3]:
				image.blit(i1, (0,i))
				image2.blit(i2, (0,i))

				image.blit(i1, (rect[2] - 5,i))
				image2.blit(i2, (rect[2] - 5,i))

				i += 32

			#blit horizontal lines.
			i = sprites.level_sheet.getImage(215, 31, 5, 32)
			i1 = pygame.transform.rotate(i, 90)

			i = sprites.level_sheet.getImage(221, 31, 5, 32)
			i2 = pygame.transform.rotate(i, 90)


			i = 0
			while i < rect[2]:
				image.blit(i1, (i,0))
				image2.blit(i2, (i,0))

				image.blit(i1, (i,rect[3] - 5))
				image2.blit(i2, (i,rect[3] - 5))
				i += 32

			self.image_list.append(image)
			self.image_list.append(image2)

			self.image = self.image_list[0]
			self.rect = self.image.get_rect()
			self.rect.x = rect[0]
			self.rect.y = rect[1]

			for tile in sprites.tile_list:
				if self.opposite is False:
					if self.rect.collidepoint(tile.rect.center): 
						tile.inverted_g = True
				else:
					if self.rect.collidepoint(tile.rect.center) is False:
						tile.inverted_g = True
		

		sprites.gravity_objects.add(self) #placed here so it is active immediately (before countdown)
		sprites.active_sprite_list.add(self)

		self.dirty = 1
	'''		
	def switch_tiles(self):
		for tile in sprites.tile_list:
			if self.orientation == 'vertical':
				if self.opposite is False:
					if tile.rect.centerx < self.rect.centerx:
						tile.inverted_g = True
					else:
						tile.inverted_g = False
				else:
					if tile.rect.centerx > self.rect.centerx:
						tile.inverted_g = True
					else:
						tile.inverted_g = False
			else:
				for tile in sprites.tile_list:
					if self.opposite is False:
						if tile.rect.centery > self.rect.centery:
							tile.inverted_g = True
						else:
							tile.inverted_g = False
					else:
						if tile.rect.centery < self.rect.centery:
							tile.inverted_g = True
						else:
							tile.inverted_g = False
	'''


	def update(self):
		self.frame_counter += 1
		if self.frame_counter >= 12:
			self.frame_counter = 0
			if self.image_number == 0:
				self.image_number = 1
			else:
				self.image_number = 0
			self.image = self.image_list[self.image_number]
			self.dirty = 1

		if self.orientation == 'rect':
				if self.opposite is False:
					for ninja in sprites.ninja_list:
						if self.rect.collidepoint(ninja.rect.center):
							if ninja.inverted_g is True and ninja.status == 'metal pound':
								ninja.status = 'duck'
							ninja.inverted_g = False
						else:
							if ninja.inverted_g is False and ninja.status == 'metal pound':
								ninja.status = 'duck'
							ninja.inverted_g = True

					for sprite in sprites.gravity_effects:
						if self.rect.collidepoint(sprite.rect.center):
							sprite.invert_g(False)
						else:
							sprite.invert_g(True)
						

					

					for item in sprites.active_items:
						if self.rect.collidepoint(item.rect.center):
							item.inverted_g = False
						else:
							item.inverted_g = True

					for enemy in sprites.enemy_list:
						if self.rect.collidepoint(enemy.rect.center):
							enemy.inverted_g = not enemy.inverted_g
						for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g


					for particle in sprites.active_particle_list:
						if self.rect.collidepoint(particle.rect.center):
							if particle.inverted_g is True:
								particle.normal_g()
						else:
							if particle.inverted_g is False:
								particle.invert_g()

				else: #self.opposite is True
					for ninja in sprites.ninja_list:
						if self.rect.collidepoint(ninja.rect.center):
							if ninja.inverted_g is False and ninja.status == 'metal pound':
								ninja.status = 'duck'
							ninja.inverted_g = True
						else:
							if ninja.inverted_g is True and ninja.status == 'metal pound':
								ninja.status = 'duck'
							ninja.inverted_g = False

					for sprite in sprites.gravity_effects:
						if self.rect.collidepoint(sprite.rect.center):
							sprite.invert_g(True)
						else:
							sprite.invert_g(False)

					for item in sprites.active_items:
						if self.rect.collidepoint(item.rect.center):
							item.inverted_g = True
						else:
							item.inverted_g = False

					for enemy in sprites.enemy_list:
						if self.rect.collidepoint(enemy.rect.center):
							enemy.inverted_g = True
						else:
							enemy.inverted_g = False

						for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g

					for particle in sprites.active_particle_list:
						if self.rect.collidepoint(particle.rect.center):
							if particle.inverted_g is False:
								particle.invert_g()
						else:
							if particle.inverted_g is True:
								particle.normal_g()

		elif self.orientation == 'vertical':
				if self.opposite is False:
					for ninja in sprites.ninja_list:
						if ninja.rect.centerx <= self.rect.centerx:
							ninja.inverted_g = False
						else:
							ninja.inverted_g = True

					for sprite in sprites.gravity_effects:
						if sprite.rect.centerx <= self.rect.centerx:
							sprite.invert_g(False)
						else:
							sprite.invert_g(True)

					for item in sprites.active_items:
						if item.rect.centerx <= self.rect.centerx:
							item.inverted_g = False
						else:
							item.inverted_g = True

					for enemy in sprites.enemy_list:
						if enemy.rect.centerx <= self.rect.centerx:
							enemy.inverted_g = False
						else:
							enemy.inverted_g = True

						for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g

					for particle in sprites.active_particle_list:
						if particle.rect.centerx <= self.rect.centerx:
							if particle.inverted_g is True:
								particle.normal_g()
						else:
							if particle.inverted_g is False:
								particle.invert_g()

				else: #self.opposite is True
					for ninja in sprites.ninja_list:
						if ninja.rect.centerx >= self.rect.centerx:
							ninja.inverted_g = False
						else:
							ninja.inverted_g = True

					for sprite in sprites.gravity_effects:
						if sprite.rect.centerx >= self.rect.centerx:
							sprite.invert_g(False)
						else:
							sprite.invert_g(True)

					for item in sprites.active_items:
						if item.rect.centerx >= self.rect.centerx:
							item.inverted_g = False
						else:
							item.inverted_g = True

					for enemy in sprites.enemy_list:
						if enemy.rect.centerx >= self.rect.centerx:
							enemy.inverted_g = False
						else:
							enemy.inverted_g = True

						for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g

					for particle in sprites.active_particle_list:
						if particle.rect.centerx >= self.rect.centerx:
							if particle.inverted_g is True:
								particle.normal_g()
						else:
							if particle.inverted_g is False:
								particle.invert_g()


		
		elif self.orientation == 'horizontal':
			for ninja in sprites.ninja_list:
				if self.opposite is False:
					if ninja.rect.centery > self.rect.centery + 1:
						if ninja.inverted_g is True and ninja.status == 'metal pound':
							ninja.status = 'duck'
						ninja.inverted_g = False
					elif ninja.rect.centery < self.rect.centery - 1:
						if ninja.inverted_g is False and ninja.status == 'metal pound':
							ninja.status = 'duck'

						ninja.inverted_g = True
				else: #self.opposite is True
					if ninja.rect.centery < self.rect.centery - 1:

						if ninja.inverted_g is True and ninja.status == 'metal pound':
							ninja.status = 'duck'

						ninja.inverted_g = False
					elif ninja.rect.centery > self.rect.centery + 1:

						if ninja.inverted_g is False and ninja.status == 'metal pound':
							ninja.status = 'duck'

						ninja.inverted_g = True


			if self.opposite is False:
				for item in sprites.active_items:
					if item.rect.centery >= self.rect.centery:
						item.inverted_g = False
					else:
						item.inverted_g = True

				for sprite in sprites.gravity_effects:
					if sprite.rect.centery >= self.rect.centery:
						sprite.invert_g(False)
					else:
						sprite.invert_g(True)

				

				for enemy in sprites.enemy_list:
					if enemy.rect.centery >= self.rect.centery:
						enemy.inverted_g = False
					else:
						enemy.inverted_g = True

					for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g


				for particle in sprites.active_particle_list:
					if particle.rect.centery > self.rect.centery + 1:
						if particle.inverted_g is True:
							particle.normal_g()
					elif particle.rect.centery < self.rect.centery - 1:
						if particle.inverted_g is False:
							particle.invert_g()


			else:
				for item in sprites.active_items:
					if item.rect.centery <= self.rect.centery:
						item.inverted_g = False
					else:
						item.inverted_g = True

				for sprite in sprites.gravity_effects:
					if sprite.rect.centery <= self.rect.centery:
						sprite.invert_g(False)
					else:
						sprite.invert_g(True)


				for enemy in sprites.enemy_list:
					if enemy.rect.centery <= self.rect.centery:
						enemy.inverted_g = False
					else:
						enemy.inverted_g = True

					for sprite in enemy.subsprite_list:
							sprite.inverted_g = enemy.inverted_g

				for particle in sprites.active_particle_list:
					if particle.rect.centery < self.rect.centery - 1:
						if particle.inverted_g is True:
							particle.normal_g()
					elif particle.rect.centery > self.rect.centery + 1:
						if particle.inverted_g is False:
							particle.invert_g()

	def return_gravity_point(self, point):
		inverted_g = False
		
		if self.orientation == 'rect':
			if self.opposite is False:
				if self.rect.collidepoint(point):
					inverted_g = False
				else:
					inverted_g = True
			else:
				if self.rect.collidepoint(point):
					inverted_g = True
				else:
					inverted_g = False


		elif self.orientation == 'vertical':
			if self.opposite is False:
				if point[0] <= self.rect.centerx:
					inverted_g = False
				else:
					inverted_g = True
			else:
				if point[0] <= self.rect.centerx:
					inverted_g = True
				else:
					inverted_g = False

		elif self.orientation == 'horizontal':
			if self.opposite is False:
				if point[1] > self.rect.centery:
					inverted_g = False
				else:
					inverted_g = True
			else:
				if point[1] > self.rect.centery:
					inverted_g = True
				else:
					inverted_g = False

		return(inverted_g)





class Inversion_Clock(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, switch_time):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		self.frame_counter = 0

		#switch_time in seconds
		self.switch_time = switch_time * 30

		sprites.level_objects.add(self)


	def update(self):
		self.frame_counter += 1

		if self.frame_counter >= self.switch_time:
			chosen_ninja = None
			for ninja in sprites.ninja_list:
				chosen_ninja = ninja
				break

			if chosen_ninja.inverted_g is False:
				self.inverted_g()
			else:
				self.regular_g()

			self.frame_counter = 0

	def regular_g(self):
		for ninja in sprites.ninja_list:
			ninja.revert_g()

		for tile in sprites.tile_list:
			tile.inverted_g = False
			tile.update()

	def inverted_g(self):
		for ninja in sprites.ninja_list:
			ninja.invert_g()

		for tile in sprites.tile_list:
			tile.inverted_g = True
			tile.update()


class Mallow(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rect, inverted):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.type = 'mallow'
		self.subtype = None
		
		self.inverted = inverted

		self.online_key = 0

		self.image_list = []
		self.image1 = pygame.Surface((rect[2],rect[3]))
		self.image1.fill(options.GREEN)
		self.image1.set_colorkey(options.GREEN)
		self.image2 = pygame.Surface((rect[2],rect[3]))
		self.image2.fill(options.GREEN)
		self.image2.set_colorkey(options.GREEN)
		self.image3 = pygame.Surface((rect[2],rect[3]))
		self.image3.fill(options.GREEN)
		self.image3.set_colorkey(options.GREEN)
		self.image4 = pygame.Surface((rect[2],rect[3]))
		self.image4.fill(options.GREEN)
		self.image4.set_colorkey(options.GREEN)
		self.image_list.append(self.image1)
		self.image_list.append(self.image2)
		self.image_list.append(self.image3)
		self.image_list.append(self.image4)

		x = 0
		coord_list = ((44, 0, 48, 30),(93, 0, 48, 30),(142, 0, 48, 30),(191, 0, 48, 30))
		while x < rect[2]:
			i = random.choice((0,1,2,3))
			image_counter = 0
			while image_counter <= 3:

				image = sprites.level_sheet.getImage(coord_list[i][0],coord_list[i][1],coord_list[i][2],coord_list[i][3])
				if self.inverted is True:
					image = pygame.transform.flip(image, False, True)
				self.image_list[image_counter].blit(image,(x,0))	

				i += 1
				if i > 3:
					i = 0
				image_counter += 1

			x += 48 #48 is width of mallow pic


		self.image_number = 0
		self.image = self.image_list[self.image_number]
		self.frame_counter = 0
		
		self.rect = self.image.get_rect()
		self.dirty = 1

		self.rect.x = rect[0]
		self.rect.y = rect[1]

		#create thin rects on top/bottom for collision checking purposes.
		self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
		self.bottom_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height - 5, self.rect.width, 5)

		sprites.active_sprite_list.add(self)
		sprites.tile_list.add(self)
		sprites.active_sprite_list.change_layer(self, 5)

		sprites.quadrant_handler.join_quadrants(self)

	def update(self):
		self.frame_counter += 1
		if self.frame_counter > 30:
			self.image_number += 1
			if self.image_number > 3:
				self.image_number = 0
			self.image = self.image_list[self.image_number]
			self.frame_counter = 0
			self.dirty = 1

class Rising_Mallow(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rect, inverted):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.alarm = None
		self.type = 'mallow'
		self.subtype = 'rising mallow'

		self.online_key = 0


		self.inverted = inverted

		self.upper_limit = 360 - rect[3]
		#rect = pygame.Rect(rect[0], rect[1], rect[2],30 )

		self.image_list = []
		self.image1 = pygame.Surface((rect[2],rect[3]))
		self.image1.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image1, options.GREEN, (0, 0, self.image1.get_width(), 10), 0)
		self.image1.set_colorkey(options.GREEN)
		self.image2 = pygame.Surface((rect[2],rect[3]))
		self.image2.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image2, options.GREEN, (0, 0, self.image2.get_width(), 10), 0)
		self.image2.set_colorkey(options.GREEN)
		self.image3 = pygame.Surface((rect[2],rect[3]))
		self.image3.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image3, options.GREEN, (0, 0, self.image3.get_width(), 10), 0)
		self.image3.set_colorkey(options.GREEN)
		self.image4 = pygame.Surface((rect[2],rect[3]))
		self.image4.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image4, options.GREEN, (0, 0, self.image4.get_width(), 10), 0)
		self.image4.set_colorkey(options.GREEN)
		
		self.image_list.append(self.image1)
		self.image_list.append(self.image2)
		self.image_list.append(self.image3)
		self.image_list.append(self.image4)

		x = 0
		y = 0
		coord_list = ((44, 0, 48, 30),(93, 0, 48, 30),(142, 0, 48, 30),(191, 0, 48, 30))
		coord_list2 = ((44, 18, 48, 12),(93, 18, 48, 12),(142, 18, 48, 12),(191, 18, 48, 12))
		while y < rect[3]:	
			while x < rect[2]:
				i = random.choice((0,1,2,3))
				image_counter = 0
				while image_counter <= 3:

					if y == 0:
						image = sprites.level_sheet.getImage(coord_list[i][0],coord_list[i][1],coord_list[i][2],coord_list[i][3])
					else:
						image = sprites.level_sheet.getImage(coord_list2[i][0],coord_list2[i][1],coord_list2[i][2],coord_list2[i][3])
					
					if self.inverted is True:
						image = pygame.transform.flip(image, False, True)
					self.image_list[image_counter].blit(image,(x,y))	

					i += 1
					if i > 3:
						i = 0
					image_counter += 1

				x += 48 #48 is width of mallow pic
			if y == 0:
				y += 30 + 12
			else:
				y += 30
			x = 0



		self.image_number = 0
		self.image = self.image_list[self.image_number]
		self.frame_counter = 0
		
		self.rect = self.image.get_rect()
		self.dirty = 1

		self.rect.x = rect[0]
		self.rect.top = 330 #basic mallow height

		#create thin rects on top/bottom for collision checking purposes.
		self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
		self.bottom_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height - 5, self.rect.width, 5)

		sprites.active_sprite_list.add(self)
		sprites.tile_list.add(self)
		sprites.active_sprite_list.change_layer(self, 5)

		sprites.quadrant_handler.join_all_quadrants(self)

		self.move_timer = 0
		self.true_y = self.rect.y
		self.change_y = 0.2
		self.status = 'idle'

		self.rise_timer = 300
		self.base_rise_timer = 300
		self.next_direction = 'up'

		self.start_delay = 60

	def update(self):
		if self.alarm.status == 'active':
			self.start_delay -= 1
			
			if self.start_delay <= 0:
				self.frame_counter += 1
				if self.frame_counter > 30:
					self.dirty = 1
					self.image_number += 1
					if self.image_number > 3:
						self.image_number = 0
					self.image = self.image_list[self.image_number]
					self.frame_counter = 0
					

				if self.status == 'idle' and sprites.countdown_timer.done is True:
						self.rise_timer -= 1
						if self.rise_timer == 0:
							self.rise_timer = self.base_rise_timer
							self.status = self.next_direction

				else:
					self.dirty = 1
					if self.status == 'up':
						self.true_y -= self.change_y
						self.rect.y = round(self.true_y)

					elif self.status == 'down':
						self.true_y += self.change_y
						self.rect.y = round(self.true_y)

					if self.status == 'up':
						#if self.rect.bottom <= 360:
						if self.rect.top <= self.upper_limit:
							self.status = 'idle'
							self.next_direction = 'down'
					elif self.status == 'down':
						if self.rect.top >= 330:
							self.status = 'idle'
							self.next_direction = 'up'
							self.start_delay = 60
							self.alarm.off_switch = True

					for ninja in sprites.ninja_list:
						if ninja.splash_sprite.visible == 1:
							ninja.splash_sprite.rect.bottom = self.rect.top + 3

					for sprite in sprites.background_objects:
						try:
							if sprite.type == 'waterfall mallow splash':
								if self.rect.top > sprite.waterfall.rect.top:
									sprite.rect.bottom  = self.rect.top + 3


						except AttributeError:
							pass
		else:
			self.frame_counter += 1
			if self.frame_counter > 30:
				self.dirty = 1
				self.image_number += 1
				if self.image_number > 3:
					self.image_number = 0
				self.image = self.image_list[self.image_number]
				self.frame_counter = 0


class New_Rising_Mallow(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rect, inverted):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.alarm = None
		self.type = 'mallow'
		self.subtype = 'rising mallow'

		self.inverted = inverted

		self.upper_limit = 360 - rect[3]
		rect = pygame.Rect(rect[0], rect[1], rect[2],30 )

		self.image_list = []
		self.image1 = pygame.Surface((rect[2],rect[3]))
		self.image1.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image1, options.GREEN, (0, 0, self.image1.get_width(), 10), 0)
		self.image1.set_colorkey(options.GREEN)
		self.image2 = pygame.Surface((rect[2],rect[3]))
		self.image2.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image2, options.GREEN, (0, 0, self.image2.get_width(), 10), 0)
		self.image2.set_colorkey(options.GREEN)
		self.image3 = pygame.Surface((rect[2],rect[3]))
		self.image3.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image3, options.GREEN, (0, 0, self.image3.get_width(), 10), 0)
		self.image3.set_colorkey(options.GREEN)
		self.image4 = pygame.Surface((rect[2],rect[3]))
		self.image4.fill(options.DARK_PURPLE)
		pygame.draw.rect(self.image4, options.GREEN, (0, 0, self.image4.get_width(), 10), 0)
		self.image4.set_colorkey(options.GREEN)
		
		self.image_list.append(self.image1)
		self.image_list.append(self.image2)
		self.image_list.append(self.image3)
		self.image_list.append(self.image4)

		x = 0
		y = 0
		coord_list = ((44, 0, 48, 30),(93, 0, 48, 30),(142, 0, 48, 30),(191, 0, 48, 30))
		coord_list2 = ((44, 18, 48, 12),(93, 18, 48, 12),(142, 18, 48, 12),(191, 18, 48, 12))
		while y < rect[3]:	
			while x < rect[2]:
				i = random.choice((0,1,2,3))
				image_counter = 0
				while image_counter <= 3:

					if y == 0:
						image = sprites.level_sheet.getImage(coord_list[i][0],coord_list[i][1],coord_list[i][2],coord_list[i][3])
					else:
						image = sprites.level_sheet.getImage(coord_list2[i][0],coord_list2[i][1],coord_list2[i][2],coord_list2[i][3])
					
					if self.inverted is True:
						image = pygame.transform.flip(image, False, True)
					self.image_list[image_counter].blit(image,(x,y))	

					i += 1
					if i > 3:
						i = 0
					image_counter += 1

				x += 48 #48 is width of mallow pic
			if y == 0:
				y += 30 + 12
			else:
				y += 30
			x = 0

	

		self.image_number = 0
		self.image = self.image_list[self.image_number]
		self.frame_counter = 0
		
		self.rect = self.image.get_rect()
		self.dirty = 1

		self.rect.x = rect[0]
		self.rect.top = 330 #basic mallow height

		#create thin rects on top/bottom for collision checking purposes.
		self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
		self.bottom_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height - 5, self.rect.width, 5)

		sprites.active_sprite_list.add(self)
		sprites.tile_list.add(self)
		sprites.active_sprite_list.change_layer(self, 5)

		sprites.quadrant_handler.join_all_quadrants(self)

		self.move_timer = 0
		self.true_y = self.rect.y
		self.change_y = 0.2
		self.status = 'idle'

		self.rise_timer = 300
		self.base_rise_timer = 300
		self.next_direction = 'up'

		self.start_delay = 60

		#build ripples
		self.ripple_sprite_list = []
		i = 1
		while i < 4:
			ripple = Mallow_Ripple(self, i)
			self.ripple_sprite_list.append(ripple)
			i += 1

	def update(self):
		if self.alarm.status == 'active':
			self.start_delay -= 1
			
			if self.start_delay <= 0:
				self.frame_counter += 1
				if self.frame_counter > 30:
					self.dirty = 1
					self.image_number += 1
					if self.image_number > 3:
						self.image_number = 0
					self.image = self.image_list[self.image_number]
					self.frame_counter = 0
					

				if self.status == 'idle' and sprites.countdown_timer.done is True:
					self.rise_timer -= 1
					if self.rise_timer <= 0:
						self.rise_timer = self.base_rise_timer
						self.status = self.next_direction

				else:
					self.dirty = 1
					if self.status == 'up':
						self.true_y -= self.change_y
						self.rect.y = round(self.true_y)
						for ripple in self.ripple_sprite_list:
							ripple.move_ripples()

					elif self.status == 'down':
						self.true_y += self.change_y
						self.rect.y = round(self.true_y)
						for ripple in self.ripple_sprite_list:
							ripple.move_ripples()

					if self.status == 'up':
						#if self.rect.bottom <= 360:
						if self.rect.top <= self.upper_limit:
							self.status = 'idle'
							self.next_direction = 'down'
					elif self.status == 'down':
						if self.rect.top >= 330:
							self.status = 'idle'
							self.next_direction = 'up'
							self.start_delay = 60
							self.alarm.off_switch = True

					for ninja in sprites.ninja_list:
						if ninja.splash_sprite.visible == 1:
							ninja.splash_sprite.rect.bottom = self.rect.top + 3

					for sprite in sprites.background_objects:
						try:
							if sprite.type == 'waterfall mallow splash':
								if self.rect.top > sprite.waterfall.rect.top:
									sprite.rect.bottom  = self.rect.top + 3


						except AttributeError:
							pass
		else:
			self.frame_counter += 1
			if self.frame_counter > 30:
				self.dirty = 1
				self.image_number += 1
				if self.image_number > 3:
					self.image_number = 0
				self.image = self.image_list[self.image_number]
				self.frame_counter = 0


class Mallow_Ripple(pygame.sprite.DirtySprite):

	def __init__(self, mallow, ripple_number):

		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.mallow = mallow
		self.ripple_number = ripple_number

		width = self.mallow.rect.width
		height = 12

		self.image_list = []
		self.image1 = pygame.Surface((width,height))
		#self.image1.fill(options.DARK_PURPLE)
		#pygame.draw.rect(self.image1, options.GREEN, (0, 0, self.image1.get_width(), 10), 0)
		#self.image1.set_colorkey(options.GREEN)
		self.image2 = pygame.Surface((width,height))
		#self.image2.fill(options.DARK_PURPLE)
		#pygame.draw.rect(self.image2, options.GREEN, (0, 0, self.image2.get_width(), 10), 0)
		#self.image2.set_colorkey(options.GREEN)
		self.image3 = pygame.Surface((width,height))
		#self.image3.fill(options.DARK_PURPLE)
		#pygame.draw.rect(self.image3, options.GREEN, (0, 0, self.image3.get_width(), 10), 0)
		#self.image3.set_colorkey(options.GREEN)
		self.image4 = pygame.Surface((width,height))
		#self.image4.fill(options.DARK_PURPLE)
		#pygame.draw.rect(self.image4, options.GREEN, (0, 0, self.image4.get_width(), 10), 0)
		#self.image4.set_colorkey(options.GREEN)
		
		self.image_list.append(self.image1)
		self.image_list.append(self.image2)
		self.image_list.append(self.image3)
		self.image_list.append(self.image4)

		x = 0
		coord_list = ((44, 18, 48, 12),(93, 18, 48, 12),(142, 18, 48, 12),(191, 18, 48, 12))
		while x < width:
			i = random.choice((0,1,2,3))
			image_counter = 0
			while image_counter <= 3:
					image = sprites.level_sheet.getImage(coord_list[i][0],coord_list[i][1],coord_list[i][2],coord_list[i][3])
					self.image_list[image_counter].blit(image,(x,0))	
					i += 1
					if i > 3:
						i = 0
					image_counter += 1
			x += 48 #48 is width of mallow pic

		self.image_number = 0
		self.image = self.image_list[self.image_number]
		self.frame_counter = 0
		self.rect = self.image.get_rect()

		self.rect.x = self.mallow.rect.x
		self.rect.top = self.mallow.rect.top + 20 + (self.ripple_number * 45)

		sprites.active_sprite_list.add(self)
		sprites.background_objects.add(self)
		sprites.active_sprite_list.change_layer(self, 5)
		self.dirty = 1

	def update(self):
		self.dirty = 1
		self.frame_counter += 1
		if self.frame_counter > 30:
			self.dirty = 1
			self.image_number += 1
			if self.image_number > 3:
				self.image_number = 0
			self.image = self.image_list[self.image_number]
			self.frame_counter = 0

	def move_ripples(self):
		self.dirty = 1
		self.rect.top = self.mallow.rect.top + 20 + (self.ripple_number * 45)



class Mallow_Wall(pygame.sprite.DirtySprite):

	def __init__(self, side, rectx, recty, width, height, bubble_number, bubble_movement):
		#movement = 'True or False'
		#side is 'left', 'right', 'roof', 'floor'
		#constructor function

		pygame.sprite.DirtySprite.__init__(self)
		self.type = 'mallow_wall'
		self.subtype = None
		self.bubble_movement = bubble_movement #true or false

		self.level = None #lists level of map 1,2,3,4,5 (top to bottom)

		self.image = pygame.Surface((width, height))
		self.image.fill((200,100,200), rect = None)
		self.rect = self.image.get_rect()

		self.attached_list = pygame.sprite.LayeredDirty() #lists things attached to the tile
		 
		self.dirty = 1

		self.rect.x = rectx
		self.rect.y = recty

		#create thin rects on top/bottom for collision checking purposes.
		self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,4) 
		self.bottom_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height - 4, self.rect.width, 4)
		self.left_rect = pygame.Rect(self.rect.x, self.rect.top + 1, 5, self.rect.height - 2) 
		self.right_rect = pygame.Rect(self.rect.right - 5, self.rect.top + 1, 5, self.rect.height - 2) 

		self.side = side #holds 'left' or 'right' wall, or 'roof', or 'floor'
		self.bubble_list = []
		while bubble_number > 0:
			item_bubble = Item_Bubble(self)
			self.bubble_list.append(item_bubble)
			bubble_number -= 1


		'''	
		self.item_bubble1 = Item_Bubble(self)
		self.bubble_list.append(self.item_bubble1)
		self.item_bubble2 = Item_Bubble(self)
		self.bubble_list.append(self.item_bubble2)
		self.item_bubble3 = Item_Bubble(self)
		self.bubble_list.append(self.item_bubble3)
		self.item_bubble4 = Item_Bubble(self)
		self.bubble_list.append(self.item_bubble4)
		self.item_bubble5 = Item_Bubble(self)
		self.bubble_list.append(self.item_bubble5)
		self.item_bubble6 = Item_Bubble(self)
		self.bubble_list.append(self.item_bubble6)
		'''

		self.top_open = True
		self.bottom_open = True

		self.breakable = False

		sprites.tile_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, -5)

		sprites.quadrant_handler.join_quadrants(self)


	def update(self):
		for bubble in self.bubble_list:
			if bubble.visible is False:
				bubble.spawn_attempt()

class Classic_Item_Spawner(pygame.sprite.DirtySprite):

	def __init__(self, side, startpoint):
		#movement = 'True or False'
		#side is 'left', 'right', 'roof', 'floor'
		#point is centerx or centery
		#constructor function

		pygame.sprite.DirtySprite.__init__(self)
		self.type = 'classic_spawn_point'


		self.online_key = 0


		self.constant_item = False

		self.bubble_movement = True

		self.level = None #lists level of map 1,2,3,4,5 (top to bottom)

		self.image_list = []
		base_image = sprites.level_sheet.getImage(0, 128, 36, 30)
		self.image_list.append(base_image)
		
		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(1,159,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)

		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(18,159,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)

		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(1,176,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)

		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(18,176,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)

		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(1,193,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)

		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(18,193,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)

		i = base_image.copy()
		temp_image = sprites.level_sheet.getImage(0,60,16,16)
		i.blit(temp_image, (20,7))
		self.image_list.append(i)
		
		if side == 'right':
			temp_list = []
			for image in self.image_list:
				image = pygame.transform.flip(image, True, False)
				temp_list.append(image)
			self.image_list = temp_list
		if side == 'roof':
			temp_list = []
			for image in self.image_list:
				image = pygame.transform.flip(image, True, False)
				image = pygame.transform.rotate(image, 90)
				temp_list.append(image)
			self.image_list = temp_list

		if side == 'floor':
			temp_list = []
			for image in self.image_list:
				image = pygame.transform.flip(image, True, False)
				image = pygame.transform.rotate(image, -90)
				temp_list.append(image)
			self.image_list = temp_list

		self.image_number = 0
		self.frame_counter = 0
		self.image = self.image_list[0]

		self.rect = self.image.get_rect()
		self.rect.x = startpoint[0]
		self.rect.y = startpoint[1]
		 
		self.dirty = 1

		self.side = side
		self.bubble_list = []
		i = 0
		while i < 2:
			item_bubble = Item_Bubble(self)
			self.bubble_list.append(item_bubble)
			i += 1

		sprites.level_objects.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, -3)

		self.timer = random.randrange(-90,90,1)

		self.status = 'idle' #idle or spawn
		self.current_bubble = None

	def update(self):

		self.timer += 1
		
		if self.timer > 420 and self.status == 'idle':
			self.timer = random.randrange(-90,90,1)

			for bubble in self.bubble_list:
				if bubble.visible is False and len(bubble.item_options) > 0:
					self.current_bubble = bubble
					self.current_bubble.online_counter = 0
					self.status = 'spawn'

					#moved here for online reasons:
					self.current_bubble.item = random.choice(self.current_bubble.item_options)
					if self.side == 'left':
						self.current_bubble.rect.right = self.rect.right
						self.current_bubble.rect.centery = self.rect.centery
						self.current_bubble.change_x = random.randrange(0, 7,1) * 0.1
						self.current_bubble.change_y = random.randrange(-7, 7,1) * 0.1
					elif self.side == 'right':
						self.current_bubble.rect.left = self.rect.left
						self.current_bubble.rect.centery = self.rect.centery
						self.current_bubble.change_x = random.randrange(-7, 0,1) * 0.1
						self.current_bubble.change_y = random.randrange(-7, 7,1) * 0.1
					elif self.side == 'roof':
						self.current_bubble.rect.bottom = self.rect.bottom
						self.current_bubble.rect.centerx = self.rect.centerx
						self.current_bubble.change_x = random.randrange(-7, 7,1) * 0.1
						self.current_bubble.change_y = random.randrange(0, 7,1) * 0.1
					elif self.side == 'floor':
						self.current_bubble.rect.top = self.rect.top
						self.current_bubble.rect.centerx = self.rect.centerx
						self.current_bubble.change_x = random.randrange(-7, 7,1) * 0.1
						self.current_bubble.change_y = random.randrange(-7, 0,1) * 0.1
					
					if self.current_bubble.change_x == 0:
						self.current_bubble.change_x += random.choice((-0.25,0.25))
					if self.current_bubble.change_y == 0:
						self.current_bubble.change_y += random.choice((-0.25,0.25))

					self.current_bubble.true_x = self.current_bubble.rect.x
					self.current_bubble.true_y = self.current_bubble.rect.y


					break

		if self.status == 'spawn':
			self.frame_counter += 1
			if self.frame_counter > 8:
				self.dirty = 1
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number >= len(self.image_list): #spawn!
					'''
					if self.side == 'left':
						self.current_bubble.rect.right = self.rect.right
						self.current_bubble.rect.centery = self.rect.centery
						self.current_bubble.change_x = random.randrange(0, 7,1) * 0.1
						self.current_bubble.change_y = random.randrange(-7, 7,1) * 0.1
					elif self.side == 'right':
						self.current_bubble.rect.left = self.rect.left
						self.current_bubble.rect.centery = self.rect.centery
						self.current_bubble.change_x = random.randrange(-7, 0,1) * 0.1
						self.current_bubble.change_y = random.randrange(-7, 7,1) * 0.1
					elif self.side == 'roof':
						self.current_bubble.rect.bottom = self.rect.bottom
						self.current_bubble.rect.centerx = self.rect.centerx
						self.current_bubble.change_x = random.randrange(-7, 7,1) * 0.1
						self.current_bubble.change_y = random.randrange(0, 7,1) * 0.1

								
					if self.current_bubble.change_x == 0:
						self.current_bubble.change_x += random.choice((-0.25,0.25))
					if self.current_bubble.change_y == 0:
						self.current_bubble.change_y += random.choice((-0.25,0.25))


					self.current_bubble.true_x = self.current_bubble.rect.x
					self.current_bubble.true_y = self.current_bubble.rect.y
					'''
					self.reset()
					#self.image_number = 0
					#self.frame_counter = 0
					#self.image = self.image_list[self.image_number]
					#self.status = 'idle'

					self.current_bubble.visible = True
					self.current_bubble.dirty = 1
					#self.current_bubble.item = random.choice(self.current_bubble.item_options)
					self.current_bubble.status = 'item'
					self.current_bubble.frame_counter = 0
					self.current_bubble.image_number = 0
					self.current_bubble.update()
					self.current_bubble.pop_possible = True

				else:
					self.image = self.image_list[self.image_number]

	def reset(self):
		self.image_number = 0
		self.frame_counter = 0
		self.image = self.image_list[self.image_number]
		self.status = 'idle'


	def update_bubble_position(self): #used from client handler. Online use only.
		if self.side == 'left':
			self.current_bubble.rect.right = self.rect.right
			self.current_bubble.rect.centery = self.rect.centery
		elif self.side == 'right':
			self.current_bubble.rect.left = self.rect.left
			self.current_bubble.rect.centery = self.rect.centery
		elif self.side == 'roof':
			self.current_bubble.rect.bottom = self.rect.bottom
			self.current_bubble.rect.centerx = self.rect.centerx
		elif self.side == 'floor':
			self.current_bubble.rect.top = self.rect.top
			self.current_bubble.rect.centerx = self.rect.centerx


		self.current_bubble.true_x = self.current_bubble.rect.x
		self.current_bubble.true_y = self.current_bubble.rect.y
		

class Tile_Item_Spawner(pygame.sprite.DirtySprite):

	def __init__(self, bubble_movement, bubble_number, side):
		#movement = 'True or False'
		#side is 'left', 'right', 'roof', 'floor'
		#point is centerx or centery
		#constructor function

		pygame.sprite.DirtySprite.__init__(self)
		self.type = 'spawn_point'
		self.bubble_movement = bubble_movement #true or false

		self.constant_item = False

		self.level = None #lists level of map 1,2,3,4,5 (top to bottom)

		self.image = pygame.Surface((0, 0))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		 
		self.dirty = 1

		self.side = side
		self.bubble_list = []
		i = 0
		while i < bubble_number:
			item_bubble = Item_Bubble(self)
			self.bubble_list.append(item_bubble)
			i += 1

		sprites.level_objects.add(self)

	def update(self):
		tile_list = []
		for tile in sprites.tile_list:
			if tile.type == 'platform' and tile.subtype != 'moving platform':
				tile_list.append(tile)
		
		for bubble in self.bubble_list:
				if bubble.visible is False and len(bubble.item_options) > 0:
					tile = random.choice(tile_list)
					tile_list.remove(tile)
					if self.side == 'roof':
						self.rect.y = tile.rect.bottom
					else:
						self.rect.y = tile.rect.top
					self.rect.x = tile.rect.centerx
					bubble.spawn_attempt()
				

class Item_Spawn_Point(pygame.sprite.DirtySprite):

	def __init__(self, side, bubble_movement, x, y, constant_item):
		#movement = 'True or False'
		#side is 'left', 'right', 'roof', 'floor'
		#point is centerx or centery
		#constructor function

		pygame.sprite.DirtySprite.__init__(self)


		self.constant_item = constant_item #True if spawns immediately when item is taken.
		self.type = 'spawn_point'
		self.bubble_movement = bubble_movement #true or false

		self.level = None #lists level of map 1,2,3,4,5 (top to bottom)

		self.image = pygame.Surface((0, 0))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		 
		self.dirty = 1

		self.side = side #holds 'left' or 'right' wall, or 'roof', or 'floor'
		self.bubble_list = []
		item_bubble = Item_Bubble(self)
		self.bubble_list.append(item_bubble)

		self.constant_counter = 0

		#just moing it so it doesn't collide with other bubbles.
		item_bubble.rect.center = self.rect.center

		sprites.level_objects.add(self)
		sprites.active_sprite_list.add(self)

	def update(self):
			if sprites.transition_screen.status == 'idle':
				for bubble in self.bubble_list:
					if bubble.visible is False and len(bubble.item_options) > 0:
						
						bubble.spawn_attempt()

class Item_Bubble(pygame.sprite.DirtySprite):

	def __init__(self, wall, items = None,  item_locked = False):

		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'item_bubble'

		self.online_key = 0

		self.online_counter = self.online_key #send updated position 1x/30sec ; used to send bonus position updates

		self.online_event_counter = 0 #used to count up and order popping/spawning events online.

		self.item_locked = item_locked

		self.queue_pop = False

		self.wall = wall

		self.frame_counter = 0
		self.image_number = 0

		self.image_list = []
		image = sprites.level_sheet.getImage(0, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(17, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(34, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(50, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(68, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(85, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(102, 43, 16, 16)
		self.image_list.append(image)
		image = sprites.level_sheet.getImage(119, 43, 16, 16)
		self.image_list.append(image)

		if self.wall != None:
			if self.wall.side == 'right':
				temp_list = []
				for image in self.image_list:
					i = pygame.transform.flip(image, True, False)
					temp_list.append(i)
				self.image_list = temp_list

			if self.wall.side == 'roof':
				temp_list = []
				for image in self.image_list:
					i = pygame.transform.rotate(image, -90)
					temp_list.append(i)
				self.image_list = temp_list

			if self.wall.side == 'floor':
				temp_list = []
				for image in self.image_list:
					i = pygame.transform.rotate(image, 90)
					temp_list.append(i)
				self.image_list = temp_list
		
		self.bubble_image_list = []
		image = sprites.level_sheet.getImage(0, 60, 16, 16)
		self.bubble_image_list.append(image)
		image = sprites.level_sheet.getImage(17, 60, 16, 16)
		self.bubble_image_list.append(image)
		image = sprites.level_sheet.getImage(0, 60, 16, 16)
		self.bubble_image_list.append(image)
		image = sprites.level_sheet.getImage(34, 60, 16, 16)
		self.bubble_image_list.append(image)

		

		self.item_bubble_x_list = []
		image = sprites.level_sheet.getImage(51, 60, 16, 16)
		self.item_bubble_x_list.append(image)
		image = sprites.level_sheet.getImage(68, 60, 16, 16)
		self.item_bubble_x_list.append(image)
		image = sprites.level_sheet.getImage(51, 60, 16, 16)
		self.item_bubble_x_list.append(image)
		image = sprites.level_sheet.getImage(85, 60, 16, 16)
		self.item_bubble_x_list.append(image)

		self.item_bubble_shoes_list = []
		image = sprites.level_sheet.getImage(102, 60, 16, 16)
		self.item_bubble_shoes_list.append(image)
		image = sprites.level_sheet.getImage(119, 60, 16, 16)
		self.item_bubble_shoes_list.append(image)
		image = sprites.level_sheet.getImage(102, 60, 16, 16)
		self.item_bubble_shoes_list.append(image)
		image = sprites.level_sheet.getImage(136, 60, 16, 16)
		self.item_bubble_shoes_list.append(image)

		self.item_bubble_laser_list = []
		image = sprites.level_sheet.getImage(51, 77, 16, 16)
		self.item_bubble_laser_list.append(image)
		image = sprites.level_sheet.getImage(68, 77, 16, 16)
		self.item_bubble_laser_list.append(image)
		image = sprites.level_sheet.getImage(51, 77, 16, 16)
		self.item_bubble_laser_list.append(image)
		image = sprites.level_sheet.getImage(85, 77, 16, 16)
		self.item_bubble_laser_list.append(image)

		self.item_bubble_wings_list = []
		image = sprites.level_sheet.getImage(102, 77, 16, 16)
		self.item_bubble_wings_list.append(image)
		image = sprites.level_sheet.getImage(119, 77, 16, 16)
		self.item_bubble_wings_list.append(image)
		image = sprites.level_sheet.getImage(102, 77, 16, 16)
		self.item_bubble_wings_list.append(image)
		image = sprites.level_sheet.getImage(136, 77, 16, 16)
		self.item_bubble_wings_list.append(image)

		self.item_bubble_skull_list = []
		image = sprites.level_sheet.getImage(51, 94, 16, 16)
		self.item_bubble_skull_list.append(image)
		image = sprites.level_sheet.getImage(68, 94, 16, 16)
		self.item_bubble_skull_list.append(image)
		image = sprites.level_sheet.getImage(51, 94, 16, 16)
		self.item_bubble_skull_list.append(image)
		image = sprites.level_sheet.getImage(85, 94, 16, 16)
		self.item_bubble_skull_list.append(image)

		self.item_bubble_bomb_list = []
		image = sprites.level_sheet.getImage(102, 94, 16, 16)
		self.item_bubble_bomb_list.append(image)
		image = sprites.level_sheet.getImage(119, 94, 16, 16)
		self.item_bubble_bomb_list.append(image)
		image = sprites.level_sheet.getImage(102, 94, 16, 16)
		self.item_bubble_bomb_list.append(image)
		image = sprites.level_sheet.getImage(136, 94, 16, 16)
		self.item_bubble_bomb_list.append(image)

		self.item_bubble_volt_list = []
		image = sprites.level_sheet.getImage(51, 111, 16, 16)
		self.item_bubble_volt_list.append(image)
		image = sprites.level_sheet.getImage(68, 111, 16, 16)
		self.item_bubble_volt_list.append(image)
		image = sprites.level_sheet.getImage(51, 111, 16, 16)
		self.item_bubble_volt_list.append(image)
		image = sprites.level_sheet.getImage(85, 111, 16, 16)
		self.item_bubble_volt_list.append(image)

		self.item_bubble_mine_list = []
		image = sprites.level_sheet.getImage(102, 111, 16, 16)
		self.item_bubble_mine_list.append(image)
		image = sprites.level_sheet.getImage(119, 111, 16, 16)
		self.item_bubble_mine_list.append(image)
		image = sprites.level_sheet.getImage(102, 111, 16, 16)
		self.item_bubble_mine_list.append(image)
		image = sprites.level_sheet.getImage(136, 111, 16, 16)
		self.item_bubble_mine_list.append(image)

		self.item_bubble_rocket_list = []
		image = sprites.level_sheet.getImage(102, 128, 16, 16)
		self.item_bubble_rocket_list.append(image)
		image = sprites.level_sheet.getImage(119, 128, 16, 16)
		self.item_bubble_rocket_list.append(image)
		image = sprites.level_sheet.getImage(102, 128, 16, 16)
		self.item_bubble_rocket_list.append(image)
		image = sprites.level_sheet.getImage(136, 128, 16, 16)
		self.item_bubble_rocket_list.append(image)

		self.item_bubble_gravity_list = []
		image = sprites.level_sheet.getImage(51, 128, 16, 16)
		self.item_bubble_gravity_list.append(image)
		image = sprites.level_sheet.getImage(68, 128, 16, 16)
		self.item_bubble_gravity_list.append(image)
		image = sprites.level_sheet.getImage(51, 128, 16, 16)
		self.item_bubble_gravity_list.append(image)
		image = sprites.level_sheet.getImage(85, 128, 16, 16)
		self.item_bubble_gravity_list.append(image)

		self.item_bubble_portal_gun_list = []
		image = sprites.level_sheet.getImage(51, 145, 16, 16)
		self.item_bubble_portal_gun_list.append(image)
		image = sprites.level_sheet.getImage(68, 145, 16, 16)
		self.item_bubble_portal_gun_list.append(image)
		image = sprites.level_sheet.getImage(51, 145, 16, 16)
		self.item_bubble_portal_gun_list.append(image)
		image = sprites.level_sheet.getImage(85, 145, 16, 16)
		self.item_bubble_portal_gun_list.append(image)

		self.item_bubble_ice_bomb_list = []
		image = sprites.level_sheet.getImage(102, 145, 16, 16)
		self.item_bubble_ice_bomb_list.append(image)
		image = sprites.level_sheet.getImage(119, 145, 16, 16)
		self.item_bubble_ice_bomb_list.append(image)
		image = sprites.level_sheet.getImage(102, 145, 16, 16)
		self.item_bubble_ice_bomb_list.append(image)
		image = sprites.level_sheet.getImage(136, 145, 16, 16)
		self.item_bubble_ice_bomb_list.append(image)

		self.item_bubble_cloak_list = []
		image = sprites.level_sheet.getImage(102, 162, 16, 16)
		self.item_bubble_cloak_list.append(image)
		image = sprites.level_sheet.getImage(119, 162, 16, 16)
		self.item_bubble_cloak_list.append(image)
		image = sprites.level_sheet.getImage(102, 162, 16, 16)
		self.item_bubble_cloak_list.append(image)
		image = sprites.level_sheet.getImage(136, 162, 16, 16)
		self.item_bubble_cloak_list.append(image)

		self.item_bubble_shield_list = []
		image = sprites.level_sheet.getImage(51, 162, 16, 16)
		self.item_bubble_shield_list.append(image)
		image = sprites.level_sheet.getImage(68, 162, 16, 16)
		self.item_bubble_shield_list.append(image)
		image = sprites.level_sheet.getImage(51, 162, 16, 16)
		self.item_bubble_shield_list.append(image)
		image = sprites.level_sheet.getImage(85, 162, 16, 16)
		self.item_bubble_shield_list.append(image)

		self.item_bubble_homing_bomb_list = []
		image = sprites.level_sheet.getImage(51, 179, 16, 16)
		self.item_bubble_homing_bomb_list.append(image)
		image = sprites.level_sheet.getImage(68, 179, 16, 16)
		self.item_bubble_homing_bomb_list.append(image)
		image = sprites.level_sheet.getImage(51, 179, 16, 16)
		self.item_bubble_homing_bomb_list.append(image)
		image = sprites.level_sheet.getImage(85, 179, 16, 16)
		self.item_bubble_homing_bomb_list.append(image)

		self.item_bubble_metal_suit_list = []
		image = sprites.level_sheet.getImage(102, 179, 16, 16)
		self.item_bubble_metal_suit_list.append(image)
		image = sprites.level_sheet.getImage(119, 179, 16, 16)
		self.item_bubble_metal_suit_list.append(image)
		image = sprites.level_sheet.getImage(102, 179, 16, 16)
		self.item_bubble_metal_suit_list.append(image)
		image = sprites.level_sheet.getImage(136, 179, 16, 16)
		self.item_bubble_metal_suit_list.append(image)

		self.item_bubble_solar_flare_list = []
		image = sprites.level_sheet.getImage(51, 196, 16, 16)
		self.item_bubble_solar_flare_list.append(image)
		image = sprites.level_sheet.getImage(68, 196, 16, 16)
		self.item_bubble_solar_flare_list.append(image)
		image = sprites.level_sheet.getImage(51, 196, 16, 16)
		self.item_bubble_solar_flare_list.append(image)
		image = sprites.level_sheet.getImage(85, 196, 16, 16)
		self.item_bubble_solar_flare_list.append(image)



		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		self.status = 'bubble' #'bubble' or 'item'.
		self.item = 'none' #holds item to pass on
		#self.item_options = ('x', 'shoes', 'laser', 'wings', 'skull', 'bomb', 'volt', 'mine', 'rocket', portal_gun)
		#self.item_options = ('x', 'laser')
		
		'''
		self.item_options = []
		for entry in options.items_dict.keys():
			if options.items_dict[entry] == 'on':
				self.item_options.append(str(entry))
		'''
		
		if items == None:
			self.item_options = options.level_builder.item_options
		else:
			self.item_options = items



		if len(self.item_options) == 0:
			self.kill()

		if options.item_spawn_rate == 'Normal':
			self.spawn_rate = 7
		elif options.item_spawn_rate == 'High':
			self.spawn_rate  = 9
		elif options.item_spawn_rate == 'Low':
			self.spawn_rate = 5
		elif options.item_spawn_rate == 'Very High':
			self.spawn_rate  = 10
		elif options.item_spawn_rate == 'Very Low':
			self.spawn_rate = 2
		elif options.item_spawn_rate == 'Off':
			self.spawn_rate = 0


		self.pop_possible = False
		self.visible = False
		self.dirty = 1

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 2)
		sprites.level_objects.add(self)

		self.change_x = 0
		self.change_y = 0

		self.spawn_speed_x = 0
		self.spawn_speed_y = 0

		self.true_x = 0
		self.true_y = 0

		#self.move_counter = 0

	def update(self):

		if self.queue_pop is True: #used to pop one fame later
			self.reset()
		if len(self.item_options) > 0:
			if self.visible == True:
				self.dirty = 1

				if self.status == 'bubble':
					self.image = self.image_list[self.image_number]
					self.frame_counter += 1
					if self.frame_counter >= 16:
						self.frame_counter = 0
						self.image_number += 1
						if self.image_number >= len(self.image_list):
							self.status = 'item'
							self.pop_possible = True
							self.frame_counter = 0
							self.image_number = 0
							self.online_counter = 0
							if self.wall.bubble_movement is True:
								self.change_x = self.spawn_speed_x
								self.change_y = self.spawn_speed_y
								
				elif self.status == 'item':
					self.frame_counter += 1
					if self.frame_counter > 16:
						self.frame_counter = 0
						self.image_number += 1
						if self.image_number >= len(self.bubble_image_list):
							self.image_number = 0
					#self.image = self.bubble_image_list[self.image_number]
					if self.item == 'x':
						self.image = self.item_bubble_x_list[self.image_number]
					elif self.item == 'shoes':
						self.image = self.item_bubble_shoes_list[self.image_number]
					elif self.item == 'laser':
						self.image = self.item_bubble_laser_list[self.image_number]
					elif self.item == 'wings':
						self.image = self.item_bubble_wings_list[self.image_number]
					elif self.item == 'skull':
						self.image = self.item_bubble_skull_list[self.image_number]
					elif self.item == 'bomb':
						self.image = self.item_bubble_bomb_list[self.image_number]
					elif self.item == 'volt':
						self.image = self.item_bubble_volt_list[self.image_number]
					elif self.item == 'mine':
						self.image = self.item_bubble_mine_list[self.image_number]
					elif self.item == 'rocket':
						self.image = self.item_bubble_rocket_list[self.image_number]
					elif self.item == 'gravity':
						self.image = self.item_bubble_gravity_list[self.image_number]
					elif self.item == 'portal gun':
						self.image = self.item_bubble_portal_gun_list[self.image_number]
					elif self.item == 'ice bomb':
						self.image = self.item_bubble_ice_bomb_list[self.image_number]
					elif self.item == 'cloak':
						self.image = self.item_bubble_cloak_list[self.image_number]
					elif self.item == 'shield':
						self.image = self.item_bubble_shield_list[self.image_number]
					elif self.item == 'homing bomb':
						self.image = self.item_bubble_homing_bomb_list[self.image_number]
					elif self.item == 'metal suit':
						self.image = self.item_bubble_metal_suit_list[self.image_number]
					elif self.item == 'solar flare':
						self.image = self.item_bubble_solar_flare_list[self.image_number]


				#self.move_counter += 1 #slows down items by 50 percent
				#if self.move_counter >= 1:
				self.true_x += self.change_x
				self.true_y += self.change_y

				self.rect.x = round(self.true_x)
				self.rect.y = round(self.true_y)
				#self.move_counter = 0

				if self.status == 'item' and options.game_state in ('level', 'online_pause', 'game_credits'):
					self.collision_check()

	def collision_check(self):
		#loop_physics = False
		#for ninja in sprites.ninja_list:
		#	if ninja.loop_physics is True:
		#		loop_physics = True
		#	break

		if options.loop_physics is False:
			if self.rect.top < 0:
				self.rect.top = 0
				self.change_y = self.change_y * -1
				self.true_y = self.rect.y
			elif self.rect.bottom > sprites.size[1]:
				self.rect.bottom = sprites.size[1]
				self.change_y = self.change_y * -1
				self.true_y = self.rect.y
		else:
			if self.rect.bottom < 0 and self.change_y < 0:
				self.rect.top = sprites.size[1]
				self.true_y = self.rect.y
			if self.rect.top > sprites.size[1] and self.change_y > 0:
				self.rect.bottom = 0
				self.true_y = self.rect.y
			if self.rect.right < 0 and self.change_x < 0:
				self.rect.left = sprites.size[0]
				self.true_x = self.rect.x
			if self.rect.left > sprites.size[0] and self.change_x > 0:
				self.rect.right = 0
				self.true_x = self.rect.x

		tile_list = []
		for sprite in sprites.tile_list:
			if sprite.rect.colliderect(self.rect):
				if sprite.type == 'mallow_wall':
					if sprite.side == 'left':
						self.rect.left = sprite.rect.right
						self.true_x = self.rect.x
						self.change_x = self.change_x * -1
					elif sprite.side == 'right':
						self.rect.right = sprite.rect.left
						self.true_x = self.rect.x
						self.change_x = self.change_x * -1
					elif sprite.side == 'roof' or sprite.side == 'floor':
						if self.rect.centery > sprite.rect.centery:
							self.rect.top = sprite.rect.bottom
							self.true_y = self.rect.y
							self.change_y = self.change_y * -1
						else:
							self.rect.bottom = sprite.rect.top
							self.true_y = self.rect.y
							self.change_y = self.change_y * -1
					#elif sprite.side == 'floor':
					#	self.rect.bottom = sprite.rect.top
					#	self.true_y = self.rect.y
					#	self.change_y = self.change_y * -1

				elif sprite.type == 'mallow':
					#if sprite.inverted is False:
					if self.rect.bottom >= sprite.rect.top + 6 and self.rect.centery < sprite.rect.centery:
							if self.change_y > 0:
								self.rect.bottom = sprite.rect.top + 6
								self.true_y = self.rect.y
								self.change_y = self.change_y * -1
					else: #inverted
						if self.rect.top <= sprite.rect.bottom - 6 and self.rect.centery > sprite.rect.centery:
							if self.change_y < 0:
								self.rect.top = sprite.rect.bottom - 6
								self.true_y = self.rect.y
								self.change_y = self.change_y * -1
				
				elif sprite.type == 'tile':
					tile_list.append(sprite)

		'''
		if inverted_g is False:
			top_rect = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 3)
			bottom_rect = pygame.Rect(self.rect.x, self.rect. bottom - 3, self.rect.width, 3)
		else:
			bottom_rect = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 3)
			top_rect = pygame.Rect(self.rect.x, self.rect. bottom - 3, self.rect.width, 3)
		'''
		
		for tile in tile_list: #fix vertically if needed
			if tile.rect.colliderect(self.rect) and tile.inverted_g is False:
				top_rect = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 4)
				bottom_rect = pygame.Rect(self.rect.x, self.rect. bottom - 4, self.rect.width, 4)
				
				if tile.bottom_rect.colliderect(top_rect):
					self.rect.top = tile.rect.bottom
					self.true_y = self.rect.y
					self.change_y *= -1

				elif tile.top_rect.colliderect(bottom_rect):
					self.rect.bottom = tile.rect.top
					self.true_y = self.rect.y
					self.change_y *= -1

			elif tile.rect.colliderect(self.rect) and tile.inverted_g is True:
				bottom_rect = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 4)
				top_rect = pygame.Rect(self.rect.x, self.rect. bottom - 4, self.rect.width, 4)
				if tile.top_rect.colliderect(top_rect):
					self.rect.bottom = tile.rect.top
					self.true_y = self.rect.y
					self.change_y *= -1

				elif tile.bottom_rect.colliderect(bottom_rect):
					self.rect.top = tile.rect.bottom
					self.true_y = self.rect.y
					self.change_y *= -1

		for tile in tile_list: #fix horizontally if needed.
			if tile.rect.colliderect(self.rect):
				if self.rect.colliderect(tile.left_rect):
					self.rect.right = tile.rect.left
					self.true_x = self.rect.x
					if self.change_x > 0:
						self.change_x *= -1
				elif self.rect.colliderect(tile.right_rect):
					self.rect.left = tile.rect.right
					self.true_x = self.rect.x
					if self.change_x < 0:
						self.change_x *= -1
				'''
				if self.change_x > 0:
					self.rect.right = tile.rect.left
					self.change_x *= -1
				elif self.change_x < 0:
					self.rect.left = tile.rect.right
					self.change_x *= -1
				'''



		if self.item == 'x':
				for tile in sprites.tile_list:
					bubble_rect = pygame.Rect(self.rect.left + 3, self.rect.top + 3, self.rect.width - 6, self.rect.height - 6)
					if bubble_rect.colliderect(tile.rect):
						if tile.type == 'platform':
							tile.destroy_platform()
							self.reset()
							break

		else:
			for ninja in sprites.ninja_list:
				ninja_rect = pygame.Rect(ninja.rect.left + 4, ninja.rect.top + 4, ninja.rect.width - 8, ninja.rect.height - 8)
				if ninja_rect.colliderect(self.rect):
						if self.pop_possible is True:
							sounds.mixer.collect_item.play()
							ninja.item_stats_update(self.item)
							if ninja.item == 'metal suit' and self.item != 'metal suit':
								if ninja.rect.height == 24:
									mod = 0
								else:
									mod = 12
								sprites.particle_generator.metal_off_particles((ninja.rect.center), ninja)
							ninja.item = self.item
							ninja.item_counter = 0
							#ninja.volt_sprite.active = False
							ninja.volt_sprite.reset()
							#ninja.shield_sprite.reset()
							ninja.projectile_count = 0
							self.reset()
							if ninja.item == 'metal suit':
								sprites.particle_generator.metal_suit_particles((ninja.rect.center), ninja)
								sounds.mixer.activate_metal_suit.play()
							else:
								if ninja.status == 'metal pound':
									ninja.status = 'duck'
									ninja.frame_counter = 0
									ninja.image_number = 1
							if ninja.item == 'skull':
								ninja.shield_sprite.reset()
								#ninja.volt_sprite.reset()
								ninja.activate_death_sprite('skull', self)
								ninja.lose()
							if ninja.item == 'volt':
								ninja.shield_sprite.reset()
								sounds.mixer.volt.play()
							if ninja.item != 'cloak': #become visible if getting any item other than a cloak
								ninja.visible = 1
							break



	def reset(self):
		sprites.particle_generator.bubble_pop_particles((self.rect.center))
		self.status = 'bubble'
		self.visible = False
		self.dirty = 1
		self.frame_counter = 0
		self.image_number = 0
		self.image = self.image_list[0]
		self.change_x = 0
		self.change_y = 0
		self.item = 'none'
		self.queue_pop = False
		self.pop_possible = False

	def force_place(self, center, item):
		self.dirty = 1
		self.frame_counter = 0
		self.image_number = 0
		self.image = self.image_list[0]
		self.change_x = 0
		self.change_y = 0
		self.item = item
		self.status = 'item'
		self.visible = True
		self.dirty = 1
		self.item = random.choice(self.item_options)
		self.rect.center = center
		self.true_x = self.rect.x
		self.true_y = self.rect.y
		#sprites.active_sprite_list.change_layer(self, 110)


	def spawn_attempt(self):
		#self.reset()
		spawn_item = False
		spawn = False
		if self.wall.type == 'spawn_point' and self.wall.constant_item is True:
				self.wall.constant_counter += 1
				if self.wall.constant_counter == 120:
					self.wall.constant_counter = 0
					spawn = True
		#if self.wall.type == 'spawn_point':
		elif len(self.item_options) > 0:
			rand = random.randrange(0,10000,1)
			if rand < self.spawn_rate:
				spawn = True
			

		if spawn is True:

				if self.wall.side == 'left':
					self.rect.left = self.wall.rect.right
				elif self.wall.side == 'right':
					self.rect.right = self.wall.rect.left
				elif self.wall.side == 'roof':
					self.rect.top = self.wall.rect.bottom
				elif self.wall.side == 'floor':
					self.rect.bottom = self.wall.rect.top

				if self.wall.type == 'mallow_wall':
					if self.wall.side == 'left' or self.wall.side == 'right':
						self.rect.top = random.randrange(50, sprites.size[1] - 50, 1)
					else:
						self.rect.centerx = random.randrange(50, 640 - 50 - self.rect.width, 1)
				elif self.wall.type == 'spawn_point':
					if self.wall.side == 'left' or self.wall.side == 'right':
						self.rect.centery = self.wall.rect.centery
					else:
						self.rect.centerx = self.wall.rect.centerx

				self.true_x = self.rect.x
				self.true_y = self.rect.y

				for bubble in self.wall.bubble_list:
					if bubble != self:
						if self.rect.colliderect(bubble.rect) and bubble.visible is True:
							spawn = False
			

		if spawn is True:

				self.visible = True
				self.dirty = 1
				self.item = random.choice(self.item_options)

				#sort out eventual speeds. Won't apply until spawn is done.
				self.spawn_speed_y = random.randrange(-7,7,1) * 0.1
				if self.wall.side == 'left':
					self.spawn_speed_x = random.randrange(1,7,1) * 0.1
				elif self.wall.side == 'right':
					self.spawn_speed_x = random.randrange(-7, -1,1) * 0.1
				else:
					self.spawn_speed_x = random.randrange(-7, 7,1) * 0.1
								
				if self.spawn_speed_x == 0:
					self.spawn_speed_x += random.choice((-0.25,0.25))
				if self.spawn_speed_y == 0:
					self.spawn_speed_y += random.choice((-0.25,0.25))




class Tile(pygame.sprite.DirtySprite):

	def __init__(self, rectx, recty, style, breakable):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.type = 'tile'

		self.subtype = 'tile' #differentiates from 'moving tile'... not yet made

		self.breakable = breakable

		self.top_friction = 'normal'
		self.bottom_friction = 'normal'

		self.attached_list = pygame.sprite.LayeredDirty()

		self.level = None #lists level of map 1,2,3,4,5 (top to bottom)

		self.style = style

		self.image = pygame.Surface((24,24))
		self.rect = self.image.get_rect()

		self.unfrozen = pygame.Surface((24,24))
		self.top_frozen = pygame.Surface((24,24))
		self.bottom_frozen = pygame.Surface((24,24))
		self.both_frozen = pygame.Surface((24,24))
		 
		self.dirty = 1

		self.rect.x = rectx
		self.rect.y = recty

		self.inverted_g = False

		#create thin rects on top/bottom for collision checking purposes.
		self.top_rect = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4,5) 
		self.bottom_rect = pygame.Rect(self.rect.x + 2, self.rect.y + self.rect.height - 5, self.rect.width - 4, 5)
		self.left_rect = pygame.Rect(self.rect.x, self.rect.top + 1, 7, self.rect.height - 2) 
		self.right_rect = pygame.Rect(self.rect.right - 7, self.rect.top + 1, 7, self.rect.height - 2) 

		self.top_open = True
		self.bottom_open = True
		self.left_open = True
		self.right_open = True

		sprites.tile_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, -5)

		sprites.quadrant_handler.join_quadrants(self)

		self.left_tile_dist = None
		self.right_tile_dist = None
		self.top_tile_dist = None
		self.bottom_tile_dist = None

		#if self.breakable is True:
		#	sprites.breakable_tile_list.add(self)
	def update(self):
		pass

		'''
		if self.inverted_g is False:
			#create thin rects on top/bottom for collision checking purposes.
			self.top_rect = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4,5) 
			self.bottom_rect = pygame.Rect(self.rect.x + 2, self.rect.y + self.rect.height - 5, self.rect.width - 4, 5)
		else:
			#create thin rects on top/bottom for collision checking purposes.
			self.bottom_rect = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4,5) 
			self.top_rect = pygame.Rect(self.rect.x + 2, self.rect.y + self.rect.height - 5, self.rect.width - 4, 5)
		'''

	def destroy(self, source):
		if self.top_friction == 'icy' and self.bottom_friction == 'icy':
			style = 'ice'
		else:
			style = self.style

		if source.type == 'Ninja':
			delay = source.tile_particle_timer 
			source.tile_particle_timer = 60
		else:
			delay = 0

		sprites.particle_generator.tile_death_particles(self.rect, style, self.inverted_g, delay)
		sounds.mixer.block_break.play()

		for particle in self.attached_list:
			particle.reset()



		self.kill()

		for tile in self.neighbor_list:
			tile.find_neighbors()

		if sprites.shake_handler.current_shake < 1.5:
			sprites.shake_handler.current_shake = 1.5
			#sprites.shake_handler.current_shake += 0.5

	def apply_ice(self):
		self.dirty = 1
		if self.top_friction == 'icy' and self.bottom_friction == 'icy':
			self.image = self.both_frozen
		elif self.top_friction == 'icy':
			self.image = self.top_frozen
		elif self.bottom_friction == 'icy':
			self.image = self.bottom_frozen
		else:
			self.image = self.unfrozen


	def find_neighbors(self):
		self.neighbor_list = []
		left_tile = None
		right_tile = None
		top_tile = None
		bottom_tile = None

		self.left_tile_dist = None
		self.right_tile_dist = None
		self.top_tile_dist = None
		self.bottom_tile_dist = None

		for tile in sprites.tile_list:
			if tile != self:
				if tile.type in ('tile', 'platform'):
					if tile.rect.top == self.rect.top:
						left_dist = self.rect.left - tile.rect.right
						if left_dist >= 0:
							if self.left_tile_dist == None or left_dist < self.left_tile_dist:
								self.left_tile_dist = left_dist
								left_tile = tile

						right_dist = tile.rect.left - self.rect.right
						if right_dist >= 0:
							if self.right_tile_dist == None or right_dist < self.right_tile_dist:
								self.right_tile_dist = right_dist
								right_tile = tile

					if tile.rect.centerx < self.rect.right and tile.rect.centerx > self.rect.left:
						top_dist = self.rect.top - tile.rect.top
						if top_dist > 0:
							if self.top_tile_dist == None or top_dist < self.top_tile_dist:
								self.top_tile_dist = top_dist
								top_tile = tile

						bottom_dist = tile.rect.top - self.rect.top
						if bottom_dist > 0:
							if self.bottom_tile_dist == None or bottom_dist < self.bottom_tile_dist:
								self.bottom_tile_dist = bottom_dist
								bottom_tile = tile
		if left_tile != None:
			self.neighbor_list.append(left_tile)
		if right_tile != None:
			self.neighbor_list.append(right_tile)
		if top_tile != None:
			self.neighbor_list.append(top_tile)
		if bottom_tile != None:
			self.neighbor_list.append(bottom_tile)
	def check_sides(self, mid_level = False):
		for tile in sprites.tile_list:
			if tile.type == 'tile' and tile != self:
				if tile.rect.x == self.rect.x:
					if tile.rect.width == self.rect.width:
						if self.rect.top == tile.rect.bottom:
							self.top_open = False
						if self.rect.bottom == tile.rect.top:
							self.bottom_open = False
				if tile.rect.y == self.rect.y:
					if tile.rect.height == self.rect.height:
						if self.rect.left == tile.rect.right:
							self.left_open = False
						if self.rect.right == tile.rect.left:
							self.right_open = False

		if sprites.countdown_timer.done is False or mid_level is True:
			if self.style == 'dungeon':
				if self.left_open is True and self.right_open is True:
					coord = random.choice(((318,75), (318,75), (318,75), (318,100), (418,75), (418,100)))
				elif self.left_open is True:	
					coord = random.choice(((343,75), (343,75), (343,75), (343,100), (443, 75), (443,100)))
				elif self.right_open is True:
					coord = random.choice(((368,75), (368,75), (368,75), (368,100), (468, 75), (468,100)))
				else:
					coord = random.choice(((293, 75), (293, 75), (293, 75), (293, 100), (393, 75), (393,100)))

			#tiles are no longer specifically ice. Just get covered in ice at start of level as needed.
			elif self.style == 'ice':
				coord = (381,50)

			elif self.style == 'exploding':
				coord = (294,390)

			elif self.style == 'paradox':
				coord = (344,341)

			elif self.style == 'menu':
				coord = (268,1)

			elif self.style == 'stone':
				coord = (293,180)
				if self.top_open is True:
					if self.left_open is True and self.right_open is True and self.bottom_open is True:
						coord = (293,205)
					elif self.left_open is True and self.right_open is True and self.bottom_open is False:
						coord = (343,205)
					elif self.left_open is False and self.right_open is False and self.bottom_open is True:
						coord = (368,205)
					elif self.left_open is True and self.right_open is False and self.bottom_open is True:
						coord = (393,205)
					elif self.left_open is False and self.right_open is True and self.bottom_open is True:
						coord = (418,205)

					elif self.left_open is True and self.right_open is False and self.bottom_open is False:
						coord = (293,230)
					elif self.left_open is False and self.right_open is True and self.bottom_open is False:
						coord = (318,230)

					elif self.left_open is False and self.right_open is False:
						coord = (318,205)
				else:
					if self.left_open is True and self.right_open is False and self.bottom_open is True:
						coord = (368,180)
					elif self.left_open is False and self.right_open is True and self.bottom_open is True:
						coord = (343,180)
					elif self.left_open is True and self.right_open is True and self.bottom_open is False:
						coord = (318,180)
					elif self.left_open is False and self.right_open is False and self.bottom_open is True:
						coord = (393,180)
					elif self.left_open is True and self.right_open is True and self.bottom_open is True:
						coord = (418,180)
					elif self.bottom_open is False:
						if self.left_open is True and self.right_open is False:
							coord = (405,230)
						elif self.right_open is True and self.left_open is False:
							coord = (343,230)


			elif self.style == 'volcanic':
				x_mod = 364
				y_mod = -180
				coord = (293 + x_mod,180 + y_mod)
				if self.top_open is True:
					if self.left_open is True and self.right_open is True and self.bottom_open is True:
						coord = (293 + x_mod,205 + y_mod)
					elif self.left_open is True and self.right_open is True and self.bottom_open is False:
						coord = (343 + x_mod,205 + y_mod)
					elif self.left_open is False and self.right_open is False and self.bottom_open is True:
						coord = (368 + x_mod,205 + y_mod)
					elif self.left_open is True and self.right_open is False and self.bottom_open is True:
						coord = (393 + x_mod,205 + y_mod)
					elif self.left_open is False and self.right_open is True and self.bottom_open is True:
						coord = (418 + x_mod,205 + y_mod)

					elif self.left_open is True and self.right_open is False and self.bottom_open is False:
						coord = (293 + x_mod,230 + y_mod)
					elif self.left_open is False and self.right_open is True and self.bottom_open is False:
						coord = (318 + x_mod,230 + y_mod)

					elif self.left_open is False and self.right_open is False:
						coord = (318 + x_mod,205 + y_mod)
				else:
					if self.left_open is True and self.right_open is False and self.bottom_open is True:
						coord = (368 + x_mod,180 + y_mod)
					elif self.left_open is False and self.right_open is True and self.bottom_open is True:
						coord = (343 + x_mod,180 + y_mod)
					elif self.left_open is True and self.right_open is True and self.bottom_open is False:
						coord = (318 + x_mod,180 + y_mod)
					elif self.left_open is False and self.right_open is False and self.bottom_open is True:
						coord = (393 + x_mod,180 + y_mod)

			elif self.style == 'mystic':
				coord = (393,280)
				if self.top_open is True:
					if self.left_open is True and self.right_open is True and self.bottom_open is True:
						coord = (293,255)
					elif self.left_open is True and self.right_open is True and self.bottom_open is False:
						coord = (293,305)
					elif self.left_open is False and self.right_open is False and self.bottom_open is True:
						coord = (318,255)
					elif self.left_open is True and self.right_open is False and self.bottom_open is True:
						coord = (368,255)
					elif self.left_open is False and self.right_open is True and self.bottom_open is True:
						coord = (343,255)

					elif self.left_open is True and self.right_open is False and self.bottom_open is False:
						coord = (318,280)
					elif self.left_open is False and self.right_open is True and self.bottom_open is False:
						coord = (293,280)

					elif self.left_open is False and self.right_open is False and self.bottom_open is False:
						coord = (343,305)

					elif self.left_open is False and self.right_open is False:
						coord = (293,280)
				else:
					if self.left_open is True and self.right_open is False and self.bottom_open is True:
						coord = (343,280)
					elif self.left_open is False and self.right_open is True and self.bottom_open is True:
						coord = (368,280)
					elif self.left_open is True and self.right_open is True and self.bottom_open is True:
						coord = (368,305)
					elif self.left_open is True and self.right_open is True and self.bottom_open is False:
						coord = (393,255)
					elif self.left_open is False and self.right_open is False and self.bottom_open is True:
						coord = (318,305)
					elif self.left_open is False and self.right_open is False and self.bottom_open is False:
						coord = (393,280)
					elif self.left_open is False and self.right_open is True and self.bottom_open is False:
						coord = (293,330)
					elif self.left_open is True and self.right_open is False and self.bottom_open is False:
						coord = (318,330)


			elif self.style == 'space':
				if self.rect.centery > sprites.size[1] - 24 or self.rect.centery < 24:
					if self.left_open is False and self.right_open is False:
						coord = (430,136)
					else:
						coord = (355,136)

				elif self.rect.centerx < 24 or self.rect.centerx > sprites.size[0] - 24:
					if self.top_open is False and self.bottom_open is False:
						coord = (405,136)
					else:
						coord = (355,136)

				else:
					coord  = (380, 136)

				'''
				i = random.randrange(0, 10, 1)
				if i < 3:
					if self.top_open is False and self.bottom_open is False:
						coord = random.choice(((330,136), (355,136), (405,136)))

					elif self.left_open is False and self.right_open is False:
						coord = random.choice(((330,136), (355,136), (430,136)))

					else:
						coord = random.choice(((330,136), (355,136)))
				'''

			elif self.style == 'temple':
				coord = random.choice(((293,0), (318,0), (343,0), (368,0), (393, 0), (418, 0), (443, 0)))

			elif self.style == 'classic':
				coord = (406,50)

			ice_up = sprites.level_sheet.getImage(356, 45, 24, 14)
			ice_down = sprites.level_sheet.getImage(356, 60, 24, 14)

			self.image = sprites.level_sheet.getImage(coord[0], coord[1], 24, 24)
			self.unfrozen = sprites.level_sheet.getImage(coord[0], coord[1], 24, 24)

			self.top_frozen =  sprites.level_sheet.getImage(coord[0], coord[1], 24, 24)
			self.top_frozen.blit(ice_up, (0,0))

			self.bottom_frozen = sprites.level_sheet.getImage(coord[0], coord[1], 24, 24)
			self.bottom_frozen.blit(ice_down, (0,10))

			self.both_frozen =  sprites.level_sheet.getImage(318, 25, 24, 24)
			#self.both_frozen.blit(ice_up, (0,0))
			#self.both_frozen.blit(ice_down, (0,10))

			if self.breakable is True:
				coord = random.choice(((545,8), (570,8), (595,8),(520,8)))
				image = sprites.level_sheet.getImage(coord[0], coord[1], 24, 24)
				self.image.blit(image, (0,0))

			self.dirty = 1
			#if self.bottom_open is True:
			#	pygame.draw.line(self.image, (0,255,255), (0, self.rect.height - 2), (self.rect.width, self.rect.height - 2), 5)
			#if self.top_open is True:
			#	pygame.draw.line(self.image, (0,255,255), (0, 0), (self.rect.width, 0), 5)



class Platform(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, rectx, recty, style, breakable):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.type = 'platform'
		self.subtype = 'none'
		self.top_friction = 'normal'
		self.bottom_friction = 'normal'

		self.online_key = 0
		self.destroyed = False



		self.attached_list = pygame.sprite.LayeredDirty() #lists things attached to the tile

		self.breakable = breakable

		self.level = None #level of map, 1,2,3,4, or 5
		self.style = style
		#self.image = pygame.Surface((36,12))

		#print(self.style)
		#print(self.type)

		if style == 'temple':
			coord = (468, 0)

		elif style == 'paradox':
			coord = (344,330)

		elif style == 'phasing':
			coord = (306,355)

		elif style == 'dungeon':
			coord = random.choice(((493,75), (493,86), (493,97), (493,108)))

		elif style == 'classic':
			coord = (293,125)

		elif style == 'gravity switch':
			coord = (343, 366)

		elif style == 'space':
			#coord = random.choice(((293,136), (293,147), (293, 158), (293, 169), (330,147), (330, 158)))
			coord = random.choice(((293,136), (293,147), (293, 158), (293, 169)))

		elif style == 'stone':
			coord = (330,169)

		elif style == 'mystic':
			coord = (368,244)

		elif style == 'log':
			coord = (330, 125)


		#tiles are no longer specifically ice. Just get covered in ice at start of level as needed.
		elif style == 'ice':
			coord = (381,39)

		else:
			coord = (293,125)

		image = sprites.level_sheet.getImage(coord[0], coord[1], 36, 10)
		self.image = image
		self.rect = self.image.get_rect()
		self.dirty = 1

		ice_up = sprites.level_sheet.getImage(318, 57, 36, 7)
		ice_down = sprites.level_sheet.getImage(318, 65, 36, 7)

		self.unfrozen = sprites.level_sheet.getImage(coord[0], coord[1], 36, 10)

		self.top_frozen =  sprites.level_sheet.getImage(coord[0], coord[1], 36, 10)
		self.top_frozen.blit(ice_up, (0,0))

		self.bottom_frozen = sprites.level_sheet.getImage(coord[0], coord[1], 36, 10)
		self.bottom_frozen.blit(ice_down, (0,3))

		self.both_frozen =  sprites.level_sheet.getImage(343, 25, 36, 10)
		#self.both_frozen.blit(ice_up, (0,0))
		#self.both_frozen.blit(ice_down, (0,3))

		self.dirty = 1

		self.rect.x = rectx
		self.rect.y = recty

		self.inverted_g = False

		#create thin rects on top/bottom for collision checking purposes.
		self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
		self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)

		self.top_open = True
		self.bottom_open = True

		sprites.tile_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, -5)

		sprites.quadrant_handler.join_quadrants(self)

		self.left_tile_dist = None
		self.right_tile_dist = None
		self.top_tile_dist = None
		self.bottom_tile_dist = None



	def update(self):
		pass

		'''
		if self.inverted_g is False:
			#create thin rects on top/bottom for collision checking purposes.
			self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
			self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
		else:
			#create thin rects on top/bottom for collision checking purposes.
			self.bottom_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
			self.top_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
		'''

	def destroy_platform(self):
		if self.destroyed is False:
			self.destroyed = True
			if self.top_friction == 'icy' and self.bottom_friction == 'icy':
				style = 'ice'
			else:
				style = self.style
							

			sprites.particle_generator.tile_death_particles(self.rect, style, self.inverted_g, 0)
			
			for particle in self.attached_list:
				particle.reset()

			self.kill()

			if self in level_builder.moving_platform_spawn_options:
				level_builder.moving_platform_spawn_options.remove(self)

			for tile in self.neighbor_list:
				tile.find_neighbors()

			if sprites.shake_handler.current_shake < 2.5:
				sprites.shake_handler.current_shake = 2.5

	def apply_ice(self):
		if self.top_friction == 'icy' and self.bottom_friction == 'icy':
			self.image = self.both_frozen
		elif self.top_friction == 'icy':
			self.image = self.top_frozen
		elif self.bottom_friction == 'icy':
			self.image = self.bottom_frozen
		else:
			self.image = self.unfrozen
		self.dirty = 1

	def find_neighbors(self):
		self.neighbor_list = []
		left_tile = None
		right_tile = None
		top_tile = None
		bottom_tile = None

		self.left_tile_dist = None
		self.right_tile_dist = None
		self.top_tile_dist = None
		self.bottom_tile_dist = None

		for tile in sprites.tile_list:
			if tile != self:
				if tile.type in ('tile', 'platform'):
					if tile.rect.top == self.rect.top:
						left_dist = self.rect.left - tile.rect.right
						if left_dist >= 0:
							if self.left_tile_dist == None or left_dist < self.left_tile_dist:
								self.left_tile_dist = left_dist
								left_tile = tile

						right_dist = tile.rect.left - self.rect.right
						if right_dist >= 0:
							if self.right_tile_dist == None or right_dist < self.right_tile_dist:
								self.right_tile_dist = right_dist
								right_tile = tile

					if tile.rect.centerx < self.rect.right and tile.rect.centerx > self.rect.left:
						top_dist = self.rect.top - tile.rect.top
						if top_dist > 0:
							if self.top_tile_dist == None or top_dist < self.top_tile_dist:
								self.top_tile_dist = top_dist
								top_tile = tile

						bottom_dist = tile.rect.top - self.rect.top
						if bottom_dist > 0:
							if self.bottom_tile_dist == None or bottom_dist < self.bottom_tile_dist:
								self.bottom_tile_dist = bottom_dist
								bottom_tile = tile
		if left_tile != None:
			self.neighbor_list.append(left_tile)
		if right_tile != None:
			self.neighbor_list.append(right_tile)
		if top_tile != None:
			self.neighbor_list.append(top_tile)
		if bottom_tile != None:
			self.neighbor_list.append(bottom_tile)



class Log(Platform): #moving platform
	#you can jump up through platforms
	def __init__(self, rectx, recty, waterfall, style):
		#constructor function
		Platform.__init__(self, rectx, recty, style, False)

		self.active = True #Needed ONLY for volt particles on respawn in practice mode?? Not sure why. BUG


		self.online_key = 0
		

		self.waterfall = waterfall
		self.waterfall.log_list.append(self)
		self.rect.centerx = rectx
		self.rect.centery = recty

		self.true_x = self.rect.x
		self.true_y = self.rect.y

		self.yspeed = 1

		

		self.subtype = 'moving platform'
		self.log = True

		self.sticky_rect = pygame.Rect(0,0,0,0)

		self.front_layer = sprites.active_sprite_list.get_layer_of_sprite(waterfall) + 1
		self.back_layer = self.front_layer - 2
		self.layer = self.front_layer
		sprites.active_sprite_list.change_layer(self, self.layer)

		self.direction = 'down' #'up' or 'down'
		
		if self.waterfall.inverted is True:
			self.yspeed *= -1

		self.start = False
	def update(self):
		pass
	
	def falls_update(self):
		if self.start is True:
			#if options.update_state == 1:
			self.dirty = 1

			self.get_rects()
			


			sprite_list = self.apply_sticky_rect()

			old_x = self.rect.x
			old_y = self.rect.y

			
			#if self.inverted_g is False:
			if self.direction == 'down':
					self.true_y += self.yspeed
					self.rect.y = round(self.true_y)
					#for sprite in sprite_list:
					#		sprite.rect.bottom = self.rect.top
					#		sprite.true_y = sprite.rect.y
			elif self.direction == 'up':
					self.true_y -= self.yspeed
					self.rect.y = round(self.true_y)
					#for sprite in sprite_list:
					#		sprite.rect.bottom = self.rect.top
					#		sprite.true_y = sprite.rect.y

			'''
			else: #inverted gravity
				if self.direction =='down':
					self.true_y += self.yspeed
					self.rect.y = round(self.true_y)
					#for sprite in sprite_list:
					#		sprite.rect.top = self.rect.bottom
					#		sprite.true_y = sprite.rect.y
				elif self.direction == 'up':
					self.true_y -= self.yspeed
					self.rect.y = round(self.true_y)
					#for sprite in sprite_list:
					#		sprite.rect.top = self.rect.bottom
					#		sprite.true_y = sprite.rect.y
			'''


			#Finally, Move Affected Sprites
			x_change = self.rect.x - old_x
			y_change = self.rect.y - old_y
			for sprite in sprite_list:
				sprite.true_x += x_change
				sprite.rect.x = round(sprite.true_x)
				sprite.true_y += y_change
				sprite.rect.y = round(sprite.true_y)


			if self.layer == self.front_layer:
				if self.waterfall.inverted is True:
					if self.rect.bottom < self.waterfall.rect.top:
						self.layer = self.back_layer
						sprites.active_sprite_list.change_layer(self, self.layer)
						self.direction = 'up'
						self.rect.bottom = self.waterfall.rect.bottom + 5
						self.true_y = self.rect.y
						for sprite in self.attached_list:
							self.attached_list.remove(sprite)
						self.reset_ice()
				else:
					if self.rect.top > self.waterfall.rect.bottom:
						self.layer = self.back_layer
						sprites.active_sprite_list.change_layer(self, self.layer)
						self.direction = 'up'
						self.rect.top = self.waterfall.rect.top - 5
						self.true_y = self.rect.y
						for sprite in self.attached_list:
							self.attached_list.remove(sprite)
						self.reset_ice()

			if self.layer == self.back_layer:
				if self.waterfall.inverted is True:
					if self.rect.top >= self.waterfall.rect.bottom:
						self.rect.top = self.waterfall.rect.bottom
						self.true_y = self.rect.y
						self.direction = 'down'
						self.layer = self.front_layer
						sprites.active_sprite_list.change_layer(self, self.layer)
				else:
					if self.rect.bottom <= self.waterfall.rect.top:
						self.rect.bottom = self.waterfall.rect.top
						self.true_y = self.rect.y
						self.direction = 'down'
						self.layer = self.front_layer
						sprites.active_sprite_list.change_layer(self, self.layer)

			self.get_rects()

	def reset_ice(self):
		self.top_friction = 'normal'
		self.bottom_friction = 'normal'
		self.image = self.unfrozen
		self.dirty = 1

	def get_rects(self):
		if self.waterfall.inverted is False:
			#create thin rects on top/bottom for collision checking purposes.
			self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
			self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
			self.sticky_rect = pygame.Rect(self.rect.x, self.rect.top -4, self.rect.width,5)
		else:
			#create thin rects on top/bottom for collision checking purposes.
			self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
			self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
			self.sticky_rect = pygame.Rect(self.rect.x, self.rect.bottom - 1, self.rect.width,5)

	def apply_sticky_rect(self):
		sprite_list = []
		for ninja in sprites.ninja_list:
			ninja.update_collision_rects()
			if ninja.moving_platform is False:
				ninja.online_platform_key = None
				if self.sticky_rect.colliderect(ninja.rect_bottom):
					#if ninja.change_y == 0:
					sprite_list.append(ninja)
					ninja.moving_platform = True
					ninja.online_platform_key = self.online_key

			for mine in ninja.mine_list:
				if mine.status == 'armed' and mine.moving_platform is False:
					if self.sticky_rect.colliderect(mine.rect):
						sprite_list.append(mine)

			if self.sticky_rect.colliderect(ninja.bomb_sprite):
				sprite_list.append(ninja.bomb_sprite)


		for sprite in sprites.gravity_effects:
			if self.sticky_rect.colliderect(sprite.rect):
				sprite_list.append(sprite)

		for sprite in self.attached_list:
			sprite_list.append(sprite)
			sprite.dirty = 1

		return sprite_list


class Moving_Platform(Platform):
	#you can jump up through platforms
	def __init__(self, start_position, position_list, xspeed, yspeed, style, breakable):
		#constructor function
		

		Platform.__init__(self, 0, 0, style, breakable)


		
		#self.online_frame = 0 #counts up 1 at a time. Used to only use most current.
		#self.offline_frame = 0 #counts up 1 locally each frame. Used to compare to online frame.
		self.online_key = 0


		self.active = True #Needed ONLY for volt particles on respawn in practice mode?? Not sure why. BUG

		self.log = False
		self.subtype = 'moving platform'
		self.bonus_subtype = None
		if len(position_list) == 1440:
			self.bonus_subtype = 'circle'

		self.position_list = position_list
		self.position_number = start_position #holds current position

		if isinstance (self.position_number, int):
			point = self.position_list[self.position_number]
			self.rect.centerx = point[0]
			self.rect.centery = point[1]
		else:
			point1_number = int(self.position_number)
			if point1_number >= len(self.position_list):
				point1_number = 0
			point2_number = math.ceil(self.position_number)
			if point2_number >= len(self.position_list):
				point2_number = 0
			
			point1 = self.position_list[point1_number]
			point2 = self.position_list[point2_number]

			self.rect.centerx = (point1[0] + point2[0]) / 2
			self.rect.centery = (point1[1] + point2[1]) / 2

			self.position_number = point2_number



		if xspeed == -1: #triggers counterclockwise
			xspeed = 1
			new_list = list(reversed(self.position_list))
			self.position_list = new_list

			self.position_number = self.position_list.index(point)



		self.frame_counter = 0
		self.xspeed = xspeed / 2
		self.yspeed = yspeed / 2

		self.goal_position = self.position_list[self.position_number] #(x,y)

		self.sticky_rect = pygame.Rect(0,0,0,0)

		self.true_x = self.rect.x
		self.true_y = self.rect.y

		self.last_quadrant = None

		self.start = True
		self.update()
		self.start = False #used to help proper starting locations online

	def update(self):
		#self.offline_frame += 1
		if self.start is True:
			i = sprites.quadrant_handler.join_quadrants(self)
			if self.last_quadrant != i and self.last_quadrant != None:
				self.last_quadrant.remove(self)
				self.last_quadrant = i
			
			if 1 == 1:
				self.dirty = 1
				self.get_rects()
				sprite_list = self.apply_sticky_rect()

				if self.bonus_subtype == None:
					old_x = self.rect.x
					old_y = self.rect.y

					if self.rect.centerx < self.goal_position[0]:
						self.true_x += self.xspeed
						self.rect.x = round(self.true_x)
						#for sprite in sprite_list:
						#	sprite.true_x += self.xspeed
						#	sprite.rect.x = round(sprite.true_x)
					elif self.rect.centerx > self.goal_position[0]:
						self.true_x -= self.xspeed
						self.rect.x = round(self.true_x)
						#for sprite in sprite_list:
						#	sprite.true_x -= self.xspeed
						#	sprite.rect.x = round(sprite.true_x)

					if self.inverted_g is False:
						if self.rect.centery < self.goal_position[1]:
							self.true_y += self.yspeed
							self.rect.y = round(self.true_y)
							#for sprite in sprite_list:
							#		sprite.rect.bottom = self.rect.top
							#		sprite.true_y = sprite.rect.y

						elif self.rect.centery > self.goal_position[1]:
							self.true_y -= self.yspeed
							self.rect.y = round(self.true_y)
							#for sprite in sprite_list:
							#		sprite.rect.bottom = self.rect.top
							#		sprite.true_y = sprite.rect.y

					else: #inverted gravity
						if self.rect.centery < self.goal_position[1]:
							self.true_y += self.yspeed
							self.rect.y = round(self.true_y)
							#for sprite in sprite_list:
							#		sprite.rect.top = self.rect.bottom
							#		sprite.true_y = sprite.rect.y
						elif self.rect.centery > self.goal_position[1]:
							self.true_y -= self.yspeed
							self.rect.y = round(self.true_y)
							#for sprite in sprite_list:
							#		sprite.rect.top = self.rect.bottom
							#		sprite.true_y = sprite.rect.y

					if self.rect.centerx == self.goal_position[0] and self.rect.centery == self.goal_position[1]:
						self.position_number += 1
						if self.position_number >= len(self.position_list):
							self.position_number = 0
						self.goal_position = self.position_list[self.position_number]
					
					#Finally, Move Affected Sprites
					x_change = self.rect.x - old_x
					y_change = self.rect.y - old_y
					for sprite in sprite_list:
						sprite.true_x += x_change
						sprite.rect.x = round(sprite.true_x)
						sprite.true_y += y_change
						sprite.rect.y = round(sprite.true_y)

				elif self.bonus_subtype == 'circle':
					self.frame_counter += 1
					if self.frame_counter == 1:
						#try it how CLIENT one is moved. Get center point of sprite vs tile before, and then again after.
						self.frame_counter = 0
						old_x = self.rect.x
						old_y = self.rect.y
						self.rect.centerx = self.goal_position[0]
						self.rect.centery = self.goal_position[1]
						x_change = self.rect.x - old_x
						y_change = self.rect.y - old_y

						for sprite in sprite_list:
							sprite.true_x += x_change
							sprite.rect.x = round(sprite.true_x)
							sprite.true_y += y_change
							sprite.rect.y = round(sprite.true_y)


						self.position_number += 1
						if self.position_number >= len(self.position_list):
							self.position_number = 0
						self.goal_position = self.position_list[self.position_number]

				self.get_rects()

	def get_rects(self):
		self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
		self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)

		if self.inverted_g is False:
			#create thin rects on top/bottom for collision checking purposes.
			#self.top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
			#self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
			self.sticky_rect = pygame.Rect(self.rect.x, self.rect.top -4, self.rect.width,5)
		else:
			#create thin rects on top/bottom for collision checking purposes.
			#self.bottom_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,5) 
			#self.top_rect = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
			self.sticky_rect = pygame.Rect(self.rect.x, self.rect.bottom - 1, self.rect.width,5)

	def apply_sticky_rect(self):

		sprite_list = []
		for ninja in sprites.ninja_list:
			ninja.update_collision_rects()
			if ninja.moving_platform is False:
				ninja.online_platform_key = None
				if self.sticky_rect.colliderect(ninja.rect_bottom):
					#if ninja.check_squished('moving_platform') is False:
					#if ninja.change_y == 0:
					sprite_list.append(ninja)
					ninja.moving_platform = True
					ninja.online_platform_key = self.online_key

			for mine in ninja.mine_list:
				if mine.status == 'armed' and mine.moving_platform is False:
					if self.sticky_rect.colliderect(mine.rect):
						sprite_list.append(mine)
						mine.moving_platform = True

			if ninja.bomb_sprite.moving_platform is False and self.sticky_rect.colliderect(ninja.bomb_sprite):
				sprite_list.append(ninja.bomb_sprite)
				ninja.bomb_sprite.moving_platform = True

		'''
		for ninja in sprites.player_list:
			if ninja.death_sprite.rect.colliderect(self.sticky_rect):
				if ninja.death_sprite.inverted_g is False:
					bottom_rect = pygame.Rect(ninja.death_sprite.rect.left + 2, ninja.death_sprite.rect.top, 24 - 2, 4)
				else:
					bottom_rect = pygame.Rect(ninja.death_sprite.rect.left + 2, ninja.death_sprite.rect.bottom - 4, 24 - 2, 4)
				if self.sticky_rect.colliderect(bottom_rect):
					sprite_list.append(ninja.death_sprite)
		'''

		for sprite in sprites.gravity_effects:
			if self.sticky_rect.colliderect(sprite.rect):
				sprite_list.append(sprite)

		for sprite in self.attached_list:
			sprite_list.append(sprite)
			sprite.dirty = 1

		return sprite_list


		

class Pole(pygame.sprite.DirtySprite):
	def __init__(self, centerx, y_change, bottom_level, level_height): #floor span is how many floors the pole goes up
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'pole'
		self.ends = False
		if level_height != 'random':

			self.image = pygame.Surface((6, (y_change * level_height) - 16))
			self.image.fill((0,255,0), rect = None)
			self.rect = self.image.get_rect()
			self.rect.centerx = centerx
			self.rect.bottom = 60 + (y_change * (bottom_level - 1))



			self.top_rect = self.rect
			self.bottom_rect = self.rect

			#draw pole
			pole_pic = sprites.level_sheet.getImage(37, 21, 6, 6)
			i = 0
			while i < self.rect.height:
				self.image.blit(pole_pic, (0, i))
				i += pole_pic.get_height()

			pole_top = sprites.level_sheet.getImage(37, 14, 6, 6)
			self.image.blit(pole_top, (0,0))

			GREEN = (0,255,0)
			self.image.set_colorkey(GREEN)

			self.dirty = 1

			sprites.tile_list.add(self)
			sprites.active_sprite_list.add(self)
			sprites.active_sprite_list.change_layer(self, 4)

			self.collision_rect = (self.rect.x,self.rect.y - 1, self.rect.width, self.rect.height + 2)

		sprites.quadrant_handler.join_quadrants(self)

	def update(self):
		i = random.choice((0,1,2,3,4,5,6,7,8,9,10))
		if i == 5:
			death = True
			for tile in sprites.tile_list:
				if tile.type == 'platform' or tile.type == 'tile':
					if tile.rect.colliderect(self.collision_rect):
						death = False
						break
			if death is True:
				for ninja in sprites.ninja_list:
					if ninja.status == 'climb':
						if ninja.rect.colliderect(self.collision_rect):
							ninja.status = 'falling'
				self.pole_death()




	def pole_death(self):
		sprites.particle_generator.pole_death_particles(self.rect)
		self.kill()

class Rope(pygame.sprite.DirtySprite):
	def __init__(self, centerx, top, bottom, ends = False): #floor span is how many floors the pole goes up
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'pole'
		self.ends = ends

		self.image = pygame.Surface((6, bottom - top))
		self.image.fill((0,255,0), rect = None)
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.bottom = bottom

		self.top_rect = self.rect
		self.bottom_rect = self.rect

		#draw pole
		pole_pic = sprites.level_sheet.getImage(37, 21, 6, 6)
		i = 0
		while i < self.rect.height:
			self.image.blit(pole_pic, (0, i))
			i += pole_pic.get_height()

		if ends is True: #floating ends, needs top
			pole_top = sprites.level_sheet.getImage(37, 14, 6, 6)
			self.image.blit(pole_top, (0,0))
			pole_bottom = pygame.transform.flip(pole_top, False, True)
			self.image.blit(pole_bottom, (0,self.rect.height - 6))
		elif ends == 'top':
			pole_top = sprites.level_sheet.getImage(37, 14, 6, 6)
			self.image.blit(pole_top, (0,0))
		elif ends == 'bottom':
			print('made it!')
			pole_top = sprites.level_sheet.getImage(37, 14, 6, 6)
			pole_bottom = pygame.transform.flip(pole_top, False, True)
			self.image.blit(pole_top, (0,self.rect.height - 6))

		GREEN = (0,255,0)
		self.image.set_colorkey(GREEN)
		self.dirty = 1

		sprites.tile_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 4)

		self.collision_rect = (self.rect.x,self.rect.y - 1, self.rect.width, self.rect.height + 2)

		sprites.quadrant_handler.join_quadrants(self)

	def update(self):
		i = random.choice((0,1,2,3,4,5,6,7,8,9,10))
		if i == 5:
			death = True
			for tile in sprites.tile_list:
				if tile.type == 'platform' or tile.type == 'tile':
					if tile.rect.colliderect(self.collision_rect):
						death = False
						break
			if death is True:
				for ninja in sprites.ninja_list:
					if ninja.status == 'climb':
						if ninja.rect.colliderect(self.collision_rect):
							ninja.status = 'falling'
				self.pole_death()


	def pole_death(self):
		sprites.particle_generator.pole_death_particles(self.rect)
		self.kill()

def Collision_Check():
	#AAA colission code AAA#

	temp_list = [] #holds current ninjas. Want to remove ninjas as 'collision occurs'. Only react to one collision at a time per ninja.
	for ninja in sprites.ninja_list:
			ninja.local_collision_ID = 0 #start with NO collisions to send out.
			temp_list.append(ninja)

	
	for ninja in temp_list:
		for otherninja in temp_list:
			if ninja != otherninja and ninja.last_collision != otherninja.name and otherninja.last_collision != ninja.name: #and sprites.countdown_timer.done is True: #check countdown timer to make sure not dealing with old 'collisions'
				
				if ninja.collision_rect.colliderect(otherninja.collision_rect):
						
						#set fire
						if ninja.on_fire is True:
							otherninja.set_fire()
						if otherninja.on_fire is True:
							ninja.set_fire()

						otherninja_base_y = otherninja.change_y
						ninja_base_y = ninja.change_y

						temp_list.remove(ninja)
						temp_list.remove(otherninja)

						#create delay in next collision between these ninjas
						ninja.last_collision = otherninja.name
						ninja.FID_inflictor = otherninja
						ninja.last_collision_timer = 14

						otherninja.last_collision = ninja.name
						otherninja.FID_inflictor = ninja
						otherninja.last_collision_timer = 14

						#Find an estimate of the collision point. Used at end of collision calculations to generate splatter.
						overlap_rect = ninja.collision_rect.clip(otherninja.rect)
						splatter_point = overlap_rect.center

						#True if no space above or below
						ninja.tight_space = ninja.check_squished('collision')
						otherninja.tight_space = otherninja.check_squished('collision')

						#True if no space above or below
						ninja.tight_trip_space = ninja.check_squished('trip collision')
						otherninja.tight_trip_space = otherninja.check_squished('trip collision')


						#handles switching 'homing bombs'. POSSIBLY NOT NEEDED NOW
						for item in sprites.active_items:
							if item.type == 'homing_bomb':
								if item.collision_delay == 0:
									if item.target_ninja == ninja:
										item.collision_delay = 8
										item.target_ninja = otherninja
										ninja.stats_homing_bomb_transferred += 1
										otherninja.stats_homing_bomb_received += 1
									elif item.target_ninja == otherninja:
										item.collision_delay = 8
										item.target_ninja = ninja
										otherninja.stats_homing_bomb_transferred += 1
										ninja.stats_homing_bomb_received += 1

						if ninja.inverted_g is False:
							otherninja_rect_bottom = pygame.Rect(otherninja.rect.x, otherninja.rect.bottom - 6, otherninja.rect.width, 6)
							ninja_rect_bottom = pygame.Rect(ninja.rect.x, ninja.rect.bottom - 6, ninja.rect.width, 6)
						else:
							otherninja_rect_bottom = pygame.Rect(otherninja.rect.x, otherninja.rect.top, otherninja.rect.width, 6)
							ninja_rect_bottom = pygame.Rect(ninja.rect.x, ninja.rect.top, ninja.rect.width, 6)
						#to prevent rolls from acting weird when collisions are from above. Needs to hit bottom or it won't 'trip'
						if ninja.status == 'roll':
							if ninja_rect_bottom.colliderect(otherninja_rect_bottom):
								pass
							else:
								ninja.status = 'jump'

						if otherninja.status == 'roll':
							if otherninja_rect_bottom.colliderect(ninja_rect_bottom):
								pass
							else:
								otherninja.status = 'jump'

						#add collision check to see if 'bounced on head'
						ninja_stomped = False
						otherninja_stomped = False

						ninja.update_collision_rects()
						otherninja.update_collision_rects()

						if ninja.rect_bottom.colliderect(otherninja.rect_top):
							ninja_y_mod = 1.3
							ninja_x_mod = 0.7
							otherninja_y_mod = 1
							otherninja_x_mod = 1
							if ninja.item == 'metal suit' and otherninja.item not in ('volt') and otherninja.shield_sprite.active is False:
								if ninja.status == 'metal pound':
									if abs(ninja.rect.centerx - otherninja.rect.centerx) <= 18:
										otherninja_stomped = True
								#if (ninja.inverted_g is False and ninja.change_y > 5) or (ninja.inverted_g is True and ninja.change_y < -5):
								#if ninja.change_y != 0:
								#	otherninja_stomped = True
							if ninja.inverted_g is False: 
								ninja.rect.bottom = otherninja.rect.top
								#bonus mini collision check
								for tile in sprites.tile_list:
									if tile.type == 'tile':
										if tile.rect.colliderect(ninja.rect):
											ninja.rect.top = tile.rect.bottom
											ninja.set_true_xy('y')
											break
							else:
								ninja.rect.top = otherninja.rect.bottom
								ninja.set_true_xy('y')
								#bonus mini collision check
								for tile in sprites.tile_list:
									if tile.type == 'tile':
										if tile.rect.colliderect(ninja.rect):
											ninja.rect.bottom = tile.rect.top
											ninja.set_true_xy('y')
											break

						elif otherninja.rect_bottom.colliderect(ninja.rect_top):
							ninja_y_mod = 1
							ninja_x_mod = 1
							otherninja_y_mod = 1.3
							otherninja_x_mod = 0.7
							if otherninja.item == 'metal suit' and ninja.item not in ('volt') and ninja.shield_sprite.active is False:
								if otherninja.status == 'metal pound':
									if abs(ninja.rect.centerx - otherninja.rect.centerx) <= 18:
										ninja_stomped = True
								#if (otherninja.inverted_g is False and otherninja.change_y > 5) or (otherninja.inverted_g is True and otherninja.change_y < -5):
								#if otherninja.change_y != 0:
								#	ninja_stomped = True
							if otherninja.inverted_g is False:
								otherninja.rect.bottom = ninja.rect.top
								otherninja.set_true_xy('y')
								#bonus mini collision check
								for tile in sprites.tile_list:
									if tile.type == 'tile':
										if tile.rect.colliderect(otherninja.rect):
											otherninja.rect.top = tile.rect.bottom
											otherninja.set_true_xy('y')
											break
							else:
								otherninja.rect.top = ninja.rect.bottom
								#bonus mini collision check
								for tile in sprites.tile_list:
									if tile.type == 'tile':
										if tile.rect.colliderect(otherninja.rect):
											otherninja.rect.bottom = tile.rect.top
											otherninja.set_true_xy('y')
											break
						else:
							ninja_y_mod = 1
							ninja_x_mod = 1
							otherninja_y_mod = 1
							otherninja_x_mod = 1


						#set timer to temporarily lock out controls regardless of collision type.
						ninja.collision_timer = ninja.collision_timer_max
						otherninja.collision_timer = otherninja.collision_timer_max


						collision_center = int((ninja.rect.centerx + otherninja.rect.centerx)/2)
						max_knock_x = 1.6
						if ninja.inverted_g is False:
							max_knock_y = 3.6
						else:
							max_knock_y = -3.6

						#handles frozen ninjas.
						if ninja.status == 'frozen' or otherninja.status == 'frozen':
							if ninja.status == 'frozen' and otherninja.status == 'frozen': #both cubes

								if ninja.rect.centerx > otherninja.rect.centerx: #ninja on right
									ninja.change_x = ninja.ice_cube.knock_speed / 2
									otherninja.change_x = -(otherninja.ice_cube.knock_speed / 2)
								else: #otherninja on right
									ninja.change_x = -(ninja.ice_cube.knock_speed / 2)
									otherninja.change_x = otherninja.ice_cube.knock_speed / 2
							elif ninja.status == 'frozen':
								if otherninja.status == 'climb':
									otherninja.status = 'idle'
								if ninja.rect.centerx > otherninja.rect.centerx: #ninja on right
									ninja.change_x = ninja.ice_cube.knock_speed
									ninja.change_y = -(max_knock_y / 2)
									otherninja.change_x = -max_knock_x# / 2
									otherninja.change_y = -max_knock_y
								else: #otherninja on right
									ninja.change_x = -ninja.ice_cube.knock_speed
									ninja.change_y = -(max_knock_y / 2)
									otherninja.change_x = max_knock_x# / 2
									otherninja.change_y = -max_knock_y


							elif otherninja.status == 'frozen':
								if ninja.status == 'climb':
									ninja.status = 'idle'
								if ninja.rect.centerx > otherninja.rect.centerx: #ninja on right
									ninja.change_x = max_knock_x# / 2
									ninja.change_y = -max_knock_y
									otherninja.change_x = -otherninja.ice_cube.knock_speed
									otherninja.change_y = -(max_knock_y / 2)
								else: #otherninja on right
									ninja.change_x = -max_knock_x# / 2
									ninja.change_y = -max_knock_y
									otherninja.change_x = otherninja.ice_cube.knock_speed
									otherninja.change_y = -(max_knock_y / 2)

						if ninja.status == 'roll' and otherninja.status == 'roll':
							if abs(ninja.rect.centery - otherninja.rect.centery) < 5:
								#ninja.change_x *= -1
								#otherninja.change_x *= -1
								if ninja.rect.x < otherninja.rect.x:
									ninja.change_x = max_knock_x * -1
									otherninja.change_x = max_knock_x
									ninja.rect.right = otherninja.rect.left
									ninja.set_true_xy('x')
									ninja.direction = 'left'
									otherninja.direction = 'right'
								else:
									otherninja.change_x = max_knock_x * -1
									ninja.change_x = max_knock_x
									otherninja.rect.right = ninja.rect.left
									otherninja.set_true_xy('x')
									otherninja.direction = 'left'
									ninja.direction = 'right'
								#need noise because 'knocked status' won't activate it.
								sounds.mixer.knocked.play()

				

						elif ninja.status != 'frozen' and otherninja.status != 'frozen':
							#both win, both 'jump back'
							collision = False
							if collision is False and (ninja.status == 'metal pound' or otherninja.status == 'metal pound'):
								collision = True
								if ninja.status != 'metal pound':
									sounds.mixer.knocked.play()
									if ninja.rect.centerx <= otherninja.rect.centerx: #ninja on the left
										ninja.change_x = max_knock_x * -1
										ninja.change_y = max_knock_y * -1
									else: #ninja on the right
										ninja.change_x = max_knock_x
										ninja.change_y = max_knock_y * -1

								elif otherninja.status != 'metal pound':
									if otherninja.rect.centerx <= ninja.rect.centerx: #ninja on the left
										otherninja.change_x = max_knock_x * -1
										otherninja.change_y = max_knock_y * -1
									else: #ninja on the right
										otherninja.change_x = max_knock_x
										otherninja.change_y = max_knock_y * -1

							if collision is False and (ninja.status == 'jump' or ninja.status == 'roll' or ninja.status == 'duck'):
								if otherninja.status == 'jump' or otherninja.status == 'roll' or otherninja.status == 'duck':
									collision = True
									sounds.mixer.knocked.play()
									#both ninjas 'jump back'
									if ninja.rect.centerx <= otherninja.rect.centerx: #ninja on the left
										#ninja.rect.right = collision_center
										ninja.status = 'jump'
										ninja.change_x = max_knock_x * -1
										ninja.change_y = max_knock_y * -1
										#ninja.direction = 'left'
										

										#otherninja.rect.left = collision_center
										otherninja.status = 'jump'
										otherninja.change_x = max_knock_x
										otherninja.change_y = max_knock_y * -1
										#otherninja.direction = 'right'

									else: #ninja on the right
										#ninja.rect.left = collision_center
										ninja.status = 'jump'
										ninja.change_x = max_knock_x
										ninja.change_y = max_knock_y * -1
										#ninja.direction = 'right'

										#otherninja.rect.right = collision_center
										otherninja.status = 'jump'
										otherninja.change_x = max_knock_x * -1
										otherninja.change_y = max_knock_y * -1
										#otherninja.direction = 'left'



							




							#ninja wins
							if collision is False and (ninja.status == 'jump' or ninja.status == 'roll' or ninja.status == 'duck'):
								if otherninja.status != 'jump' and otherninja.status != 'roll': # and otherninja.status != 'falling':
									collision = True
									if ninja.status == 'jump':
										if ninja.rect.centerx < otherninja.rect.centerx - 1: #ninja on the left
											#ninja.rect.right = collision_center
											ninja.change_x = max_knock_x * -1
											ninja.change_y = max_knock_y * -1

											#otherninja.rect.left = collision_center
											otherninja.status = 'knocked'
											otherninja.frame_counter = 0
											sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x
											otherninja.change_y = max_knock_y * -1

										elif ninja.rect.centerx > otherninja.rect.centerx + 1: #ninja on theright
											#ninja.rect.left = collision_center
											ninja.change_x = max_knock_x
											ninja.change_y = max_knock_y * -1

											#otherninja.rect.right = collision_center
											otherninja.status = 'knocked'
											otherninja.frame_counter = 0
											sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x * -1
											otherninja.change_y = max_knock_y * -1

										else:
											#ninja.rect.right = collision_center
											if ninja.direction == 'right':
												i = 1
											else:
												i = -1
											ninja.change_x = max_knock_x * i
											ninja.change_y = max_knock_y * -1

											#otherninja.rect.left = collision_center
											otherninja.status = 'knocked'
											otherninja.frame_counter = 0
											sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x * (i * -1)
											otherninja.change_y = max_knock_y * (-1)

										if otherninja.tight_space is True:
											old_centery = otherninja.rect.centery
											otherninja.shrink('knocked')
											otherninja.rect.centery = old_centery
											otherninja.set_true_xy('xy')

									elif ninja.status == 'roll' or ninja.status == 'duck':
										if otherninja.inverted_g is False:
											
											if otherninja.tight_trip_space is True:
												otherninja.shrink('knocked')
											otherninja.rect.bottom = ninja.rect.top
											otherninja.set_true_xy('xy')
											sounds.mixer.knocked.play()
										else:
											#otherninja.rect.top = ninja.rect.bottom
											if otherninja.tight_trip_space is True:
												otherninja.shrink('knocked')
											otherninja.rect.top = ninja.rect.bottom
											otherninja.set_true_xy('xy')
											sounds.mixer.knocked.play()
										

										
										if ninja.rect.centerx <= otherninja.rect.centerx: #ninja on the left
											#ninja.change_x = max_knock_x * 1

											if otherninja.status not in ('jump', 'roll'):
												otherninja.status = 'knocked'
												otherninja.frame_counter = 0
												sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x * -1
											otherninja.change_y = max_knock_y * -1

										else: #ninja on theright
											#ninja.change_x = max_knock_x *-1

											if otherninja.status not in ('jump', 'roll'):
												otherninja.status = 'knocked'
												otherninja.frame_counter = 0
												sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x
											otherninja.change_y = max_knock_y * -1

										

							#other ninja wins
							if collision is False and (otherninja.status == 'jump' or otherninja.status == 'roll' or otherninja.status == 'duck'):
								if ninja.status != 'jump' and ninja.status != 'roll': # and ninja.status != 'falling':
									collision = True
									if otherninja.status == 'jump':	
										if otherninja.rect.centerx < ninja.rect.centerx - 1: #otherninja on the left
											#otherninja.rect.right = collision_center
											otherninja.change_x = max_knock_x * -1
											otherninja.change_y = max_knock_y * -1

											#ninja.rect.left = collision_center
											ninja.status = 'knocked'
											ninja.frame_counter = 0
											sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x
											ninja.change_y = max_knock_y * -1

										elif otherninja.rect.centerx > ninja.rect.centerx + 1: #otherninja on theright
											#otherninja.rect.left = collision_center
											otherninja.change_x = max_knock_x
											otherninja.change_y = max_knock_y * -1

											#ninja.rect.right = collision_center
											ninja.status = 'knocked'
											ninja.frame_counter = 0
											sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x * -1
											ninja.change_y = max_knock_y * -1

										else:
											#ninja.rect.right = collision_center
											if otherninja.direction == 'right':
												i = 1
											else:
												i = -1
											otherninja.change_x = max_knock_x * i
											otherninja.change_y = max_knock_y * -1

											#otherninja.rect.left = collision_center
											ninja.status = 'knocked'
											ninja.frame_counter = 0
											sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x * (i * -1)
											ninja.change_y = max_knock_y * (-1)

										if ninja.tight_space is True:
											old_centery = ninja.rect.centery
											ninja.shrink('knocked')
											ninja.rect.centery = old_centery
											ninja.set_true_xy('xy')

									elif otherninja.status == 'roll' or otherninja.status == 'duck':
										if ninja.inverted_g is False:
											if ninja.tight_trip_space is True:
												ninja.shrink('knocked')
											ninja.rect.bottom = otherninja.rect.top
											ninja.set_true_xy('xy')
											sounds.mixer.knocked.play()
										else:
											#ninja.rect.top = otherninja.rect.bottom
											if ninja.tight_trip_space is True:
												ninja.shrink('knocked')
												ninja.rect.top = otherninja.rect.bottom
											ninja.set_true_xy('xy')
											sounds.mixer.knocked.play()

										if otherninja.rect.centerx <= ninja.rect.centerx: #otherninja on the left
											#otherninja.change_x = max_knock_x

											if ninja.status not in ('jump', 'roll'):
												ninja.status = 'knocked'
												ninja.frame_counter = 0
												sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x * -1
											ninja.change_y = max_knock_y * -1

										else: #otherninja on theright
											#otherninja.change_x = max_knock_x * -1

											if ninja.status not in ('jump', 'roll'):
												ninja.status = 'knocked'
												ninja.frame_counter = 0
												sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x
											ninja.change_y = max_knock_y * -1
									'''
									#modify for tight quarters:
									if otherninja.tight_space is True:
										otherninja.shrink('knocked')
										if otherninja.inverted_g is False:
											otherninja.rect.top = otherninja.tight_top_tile.rect.bottom
										else:
											otherninja.rect.bottom = otherninja.tight_bottom_tile.rect.top
									#modify for tight quarters:
									if ninja.tight_space is True:
										ninja.shrink('knocked')
										if ninja.inverted_g is False:
											ninja.rect.top = ninja.tight_top_tile.rect.bottom
										else:
											ninja.rect.bottom = ninja.tight_bottom_tile.rect.top
									'''

							
							#one ninja pushed other.
							if collision is False and otherninja.status != 'jump' and otherninja.status != 'roll' and (ninja.change_x == 0 or otherninja.change_x == 0) and (ninja.change_x != 0 or otherninja.change_x != 0) and otherninja.status != 'knocked' and ninja.status != 'knocked':
								if ninja.status != 'jump' and ninja.status != 'roll' and ninja.status != 'falling' and otherninja.status != 'falling':
									collision = True

									if otherninja.rect.centerx <= ninja.rect.centerx: #otherninja on the left
										if ninja.change_x != 0 and otherninja.change_x == 0:
											otherninja.rect.right = ninja.rect.left
											otherninja.set_true_xy('x')
											for tile in sprites.tile_list:
												if tile.type == 'tile':
													if tile.rect.colliderect(otherninja.rect):
														otherninja.rect.left = tile.rect.right
														otherninja.set_true_xy('x')
														break
											otherninja.status = 'knocked'
											otherninja.frame_counter = 0
											sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x * -1
											otherninja.change_y -= max_knock_y

											#ninja.rect.left = collision_center
											ninja.status = 'falling'
											ninja.change_x = max_knock_x / 2
											ninja.change_y -= max_knock_y / 2

										elif ninja.change_x == 0 and otherninja.change_x != 0:
											#otherninja.rect.right = ninja.rect.left_rect
											otherninja.status = 'falling'
											otherninja.change_x = max_knock_x * -1 / 2
											otherninja.change_y -= max_knock_y / 2
											
											ninja.rect.left = otherninja.rect.right
											ninja.set_true_xy('x')
											for tile in sprites.tile_list:
												if tile.type == 'tile':
													if tile.rect.colliderect(ninja.rect):
														ninja.rect.right = tile.rect.left
														ninja.set_true_xy('x')
														break
											ninja.status = 'knocked'
											ninja.frame_counter = 0
											sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x
											ninja.change_y -= max_knock_y

									else: #otherninja on theright
										if ninja.change_x != 0 and otherninja.change_x == 0:
											otherninja.rect.left = ninja.rect.right
											otherninja.set_true_xy('x')
											for tile in sprites.tile_list:
												if tile.type == 'tile':
													if tile.rect.colliderect(otherninja.rect):
														otherninja.rect.right = tile.rect.left
														otherninja.set_true_xy('x')
														break
											otherninja.status = 'knocked'
											otherninja.frame_counter = 0
											sounds.mixer.knocked.play()
											otherninja.change_x = max_knock_x
											otherninja.change_y -= max_knock_y

											#ninja.rect.right = collision_center
											ninja.status = 'falling'
											ninja.change_x = max_knock_x * -1 / 2
											ninja.change_y -= max_knock_y / 2

										if ninja.change_x == 0 and otherninja.change_x != 0:
											#otherninja.rect.left = collision_center
											otherninja.status = 'falling'
											otherninja.change_x = max_knock_x / 2
											otherninja.change_y -= max_knock_y / 2

											ninja.rect.right = otherninja.rect.left
											ninja.set_true_xy('x')
											for tile in sprites.tile_list:
												if tile.type == 'tile':
													if tile.rect.colliderect(ninja.rect):
														ninja.rect.left = tile.rect.right
														ninja.set_true_xy('x')
											ninja.status = 'knocked'
											ninja.frame_counter = 0
											sounds.mixer.knocked.play()
											ninja.change_x = max_knock_x * -1
											ninja.change_y -= max_knock_y

									#modify for tight quarters:
									if ninja.tight_space is True:
										if ninja.status == 'knocked':
											ninja.shrink('knocked')
											ninja.set_true_xy('xy')
										else:
											ninja.shrink('knocked')
											ninja.set_true_xy('xy')
											ninja.roll_timer = 1
										if ninja.inverted_g is False:
											ninja.rect.top = ninja.tight_top_tile.rect.bottom
											ninja.set_true_xy('y')
										else:
											ninja.rect.bottom = ninja.tight_bottom_tile.rect.top
											ninja.set_true_xy('y')

									if otherninja.tight_space is True:
										if otherninja.status == 'knocked':
											otherninja.shrink('knocked')
											otherninja.set_true_xy('xy')
										else:
											otherninja.shrink('knocked')
											otherninja.set_true_xy('xy')
											otherninja.roll_timer = 1
										if otherninja.inverted_g is False:
											otherninja.rect.top = otherninja.tight_top_tile.rect.bottom
											otherninja.set_true_xy('y')
										else:
											otherninja.rect.bottom = otherninja.tight_bottom_tile.rect.top
											otherninja.set_true_xy('y')


							#both lose only activate if one ninja hasn't pusched the other.
							if collision is False and otherninja.status != 'jump' and otherninja.status != 'roll':
								if ninja.status != 'jump' and ninja.status != 'roll':
									collision = True
									if otherninja.rect.centerx <= ninja.rect.centerx: #otherninja on the left
										#otherninja.rect.right = collision_center
										otherninja.status = 'knocked'
										otherninja.frame_counter = 0
										sounds.mixer.knocked.play()
										otherninja.change_x = max_knock_x * -1
										otherninja.change_y = -max_knock_y

										#ninja.rect.left = collision_center
										ninja.status = 'knocked'
										ninja.frame_counter = 0
										sounds.mixer.knocked.play()
										ninja.change_x = max_knock_x
										ninja.change_y = -max_knock_y

									else: #otherninja on theright
										#otherninja.rect.left = collision_center
										otherninja.status = 'knocked'
										otherninja.frame_counter = 0
										sounds.mixer.knocked.play()
										otherninja.change_x = max_knock_x
										otherninja.change_y = -max_knock_y

										#ninja.rect.right = collision_center
										ninja.status = 'knocked'
										ninja.frame_counter = 0
										sounds.mixer.knocked.play()
										ninja.change_x = max_knock_x * -1
										ninja.change_y = -max_knock_y

									#modify for tight quarters:
									if ninja.tight_space is True:
										ninja.shrink('knocked')
										ninja.set_true_xy('xy')
										if ninja.inverted_g is False:
											ninja.rect.top = ninja.tight_top_tile.rect.bottom
											ninja.set_true_xy('y')
										else:
											ninja.rect.bottom = ninja.tight_bottom_tile.rect.top
											ninja.set_true_xy('y')
									#modify for tight quarters:
									if otherninja.tight_space is True:
										otherninja.shrink('knocked')
										otherninja.set_true_xy('xy')
										if otherninja.inverted_g is False:
											otherninja.rect.top = otherninja.tight_top_tile.rect.bottom
											otherninja.set_true_xy('y')
										else:
											otherninja.rect.bottom = otherninja.tight_bottom_tile.rect.top
											otherninja.set_true_xy('y')
						
						
						#prevent excessive vertical bumb
						if ninja.inverted_g is False:
							if ninja.change_y < ninja.jump_force:
								ninja.change_y = ninja.jump_force
							if otherninja.change_y < otherninja.jump_force:
								otherninja.change_y = otherninja.jump_force
						else:
							if ninja.change_y > ninja.jump_force * -1:
								ninja.change_y = ninja.jump_force * -1
							if otherninja.change_y > otherninja.jump_force * -1:
								otherninja.change_y = otherninja.jump_force * -1
						
						
						#Extra collision check, mostly for 'vertical bumps'. Prevents ninjas from going into ceiling.
						'''
						for tile in sprites.tile_list:
							if tile.type == 'tile':
								if tile.rect.colliderect(ninja.rect):
									if ninja.inverted_g is False:
										ninja.rect.top = tile.rect.bottom
									else:
										ninja.rect.bottom = tile.rect.top
									break
						for tile in sprites.tile_list:
							if tile.type == 'tile':
								if tile.rect.colliderect(otherninja.rect):
									if otherninja.inverted_g is False:
										otherninja.rect.top = tile.rect.bottom
									else:
										otherninja.rect.bottom = tile.rect.top
									break
						'''

						#Modify collision vectors if hit top or bottom of ninjas (more vertical collision)
						'''
						if ninja.status != 'knocked':
							ninja.change_y *= ninja_y_mod
							ninja.change_x *= ninja_x_mod
						if otherninja.status != 'knocked':
							otherninja.change_y *= otherninja_y_mod
							otherninja.change_x *= otherninja_x_mod
						'''

						#add basic x / y mods
						ninja.change_y *= ninja_y_mod
						ninja.change_x *= ninja_x_mod
						otherninja.change_y *= otherninja_y_mod
						otherninja.change_x *= otherninja_x_mod

						#Mod for 'metal suit'
						suit_x = 1.5
						suit_y = 1.5
						if ninja.item == 'metal suit' and otherninja.item == 'metal suit':
							if otherninja_stomped is True:
								'''
								if ninja.inverted_g is False:
									ninja.rect.bottom = otherninja.rect.top
									ninja.true_y = ninja.rect.y
									ninja.change_y = -1
								else:
									ninja.rect.top = otherninja.rect.bottom
									ninja.true_y = ninja.rect.y
									ninja.change_y = 1
								'''
								otherninja.activate_death_sprite('metal suit', ninja)
							if ninja_stomped is True:
								'''
								if otherninja.inverted_g is False:
									otherninja.rect.bottom = ninja.rect.top
									otherninja.true_y = ninja.rect.y
									otherninja.change_y = -1
								else:
									otherninja.rect.top = ninja.rect.bottom
									otherninja.true_y = ninja.rect.y
									otherninja.change_y = 1
								'''
								ninja.activate_death_sprite('metal suit', otherninja)
						
						elif ninja.item == 'metal suit':
							ninja.change_x /= suit_x
							ninja.change_y /= suit_y
							otherninja.change_x *= suit_x
							otherninja.change_y *= suit_y
							if otherninja_stomped is True:
								otherninja.activate_death_sprite('metal suit', ninja)
								#if ninja.status == 'knocked':
								#	ninja.status = 'falling'
						elif otherninja.item == 'metal suit':
							otherninja.change_x /= suit_x
							otherninja.change_y /= suit_y
							ninja.change_x *= suit_x
							ninja.change_y *= suit_y
							if ninja_stomped is True:
								ninja.activate_death_sprite('metal suit', otherninja)
								#if otherninja.status == 'knocked':
								#	otherninja.status = 'falling'

						#collect stats
						if ninja.status == 'knocked':
							ninja.stats_knocks_received += 1
							otherninja.stats_knocks_inflicted += 1
						if otherninja.status == 'knocked':
							otherninja.stats_knocks_received += 1
							ninja.stats_knocks_inflicted += 1

						'''
						#Generate collision splatter - NOT IN USE
						if ninja.status == 'knocked':
							sprites.particle_generator.ninja_collision_particles(ninja.rect.center, splatter_point, ninja.inverted_g)
						if otherninja.status == 'knocked':
							sprites.particle_generator.ninja_collision_particles(otherninja.rect.center, splatter_point, otherninja.inverted_g)
						'''

						#fix infinite knocks on edge of 'loop physics' levels.
						if ninja.status == 'knocked':
							if ninja.change_x > 0:
								if ninja.rect.left >= sprites.size[0]:
									ninja.rect.right = 0
									ninja.set_true_xy('x')
							elif ninja.change_x < 0: 
								if ninja.rect.right <= 0:
									ninja.rect.left = sprites.size[0]
									ninja.set_true_xy('x')
							if ninja.status != 'frozen':
								ninja.knock_timer = ninja.max_knock_timer

						if otherninja.status == 'knocked':
							if otherninja.change_x > 0:
								if otherninja.rect.left >= sprites.size[0]:
									otherninja.rect.right = 0
									otherninja.set_true_xy('x')
							elif otherninja.change_x < 0: 
								if otherninja.rect.right <= 0:
									otherninja.rect.left = sprites.size[0]
									otherninja.set_true_xy('x')
							if otherninja.status != 'frozen':
								otherninja.knock_timer = otherninja.max_knock_timer

						#To prevent FID errors.
						if otherninja.FID is True:
							otherninja.change_y = otherninja_base_y
						if ninja.FID is True:
							ninja.change_y = ninja_base_y



def check_win():
	#Only check for win if OFFLINE play OR if hosting online play. Triggers new match from versus score.
	if options.game_state == 'level':
		if len(sprites.player_list) == 1: #online and other players quit:
			sounds.mixer.menu_select.play()
			options.game_state = 'versus_level_selection'
			level_builder.level_reset()
			sounds.mixer.change_song('music_menu.wav')
			sounds.mixer.start_song()
			sprites.player1.text_sprite.activate('All Players Have Disconnected.', options.RED_LIST[2], (320, 13), 120)


	if options.game_state in ('level', 'online_pause') and sprites.transition_screen.status == 'idle':
		if options.game_mode == 'versus' and options.win_condition in ('Practice', 'Stock'):
			for ninja in sprites.player_list:
				if ninja not in sprites.ninja_list and ninja.spawn_sprite.status == 'idle' and ninja.death_sprite.active is False:
					ninja.respawn_timer += 1
					if ninja.respawn_timer > 60 and (options.win_condition == 'Practice' or ninja.lives >= 0):
							if len(level_builder.spawn_options) == 0:
								level_builder.spawn_options = level_builder.starting_positions.copy()
							
							rising_mallow = False
							for tile in sprites.tile_list:
								if tile.type == 'mallow' and tile.subtype == 'rising mallow':
									rising_mallow = True

									if tile.status == 'idle':
										safe_dist = tile.rect.top
									else:
										safe_dist = tile.rect.top + 60

									break

							inverted_g = False
							moving_platform = False
							specific_tile = None
							if len(level_builder.moving_platform_spawn_options) > 0:
								moving_platform = True
								
								#safe system used to screen for lower logs.
								safe = False
								while safe is False:
									specific_tile = random.choice(level_builder.moving_platform_spawn_options)
									i = (specific_tile.rect.centerx, specific_tile.rect.top - 24)
									if specific_tile.log is False or specific_tile.rect.top < 260:
										safe = True
									


							else: #everything else
								#If gravity barriers exist, choose the appropriate point list based on current gravity.
								if len(level_builder.inverted_spawn_options) == 0:
									i = random.choice(level_builder.spawn_options)
								else:
									done = False
									if len(sprites.gravity_objects) > 0:
										while done is False:
											choice = random.choice((1,2))
											if choice == 1: #regular
												i = random.choice(level_builder.spawn_options)
												for barrier in sprites.gravity_objects:
													inverted_g = barrier.return_gravity_point(i)
													if inverted_g is False:
														done = True
											if choice == 2: #inverted
												i = random.choice(level_builder.inverted_spawn_options)
												for barrier in sprites.gravity_objects:
													inverted_g = barrier.return_gravity_point(i)
													if inverted_g is True:
														done = True
									else:
										if options.inverted_g is True:
											i = random.choice(level_builder.inverted_spawn_options)
											inverted_g = True
										else:
											i = random.choice(level_builder.spawn_options)
											inverted_g = False

							if ninja.respawn_timer < 180:
								temp_rect = pygame.Rect(i[0] - 125, i[1] - 60, 250, 120) 
							elif ninja.respawn_timer < 240:#make smaller rect if having trouble sapwning.
								temp_rect = pygame.Rect(i[0] - 48, i[1] - 40, 48 * 2, 80)
							else:
								temp_rect = pygame.Rect(i[0] - 11, i[1] - 24, 22, 48)

							spawn = True
							
							if rising_mallow is True:
								if i[1] > safe_dist:
									spawn = False

							for other_ninja in sprites.player_list:
								if other_ninja.spawn_sprite.status != 'idle':
									if other_ninja.spawn_sprite.rect.colliderect(temp_rect):
										if ninja.respawn_timer < 300:
												spawn = False
												break

								else:
									if other_ninja in sprites.ninja_list:
										if other_ninja.rect.colliderect(temp_rect):
											if ninja.respawn_timer < 300:
												spawn = False
												break

							if ninja.respawn_timer > 300:
								spawn = True

							#for other_ninja in sprites.ninja_list:
							#	if other_ninja.spawn_sprite.rect.colliderect(temp_rect):
							#		spawn = False
							#		break

							for tile in sprites.tile_list:
								if tile.type == 'mallow' and tile.subtype == 'rising mallow':
									if tile.rect.colliderect(temp_rect):
										spawn = False
										break

							if spawn is True and moving_platform is False: #Don't need check in moving platorm levels.
								#make sure tile not destroy:
								spawn = False
								temp_rect = pygame.Rect(i[0] - 5, i[1] - 28, 10, 56)
								for tile in sprites.tile_list:
									if tile.type in ('tile','platform'):
										if tile.rect.colliderect(temp_rect):
											spawn = True
											break

								#make sure top is open
								temp_rect = pygame.Rect(i[0] - 5, i[1] - 22, 10, 44)
								for tile in sprites.tile_list:
									if tile.type in ('tile','platform'):
										if tile.rect.colliderect(temp_rect):
											spawn = False
											break

							if spawn is True:
								ninja.respawn_timer = 0
								if moving_platform is False:
									ninja.place_ninja(i, phase_in=True, inverted_g = inverted_g)
								else:
									ninja.place_ninja(i, phase_in=True, inverted_g = inverted_g, moving_platform = specific_tile)

								if options.versus_mode == 'Stock':
									#ninja.name_bar.activate()
									ninja.stock_bar.update_score()
									ninja.stock_bar.activate(source = 'stock')

			#Check for stock win
			if options.versus_mode == 'Stock':
				win = True

				for ninja in sprites.player_list: #block game from ending before death animations finish
					if ninja.death_sprite.active is True:
						win = False

				#see who's left
				alive_list = []
				for sprite in sprites.player_list:
					if sprite.lives >= 0:
						alive_list.append(sprite)
				
				if len(alive_list) > 1: #if any ninjas aren't on the same team but ARE alive, keep playing
					color = alive_list[0].color
					for ninja in alive_list:
						if ninja.color != color:
							win = False


				if win is True or len(alive_list) == 0:
					options.win_timer -= 1 * (60 / options.current_fps)
					for sprite in sprites.ninja_list:
						sprite.smug = True

					if options.win_timer <= 0:
						options.win_timer = 300
						options.game_state = 'versus_awards'

						pygame.mixer.stop()
						for sprite in sprites.player_list:
							sprite.duels_participated += 1
					

						options.change_g = 0.3
						options.max_g = 5.1


		if options.game_mode == 'versus' and options.win_condition == 'Points':
			win = True
			
			for ninja in sprites.player_list: #block game from ending before death animations finish
				if ninja.death_sprite.active is True:
					win = False

			for sprite in sprites.ninja_list:
				for othersprite in sprites.ninja_list:
					if sprite.color != othersprite.color:
						win = False

			if win is True or len(sprites.ninja_list) == 0:
				for sprite in sprites.ninja_list:
					sprite.smug = True




				options.win_timer -= 1 * (60 / options.current_fps)

				if options.win_timer <= 0:
					options.win_timer = 300
					for sprite in sprites.ninja_list:
						if sprite.win is False and sprite.FID is False:
							sprite.win = True
							VP_change = 0
							if options.versus_VP_per_duel_win == '+1 For Last Human/Team Left Standing':
								VP_change = 1
							elif options.versus_VP_per_duel_win == '+2 For Last Human/Team Left Standing':
								VP_change = 2
							elif options.versus_VP_per_duel_win == '+1 For Each Human Left Standing':
								VP_change = 1 * len(sprites.ninja_list)
							elif options.versus_VP_per_duel_win == '+2 For Each Human Left Standing':
								VP_change = 2 * len(sprites.ninja_list)

							sprite.current_VP += VP_change
							sprite.VP_earned += VP_change

					for sprite in sprites.player_list: #now make sure even 'dead' teammates get credit
						for othersprite in sprites.player_list:
							if othersprite.color == sprite.color: #make sure dead sprite credited with team win.
								if othersprite.current_VP < sprite.current_VP:
									othersprite.current_VP = sprite.current_VP

					options.game_state = 'versus_score'
					#sprites.player1.test_stats()
					pygame.mixer.stop()
					for sprite in sprites.player_list:
						sprite.duels_participated += 1
						if sprite in sprites.ninja_list: #survived:
							sprite.stats_duels_survived += 1



					options.change_g = 0.3
					options.max_g = 5.1

		if options.game_mode == 'versus' and options.win_condition == 'Wins':
			win = True
			
			for ninja in sprites.player_list: #block game from ending before death animations finish
				if ninja.death_sprite.active is True:
					win = False

			for sprite in sprites.ninja_list:
				for othersprite in sprites.ninja_list:
					if sprite.color != othersprite.color:
						win = False

			if win is True or len(sprites.ninja_list) == 0:
				for sprite in sprites.ninja_list:
					sprite.smug = True


				options.win_timer -= 1 * (60 / options.current_fps)
				


				if options.win_timer <= 0:
					options.win_timer = 300
					for sprite in sprites.ninja_list:
						if sprite.win is False and sprite.FID is False:
							sprite.win = True
							sprite.current_wins += 1
							sprite.wins_earned += 1

					for sprite in sprites.player_list: #now make sure even 'dead' teammates get credit
						for othersprite in sprites.player_list:
							if othersprite.color == sprite.color: #make sure dead sprite credited with team win.
								if othersprite.current_wins < sprite.current_wins:
									othersprite.current_wins = sprite.current_wins

					

					options.game_state = 'versus_score'
					#sprites.player1.test_stats()
					pygame.mixer.stop()
					for sprite in sprites.player_list:
						sprite.duels_participated += 1
						if sprite in sprites.ninja_list: #survived:
							sprite.stats_duels_survived += 1


					
					options.change_g = 0.3
					options.max_g = 5.1

level_builder = None

class Level_Builder():

	def __init__(self):
		 #sssssssss

		 self.versus_dict = {'The Colliseum' : ('The Colliseum', [(100,30), (540,30), (100,290), (540,290)]),
							'Mt Olympus' : ('Mt Olympus', [(260,225), (375,225), (100,286), (540,286)]),
							'The Crucible' : ('The Crucible', [(200,312), (440,312), (100,312), (540,312)]),
							'Dimension M' : ('Dimension M', [(124,30), (516,30), (124,280), (516,280)]),
							'Decrepit Tower' : ('Decrepit Tower', [(176,312), (272,312), (368,312), (464,312)]),
							'Densinium Caves' : ('Densinium Caves', [(176,264), (272,56), (368,264), (464,56)]),
							'Retro Falls' : ('Retro Falls', [(176,130), (272,130), (368,130), (464,130)]),
							'Secret Lab' : ('Secret Lab', [(212,106), (212,156), (428,156), (428,106)]),
							'Ancient Tomb' : ('Ancient Tomb', [(64,312), (212,312), (428,312), (576,312)]),
							'Frozen Ruins' : ('Frozen Ruins',  [(102,200), (102,56), (538,200), (538,56)]),
							'Moon Base 7' : ('Moon Base 7', [(100,30), (540,30), (100,290), (540,290)]),
							'Testing' : ('Testing', [(176 + 50,230), (272,230), (368,230), (464 - 50,230)]),

							'Tutorial' : ('Tutorial', [(176 + 50,230), (272,230), (368,230), (464 - 50,230)]),
									}


		 self.current_level = None #holds the current level for manipulating
		 self.starting_positions = None
		 self.item_options = None #holds the current level 'item_list'.
		 self.spawn_options = []

		 self.seed = random.randrange(0,99999999999,1)
	
	def level_reset(self, light_reset = False):
		#options.win_condition = 'versus'
		#options.pause_item_options = False

		if menus.online_pause_handler.menu_created is True:
			menus.online_pause_handler.reset()
			controls.input_handler.remove_controls()

		
		self.passive_dict = {} #holds things that probably don't need constant info sent.
		self.active_dict = {} #holds things that need to be updated each round. Sent out by 'host'.
		self.key_number = 0


		options.change_g = 0.3
		options.max_g = 5.1
		options.inverted_g = False

		options.win_timer = 300

		for ninja in sprites.player_list:
			ninja.lives = options.max_lives




		self.spawn_options = []
		self.inverted_spawn_options = []
		self.moving_platform_spawn_options = []

		if options.game_mode == 'versus':
			if options.versus_mode == 'Classic':
				options.win_condition = 'Wins'
				options.pause_item_options = False

			elif options.versus_mode == 'Points':
				options.win_condition = 'Points'
				options.pause_item_options = False

			elif options.versus_mode == 'Stock':
				options.win_condition = 'Stock'
				options.pause_item_options = False

			elif options.versus_mode == 'Practice':
				options.win_condition = 'Practice'
				options.pause_item_options = True

			elif options.versus_mode == 'Tutorial':
				options.win_condition = 'Tutorial'
				options.pause_item_options = False #turns itself on when needed.


		#options.win_condition = 'practice'
		#options.pause_item_options = True
		
		options.banned_items = [] #holds items banned in that level


		sprites.active_items = []

		for ninja in sprites.player_list:
			ninja.reset()

		for sprite in sprites.tile_list:
			#sprite.remove(sprites.tile_list, sprites.active_sprite_list)
			sprite.kill()

		for sprite in sprites.level_objects:
			sprite.kill()

		for sprite in sprites.background_objects:
			sprite.kill()

		sprites.particle_generator.reset()

		sprites.transition_screen.fade(None, False, options.GREEN, timer = True)
		sounds.mixer.background_music = None
		sounds.mixer.clear_temp_sounds()


		self.seed = random.randrange(0,99999999999,1)

		random.seed(self.seed)

		#select new random level if options tells us to.
		if options.stage_selection == 'Random Each Duel':
			#randomly choose NOT testing or tutorial, but any other from list.
			key = None
			while key not in menus.versus_level_selection_sprite.unlocked_level_list:
				key = random.choice(list(self.versus_dict))
			self.current_level = self.versus_dict[key]


			
		if light_reset is False:



			self.build_level(self.current_level[0])

			#For AI purposes
			for tile in sprites.tile_list:
				if tile.type in ('tile', 'platform'):
					tile.find_neighbors()

			if self.starting_positions == None:
				self.starting_positions = self.current_level[1].copy()

			self.temp_starting_positions = self.starting_positions.copy()
			
			for ninja in sprites.ninja_list:
				i = random.choice(self.temp_starting_positions)
				ninja.place_ninja(i)
				#ninja.rect.centerx = i[0]
				#ninja.rect.centery = i[1]
				self.temp_starting_positions.remove(i)
				if ninja.rect.centerx < sprites.size[0] / 2:
					ninja.direction = 'right'

				elif ninja.rect.centerx > sprites.size[0] / 2:
					ninja.direction = 'left'

				#ninja.current_VP = 0
				#ninja.current_wins = 0
				#ninja.reset_stats()
				ninja.matches_participated += 1

				ninja.online_starting_position = ninja.rect.center #host will pass these to other CPUs. Overrides their decision.

				ninja.name_bar.activate()

				if options.versus_mode in ('Stock', 'Practice'):
					ninja.stock_bar.update_score()
					ninja.stock_bar.activate()
				else:
					ninja.score_bar.update_score()
					ninja.score_bar.activate()

				versus_mode = 'Classic' #classic, stock, practice, tutorial
				#911
		#sprites.versus_match_sprite.activate()



	def build_level(self, level_name):
		self.starting_positions = None
		options.inverted_g = False
		options.level_builder = self

		if level_name == 'The Colliseum':
			self.build_versus_classic()
		elif level_name == 'Mt Olympus':
			self.build_versus_olympus()
		elif level_name == 'The Crucible':
			self.build_versus_crucible()
		elif level_name == 'Dimension M':
			self.build_versus_paradox()
		elif level_name == 'Decrepit Tower':
			self.build_versus_tartarus()
		elif level_name == 'Densinium Caves':
			self.build_versus_mystic_cavern()
		elif level_name == 'Retro Falls':
			self.build_versus_falls()
		elif level_name == 'Secret Lab':
			self.build_versus_pump()
		elif level_name == 'Ancient Tomb':
			self.build_versus_labyrinth()
		elif level_name == 'Frozen Ruins':
			self.build_versus_ice()
		elif level_name == 'Moon Base 7':
			self.build_versus_space()
		elif level_name == 'Testing':
			self.build_versus_testing()

		elif level_name == 'Tutorial':
			self.build_versus_tutorial()

	def build_versus_classic(self):
		random.seed(self.seed)
		#random.seed(11)

		sounds.mixer.change_song('music_classic.wav')
		sounds.mixer.background_music.set_volume(options.music_volume)

		#pygame.draw.rect(sprites.screen, (0,0,0), (0, 0, sprites.screen.get_width(), sprites.screen.get_height()), 0)
		menus.pause_sprite.visible = 0
		menus.pause_sprite.dirty = 1

		#create a pole list. Just used for replacing them with ropes later.
		pole_list = []

		for ninja in sprites.ninja_list:
			ninja.loop_physics = False
		options.loop_physics = False

		self.item_options = []
		for entry in options.items_dict.keys():
			if options.items_dict[entry] == 'on':
				if entry != 'gravity':
					self.item_options.append(str(entry))


		options.banned_items = ['gravity']

		background = Level_Background(-9, 'background_classic.png')
		
		#moved as we need 'unimportant visual things at the end. Prevents breaking of 'seed' system.
		#window = Window((0,46,640,98), -12, 'classic')
		#screen = TV_Screen((120,5), sprites.screen ,sprites.player1, -8)
		#screen = TV_Screen((422,5), sprites.screen ,sprites.player2, -8)
		



		#level_choice = random.choice((1,2,3,4,5,6,7,8,9,10))
		level_choice = random.choice((1,1,1,1,1,3,4,5))
		#level_choice = 6

		if level_choice in (1,2):
			classic_door = Classic_Door((253,14), -10, None)
			mallow = Mallow((0,330,640,30), False)

		elif level_choice == 3:
			classic_door = Classic_Door((253,14), -10, None)
			mallow = Rising_Mallow((6,180,640 - 6 - 6,184) , False) #184
			alarm = Mallow_Alarm(56,30, -8, mallow, None)
			alarm = Mallow_Alarm(584,30, -8, None, alarm)


		elif level_choice == 4: #All possible enemys
			classic_door = Classic_Door((253,14), -10, ['slime'])
			mallow = Mallow((0,330,640,30), False)

		elif level_choice == 5: #All possible enemys
			classic_door = Classic_Door((253,14), -10, ['volcanic slime'])
			mallow = Mallow((0,330,640,30), False)

		elif level_choice == 6:
			classic_door = Classic_Door((253,14), -10, ['wheel', 'wheel', 'laser wheel'])
			#classic_door = Classic_Door((253,14), -10, ['wheel', 'slime'])
			#create rising mallow
			choice = random.choice((1,2,3,4,5))
			#choice = 1
			if choice == 1:
				mallow = Rising_Mallow((6,180,640 - 6 - 6,184) , False)
				alarm = Mallow_Alarm(56,30, -8, mallow, None)
				alarm = Mallow_Alarm(584,30, -8, None, alarm)
			else:
				mallow = Mallow((0,330,640,30), False)

		elif level_choice == 7:
			classic_door = Classic_Door((253,14), -10, ['wheel'])
			#create rising mallow
			choice = random.choice((1,2,3,4,5))
			if choice == 1:
				mallow = Rising_Mallow((6,180,640 - 6 - 6,184) , False)
				alarm = Mallow_Alarm(56,30, -8, mallow, None)
				alarm = Mallow_Alarm(584,30, -8, None, alarm)
			else:
				mallow = Mallow((0,330,640,30), False)

		elif level_choice == 8: #just laser whele
			classic_door = Classic_Door((253,14), -10, ['laser wheel'])
			#create rising mallow
			choice = random.choice((1,2,3,4,5))
			if choice == 1:
				mallow = Rising_Mallow((6,180,640 - 6 - 6,184) , False)
				alarm = Mallow_Alarm(56,30, -8, mallow, None)
				alarm = Mallow_Alarm(584,30, -8, None, alarm)
			else:
				mallow = Mallow((0,330,640,30), False)
		
		elif level_choice == 9: #All possible enemys
			classic_door = Classic_Door((253,14), -10, ['laser wheel', 'wheel', 'slime'])
			mallow = Mallow((0,330,640,30), False)

		elif level_choice == 10: #EVERYTHING except slime
			classic_door = Classic_Door((253,14), -10, ['laser wheel', 'wheel'])
			#create rising mallow
			choice = random.choice((1,2,3,4,5))
			if choice == 1:
				mallow = Rising_Mallow((6,180,640 - 6 - 6,184) , False)
				alarm = Mallow_Alarm(56,30, -8, mallow, None)
				alarm = Mallow_Alarm(584,30, -8, None, alarm)
			else:
				mallow = Mallow((0,330,640,30), False)

		
		#mallow = Mallow((0,330,640,30), False)

		#create rising mallow
		#mallow = Rising_Mallow((6,180,640 - 6 - 6,184) , False)
		#alarm = Mallow_Alarm(56,30, -8, mallow, None)
		#alarm = Mallow_Alarm(584,30, -8, None, alarm)

		
		#wheel = Wheel_Enemy((360,0), None)

		#create opening door
		#classic_door = Classic_Door((253,14), -10, ['laser wheel'])

		'''
		enemy = Slime_Enemy((320,0))
		enemy = Slime_Enemy((random.randrange(100,500,1),0))
		enemy = Slime_Enemy((random.randrange(100,500,1),0))
		enemy = Slime_Enemy((random.randrange(100,500,1),0))
		enemy = Slime_Enemy((random.randrange(100,500,1),0))
		enemy = Slime_Enemy((random.randrange(100,500,1),0))
		enemy = Slime_Enemy((random.randrange(100,500,1),0))
		'''

		
		#(self, layer, rect, tile_split)
		choice = random.choice((1,1))
		#choice = 1
		if choice == 0:
			#create walls
			#left wall
			thickness = 6
			bonus_height = 200

			tile_pic = sprites.level_sheet.getImage(37,28,6,6)
			tile = Mallow_Wall('left', 0,0 - bonus_height,thickness,sprites.size[1] + bonus_height, 4, True)
			i = 0
			while i < tile.rect.height:
				tile.image.blit(tile_pic, (0,i))
				i += tile_pic.get_height()

			#right wall
			tile = Mallow_Wall('right', sprites.size[0] - thickness, 0 - bonus_height, thickness, sprites.size[1] + bonus_height, 4, True)
			i = 0
			while i < tile.rect.height:
				image = pygame.transform.flip(tile_pic, True, False)
				tile.image.blit(image, (0,i))
				i += tile_pic.get_height()

		elif choice == 1:
			#create Mountain Walls
			count = 0
			while count < 20:
				platform = Tile(0 - 18, sprites.size[1] - (24 * count), 'classic', False)

				platform = Tile(sprites.size[0] - 6, sprites.size[1] - (24 * count), 'classic', False)

				count += 1

			item_spawner1 = Classic_Item_Spawner('left', (6,(sprites.size[1] / 2) - 15 - 24))
			item_spawner2 = Classic_Item_Spawner('right', (sprites.size[0] - 42,(sprites.size[1] / 2) - 15 - 24))
			item_spawner3 = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 15,0))



		y = 60
		y_change = 65
		x = 50
		x_change = 36
		count = 0
		while count < 3:
			platform = Platform(x + (x_change * count) , y, 'classic', False)
			platform.level = 1 #top level
			count += 1

		#top right start -always same
		count = 0
		while count < 3:
			count += 1
			platform = Platform(640 - x - (x_change * count), y, 'classic', False)
			platform.level = 1 #top level

		#create random layer 1 of 3
		if options.platform_density == 'Normal':
			platform_variable = 70
		elif options.platform_density == 'High':
			platform_variable  = 85
		elif options.platform_density == 'Low':
			platform_variable = 60
		elif options.platform_density == 'Very High':
			platform_variable  = 95
		elif options.platform_density == 'Very Low':
			platform_variable = 50

		count = 0
		while count < 15:
			rand = random.randrange(0,100,1)
			if rand < platform_variable:
				platform = Platform(x + (x_change * count), y + y_change, 'classic', False)
				platform.level = 2 #2nd level
			count += 1

		#create random layer 2 of 3
		count = 0
		while count < 15:
			rand = random.randrange(0,100,1)
			if rand < platform_variable:
				platform = Platform(x + (x_change * count), y + (y_change * 2), 'classic', False)
				platform.level = 3 #3rd level
			count += 1

		#create random layer 3 of 3
		count = 0
		while count < 15:
			rand = random.randrange(0,100,1)
			if rand < platform_variable:
				platform = Platform(x + (x_change * count), y + (y_change * 3), 'classic', False)
				platform.level = 4 #4th level
			count += 1

		#starting bottom left -always same
		count = 0
		while count < 3:
			platform = Platform(x + (x_change * count), y + (y_change * 4), 'classic', False)
			platform.level = 5 #5th level
			count += 1

		#bottom right -always same
		count = 0
		while count < 3:
			count += 1
			platform = Platform(640 - x - (x_change * count), y + (y_change * 4), 'classic', False)
			platform.level = 5 #5th level

		#create start poles, one on left, and one on right.
		centerx = x + (x_change * 2) + (x_change / 2) 
		pole = Pole(centerx, y_change, 5, 5)
		pole_list.append(pole)



		centerx = sprites.size[0] - x - (x_change * 2) - (x_change / 2)
		pole = Pole(centerx, y_change, 5, 5)
		pole_list.append(pole)

		#build up to three random size poles.
		i = random.choice((0,1,1,2,2,2,2,3,3,3,3))
		temp_list = []
		for tile in sprites.tile_list:
			if tile.type == 'platform':
				if tile.level != 1 and tile.level != 5:
					temp_list.append(tile)

		while i > 0:
			tile = random.choice(temp_list)
			bottom_level = tile.level
			level_height = random.choice((2, 2, 2, 3, 4))
			while bottom_level - level_height < 0:
				level_height -= 1
			#temp_list.remove(tile)

			#make sure pole doesnt exist here
			spot_taken = False
			for pole in sprites.tile_list:
				if pole.type == 'pole':
					tempcheck = tile.rect.centerx - pole.rect.centerx
					if tempcheck > -2 and tempcheck < 2: #close enough to same spot... in case off by a pixel.
						spot_taken = True
						break

			#make pole at the desired location, assuming one doesn't exist.
			if spot_taken is False:
				pole = Pole(tile.rect.centerx, y_change, bottom_level, level_height)
				pole_list.append(pole)
				i -= 1

		#
		#
		#HERE GOES visual effects type stuff. This goes at the end so as not to disrupt random seeding system.
		
		#Now replace poles with ropes:
		if options.rope_physics == 'On':
			for pole in pole_list:	
				rope_physics.Create_Rope((pole.rect.midtop),(pole.rect.midbottom))
				pole.kill()

		window = Window((0,46,640,98), -12, 'classic')
		screen = TV_Screen((120,5), sprites.screen ,sprites.player1, -8)
		screen = TV_Screen((422,5), sprites.screen ,sprites.player2, -8)

		if options.background_effects != 'Off':
			waterfall4 = Waterfall(-6, (176,236,13,124), 'classic')
			sprites.active_sprite_list.change_layer(waterfall4.mallow_splash,-5)

			waterfall5 = Waterfall(-6, (452,236,13,124), 'classic')
			sprites.active_sprite_list.change_layer(waterfall5.mallow_splash,-5)

		#End of stuff that is "visual only"
		#
		#


		#for collision checking, find out which tiles have open tops/bottoms.
		for tile in sprites.tile_list:
			if tile.type == 'tile':
				tile.check_sides()

		self.spawn_options = []
		for tile in sprites.tile_list:
			if tile.type == 'platform':
				self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))

	
	def build_versus_olympus(self):
		random.seed(self.seed)
		sounds.mixer.change_song('music_olympus.wav')
		sounds.mixer.background_music.set_volume(options.music_volume)

		menus.pause_sprite.visible = 0
		menus.pause_sprite.dirty = 1

		self.item_options = []
		for entry in options.items_dict.keys():
			if options.items_dict[entry] == 'on':
				if entry not in ('gravity', 'x', 'volt'):
					self.item_options.append(str(entry))

		options.banned_items = ['gravity', 'x', 'volt']


		for ninja in sprites.ninja_list:
			ninja.loop_physics = False
		options.loop_physics = False
		

		i = random.choice((3,4,5))
		#i = 5
		if i == 5:
			options.loop_physics = True
			for ninja in sprites.ninja_list:
				ninja.loop_physics = True


		#create walls
		#create Mountain Walls
		block_rand = False #just to set up later things
		if options.loop_physics is False:
			count = 0
			while count < 20:
				platform = Tile(0, sprites.size[1] - (24 * count), 'stone', False)
				platform = Tile(-24, sprites.size[1] - (24 * count), 'stone', False)
				platform = Tile(sprites.size[0] - 24, sprites.size[1] - (24 * count), 'stone', False)
				platform = Tile(sprites.size[0], sprites.size[1] - (24 * count), 'stone', False)

				count += 1
		else:
			block_rand = random.choice((True, False))
			block_range = random.choice(((6,7,8),(7,8,9),(8,9,10),(9,10,11),(10,11,12),(11,12,13),(12,13,14),(13,14,15)))
			# = (13,14,15)
			if block_rand is False:
				block_range = None
			count = 0
			while count < 20:
				if block_range == None or count not in block_range:
					platform = Tile(0, sprites.size[1] - (24 * count), 'stone', False)
					platform = Tile(-24, sprites.size[1] - (24 * count), 'stone', False)

					platform = Tile(sprites.size[0] - 24, sprites.size[1] - (24 * count), 'stone', False)
					platform = Tile(sprites.size[0], sprites.size[1] - (24 * count), 'stone', False)

				count += 1

			if block_range != None:
				#platform = Tile(0 - 0 - 24, sprites.size[1] - (24 * (block_range[0] - 1)), 'stone', False)
				#platform = Tile(0 - 0 - 24, sprites.size[1] - (24 * (block_range[2] + 1)), 'stone', False)
				platform = Tile(0 - 0 + 24, sprites.size[1] - (24 * (block_range[0] - 1)), 'stone', False)
				#platform = Tile(sprites.size[0] - 24 + 24, sprites.size[1] - (24 * (block_range[0] - 1)), 'stone', False)
				#platform = Tile(sprites.size[0] - 24 + 24, sprites.size[1] - (24 * (block_range[2] + 1)), 'stone', False)
				platform = Tile(sprites.size[0] - 24 - 24, sprites.size[1] - (24 * (block_range[0] - 1)), 'stone', False)



		#Create Platforms
		#top left start -always same
		y = 50
		y_change = 65
		x = 50
		x_change = 36
		count = 0

		#create Floor
		if options.loop_physics is False:
			count = 0
			while count < 20:
				platform = Tile(80 + (24 * count), y + (y_change * 4), 'stone', False)
				count += 1
		else:
			count = 0
			y_mod = 2
			while count < 20:
				if count not in (9,10):
					platform = Tile(80 + (24 * count), y + (y_change * 4) + y_mod, 'stone', False)
					platform = Tile(80 + (24 * count), 24 + y + (y_change * 4) + y_mod, 'stone', False)
					#platform = Tile(80 + (24 * count), 48 + y + (y_change * 4) + y_mod, 'stone', False)
				count += 1

			#count = 0
			#while count < 28:
			#	if count not in (12,13,14,15):
			#		platform = Tile(-16 + (24 * count), -48 + 1, 'stone', False)
			#	count += 1

			#platform = Tile(80 + (8 * 24), y + (y_change * 4), 'stone', False)
			#platform = Tile(80 + (11 * 24), y + (y_change * 4), 'stone', False)
			#platform = Tile(80 + (8 * 24), y + 24 + (y_change * 4), 'stone', False)
			#platform = Tile(80 + (11 * 24), y + 24 + (y_change *4), 'stone', False)
			#platform = Tile(80 + (8 * 24), y + 48 + (y_change * 4), 'stone', False)
			#platform = Tile(80 + (11 * 24), y + 48 +(y_change * 4), 'stone', False)

			#barrier = Barrier((80 + (8 * 24),360,24,24),'right')
			#barrier = Barrier((80 + (11 * 24),360,24,24), 'left')

			#platform = Tile(80 + (8 * 24), -6, 'stone', False)
			#platform = Tile(80 + (11 * 24), -6, 'stone', False)
			#platform = Tile(80 + (8 * 24), -24 - 6, 'stone', False)
			#platform = Tile(80 + (11 * 24), -24 - 6, 'stone', False)



		i = random.randrange(0,12,1)
		#i = 9
		if i <= 2:
			self.spawn_options = self.current_level[1].copy()
			self.spawn_options.append((484, 120 - 24))
			self.spawn_options.append((155, 120 - 24))

			#create Mountain Walls
			count = 3
			while count < 11:
				platform = Tile((sprites.size[0] / 2) - 40 - 12 + 4, (y + (y_change * 4)) - (24 * count), 'stone', False)
				platform = Tile((sprites.size[0] / 2) + 40 - 12 - 4,  (y + (y_change * 4)) - (24 * count), 'stone', False)
				count += 1

			#create tunnel
			count = 0
			while count < 2:
				platform = Tile((sprites.size[0] / 2) - 40 - 12 - 24 + 4 + (count * 24), (y + (y_change * 4)) - 48, 'stone', False)
				count += 1

			count = 0
			while count < 2:
				platform = Tile((sprites.size[0] / 2) + 40 + 12 + - 24 - 4 + (count * 24), (y + (y_change * 4)) - 48, 'stone', False)
				count += 1

		elif i <= 4:
			self.spawn_options = self.current_level[1].copy()
			self.spawn_options.append((484, 120 - 24))
			self.spawn_options.append((155, 120 - 24))

			platform = Tile((sprites.size[0] / 2) - 40 - 12, (y + (y_change * 4)) - (24 * 9), 'stone', False)
			platform = Tile((sprites.size[0] / 2) + 40 - 12,  (y + (y_change * 4)) - (24 * 9), 'stone', False)
			platform = Tile((sprites.size[0] / 2) - 40 - 12 - 24, (y + (y_change * 4)) - (24 * 9), 'stone', False)
			platform = Tile((sprites.size[0] / 2) + 40 - 12 + 24,  (y + (y_change * 4)) - (24 * 9), 'stone', False)
			platform = Tile((sprites.size[0] / 2) - 40 - 12 - 48, (y + (y_change * 4)) - (24 * 9), 'stone', False)
			platform = Tile((sprites.size[0] / 2) + 40 - 12 + 48,  (y + (y_change * 4)) - (24 * 9), 'stone', False)
			#create tunnel
			platform = Tile((sprites.size[0] / 2) - 40 - 12 - 24 - (0 * 24), (y + (y_change * 4)) - 48, 'stone', False)
			platform = Tile((sprites.size[0] / 2) + 40 + 12 + - 24 + (1* 24), (y + (y_change * 4)) - 48, 'stone', False)

		elif i <= 6:
			self.spawn_options = self.current_level[1].copy()
			self.spawn_options.append((484, 120 - 24))
			self.spawn_options.append((155, 120 - 24))

			count = 0
			while count < 3:
				#create tunnel
				platform = Tile((sprites.size[0] / 2) - 24 - (count * 24), (y + (y_change * 4)) - 48, 'stone', False)
				platform = Tile((sprites.size[0] / 2) + (count* 24), (y + (y_change * 4)) - 48, 'stone', False)
				count += 1

		elif i <= 8:
			self.spawn_options = self.current_level[1].copy()
			self.spawn_options.append((484, 120 - 24))
			self.spawn_options.append((155, 120 - 24))
			x = (sprites.size[0] / 2) - 18
			y =  100
			platform = Moving_Platform(0, ((x, y), (x, 230)), 1, 1, 'stone', False)
			x = sprites.size[0] / 2 + 18
			platform2 = Moving_Platform(0, ((x, y), (x, 230)), 1, 1, 'stone', False)

			platform = Platform((640 / 2) -36 -36, 260, 'stone', False)
			platform = Platform((640 / 2) + 36, 260, 'stone', False)

		else:
			y_mod = 2
			if options.loop_physics is False:
				for tile in sprites.tile_list:
					if tile.type == 'tile':
						tile.rect.y +=  y_mod
			#Mountain version
			self.starting_positions = [(115,286 + y_mod), (284,238 + y_mod), (355,238 + y_mod), (524,286 + y_mod)]
			self.spawn_options = self.starting_positions.copy()

			#Roof
			choice = random.choice((True, False, False))
			tile = Item_Spawn_Point('floor', False, 640 / 2, 286 - (24 * 10) + y_mod, choice)
			for bubble in tile.bubble_list:	
				bubble.item_options = ['volt']
				bubble.item_locked = True

			
			choice = random.choice((1,2))
			if choice == 1:
				item_spawner1 = Classic_Item_Spawner('left', (320 - (24 * 9), 286 - (24 * 0.5) + y_mod))
			else:
				item_spawner1 = Classic_Item_Spawner('left', (23,(sprites.size[1]) - (24 * 4)))
			
			choice = random.choice((1,2))
			if choice == 1:
				item_spawner2 = Classic_Item_Spawner('right', (320 + (24 * 9) - 36 ,286 - (24 * 0.5) + y_mod))
			else:
				item_spawner2 = Classic_Item_Spawner('right', (sprites.size[0] - 59,(sprites.size[1]) - (24 * 4)))



			platform = Platform((640 / 2) - 17, 286 - (24 * 4) + y_mod, 'stone', False)

			choice = random.choice((True, False))
			choice = True
			if choice is True:
				if block_rand is False:
					platform = Moving_Platform(0, ((42, 260), (42, 51)), 1, 1, 'stone', False)

				platform = Moving_Platform(0, ((108, 160), (108, 51)), 1, 1, 'stone', False)


				platform = Platform(170 - 18 + 10 - 8, 286 - (24 * 10), 'stone', False)

				platform = Platform(240 - 18 + 5 - 8, 286 - (24 * 10), 'stone', False)


			choice = random.choice((True, False))
			choice = True
			if choice is True:
				if block_rand is False:
					platform = Moving_Platform(0, ((sprites.size[0] - 30 - 20 + 8, 260), (sprites.size[0] - 30 - 20 + 8, 51)), 1, 1, 'stone', False)

				platform = Moving_Platform(0, ((sprites.size[0] - 100 - 15 + 8, 160), (sprites.size[0] - 100 - 15 + 8, 51)), 1, 1, 'stone', False)


				platform = Platform(sprites.size[0] - 170 - 18 - 10 + 8, 286 - (24 * 10), 'stone', False)

				platform = Platform(sprites.size[0] -  240 - 18 - 5 + 8, 286 - (24 * 10), 'stone', False)

			count = 0
			while count < 10:
				if count not in (0,1,2,3,4,5,6,7,8):
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 0) + y_mod, 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 0) + y_mod, 'stone', False)
				if count not in (2,3,4,5,6,7,8):
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 1) + y_mod, 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 1) + y_mod, 'stone', False)

				count += 1

			count = 0

			while count < 8:
				if count not in (1,2,3):
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 2) + y_mod, 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 2) + y_mod, 'stone', False)
				


				if count < 4:
					if count not in (0,1,2):
						platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 4) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 4) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) - 24 - 24 -(count * 24), 286 - (24 * 3) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) + 0 + 24 + (count * 24),  286 - (24 * 3) + y_mod, 'stone', False)


				if count < 3:
					if count not in (0,1):
						platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 6) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 6) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 5) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 5) + y_mod, 'stone', False)


				if count < 2:
					if count != 0:
						platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 8) + y_mod, 'stone', False)
						platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 8) + y_mod, 'stone', False)
						#platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 7), 'stone', False)
						#platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 7), 'stone', False)


				if count < 1:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 10) + y_mod, 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 10) + y_mod, 'stone', False)
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 9) + y_mod, 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 9) + y_mod, 'stone', False)

				count += 1

		'''
		else:
			#Mountain version
			self.starting_positions = [(260,0), (375,0), (100,0), (540,0)]


			count = 0
			while count < 10:
				platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 0), 'stone', False)
				platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 0), 'stone', False)
				platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 1), 'stone', False)
				platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 1), 'stone', False)

				count += 1

			count = 0
			while count < 9:
				platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 2), 'stone', False)
				platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 2), 'stone', False)
				
				if count < 8:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 3), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 3), 'stone', False)

				if count < 7:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 4), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 4), 'stone', False)

				if count < 6:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 5), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 5), 'stone', False)

				if count < 5:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 6), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 6), 'stone', False)

				if count < 4:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 7), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 7), 'stone', False)

				if count < 3:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 8), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 8), 'stone', False)

				if count < 2:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 9), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 9), 'stone', False)

				if count < 1:
					platform = Tile((sprites.size[0] / 2) - 24 -(count * 24), 286 - (24 * 10), 'stone', False)
					platform = Tile((sprites.size[0] / 2) + 0 + (count * 24),  286 - (24 * 10), 'stone', False)

				count += 1
		'''
			



		if i in (0,1,2,3,4,5,6,7,8): #not for the new versions.
			#create left and right bottom mountin layer
			#Roof
			choice = random.choice((True, False, False))
			tile = Item_Spawn_Point('floor', False, 640 / 2, 40 + 12, choice)
			for bubble in tile.bubble_list:	
				bubble.item_options = ['volt']
				bubble.item_locked = True

			item_spawner1 = Classic_Item_Spawner('left', (23,(sprites.size[1]) - (24 * 4)))
			item_spawner2 = Classic_Item_Spawner('right', (sprites.size[0] - 59,(sprites.size[1]) - (24 * 4)))
			#item_spawner3 = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 15,0))

			count = 0
			while count < 5:
				platform = Tile((sprites.size[0] / 2) - 80 - 48 -(count * 24), 240 - 24, 'stone', False)

				platform = Tile((sprites.size[0] / 2) + 80 + 24 + (count * 24),  240 - 24, 'stone', False)

				count += 1

			#steps
			platform = Tile((sprites.size[0] / 2) - 80 - 48 -(6 * 24), 240 - 24, 'stone', False)

			platform = Tile((sprites.size[0] / 2) + 80 + 24 + (6 * 24),  240 - 24, 'stone', False)

			#create left & right middle layer
			count = 1
			while count < 4:
				platform = Tile((sprites.size[0] / 2) - 80 - 48 -(count * 24), 240 - 48 - 24, 'stone', False)

				platform = Tile((sprites.size[0] / 2) + 80 + 24 + (count * 24),  240 - 48 - 24, 'stone', False)

				count += 1

			#create left & right top layer
			count = 0
			while count < 1:
				platform = Tile((sprites.size[0] / 2) - 80 - 96 -(count * 24), 240 - 48 - 24 - 48, 'stone', False)

				platform = Tile((sprites.size[0] / 2) + 80 + 24 + 48 +(count * 24),  240 - 48 - 24 - 48, 'stone', False)

				count += 1

			#mountain top
			platform = Platform((640 / 2) - 17, 40 + 12, 'stone', False)

			x = (sprites.size[0] / 2) - 48 - 24
			y = 240 - 48 - 24 - 48 - 40
			platform = Moving_Platform(0, ((x, y), (80 + 24, y)), 1, 1, 'stone', False)

			x = (sprites.size[0] / 2) + 48 + 24
			y = 240 - 48 - 24 - 48 - 40
			platform2 = Moving_Platform(0, ((x, y), (sprites.size[0] - 80 - 24, y)), 1, 1, 'stone', False)

			choice = random.choice((True, False))
			if choice is True:
				x = 30 + 12 + 24
				y = 188
				platform3 = Moving_Platform(0, ((x, y), (x, 240 - 48 - 24 - 48 - 40)), 1, 1, 'stone', False)

				x = sprites.size[0] - 30 - 12 - 24
				y = 188
				platform4 = Moving_Platform(0, ((x, y), (x, 240 - 48 - 24 - 48 - 40)), 1, 1, 'stone', False)



		#create Mallow
		if options.loop_physics is False:
			mallow = Mallow((0,330,640,30), False)
		else:
			pass
			'''
			y = 50
			y_change = 65
			platform = Tile(80 + (8 * 24), y + (y_change * 5), 'stone', False)
			platform = Tile(80 + (11 * 24), y + (y_change * 5), 'stone', False)
			platform = Tile(80 + (8 * 24), y + (y_change * 6), 'stone', False)
			platform = Tile(80 + (11 * 24), y + (y_change * 6), 'stone', False)
			mallow = Mallow((0,330,(80 + (8 * 24)),30), False)
			mallow = Mallow(((80 + (12 * 24)),330,300,30), False)
			'''
		'''
		i = 0
		while i < 640:
			mallow = Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		#for collision checking, find out which tiles have open tops/bottoms.
		for tile in sprites.tile_list:
			if tile.type == 'tile':
				tile.check_sides()

		#(self, rectx, recty, position1, position2, xspeed, yspeed)
		choice = random.choice((1,2,3))
		#choice = 3
		if choice == 1:
			background = Level_Background(-12, 'background_olympus.png')
			background2 = Level_Background(-10, 'close_background_olympus.png')

			if options.background_effects != 'Off':
				cloud1 = Cloud([-9, -11, 10], 250, 55, 0.25, (433,231,206,40), 50)
				cloud2 = Cloud([10, -9], 500, 150, 0.5, (433,231,206,40), 150)
				if options.background_effects == 'High':
					cloud3 = Cloud([-11, -9, 10], -100, 110, 0.25, (461,187,177,40), 110)
					cloud_4 = Cloud([10, -9], -50, 240, 0.5, (461,187,177,40), 30)
		elif choice == 2:
			storm = Rainstorm(1)
			background = Level_Background(-12, 'background_olympus_storm.png')
			background2 = Level_Background(-10, 'close_background_olympus_storm.png')

		else:
			snowfield = Snowfield(False)
			background = Level_Background(-12, 'background_olympus_snow.png')
			background2 = Level_Background(-10, 'close_background_olympus_snow.png')

			for tile in sprites.tile_list:
				if tile.type in ('tile', 'platform'):
					tile.top_friction = 'icy'
					tile.bottom_friction = 'icy'
					tile.apply_ice()
	
	def build_versus_falls(self):
		random.seed(self.seed)
		sounds.mixer.change_song('music_falls.wav')
		sounds.mixer.background_music.set_volume(options.music_volume)
		#sounds.mixer.start_song()

		menus.pause_sprite.visible = 0
		menus.pause_sprite.dirty = 1

		self.item_options = []
		for entry in options.items_dict.keys():
			if options.items_dict[entry] == 'on':
				if entry not in ('x', 'gravity'):
					self.item_options.append(str(entry))
		options.banned_items = ['gravity', 'x']

		for ninja in sprites.ninja_list:
			ninja.loop_physics = False
		options.loop_physics = False
		
		#create side walls
		count = 0
		while count <= 20:
			tile = Tile(-17, 360 - 24 - (24 * count), 'stone', False)
			tile = Tile(640 - 7, 360 - 24 - (24 * count), 'stone', False)
			count += 1

		'''
		while count <= 18:
			if count <= 10:
				tile = Tile(-17, 360 - 24 - (24 * count), 'stone', False)
				tile = Tile(640 - 7, 360 - 24 - (24 * count), 'stone', False)
			else:
				tile = Tile(-24, 360 - 24 - (24 * count), 'stone', False)
				tile = Tile(640, 360 - 24 - (24 * count), 'stone', False)
			count += 1
		'''
		
		barrier = Barrier((0,0,7,100),'right')
		barrier = Barrier((640-7,0,7,100), 'left')


		#Clouds
		#(self, layer_list, startx, starty, speed, sprite_rect, y_range):
		#cloud1 = Cloud([-5, -5, -5], 300, 5, 0.1, (433,231,206,40), None)
		#cloud3 = Cloud([-5, -5, -5], -100, 15, 0.1, (461,187,177,40), None)

		
		choice = random.choice((1,2,3,4,5,6,7,8,9))
		#choice = 9
		#if choice == 3 or choice == 1 or choice == 2:
		#choice = 4
		if choice == 1:
			#create Mallow
			mallow = Mallow((0,330,640,30),False)

			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 250 - 15,0))
			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) + 250 - 15,0))

			for tile in sprites.tile_list:
				if tile.type == 'tile':
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))


		elif choice == 2:
			#create Mallow
			mallow = Mallow((0,330,640,30),False)

			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 250 - 15,0))
			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) + 250 - 15,0))
			#create Floor
			count = 0
			while count <= 6:
				tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2) - 24, 'stone', False)
				tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2) - 24, 'stone', False)
				tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2), 'stone', False)
				tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2), 'stone', False)
				count += 1

			#i = random.choice(('mine', 'portal gun', 'laser', 'shoes','metal suit', 'rocket', 'homing bomb', 'bomb', 'ice bomb'))
			i = random.choice(('mine', 'laser', 'shoes','rocket','bomb', 'ice bomb'))

			tile = Item_Spawn_Point('floor', False, 224, (sprites.size[1] / 2) - 24, True)
			for bubble in tile.bubble_list:	
				bubble.item_options = [i]
			tile = Item_Spawn_Point('floor', False, 320, (sprites.size[1] / 2) - 24, True)
			for bubble in tile.bubble_list:	
				bubble.item_options = [i]
			tile = Item_Spawn_Point('floor', False, 416, (sprites.size[1] / 2) - 24, True)
			for bubble in tile.bubble_list:	
				bubble.item_options = [i]



		elif choice == 3:
			#create Mallow
			mallow = Mallow((0,330,640,30),False)

			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 250 - 15,0))
			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) + 250 - 15,0))
			#create Floor
			count = 1
			while count <= 7:
				if count != 4:
					tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2) - 24, 'stone', False)
					tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2) - 24, 'stone', False)
					tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2), 'stone', False)
					tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2), 'stone', False)
				count += 1

		elif choice == 4:
			#create Mallow
			mallow = Mallow((0,330,640,30),False)

			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 250 - 15,0))
			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) + 250 - 15,0))
			#create Floor
			count = 1
			while count <= 7:
				tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2) - 24, 'stone', False)
				tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2) - 24, 'stone', False)
				tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2), 'stone', False)
				tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2), 'stone', False)
				count += 1

			#test tiles:
			tile = Tile((sprites.size[0] / 2) - 24 - (24 * 8), 275, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 24 - (24 * 10), 225, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 24 - (24 * 11), 225, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 24 - (24 * 11), 201, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 24 - (24 * 11), 177, 'stone', False)
			
			tile = Tile((sprites.size[0] / 2) + (24 * 8), 275, 'stone', False)
			tile = Tile((sprites.size[0] / 2) + (24 * 10), 225, 'stone', False)
			tile = Tile((sprites.size[0] / 2) + (24 * 11), 225, 'stone', False)
			tile = Tile((sprites.size[0] / 2) + (24 * 11), 201, 'stone', False)
			tile = Tile((sprites.size[0] / 2) + (24 * 11), 177, 'stone', False)

			x = 50
			y = 133
			platform = Moving_Platform(0, ((x, y), (x + 80, y)), 1, 1, 'stone', False)
			x = 640 - 50
			y = 133
			platform = Moving_Platform(0, ((x, y), (x - 80, y)), 1, 1, 'stone', False)

			tile = Item_Spawn_Point('floor', False, 224, (sprites.size[1] / 2) - 24, False)
			for bubble in tile.bubble_list:	
				bubble.item_options = ['mine']
		
			tile = Item_Spawn_Point('floor', False, 416, (sprites.size[1] / 2) - 24, False)
			for bubble in tile.bubble_list:	
				bubble.item_options = ['bomb']

			tile = Item_Spawn_Point('floor', False, (sprites.size[0] / 2) + (24 * 8) + 12, 275, False)
			for bubble in tile.bubble_list:	
				bubble.item_options = random.choice((['rocket'], ['wings']))

			tile = Item_Spawn_Point('floor', False, (sprites.size[0] / 2) - 24 - (24 * 8) + 12, 275, False)
			for bubble in tile.bubble_list:	
				bubble.item_options = random.choice((['rocket'], ['wings']))

		elif choice == 5:
			#create Mallow
			mallow = Mallow((0,330,640,30),False)

			self.starting_positions = [(80,0), (200,0), (640-200,0), (640-80,0)]

			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 15,0))
			item_spawner2 = Classic_Item_Spawner('left', (6,360 - (24 * 5)))
			item_spawner1 = Classic_Item_Spawner('right', (sprites.size[0] - 42,360 - (24 * 5)))

			#create Floor
			count = 0
			while count <= 6:
				tile = Tile(7 + (24 * 2) + (24 * count), (sprites.size[1] / 2) - 24 - 12, 'stone', False)
				tile = Tile(7 + (24 * 2) + (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)

				tile = Tile(640 - 7 - 24 - (24 * 2) - (24 * count), (sprites.size[1] / 2) - 24 - 12, 'stone', False)
				tile = Tile(640 - 7 - 24 - (24 * 2) - (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
				
				count += 1

		elif choice == 6:
			#create Mallow
			mallow = Mallow((0,330,640,30),False)

			self.starting_positions = [(80,0), (180,0), (640-180,0), (640-80,0)]

			item_spawner = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 15,0))
			item_spawner2 = Classic_Item_Spawner('left', (6,360 - (24 * 5)))
			item_spawner1 = Classic_Item_Spawner('right', (sprites.size[0] - 42,360 - (24 * 5)))

			#create Floor
			count = 0
			while count <= 5:
				tile = Tile(7 + (24 * 2) + (24 * count), (sprites.size[1] / 2) - 24 - 12, 'stone', False)
				tile = Tile(640 - 7 - 24 - (24 * 2) - (24 * count), (sprites.size[1] / 2) - 24 - 12, 'stone', False)
				
				count += 1

			tile = Tile(320 - 24, (sprites.size[1] / 2) + (24 * 2) - 12, 'stone', False)
			tile = Tile(320 - 24 - 24, (sprites.size[1] / 2) + (24 * 2) - 12, 'stone', False)
			tile = Tile(320, (sprites.size[1] / 2) + (24 * 2) - 12, 'stone', False)
			tile = Tile(320 + 24, (sprites.size[1] / 2) + (24 * 2) - 12, 'stone', False)
			#tile = Tile(320 - 12 + 48, (sprites.size[1] / 2) + 48 - 12, 'stone', False)

		elif choice == 7:
	

			self.starting_positions = [(176,130 + 12), (272,130 + 12), (368,130 + 12), (464,130 + 12)]

			#create Floor
			count = 0

			hole_list = random.choice(((3,4),(0,0), (0,3), (0,4), (99,99), (99,99)))
			while count <= 6:
				if count not in hole_list:
					tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))
					tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))

				#tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2), 'mystic', False)
				#tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2), 'mystic', False)
				count += 1

			#mallow = Mallow((0,0,640,30),True)
			#mallow = Mallow((0,330,640,30),False)

			#GRAVITY BARRIER must be built at end. Needs Tile list built first.
			gravity_barrier = Gravity_Barrier('horizontal', sprites.size[1] / 2, True, None)

			item_spawner0 = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 15 - 150,0))
			item_spawner1 = Classic_Item_Spawner('floor', ((sprites.size[0] / 2) - 15 - 150,360 - 36))

			item_spawner0 = Classic_Item_Spawner('roof', ((sprites.size[0] / 2) - 15 + 150,0))
			item_spawner1 = Classic_Item_Spawner('floor', ((sprites.size[0] / 2) - 15 + 150,360 - 36))

			#item_spawner2 = Classic_Item_Spawner('left', (6,360 - (24 * 5)))
			#item_spawner3 = Classic_Item_Spawner('right', (sprites.size[0] - 42,360 - (24 * 5)))

		elif choice == 8:
	

			self.starting_positions = [(176,130 + 12), (272,130 + 12), (368,130 + 12 + 24 + 48), (464,130 + 12 + 24 + 48)]

			mallow = Mallow((6,330,320 - 6,30),False)
			mallow = Mallow((320,0,320 - 6,30),True)

			#create Floor
			count = 0

			hole_list = random.choice(((0,3,4),(0,0), (0,3), (0,4)))
			while count <= 6:
				if count not in hole_list:
					tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))
					tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))

				#tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2), 'mystic', False)
				#tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2), 'mystic', False)
				count += 1

			tile = Tile((sprites.size[0] / 2)  - 24 + 1, 38 - 24, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 24 + 1, 38 - 48, 'stone', False)
			
			tile = Tile((sprites.size[0] / 2) - 1, 360 - 38, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 1, 360 - 38 + 24, 'stone', False)

			#mallow = Mallow((0,0,640,30),True)
			#mallow = Mallow((0,330,640,30),False)

			#GRAVITY BARRIER must be built at end. Needs Tile list built first.
			gravity_barrier = Gravity_Barrier('vertical', sprites.size[0] / 2, False, None)

			item_spawner1 = Classic_Item_Spawner('floor', (640 -6 - (24 * 8) - 30 ,360-36))
			item_spawner2 = Classic_Item_Spawner('roof', (6 + (24 * 8), 0))

			tile = Item_Spawn_Point('roof', False, (sprites.size[0] / 2) - 12, 35, False)
			for bubble in tile.bubble_list:	
				for item in ('x', 'skull'):
					try:
						bubble.item_options.remove(item)
					except ValueError:
						pass

			tile = Item_Spawn_Point('floor', False, (sprites.size[0] / 2) + 12, 360 -35, False)
			for bubble in tile.bubble_list:	
				for item in ('x', 'skull'):
					try:
						bubble.item_options.remove(item)
					except ValueError:
						pass


		elif choice == 9:
	

			self.starting_positions = [(176 - (24 * 2),130 + 12 + 24 + 48), (272 - (24 * 3),130 + 12 + 24 + 48), (368 + (24 * 3),130 + 12), (464 + (24 * 2),130 + 12)]

			mallow = Mallow((320,330,320 - 6,30),False)
			mallow = Mallow((6,0,320 - 6,30),True)

			#create Floor
			count = 0

			hole_list = random.choice(((0,1,2,3),(0,1,2,3)))
			while count <= 8:
				if count not in hole_list:
					tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))
					tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2) - 12, 'stone', False)
					self.inverted_spawn_options.append((tile.rect.centerx, tile.rect.bottom + 24))
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))

				#tile = Tile((sprites.size[0] / 2) - 24 - (24 * count), (sprites.size[1] / 2), 'mystic', False)
				#tile = Tile((sprites.size[0] / 2) + (24 * count), (sprites.size[1] / 2), 'mystic', False)
				count += 1

			tile = Tile((sprites.size[0] / 2)  -  1, 38 - 24, 'stone', False)
			tile = Tile((sprites.size[0] / 2) -  1, 38 - 48, 'stone', False)
			
			tile = Tile((sprites.size[0] / 2) - 24 + 1, 360 - 38, 'stone', False)
			tile = Tile((sprites.size[0] / 2) - 24 + 1, 360 - 38 + 24, 'stone', False)

			#mallow = Mallow((0,0,640,30),True)
			#mallow = Mallow((0,330,640,30),False)

			#GRAVITY BARRIER must be built at end. Needs Tile list built first.
			gravity_barrier = Gravity_Barrier('vertical', sprites.size[0] / 2, True, None)

			
			tile = Item_Spawn_Point('roof', False, (sprites.size[0] / 2) - 12 - (24 * 6), (sprites.size[1] / 2) - 12 + 24, False)
			for bubble in tile.bubble_list:	
				for item in ('x', 'skull'):
					try:
						bubble.item_options.remove(item)
					except ValueError:
						pass

			tile = Item_Spawn_Point('floor', False, (sprites.size[0] / 2) + 12 +(24 * 6), (sprites.size[1] / 2) - 12, False)
			for bubble in tile.bubble_list:	
				for item in ('x', 'skull'):
					try:
						bubble.item_options.remove(item)
					except ValueError:
						pass


		#for collision checking, find out which tiles have open tops/bottoms.
		for tile in sprites.tile_list:
			if tile.type == 'tile':
				tile.check_sides()

		if choice == 7:
			waterfall = Waterfall(-9, (6,100,sprites.size[0] - 12,80), True, fix_edges = False)
			sprites.active_sprite_list.change_layer(waterfall.mallow_splash, -8)
			waterfall = Waterfall(-9, (6,180,sprites.size[0] - 12,80), True, inverted = True, fix_edges = False)
			sprites.active_sprite_list.change_layer(waterfall.mallow_splash, -8)
		elif choice == 8:
			waterfall1 = Waterfall(-9, (6,100,320 - 6,240), True)
			waterfall2 = Waterfall(-9, (320,20,320 - 6,240), True, inverted = True)
		elif choice == 9:
			waterfall1 = Waterfall(-9, (320,100,320 - 6,310), True)
			waterfall2 = Waterfall(-9, (6,-50,320 - 6,310), True, inverted = True)
		else:
			waterfall = Waterfall(-9, (6,100,sprites.size[0] - 12,sprites.size[1] - 50), True)
			
		
		if choice == 1:
			self.starting_positions = [(176 + 24,0), (272 + 24,0), (368 - 24 + 50,0), (464-24 + 50,0)]
			#create Floor
			for i in (0, -96, 96, -192, 192, -288, 288):
				if i != -288:
					log = Log(320 - 24 + i, 108, waterfall, 'log')
					log = Log(320 - 24 + i, 216, waterfall, 'log')
					log = Log(320 - 24 + i, 324, waterfall, 'log')
				
				if i != 288:
					log = Log(320 + 24 + i, 270, waterfall, 'log')
					log = Log(320 + 24 + i, 378, waterfall, 'log')
					log = Log(320 + 24 + i, 162, waterfall, 'log')

			for tile in sprites.tile_list:
				if tile.type == 'platform':
					if tile.subtype == 'moving platform':
						self.moving_platform_spawn_options.append(tile)


		elif choice in (2,3): #levels where logs fit
			#log = Log(50, 54, waterfall, 'log')
			i = random.choice((True, False))
			if i is True:
				i = random.choice((1,2,3))
				if i == 1:
					log = Log(50, 108, waterfall, 'log')
					log = Log(100, 162, waterfall, 'log')
					log = Log(50, 216, waterfall, 'log')
					log = Log(100, 270, waterfall, 'log')
					log = Log(50, 324, waterfall, 'log')
					log = Log(100, 378, waterfall, 'log')
				elif i == 2:
					log = Log(100, 162, waterfall, 'log')
					log = Log(50, 216, waterfall, 'log')
					log = Log(100, 270, waterfall, 'log')
					log = Log(50, 324, waterfall, 'log')
				elif i == 3:
					i = random.choice((True,False))
					if i is True:
						log = Log(50, 108, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(100, 162, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(50, 216, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(100, 270, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(50, 324, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(100, 378, waterfall, 'log')


			i = random.choice((True,False))
			if i is True:
				i = random.choice((1,2,3))
				if i == 1:
					log = Log(640 - 50, 108, waterfall, 'log')
					log = Log(640 - 100, 162, waterfall, 'log')
					log = Log(640 - 50, 216, waterfall, 'log')
					log = Log(640 - 100, 270, waterfall, 'log')
					log = Log(640 - 50, 324, waterfall, 'log')
					log = Log(640 - 100, 378, waterfall, 'log')
				elif i == 2:
					log = Log(640 - 100, 162, waterfall, 'log')
					log = Log(640 - 50, 216, waterfall, 'log')
					log = Log(640 - 100, 270, waterfall, 'log')
					log = Log(640 - 50, 324, waterfall, 'log')
				elif i == 3:
					i = random.choice((True,False))
					if i is True:
						log = Log(640 - 50, 108, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(640 - 100, 162, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(640 - 50, 216, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(640 - 100, 270, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(640 - 50, 324, waterfall, 'log')
					i = random.choice((True,False))
					if i is True:
						log = Log(640 - 100, 378, waterfall, 'log')

		elif choice == 5:
			#create Floor
			i = 36 + 16
			log = Log(320 - i, 108, waterfall, 'log')
			log = Log(320 - i, 216, waterfall, 'log')
			log = Log(320 - i, 324, waterfall, 'log')

			log = Log(320 + i, 108, waterfall, 'log')
			log = Log(320 + i, 216, waterfall, 'log')
			log = Log(320 + i, 324, waterfall, 'log')
				
			log = Log(320, 270, waterfall, 'log')
			log = Log(320, 378, waterfall, 'log')
			log = Log(320, 162, waterfall, 'log')

			for tile in sprites.tile_list:
				if tile.type == 'platform':
					if tile.subtype == 'moving platform':
						self.moving_platform_spawn_options.append(tile)

		elif choice == 6:
			#create Floor
			i = 24 * 3.5
			log = Log(320 - i, 108, waterfall, 'log')
			log = Log(320 - i, 216, waterfall, 'log')
			log = Log(320 - i, 324, waterfall, 'log')
				
			log = Log(320 + i, 270, waterfall, 'log')
			log = Log(320 + i, 378, waterfall, 'log')
			log = Log(320 + i, 162, waterfall, 'log')

			for tile in sprites.tile_list:
				if tile.type == 'platform':
					if tile.subtype == 'moving platform':
						self.moving_platform_spawn_options.append(tile)

		elif choice == 9:
			#Logs
			log = Log(585, 100, waterfall1, 'log')
			log = Log(585, 178, waterfall1, 'log')
			log = Log(585, 256, waterfall1, 'log')
			log = Log(585, 334, waterfall1, 'log')

			#Logs
			log = Log(320 + (24 * 2), 100, waterfall1, 'log')
			log = Log(320 + (24 * 2), 178, waterfall1, 'log')
			log = Log(320 + (24 * 2), 256, waterfall1, 'log')
			log = Log(320 + (24 * 2), 334, waterfall1, 'log')

			#Logs
			log = Log(55, 260, waterfall2, 'log')
			log = Log(55, 182, waterfall2, 'log')
			log = Log(55, 104, waterfall2, 'log')
			log = Log(55, 26, waterfall2, 'log')

			#Logs
			log = Log(320 - (24 * 2), 260, waterfall2, 'log')
			log = Log(320 - (24 * 2), 182, waterfall2, 'log')
			log = Log(320 - (24 * 2), 104, waterfall2, 'log')
			log = Log(320 - (24 * 2), 26, waterfall2, 'log')

			for tile in sprites.tile_list:
				if tile.type == 'platform':
					if tile.subtype == 'moving platform':
						self.moving_platform_spawn_options.append(tile)
		

		#Clouds
		#(self, layer_list, startx, starty, speed, sprite_rect, y_range):
		
		if choice < 7:
			if options.background_effects == 'High':
				cloud1 = Cloud([-7, -7, -7], 300, 5, 0.1, (433,231,206,40), None)
				cloud3 = Cloud([-7, -7, -7], -100, 15, 0.1, (461,187,177,40), None)
			elif options.background_effects == 'Low':
				cloud3 = Cloud([-7, -7, -7], -100, 15, 0.1, (461,187,177,40), None)

		for tile in sprites.tile_list:
			if tile.type == 'tile':
				if tile.rect.centerx > 24 and tile.rect.centerx < 640-24:
					self.spawn_options.append((tile.rect.centerx, tile.rect.top - 24))

		if choice == 7:
			background = Level_Background(-12, 'background_falls_horizontal_mirror.png')
		elif choice == 8:
			background = Level_Background(-12, 'background_falls_vertical_mirror.png')
		elif choice == 9:
			background = Level_Background(-12, 'background_falls_vertical_mirror.png')
			background.image = pygame.transform.flip(background.image, True, False)	
			background.dirty = 1
		else:
			background = Level_Background(-12, 'background_falls.png')

		#set the top particles for the waterfall. At the bottom here to keep 'random' working.
		for tile in sprites.tile_list:
			if tile.type == 'waterfall':
				tile.set_top_particles()

		#cloud = Cloud([-11], 50, 25, 1, (461,187,177,40), 25)
		#def __init__(self, layer, startx, starty, speed, sprite_rect)

	def build_versus_pump(self):
		pass

	def build_versus_labyrinth(self):
		pass

	def build_versus_ice(self):
		pass

	def build_versus_space(self):
		pass

	def build_versus_testing(self):
		pass

	def build_versus_crucible(self):
		pass

	def build_versus_paradox(self):
		pass

	def build_versus_tartarus(self):
		pass

	def build_versus_mystic_cavern(self):
		pass