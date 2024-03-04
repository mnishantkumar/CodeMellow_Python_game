import pygame

import math
import random
import sprites
import options
import level
import sounds
import data_manager


def dist_check(point1, point2):
	distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
	return distance

def Create_Rope(startxy, endxy, end_fixed = False, rope_type = 'classic'):
	if rope_type == 'classic':
		dist = dist_check(startxy, endxy)
		point_total = round(dist / 12)
	else:
		dist = dist_check(startxy, endxy)
		point_total = round(dist / 12)

	if end_fixed is False:
		test_rope = Rope(startxy,endxy, point_total, [0], rope_type)
	else:
		test_rope = Rope(startxy,endxy, point_total, [0,point_total - 1], rope_type)



	i = 0
	while i < 50:
		test_rope.update_point_physics()
		i += 1

	while test_rope.point_list[-1].true_y > endxy[1]:
		test_rope.point_list[-1].destroy()
		test_rope.segment_list[-1].destroy()
		i = 0
		while i < 50:
			test_rope.update_point_physics()
			i += 1

	#now make rope sawy
	for point in test_rope.point_list:
		if point.point_number == len(test_rope.point_list) - 1:
			point.sway = 0.0005

	return test_rope
			


class Rope(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, startxy, endxy, number_of_points, fixed_point_list, rope_type = 'classic'):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'simple rope'
		self.rope_type = rope_type

		self.online_key = 0


		self.rope_number = options.rope_number
		options.rope_number += 1
		if options.rope_number > 3:
			options.rope_number = 1
		self.collision_check_counter = 1

		

		self.point_list = []
		self.ninja_list = []
		self.fixed_point_list = fixed_point_list

		if rope_type == 'classic':
			self.friction = 0.975
			self.spring_stiffness = 0.85 #spring stiffness
			self.update_switch = 0 #updates every frame
		elif rope_type in ('background wire', 'tube wire'):
			self.friction = 0.95
			self.spring_stiffness = 0.85 #spring stiffness
		self.update_switch = options.update_state #updates every second frame
		options.update_state = not options.update_state
		
		self.spring_length  = self.dist_check(startxy,endxy) / (number_of_points - 1)
		self.point_mass = 1 #/ (number_of_points)# - len(fixed_point_list)) #mass of each ball

		i = 0
		while i < number_of_points: 
		
			if i == 0:
				startx = startxy[0]
				starty = startxy[1]
			else:
				startx = startxy[0] + round((endxy[0] - startxy[0]) / (number_of_points - 1) * i)
				starty = startxy[1] + round((endxy[1] - startxy[1]) / (number_of_points - 1) * i)

			if i in fixed_point_list:
				fixed = True
			else:
				fixed = False

			point = Rope_Point((startx,starty), fixed, self, i)

			self.point_list.append(point)

			i += 1

		for point in self.point_list:
			point.find_neighbors()

		i = 0
		self.segment_list = []
		while i < len(self.point_list) - 1:
			segment = Rope_Segment(self.point_list[i], self.point_list[i + 1], self)
			self.segment_list.append(segment)
			i += 1


		

		self.inverted_g = False

		#only needed for 'test updates'
		sprites.level_ropes.add(self)

		self.frame_counter = 0

		self.test_counter = 0

		self.climbable = True
		self.climbable_timer = 0

		#Just used when testing max distance. Used to create appropriate sized 'segment' sprites.
		#self.max_dist = 0

		height = endxy[1] - startxy[1]
		self.rough_rect = pygame.Rect(startxy[0] - 50, startxy[1] - height, 100, height * 2)


	def update(self):

		if self.climbable_timer > 0:
			self.climbable_timer -= 1
			if self.climbable_timer == 0:
				self.climbable = True

		self.collision_check_counter += 1
		if self.collision_check_counter > 3:
			self.collision_check_counter = 1

		'''
		if sprites.player1.status == 'duck':
			for point in self.point_list:
				y = self.point_list[0].rect.centery
				x = self.point_list[0].rect.centerx - (self.spring_length * point.point_number)

				point.rect.centerx = x
				point.rect.centery = y
				point.true_x = point.rect.centerx
				point.true_y = point.rect.centery

				point.change_x = 0
				point.change_y = 0



		elif sprites.player2.status == 'duck':
			for point in self.point_list:
				y = self.point_list[0].rect.centery
				x = self.point_list[0].rect.centerx + (self.spring_length * point.point_number)

				point.rect.centerx = x
				point.rect.centery = y
				point.true_x = point.rect.centerx
				point.true_y = point.rect.centery

				point.change_x = 0
				point.change_y = 0
		'''

		
		#if sprites.countdown_timer.done is True:
		self.update_point_physics()

		if self.collision_check_counter == self.rope_number:		
			for ninja in sprites.ninja_list:
				if ninja.rect.colliderect(self.rough_rect):
					for point in self.point_list:
						point.update_ninja_collision_physics(ninja)

			for enemy in sprites.enemy_list:
				if enemy.rect.colliderect(self.rough_rect):
					for point in self.point_list:
						point.update_enemy_collision_physics(enemy)

		for ninja in self.ninja_list:
			self.update_ninja_climb(ninja)

		for segment in self.segment_list:
			segment.update()

				#self.test_counter += 1
				#if self.test_counter == 120:
				#	self.test_counter = 0
				#	self.point_list[random.randrange(0,len(self.point_list)-1,1)].destroy()

	def invert_g(self):
		if self.inverted_g is True:
			self.inverted_g = False
		else:
			self.inverted_g = True	

		if len(self.fixed_point_list) < 2:
			self.climbable = False
			self.climbable_timer = 60
			for ninja in self.ninja_list:
				ninja.climb_timer = 10
				self.ninja_list.remove(ninja)
				if ninja.status == 'climb':
					ninja.status = 'falling'
	
	def update_ninja_climb(self, ninja):
		if ninja.status == 'climb':
			if ninja.inverted_g is False:
				temp_rect = pygame.Rect(ninja.rect.x,ninja.rect.centery,ninja.rect.width,24)
			else:
				temp_rect = pygame.Rect(ninja.rect.x,ninja.rect.top,ninja.rect.width,24)

			collision = False
			for point in self.point_list:
				if temp_rect.collidepoint(point.rect.center):
					ninja.rect.centerx = point.rect.centerx + 1
					ninja.set_true_xy('x')
					collision = True
					
					if point.fixed is False and ninja.change_y != 0:
						point.change_x += 0.05 * ninja.rope_climb_mod

					break

			if self.inverted_g is False:
				if ninja.rect.top < self.point_list[0].rect.top:
					ninja.change_y = 0
					ninja.rect.top = self.point_list[0].rect.top
					ninja.set_true_xy('y')
				#elif ninja.rect.bottom > self.point_list[len(self.point_list) - 1].rect.bottom:
				#	if ninja.change_y <= 0: #not pressing down
				#		ninja.change_y = 0
				#		ninja.rect.bottom = self.point_list[len(self.point_list) - 1].rect.bottom
				#		ninja.set_true_xy('y')
			else:
				if ninja.rect.bottom > self.point_list[0].rect.bottom:
					ninja.change_y = 0
					ninja.rect.bottom = self.point_list[0].rect.bottom
					ninja.set_true_xy('y')
				#elif ninja.rect.top < self.point_list[len(self.point_list) - 1].rect.top:
				#	if ninja.change_y >= 0: #not pressing up
				#		ninja.change_y = 0
				#		ninja.rect.top = self.point_list[len(self.point_list) - 1].rect.top
				#		ninja.set_true_xy('y')
			

			if collision is False:
				ninja.climb_timer = 10
				self.ninja_list.remove(ninja)
				if ninja.status == 'climb':
					ninja.status = 'falling'



		else:
			ninja.climb_timer = 10
			self.ninja_list.remove(ninja)

	def kill(self):
		for point in self.point_list:
			point.kill()

		for segment in self.segment_list:
			segment.kill()

		super(Rope, self).kill()

	def update_point_physics(self):
		#First get forces on all points
		for segment in self.segment_list:
			segment.update_spring_forces()

		for point in self.point_list:
			point.update_friction()
			point.apply_sway()
			point.apply_gravity() #applies force from gravity
					
				
		#Now move all points
		for point in self.point_list:
			#point.dirty = 1
						
			point.true_x += point.change_x
			point.true_y += point.change_y
			point.rect.centerx = round(point.true_x)
			point.rect.centery = round(point.true_y)

	
	def dist_check(self, point1, point2):
			distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
			return distance


