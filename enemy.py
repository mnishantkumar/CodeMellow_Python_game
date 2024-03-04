#import pygame_sdl2
#pygame_sdl2.import_as_pygame()

import pygame

import math
import random
import sprites
import options
import level
import sounds
import data_manager

class Enemy(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, phase_in = False):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.current_tile_list = []

		self.online_update_trigger = False

		self.type = 'Enemy'

		self.destroyed = False #flipped to true on death. Prevents some endless online kill attemps.

		self.subsprite_list = []

		self.current_quadrant = None

		self.max_knock_y = -3.6
		self.max_knock_x = 1.6

		self.inverted_g = False

		self.land_mod_x = 2 #how much the landing zone on platforms shrinks

		self.freezable = False
		self.frozen = False
		self.frozen_type = 'knock' #'knock', 'static'

		self.FID_possible = True #can this be FIDed?
		self.FID = False
		self.FID_source = None #holds mallow

		self.physics = 'normal'

		self.friction_applies = True
		self.x_accel = 0.5 #how much x_speed can change each frame
		self.icy_x_accel = 0.04 #how much change_x can change each frame.
		self.bounce_var = 0.4
		self.wall_bounce_var = 1

		self.portal_delay = 0

		self.particle_type = 'debris' #stick, debris

		self.change_x = 0
		self.change_y = 0

		self.mass = 1 #1.5 is metal suit

		#used to remove controls for 0.5 seconds after collision
		self.collision_timer = 0 #temporarily locks out controls after collision
		self.collision_timer_max = 30


		self.last_collision = None
		self.last_collision_timer = 0
		self.last_collision_timer_max = 14 #how long between 'possible collisions' between two sprites

		self.current_tile = None

		self.phase_in = phase_in
		if self.phase_in is True:
			self.visible_timer = 20
		else:
			self.visible_timer = 0




	def update(self):
		if self.status != 'death': #not presently death animation

			self.current_tile_list = sprites.quadrant_handler.get_quadrant(self)

			if self.collision_timer > 0:
				self.collision_timer -= 1

			if self.portal_delay > 0:
				self.portal_delay -= 1

			if self.last_collision_timer > 0:
				self.last_collision_timer -= 1
				if self.last_collision_timer == 0:
					self.last_collision = None

			self.apply_gravity()
			if self.friction_applies is True:
				self.apply_friction()
			self.apply_FID()

			self.true_x += self.change_x
			self.true_y += self.change_y

			self.rect.centerx = round(self.true_x)
			self.rect.centery = round(self.true_y)

			self.tile_collision_check()
			self.ninja_collision_check()
			self.enemy_collision_check()	

			if self.phase_in is True:
				self.visible_timer -= 1
				self.turn_visible()
				if self.visible_timer == 0:
					self.phase_in = False

	
	def turn_visible(self):
		if self.visible == 0:
			self.visible = 1
		i = self.image.copy()
		i.lock()
		array = pygame.PixelArray(i)
		x = 0
		y = 0
		while y <= i.get_height() - 1:
			x = 0
			while x <= i.get_width() - 1:
				color = self.image.unmap_rgb(array[x,y])
				if color != (0,255,0):
					if self.visible_timer > 13:
						visible = random.choice((True,False,False,False))
					elif self.visible_timer > 7:
						visible = random.choice((True,False))
					else:
						visible = random.choice((True,True,True,False))
					
					if visible is False:
						array[x,y] = (0,255,0)
				x += 1
			y += 1
		i.unlock()
		self.image = i


		self.frame_counter += 1

		if self.inverted_g is True and options.blit_frame is True:
			i = self.image.copy()
			self.image = pygame.transform.flip(i, False, True)

	def enemy_collision_check(self):
			if self.frozen is True:
				for enemy in sprites.enemy_list:
					if enemy != self and self.last_collision != enemy:
						if enemy.frozen is True:
							if enemy.rect.colliderect(self.rect):
								self.last_collision = enemy
								self.last_collision_timer = self.last_collision_timer_max
								if self.frozen_type == 'knock':
									if self.rect.centerx <= enemy.rect.centerx:
										self.change_x = -(self.ice_cube.knock_speed / 2)
										if enemy.frozen_type == 'knock':
											enemy.change_x = enemy.ice_cube.knock_speed / 2
									else:
										self.change_x = self.ice_cube.knock_speed / 2
										if enemy.frozen_type == 'knock':
											enemy.change_x = -(enemy.ice_cube.knock_speed / 2)
						else:
							if enemy.rect.colliderect(self.rect):
								if 'ice cube' in enemy.death_list:
									enemy.destroy()
								else:
									self.last_collision = enemy
									self.last_collision_timer = self.last_collision_timer_max
									if self.frozen_type == 'knock':
										if self.rect.centerx <= enemy.rect.centerx:
											self.change_x = -(self.ice_cube.knock_speed / 2)
											enemy.change_x = enemy.max_knock_x / 2
											enemy.change_y = enemy.max_knock_y / 2
										else:
											self.change_x = self.ice_cube.knock_speed / 2
											enemy.change_x = -enemy.max_knock_x / 2
											enemy.change_y = enemy.max_knock_y / 2

									if enemy.inverted_g is True:
										enemy.change_y *= -1



			else: #not Frozen'
				for collision_type in self.collision_dict.keys():
					if collision_type == 'normal':
						for enemy in sprites.enemy_list:
							if enemy != self and self.last_collision != enemy and enemy.frozen is False:
								for enemy_collision_type in enemy.collision_dict.keys():
									if enemy_collision_type == 'normal':
										if self.collision_dict[collision_type].colliderect(enemy.collision_dict[enemy_collision_type]):
											self.last_collision = enemy
											self.last_collision_timer = self.last_collision_timer_max
											enemy.last_collision = self
											enemy.last_collision_timer = enemy.last_collision_timer_max
											self.collision_timer = self.collision_timer_max
											enemy.collision_timer = enemy.collision_timer_max

											#set y_forces
											if self.inverted_g is False:
												self.change_y = self.max_knock_y
											else:
												self.change_y = -self.max_knock_y

											if enemy.inverted_g is False:
												enemy.change_y = enemy.max_knock_y
											else:
												enemy.change_y = -enemy.max_knock_y

											#set x_forces
											if self.rect.centerx <= enemy.rect.centerx:
												self.change_x = self.max_knock_x * -1
												enemy.change_x = enemy.max_knock_x
											else:
												self.change_x = self.max_knock_x
												enemy.change_x = enemy.max_knock_x * -1

											#set animations
											self.collision_bounce(enemy)
											enemy.collision_bounce(self)



	def land(self, y_speed):
		pass					
	
	def bounce(self): #bounce off floor
		pass #may hold enemey-specific animation stuff

	def collision_bounce(self, source): #bounce off other sprite
		pass #may hold enemey-specific animation stuff

	def wall_bounce(self): #bounce off wall
		self.collision_timer = self.collision_timer_max
		#pass #may hold enemy-specific animation stuff

	def ninja_collision_check(self):
			for collision_type in self.collision_dict.keys():
				for ninja in sprites.ninja_list:

						ninja_base_y = ninja.change_y
						ninja_centery = ninja.rect.centery
						if ninja.collision_rect.colliderect(self.collision_dict[collision_type]) and self.last_collision != ninja:
							self.last_collision = ninja
							self.last_collision_timer = self.last_collision_timer_max
							#ninja.collision_timer = ninja.collision_timer_max
							ninja.last_collision = ninja.collision_timer_max

							if self.inverted_g is True:
								y_mod = -1
							else:
								y_mod = 1

							if ninja.inverted_g is True:
								ninja_y_mod = -1
							else:
								ninja_y_mod = 1

							if ninja.item == 'metal suit':
								ninja_mass = 1.5
							else:
								ninja_mass = 1
							ninja_knock_mod = self.mass / ninja_mass
							enemy_knock_mod = ninja_mass / self.mass


							if self.frozen is True:
								if self.frozen_type == 'knock':
									if ninja.status == 'frozen':
										if ninja.rect.centerx > self.rect.centerx: #ninja on right
											ninja.change_x = ninja.ice_cube.knock_speed / 2
											self.change_x = -(self.ice_cube.knock_speed / 2)
										else: #otherninja on right
											ninja.change_x = -(ninja.ice_cube.knock_speed / 2)
											self.change_x = self.ice_cube.knock_speed / 2

									elif ninja.status == 'metal pound':
										if 'metal pound' in self.death_list:
											self.destroy()

									else:
										ninja.collision_timer = ninja.collision_timer_max
										if ninja.status == 'climb':
											ninja.status = 'idle'
										
										if ninja.rect.centerx < self.rect.centerx: #ninja on right
											self.change_x = self.ice_cube.knock_speed
											self.change_y = (self.max_knock_y / 2) * y_mod
											ninja.change_x = -ninja.max_knock_x * ninja_knock_mod# / 2
											ninja.change_y = ninja.max_knock_y * ninja_y_mod * ninja_knock_mod
										else: #otherninja on right
											self.change_x = -self.ice_cube.knock_speed
											self.change_y = (self.max_knock_y / 2) * y_mod
											ninja.change_x = ninja.max_knock_x * ninja_knock_mod# / 2
											ninja.change_y = ninja.max_knock_y * ninja_y_mod * ninja_knock_mod

							elif self.frozen is False and ninja.status == 'frozen':
									if 'ice cube' in self.death_list:
										self.destroy()
									if ninja.rect.centerx > self.rect.centerx: #ninja on right
										ninja.change_x = ninja.ice_cube.knock_speed / 2
										self.change_x = -(self.max_knock_x / 2)
										self.change_y = (self.max_knock_y / 2) * y_mod
										ninja.collision_timer = ninja.collision_timer_max
									else: #otherninja on right
										ninja.change_x = -(ninja.ice_cube.knock_speed / 2)
										self.change_x = (self.max_knock_x / 2)
										self.change_y = (self.max_knock_y / 2) * y_mod
										ninja.collision_timer = ninja.collision_timer_max


							
							elif collision_type == 'kill':
								ninja.activate_death_sprite(None, self)


							elif collision_type == 'ghost':
								if ninja.status in ('jump', 'roll', 'duck'):
									ninja.collision_timer = ninja.collision_timer_max
									
									ninja.change_y = ninja.max_knock_y * y_mod * ninja_knock_mod

									if ninja.rect.centerx < self.rect.centerx - 1:
										ninja.change_x = ninja.max_knock_x * -1 * ninja_knock_mod
									elif ninja.rect.centerx > self.rect.centerx + 1:
										ninja.change_x = ninja.max_knock_x * ninja_knock_mod

									if ninja.status == 'duck':
										ninja.status = 'jump'
										ninja.frame_counter = 0
										ninja.image_number = 0

									

									#if destroyed, destroy. Else, get knocked.
									if any(i in ('jump', 'roll') for i in self.death_list):
										self.destroy()
									else:
										self.collision_timer = self.collision_timer_max

										if ninja.rect.centerx < self.rect.centerx - 1:
											self.change_x = self.max_knock_x * ninja_knock_mod
										elif ninja.rect.centerx > self.rect.centerx + 1:
											self.change_x = self.max_knock_x * -1 * ninja_knock_mod
										
										self.change_y = self.max_knock_y * ninja_knock_mod * y_mod #y_mod accounts for gravity

							elif collision_type == 'normal':
								
								if ninja.status in ('jump', 'roll', 'duck'):
									ninja.collision_timer = ninja.collision_timer_max
									
									ninja.change_y = ninja.max_knock_y * ninja_y_mod * ninja_knock_mod

									if ninja.rect.centerx <= self.rect.centerx:
										ninja.change_x = ninja.max_knock_x * -1 * ninja_knock_mod
									elif ninja.rect.centerx > self.rect.centerx:
										ninja.change_x = ninja.max_knock_x * ninja_knock_mod

									if ninja.status == 'duck':
										ninja.status = 'jump'
										ninja.frame_counter = 0
										ninja.image_number = 0


									#if destroyed, destroy. Else, get knocked.
									if any(i in ('jump', 'roll') for i in self.death_list):
										self.destroy()
									else:
										self.collision_timer = self.collision_timer_max

										if ninja.rect.centerx <= self.rect.centerx:
											self.change_x = self.max_knock_x * enemy_knock_mod
										elif ninja.rect.centerx > self.rect.centerx:
											self.change_x = self.max_knock_x * -1 * enemy_knock_mod
										
										self.change_y = self.max_knock_y * enemy_knock_mod * y_mod #y_mod accounts for gravity

								elif ninja.status not in ('metal pound'):
									
									if self.rect.centerx <= ninja.rect.centerx: #ninja on the left
										self.change_x = self.max_knock_x * -1 * enemy_knock_mod
										self.change_y = self.max_knock_y * y_mod * enemy_knock_mod

										ninja.status = 'knocked'
										ninja.frame_counter = 0
										sounds.mixer.knocked.play()
										ninja.change_x = ninja.max_knock_x * ninja_knock_mod
										ninja.change_y = ninja.max_knock_y * ninja_y_mod * ninja_knock_mod

									elif self.rect.centerx > ninja.rect.centerx: #ninja on theright
										self.change_x = self.max_knock_x * enemy_knock_mod
										self.change_y = self.max_knock_y * y_mod * enemy_knock_mod

										ninja.status = 'knocked'
										ninja.frame_counter = 0
										sounds.mixer.knocked.play()
										ninja.change_x = ninja.max_knock_x * -1 * ninja_knock_mod
										ninja.change_y = ninja.max_knock_y * ninja_y_mod * ninja_knock_mod

									if ninja.tight_space is True:
										old_centery = ninja.rect.centery
										ninja.shrink('knocked')
										ninja.rect.centery = old_centery
										ninja.set_true_xy('xy')




								elif ninja.status == 'metal pound':
									pound = False
									if self.inverted_g is False:
										if abs(ninja.rect.bottom - self.rect.top) <= 12:
											pound = True
									else:
										if abs(ninja.rect.top - self.rect.bottom) <= 12:
											pound = True
									
									if pound is True and 'metal pound' in self.death_list:
										self.destroy()
									else:
										ninja.status = 'jump'
										ninja.frame_counter = 0

										'''copied from above'''
										ninja.collision_timer = ninja.collision_timer_max
										ninja.change_y = ninja.max_knock_y * ninja_y_mod * ninja_knock_mod

										if ninja.rect.centerx <= self.rect.centerx:
											ninja.change_x = ninja.max_knock_x * -1 * ninja_knock_mod
										elif ninja.rect.centerx > self.rect.centerx:
											ninja.change_x = ninja.max_knock_x * ninja_knock_mod

										if ninja.status == 'duck':
											ninja.status = 'jump'
											ninja.frame_counter = 0
											ninja.image_number = 0
										#if destroyed, destroy. Else, get knocked.
										if any(i in ('jump', 'roll') for i in self.death_list):
											self.destroy()
										else:
											self.collision_timer = self.collision_timer_max

											if ninja.rect.centerx <= self.rect.centerx:
												self.change_x = self.max_knock_x * enemy_knock_mod
											elif ninja.rect.centerx > self.rect.centerx:
												self.change_x = self.max_knock_x * -1 * enemy_knock_mod
											
											self.change_y = self.max_knock_y * enemy_knock_mod * y_mod #y_mod accounts for gravity
										'''done copying from above'''


								self.collision_bounce(ninja)

							#to prevent FID errors
							if ninja.FID is True:
								ninja.change_y = ninja_base_y
								ninja.change_x = 0
								ninja.rect.centery = ninja_centery
								ninja.true_y = ninja.rect.y
							

							break


	def pre_kill(self, reset_kill = False):
		self.crumble()
		self.kill()


	def destroy(self):
		if self.frozen is True:
			self.ice_cube.shatter()

		self.pre_kill()

	def crumble(self):
		if self.death_type == 'crumble':
			#print(self.image)
			#self.image.fill(options.BLACK)
			
			self.image.lock()
			array = pygame.PixelArray(self.image)
			#print(array)
			x = 1
			y = 1
			while y <= self.image.get_height() - 1:
				x = 0
				while x <= self.image.get_width() - 1:


					#print((x,y))
					#print(array)
					#print(array[x,y])
					color = self.image.unmap_rgb(array[x,y])
					#color = (1,1,1)
					if color != (0,255,0):
						sprites.particle_generator.enemy_death_particle(self.inverted_g, color, (self.rect.x + x, self.rect.y + y), self.rect, self.particle_type)


					x += random.choice((3,4,5))
				y += random.choice((3,4,5))
			self.image.unlock()

			#self.pre_kill()

			#now take care of any subsprites
			for sprite in self.subsprite_list:
				if self.death_type == 'crumble':
					self.image.lock()
					array = pygame.PixelArray(sprite.image)
					x = 0
					y = 0
					while y <= sprite.image.get_height() - 1:
						x = 0
						while x <= sprite.image.get_width() - 1:

							color = sprite.image.unmap_rgb(array[x,y])
							if color != (0,255,0):
								sprites.particle_generator.single_debris_particle(self.inverted_g, color, (sprite.rect.x + x, sprite.rect.y + y), sprite.rect)


							x += random.choice((2,3,4))
						y += random.choice((2,3,4))
					self.image.unlock()
				sprite.kill()


			

	def freeze(self):
		if 'freeze' in self.death_list:
			self.destroy()
		else:
			self.ice_cube.freeze_enemy()

	def apply_FID(self):
		if self.FID is True:
			if self.FID_source.inverted is False:
				self.change_x = 0
				self.change_y = 0.5
				if self.rect.top > self.FID_source.rect.top + 10:
					self.pre_kill()
					#self.kill()
			else:
				self.change_x = 0
				self.change_y = -0.5
				if self.rect.bottom < self.FID_source.rect.bottom - 10:
					self.pre_kill()

	
	def apply_friction(self):
		current_tile_list = sprites.quadrant_handler.get_quadrant(self)

		apply_friction = False
		
		if self.frozen is True:
			friction_type = 'icy'
		else:
			friction_type = 'normal'
			if self.inverted_g is False:
				friction_rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1)
				for tile in sprites.tile_list:
					if tile.type == 'tile' or tile.type == 'platform':
						if tile.rect.colliderect(friction_rect):
							apply_friction = True
							if tile.top_friction == 'icy':
								friction_type = 'icy'
								break

			else:
				friction_rect = pygame.Rect(self.rect.left, self.rect.top - 1, self.rect.width, 1)
				for tile in sprites.tile_list:
					if tile.type == 'tile' or tile.type == 'platform':
						if tile.rect.colliderect(friction_rect):
							apply_friction = True
							if tile.bottom_friction == 'icy':
								friction_type = 'icy'
								break



		if friction_type == 'icy':
			if self.change_x > self.icy_x_accel:
				self.change_x -= self.icy_x_accel
			elif self.change_x < -self.icy_x_accel:
				self.change_x += self.icy_x_accel
			else:
				self.change_x = 0

		elif friction_type == 'normal':
			if self.change_x > self.x_accel:
				self.change_x -= self.x_accel
			elif self.change_x < -self.x_accel:
				self.change_x += self.x_accel
			else:
				self.change_x = 0

	def apply_gravity(self):
		if self.physics in ('normal', 'bounce') or self.frozen is True:
			if self.inverted_g is False:
				if self.change_y < options.max_g:
					self.change_y += options.change_g
			else:
				if self.change_y > (options.max_g * -1):
					self.change_y -= options.change_g

	def dist_check(self, point1, point2):
		distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
		return distance

	def tile_collision_check(self):
		
		#Make sure not on top of portal
		portal = False
		if self.portal_delay == 0:
			for item in sprites.active_items:
				if item.type == 'portal_gun_portal':
					if self.rect.colliderect(item.collision_rect):
						if len(item.portal_gun.active_portal_list) == 2: #portal to teleport to!
							portal = True
							break

		if (self.physics != 'ghost' or self.frozen is True) and portal is False and self.FID is False:
			current_tile_list = sprites.quadrant_handler.get_quadrant(self)
			temp_list = []

			if 0 == 0:#(self.change_x != 0 or self.change_y != 0):
				last_tile = None
				for tile in current_tile_list:#current_tile_list:
					if tile.rect.colliderect(self.rect):
						if tile.type == 'platform' or tile.type == 'tile':
							temp_list.append(tile)

						elif tile.type == 'mallow_wall':
							if tile.rect.colliderect(self.rect):
								if self.change_x > 0:
									self.rect.right = tile.rect.left
									self.true_x = self.rect.centerx
								elif self.change_x < 0:
									self.rect.left = tile.rect.right
									self.true_x = self.rect.centerx
								if self.physics == 'bounce' or self.frozen is True:
									self.change_x *= -self.wall_bounce_var
									self.wall_bounce()
								
						elif tile.type == 'mallow': #NEED TO FIX FIDS
								if self.FID is False and tile.rect.colliderect(self.rect):
									if self.frozen is True:
										self.ice_cube.shatter()
									if tile.inverted is True:
										temp_xy = self.rect.midtop
									else:
										temp_xy = self.rect.midbottom
									sprites.particle_generator.FID_particles(temp_xy, tile.inverted, self)
									if self.FID_possible is True:
										self.FID = True
										self.FID_source = tile
										#i = sprites.active_sprite_list.get_layer_of_sprite(tile)
										#sprites.active_sprite_list.change_layer(self, i - 2)
										#sprites.active_sprite_list.change_layer(self.ice_cube, i - 1)

				enemy_tile_list = []
				for tile in temp_list:
					if tile.type == 'tile':
						enemy_tile_list.append(tile)
					
					if len(enemy_tile_list) > 0:
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
								for tile in enemy_tile_list:
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
							#make temp rects FIRST so changing positions doesn't affect collisions.
							temp_right_rect = pygame.Rect(self.rect.right,self.rect.y + 1,1,self.rect.height - 2)
							temp_left_rect = pygame.Rect(self.rect.left - 1,self.rect.y + 1,1,self.rect.height - 2)
							temp_bottom_rect = pygame.Rect(self.rect.x + self.land_mod_x,self.rect.bottom,self.rect.width - (self.land_mod_x * 2),1)
							temp_top_rect = pygame.Rect(self.rect.x + self.land_mod_x,self.rect.top - 1,self.rect.width - (self.land_mod_x * 2),1)
							if self.change_x > 0:
								for tile in first_tile_list:
									#temp_rect = pygame.Rect(self.rect.right,self.rect.y + 1,1,self.rect.height - 2)
									if tile.rect.colliderect(temp_right_rect):
										last_tile = tile
										self.rect.right = tile.rect.left
										self.true_x = self.rect.centerx
										if self.physics == 'bounce' or self.frozen is True:
											self.change_x *= -self.wall_bounce_var
											self.wall_bounce()
										else:
											self.change_x = 0
										break

							elif self.change_x < 0:
								for tile in first_tile_list:
									#temp_rect = pygame.Rect(self.rect.left - 1,self.rect.y + 1,1,self.rect.height - 2)
									if tile.rect.colliderect(temp_left_rect):
										last_tile = tile
										self.rect.left = tile.rect.right
										self.true_x = self.rect.centerx
										if self.physics == 'bounce' or self.frozen is True:
											self.change_x *= -self.wall_bounce_var
											self.wall_bounce()
										else:
											self.change_x = 0
										break

							#Now fix y_direction. bomb should currently be JUST before a collision.
							#Get closest tile

							if self.change_y > 0:
								for tile in first_tile_list:
									#temp_rect = pygame.Rect(self.rect.x + self.land_mod_x,self.rect.bottom,self.rect.width - (self.land_mod_x * 2),1)
									if tile.rect.colliderect(temp_bottom_rect):
										last_tile = tile
										self.rect.bottom = tile.rect.top
										self.true_y = self.rect.centery
										if self.physics == 'bounce' and self.frozen is False:
											if self.inverted_g is False:
												self.change_y *= -self.bounce_var
												self.bounce()
											else:
												self.change_y *= -self.bounce_var
												self.bounce()
										else:
											self.land(self.change_y)
											self.change_y = 0
										break

							elif self.change_y < 0:
								for tile in first_tile_list:
									#temp_rect = pygame.Rect(self.rect.x + self.land_mod_x,self.rect.top - 1,self.rect.width - (self.land_mod_x * 2),1)
									if tile.rect.colliderect(temp_top_rect):
										last_tile = tile
										self.rect.top = tile.rect.bottom
										self.true_y = self.rect.centery
										if self.physics == 'bounce' and self.frozen is False:
											if self.inverted_g is True:
												self.change_y *= -self.bounce_var
												self.bounce()
											else:
												self.change_y *= -self.bounce_var
												self.bounce()
										else:
											self.land(self.change_y)
											self.change_y = 0
											
										break

				#now do platforms!
				for tile in temp_list:

						if tile.type == 'platform':
							if self.inverted_g is False: #makes sure top isn't covered by another tile
								temp_rect = pygame.Rect(self.rect.left + self.land_mod_x, self.rect.bottom - 6, self.rect.width - (self.land_mod_x * 2), 6)
								#pygame.Rect(self.rect.x + 2,self.rect.bottom - 1,self.rect.width - 4,2)
								if temp_rect.colliderect(tile.top_rect) and self.change_y >= 0:
									last_tile = tile
									self.rect.bottom = tile.rect.top
									self.true_y = self.rect.centery
									if self.physics == 'bounce' and self.frozen is False:
										self.change_y *= -self.bounce_var
										self.bounce()
									else:
										self.land(self.change_y)
										self.change_y = 0
										
									break
									#bounce = True
									
							elif self.inverted_g is True: #makes sure bottom of tile -inverted top- is available.
								temp_rect = pygame.Rect(self.rect.left + self.land_mod_x, self.rect.top, self.rect.width - (self.land_mod_x * 2), 6)
								#pygame.Rect(self.rect.x + 2,self.rect.top - 1,self.rect.width - 4,2)
								if temp_rect.colliderect(tile.bottom_rect) and self.change_y <= 0:
									last_tile = tile
									self.rect.top = tile.rect.bottom
									self.true_y = self.rect.centery
									if self.physics == 'bounce' and self.frozen is False:
										self.change_y *= -self.bounce_var
										self.bounce()
									else:
										self.land(self.change_y)
										self.change_y = 0

									break


			#now find 'current closest tile' to sprite bottom. For AI purposes
			temp_current_tile = None
			self.current_tile = None
			for tile in temp_list:
				if tile.type == 'platform' or tile.type == 'tile':
					if (self.inverted_g is False and self.rect.bottom <= tile.rect.top) or (self.inverted_g is True and self.rect.top >= tile.rect.bottom): 
						if self.inverted_g is False:
							dist = self.dist_check(self.rect.midbottom,tile.rect.midtop)
						else:
							dist = self.dist_check(self.rect.midtop, tile.rect.midbottom)
										
						if temp_current_tile == None:
							self.current_tile = tile
							temp_current_tile = (tile,dist)
						else:
							if dist < temp_current_tile[1]:
								self.current_tile = tile
								temp_current_tile = (tile,dist)