class Rope_Point(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, centerxy, fixed, rope, point_number):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.rope = rope
		self.fixed = fixed

		self.mass = self.rope.point_mass

		self.point_number = point_number
		self.neighbor_list = []

		if self.fixed is False or self.rope.type == 'bandana':
			self.image = pygame.Surface((1,1))
			#self.image.fill(options.GREEN)
			#self.image.set_colorkey(options.GREEN)
		else:
			if self.rope.rope_type == 'classic':
				self.image = sprites.level_sheet.getImage(113, 267, 17, 16)
			else:
				self.image = pygame.Surface((1,1))
				self.image.fill(options.GREEN)
				self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()
		self.rect.center = centerxy
		'''
		self.image = pygame.Surface((5,5))
		self.image.fill(options.GREEN)
		if fixed is False:
			pygame.draw.circle(self.image, (255,50,50), (3,3), 3, 0)
		else:
			pygame.draw.circle(self.image, (50,255,50), (3,3), 3, 0)
		self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()
		self.rect.center = centerxy
		'''

		self.sway = 0
		self.sway_counter = random.randrange(0,60,1)
		self.sway_mod = 1
		

		self.change_x = 0
		self.change_y = 0

		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery

		if self.rope.rope_type == 'classic':
			layer = 5
		elif self.rope.rope_type == 'background wire':
			layer = -7
		else:
			layer = -6
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)
		#sprites.screen_objects.add(self)

		if self.fixed is True and self.rope.type != 'bandana':
			self.dirty = 1
			self.visible = 1
		else:
			self.dirty = 1
			self.visible = 0


		#calculate spring force between each point #stretched or compressed away from norm
		#Apply force on masses in appropriate dirctions
		#Add graviational foce
		#add other external forces.

	def destroy(self):
		for neighbor in self.neighbor_list:
			neighbor.neighbor_list.remove(self)
		self.rope.point_list.remove(self)


		self.kill()

	def update(self):
		pass
		
	def update_ninja_collision_physics(self, ninja):
		if self.fixed is False and self.rope.rope_type in ('background wire', 'classic'):
			if ninja.status != 'climb' and ninja.collision_rect.collidepoint(self.rect.center):
					self.change_x += ninja.change_x / (40 * ninja.rect.height / 48) * 3
					self.change_y += ninja.change_y / (40 * ninja.rect.height / 48) * 3


	def update_enemy_collision_physics(self, enemy):
		if self.fixed is False and self.rope.rope_type in ('background wire', 'classic'):
			for enemy in sprites.enemy_list:
				if enemy.rect.collidepoint(self.rect.center):
					self.change_x += enemy.change_x / 40 * 3
					self.change_y += enemy.change_y / 40 * 3

		#explosion phyics will originate from explosions so we don't have to check every frame.

	def explosion_force(self, source_center):
		if self.fixed is False and self.rope.rope_type in ('background wire', 'classic'):
			dist = self.rope.dist_check(source_center, self.rect.center)

			if abs(dist) < 1:
				force = 10
			else:
				force = 10 / dist

			adj_side = self.true_x - source_center[0]
			opp_side = self.true_y - source_center[1]


			try:
				angle = math.atan(opp_side / adj_side)
			except ZeroDivisionError:
				angle = math.atan(0)

			x_force = math.cos(angle) * force
			y_force = math.sin(angle) * force
				
			#APPLY VECTORS
			if self.true_y > source_center[1]:
				y_force = abs(y_force)
			else:
				y_force = abs(y_force) * -1

			if self.true_x > source_center[0]:
				x_force = abs(x_force)
			else:
				x_force = abs(x_force) * -1

			self.change_x += x_force
			self.change_y += y_force

	def update_friction(self):
		#self.friction = 0.975#**math.hypot(self.change_x, self.change_y)
		self.change_x *= self.rope.friction
		self.change_y *= self.rope.friction

	def apply_sway(self):
		self.change_x += self.sway * self.sway_mod
		self.sway_counter += 1
		if self.sway_counter > 45:
			self.sway_counter = 0
			self.sway_mod *= -1

	
	def apply_gravity(self):
		#if self.fixed is False:
		#	self.change_y += options.max_g
		#change_g = 0.5
		if self.fixed is False:
			if self.rope.inverted_g is False:
				if self.change_y < options.max_g:
					self.change_y += options.change_g * self.mass

			else:
				if self.change_y > -options.max_g:
					self.change_y -= options.change_g * self.mass


	def find_neighbors(self):
		self.neighbor_list = []
		if self.point_number > 0:
			point = self.point_number - 1
			self.neighbor_list.append(self.rope.point_list[point])

		if self.point_number < len(self.rope.point_list) - 1:
			point = self.point_number + 1
			self.neighbor_list.append(self.rope.point_list[point])

class Rope_Segment(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, point1, point2, rope):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.rope = rope
		self.point1 = point1
		self.point2 = point2

		self.p1 = (0,0) #just to start somewhere
		self.p2 = (0,0)

		self.update_spring_forces
		self.stretched = False


		self.image = pygame.Surface((23,23))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)


		self.rect = self.image.get_rect()

		if self.rope.rope_type == 'classic':
			layer = 4
		elif self.rope.rope_type == 'background wire':
			layer = -9
		else:
			layer = -7

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, layer)

		self.update_switch = self.rope.update_switch

		#sprites.screen_objects.add(self)

	'''
	def update(self):
		self.dirty = 1
		self.image = self.base_image

		if self.point1.true_y <= self.point2.true_y:
			self.rect.top = self.point1.rect.centery - 1
		else:
			self.rect.top = self.point2.rect.centery - 1
		if self.point1.true_x < self.point2.true_x:
			self.rect.left = self.point1.rect.centerx - 1
		else:
			self.rect.left = self.point2.rect.centerx - 1
	'''
	
	def update(self):
		if self.update_switch == 0 or self.update_switch == options.update_state:

			if (self.update_switch == 0 and options.blit_frame is True) or self.update_switch == options.update_state: #only blit every frame at 60fps
				self.dirty = 1
				self.image.fill(options.GREEN)

				if self.point1.true_y <= self.point2.true_y:
					self.rect.top = self.point1.rect.centery - 1
				else:
					self.rect.top = self.point2.rect.centery - 1

				if self.point1.true_x < self.point2.true_x:
					self.rect.left = self.point1.rect.centerx - 1
				else:
					self.rect.left = self.point2.rect.centerx - 1

				self.p1 = (self.point1.rect.centerx - self.rect.left, self.point1.rect.centery - self.rect.top)
				self.p2 = (self.point2.rect.centerx - self.rect.left, self.point2.rect.centery - self.rect.top)

				slopex = self.p1[0] - self.p2[0]
				slopey = self.p1[1] - self.p2[1]

				inverted_slopex = -slopey
				inverted_slopey = -slopex

				#make sure slope is only 1 pixel away
				while abs(round(inverted_slopex)) > 1 or abs(round(inverted_slopey)) > 1:
					inverted_slopex /= 1.1
					inverted_slopey /= 1.1

				if round(inverted_slopex) == 0 and round(inverted_slopey) == 0:
					inverted_slopex = 1
					inverted_slopey = 0



				x_mod = 0
				y_mod = 0


				#zzzzz
				if self.rope.type == 'simple rope':
					if self.rope.rope_type == 'classic':
						pygame.draw.line(self.image,options.BROWN_ROPE_MEDIUM, self.p1, self.p2, 4)
						pygame.draw.line(self.image,options.BROWN_ROPE_LIGHT, self.p1, self.p2, 1)
					elif self.rope.rope_type == 'tube wire':
						pygame.draw.line(self.image, (52,42,54), self.p1, self.p2, 4)
						pygame.draw.line(self.image, (89,78,100), self.p1, self.p2, 1)
					else:
						pygame.draw.line(self.image,options.BLACK_ROPE_MEDIUM, self.p1, self.p2, 4)
						pygame.draw.line(self.image,options.BLACK_ROPE_LIGHT, self.p1, self.p2, 1)
				else:
					pygame.draw.line(self.image, self.rope.color, self.p1, self.p2, 2)

				#if self.rope.ninja.visible_timer > 0:#transition
				#	self.check_visible_fade(point1, point2)


	def check_visible_fade(self):
		if self.rope.ninja.visible_timer > 0 and options.blit_frame is True:#transition

			if self.visible == 0:
				self.visible = 1

			point_number = 4

			slopex = self.p2[0] - self.p1[0]
			slopey = self.p2[1] - self.p1[1]

			i = 0
			while i <= point_number:
				point_mod = random.randrange(1,10,1)

				new_x = self.p1[0] + (slopex / point_mod) + random.choice((-1,0,1,))
				new_y = self.p1[1] + (slopey / point_mod) + random.choice((-1,0,1,))

				pygame.draw.rect(self.image, options.GREEN, (new_x,new_y,1,1), 0)

				i += 1

		
		
	
	'''
	def check_visible_fade(self):
		#pass


		
		if self.rope.ninja.visible_timer > 0: #transition
			if self.visible == 0:
				self.visible = 1
			array = pygame.PixelArray(self.image)
			x = 0
			y = 0
			while y <= self.image.get_height() - 1:
				x = 0
				while x <= self.image.get_width() - 1:
					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):
						array[x,y] = (0,255,0)

					
					if self.rope.ninja.visible_switch is False: #turning invisible
						if self.rope.ninja.visible_timer > 3:
							x_mod = random.choice((1,2))
						else:
							x_mod = random.choice((1,2,3))
					else:
						if self.rope.ninja.visible_timer > 3:
							x_mod = random.choice((1,2,3))
						else:
							x_mod = random.choice((1,2))

					x += x_mod
				y += 1
		else:
			pass
			#self.image = self.base_image
	'''	

	def destroy(self):
		self.rope.segment_list.remove(self)
		self.kill()
	def update_spring_forces(self):
		dist = self.rope.dist_check((self.point1.true_x, self.point1.true_y),(self.point2.true_x,self.point2.true_y))
		force = -self.rope.spring_stiffness * (dist - self.rope.spring_length) * self.rope.friction
		adj_side = self.point2.true_x - self.point1.true_x
		opp_side = self.point2.true_y - self.point1.true_y

		try:
			angle = math.atan(opp_side / adj_side)
		except ZeroDivisionError:
			angle = math.atan(0)

		x_force = math.cos(angle) * force
		y_force = math.sin(angle) * force
				

		#APPLY FORCES to Points
		#spring strethches
		for point in (self.point1, self.point2):
			if point.fixed is False:	
				for other_point in (self.point1, self.point2):
					if other_point != point:
						neighbor = other_point
						break

				if dist >= self.rope.spring_length:
					#y stuff
					if point.true_y > neighbor.true_y:
						y_force = abs(y_force) * -1
					else:
						y_force = abs(y_force)
					#x stuff
					if point.true_x > neighbor.true_x:
						x_force = abs(x_force) * -1
					else:
						x_force = abs(x_force)
						
				else:
					#y stuff
					if point.true_y > neighbor.true_y:
						y_force = abs(y_force)
					else:
						y_force = abs(y_force) * -1
					#x stuff
					if point.true_x > neighbor.true_x:
						x_force = abs(x_force)
					else:
						x_force = abs(x_force) * -1

				point.change_x += x_force
				point.change_y += y_force