class Ice_Cube_Sprite(pygame.sprite.DirtySprite):

	def __init__(self, enemy, coord):
		self.type = 'enemy ice cube'

		pygame.sprite.DirtySprite.__init__(self)

		self.enemy = enemy

		self.ice_cube = sprites.enemy_sheet.getImage(coord[0], coord[1], coord[2], coord[3])
		self.ice_cube.set_alpha(200)

		self.image = self.ice_cube.copy()
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.active = False
		self.cube_timer = 0
		self.knock_speed = 4

	def update(self):
		if self.active is True:

			self.visible = 1
			self.dirty = 1
			self.cube_timer -= 1
			if self.cube_timer == 0:
				self.shatter()

			self.collision_check()

			self.rect.centerx = self.enemy.rect.centerx
			if self.enemy.inverted_g is False:
				self.rect.bottom = self.enemy.rect.bottom
			else:
				self.rect.top = self.enemy.rect.top

			
	def shatter(self):
		sprites.particle_generator.break_ice_particles(self.rect, self.enemy.inverted_g, 'snow_finish')
		sounds.mixer.shatter.play()
		self.reset()
	
	def freeze_enemy(self):
		self.cube_timer = 300
		if self.enemy.status != 'frozen':
			sounds.mixer.freeze.play()

			#if self.enemy.inverted_g is True:
			#	self.ninja.frozen_image = pygame.transform.flip(self.ninja.frozen_image, False, True)
			#self.ninja.frozen_image.set_colorkey((0,255,0))
			#self.ninja.status = 'frozen'
			self.enemy.frozen = True
			self.enemy.status = 'frozen'
			self.active = True

			#self.enemy.base_layer = sprites.active_sprite_list.get_layer_of_sprite(self.enemy)
			#sprites.active_sprite_list.change_layer(self.enemy, 1)
		

	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.active = False
		self.cube_timer = 0
		#sprites.active_sprite_list.change_layer(self.enemy, self.enemy.base_layer)
		self.active
		self.enemy.status = 'idle'
		self.enemy.frozen = False

	def collision_check(self):
		pass
		#moved to level collision check.