class Bandana_Knot(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja, color):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.mass = 1

		self.type = 'bandana knot'

		self.base_image = self.ninja.spritesheet.getImage(50, 196, 5, 5)
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect()

		if self.ninja.direction == 'left':
			self.rect.centerx = self.ninja.rect.right
		else:
			self.rect.centerx = self.ninja.rect.left
		if self.ninja.inverted_g is False:
			self.rect.centery = self.ninja.rect.top + 5
		else:
			self.rect.centery = self.ninja.rect.bottom - 5

		self.rope1 = Bandana_Rope(self,color[1], 1, 1)
		self.rope2 = Bandana_Rope(self,color[1], 2, -1)

		self.rope1.ninja = ninja
		self.rope2.ninja = ninja

		self.headband = Bandana_Headband(self, ninja, color)

		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 0)

		self.change_y = 0
		self.change_x = 0
		self.inverted_g = False

		self.position_dict = {'run' : ((1,7), (1,7), (1,5), (0,4), (2,5), (1,7), (1,7), (1,5), (0,4), (2,5)),
							'idle': ((2,4), (1,6), (0,4), (1,6)),
							'smug': ((13,4), (12,6), (11,4), (12,6)),
							'climb': ((12,4), (12,4), (12,4), (12,4)),
							'falling': ((1,3),(1,6)),
							'slide': ((1,5),(1,5)),
							'knocked back': ((5,-1),(5,-1)),
							'knocked forward': ((0,12),(0,12)),
							'duck': ((4,1),(4,4)),
							'jump': ((4,0),(14,-1),(19,4),(21,13), (16,19), (7,20),(-1,15),(-1,7)),
							'FID': ((12,4), (12,4)),
							'laser': ((0,4), (0,4)),
							'portal': ((0,4), (0,4)),
							'portal up': ((5,19), (6,22), (6,22), (6,22), (5,19)),
							'rocket': ((5,19), (6,22), (6,22), (6,22)),
							'cling': ((20,4),(20,4))
							}


	def update(self):
		self.dirty = 1

		info = self.ninja.bandana_info #(image_type, direction, image_number)
		image_type = info[0]
		direction = info[1]
		image_number = info[2]

		if self.headband.status == 'ninja': #and self.ninja.visible == 1:
			if image_type in self.position_dict:
				position_mod = self.position_dict[image_type][image_number]
				if direction == 'right':
					self.rect.x = self.ninja.rect.x + position_mod[0] - 1
					if self.ninja.inverted_g is False:
						self.rope1.inverted_g = False
						self.rope2.inverted_g = False
						self.rect.y = self.ninja.rect.y + position_mod[1]
					else:
						self.rope1.inverted_g = True
						self.rope2.inverted_g = True
						self.rect.y = self.ninja.rect.bottom - position_mod[1] - 5
				else:
					self.rect.x = self.ninja.rect.right - position_mod[0] - 4
					if self.ninja.inverted_g is False:
						self.rope1.inverted_g = False
						self.rope2.inverted_g = False
						self.rect.y = self.ninja.rect.y + position_mod[1]
					else:
						self.rope1.inverted_g = True
						self.rope2.inverted_g = True
						self.rect.y = self.ninja.rect.bottom - position_mod[1] - 5
			else:
				if self.ninja.direction == 'left':
					self.rect.centerx = self.ninja.rect.right
				else:
					self.rect.centerx = self.ninja.rect.left

				if self.ninja.inverted_g is False:
					self.rect.centery = self.ninja.rect.top + 5
				else:
					self.rect.centery = self.ninja.rect.bottom - 5
		
			self.true_x = self.rect.centerx
			self.true_y = self.rect.centery
			self.check_visible_fade()



	def check_visible_fade(self):
		if self.ninja.visible_timer > 0: #transition
			
			for segment in self.rope1.segment_list:
				segment.check_visible_fade()

			for segment in self.rope2.segment_list:
				segment.check_visible_fade()
			

			if self.visible == 0:
				self.visible = 1
			i = self.base_image.copy()
			array = pygame.PixelArray(i)
			x = 0
			y = 0
			while y <= i.get_height() - 1:
				x = 0
				while x <= i.get_width() - 1:
					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):
						if self.ninja.visible_switch is False: #turning invisible
							if self.ninja.visible_timer > 3:
								visible = random.choice((True,False))
							else:
								visible = random.choice((True,False,False))
						else:
							if self.ninja.visible_timer > 3:
								visible = random.choice((True,False,False))
							else:
								visible = random.choice((True,False))
						if visible is False:
							array[x,y] = (0,255,0)
					x += 1
				y += 1
			self.image = i
		else:
			self.image = self.base_image





	def flip_visible(self, visible_type):
		if visible_type == 'invisible':
			self.visible = 0
			for segment in self.rope1.segment_list:
				segment.visible = 0

			for segment in self.rope2.segment_list:
				segment.visible = 0

			self.headband.visible = 0

		if visible_type == 'visible':
			self.visible = 1
			for segment in self.rope1.segment_list:
				segment.visible = 1

			for segment in self.rope2.segment_list:
				segment.visible = 1

			self.headband.visible = 1

	def new_position(self):
		if self.headband.status == 'ninja':
			self.update()
		else:
			self.headband.lure_knot()
		self.rope1.follow_knot()
		self.rope2.follow_knot()
		for point in self.rope1.point_list:
			if point != self.rope1.point_list[0]:
				point.rect.centerx = self.rope1.point_list[0].rect.centerx + point.startx
				point.rect.centery = self.rope1.point_list[0].rect.centery + point.starty
				point.true_x = point.rect.centerx
				point.true_y = point.rect.centery
				point.change_x = 0
				point.change_y = 0

		for point in self.rope2.point_list:
			if point != self.rope2.point_list[0]:
				point.rect.centerx = self.rope2.point_list[0].rect.centerx + point.startx
				point.rect.centery = self.rope2.point_list[0].rect.centery + point.starty
				point.true_x = point.rect.centerx
				point.true_y = point.rect.centery
				point.change_x = 0
				point.change_y = 0

	def crumble(self):
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.image.get_height() - 1:
			x = 0
			while x <= self.image.get_width() - 1:
				color = self.image.unmap_rgb(array[x,y])
				if color != (0,255,0):
					sprites.particle_generator.enemy_death_particle(self.inverted_g, color, (self.rect.x + x, self.rect.y + y), self.rect, 'debris')


				x += random.choice((1,2))
			y += random.choice((1,2))

		array = pygame.PixelArray(self.headband.image)
		x = 0
		y = 0
		while y <= self.headband.image.get_height() - 1:
			x = 0
			while x <= self.headband.image.get_width() - 1:
				color = self.headband.image.unmap_rgb(array[x,y])
				if color != (0,255,0):
					sprites.particle_generator.enemy_death_particle(self.inverted_g, color, (self.headband.rect.x + x, self.headband.rect.y + y), self.headband.rect, 'debris')


				x += random.choice((2,3))
			y += random.choice((2,3))

		for segment in self.rope1.segment_list:
			array = pygame.PixelArray(segment.image)
			x = 0
			y = 0
			while y <= segment.image.get_height() - 1:
				x = 0
				while x <= segment.image.get_width() - 1:
					color = segment.image.unmap_rgb(array[x,y])
					if color != (0,255,0):
						sprites.particle_generator.enemy_death_particle(self.inverted_g, color, (segment.rect.x + x, segment.rect.y + y), segment.rect, 'debris')


					x += random.choice((2,3))
				y += random.choice((2,3))

		self.kill()

	def kill(self, headband=False):
		self.rope1.kill()
		self.rope2.kill()
		if headband is False:
			self.headband.kill()
		super(Bandana_Knot, self).kill()
 

class Bandana_Rope(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, knot, color, number, sway_mod):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.type = 'bandana'
		self.rope_type = 'classic'
		#tracks / differentiates the ropes, apply alternating forces.
		self.sway_mod = sway_mod
		self.sway_counter = 0
		self.knot = knot
		self.color = color
		self.number = number

		self.friction = 0.8

		number_of_points = 4
		self.point_list = []

		startxy = knot.rect.center
		endxy = (knot.rect.centerx, knot.rect.centery + 12)

		self.spring_stiffness = 0.9 #spring stiffness
		self.spring_length  = self.dist_check(startxy,endxy) / (number_of_points - 1)
		self.point_mass = 1 #/ (number_of_points)# - len(fixed_point_list)) #mass of each ball

		self.update_switch = 0

		i = 0
		while i < number_of_points: 
		
			if i == 0:
				startx = startxy[0]
				starty = startxy[1]
			else:
				startx = startxy[0] + round((endxy[0] - startxy[0]) / (number_of_points - 1) * i)
				starty = startxy[1] + round((endxy[1] - startxy[1]) / (number_of_points - 1) * i)

			if i == 0:
				fixed = True
			else:
				fixed = False

			point = Rope_Point((startx,starty), fixed, self, i)
			point.startx = startx - startxy[0]
			point.starty = starty - startxy[1]

			self.point_list.append(point)

			i += 1

		for point in self.point_list:
			point.find_neighbors()

		i = 0
		self.segment_list = []
		while i < len(self.point_list) - 1:
			segment = Rope_Segment(self.point_list[i], self.point_list[i + 1], self)
			self.segment_list.append(segment)
			sprites.active_sprite_list.change_layer(segment, 0)
			i += 1


		

		self.inverted_g = False

		#only needed for 'test updates'
		sprites.background_objects.add(self)

		self.frame_counter = 0

		self.test_counter = 0

	def update(self):
		self.follow_knot()

		if self.knot.ninja.status != 'Frozen':
			self.update_point_physics()

		for segment in self.segment_list:
			segment.update()

	def follow_knot(self):
		if self.number == 1:
			if self.knot.ninja.direction == 'left':
				#self.point_list[0].rect.center = self.knot.rect.right
				self.point_list[0].true_x = self.knot.rect.right - 2
				if self.knot.ninja.inverted_g is False:
					self.point_list[0].true_y = self.knot.rect.top + 1
				else:
					self.point_list[0].true_y = self.knot.rect.bottom - 2
			else:
				#self.point_list[0].rect.center = self.knot.rect.right
				self.point_list[0].true_x = self.knot.rect.left
				if self.knot.ninja.inverted_g is False:
					self.point_list[0].true_y = self.knot.rect.top + 1
				else:
					self.point_list[0].true_y = self.knot.rect.bottom - 2
			self.point_list[0].rect.centerx = round(self.point_list[0].true_x)
			self.point_list[0].rect.centery = round(self.point_list[0].true_y)

		elif self.number == 2:
			if self.knot.ninja.direction == 'left':
				#self.point_list[0].rect.center = self.knot.rect.right
				self.point_list[0].true_x = self.knot.rect.right - 4
				if self.knot.ninja.inverted_g is False:
					self.point_list[0].true_y = self.knot.rect.top + 2
				else:
					self.point_list[0].true_y = self.knot.rect.bottom - 2
			else:
				#self.point_list[0].rect.center = self.knot.rect.right
				self.point_list[0].true_x = self.knot.rect.left + 2
				if self.knot.ninja.inverted_g is False:
					self.point_list[0].true_y = self.knot.rect.top + 2
				else:
					self.point_list[0].true_y = self.knot.rect.bottom - 2
			self.point_list[0].rect.centerx = round(self.point_list[0].true_x)
			self.point_list[0].rect.centery = round(self.point_list[0].true_y)

		if self.knot.ninja.status == 'frozen':
			if self.inverted_g is False:
				gravity_mod = 1
			else:
				gravity_mod = -1

			for point in self.point_list:
				#point.true_x = self.point_list[0].true_x + point.startx
				#point.true_y = self.point_list[0].true_y + point.starty
				point.true_x = self.knot.ninja.rect.centerx
				point.true_y = self.knot.ninja.rect.centery
				point.rect.centerx = round(point.true_x)
				point.rect.centery = round(point.true_y)
				point.change_x = 0
				point.change_y = 0





	def invert_g(self):
		if self.inverted_g is True:
			self.inverted_g = False
		else:
			self.inverted_g = True	


	def kill(self):
		for point in self.point_list:
			point.kill()

		for segment in self.segment_list:
			segment.kill()

		super(Bandana_Rope, self).kill()

	def update_point_physics(self):
		#First get forces on all points
		for segment in self.segment_list:
			segment.update_spring_forces()

		for point in self.point_list:
			point.update_friction()
			point.apply_gravity() #applies force from gravity
		
		
		
		#apply bandana sway
		'''
		x_sway = (abs(self.knot.ninja.change_y) / 10) + 0.1
		y_sway = abs(self.knot.ninja.change_x) / 6

		self.sway_counter += 1
		if self.sway_counter in (0,1,2,3,4):
			#self.point_list[1].change_x += x_sway * self.sway_mod
			self.point_list[3].change_y += y_sway * self.sway_mod

		if self.sway_counter >= 10:
			self.sway_counter = 0
			self.sway_mod *= -1
		'''
		

		#Now move all points
		for point in self.point_list:
			#point.dirty = 1
						
			point.true_x += point.change_x
			point.true_y += point.change_y
			point.rect.centerx = round(point.true_x)
			point.rect.centery = round(point.true_y)
	
	def dist_check(self, point1, point2):
			distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
			return distance