class Target(Enemy):
	def __init__(self, centerxy, phase_in = False):
		#constructor function
		Enemy.__init__(self, phase_in)

		#pygame.sprite.DirtySprite.__init__(self)

		self.image_list = []
		

		image = sprites.enemy_sheet.getImage(70, 305, 24, 24)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(95, 305, 24, 24)
		self.image_list.append(image)
		image = sprites.enemy_sheet.getImage(120, 305, 24, 24)
		self.image_list.append(image)

		self.image_number = 0
		self.image = self.image_list[2]
		self.rect = self.image.get_rect()
		self.frame_counter = 0

		self.rect.center = centerxy
		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery

		sprites.enemy_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 0)

		self.dirty = 1


		self.freezable = False
		self.frozen = False

		#self.ice_cube = enemy.Ice_Cube_Sprite(self,(0,388,19,12))

		self.status = 'idle'

		self.physics = 'ghost' #'ghost', 'normal', 'stick'

		self.collision_dict = 	{'ghost' : pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2), 
								'death' : pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)

								}

		self.ice_cube = Ice_Cube_Sprite(self,(0,305,24,24))

		self.death_list = ['collision', 'jump', 'roll', 'explosion', 'laser', 'volt', 'metal pound', 'ice cube'] #jump, roll, metal pound, explosion, laser
		self.death_type = 'crumble' #crumble, explode,
		#self.particle_type = 'stick'
		self.dirty = 1


		self.max_knock_x = 0
		self.max_knock_y = 0

	def update(self):
		self.dirty = 1
		'''
		self.image = 
		if self.image_number < len(self.image_list) - 1:
			self.frame_counter += 1
			if self.frame_counter >= 10:
				self.dirty = 1
				self.frame_counter = 0
				self.image_number +=1
				if self.image_number >= len(self.image_list):
					self.image_number = 0
				self.image = self.image_list[self.image_number]
		'''
		self.image = self.image_list[2]

		self.update_collision_dict()

		self.base_xy = self.rect.center

		#The following are handled in the Enemy Class. Gravity, Tile Collisions, movex_y
		super(Target, self).update()
		
		#to fix random 'frozen' error. Fixed by making max knock y and x 0
		'''
		self.change_x = 0
		self.change_y = 0
		self.rect.center = self.base_xy
		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery
		'''



	def pre_kill(self):
		self.ice_cube.kill()
		self.kill()

	def update_collision_dict(self):
		self.collision_dict['ghost'] = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)
		self.collision_dict['death'] = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)
		#self.collision_dict['tile' ] = pygame.Rect(self.rect.x + 2, self.rect.y, self.rect.width - 4, self.rect.height)