class Bandana_Headband(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, knot, ninja, color):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.knot = knot
		self.color = color

		self.type = 'bandana headband'

		self.image_list = []
		self.right_image = self.ninja.spritesheet.getImage(56,196,20,5)
		self.image_list.append(self.right_image)
		self.left_image = self.ninja.spritesheet.getImage(77,196,20,5)
		self.image_list.append(self.left_image)
		self.knocked_back_right = self.ninja.spritesheet.getImage(50,203,17,12)
		self.image_list.append(self.knocked_back_right)
		self.knocked_back_left = self.ninja.spritesheet.getImage(85,202,17,12)
		self.image_list.append(self.knocked_back_left)
		self.knocked_forward_right = self.ninja.spritesheet.getImage(68,202,16,16)
		self.image_list.append(self.knocked_forward_right)
		self.knocked_forward_left = self.ninja.spritesheet.getImage(103,202,16,16)
		self.image_list.append(self.knocked_forward_left)
		self.FID = self.ninja.spritesheet.getImage(98,197,18,4)
		self.image_list.append(self.FID)
		self.falling_image = self.ninja.spritesheet.getImage(120,197,20,7)
		self.image_list.append(self.falling_image)
		i = self.falling_image.copy()
		self.rising_image = pygame.transform.flip(i, False, True)
		self.image_list.append(self.rising_image)
		
		self.image_list.append(self.knot.image)
		self.image_list.append(self.knot.base_image)

		self.change_color(None, self.color)

		if self.ninja.direction == 'right':
			self.image = self.right_image
		else:
			self.image = self.left_image

		self.rect = self.image.get_rect()

		self.status = 'ninja' #ninja or free
		self.direction = None
		self.change_x = 0
		self.change_y = 0
		self.true_y = 0
		self.true_x = 0
		self.inverted_g = False

		#used for FIDS
		self.mallow = None

		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 1)

		'''
		self.position_dict = {'run' : ((2,6), (2,6), (2,4), (1,3), (3,4), (2,6), (2,6), (2,4), (1,3), (3,4)),
							'idle': ((3,3), (2,5), (1,3), (2,5)),
							'smug': ((3,3), (2,5), (1,3), (2,5)),
							'climb': ((2,3), (2,3), (2,3), (2,3)),
							'falling': ((2,3),(2,5)),
							'slide': ((1,4),(1,4)),
							'knocked back': ((6,1),(6,1)),
							'knocked forward': ((1,0),(1,0)),
							'duck': None,
							'jump': None,
							'FID': ((3,2), (3,2)),
							'laser': ((1,3), (1,3)),
							'portal': ((1,3), (1,3)),
							'portal up': None,
							'rocket': None,
							'cling': ((3,3),(3,3))
							}
		'''
		self.position_dict = self.ninja.position_dict


	def update(self):
		self.dirty = 1
		if self.status == 'ninja':
			info = self.ninja.bandana_info #(image_type, direction, image_number)
			image_type = info[0]
			direction = info[1]
			image_number = info[2]

			if self.position_dict[image_type] == None or self.ninja.visible == 0:
				self.visible = 0

				#follow ninja so in right place for death
				if self.ninja.inverted_g is False:
					self.rect.top = self.ninja.rect.top + 3
				else:
					self.rect.bottom = self.ninja.rect.bottom - 3
				self.rect.centerx = self.ninja.rect.centerx
			else:
				self.visible = 1

				self.update_image(image_type, direction)

				if image_type in self.position_dict:
					position_mod = self.position_dict[image_type][image_number]
					if direction == 'right':
						self.rect.x = self.ninja.rect.x + position_mod[0]
						if self.ninja.inverted_g is False:
							self.knot.rope1.inverted_g = False
							self.knot.rope2.inverted_g = False
							self.rect.y = self.ninja.rect.y + position_mod[1]
						else:
							self.knot.rope1.inverted_g = True
							self.knot.rope2.inverted_g = True
							self.rect.y = self.ninja.rect.bottom - position_mod[1] - self.rect.height
					else:
						self.rect.x = self.ninja.rect.right - position_mod[0] - self.rect.width
						if self.ninja.inverted_g is False:
							self.knot.rope1.inverted_g = False
							self.knot.rope2.inverted_g = False
							self.rect.y = self.ninja.rect.y + position_mod[1]
						else:
							self.knot.rope1.inverted_g = True
							self.knot.rope2.inverted_g = True
							self.rect.y = self.ninja.rect.bottom - position_mod[1] - self.rect.height
				else:
					if self.ninja.direction == 'left':
						self.rect.centerx = self.ninja.rect.right
					else:
						self.rect.centerx = self.ninja.rect.left

					if self.ninja.inverted_g is False:
						self.rect.centery = self.ninja.rect.top + 5
					else:
						self.rect.centery = self.ninja.rect.bottom - 5

				#if self.ninja.status == 'lose':
				#	#trigger knot physics / throw knot.
				#	self.status = 'free'
				#	self.direction = self.ninja.direction
				#	self.true_x = self.rect.centerx
				#	self.true_y = self.rect.centery
			
		elif self.status == 'free':
			self.dirty = 1
			self.update_image(None, self.direction)
			self.apply_gravity()

			if self.mallow != None:
				if self.mallow.inverted is True:
					mod = -1
				else:
					mod = 1

				self.chang_x = 0
				self.change_y = 2 * mod

			self.true_x += self.change_x
			self.true_y += self.change_y
			self.rect.centerx = round(self.true_x)
			self.rect.centery = round(self.true_y)


			self.tile_check()
			self.lure_knot()

			self.boundary_check()

		if self.ninja.swag == 'None':
			self.kill()
			self.knot.kill()
		elif self.ninja.swag == 'Headband' or options.bandana_physics == 'Off':
			self.knot.kill(headband=True) #kills everything except the headband
			if options.bandana_physics == 'Off':
				if self.ninja.swag == 'Bandana':
					self.ninja.swag = 'Headband'
			

	def invert_g(self, direction):
		if direction == None:
			if self.inverted_g is True:
				self.inverted_g = False
			else:
				self.inverted_g = True
		elif direction == True:
			self.inverted_g = True
		elif direction == False:
			self.inverted_g = False

		self.knot.inverted_g = self.inverted_g
		self.knot.rope1.inverted_g = self.inverted_g
		self.knot.rope2.inverted_g = self.inverted_g
	
	def boundary_check(self):
		if options.loop_physics is True:
			if self.change_x < 0:
				if self.rect.right < 0:
					self.rect.left = sprites.size[0]
					self.true_x = self.rect.centerx
					self.knot.new_position()

			elif self.change_x > 0:
				if self.rect.left > sprites.size[0]:
					self.rect.right = 0
					self.truex_x = self.rect.centerx
					self.knot.new_position()

			if self.change_y < 0:
				if self.rect.bottom < 0:
					self.rect.top = sprites.size[1]
					self.true_y = self.rect.centery
					self.knot.new_position()

			elif self.change_y > 0:
				if self.rect.top > sprites.size[1]:
					self.rect.bottom = 0
					self.true_y = self.rect.centery
					self.knot.new_position()

	def set_free(self, inverted_g):
		self.inverted_g = inverted_g
		self.status = 'free'
		self.direction = self.ninja.direction
		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery

		self.knot.flip_visible('visible') #make visible
		self.knot.image = self.knot.base_image
		sprites.active_sprite_list.change_layer(self,0)
		
		if self.ninja.swag == 'Bandana':
			sprites.active_sprite_list.change_layer(self.knot,-1)

			for segment in self.knot.rope1.segment_list:
				sprites.active_sprite_list.change_layer(segment,-2)

			for segment in self.knot.rope2.segment_list:
				sprites.active_sprite_list.change_layer(segment,-2)

		sprites.gravity_effects.add(self)

	def tile_check(self):
		self.current_tile_list = sprites.quadrant_handler.get_quadrant(self)

		collision_rect = pygame.Rect(self.rect.x + 5, self.rect.y, self.rect.width - 10, self.rect.height)
		for tile in self.current_tile_list:
			if tile.type == 'platform' or tile.type == 'tile':
				if tile.rect.colliderect(collision_rect):
					if self.change_y > 0:
						self.image = self.right_image.copy()
						self.rect = self.image.get_rect()
						self.rect.centerx = round(self.true_x)
						self.rect.bottom = tile.rect.top
						self.change_y = 0
						self.true_y = self.rect.centery

					elif self.change_y < 0:
						i = self.right_image.copy() #self.image.copy()
						self.image = pygame.transform.flip(i, False, True)
						self.rect = self.image.get_rect()
						self.rect.centerx = round(self.true_x)
						self.rect.top = tile.rect.bottom
						self.change_y = 0
						self.true_y = self.rect.centery

			elif tile.type == 'mallow':
				if self.mallow == None:
					if tile.rect.colliderect(self.rect):
						self.mallow = tile
						if tile.inverted is True:
							temp_xy = self.rect.midtop
						else:
							temp_xy = self.rect.midbottom
						sprites.particle_generator.FID_particles(temp_xy, tile.inverted, self)

				if self.mallow != None:
					if self.rect.centery < tile.rect.centery + 5 and self.rect.centery > tile.rect.centery - 5:
						self.knot.kill()

	def apply_gravity(self):
		if self.inverted_g is False:
			if self.change_y < options.max_g:
				self.change_y += options.change_g

		else:
			if self.change_y > -options.max_g:
				self.change_y -= options.change_g

	def lure_knot(self):
		'''
		if self.direction == 'left':
			self.knot.true_y = self.rect.centery
			self.knot.true_x = self.rect.right

		elif self.direction == 'right':
			self.knot.true_y = self.rect.centery
			self.knot.true_x = self.rect.left
		
		self.knot.rect.centerx = round(self.knot.true_x)
		self.knot.rect.centery = round(self.knot.true_y)
		'''


		if self.direction == 'left':
			self.knot.rect.centery = self.rect.centery
			self.knot.rect.centerx = self.rect.right

		elif self.direction == 'right':
			self.knot.rect.centery = self.rect.centery
			self.knot.rect.centerx= self.rect.left
		
		self.knot.true_x = self.knot.rect.centerx 
		self.knot.true_y = self.knot.rect.centery


	def update_image(self, image_type, direction):
		if image_type == 'knocked back':
			if direction == 'left':
				self.image = self.knocked_back_left
			else:
				self.image = self.knocked_back_right

		elif image_type == 'knocked forward':
			if direction == 'left':
				self.image = self.knocked_forward_left
			else:
				self.image = self.knocked_forward_right

		elif image_type == 'FID':
			self.image = self.FID

		elif direction == 'left':
			self.image = self.left_image

		elif direction == 'right':
			self.image = self.right_image

		if self.status == 'ninja':
			if self.ninja.inverted_g is True:
				i = self.image.copy()
				self.image = pygame.transform.flip(i, False, True)
		else:
			if self.change_y > 0.75:
				self.image = self.falling_image
			elif self.change_y < -0.75:
				self.image = self.rising_image
			else:
				self.image = self.right_image
				if self.inverted_g is True:
					i = self.image.copy()
					self.image = pygame.transform.flip(i, False, True)

		self.rect = self.image.get_rect()

		if self.ninja in sprites.ninja_list: #not dead!
				self.check_visible_fade()

	def check_visible_fade(self):
		if self.ninja.visible_timer > 0: #transition
			if self.visible == 0:
				self.visible = 1
			i = self.image.copy()
			array = pygame.PixelArray(i)
			x = 0
			y = 0
			while y <= i.get_height() - 1:
				x = 0
				while x <= i.get_width() - 1:
					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):
						if self.ninja.visible_switch is False: #turning invisible
							if self.ninja.visible_timer > 3:
								visible = random.choice((True,False))
							else:
								visible = random.choice((True,False,False))
						else:
							if self.ninja.visible_timer > 3:
								visible = random.choice((True,False,False))
							else:
								visible = random.choice((True,False))
						if visible is False:
							array[x,y] = (0,255,0)
					x += 1
				y += 1
			self.image = i


	def change_color(self, direction, color):

		#if self.ninja.bandana_color == None: #Initially make headband same color as ninja
		#	old_color = options.RED_LIST

		if color == None:
			i = options.bandana_color_choices.index(self.color) #used to change color via menu
			if direction == 'right':
				i += 1
				if i > len(options.bandana_color_choices) - 1:
					i = 0
			elif direction =='left':
				i -= 1
				if i < 0:
					i = len(options.bandana_color_choices) - 1

			old_color = self.color
			self.color = options.bandana_color_choices[i]
			self.knot.rope1.color = self.color[1]
			self.knot.rope2.color = self.color[1]
			self.ninja.bandana_color = self.color
		else: #used to change color when placing ninja
			old_color = options.RED_LIST
			self.ninja.bandana_color = color
			self.color = color
			self.knot.rope1.color = color[1]
			self.knot.rope2.color = color[1]
		

		for image in self.image_list:
				array = pygame.PixelArray(image)
				array.replace(old_color[0], self.color[0])
				array.replace(old_color[1], self.color[1])
				array.replace(old_color[2], self.color[2])
				array.replace(old_color[3], self.color[3])

		self.knot.image = self.knot.base_image.copy()
		#self.knot.dirty = 1

