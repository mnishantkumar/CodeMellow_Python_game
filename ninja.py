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
import rope_physics
import controls
import menus

class Ninja(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, start_point, player_number, spritesheet):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)


		#self.color_choices = (options.RED_LIST, options.GREEN_LIST, options.BLUE_LIST, options.PINK_LIST, options.GREY_LIST, options.PURPLE_LIST, options.ORANGE_LIST)

		self.spritesheet = spritesheet

		self.gamepad_config = False #used to lockout menu controls during controller mapping
		self.gamepad_layout = None #just start with basic layout

		self.type = 'Ninja'
		self.dummy = False #Used to add dummies to single player matches.

		#Only used/set during online play.
		self.online_type = 'local' #local or online. Only used/set during online play.
		self.ip = None
		self.online_ID = 0 #will be 1,2,3,4
		self.online_frame = 0 #counts up 1 at a time. Used to only use most current
		self.local_collision_ID = 0 #personal collision attempt number. Referrences online_ID of other ninjas. Sent OUT each frame to other ninjas each frame.
		self.online_collision_ID_list = [] #list of IDs attempting to collide with local ninja.
		self.port = None
		self.host = False
		self.online_starting_position = (0,0)
		self.online_platform_key = None #Used to make ninja sit nicely on moving platform if its in it's sticky rect

		self.online_player_select_timer = 0

		self.online_update_trigger = False
		self.online_update_counter = 0

		self.item_dict = {} #used to store weapons for online sorting purposes 
		self.item_key_number = 0 #counst up sequentially

		self.player_number = player_number

		self.name = ""

		self.lives = 3

		self.rating = None #used for awards purposes

		if player_number == 1:
			self.profile = "Player1"
		elif player_number == 2:
			self.profile = "Player2"
		elif player_number == 3:
			self.profile = "Player3"
		elif player_number == 4:
			self.profile = "Player4"

		self.bandana_info = None #(holds tuple, image_type, direction)
		self.bandana = None
		self.bandana_color = None

		self.swag = 'Bandana' #currently 'Bandana', 'Headband', or 'None'
		self.swag_list = ['Bandana', 'Headband', 'None']

		self.avatar = 'Ninja' #currently 'Human', 'Robot', Cyclops
		self.avatar_list = ['Ninja', 'Robot', 'Cyclops']

		self.respawn_timer = 0


		#self.name_bar = None


		self.rope_climb_mod = 1 #just use to sway ropes back and forth gently

		self.current_quadrant = None

		#holds image for 'awards' screen. Built in 'menus'
		self.stats_screen = None
		self.awards_screen = None

		self.profile_number = 0
		self.profile_text = '' #used to write in new profiles
		self.text_case = 'uppercase'
		self.text_number = 0
		self.text_blink = 0 #used to let ninja specific text blink

		self.menu_status = ""

		self.big_image_list = []
		

		self.death_sprite = DeathSprite(self)
		

		self.splash_sprite = SplashSprite(self)
		self.item_effect1 = Item_Effect_Sprite(self, 0)
		self.item_effect2 = Item_Effect_Sprite(self, 1)
		self.item_effect3 = Item_Effect_Sprite(self, 2)

		self.spawn_sprite = Spawn_Sprite(self)


		self.feather_effect1 = Feather_Effect_Sprite(self,1)
		self.feather_effect2 = Feather_Effect_Sprite(self,2)
		self.feather_effect3 = Feather_Effect_Sprite(self,3)
		self.feather_effect4 = Feather_Effect_Sprite(self,4)
		self.feather_effect5 = Feather_Effect_Sprite(self,5)
		self.feather_effect6 = Feather_Effect_Sprite(self,6)

		self.name_bar = Name_Bar_Sprite(self)
		self.choice_bar = Choice_Bar_Sprite(self)
		self.score_bar = Score_Bar_Sprite(self)
		self.stock_bar = Stock_Bar_Sprite(self)
		self.controls_sprite = Controls_Sprite(self)
		self.text_sprite = Text_Sprite(self)

		self.awards_screen_sprite = Award_Screen_Sprite(self)

		self.projectile1 = Projectile_Sprite(self, 0)
		self.projectile2 = Projectile_Sprite(self, 1)
		self.projectile3 = Projectile_Sprite(self, 2)
		self.projectile4 = Projectile_Sprite(self, 3)
		self.projectile5 = Projectile_Sprite(self, 4)
		self.projectile6 = Projectile_Sprite(self, 5)

		self.rocket = Rocket_Sprite(self)

		#up to 4 homing bombs.
		#self.homing_bomb1 = Homing_Bomb(self)
		#self.homing_bomb2 = Homing_Bomb(self)
		#self.homing_bomb3 = Homing_Bomb(self)
		#self.homing_bomb4 = Homing_Bomb(self)

		self.mine_list = []
		self.mine1 = Mine_Sprite(self, 0)
		self.mine_list.append(self.mine1)
		self.mine2 = Mine_Sprite(self, 1)
		self.mine_list.append(self.mine2)
		self.mine3 = Mine_Sprite(self, 2)
		self.mine_list.append(self.mine3)
		self.mine4 = Mine_Sprite(self, 3)
		self.mine_list.append(self.mine4)
		self.mine5 = Mine_Sprite(self, 4)
		self.mine_list.append(self.mine5)
		self.mine6 = Mine_Sprite(self, 5)
		self.mine_list.append(self.mine6)

		self.bomb_sprite = Bomb_Sprite(self)

		self.ice_bomb_sprite = Ice_Bomb_Sprite(self)

		self.volt_sprite = Volt_Sprite(self)

		self.shield_sprite = Shield_Sprite(self)

		self.standing_image = pygame.Surface((24,48))
		rand1 = random.randrange(0,255,1)
		rand2 = random.randrange(0,255,1)
		rand3 = random.randrange(0,255,1)
		self.standing_image.fill((rand1,rand2,rand3), rect = None)

		self.ducking_image = pygame.Surface((24,24))
		self.ducking_image.fill((rand1,rand2,rand3), rect = None)


		self.image = self.standing_image

		self.rect = self.image.get_rect()
		self.dirty = 1

		self.rect.centerx = start_point[0]
		self.rect.centery = start_point[1]

		self.x_speed_max = 2 #max speed for left to right movement
		self.x_accel = 0.5 #how much x_speed can change each frame

		self.max_knock_y = -3.6
		self.max_knock_x = 1.6

		self.friction = 'normal' #normal or 'icy'
		self.icy_x_accel = 0.04 #how much change_x can change each frame.
		self.fire_x_speed = 0 #used to skirt weird collision_rules

		self.frozen_image = None #will turn into frozen image big/small as needed
		self.frozen_image_big = pygame.Surface((24,48)) #holds spot to blit large frozen image once frozen
		self.frozen_image_small = pygame.Surface((24,24)) #holds spot to blit small frozen image once frozen
		self.ice_cube = Ice_Cube_Sprite(self)

		self.climb_speed = 2
		self.climb_timer = 0 #must be zero to initiate climb. Brief lockout following droping off ladder
		self.climb_jump_timer = 0 #lets you jump for a brief window after falling off rope
		self.climb_lock = 0 #used to lock you into climbing briefly, prevents falling off the rope immediately.

		self.knock_timer = 0
		self.max_knock_timer = 300

		self.confused = False
		self.confused_timer = 0

		self.metal_pound_timer = 0

		#attibutes to update every frame
		self.last_change_x = 0
		self.last_change_y = 0
		self.change_x = 0
		self.change_y = 0

		self.loop_physics = False #True if bottom-top and left-right screens are connected
		self.moving_platform = False #flips to true if impacted by moving platform. Allows only one platform to affect ninja each frame.
		#gravity settings HELD IN OPTIONS NOW
		#self.change_g = 0.8
		#self.max_g = 9
		self.jump_force = -4.2
		self.double_jump = False
		self.projectile_count = 0 #will 'end item' after enough uses. Depends on item.
		self.jump_held = False #holds if jump button is being held down.
		self.inverted_g = False #inverts gravity
		self.hold_duck = False #allows duck to be held when landing.
		#self.roll_force = 3 Got rid of this! Now just use x_speed max. Smoother application of shoes.
		self.roll_duration = 25
		self.roll_timer = 0

		self.item_counter = 0

		self.tight_space = False #true if tile space is 48 or smaller
		self.tight_top_tile = None #holds tile that makes up 'top'
		self.tight_bottom_tile = None

		self.tight_trip_space = False #true if tile space is 48 or smaller
		self.tight_trip_top_tile = None #holds tile that makes up 'top'
		self.tight_trip_bottom_tile = None

		#self.cling_x_burst = 3 #how fast you push off wall following cling-jump

		self.wall_knock = 2

		self.land_frame = False #True if just landed. Will turn on 'land_frame'
		self.land_frame_counter = 0

		self.visible_timer = 0 #true if switching to/from visible.
		self.visible_switch = True #true if going visible

		self.collision_timer = 0 #temporarily locks out controls after collision
		self.collision_timer_max = 30

		self.tile_particle_timer = 0
		self.knocked_particle_timer = 0

		self.last_collision = None #holds 'name' of last ninja collided
		self.last_collision_timer = 0 #restes 'name' at 0. Counts down.

		self.collision_check_needed = True #makes it go through collision check until not needed

		self.item = 'none'
		self.status = 'idle'	#idle, jump, left, right, duck, roll, fall, knocked
		self.direction = 'right' #right or left
		self.FID = False #is True if fall in the 'drink'
		self.win = False #true if win conditions are met.
		self.current_VP = 0 #needs to meet options.vp_required for 'series win'
		self.current_wins = 0 #needs to meet options.wins_required for 'series win'

		self.image_number = 0 #holds current frame number for animations.
		self.frame_counter = 0 #counts up and tell sthe image_number/frame when to change.

		self.portal_delay = 0 #brief delay after portal use in which you cannot be sent through another portal
		self.wind_speed = 0
		self.fall_timer = 0 #resets to 0 every time you land. Used for stats. Also used to delay wind effect when falling... just to let you get over edge.
		
		self.mallow = None #holds mallow of FID
		self.rope = None #holds current rope

		self.on_fire = False
		self.on_fire_timer = 0

		self.color = options.BLUE_LIST
		self.build_ninja() #builds ninja images based on 'self.spritesheet'

		

		

		#change color of mask/legs using pixelarray. Colors go 'dark, middle, light'
		#COLOR LIST moved to options
		#RED = ((192,34,20), (221,57,57), (255,245,247))
		#GREEN = ((27,116,74), (91,190,97), (209,255,204))
		#BLUE = ((52,58,241), (34,116,255), (150,218,255))
		#PINK = ((217,72,221), (241,118,255), (254,245,246))
		#GREY = ((97,84,118), (163,146,212), (210,204,243))
		#PURPLE = ((97,24,149), (143,75,237), (242,237,254))
		#ORANGE = ((241,110,3), (253,164,20), (255,226,44))

		temp_list = []
		for ninja in sprites.ninja_list:
			if ninja != self:
				temp_list.append(ninja.color)

		#self.color_choices = (options.RED_LIST, options.GREEN_LIST, options.BLUE_LIST, options.PINK_LIST, options.GREY_LIST, options.PURPLE_LIST, options.ORANGE_LIST)
		self.color = random.choice(options.color_choices)
		while self.color in temp_list:
			self.color = random.choice(options.color_choices)

		
		
		default_color = options.BLUE_LIST #default color on sprite sheet
		
		for image_list in self.big_image_list:
			for image in image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace(default_color[0], self.color[0])
				array.replace(default_color[1], self.color[1])
				array.replace(default_color[2], self.color[2])
				array.replace(default_color[3], self.color[3])
				image.unlock()

		for image_list in self.death_sprite.big_image_list:
			for image in image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace(default_color[0], self.color[0])
				array.replace(default_color[1], self.color[1])
				array.replace(default_color[2], self.color[2])
				array.replace(default_color[3], self.color[3])
				image.unlock()



		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 1)


		#These are held here to facilitate menu controls.
		#modified from within controls.input_handler
		self.menu_up_press = False
		self.menu_down_press = False
		self.menu_left_press = False
		self.menu_right_press = False

		self.menu_select_press = False
		self.menu_back_press = False

		self.menu_start_press = False
		self.menu_y_press = False
		self.menu_x_press = False

		self.menu_press_delay = 0

		#create extra personal rects for collision purposes. Updated regularly.
		self.collision_rect = pygame.Rect(self.rect.left + 2, self.rect.top + 2, self.rect.width - 4, self.rect.height - 4)
		
		self.rect_top = pygame.Rect(self.rect.left + 2, self.rect.top + 2, self.rect.width - 4, 8)
		self.rect_bottom = pygame.Rect(self.rect.left + 2, self.rect.bottom - 7, self.rect.width - 4, 5)
		self.rect_left = pygame.Rect(self.rect.left + 2, self.rect.top + 2, 5, self.rect.height - 4)
		self.rect_right = pygame.Rect(self.rect.right - 9, self.rect.top + 2, 5, self.rect.height - 4)

		self.true_x = 0
		self.true_y = 0

		#self.rect_top_right = None
		#self.rect_top_left = None
		#self.rect_bottom_right = None
		#self.rect_bottom_left = None

		self.rect_top_middle = None
		self.rect_bottom_middle = None

		self.left_held = False
		self.right_held = False
		self.down_held = False

		self.smug = False

		#used for STAT tracking. Held here only temporarily.
		self.FID_inflictor = None
		self.FID_inflicted = 0

		self.stats_awards_list = [] #used to hold up to three awards after match is over.
		
		#STATS TO TRACK!!!!! These stats are kept for the match (however many duels). On Exit, OR on end of Duel, ninja profiles are updated.
		self.stats_FIDs_inflicted = 0 #done
		self.stats_FIDs_received = 0 #done
		self.stats_FIDs_suicide = 0 #done
		self.stats_item_kills = 0 #done
		self.stats_item_deaths = 0 #done
		self.stats_ally_item_kill = 0 #done
		self.stats_ally_FIDs_inflicted = 0 #done
		self.VP_earned = 0 #peronal VP earned. vs currentVP which as a team stat.
		self.wins_earned = 0 #personal wins earned. Vs currentWins which is a team stat
		self.stats_x_pixels_travelled = 0 #done
		self.stats_y_pixels_travelled = 0 #done
		self.stats_jumps_performed = 0 #done
		self.stats_frames_jumping = 0 #done
		self.stats_wall_jumps_performed = 0 #done
		self.stats_rolls_performed = 0 #done
		self.stats_ducks_performed = 0 #done
		self.stats_frames_rolling = 0 #done
		self.stats_frames_falling = 0 #done
		self.stats_frames_running = 0 #done
		self.stats_frames_idle = 0 #done
		self.stats_frames_smug = 0 #done
		self.stats_frames_ducking = 0 #done
		self.stats_knocks_received = 0 #done
		self.stats_knocks_inflicted = 0 #done


		self.stats_shoes_acquired = 0 #done
		self.stats_shoes_pixels_travelled = 0 #done


		self.stats_laser_acquired = 0 #done
		self.stats_laser_fired = 0 #done
		self.stats_laser_kills = 0 #done
		self.stats_laser_suicides = 0 #done
		self.stats_laser_double_kills = 0 #done
		self.stats_laser_triple_kills = 0 #done
		self.stats_laser_vertical_kills = 0 #done

		self.stats_wings_acquired = 0 #done
		self.stats_wing_double_jumps = 0 #done

		self.stats_skull_acquired = 0 #done

		self.stats_bomb_acquired = 0 #done
		self.stats_bomb_thrown = 0 #done
		self.stats_bomb_kills = 0 #done
		self.stats_bomb_suicides = 0 #done
		self.stats_bomb_double_kills = 0 #done
		self.stats_bomb_triple_kills = 0 #done

		self.stats_volt_acquired = 0 #done
		self.stats_volt_kills = 0 #done
		self.stats_volt_double_kills = 0 #done
		self.stats_volt_triple_kills = 0 #done

		self.stats_mine_acquired = 0 #done
		self.stats_mine_thrown = 0 #done
		self.stats_mine_kills = 0 #done
		self.stats_mine_suicides = 0 #done
		self.stats_mine_double_kills = 0 #done
		self.stats_mine_triple_kills = 0 #done

		self.stats_rocket_acquired = 0 #done
		self.stats_rocket_fired = 0 #done
		self.stats_rocket_pixels_travelled = 0 #done
		self.stats_rocket_kills = 0 #done
		self.stats_rocket_suicides = 0 #done
		self.stats_rocket_double_kills = 0 #done
		self.stats_rocket_triple_kills = 0 #done

		self.stats_portal_gun_acquired = 0 #done
		self.stats_portal_gun_fired = 0 #done
		self.stats_portal_gun_portals_created = 0 #done
		self.stats_portal_gun_ninjas_teleported = 0 #done
		self.stats_portal_gun_FIDs_inflicted = 0 #Done!
		self.stats_portal_gun_FIDs_received = 0 #Done!
		self.stats_portal_gun_times_teleported = 0 #done
		self.stats_portal_gun_distance_teleported = 0 #done
		self.stats_portal_gun_items_teleported = 0 #done

		self.stats_ice_bomb_acquired = 0 #done
		self.stats_ice_bomb_thrown = 0 #done
		self.stats_ice_bomb_cubes_made = 0 #done
		self.stats_ice_bomb_self_cubes = 0 #done
		self.stats_ice_bomb_times_frozen = 0 #done
		self.stats_ice_bomb_cube_FIDs = 0
		self.stats_ice_bomb_double_cubes = 0 #done
		self.stats_ice_bomb_triple_cubes = 0 #done
		self.stats_ice_bomb_quadruple_cubes = 0 #done

		self.stats_cloak_acquired = 0 #done
		self.stats_frames_invisible = 0 #done
		self.stats_invisible_FIDs_inflicted = 0 #Done
		self.stats_invisible_FIDs_received = 0 #Done
		self.stats_invisible_item_deaths = 0 #Done
		self.stats_invisible_homing_bomb_evaded = 0 #Done

		self.stats_shield_acquired = 0 #Done
		self.stats_frames_with_shield_active = 0 #Done
		self.stats_shield_weapons_rebounded = 0 #Done

		self.stats_homing_bomb_acquired = 0 #Done
		self.stats_homing_bomb_activated = 0 #Done
		self.stats_homing_bomb_transferred = 0 #Done
		self.stats_homing_bomb_received = 0 #Done
		self.stats_homing_bomb_active_frames = 0 #Done
		self.stats_homing_bomb_kills = 0 #Done
		self.stats_homing_bomb_suicides = 0 #Done

		self.stats_gravity_acquired = 0 #Done
		self.stats_gravity_used = 0 #Done
		self.stats_frames_gravity_inverted = 0 #Done
		self.stats_frames_gravity_normal = 0 #Done
		self.stats_gravity_FIDs_inflicted = 0 #Done

		self.duels_participated = 0 #Done
		self.matches_participated = 0 #Done
		self.stats_duels_survived = 0 #Done
		self.stats_matches_won = 0 #Done
		self.stats_matches_lost = 0 #Done
		self.stats_solo_matches_won = 0 #Done
		self.stats_solo_matches_lost = 0 #Done
		self.stats_matches_1v2_won = 0 #Done
		self.stats_matches_1v2_lost = 0 #Done
		self.stats_matches_1v3_won = 0 #Done
		self.stats_matches_1v3_lost = 0 #Done
		self.stats_matches_2v2_won = 0 #Done
		self.stats_matches_2v2_lost = 0 #Done
		self.stats_matches_3v1_won = 0 #Done
		self.stats_matches_3v1_lost = 0 #Done
		self.stats_matches_2v1_won = 0 #Done
		self.stats_matches_2v1_lost = 0 #Done

		
		self.bandana = rope_physics.Bandana_Knot(self, self.color)


	def update(self):
		#For shield testing
		#self.shield_sprite.active = True
		#self.shield_sprite.shield_timer = 0

		self.dirty = 1

		if self.status != 'climb':
			self.rope = None
			self.pole = None

		self.collision_check_needed = True
		self.moving_platform = False #Flips to false each frame. Allows a single moving tile to impact ninja movement.

		if self.FID is False:
			self.apply_gravity()

		self.apply_item()


		#move x/y pending collision check.
		old_rectx = self.rect.x
		old_recty = self.rect.y
		#print(self.name)
		#print(self.true_x)
		#print(self.change_x)

		self.true_x += self.change_x
		self.true_y += self.change_y

		self.rect.x = round(self.true_x)
		self.rect.y = round(self.true_y)

		if self.status == 'idle' or self.status == 'duck': #here to try and fix moving platform jitters.
			self.true_x = self.rect.x
			self.true_y = self.rect.y

		if self.status != 'climb':
			self.rope = None

		if self.collision_timer > 0:
			self.collision_timer -= 1

		self.update_collision_rects()
		
		#self.current_quadrant = sprites.quadrant_handler.get_quadrant(self)

		if self.FID is False:
			if self.inverted_g is False:
				self.collision_check()
			else:
				self.inverted_collision_check()

		self.boundary_check()

		if self.FID is True: #Fell in the mallow
			self.splash_sprite.update()

		if self.portal_delay > 0:
			self.portal_delay -= 1

		if self.tile_particle_timer > 0:
			self.tile_particle_timer -= 1
		if self.knocked_particle_timer > 0:
			self.knocked_particle_timer -= 1

		self.check_squished('general')

		if self.climb_timer > 0:
			self.climb_timer -= 1

		if self.land_frame_counter > 0:
			self.land_frame_counter -= 1

		if self.visible_timer > 0:
			if self.visible_timer == 1:
				if self.visible_switch is True:
					self.visible = 1
					self.bandana.flip_visible('visible')
				elif self.visible_switch is False:
					self.visible = 0
					self.bandana.flip_visible('invisible')
			self.visible_timer -= 1

		if self.status == 'knocked':
			if self.knock_timer > 0:
				self.knock_timer -= 1
				if self.knock_timer == 0:
					self.status = 'falling'

		if self.last_collision != None:
			self.last_collision_timer -= 1
			if self.last_collision_timer <= 0:
				self.last_collision = None

		if (self.status == 'idle' or self.status == 'duck' or self.status == 'laser' or self.status == 'portal' or self.status == 'up_portal' or self.status == 'rocket'):
			if self.friction == 'icy':
				self.apply_friction('ice')
			else:
				self.apply_friction('normal')
		elif self.status == 'frozen':
			self.apply_friction('ice')

		if self.status == 'jump' or self.status == 'fall':
				self.apply_jump_friction()

		#Need to be after jumper_friction application.
		if self.status == 'roll':
				self.roll_timer -= 1
				if self.roll_timer <= 0:
					if self.status == 'roll':
						i = self.check_squished('land')
						if i is True:
							self.roll_timer += 1
						else:
							self.status = 'jump'

		if self.climb_lock > 0:
			self.climb_lock -= 1
		if self.climb_jump_timer > 0:
			self.climb_jump_timer -= 1

		if self.status == 'falling':
			self.fall_timer += 1

		if self.confused is True:
			self.confused_timer -= 1
			if self.confused_timer <= 0:
				self.confused_timer = 0
				self.confused = False
				if self.status == 'left':
					self.left_release()
				elif self.status == 'right':
					self.right_release()

		if self.on_fire is True:
			if self.on_fire_timer < 100:
				sprites.particle_generator.fire_burn_particles(self, 1, self.fire_x_speed)
			elif self.on_fire_timer < 200:
				sprites.particle_generator.fire_burn_particles(self, 3, self.fire_x_speed)
			else:
				sprites.particle_generator.fire_burn_particles(self, 6, self.fire_x_speed)
			self.on_fire_timer += 1
			if self.on_fire_timer > 300:
				self.on_fire = False
				self.activate_death_sprite('fire', self)


			self.fire_x_speed = self.change_x

	
		self.update_image(self.status, self.direction)

		self.score_inflicted_FIDs()

		self.collect_stats()

		self.online_update_counter += 1
		if self.item == 'shoes':
			self.online_update_counter += 1

		if abs(self.last_change_x - self.change_x) >= self.x_accel / 2:
			self.online_update_counter += 1

		#if abs(self.last_change_y - self.change_y) >= options.change_g:
		#	self.online_update_counter += 1

		self.last_change_x = self.change_x
		self.last_change_y = self.change_y	

		if self.online_update_counter >= 8:
			self.online_update_counter = 0
			self.online_update_trigger = True

		#if self.online_type == 'local':
		#	self.online_platform_key = None

	def collect_win_loss_stats(self, win_color):
		team_size = 1
		other_team_size = 0
		other_team_temp_list = []
		other_team_list = []
		for ninja in sprites.player_list:
			if ninja != self:
				if ninja.color == self.color:
					team_size += 1
				else:
					other_team_temp_list.append(ninja)

		for ninja in other_team_temp_list:
			if len(other_team_list) == 0:
				other_team_list.append(ninja)
			else:
				if ninja.color == other_team_list[0].color:
					other_team_list.append(ninja)
		other_team_size = len(other_team_list)

		if win_color == self.color:
			self.stats_matches_won += 1
			if team_size == 1:
				if other_team_size == 1:
					self.stats_solo_matches_won += 1
				elif other_team_size == 2:
					self.stats_matches_1v2_won += 1
				elif other_team_size == 3:
					self.stats_matches_1v3_won += 1
			elif team_size == 2:
				if other_team_size == 1:
					self.stats_matches_2v1_won += 1
				elif other_team_size == 2:
					self.stats_matches_2v2_won += 1
			elif team_size == 3:
				if other_team_size == 1:
					self.stats_matches_3v1_won += 1



		else:
			self.stats_matches_lost += 1
			if team_size == 1:
				if other_team_size == 1:
					self.stats_solo_matches_lost += 1
				elif other_team_size == 2:
					self.stats_matches_1v2_lost += 1
				elif other_team_size == 3:
					self.stats_matches_1v3_lost += 1
			elif team_size == 2:
				if other_team_size == 1:
					self.stats_matches_2v1_lost += 1
				elif other_team_size == 2:
					self.stats_matches_2v2_lost += 1
			elif team_size == 3:
				if other_team_size == 1:
					self.stats_matches_3v1_lost += 1

		#print('HEREEEEEE')
		#self.test_stats()

	def collect_stats(self):
		if options.game_state == 'level':
			self.stats_x_pixels_travelled += abs(self.change_x)
			self.stats_y_pixels_travelled += abs(self.change_y)

			if self.item == 'shoes':
				self.stats_shoes_pixels_travelled += abs(self.change_x)

			if self.visible == 0 and self.status != 'lose':
				self.stats_frames_invisible += 1

			if self.shield_sprite.active is True:
				self.stats_frames_with_shield_active += 1

			if self.inverted_g is False:
				self.stats_frames_gravity_normal += 1
			else:
				self.stats_frames_gravity_inverted += 1
			
			if self.status == 'roll':
				self.stats_frames_rolling += 1
			elif self.status == 'falling':
				self.stats_frames_falling +=1
			elif self.status in ('right', 'left'):	
				self.stats_frames_running +=1
			elif self.status == 'idle' and self.smug is False:	
				self.stats_frames_idle +=1
			elif self.status == 'idle' and self.smug is True:	
				self.stats_frames_smug +=1
			elif self.status == 'duck':	
				self.stats_frames_ducking +=1
			elif self.status == 'jump':
				self.stats_frames_jumping +=1


	def test_stats(self):
		print('PLAYER 1 STATS START HERE!')
		if self.name == 'player1':
			self.update_profile_stats()
			self.reset_stats()
			for key in data_manager.user_profiles[self.profile]['Stats']:
				if data_manager.user_profiles[self.profile]['Stats'][key] != 0:
					print(str(key) + ' ' + str(data_manager.user_profiles[self.profile]['Stats'][key]))



	def score_item_kills(self):
		self.stats_item_kills += 1
		VP_change = 0
		if options.versus_VP_per_weapon_kill == 'Ego Only':
			pass
		else:
			VP_change = int(options.versus_VP_per_weapon_kill)

		self.current_VP += VP_change 
		self.VP_earned += VP_change
		#Bring teammates along for the ride.
		for ninja in sprites.player_list:
			if ninja != self and ninja.color == self.color:
				ninja.current_VP = self.current_VP
	
	def get_rating(self):
		accuracy_list = []
		if self.stats_laser_acquired != 0:
			a = self.stats_laser_kills / self.stats_laser_acquired * 100
			accuracy_list.append(a)

		if self.stats_bomb_thrown != 0:
			b = self.stats_bomb_kills / self.stats_bomb_thrown * 100
			accuracy_list.append(b)

		if self.stats_mine_thrown != 0:	
			c = self.stats_mine_kills / self.stats_mine_thrown * 100
			accuracy_list.append(c)

		if self.stats_rocket_fired != 0:
			d = self.stats_rocket_kills / self.stats_rocket_fired * 100
			accuracy_list.append(d)

		if self.stats_volt_acquired != 0:
			e = self.stats_volt_kills / self.stats_volt_acquired * 100
			accuracy_list.append(e)

		if self.stats_homing_bomb_activated != 0:
			f = self.stats_homing_bomb_kills / self.stats_homing_bomb_activated * 100
			accuracy_list.append(f)

		accuracy = 0
		if len(accuracy_list) > 0:
			for item in accuracy_list:
				accuracy += item
			accuracy = accuracy / len(accuracy_list)


		if self.stats_ice_bomb_thrown != 0:
			g = self.stats_ice_bomb_cube_FIDs / self.stats_ice_bomb_thrown * 100
		else:
			g = 0

		h = self.stats_skull_acquired / self.duels_participated * 10

		i = self.stats_duels_survived / self.duels_participated * 10

		j = self.stats_FIDs_inflicted / self.duels_participated * 10

		k = self.stats_FIDs_received / self.duels_participated * 10

		l = self.stats_FIDs_suicide / self.duels_participated * 40

		m = self.stats_item_kills / self.duels_participated * 5

		o =  self.stats_item_deaths / self.duels_participated * 5

		
		rating = (accuracy + g - h + i + j - k - l + m - o) * 10

		return(int(rating))

	def score_inflicted_FIDs(self):
		if self.FID_inflicted != 0:
			if self.FID is False and self.status in ('idle','right','left','climb','duck', 'smug'):	
				VP_change = 0
				if options.versus_VP_per_FID_inflicted == 'Ego Only':
					pass
				else:
					VP_change = int(options.versus_VP_per_FID_inflicted) * self.FID_inflicted
					self.current_VP += VP_change
					self.VP_earned += VP_change
					for ninja in sprites.player_list:
						if ninja != self and ninja.color == self.color:
							ninja.current_VP = self.current_VP

				self.stats_FIDs_inflicted += self.FID_inflicted
				self.FID_inflicted = 0

	def item_stats_update(self, item):#called from level. Updates item aqcuired stats.
		if item == 'shoes':
			self.stats_shoes_acquired += 1
		elif item == 'laser':
			self.stats_laser_acquired += 1
		elif item == 'wings':
			self.stats_wings_acquired += 1
		elif item == 'skull':
			self.stats_skull_acquired += 1
		elif item == 'bomb':
			self.stats_bomb_acquired += 1
		elif item == 'volt':
			self.stats_volt_acquired += 1
		elif item == 'mine':
			self.stats_mine_acquired += 1
		elif item == 'rocket':
			self.stats_rocket_acquired += 1
		elif item == 'gravity':
			self.stats_gravity_acquired += 1
		elif item == 'portal gun':
			self.stats_portal_gun_acquired += 1
		elif item == 'ice bomb':
			self.stats_ice_bomb_acquired += 1
		elif item == 'cloak':
			self.stats_cloak_acquired += 1
		elif item == 'shield':
			self.stats_shield_acquired += 1
		elif item == 'homing bomb':
			self.stats_homing_bomb_acquired += 1


	def apply_jump_friction(self): #slows ninja gradually left to right
		if self.left_held is False and self.right_held is False:
			if self.collision_timer == 0:
				if self.change_x > self.x_accel:
					self.change_x -= self.x_accel
				elif self.change_x < -self.x_accel:
					self.change_x += self.x_accel
				else:
					self.change_x = 0

	def apply_friction(self, type):
		if type == 'ice':
			if self.item == 'shoes':
				temp_accel = self.icy_x_accel * 2
				if self.change_x > temp_accel:
					self.change_x -= temp_accel
				elif self.change_x < -temp_accel:
					self.change_x += temp_accel
				else:
					self.change_x = 0

			if self.change_x > self.icy_x_accel:
				self.change_x -= self.icy_x_accel
			elif self.change_x < -self.icy_x_accel:
				self.change_x += self.icy_x_accel
			else:
				self.change_x = 0

		elif type == 'normal':
			if self.item == 'shoes':
				temp_accel = self.x_accel * 2
				if self.change_x > temp_accel:
					self.change_x -= temp_accel
				elif self.change_x < -temp_accel:
					self.change_x += temp_accel
				else:
					self.change_x = 0
			else:
				if self.change_x > self.x_accel:
					self.change_x -= self.x_accel
				elif self.change_x < -self.x_accel:
					self.change_x += self.x_accel
				else:
					self.change_x = 0


	def stuck_check(self): #shifts ninja up or down so it doesn't 'appear' in middle of tile.
		self.update_collision_rects()

		if self.inverted_g is False:
			for tile in sprites.tile_list:
				if tile.type == 'tile' or tile.type == 'platform':
					if tile.rect.colliderect(self.rect_bottom):
						self.rect.bottom = tile.rect.top
						self.set_true_xy('y')
						break
					elif tile.rect.colliderect(self.rect_top):
						self.rect.top = tile.rect.bottom
						self.set_true_xy('y')
						break
		else:
			for tile in sprites.tile_list:
				if tile.type == 'tile' or tile.type == 'platform':
					if tile.rect.colliderect(self.rect_top):
						self.rect.bottom = tile.rect.top
						self.set_true_xy('y')
						break
					elif tile.rect.colliderect(self.rect_bottom):
						self.rect.top = tile.rect.bottom
						self.set_true_xy('y')
						break

		#self.set_true_xy()

	def build_ninja(self): #Used to build ninja images.
		#Make position dicts for 'head gear'
		if self.avatar == 'Robot':
			self.position_dict = {'run' : ((2,6), (2,6), (3,4), (3,3), (3,4), (2,6), (2,6), (3,4), (3,3), (3,4)),
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

		else:
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




		#create images for each position.
		#falling images
		
		#self.color = options.BLUE_LIST

		self.falling_right = []
		self.falling_left = []
		image = self.spritesheet.getImage(250, 0, 24, 48)
		self.falling_left.append(image)
		image = self.spritesheet.getImage(300, 0, 24, 48)
		self.falling_left.append(image)

		image = self.spritesheet.getImage(275, 0, 24, 48)
		self.falling_right.append(image)
		image = self.spritesheet.getImage(325, 0, 24, 48)
		self.falling_right.append(image)

		self.big_image_list.append(self.falling_left)
		self.big_image_list.append(self.falling_right)

		#otherimages
		self.other_images = []
		self.stock_image = self.spritesheet.getImage(350, 0, 14, 14)
		self.other_images.append(self.stock_image)

		self.big_image_list.append(self.other_images)


		#idle images
		self.idle_right = []
		self.idle_left = []

		image = self.spritesheet.getImage(0, 147, 24, 48)
		self.idle_right.append(image)
		image = self.spritesheet.getImage(75, 147, 24, 48)
		self.idle_left.append(image)

		image = self.spritesheet.getImage(25, 147, 24, 48)
		self.idle_right.append(image)
		image = self.spritesheet.getImage(100, 147, 24, 48)
		self.idle_left.append(image)

		image = self.spritesheet.getImage(50, 147, 24, 48)
		self.idle_right.append(image)
		image = self.spritesheet.getImage(125, 147, 24, 48)
		self.idle_left.append(image)

		image = self.spritesheet.getImage(25, 147, 24, 48)
		self.idle_right.append(image)
		image = self.spritesheet.getImage(100, 147, 24, 48)
		self.idle_left.append(image)

		self.big_image_list.append(self.idle_left)
		self.big_image_list.append(self.idle_right)

		self.idle_win = []
		image = self.spritesheet.getImage(100, 98, 24, 48)
		self.idle_win.append(image)
		image = self.spritesheet.getImage(125, 98, 24, 48)
		self.idle_win.append(image)
		image = self.spritesheet.getImage(150, 98, 24, 48)
		self.idle_win.append(image)
		image = self.spritesheet.getImage(125, 98, 24, 48)
		self.idle_win.append(image)

		self.big_image_list.append(self.idle_win)

		#duck images
		self.duck_neutral = []
		image = self.spritesheet.getImage(0, 196, 24, 24)
		self.duck_neutral.append(image)

		image = self.spritesheet.getImage(25, 196, 24, 24)
		self.duck_neutral.append(image)

		self.big_image_list.append(self.duck_neutral)

		#Fid Image:
		self.fid_image_list = []
		image = self.spritesheet.getImage(175,98,24,48)
		self.fid_image_list.append(image)

		self.big_image_list.append(self.fid_image_list)

		#running images
		self.run_right = []
		self.run_left = []

		image = self.spritesheet.getImage(0,0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(0,49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(25, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(25, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(50, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(50, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(75, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(75, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(100, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(100, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(125,0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(125,49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(150, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(150, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(175, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(175, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(200, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(200, 49, 24, 48)
		self.run_left.append(image)

		image = self.spritesheet.getImage(225, 0, 24, 48)
		self.run_right.append(image)
		image = self.spritesheet.getImage(225, 49, 24, 48)
		self.run_left.append(image)

		self.big_image_list.append(self.run_left)
		self.big_image_list.append(self.run_right)


		#changing direction images
		self.slide_images = []
		
		self.slide_right_image = self.spritesheet.getImage(175,147, 24, 48)
		self.slide_images.append(self.slide_right_image)
		self.slide_left_image = self.spritesheet.getImage(150,147, 24, 48)
		self.slide_images.append(self.slide_left_image)

		self.big_image_list.append(self.slide_images)

		#jumping images
		self.jump_right = []
		self.jump_left = []

		image = self.spritesheet.getImage(0, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(200, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(25, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(225, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(50, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(250, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(75, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(275, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(100, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(300, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(125, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(325, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(150, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(350, 221, 24, 24)
		self.jump_left.append(image)

		image = self.spritesheet.getImage(175, 221, 24, 24)
		self.jump_right.append(image)
		image = self.spritesheet.getImage(375, 221, 24, 24)
		self.jump_left.append(image)



		self.big_image_list.append(self.jump_left)
		self.big_image_list.append(self.jump_right)

		self.cling_list = []
		self.cling_sprite_left = self.spritesheet.getImage(379,147,24,48)
		self.cling_list.append(self.cling_sprite_left)
		self.cling_sprite_right = self.spritesheet.getImage(404,147,24,48)
		self.cling_list.append(self.cling_sprite_right)

		self.big_image_list.append(self.cling_list)

		#Knocked Back Sprites
		self.knockback_right = []
		self.knockback_left = []

		image = self.spritesheet.getImage(0,98, 24, 48)
		self.knockback_left.append(image)
		image = self.spritesheet.getImage(50,98, 24, 48)
		self.knockback_right.append(image)

		self.big_image_list.append(self.knockback_left)
		self.big_image_list.append(self.knockback_right)

		#Knocked Back Sprites
		self.knockforward_right = []
		self.knockforward_left = []

		image = self.spritesheet.getImage(25,98, 24, 48)
		self.knockforward_right.append(image)
		image = self.spritesheet.getImage(75,98, 24, 48)
		self.knockforward_left.append(image)

		self.big_image_list.append(self.knockforward_left)
		self.big_image_list.append(self.knockforward_right)

		#Climbing Sprites
		self.climbing_sprite = []

		image = self.spritesheet.getImage(0, 246, 24, 48)
		self.climbing_sprite.append(image)

		image = self.spritesheet.getImage(25, 246, 24, 48)
		self.climbing_sprite.append(image)

		image = self.spritesheet.getImage(50, 246, 24, 48)
		self.climbing_sprite.append(image)

		image = self.spritesheet.getImage(25, 246, 24, 48)
		self.climbing_sprite.append(image)

		self.big_image_list.append(self.climbing_sprite)

		#portal sprites
		self.portal_right_sprite = []
		self.portal_left_sprite = []
		self.portal_up_sprite = []

		#image = sprites.ninja_sheet.getImage(0, 344, 24, 48)
		#self.portal_right_sprite.append(image)
		image = self.spritesheet.getImage(25, 344, 24, 48)
		self.portal_right_sprite.append(image)
		image = self.spritesheet.getImage(50, 344, 24, 48)
		self.portal_right_sprite.append(image)
		image = self.spritesheet.getImage(75, 344, 24, 48)
		self.portal_right_sprite.append(image)
		image = self.spritesheet.getImage(50, 344, 24, 48)
		self.portal_right_sprite.append(image)
		image = self.spritesheet.getImage(25, 344, 24, 48)
		self.portal_right_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(0, 344, 24, 48)
		#self.portal_right_sprite.append(image)

		#image = sprites.ninja_sheet.getImage(100, 344, 24, 48)
		#self.portal_left_sprite.append(image)
		image = self.spritesheet.getImage(125, 344, 24, 48)
		self.portal_left_sprite.append(image)
		image = self.spritesheet.getImage(150, 344, 24, 48)
		self.portal_left_sprite.append(image)
		image = self.spritesheet.getImage(175, 344, 24, 48)
		self.portal_left_sprite.append(image)
		image = self.spritesheet.getImage(150, 344, 24, 48)
		self.portal_left_sprite.append(image)
		image = self.spritesheet.getImage(125, 344, 24, 48)
		self.portal_left_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(100, 344, 24, 48)
		#self.portal_left_sprite.append(image)


		#Take out last image!
		image = self.spritesheet.getImage(312, 344, 24, 48)
		self.portal_up_sprite.append(image)
		image = self.spritesheet.getImage(337, 344, 24, 48)
		self.portal_up_sprite.append(image)
		image = self.spritesheet.getImage(362, 344, 24, 48)
		self.portal_up_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(387, 344, 24, 48)
		#self.portal_up_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(387, 344, 24, 48)
		#self.portal_up_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(362, 344, 24, 48)
		#self.portal_up_sprite.append(image)
		image = self.spritesheet.getImage(337, 344, 24, 48)
		self.portal_up_sprite.append(image)
		image = self.spritesheet.getImage(312, 344, 24, 48)
		self.portal_up_sprite.append(image)

		self.big_image_list.append(self.portal_right_sprite)
		self.big_image_list.append(self.portal_left_sprite)
		self.big_image_list.append(self.portal_up_sprite)



		self.laser_right_sprite = []
		self.laser_left_sprite = []
		#TOOK OUT FIRST FRAME
		#image = sprites.ninja_sheet.getImage(75, 246, 24, 48)
		#self.laser_right_sprite.append(image)
		image = self.spritesheet.getImage(100, 246, 24, 48)
		self.laser_right_sprite.append(image)
		image = self.spritesheet.getImage(125, 246, 24, 48)
		self.laser_right_sprite.append(image)
		image = self.spritesheet.getImage(150, 246, 24, 48)
		self.laser_right_sprite.append(image)
		image = self.spritesheet.getImage(150, 246, 24, 48)
		self.laser_right_sprite.append(image)
		image = self.spritesheet.getImage(125, 246, 24, 48)
		self.laser_right_sprite.append(image)
		image = self.spritesheet.getImage(100, 246, 24, 48)
		self.laser_right_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(75, 246, 24, 48)
		#self.laser_right_sprite.append(image)

		#image = sprites.ninja_sheet.getImage(175, 246, 24, 48)
		#self.laser_left_sprite.append(image)
		image = self.spritesheet.getImage(200, 246, 24, 48)
		self.laser_left_sprite.append(image)
		image = self.spritesheet.getImage(225, 246, 24, 48)
		self.laser_left_sprite.append(image)
		image = self.spritesheet.getImage(250, 246, 24, 48)
		self.laser_left_sprite.append(image)
		image = self.spritesheet.getImage(250, 246, 24, 48)
		self.laser_left_sprite.append(image)
		image = self.spritesheet.getImage(225, 246, 24, 48)
		self.laser_left_sprite.append(image)
		image = self.spritesheet.getImage(200, 246, 24, 48)
		self.laser_left_sprite.append(image)
		#image = sprites.ninja_sheet.getImage(175, 246, 24, 48)
		#self.laser_left_sprite.append(image)

		self.big_image_list.append(self.laser_right_sprite)
		self.big_image_list.append(self.laser_left_sprite)


		self.rocket_sprite_list = []

		image = self.spritesheet.getImage(304, 147, 24, 48)
		self.rocket_sprite_list.append(image)
		image = self.spritesheet.getImage(329, 147, 24, 48)
		self.rocket_sprite_list.append(image)
		image = self.spritesheet.getImage(354, 147, 24, 48)
		self.rocket_sprite_list.append(image)
		image = self.spritesheet.getImage(329, 147, 24, 48)
		self.rocket_sprite_list.append(image)


		self.big_image_list.append(self.rocket_sprite_list)

		#update death sprite images
		self.death_sprite.kill()
		self.death_sprite = DeathSprite(self)

		#now fix color (shouldn't start blue. Need to use to changes to bring items with us)
		
		i = options.color_choices.index(self.color) #make i current color
		#change ninja to Blue, mostly to bring items along
		self.change_color('left', 2)
		#change color to prior color
		self.change_color('left', i)



	def check_squished(self, squished_type):
		if squished_type == 'wall_collision':
			left_rect = pygame.Rect(self.rect.x - 2,self.rect.y + 2,2,self.rect.height - 4)
			right_rect = pygame.Rect(self.rect.right,self.rect.y + 2,2,self.rect.height - 4)

			left_collision = False
			right_collision = False
			for tile in sprites.tile_list:
				if tile.type == 'tile' or tile.type == 'mallow_wall':
					if left_collision is False:
						if tile.rect.colliderect(left_rect):
							left_collision = True
					if right_collision is False:
						if tile.rect.colliderect(right_rect):
							right_collision = True
				if left_collision is True and right_collision is True:
					break
			if left_collision is True and right_collision is True:
				i = True
			else:
				i = False

			return(i)


		if squished_type == 'land':
			if self.inverted_g is False:
				check_rect = pygame.Rect(self.rect.x + 2, self.rect.top - 4, self.rect.width - 4, 4)
			else:
				check_rect = pygame.Rect(self.rect.x + 2, self.rect.bottom, self.rect.width - 4, 4)

			i = False
			for tile in sprites.tile_list:
				if tile.type == 'tile':
					if check_rect.colliderect(tile.rect):
						i = True
						if self.status in ('duck', 'jump'):
							if self.friction != 'icy':
								if self.rect.centerx < tile.rect.left:
									if tile.left_open is True:
										self.rect.right = tile.rect.left
										self.set_true_xy('x')
										self.change_x = 0
										i = False
								elif self.rect.centerx > tile.rect.right:
									if tile.right_open is True:
										self.rect.left = tile.rect.right
										self.set_true_xy('x')
										self.change_x = 0
										i = False

						break

			return i

		elif squished_type == 'trip collision':
			#check just above and just ;below ninja. If Tiles are in both spots, return True to modify collision mechanics.
			if self.inverted_g is False:
				check_rect_top = pygame.Rect(self.rect.x + 4, self.rect.top - 20, self.rect.width - 8,20)
				check_rect_bottom = pygame.Rect(self.rect.x + 4, self.rect.bottom, self.rect.width - 8, 4)
			else:
				check_rect_top = pygame.Rect(self.rect.x + 4, self.rect.top - 4, self.rect.width - 8, 4)
				check_rect_bottom = pygame.Rect(self.rect.x + 4, self.rect.bottom, self.rect.width - 8, 20)
			top_squished = False
			bottom_squished = False

			for tile in sprites.tile_list:
				if tile.type == 'tile':
					if top_squished is False:
						if check_rect_top.colliderect(tile.rect):
							top_squished = True
							self.tight_trip_top_tile = tile
					if bottom_squished is False:
						if check_rect_bottom.colliderect(tile.rect):
							bottom_squished = True
							self.tight_trip_bottom_tile = tile

			if top_squished is True and bottom_squished is True:
				i = True
			else:
				i = False				

			return i
		
		elif squished_type == 'moving_platform':
			if self.inverted_g is False:
				check_rect = pygame.Rect(self.rect.x + 2, self.rect.top - 5, self.rect.width - 4,5)
			else:
				check_rect = pygame.Rect(self.rect.x + 2, self.rect.bottom, self.rect.width - 4,5)

			i = False
			for tile in sprites.tile_list:
				if tile.type == 'tile':
					if check_rect.colliderect(tile.rect):
						i = True
						break

			return(i)
		
		elif squished_type == 'collision':
			#check just above and just ;below ninja. If Tiles are in both spots, return True to modify collision mechanics.
			if self.inverted_g is False:
				check_rect_top = pygame.Rect(self.rect.x + 4, self.rect.top - 5, self.rect.width - 8,5)
				check_rect_bottom = pygame.Rect(self.rect.x + 4, self.rect.bottom, self.rect.width - 8, 4)
			else:
				check_rect_top = pygame.Rect(self.rect.x + 4, self.rect.top - 4, self.rect.width - 8, 4)
				check_rect_bottom = pygame.Rect(self.rect.x + 4, self.rect.bottom, self.rect.width - 8, 5)
			top_squished = False
			bottom_squished = False

			for tile in sprites.tile_list:
				if tile.type == 'tile':
					if top_squished is False:
						if check_rect_top.colliderect(tile.rect):
							top_squished = True
							self.tight_top_tile = tile
					if bottom_squished is False:
						if check_rect_bottom.colliderect(tile.rect):
							bottom_squished = True
							self.tight_bottom_tile = tile

			if top_squished is True and bottom_squished is True:
				i = True
			else:
				i = False				

			return i
		
		elif squished_type == 'general':
			if self.status == 'duck':
				if self.hold_duck is False:
					if self.inverted_g is False:
						self.down_release()
					else:
						self.up_release()

			if self.inverted_g is False:
				check_rect_top = pygame.Rect(self.rect.x + 4, self.rect.top, self.rect.width - 8, 4)
				check_rect_bottom = pygame.Rect(self.rect.x + 4, self.rect.bottom - 4, self.rect.width - 8, 5)
				top_tile = None
				bottom_tile = None

				for tile in sprites.tile_list:
					if tile.type == 'tile':
						if tile.rect.colliderect(check_rect_top):
							top_tile = tile
							break

				for tile in sprites.tile_list:
					if tile.type == 'tile' or tile.type == 'platform':
						if tile.rect.colliderect(check_rect_bottom):
							bottom_tile = tile
							break

				if top_tile != None and bottom_tile != None: #squished
					if self.rect.height == 24: #already ducking!
						if bottom_tile.type == 'platform':
							self.rect.top = top_tile.rect.bottom
							self.set_true_xy('y')
						else:
							self.rect.bottom = bottom_tile.rect.top
							self.shield_sprite.active = False
							self.activate_death_sprite('squished', None)
							self.set_true_xy('y')
					elif self.rect.height == 48: #full size
						old_centerx = self.rect.centerx
						old_bottom = self.rect.bottom
						self.status = 'duck'
						self.image_number = 0
						self.image = self.duck_neutral[0]
						self.bandana_info = ('duck', self.direction, self.image_number)
						self.frame_counter = 0
						self.image_number = 0
						self.rect = self.image.get_rect()
						self.rect.centerx = old_centerx
						self.rect.bottom = bottom_tile.rect.top
						self.set_true_xy('xy')

			
			if self.inverted_g is True:
				check_rect_bottom = pygame.Rect(self.rect.x + 4, self.rect.top - 1, self.rect.width - 8, 4)
				check_rect_top = pygame.Rect(self.rect.x + 4, self.rect.bottom - 4, self.rect.width - 8, 4)
				top_tile = None
				bottom_tile = None

				for tile in sprites.tile_list:
					if tile.type == 'tile':
						if tile.rect.colliderect(check_rect_top):
							top_tile = tile
							break

				for tile in sprites.tile_list:
					if tile.type == 'tile' or tile.type == 'platform':
						if tile.rect.colliderect(check_rect_bottom):
							bottom_tile = tile
							break

				if top_tile != None and bottom_tile != None: #squished
					if self.rect.height == 24: #already ducking!
						if bottom_tile.type == 'platform':
							self.rect.bottom = top_tile.rect.top
							self.set_true_xy('y')
						else:
							self.rect.top = bottom_tile.rect.bottom
							self.shield_sprite.active = False
							self.activate_death_sprite('squished', self)
							self.set_true_xy('y')
					elif self.rect.height == 48: #full size
						old_centerx = self.rect.centerx
						old_top = self.rect.top
						self.status = 'duck'
						self.image_number = 0
						self.image = self.duck_neutral[0]
						self.bandana_info = ('duck', self.direction, self.image_number)
						self.frame_counter = 0
						self.image_number = 0
						self.rect = self.image.get_rect()
						self.rect.centerx = old_centerx
						self.rect.top = bottom_tile.rect.bottom
						self.set_true_xy('xy')

			'''
			if top_tile  == None or bottom_tile == None:
				if self.status == 'duck':
					if self.down_held is False:
						if self.inverted_g is False:
							self.down_release()
						else:
							self.up_release()
			'''



	def place_ninja(self,center,phase_in=False, inverted_g = False, moving_platform = None):
		

		if phase_in is True: #activate spawn_sprite. It will activate ninja.
			#MOVED TO spawn_sprite
			#self.visible = 0
			#self.visible_timer = 10
			#self.visible_switch = True
			#self.bandana.flip_visible('invisible')

			if inverted_g is False:
				base_y = center[1] + 24
			else:
				base_y = center[1] - 24


			#if self.center[0] > 320:
			#	self.direction == 'left'
			#else:
			#	self.direction == 'right'

			self.spawn_sprite.activate(inverted_g, (center[0], base_y), center, moving_platform)

		else:
			old_loop = self.loop_physics
		
			self.reset(full_reset = False) #Not resetting items.
			self.rect.centerx = center[0]
			self.rect.centery = center[1]
		
			self.update_collision_rects()
			self.loop_physics = old_loop

			self.set_true_xy('xy')

			if self.rect.centerx > 320:
				self.direction = 'left'
			else:
				self.direction = 'right'

			self.inverted_g = self.spawn_sprite.inverted_g


			self.bandana.kill()
			if self.bandana_color == None:
				self.bandana = rope_physics.Bandana_Knot(self, self.color)
				self.bandana.update()
				self.bandana.headband.update()
			else:
				self.bandana = rope_physics.Bandana_Knot(self, self.bandana_color)
				self.bandana.update()
				self.bandana.headband.update()

			#self.bandana.new_position()

	def shrink(self, situation):
		self.image_number = 0
		self.frame_number = 0
		if situation == 'knocked':
			self.status = 'roll'
			self.roll_timer = 7
			old_centerx = self.rect.centerx
			old_top = self.rect.top
			old_bottom = self.rect.bottom
			
			if self.inverted_g is False:
				if self.direction == 'left':
					self.image = self.jump_left[self.image_number]
				elif self.direction == 'right':
					self.image = self.jump_right[self.image_number]
			else:
				if self.direction == 'left':
					i = self.jump_left[self.image_number]
				elif self.direction == 'right':
					i = self.jump_right[self.image_number]
				self.image = pygame.transform.flip(i,False,True)

			self.rect = self.image.get_rect()
			self.rect.centerx = old_centerx
			if self.inverted_g is False:
				self.rect.bottom = old_bottom
			else:
				self.rect.top = old_top
			self.bandana_info = ('jump', self.direction, self.image_number)

			self.set_true_xy('xy')

		elif situation in ('online_freeze', 'online'):
			self.status = 'duck'
			old_centerx = self.rect.centerx
			old_top = self.rect.top
			old_bottom = self.rect.bottom

			self.frame_number = 0
			self.image_number = 1

			self.image = self.duck_neutral[self.image_number]
			self.bandana_info = ('duck', self.direction, self.image_number)

			self.rect = self.image.get_rect()
			self.rect.centerx = old_centerx
			if self.inverted_g is False:
				self.rect.bottom = old_bottom
			else:
				self.rect.top = old_top
			self.set_true_xy('xy')

	def grow(self, situation):
		self.image_number = 0
		self.frame_number = 0
		if situation == 'normal':
			old_centerx = self.rect.centerx
			old_top = self.rect.top
			old_bottom = self.rect.bottom

			self.image = pygame.Surface((24,48))
			self.rect = self.image.get_rect()
			self.rect.centerx = old_centerx
			if self.inverted_g is False:
				self.rect.bottom = old_bottom
			else:
				self.rect.top = old_top
			self.bandana_info = ('idle', self.direction, self.image_number)
			self.set_true_xy('xy')

		if situation in ('online_freeze', 'online'):
			self.frame_counter = 0
			self.image_number = 0

			old_centerx = self.rect.centerx
			old_top = self.rect.top
			old_bottom = self.rect.bottom

			self.image = pygame.Surface((24,48))
			self.rect = self.image.get_rect()
			self.rect.centerx = old_centerx

			self.status = 'idle'
			if self.direction == 'right':
				self.image = self.idle_right[self.image_number]
				self.bandana_info = ('idle', self.direction, self.image_number)
			elif self.direction == 'left':
				self.image = self.idle_left[self.image_number]
				self.bandana_info = ('idle', self.direction, self.image_number)

			if self.inverted_g is False:
				self.rect.bottom = old_bottom
			else:
				self.rect.top = old_top

			self.set_true_xy('xy')
				

	def update_collision_rects(self):
		if self.inverted_g is False:
			#create extra personal rects for collision purposes. Updated regularly.
			self.collision_rect = pygame.Rect(self.rect.left + 2, self.rect.top + 2, self.rect.width - 4, self.rect.height - 4)
			self.rect_top = pygame.Rect(self.rect.left + 3, self.rect.top, self.rect.width - 6, 8)
			self.rect_bottom = pygame.Rect(self.rect.left + 3, self.rect.bottom - 6, self.rect.width - 6, 6)
			self.rect_left = pygame.Rect(self.rect.left, self.rect.top + 2, 5, self.rect.height - 4)
			self.rect_right = pygame.Rect(self.rect.right - 5, self.rect.top + 2, 5, self.rect.height - 4)
			#self.rect_top_right = None
			#self.rect_top_left = None
			#self.rect_bottom_right = None
			#self.rect_bottom_left = None
			x_width = round(self.rect.width / 3)
			y_width = round(self.rect.height / 3)
			self.rect_top_middle = pygame.Rect(self.rect.left + (x_width), self.rect.top + 2, x_width, 5)
			self.rect_bottom_middle = pygame.Rect(self.rect.left + (x_width), self.rect.bottom - 7, x_width, 5)
			self.rect_left_middle = pygame.Rect(self.rect.left, self.rect.top + y_width, 5, y_width)
			self.rect_right_middle = pygame.Rect(self.rect.right - 5, self.rect.top + y_width, 5, y_width)
		else:
			#create extra personal rects for collision purposes. Updated regularly.
			self.collision_rect = pygame.Rect(self.rect.left + 2, self.rect.top + 2, self.rect.width - 4, self.rect.height - 4)
			self.rect_bottom = pygame.Rect(self.rect.left + 3, self.rect.top, self.rect.width - 6, 6)
			self.rect_top = pygame.Rect(self.rect.left + 3, self.rect.bottom - 8, self.rect.width - 6, 8)
			self.rect_left = pygame.Rect(self.rect.left, self.rect.top + 2, 5, self.rect.height - 4)
			self.rect_right = pygame.Rect(self.rect.right - 5, self.rect.top + 2, 5, self.rect.height - 4)
			#self.rect_top_right = None
			#self.rect_top_left = None
			#self.rect_bottom_right = None
			#self.rect_bottom_left = None
			x_width = round(self.rect.width / 3)
			y_width = round(self.rect.height / 3)
			self.rect_bottom_middle = pygame.Rect(self.rect.left + (x_width), self.rect.top + 2, x_width, 5)
			self.rect_top_middle = pygame.Rect(self.rect.left + (x_width), self.rect.bottom - 7, x_width, 5)
			self.rect_left_middle = pygame.Rect(self.rect.left, self.rect.top + y_width, 5, y_width)
			self.rect_right_middle = pygame.Rect(self.rect.right - 5, self.rect.top + y_width, 5, y_width)
	def apply_item(self):
		if self.item == 'shoes':
			self.x_speed_max = 3.5
			self.climb_speed = 2.5
		elif self.item == 'metal suit':
			self.x_speed_max = 1.5
			self.climb_speed = 1.5
		else:
			self.x_speed_max = 2
			self.climb_speed = 2

		if self.item == 'volt':
			self.volt_sprite.active = True

	def set_fire(self):
		if self.on_fire is False:
			if self.shield_sprite.active is False:
				if self.ice_cube.active is True:
					self.ice_cube.cube_timer = 1
					self.ice_cube.update()
				self.on_fire = True
				self.on_fire_timer = 0


	def wipeout(self): #kills all offshoots of sprite
		self.death_sprite.kill()
		self.splash_sprite.kill()
		self.item_effect1.kill()
		self.item_effect2.kill()
		self.item_effect3.kill()

		self.feather_effect1.kill()
		self.feather_effect2.kill()
		self.feather_effect3.kill()
		self.feather_effect4.kill()
		self.feather_effect5.kill()
		self.feather_effect6.kill()

		self.name_bar.kill()
		self.choice_bar.kill()
		self.score_bar.kill()
		self.stock_bar.kill()
		self.controls_sprite.kill()
		self.text_sprite.kill()

		self.awards_screen_sprite.kill()

		self.projectile1.kill()
		self.projectile2.kill()
		self.projectile3.kill()
		self.projectile4.kill()
		self.projectile5.kill()
		self.projectile6.kill()

		self.rocket.kill()


		self.mine1.kill()
		self.mine2.kill()
		self.mine3.kill()
		self.mine4.kill()
		self.mine5.kill()
		self.mine6.kill()

		self.bomb_sprite.kill()

		self.ice_bomb_sprite.kill()

		self.volt_sprite.kill()


		self.shield_sprite.kill()

	def reset(self, full_reset = True):
		self.rope = None
		self.online_platform_key = None
		self.respawn_timer = 0
		self.on_fire = False
		self.on_fire_timer = 0

		self.mallow = None #holds mallow of FID
		self.climb_speed = 2
		self.metal_pound_timer = 0
		self.tight_space = False #true if tile space is 48 or smaller
		self.confused = False
		self.confused_timer = 600

		self.text_number = 0
		self.text_case = 'uppercase'
		self.profile_text = '' #used to write in new profiles
		self.visible_timer = 0
		self.visible_switch = True
		#self.visible = 1
		self.land_frame = False
		self.land_frame_counter = 0
		self.smug = False
		self.friction = 'normal'
		self.image = pygame.Surface((24,48))
		self.rect = self.image.get_rect()
		self.FID = False
		self.change_x = 0
		self.change_y = 0
		self.status = 'idle'
		self.direction = 'right'
		self.win = False
		#self.menu_status = "join" #Now handled in menu
		self.item = 'none'
		self.double_jump = False
		self.projectile_count = 0
		self.loop_physics = False
		self.visible = 1
		self.roll_timer = 0
		self.jump_held = False
		self.revert_g()
		self.item_counter = 0
		self.moving_platform = False
		self.hold_duck = False #allows duck to be held when landing.
		self.wind_speed = 0

		self.online_player_select_timer = 0
		

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 1)
		sprites.ninja_list.add(self)


		#used for STAT tracking
		self.FID_inflictor = None #holds the last person to hit you. Resets when landing.
		self.FID_inflicted = 0 #True if you just inflicted a FID. If bigger than 0, awards points once you've landed...

		self.update_image(self.status,self.direction)

		self.death_sprite.reset()

		if full_reset is True:
			self.name_bar.update_name()
			self.choice_bar.update_name()
			self.score_bar.reset()
			self.stock_bar.reset()
			self.spawn_sprite.reset()

			self.splash_sprite.reset()
			self.item_effect1.reset()
			self.item_effect2.reset()
			self.item_effect3.reset()
			self.projectile1.reset()
			self.projectile2.reset()
			self.projectile3.reset()
			self.projectile4.reset()
			self.projectile5.reset()
			self.projectile6.reset()
			self.mine1.reset()
			self.mine2.reset()
			self.mine3.reset()
			self.mine4.reset()
			self.mine5.reset()
			self.mine6.reset()
			self.feather_effect1.reset()
			self.feather_effect2.reset()
			self.feather_effect3.reset()
			self.feather_effect4.reset()
			self.feather_effect5.reset()
			self.feather_effect6.reset()
			self.bomb_sprite.reset()
			self.ice_bomb_sprite.reset()
			self.volt_sprite.reset()
			self.shield_sprite.reset()
			self.rocket.reset()
			self.ice_cube.reset()


	def update_image(self, status, direction):

		if self.status == 'frozen':
			self.image = self.frozen_image
			#self.bandana_info = ('frozen', self.direction, self.image_number)

		elif self.FID is True:
			self.change_x = 0
			self.status = 'idle' #prevents wall-cling from preventing ninja from falling.
			old_rect_top = self.rect.top
			old_centerx = self.rect.centerx
			
			self.image = self.fid_image_list[0].copy()
			self.bandana_info = ('FID', self.direction, 0)

			self.rect = self.image.get_rect()
			'''
			if self.direction == 'right':
				self.image = self.knockforward_right[0]
				self.rect = self.image.get_rect()
			else:
				self.image = self.knockforward_left[0]
				self.rect = self.image.get_rect()
			'''
			self.rect.centerx = old_centerx
			self.rect.top = old_rect_top

			if self.mallow.inverted is False:
				if self.rect.bottom > self.mallow.rect.bottom:
					i = abs(self.rect.bottom - self.mallow.rect.bottom)
					if self.inverted_g is False:
						pygame.draw.rect(self.image, options.GREEN,(0, self.rect.height - i,self.rect.width,i),0)
					else:
						pygame.draw.rect(self.image, options.GREEN,(0, 0,self.rect.width,i),0)
				if self.rect.top > self.mallow.rect.top + 20:
					self.bandana.kill() #stop it from hitting the ground weird.
			else:
				if self.rect.top < self.mallow.rect.top:
					i = abs(self.rect.top - self.mallow.rect.top)
					if self.inverted_g is False:
						pygame.draw.rect(self.image, options.GREEN,(0, 0,self.rect.width,i),0)
					else:
						pygame.draw.rect(self.image, options.GREEN,(0, self.rect.height - i,self.rect.width,i),0)
				if self.rect.bottom < self.mallow.rect.bottom - 20:
					self.bandana.kill() #stop it from hitting the ground weird.

			#The following makes sure bandanas don't stick around in some situations
			if self.bandana.rect.top > self.mallow.rect.top and self.bandana.rect.bottom < self.mallow.rect.bottom:
				self.bandana.kill()

		elif self.status == 'laser' or self.status == 'fall_laser':
			if self.frame_counter >= 2:
				self.image_number += 1
				self.frame_counter = 0
				if self.image_number == 3:
					self.projectile1.attempt_fire()
					self.projectile_count += 1
					if self.projectile_count == 3:
						self.item = 'none'

			if self.image_number >= len(self.laser_right_sprite):
				self.frame_counter = 0
				self.image_number = 0
				self.status = 'idle'

			if self.direction == 'right':
				self.image = self.laser_right_sprite[self.image_number]
			elif self.direction == 'left':
				self.image = self.laser_left_sprite[self.image_number]
			self.bandana_info = ('laser', self.direction, 0)

		elif self.status == 'up_portal' or self.status == 'fall_up_portal':
			if self.frame_counter >= 6:
				self.image_number += 1
				self.frame_counter = 0
				if self.image_number == 3:
					pass
					#self.portal_gun.attempt_fire()

			if self.image_number >= len(self.portal_up_sprite):
				self.frame_counter = 0
				self.image_number = 0
				self.status = 'idle'

			self.image = self.portal_up_sprite[self.image_number]
			self.bandana_info = ('portal up', self.direction, self.image_number)

		elif self.status == 'portal' or self.status == 'fall_portal':
			if self.frame_counter >= 4:
				self.image_number += 1
				self.frame_counter = 0
				if self.image_number == 3:
					pass
					#self.portal_gun.attempt_fire()
					if self.direction == 'right':
						if self.change_x >= 0:
							self.change_x -= 4
						elif self.change_x >= -4:
							self.change_x = -4
					elif self.direction == 'left':
						if self.change_x <= 0:
							self.change_x += 4
						elif self.change_x <= 4:
							self.change_x = 4
				if self.status == 'portal':
					if self.image_number >= 3:
						if self.inverted_g is False:
							if self.direction == 'left':
								sprites.particle_generator.slide_particles(self.rect.bottomright, 'right', self.inverted_g)
							elif self.direction == 'right':
								sprites.particle_generator.slide_particles(self.rect.bottomleft, 'left', self.inverted_g)
						else:
							if self.direction == 'left':
								sprites.particle_generator.slide_particles(self.rect.topright, 'right', self.inverted_g)
							elif self.direction == 'right':
								sprites.particle_generator.slide_particles(self.rect.topleft, 'left', self.inverted_g)

			if self.image_number >= len(self.portal_right_sprite):
				self.frame_counter = 0
				self.image_number = 0
				self.status = 'idle'

			if self.direction == 'right':
				self.image = self.portal_right_sprite[self.image_number]
				self.bandana_info = ('portal', self.direction, 0)
				
			elif self.direction == 'left':
				self.image = self.portal_left_sprite[self.image_number]
				self.bandana_info = ('portal', self.direction, 0)

			

		elif self.status == 'rocket':
			if self.frame_counter >= 8:
				self.frame_counter = 0
				self.image_number += 1

			if self.image_number > len(self.rocket_sprite_list) - 1:
				self.image_number = len(self.rocket_sprite_list) - 1
			
			if self.image_number == 3 and self.rocket.status == '':
				self.rocket.fire_rocket()
				


			self.image = self.rocket_sprite_list[self.image_number]
			self.bandana_info = ('rocket', self.direction, self.image_number)


		elif self.status == 'idle':
			if self.land_frame is True:
				self.frame_counter = 0
				if self.land_frame_counter == 0:
					self.land_frame = False
				if self.direction == 'right':
					self.image = self.falling_right[1]
				elif self.direction == 'left':
					self.image = self.falling_left[1]
				self.bandana_info = ('falling', self.direction, 1)
			else:
				if self.frame_counter >= 14:
					self.image_number += 1
					self.frame_counter = 0
				if self.image_number >= len(self.idle_right):
					self.frame_counter = 0
					self.image_number = 0
				
				if self.smug is True: #won!
					self.image = self.idle_win[self.image_number]
					self.bandana_info = ('smug', 'right', self.image_number) #always right, are actually, no true direction.
				elif direction == 'right':
					self.image = self.idle_right[self.image_number]
					self.bandana_info = ('idle', self.direction, self.image_number)
				elif direction == 'left':
					self.image = self.idle_left[self.image_number]
					self.bandana_info = ('idle', self.direction, self.image_number)

		elif self.status == 'duck':
			if self.image_number > 1:
				self.image_number = 1
				
			self.image = self.duck_neutral[self.image_number]
			if self.frame_counter  >= 4:
				self.image_number = 1
			self.bandana_info = ('duck', self.direction, self.image_number)

		elif self.status == 'metal pound':
			self.image = self.duck_neutral[1]
			self.bandana_info = ('duck', self.direction, 1)

		elif self.status == 'cling':
			self.roll_timer = self.roll_duration / 2 #redundant. helps with online problems. Occasional permanent roll.
			if self.direction == 'left':
				self.image = self.cling_sprite_left
			elif self.direction == 'right':
				self.image = self.cling_sprite_right
			self.bandana_info = ('cling', self.direction, 0)
			self.frame_counter += 1
			if self.frame_counter >= 20:
				self.jump_press()
				if self.direction == 'left':
					sprites.particle_generator.cling_particles((self.rect.right, self.rect.centery), self.direction, self.inverted_g)
				else:
					sprites.particle_generator.cling_particles((self.rect.left, self.rect.centery), self.direction, self.inverted_g)

		elif self.status == 'left':
			if self.land_frame is True:
				if self.land_frame_counter == 0:
					self.land_frame = False
				if self.direction == 'right':
					self.image = self.falling_right[1]
				elif self.direction == 'left':
					self.image = self.falling_left[1]
			else:
				if self.change_x + self.wind_speed <= 0:
					#modify how fast running feet move
					if self.item == 'metal suit':
						q = 6
					elif self.item == 'shoes':
						q = 3
					else:
						q = 5
					if self.frame_counter >= q:
						self.image_number += 1
						self.frame_counter = 0
						'''
						if self.item == 'metal suit':
							if self.image_number in (4,9):
								sounds.mixer.heavy_step.play()
						'''
					if self.image_number >= len(self.run_left) - 1:
						self.frame_counter = 0
						self.image_number = 0
					self.image = self.run_left[self.image_number]
					self.bandana_info = ('run', 'left', self.image_number)
		

				else:
					self.image = self.slide_right_image
					self.frame_counter = 0
					self.image_number = 0
					self.bandana_info = ('slide', self.direction, self.image_number)
					if self.inverted_g is False:
						sprites.particle_generator.slide_particles(self.rect.bottomright, 'right', self.inverted_g)
					else:
						sprites.particle_generator.slide_particles(self.rect.topright, 'right', self.inverted_g)
		elif self.status == 'right':
			if self.land_frame is True:
				if self.land_frame_counter == 0:
					self.land_frame = False
				if self.direction == 'right':
					self.image = self.falling_right[1]
				elif self.direction == 'left':
					self.image = self.falling_left[1]
			else:
				if self.change_x + self.wind_speed >= 0:
					#modify how fast running feet move
					if self.item == 'metal suit':
						q = 6
					elif self.item == 'shoes':
						q = 3
					else:
						q = 5
					if self.frame_counter >= q:
						self.image_number += 1
						self.frame_counter = 0
						'''
						if self.item == 'metal suit':
							if self.image_number in (4,9):
								sounds.mixer.heavy_step.play()
						'''
					if self.image_number >= len(self.run_right):# - 1:
						self.frame_counter = 0
						self.image_number = 0
					self.image = self.run_right[self.image_number]
					self.bandana_info = ('run', 'right', self.image_number)
		
				else:
					self.image = self.slide_left_image
					self.frame_counter = 0
					self.image_number = 0
					self.bandana_info = ('slide', self.direction, self.image_number)
					if self.inverted_g is False:
						sprites.particle_generator.slide_particles(self.rect.bottomleft, 'left', self.inverted_g)
					else:
						sprites.particle_generator.slide_particles(self.rect.topleft, 'left', self.inverted_g)

		elif self.status == 'jump' or self.status == 'roll':
			if self.image_number >= len(self.jump_right) - 1:
				self.image_number = 0
				self.frame_counter = 0

			if self.direction == 'left':
				self.image = self.jump_left[self.image_number]
			elif self.direction == 'right':
				self.image = self.jump_right[self.image_number]
			self.bandana_info = ('jump', self.direction, self.image_number)
			
			if self.frame_counter >= 3:
				self.image_number += 1
				self.frame_counter = 0

			

		#merged with jump... to make roll to jump smoother
		#elif self.status == 'roll':
		#	if self.image_number >= len(self.jump_right) - 1:
		#		self.image_number = 0
		#		self.frame_counter = 0
		#	if self.direction == 'left':
		#		self.image = self.jump_left[self.image_number]
		#	elif self.direction == 'right':
		#		self.image = self.jump_right[self.image_number]
		#	
		#	if self.frame_counter >= 2:
		#		self.image_number += 1
		#		self.frame_counter = 0
		

		elif self.status == 'knocked':
			#old_bottom = self.rect.bottom
			#old_centerx = self.rect.centerx
			self.image_number = 0
			if self.change_x > 0:
				if self.direction == 'right':
					self.image = self.knockforward_right[0]
					self.bandana_info = ('knocked forward', self.direction, self.image_number)
					if self.frame_counter <= 0:
						sprites.particle_generator.knocked_particles((self.rect.left + 5, self.rect.centery), 'left', self.inverted_g, self.knocked_particle_timer)
						self.knocked_particle_timer = 60
				elif self.direction == 'left':
					self.image = self.knockback_right[0]
					self.bandana_info = ('knocked back', self.direction, self.image_number)
					if self.frame_counter <= 0:
						sprites.particle_generator.knocked_particles((self.rect.left + 5, self.rect.centery), 'left', self.inverted_g, self.knocked_particle_timer)
						self.knocked_particle_timer = 60
			elif self.change_x < 0:
				if self.direction == 'right':
					self.image = self.knockback_left[0]
					self.bandana_info = ('knocked back', self.direction, self.image_number)
					if self.frame_counter <= 0:
						sprites.particle_generator.knocked_particles((self.rect.right - 5, self.rect.centery), 'right', self.inverted_g, self.knocked_particle_timer)
						self.knocked_particle_timer = 60
				elif self.direction == 'left':
					self.image = self.knockforward_left[0]
					self.bandana_info = ('knocked forward', self.direction, self.image_number)
					if self.frame_counter <= 0:
						sprites.particle_generator.knocked_particles((self.rect.right - 5, self.rect.centery), 'right', self.inverted_g, self.knocked_particle_timer)
						self.knocked_particle_timer = 60
			#self.rect = self.image.get_rect()
			#self.rect.bottom = old_bottom
			#self.rect.centerx = old_centerx
			#self.set_true_xy('xy')

		elif self.status == 'climb':
			if self.change_y == 0: #not climbing
				self.frame_counter -= 1 #don't want to change frames if not moving

			else:
				if self.frame_counter >= 10:
					self.image_number += 1
					self.frame_counter = 0
				if self.image_number >= len(self.climbing_sprite) - 1:
					self.rope_climb_mod *= -1
					self.image_number = 0
					self.frame_counter = 0

			if self.image_number >= len(self.climbing_sprite) - 1: #extra for online reasons
				self.image_number = 0
				self.frame_counter = 0

			self.image = self.climbing_sprite[self.image_number]
			self.bandana_info = ('climb', self.direction, self.image_number)

		elif self.status == 'falling':
			self.image_number = 0
			if self.direction == 'right':
				self.image = self.falling_right[0]
				self.bandana_info = ('falling', self.direction, self.image_number)
			elif self.direction == 'left':
				self.image = self.falling_left[0]
				self.bandana_info = ('falling', self.direction, self.image_number)


		if self.item == 'metal suit' and options.blit_frame is True: #Make Mallow Metallic
			if self.rect.height == 48:
				y_start = 20
				y_finish = self.rect.height - 8
			else:
				y_start = 0
				y_finish = self.rect.height
			i = self.image.copy()
			i.lock()
			array = pygame.PixelArray(i)
			x = 0
			y = y_start
			while y < y_finish - 1:
				x = 0
				while x < i.get_width() - 1:
					color = self.image.unmap_rgb(array[x,y])
					if color == options.LIGHT_PURPLE:
						array[x,y] = options.GREY_LIST[3]
					elif color == options.PURPLE:
						array[x,y] = options.GREY_LIST[2]
					elif color == options.DARK_PURPLE:
							array[x,y] = options.GREY_LIST[1]

					x += 1
				y += 1
			i.unlock()
			self.image = i

		#for testing:
		#self.visible_timer = 1
		#self.visible_switch = False

		if self.visible_timer > 0: #transition
			if self.visible == 0:
				self.visible = 1
			i = self.image.copy()
			i.lock()
			array = pygame.PixelArray(i)
			x = 0
			y = 0
			while y <= i.get_height() - 1:
				x = random.choice((0,1,2))
				while x <= i.get_width() - 1:
					

					color = self.image.unmap_rgb(array[x,y])
					if color != (0,255,0):
						array[x,y] = (0,255,0)

					if self.visible_switch is False: #turning invisible
						if self.visible_timer > 20:
							x_mod = random.choice((1,2,2,3,3))
						elif self.visible_timer > 10:
							x_mod = random.choice((1,2))
						elif self.visible_timer > 3:
							x_mod = random.choice((1,1,2))
						else:
							x_mod = random.choice((1,1,1,2))
					else:
						if self.visible_timer > 20:
							x_mod = random.choice((1,1,1,2))
						elif self.visible_timer > 10:
							x_mod = random.choice((1,1,2))
						elif self.visible_timer > 3:
							x_mod = random.choice((1,2))
						else:
							x_mod = random.choice((1,2,2,3,3))


					#if visible is False:
					#	array[x,y] = (0,255,0)
					
					x += x_mod
				y += 1
			i.unlock()
			self.image = i


		self.frame_counter += 1

		#if self.player_number == 1:
		#	print(self.inverted_g)

		if self.inverted_g is True: #and options.blit_frame is True:
			i = self.image.copy()
			self.image = pygame.transform.flip(i, False, True)





	def set_true_xy(self, type):
		if type == 'xy':
			self.true_x = self.rect.x
			self.true_y = self.rect.y
		elif type == 'x':
			self.true_x = self.rect.x
		elif type == 'y':
			self.true_y = self.rect.y
	
	def apply_gravity(self):
		if self.status != 'climb' and self.status != 'cling':
			if self.status != 'metal pound':
				if self.inverted_g is False:
					if self.change_y < options.max_g:
						self.change_y += options.change_g
				else:
					if self.change_y > (options.max_g * -1):
						self.change_y -= options.change_g
			else:
				if self.frame_counter > 15:
					if self.inverted_g is False:
						if self.metal_pound_timer >= 15: 
							sprites.particle_generator.metal_pound_particles(self.rect.midtop, self.inverted_g)
						if self.change_y < 8:
							self.change_y += 2
					else:
						if self.metal_pound_timer >= 15:
							sprites.particle_generator.metal_pound_particles(self.rect.midbottom, self.inverted_g)
						if self.change_y > -8:
							self.change_y -= 2
				else:
					if self.frame_counter < 9:
						sprites.particle_generator.metal_pound_charge_particles(self.rect.center, self)

	def set_avatar(self, avatar = None):
		if avatar != None:
			self.avatar = avatar

		if self.avatar == 'Ninja':
			self.spritesheet = sprites.SpriteSheet("ninjasheet.png")

		elif self.avatar == 'Robot':
			self.spritesheet = sprites.SpriteSheet("robotsheet.png")

		elif self.avatar == 'Dummy':
			self.spritesheet = sprites.SpriteSheet("dummysheet.png")

		elif self.avatar == 'Mutant':
			self.spritesheet = sprites.SpriteSheet("mutantsheet.png")

		elif self.avatar == 'Cyborg':
			self.spritesheet = sprites.SpriteSheet("cyborgsheet.png")

		self.build_ninja()

	def collect_FID_stats(self):
		if options.game_state == 'level':
								try:#need error so level portal managers don't try and get FIDS.
									if self.FID_inflictor != None:
										try:	
											if self.FID_inflictor[0] == 'gravity':
												if self.FID_inflictor[1] == self: #killed self
													self.FID_inflictor[1].stats_FIDs_suicide += 1
												elif self.FID_inflictor[1].color == self.color: #killed teamated
													self.stats_ally_FIDs_inflicted += 1
												else: #killed other
													self.FID_inflictor[1].FID_inflicted += 1
													self.FID_inflictor[1].stats_gravity_FIDs_inflicted += 1
										except:
											pass

										if self.FID_inflictor.type == 'portal_gun_bubble':
											if self.FID_inflictor.ninja != self and self.FID_inflictor.ninja.color != self.color: #only award points if not self or if not sharing color
												self.FID_inflictor.ninja.FID_inflicted += 1 #goes here first. Then awards the points when 'landing'. Done this way to make sure that ninja sticks their landing and doesn't fall in for a FID as well.
											
											self.FID_inflictor.ninja.stats_portal_gun_FIDs_inflicted += 1
											self.stats_portal_gun_FIDs_received += 1
											
										elif self.FID_inflictor.type == 'Ninja':
											if self.FID_inflictor != self and self.FID_inflictor.color != self.color: #don't count self or allies
												self.FID_inflictor.FID_inflicted += 1 #goes here first. Then awards the points when 'landing'. Done this way to make sure that ninja sticks their landing and doesn't fall in for a FID as well.
												if self.FID_inflictor.visible == 0:
													self.FID_inflictor.stats_invisible_FIDs_inflicted += 1
												if self.status == 'frozen':
													self.FID_inflictor.stats_ice_bomb_cube_FIDs += 1
											elif self.FID_inflictor.color == self.color: #killed ally!
												self.stats_ally_FIDs_inflicted += 1

									else: #nobody inflicted it
										self.stats_FIDs_suicide += 1
								except AttributeError:
									pass

								if options.versus_VP_per_FID_received == 'Ego Only':
									pass
								elif options.versus_VP_per_FID_received == 'Reset to 0':
									self.current_VP = 0
									self.VP_earned = 0
									for ninja in sprites.player_list:
										if ninja != self and ninja.color == self.color:
											ninja.current_VP = 0
								else: #FID reveived must be a number. Currently -1 or -2
									VP_change = int(options.versus_VP_per_FID_received)
									self.current_VP += VP_change
									self.VP_earned += VP_change
									if self.current_VP < 0:
										self.current_VP = 0
									for ninja in sprites.player_list:
										if ninja != self and ninja.color == self.color:
											ninja.current_VP = self.current_VP

								#FID_effect = 'Ego Only' #Ego Only, Wins -1, Wins to 0
								self.stats_FIDs_received += 1
								if self.visible == 0:
									self.stats_invisible_FIDs_received += 1

	def collision_check(self):
		self.friction = 'normal'
		if self.item != 'metal suit':
			friction_rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 2)
			for tile in sprites.tile_list:
				if tile.type == 'tile' or tile.type == 'platform':
					if tile.rect.colliderect(friction_rect):
						if tile.top_friction == 'icy':
							self.friction = 'icy'


		falling = True
		tile_list = []
		self.collision_check_needed = False
		for tile in sprites.tile_list:
			if tile.rect.colliderect(self.rect):

				if tile.type == 'mallow':
					if self.FID is False:
							
							if options.game_state == 'level':
								try:#need error so level portal managers don't try and get FIDS.
									if self.FID_inflictor != None:
										try:	
											if self.FID_inflictor[0] == 'gravity':
												if self.FID_inflictor[1] == self: #killed self
													self.FID_inflictor[1].stats_FIDs_suicide += 1
												elif self.FID_inflictor[1].color == self.color: #killed teamated
													self.stats_ally_FIDs_inflicted += 1
												else: #killed other
													self.FID_inflictor[1].FID_inflicted += 1
													self.FID_inflictor[1].stats_gravity_FIDs_inflicted += 1
										except:
											pass

										if self.FID_inflictor.type == 'portal_gun_bubble':
											if self.FID_inflictor.ninja != self and self.FID_inflictor.ninja.color != self.color: #only award points if not self or if not sharing color
												self.FID_inflictor.ninja.FID_inflicted += 1 #goes here first. Then awards the points when 'landing'. Done this way to make sure that ninja sticks their landing and doesn't fall in for a FID as well.
											
											self.FID_inflictor.ninja.stats_portal_gun_FIDs_inflicted += 1
											self.stats_portal_gun_FIDs_received += 1
											
										elif self.FID_inflictor.type == 'Ninja':
											if self.FID_inflictor != self and self.FID_inflictor.color != self.color: #don't count self or allies
												self.FID_inflictor.FID_inflicted += 1 #goes here first. Then awards the points when 'landing'. Done this way to make sure that ninja sticks their landing and doesn't fall in for a FID as well.
												if self.FID_inflictor.visible == 0:
													self.FID_inflictor.stats_invisible_FIDs_inflicted += 1
												if self.status == 'frozen':
													self.FID_inflictor.stats_ice_bomb_cube_FIDs += 1
											elif self.FID_inflictor.color == self.color: #killed ally!
												self.stats_ally_FIDs_inflicted += 1

									else: #nobody inflicted it
										self.stats_FIDs_suicide += 1
								except AttributeError:
									pass

								if options.versus_VP_per_FID_received == 'Ego Only':
									pass
								elif options.versus_VP_per_FID_received == 'Reset to 0':
									self.current_VP = 0
									self.VP_earned = 0
									for ninja in sprites.player_list:
										if ninja != self and ninja.color == self.color:
											ninja.current_VP = 0
								else: #FID reveived must be a number. Currently -1 or -2
									VP_change = int(options.versus_VP_per_FID_received)
									self.current_VP += VP_change
									self.VP_earned += VP_change
									if self.current_VP < 0:
										self.current_VP = 0
									for ninja in sprites.player_list:
										if ninja != self and ninja.color == self.color:
											ninja.current_VP = self.current_VP

								#FID_effect = 'Ego Only' #Ego Only, Wins -1, Wins to 0
								self.stats_FIDs_received += 1
								if self.visible == 0:
									self.stats_invisible_FIDs_received += 1
							self.FID = True
							self.mallow = tile
							self.splash_sprite.set_location(tile)
							self.ice_cube.cube_timer = 10
							self.ice_cube.update()
							sounds.mixer.FID.play()
						


					if tile.inverted is False:
							self.change_y = 1
							self.change_x *= .5
					else:
							self.change_y = -1
							self.change_x *= .5


				if tile.type == 'platform':
					if self.status != 'climb':
						if tile.top_rect.colliderect(self.rect_bottom) and self.change_y > 0:
							self.rect.bottom = tile.rect.top
							self.set_true_xy('y')
							#friction_list.append(tile.top_friction)
							self.land()
							falling = False
					else:
						land = True
						if self.rope != None:
							for point in self.rope.point_list:
								if point.rect.centery > tile.rect.top:
									land = False
									break
						else:
							land = False
						if land is True:
							if tile.top_rect.colliderect(self.rect_bottom) and self.change_y > 0:
								self.rect.bottom = tile.rect.top
								self.set_true_xy('y')
								#friction_list.append(tile.top_friction)
								self.land()
								falling = False


				if (tile.type == 'tile' or tile.type == 'mallow_wall'): #and self.status != 'climb':
					if tile.rect.colliderect(self.rect):
						tile_list.append(tile)

				if tile.type == 'pole' and self.status == 'climb':
					if self.rect.top < tile.rect.top:
						self.rect.top = tile.rect.top
						self.set_true_xy('y')
					if self.rect.bottom > tile.rect.bottom:
						self.rect.bottom = tile.rect.bottom
						self.set_true_xy('y')
		
		
		for tile in tile_list:

			if tile.top_rect.colliderect(self.rect_bottom):
				if self.item == 'metal suit' and tile.breakable is True:
					#if self.change_y > 5.3:
					if self.status == 'metal pound' or self.status == 'knocked':
						tile.destroy(self)
						#self.change_y = -2
						#if self.status != 'metal pound':
						sprites.particle_generator.land_particles((self.rect.centerx, tile.rect.top), self.inverted_g)
						for other_tile in tile_list:
							if other_tile != tile:
								if other_tile.breakable is True:
									if other_tile.top_rect.colliderect(self.rect_bottom):
										other_tile.destroy(self)
						if self.status == 'knocked':
							self.land()
					else:
						self.land()
					self.collision_check_needed = True
					self.rect.bottom = tile.rect.top
					self.set_true_xy('y')
					falling = False
					#self.change_y = 0
				else:
					self.collision_check_needed = True
					self.rect.bottom = tile.rect.top
					self.land()
					self.set_true_xy('y')
					falling = False
					#self.change_y = 0
				break

			if tile.bottom_rect.colliderect(self.rect_top):
				if self.item == 'metal suit' and tile.breakable is True and self.change_y < -1.25:
					tile.destroy(self)
					#print(self.change_y)
					self.change_y = 3
					for other_tile in tile_list:
						if other_tile != tile:
							if other_tile.breakable is True:
								if other_tile.bottom_rect.colliderect(self.rect_top):
									other_tile.destroy(self)
				self.collision_check_needed = True
				self.rect.top = tile.rect.bottom
				self.set_true_xy('y')
				self.change_y = 0
				break


		for tile in tile_list:
			if tile.rect.colliderect(self.rect):
				if tile.right_rect.colliderect(self.rect_left):
					self.collision_check_needed = True
					self.rect.left = tile.rect.right
					self.set_true_xy('x')
					if self.status == 'knocked':
						if self.item == 'metal suit' and tile.breakable is True:
							tile.destroy(self)
							for other_tile in tile_list:
								if other_tile != tile:
									if other_tile.breakable is True:
										if other_tile.right_rect.colliderect(self.rect_left):
											other_tile.destroy(self)
						if self.check_squished('wall_collision') is False:
							sounds.mixer.knocked.play()
							self.change_x = self.wall_knock - 1 #-1 modifies to make FIDS more likes
							self.frame_counter = 0
						else:
							self.change_x *= 0.0001 #using 0 messes up ninja image with gravity inversion
					elif self.status == 'frozen':
						sounds.mixer.knocked.play()
						self.change_x *= -1
						#self.change_y -= 2.5

					else:
						self.fire_x_speed = 0
						if self.status != 'left':
							#self.change_x = 0
							if self.wind_speed != 0:
								self.change_x = self.wind_speed * -1
							elif self.status == 'roll' and self.check_squished('land') is True:
								self.change_x *= -1
								self.direction = 'right'
							else:
								self.change_x = 0
						
				if tile.left_rect.colliderect(self.rect_right):
					self.collision_check_needed = True
					self.rect.right = tile.rect.left
					self.set_true_xy('x')
					if self.status == 'knocked':
						if self.item == 'metal suit' and tile.breakable is True:
							tile.destroy(self)
							for other_tile in tile_list:
								if other_tile != tile:
									if other_tile.breakable is True:
										if other_tile.left_rect.colliderect(self.rect_right):
											other_tile.destroy(self)
						if self.check_squished('wall_collision') is False:
							sounds.mixer.knocked.play()
							self.change_x = (self.wall_knock * -1 ) + 1 #-1 modifies to make FIDS more likes
							self.frame_counter = 0
						else:
							self.change_x *= 0.001 #using 0 messes up ninja image with gravity inversion
					elif self.status == 'frozen':
						sounds.mixer.knocked.play()
						self.change_x *= -1
						#self.change_y -= 2.5
					else:
						self.fire_x_speed = 0
						if self.status != 'right':
							if self.wind_speed != 0:
								self.change_x = self.wind_speed * -1
							elif self.status == 'roll' and self.check_squished('land') is True:
								self.change_x *= -1
								self.direction = 'left'
							else:
								self.change_x = 0

		if round(self.change_y) == 0:
			for tile in sprites.tile_list:
				bonus_rect = pygame.Rect(tile.rect.x,tile.rect.y - 1,tile.rect.width,1)#Bonus check to show 'not falling' right on top of rect
				if self.rect.colliderect(bonus_rect):
					falling = False
					break


		falling_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 1)
		for tile in sprites.tile_list:
			if tile.type == 'tile':
				if tile.rect.colliderect(falling_rect):
					falling = False
					break

		if self.status != 'frozen':
			if falling is True and self.status != 'climb' and self.status != 'cling':
				if self.status != 'jump' and self.status != 'knocked' and self.status != 'roll' and self.status != 'duck' and self.status != 'laser':
					if self.status not in ('fall_laser', 'fall_portal', 'fall_up_portal', 'metal pound'):
						self.status = 'falling'


	
	def set_gravity(self):
		if options.inverted_g is True:
			if self.inverted_g is False:
				self.invert_g()

		if options.inverted_g is False:
			if self.inverted_g is True:
				self.revert_g()

	def invert_g(self):
		self.inverted_g = True
		if self.status == 'metal pound':
			self.status = 'duck'
		#self.bomb_sprite.inverted_g = True
		#self.ice_bomb_sprite.inverted_g = True
		#for mine in self.mine_list:
		#	mine.inverted_g = True
		#self.portal_gun.portal_gun_portal1.inverted_g = True
		#self.portal_gun.portal_gun_portal2.inverted_g = True


	def revert_g(self):
		self.inverted_g = False
		if self.status == 'metal pound':
			self.status = 'duck'
		#self.bomb_sprite.inverted_g = False
		#self.ice_bomb_sprite.inverted_g = False
		#for mine in self.mine_list:
		#	mine.inverted_g = False
		#self.portal_gun.portal_gun_portal1.inverted_g = False
		#self.portal_gun.portal_gun_portal2.inverted_g = False

	def inverted_collision_check(self):
		self.friction = 'normal'
		if self.item != 'metal suit':
			friction_rect = pygame.Rect(self.rect.left, self.rect.top - 2, self.rect.width, 2)
			for tile in sprites.tile_list:
				if tile.type == 'tile' or tile.type == 'platform':
					if tile.rect.colliderect(friction_rect):
						if tile.bottom_friction == 'icy':
							self.friction = 'icy'

		falling = True
		tile_list = []
		self.collision_check_needed = False

		for tile in sprites.tile_list:
			if tile.rect.colliderect(self.rect):

				if tile.type == 'mallow':
					if self.FID is False:
						self.FID = True
						self.mallow = tile
						self.splash_sprite.set_location(tile)
						sounds.mixer.FID.play()
					if tile.inverted is False:
						self.change_y = 1
						self.change_x *= .5
					else:
						self.change_y = -1
						self.change_x *= .5

				if tile.type == 'platform':
					if self.status != 'climb':
						if tile.bottom_rect.colliderect(self.rect_bottom) and self.change_y < 0:
							self.rect.top = tile.rect.bottom
							#friction_list.append(tile.top_friction)
							self.set_true_xy('y')
							self.land()
							falling = False
					else:
						land = True
						if self.rope != None:
							for point in self.rope.point_list:
								if point.rect.centery < tile.rect.bottom:
									land = False
									break
						else:
							land = False
						if land is True:
							if tile.bottom_rect.colliderect(self.rect_bottom) and self.change_y < 0:
								self.rect.top = tile.rect.bottom
								#friction_list.append(tile.top_friction)
								self.set_true_xy('y')
								self.land()
								falling = False

				if (tile.type == 'tile' or tile.type == 'mallow_wall'):# and self.status != 'climb':
					tile_list.append(tile)

				if tile.type == 'pole' and self.status == 'climb':
					if self.rect.top < tile.rect.top:
						self.rect.top = tile.rect.top
						self.set_true_xy('y')
					if self.rect.bottom > tile.rect.bottom:
						self.rect.bottom = tile.rect.bottom
						self.set_true_xy('y')

		
		for tile in tile_list:
			if tile.bottom_rect.colliderect(self.rect_bottom):
				if self.item == 'metal suit' and tile.breakable is True:
					if self.status == 'metal pound' or self.status == 'knocked':
						tile.destroy(self)
						#self.change_y = 2
						#if self.status != 'metal pound':
						sprites.particle_generator.land_particles((self.rect.centerx, tile.rect.bottom), self.inverted_g)
						for other_tile in tile_list:
							if other_tile != tile:
								if other_tile.breakable is True:
									if other_tile.bottom_rect.colliderect(self.rect_bottom):
										other_tile.destroy(self)
						if self.status == 'knocked':
							self.land()
					else:
						self.land()
					self.collision_check_needed = True
					self.rect.top = tile.rect.bottom
					self.set_true_xy('y')
					falling = False
				else:
					self.collision_check_needed = True
					self.rect.top = tile.rect.bottom
					self.set_true_xy('y')
					self.land()
					falling = False



			if tile.top_rect.colliderect(self.rect_top):
				if self.item == 'metal suit' and tile.breakable is True and self.change_y > 1.25:
					tile.destroy(self)
					self.change_y = -3
					for other_tile in tile_list:
							if other_tile != tile:
								if other_tile.breakable is True:
									if other_tile.top_rect.colliderect(self.rect_top):
										other_tile.destroy(self)
				self.collision_check_needed = True
				self.rect.bottom = tile.rect.top
				self.set_true_xy('y')
				self.change_y = 0
				break


		for tile in tile_list:
			if tile.rect.colliderect(self.rect):
				if tile.right_rect.colliderect(self.rect_left):
					self.collision_check_needed = True
					self.rect.left = tile.rect.right
					self.set_true_xy('x')
					if self.status == 'knocked':
						if self.item == 'metal suit' and tile.breakable is True:
							tile.destroy(self)
							for other_tile in tile_list:
								if other_tile != tile:
									if other_tile.breakable is True:
										if other_tile.right_rect.colliderect(self.rect_left):
											other_tile.destroy(self)
						if self.check_squished('wall_collision') is False:
							self.change_x = self.wall_knock - 1 #-1 modifies to make FIDS more likes
							self.frame_counter = 0
							sounds.mixer.knocked.play()
						else:
							self.change_x *= 0.0001 #using 0 messes up ninja image with gravity inversion
					elif self.status == 'frozen':
						sounds.mixer.knocked.play()
						self.change_x *= -1
						self.change_y += 2.5
					else:
						self.fire_x_speed = 0
						if self.status != 'left':
							#self.change_x = 0
							if self.wind_speed != 0:
								self.change_x = self.wind_speed * -1
							elif self.status == 'roll' and self.check_squished('land') is True:
								self.change_x *= -1
								self.direction = 'right'
							else:
								self.change_x = 0
						
				if tile.left_rect.colliderect(self.rect_right):
					self.collision_check_needed = True
					self.rect.right = tile.rect.left
					self.set_true_xy('x')
					if self.status == 'knocked':
						if self.item == 'metal suit' and tile.breakable is True:
							tile.destroy(self)
							for other_tile in tile_list:
								if other_tile != tile:
									if other_tile.breakable is True:
										if other_tile.left_rect.colliderect(self.rect_right):
											other_tile.destroy(self)
						if self.check_squished('wall_collision') is False:
							self.change_x = (self.wall_knock * -1 ) + 1 #-1 modifies to make FIDS more likes
							self.frame_counter = 0
							sounds.mixer.knocked.play()
						else:
							self.change_x *= 0.0001 #using 0 messes up ninja image with gravity inversion
					elif self.status == 'frozen':
						sounds.mixer.knocked.play()
						self.change_x *= -1
						self.change_y += 2.5
					else:
						self.fire_x_speed = 0
						if self.status != 'right':
							#self.change_x = 0
							if self.wind_speed != 0:
								self.change_x = self.wind_speed
							elif self.status == 'roll' and self.check_squished('land') is True:
								self.change_x *= -1
								self.direction = 'left'
							else:
								self.change_x = 0

		if round(self.change_y) == 0:
			for tile in sprites.tile_list:
				bonus_rect = pygame.Rect(tile.rect.x,tile.rect.bottom,tile.rect.width,1)#Bonus check to show 'not falling' right on top of rect
				if self.rect.colliderect(bonus_rect):
					falling = False
					break
					

		falling_rect = pygame.Rect(self.rect.x, self.rect.top - 1, self.rect.width, 1)
		for tile in sprites.tile_list:
			if tile.type == 'tile':
				if tile.rect.colliderect(falling_rect):
					falling = False
					break		

		

		if self.status != 'frozen':
			if falling is True and self.status != 'climb' and self.status != 'cling':
				if self.status != 'jump' and self.status != 'knocked' and self.status != 'roll' and self.status != 'duck' and self.status != 'laser':
					if self.status not in ('fall_laser', 'fall_portal', 'fall_up_portal', 'metal pound'):
						self.status = 'falling'


	def reset_name(self):
		if self.player_number == 1:
			self.profile = 'Player1'
			self.name = 'Player1'

		elif self.player_number ==2:
			self.profile = 'Player2'
			self.name = 'Player2'

		elif self.player_number ==3:
			self.profile = 'Player3'
			self.name = 'Player3'

		elif self.player_number == 4:
			self.profile = 'Player4'
			self.name = 'Player4'

	def dist_check(self, point1, point2):
		distance = math.hypot(point1[0] - point2[0], point1[1] - point2[1])
		return distance


	def boundary_check(self):
		if self.FID is False and self.loop_physics is True:
			if self.change_x < 0:
				if self.rect.right < 0:
					self.rect.left = sprites.size[0]
					self.set_true_xy('x')
					self.bandana.new_position()

			elif self.change_x > 0:
				if self.rect.left > sprites.size[0]:
					self.rect.right = 0
					self.set_true_xy('x')
					self.bandana.new_position()

			if self.change_y < 0:
				if self.rect.bottom < 0:
					self.rect.top = sprites.size[1]
					for tile in sprites.tile_list:
						if tile.type == 'tile':
							if tile.rect.colliderect(self.rect):
								self.rect.top = tile.rect.bottom
					self.set_true_xy('y')
					self.bandana.new_position()

			elif self.change_y > 0:
				if self.rect.top > sprites.size[1]:
					self.rect.bottom = 0
					for tile in sprites.tile_list:
						if tile.type == 'tile':
							if tile.rect.colliderect(self.rect):
								self.rect.bottom = tile.rect.top
					self.set_true_xy('y')
					self.bandana.new_position()

	def item_press(self):
		if self.FID is False and self.status != 'frozen' and self.spawn_sprite.status == 'idle' and self in sprites.ninja_list:
			if self.item == 'laser':
				if self.status == 'idle' or self.status =='left' or self.status == 'right':
					self.status = 'laser'
					#if self.friction == 'normal':
					#	self.change_x = 0
					self.frame_counter = 0
					self.image_number = 0

				if self.status == 'falling':
					self.status = 'fall_laser'
					self.frame_counter = 0
					self.image_number = 0


			elif self.item == 'metal suit':
				if self.status == 'jump' or (self.status == 'roll' and abs(self.change_y) > 0.3):
					self.status = 'metal pound'
					self.frame_counter = 0
					self.image_number = 0
					self.change_y = 0
					self.change_x = 0
					self.metal_pound_timer = 15

			elif self.item == 'portal gun':
				if self.status == 'idle' or self.status == 'falling' or self.status =='left' or self.status == 'right':
					if self.portal_gun.bubble1.status == 'idle' or self.portal_gun.bubble2.status == 'idle' or self.portal_gun.bubble3.status == 'idle':
						if self.portal_gun.up_press is False:
							#if self.friction == 'normal':
							#	self.change_x = 0
							self.frame_counter = 0
							self.image_number = 0
							if self.status == 'falling':
								self.status = 'fall_portal'
							else:
								self.status = 'portal'
						else:
							if self.status == 'falling':
								self.status = 'fall_up_portal'
							else:
								self.status = 'up_portal'
							#if self.friction == 'normal':
							#	self.change_x = 0
							self.frame_counter = 0
							self.image_number = 0


			elif self.item == 'gravity':
				sprites.effects_screen.gravity(self)
				sounds.mixer.gravity.play()
				
				'''
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
				'''
				
				self.item_counter += 1
				#self.item_counter = 0
				self.stats_gravity_used += 1
				if self.item_counter >= 0:
					self.item_counter = 0
					self.item = 'none'
				#for stat tracking
				for ninja in sprites.ninja_list:
					ninja.FID_inflictor = ('gravity',self)

			elif self.item == 'rocket':
				if self.status == 'idle' or self.status == 'left' or self.status == 'right':
					if self.rocket.status == '':
						self.status = 'rocket'
						self.frame_counter = 0
						self.image_number = 0
						if self.friction == 'normal':
							self.change_x = 0


			elif self.item == 'mine':
				if self.status == 'idle' or self.status == 'falling' or self.status =='left' or self.status == 'right' or self.status == 'jump':
					self.mine1.attempt_throw()
					#self.item = 'mine'

			elif self.item == 'bomb':
				if self.status == 'idle' or self.status == 'falling' or self.status == 'left' or self.status == 'right' or self.status == 'jump' or (self.status == 'roll' and self.change_y != 0):
					if self.bomb_sprite.status == '':
						#moved within 'throw_bomb'
						#self.bomb_sprite.reset()
						#self.stats_bomb_thrown += 1
						self.bomb_sprite.throw_bomb()
						self.projectile_count += 1
						if self.projectile_count == 3:
							self.item = 'none'


			elif self.item == 'homing bomb':
					if self.homing_bomb1.status == '':
						self.homing_bomb1.throw_bomb()
					elif self.homing_bomb2.status == '':
						self.homing_bomb2.throw_bomb()
					elif self.homing_bomb3.status == '':
						self.homing_bomb3.throw_bomb()
					elif self.homing_bomb4.status == '':
						self.homing_bomb4.throw_bomb()
					else:
						self.homing_bomb1.reset()
						self.homing_bomb1.throw_bomb()
					self.stats_homing_bomb_activated += 1
					self.item = 'none'

			elif self.item == 'cloak':
				sounds.mixer.cloak.play()
				if self.visible == 1:
					#self.visible = 0
					self.visible_timer = 10
					self.visible_switch = False
					self.projectile_count += 1
				else:
					#self.visible = 1
					self.visible_timer = 10
					self.visible_switch = True
					if self.projectile_count >= 3:
						self.item = 'none'

			elif self.item == 'shield':
				if self.status != 'lose':
					self.shield_sprite.shield_timer = 0
					self.shield_sprite.active = True
					sounds.mixer.shield.play()
					self.item = 'none'

			elif self.item == 'ice bomb':
				if self.status == 'idle' or self.status == 'falling' or self.status == 'left' or self.status == 'right' or self.status == 'jump' or (self.status == 'roll' and self.change_y != 0):
					if self.ice_bomb_sprite.status == '':
						#self.ice_bomb_sprite.reset()
						self.ice_bomb_sprite.throw_bomb()
						self.item = 'none'
						#self.stats_ice_bomb_thrown

			elif self.item == 'wings':
				self.jump_press()

			elif self.item == 'solar flare':
				if self.solar_flare_sprite.status == 'idle':
					self.solar_flare_sprite.activate()
					self.item = 'none'

	def item_release(self):
		if self.status == 'rocket':
			self.status = 'idle'
			#if self.rocket.status == 'fired':
			#	self.rocket.explode()

	def right_press(self):
		if self.FID is False and self.spawn_sprite.status == 'idle':
			if self.status == 'idle' or self.status == 'right':
				
				if self.friction == 'normal':
					#self.change_x = self.x_speed_max
					self.change_x += self.x_accel / 2
					if self.change_x > self.x_speed_max:
						self.change_x = self.x_speed_max
				else:
					self.change_x += self.icy_x_accel
					if self.change_x > self.x_speed_max:
						self.change_x = self.x_speed_max
				self.direction = 'right'
				if self.status != 'right':
					self.image_number = 0
					self.frame_counter = 0
					self.status = 'right'


			elif self.status == 'jump' or self.status == 'falling' or self.status == 'climb' or self.status == 'fall_laser' or self.status == 'fall_portal' or self.status == 'fall_up_portal':
				if self.collision_timer == 0 and self.status != 'knocked':
					self.direction = 'right'
					self.change_x += self.x_accel
					if self.change_x > self.x_speed_max:
						self.change_x = self.x_speed_max
					
					if self.status == 'climb':
						if self.climb_lock == 0:
							self.climb_timer = 20 #how many frames until can climb again
							self.climb_jump_timer = 6 #how many frames you can jump for.
							self.change_y = 0
							self.status = 'falling'
						else:
							self.change_x = 0


			if self.status == 'rocket' and self.rocket.status == 'fired':
				self.rocket.right_input = True

			self.right_held = True


	def right_release(self):
		if self.status == 'right':
			if self.friction == 'normal':
				pass
				#self.change_x = 0
			self.status = 'idle'

		#elif self.status == 'jump' or self.status == 'falling':
		#	if self.collision_timer == 0:
		#		self.change_x = 0

		self.rocket.right_input = False
		self.right_held = False

	def left_press(self):
		
		if self.FID is False and self.spawn_sprite.status == 'idle':
			if self.status == 'idle' or self.status == 'left':
				if self.friction == 'normal':
					#self.change_x = self.x_speed_max * -1
					self.change_x -= self.x_accel / 2
					if self.change_x < -self.x_speed_max:
						self.change_x = -self.x_speed_max
				else:
					self.change_x -= self.icy_x_accel
					if self.change_x < -self.x_speed_max:
						self.change_x = -self.x_speed_max
				
				self.direction = 'left'
				if self.status != 'left':
					self.image_number = 0
					self.frame_counter = 0
					self.status = 'left'


			elif self.status == 'jump' or self.status == 'falling' or self.status == 'climb' or self.status == 'fall_laser' or self.status == 'fall_portal' or self.status == 'fall_up_portal':
				if self.collision_timer == 0 and self.status != 'knocked':
					self.change_x -= self.x_accel
					if abs(self.change_x) > self.x_speed_max:
						self.change_x = self.x_speed_max * -1
					if self.status == 'climb':
						if self.climb_lock == 0:
							self.change_y = 0
							self.status = 'falling'
							self.climb_timer = 20 #how many frames until can climb again
							self.climb_jump_timer = 6 #how many frames you can jump for.
						else:
							self.change_x = 0
					self.direction = 'left'


			if self.status == 'rocket' and self.rocket.status == 'fired':
				self.rocket.left_input = True
			self.left_held = True


	def left_release(self):
		if self.status == 'left':
			if self.friction == 'normal':
				pass
				#self.change_x = 0
			self.status = 'idle'

		#elif self.status == 'jump' or self.status == 'falling':
		#	if self.collision_timer == 0:
		#		self.change_x = 0

		self.rocket.left_input = False
		self.left_held = False

	
	def up_press(self):
		if self.spawn_sprite.status == 'idle':
			if self.status == 'rocket' and self.rocket.status == 'fired':
				self.rocket.up_input = True


			self.climb_attempt()
			if self.status == 'climb':
				self.change_y = self.climb_speed * -1
				#self.change_y = self.x_speed_max * -1
				if self.inverted_g is True:
					if self.pole != None:
						if self.pole.ends in ('bottom', False):
							if self.change_y < 0 and self.rect.top <= self.pole.rect.top:
								self.status = 'idle'

			if self.inverted_g is False:
				pass
				#self.portal_gun.up_press = True
			else:
				self.hold_duck = True
				if self.status == 'idle':
					self.frame_counter = 0
					self.image_number = 0
					self.status = 'duck'
					self.dirty = 1

					old_top = self.rect.top
					old_centerx = self.rect.centerx

					i = self.duck_neutral[1].copy()
					self.image = pygame.transform.flip(i,False,True)

					self.rect = self.image.get_rect()

					self.rect.top = old_top
					self.rect.centerx = old_centerx
					self.set_true_xy('xy')


	def up_release(self):
		if self.status == 'climb':
			self.change_y = 0

		if self.inverted_g is False:
			pass
			#self.portal_gun.up_press = False
		else:
			pass

		self.hold_duck = False
		if self.status == 'duck':
			self.stand_up()

		self.rocket.up_input = False

	def down_press(self):
		if self.FID is False and self.spawn_sprite.status == 'idle':
			if self.status == 'rocket' and self.rocket.status == 'fired':
				self.rocket.down_input = True

			self.climb_attempt()
			if self.status == 'climb':
				self.change_y = self.climb_speed
				if self.inverted_g is False:
					if self.pole != None:
						if self.pole.ends in ('top', False):
							if self.change_y > 0 and self.rect.bottom >= self.pole.rect.bottom:
								self.status = 'idle'


			if self.inverted_g is False:
				self.hold_duck = True
				if self.status == 'idle':
					self.stats_ducks_performed += 1

					self.frame_counter = 0
					self.image_number = 0
					self.status = 'duck'
					self.dirty = 1

					old_bottom = self.rect.bottom
					old_centerx = self.rect.centerx

					self.image = self.duck_neutral[1]
					self.rect = self.image.get_rect()

					self.rect.bottom = old_bottom
					self.rect.centerx = old_centerx
					self.set_true_xy('xy')


			else:
				pass
				#self.portal_gun.up_press = True



	def down_release(self):
		if self.status == 'climb':
			self.change_y = 0

		self.hold_duck = False
		if self.status == 'duck':
			self.stand_up()
		
		if self.inverted_g is True:
			pass
			#self.portal_gun.up_press = False

		self.rocket.down_input = False


	def stand_up(self):
		
			self.dirty = 1
			
			if self.inverted_g is False:
				top_rect = pygame.Rect(self.rect.x + 2,self.rect.top - 24,20,24)
				tile_list = sprites.quadrant_handler.get_quadrant(self)
				for tile in tile_list:
					if tile.type in ('tile'):
						if top_rect.colliderect(tile):
							self.rect.top = tile.rect.bottom + 24
				old_bottom = self.rect.bottom
				old_centerx = self.rect.centerx
				i = self.standing_image.copy()
				self.image = pygame.transform.flip(i,False,True)
				self.rect = self.image.get_rect()
				self.rect.bottom = old_bottom
				self.rect.centerx = old_centerx

			elif self.inverted_g is True:
				bottom_rect = pygame.Rect(self.rect.x + 2,self.rect.bottom,20,24)
				tile_list = sprites.quadrant_handler.get_quadrant(self)
				for tile in tile_list:
					if tile.type in ('tile'):
						if bottom_rect.colliderect(tile):
							self.rect.bottom = tile.rect.top - 24
					
				old_top = self.rect.top
				old_centerx = self.rect.centerx
				i = self.standing_image.copy()
				self.image = pygame.transform.flip(i,False,True)
				self.rect = self.image.get_rect()
				self.rect.top = old_top
				self.rect.centerx = old_centerx

			self.set_true_xy('xy')

			self.status = 'idle'




	def jump_press(self):
		if self.FID is False and self.spawn_sprite.status == 'idle':
			just_jumped = False #stops cling from occuring on same button press as initial jump

			if self.status == 'left' or self.status == 'right' or self.status == 'idle' or self.status == 'cling' or self.status == 'laser' or self.status == 'portal' or self.status == 'up_portal' or self.status == 'climb' or (self.status == 'falling' and self.climb_jump_timer > 0):
				#self.change_x = self.wind_speed
				
				if self.status == 'climb':
					self.climb_timer = 10

				just_jumped = True
				self.frame_counter = 0
				self.image_number = 0
				self.dirty = 1
				self.jump_held = True
				sounds.mixer.jump.play()

				if self.inverted_g is False:
					old_top = self.rect.top
					old_centerx = self.rect.centerx

					self.image = self.duck_neutral[1]
					self.rect = self.image.get_rect()

					self.rect.top = old_top
					self.rect.centerx = old_centerx

					self.change_y = self.jump_force
					self.set_true_xy('xy')
				else:
					old_bottom = self.rect.bottom
					old_centerx = self.rect.centerx

					self.image = self.duck_neutral[1]
					self.rect = self.image.get_rect()

					self.rect.bottom = old_bottom
					self.rect.centerx = old_centerx

					self.change_y = self.jump_force * -1
					self.set_true_xy('xy')

				if self.status == 'cling':
					self.roll_press() #use roll to lock out x movement controls briefly.
					self.roll_timer = self.roll_duration / 2 #times when roll stops. Only want to briefly lock controls.
					if self.direction == 'right':
						self.change_x = 0 - self.x_speed_max
						self.direction = 'left'
					elif self.direction == 'left':
						self.change_x = self.x_speed_max
						self.direction = 'right'
					self.image_number = 0
					self.frame_counter = 0
					self.stats_wall_jumps_performed += 1
					#self.double_jump = False
				else:
					self.status = 'jump'
					self.stats_jumps_performed += 1

			elif (self.status == 'jump' or self.status == 'falling') and just_jumped is False:
				left_top_rect = pygame.Rect(self.rect.x - 3, self.rect.centery - 13, 6, 2)
				right_top_rect = pygame.Rect(self.rect.right - 3, self.rect.centery - 13, 6, 2)
				left_bottom_rect = pygame.Rect(self.rect.x - 3, self.rect.centery + 11, 6, 2)
				right_bottom_rect = pygame.Rect(self.rect.right - 3, self.rect.centery + 11, 6, 2)
				left_middle_rect = pygame.Rect(self.rect.x - 3, self.rect.centery -9, 6, 18)
				right_middle_rect = pygame.Rect(self.rect.right - 3, self.rect.centery -9, 6, 18)


				left_top_check = False
				right_top_check = False
				left_bottom_check = False
				right_bottom_check = False
				left_middle_check = False
				right_middle_check = False

				right_pos = 0
				left_pos = 0

				big_rect = pygame.Rect(self.rect.left - 10, self.rect.top - 10, self.rect.width + 20, self.rect.height + 20)
				tile_list = []

				for tile in sprites.tile_list:
					if tile.type == 'tile' or tile.type == 'mallow_wall':
						tile_list.append(tile)

				left_tile = None
				right_tile = None
				for tile in tile_list:
					if tile.rect.colliderect(left_top_rect):
						left_top_check = True
					if tile.rect.colliderect(right_top_rect):
						right_top_check = True
					if tile.rect.colliderect(left_bottom_rect):
						left_bottom_check = True
					if tile.rect.colliderect(right_bottom_rect):
						right_bottom_check = True
					if tile.rect.colliderect(left_middle_rect):
						left_middle_check = True
						left_pos = tile.rect.right
						if left_tile == None or (abs(tile.rect.centery - self.rect.centery) < abs(left_tile.rect.centery - self.rect.centery)):
							left_tile = tile
					if tile.rect.colliderect(right_middle_rect):
						right_middle_check = True
						right_pos = tile.rect.left
						if right_tile == None or (abs(tile.rect.centery - self.rect.centery) < abs(right_tile.rect.centery - self.rect.centery)):
							right_tile = tile
				

				if left_middle_check is True and self.direction == 'left': # and left_top_check is True and left_bottom_check is True and self.direction == 'left':
						if left_top_check is False or left_bottom_check is False:
							if self.inverted_g is True:
								mod = 5
							else:
								mod = -5
							self.rect.top = left_tile.rect.top + mod
							self.set_true_xy('y')
						tall_rect = pygame.Rect(self.rect.x - 2,self.rect.y, self.rect.width + 4,self.rect.height)
						cling_allowed = True
						for item in sprites.active_items:
							if item.type == 'portal_gun_portal':
								if item.rect.colliderect(tall_rect):
									cling_allowed = False
									break
						if cling_allowed is True:
							self.rect.left = left_pos
							self.status = 'cling'
							self.double_jump = False
							self.direction = 'left'
							self.change_y = 0
							old_x = self.rect.centerx
							old_y = self.rect.centery
							self.image = self.cling_sprite_left
							self.rect = self.image.get_rect()
							self.rect.centerx = old_x
							self.rect.centery = old_y
							self.frame_counter = 0
							self.image_number = 0
							self.change_x = 0
							self.set_true_xy('xy')
							#sprites.particle_generator.cling_particles((self.rect.left, self.rect.centery), self.direction, self.inverted_g)

				elif right_middle_check is True and self.direction == 'right': #right_top_check is True and right_bottom_check is True and self.direction == 'right':
						if right_top_check is False or right_bottom_check is False:
							if self.inverted_g is True:
								mod = 5
							else:
								mod = -5
							self.rect.top = right_tile.rect.top + mod
							self.set_true_xy('y')
						tall_rect = pygame.Rect(self.rect.x - 2,self.rect.y, self.rect.width + 4,self.rect.height)
						cling_allowed = True
						for item in sprites.active_items:
							if item.type == 'portal_gun_portal':
								if item.rect.colliderect(tall_rect):
									cling_allowed = False
									break
						if cling_allowed is True:
							self.rect.right = right_pos
							self.status = 'cling'
							self.double_jump = False
							self.direction = 'right'
							self.change_y = 0
							old_x = self.rect.centerx
							old_y = self.rect.centery
							self.image = self.cling_sprite_right
							self.rect = self.image.get_rect()
							self.rect.centerx = old_x
							self.rect.centery = old_y
							self.frame_counter = 0
							self.image_number = 0
							self.change_x = 0
							self.set_true_xy('xy')
							#sprites.particle_generator.cling_particles((self.rect.right, self.rect.centery), self.direction, self.inverted_g)

				#the following exists to prevent cling from starting down inside block.
				if self.status == 'cling':
					for tile in sprites.tile_list:
						if tile.type == 'tile':
							if tile.rect.colliderect(self.rect):
								if self.rect.top < tile.rect.top:
									self.rect.bottom = tile.rect.top
									self.set_true_xy('y')
								elif self.rect.bottom > tile.rect.bottom:
									self.rect.top = tile.rect.bottom
									self.set_true_xy('y')
								break

			if just_jumped is False and (self.status == 'jump' or self.status == 'roll') and self.item == 'wings' and self.double_jump is False:
				if options.loop_physics is True or (options.loop_physics is False and self.rect.top > -48 and self.rect.bottom < 360 + 48):
					self.double_jump = True
					if self.inverted_g is False:
						self.change_y = self.jump_force
					else:
						self.change_y = self.jump_force * -1
					self.jump_held = True
					sounds.mixer.jump.play()
					self.stats_wing_double_jumps += 1

					#add feather effect.
					if self.feather_effect1.status == 'idle':
						wing_message = '123' #online purposes
						self.feather_effect1.activate()
						self.feather_effect2.activate()
						self.feather_effect3.activate()
					else:
						wing_message = '456' #online purposes
						self.feather_effect4.activate()
						self.feather_effect5.activate()
						self.feather_effect6.activate()




	def roll_press(self):
		if self.spawn_sprite.status == 'idle' and (self.status == 'left' or self.status == 'right' or self.status == 'idle' or self.status == 'cling'):
			if self.status != 'cling':
				self.stats_rolls_performed += 1
			if self.inverted_g is False:
				old_bottom = self.rect.bottom
				old_centerx = self.rect.centerx
				self.image = self.duck_neutral[0]
				self.rect = self.image.get_rect()
				self.rect.bottom = old_bottom
				self.rect.centerx = old_centerx
				self.set_true_xy('xy')
			else:
				old_top = self.rect.top
				old_centerx = self.rect.centerx
				self.image = self.duck_neutral[0]
				self.rect = self.image.get_rect()
				self.rect.top = old_top
				self.rect.centerx = old_centerx
				self.set_true_xy('xy')

			#self.change_y = int(self.jump_force * 2/3)
			if self.status == 'left' or (self.status == 'idle' and self.direction == 'left'):
				if self.friction == 'normal':
					self.change_x = 0 - self.x_speed_max
				else:
					#less slippery version:
					#self.change_x -= self.x_speed_max
					#if self.change_x < -self.x_speed_max:
					#	self.change_x = -self.x_speed_max
					
					#slippery version:
					if self.change_x > -0.5 and self.change_x < 0.5: #makes it so you can roll forward slowly when 'running against blocks.'
						self.change_x -= 0.75
					else:
						pass #roll at current change_x

			elif self.status == 'right' or (self.status == 'idle' and self.direction == 'right'):
				if self.friction == 'normal':
					self.change_x = self.x_speed_max
				else:
					#less slippery version:
					#self.change_x += self.x_speed_max
					#if self.change_x > self.x_speed_max:
					#	self.change_x = self.x_speed_max

					#more slippery version
					if self.change_x > -0.5 and self.change_x < 0.5: #makes it so you can roll forward slowly when 'running against blocks.'
						self.change_x += 0.75
					else:
						pass #roll at current change_x



			self.status = 'roll'
			self.dirty = 1

			self.roll_timer = self.roll_duration #times when roll stops



	def jump_release(self):
		self.jump_held = False

	def climb_attempt(self):
		if self.status in ('idle', 'falling', 'jump') and self.climb_timer == 0 and self.FID is False: #must be standing or falling. Not jumping.
			for sprite in sprites.tile_list:
				if sprite.type == 'pole':
					if sprite.rect.colliderect(self.rect):
						i = self.rect.centerx - sprite.rect.centerx
						if i > -10 and i < 10:
							centerx = sprite.rect.centerx
							centery = self.rect.centery

							if self.status == 'jump': #need to grow safely.
								self.image = self.climbing_sprite[0]
								self.rect = self.image.get_rect()
								self.rect.centery = centery
								if self.rect.top < sprite.rect.top:
									self.rect.top = sprite.rect.top
								elif self.rect.bottom > sprite.rect.bottom:
									self.rect.bottom = sprite.rect.bottom
							self.rect.centerx = centerx
							self.status = 'climb'
							self.double_jump = False
							self.image_number = 0
							self.frame_number = 0
							self.change_x = 0
							self.set_true_xy('xy')
							self.pole = sprite
							self.climb_lock = 30 #locks in climbing for 10 frames
							break

			for rope in sprites.level_ropes:
				if rope.climbable is True and rope.rope_type == 'classic':
					for point in rope.point_list:
						if self.rect.collidepoint(point.rect.center):
							i = self.rect.centerx - point.rect.centerx
							if i > -10 and i < 10:
								centery = self.rect.centery
								if self.status == 'jump': #need to grow safely.
									self.image = self.climbing_sprite[0]
									self.rect = self.image.get_rect()
									self.rect.centery = centery
								#if self.rect.top < sprite.rect.top:
								#	self.rect.top = sprite.rect.top
								#elif self.rect.bottom > sprite.rect.bottom:
								#	self.rect.bottom = sprite.rect.bottom

								self.rect.centerx = point.rect.centerx
								self.status = 'climb'
								self.double_jump = False
								self.image_number = 0
								self.frame_number = 0
								self.change_x = 0
								self.set_true_xy('xy')
								rope.ninja_list.append(self)
								self.rope = rope
								self.climb_lock = 30 #locks in climbing for 10 frames
								break

	def lose(self, menu_use = False):
		
		sprites.ninja_list.remove(self)
		sprites.active_sprite_list.remove(self)
		self.item_effect1.reset()
		self.item_effect2.reset()
		self.item_effect3.reset()
		self.shield_sprite.reset()
		self.volt_sprite.reset()
		self.ice_cube.reset()
		self.confused = False

		self.respawn_timer = 0
		self.status = 'lose'
		if options.versus_mode == 'Stock':
			if menu_use is False:
				self.lives -= 1


	def activate_death_sprite(self, death_type, cause):
		if self.FID is False and self.death_sprite.active is False:
			if self.visible == 0:
				self.stats_invisible_item_deaths += 1

			self.death_sprite.activate_death_sprite(self.rect, death_type, cause)
			if options.game_state == 'level':
				self.stats_item_deaths += 1

			if self.ice_cube.active is True:
				self.ice_cube.cube_timer = 1
				self.ice_cube.update()
			self.lose()
			#self.ice_cube.reset()
			sounds.mixer.death.play()

			if self.swag in ('Bandana', 'Headband'):
				self.bandana.headband.set_free(self.inverted_g)

	def land(self):
		#check for portal first:
		#make sure no portal collision bofore doing tile checks
		land = True
		for item in sprites.active_items:
			if item.type == 'portal_gun_portal':
				if self.rect.colliderect(item.collision_rect):
					if len(item.portal_gun.active_portal_list) == 2: #portal to teleport to!
						land = False
						break

		if land is True:
			#check space
			if self.status == 'climb':
				self.status = 'idle'
			if self.status not in ('jump', 'roll'):
				temp_change_y = self.change_y
				if temp_change_y > 3.5 or temp_change_y < -3.5:
					#if self.status == 'falling':
					self.land_frame = True
					self.land_frame_counter = 6
			else:
				temp_change_y = 0 #want roll and jump landings to look 'smoother'

			if self.item == 'metal suit':
				recent_pound = False
				temp_change_y = self.change_y
				if self.status == 'metal pound':
					if self.metal_pound_timer > 0:
						self.metal_pound_timer -= 1
						recent_pound = True
						if self.metal_pound_timer > 10:
							if self.inverted_g is False:
								sprites.particle_generator.metal_pound_land_particles((self.rect.centerx, self.rect.bottom), self.inverted_g)
							else:
								sprites.particle_generator.metal_pound_land_particles((self.rect.centerx, self.rect.top), self.inverted_g)
						if self.metal_pound_timer == 14:
							sounds.mixer.metal_pound.play()
							if sprites.shake_handler.current_shake < 2.5:
								sprites.shake_handler.current_shake = 2.5

			#print(self.max_knock_timer - self.knock_timer)
			self.fall_timer = 0
			if self.FID is False and self.status != 'frozen':
				self.FID_inflictor = None

				if self.status == 'duck' or self.status == 'roll':
					self.change_y = 0
					squished = self.check_squished('land')
					if squished is True:#check to see if there is room to stand.
						if self.status == 'duck':
							self.status = 'roll'
							self.image_number = 0
							self.frame_number = 0
						if self.roll_timer < 1:
							self.roll_timer = 1

				elif self.status == 'jump' or self.status == 'falling' or self.status =='knocked' or (self.status == 'metal pound' and self.metal_pound_timer == 0): # or self.status == 'roll':
					squished = self.check_squished('land')
					if squished is True:#check to see if there is room to stand.
						if self.direction == 'right':
							self.status = 'right'
						elif self.direction == 'left':
							self.status = 'left'
						self.roll_press()
						self.roll_timer = 1 #not a real roll...just a short one to get out of 'stuck'

					else: #not squished, proceed with linding.
							#if (self.status != 'roll' and self.status != 'duck') or (self.status == 'roll' and self.roll_timer <= 0):
							self.frame_counter = 0
							self.image_number = 1
							self.double_jump = False
							self.collision_timer = 0
							self.status = 'idle'
							self.dirty = 1
							self.jump_held = False

							if self.inverted_g is False:

								old_bottom = self.rect.bottom
								old_centerx = self.rect.centerx

								if self.hold_duck is False:
									self.image = self.standing_image
									self.rect = self.image.get_rect()
								else:
									self.status = 'duck'
									self.image = self.duck_neutral[1]
									self.rect = self.image.get_rect()
									self.image_number = 0



								self.rect.bottom = old_bottom
								self.rect.centerx = old_centerx
								self.set_true_xy('xy')
							else:
								old_top = self.rect.top
								old_centerx = self.rect.centerx

								if self.hold_duck is False:
									self.image = self.standing_image
									self.rect = self.image.get_rect()
								else:
									self.status = 'duck'
									self.image = self.duck_neutral[1]
									self.rect = self.image.get_rect()
									self.image_number = 0

								self.rect.top = old_top
								self.rect.centerx = old_centerx
								self.set_true_xy('xy')

							if self.friction == 'normal':
								pass
								#self.change_x = 0
							self.change_y = 0
				elif self.status == 'idle':
					if self.friction == 'normal':
						pass
						#self.change_x = 0
					self.change_y = 0

				elif self.status == 'fall_laser':
					self.change_y = 0
					self.status = 'laser'

				elif self.status == 'fall_up_portal':
					self.change_y = 0
					self.status = 'up_portal'
					
				elif self.status == 'fall_portal':
					self.change_y = 0
					self.status = 'portal'
				else:
					self.change_y = 0

				if temp_change_y > 4 or temp_change_y < -4:
					if self.inverted_g is False:
						sprites.particle_generator.land_particles((self.rect.centerx, self.rect.bottom - 2), self.inverted_g)
					else:
						sprites.particle_generator.land_particles((self.rect.centerx, self.rect.top + 2), self.inverted_g)
				if self.item == 'metal suit':
					if temp_change_y < -1 or temp_change_y > 1:
						if self.status != 'metal pound' and recent_pound is False:
							sounds.mixer.heavy_step.play()
							if sprites.shake_handler.current_shake < 1.5:
									sprites.shake_handler.current_shake = 1.5
							if self.inverted_g is False:
								sprites.particle_generator.land_particles((self.rect.centerx, self.rect.bottom - 2), self.inverted_g)
							else:
								sprites.particle_generator.land_particles((self.rect.centerx, self.rect.top + 2), self.inverted_g)



			elif self.status == 'frozen':
				self.change_y = 0




	def change_color(self, direction, color, color_tuple = None, change_bandana = True):
		#change color of mask/legs using pixelarray
		#moved to options.
		#RED = ((192,34,20), (221,57,57), (255,245,247))
		#GREEN = ((27,116,74), (91,190,97), (209,255,204))
		#BLUE = ((52,58,241), (34,116,255), (150,218,255))
		#PINK = ((217,72,221), (241,118,255), (254,245,246
		#GREY = ((97,84,118), (163,146,212), (210,204,243))
		#PURPLE = ((97,24,149), (143,75,237), (242,237,254))
		#ORANGE = ((241,110,3), (253,164,20), (255,226,44))

		if direction != None and color == None:
			i = options.color_choices.index(self.color) #get current position in choices
			if direction == 'right':
				i += 1
				if i > len(options.color_choices) - 1:
					i = 0
			elif direction =='left':
				i -= 1
				if i < 0:
					i = len(options.color_choices) - 1

			old_color = self.color
			self.color = options.color_choices[i]
		else:
			old_color = self.color
			if color == 'dummy':
				self.color = options.ORANGE_LIST
			else:
				if color_tuple is None:
					self.color = options.color_choices[color]
				else:
					self.color = color_tuple

			#make bananda same color as ninja for main menu
			if change_bandana is True:
				if self.bandana != None:
					self.bandana.kill()
				self.bandana = rope_physics.Bandana_Knot(self, self.color)

		for image_list in self.big_image_list:
			for image in image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace(old_color[0], self.color[0])
				array.replace(old_color[1], self.color[1])
				array.replace(old_color[2], self.color[2])
				array.replace(old_color[3], self.color[3])
				image.unlock()

		for image_list in self.death_sprite.big_image_list:
			for image in image_list:
				image.lock()
				array = pygame.PixelArray(image)
				array.replace(old_color[0], self.color[0])
				array.replace(old_color[1], self.color[1])
				array.replace(old_color[2], self.color[2])
				array.replace(old_color[3], self.color[3])
				image.unlock()



	def reset_stats(self):
		self.stats_awards_list = []
		self.rating = None
		#STATS TO TRACK!!!!! These stats are kept for the match (however many duels). On Exit, OR on end of Duel, ninja profiles are updated.
		self.stats_FIDs_inflicted = 0
		self.stats_FIDs_received = 0
		self.stats_FIDs_suicide = 0
		self.stats_item_kills = 0
		self.stats_item_deaths = 0
		self.stats_ally_item_kill = 0 #done
		self.stats_ally_FIDs_inflicted = 0 #done
		self.VP_earned = 0 #peronal VP earned. vs currentVP which as a team stat.
		self.wins_earned = 0 #personal wins earned. Vs currentWins which is a team stat
		self.stats_x_pixels_travelled = 0
		self.stats_y_pixels_travelled = 0
		self.stats_jumps_performed = 0
		self.stats_frames_jumping = 0
		self.stats_wall_jumps_performed = 0
		self.stats_rolls_performed = 0
		self.stats_ducks_performed = 0
		self.stats_frames_rolling = 0
		self.stats_frames_falling = 0
		self.stats_frames_running = 0
		self.stats_frames_idle = 0
		self.stats_frames_smug = 0
		self.stats_frames_ducking = 0
		self.stats_knocks_received = 0
		self.stats_knocks_inflicted = 0


		self.stats_shoes_acquired = 0
		self.stats_shoes_pixels_travelled = 0


		self.stats_laser_acquired = 0
		self.stats_laser_fired = 0
		self.stats_laser_kills = 0
		self.stats_laser_suicides = 0
		self.stats_laser_double_kills = 0
		self.stats_laser_triple_kills = 0
		self.stats_laser_vertical_kills = 0

		self.stats_wings_acquired = 0
		self.stats_wing_double_jumps = 0

		self.stats_skull_acquired = 0

		self.stats_bomb_acquired = 0
		self.stats_bomb_thrown = 0
		self.stats_bomb_kills = 0
		self.stats_bomb_suicides = 0
		self.stats_bomb_double_kills = 0
		self.stats_bomb_triple_kills = 0

		self.stats_volt_acquired = 0
		self.stats_volt_kills = 0
		self.stats_volt_double_kills = 0
		self.stats_volt_triple_kills = 0

		self.stats_mine_acquired = 0
		self.stats_mine_thrown = 0
		self.stats_mine_kills = 0
		self.stats_mine_suicides = 0
		self.stats_mine_double_kills = 0
		self.stats_mine_triple_kills = 0

		self.stats_rocket_acquired = 0
		self.stats_rocket_fired = 0
		self.stats_rocket_pixels_travelled = 0
		self.stats_rocket_kills = 0
		self.stats_rocket_suicides = 0
		self.stats_rocket_double_kills = 0
		self.stats_rocket_triple_kills = 0

		self.stats_portal_gun_acquired = 0
		self.stats_portal_gun_fired = 0
		self.stats_portal_gun_portals_created = 0
		self.stats_portal_gun_ninjas_teleported = 0
		self.stats_portal_gun_FIDs_inflicted = 0
		self.stats_portal_gun_FIDs_received = 0
		self.stats_portal_gun_times_teleported = 0
		self.stats_portal_gun_distance_teleported = 0
		self.stats_portal_gun_items_teleported = 0

		self.stats_ice_bomb_acquired = 0
		self.stats_ice_bomb_thrown = 0
		self.stats_ice_bomb_cubes_made = 0
		self.stats_ice_bomb_self_cubes = 0
		self.stats_ice_bomb_times_frozen = 0
		self.stats_ice_bomb_cube_FIDs = 0
		self.stats_ice_bomb_double_cubes = 0
		self.stats_ice_bomb_triple_cubes = 0
		self.stats_ice_bomb_quadruple_cubes = 0

		self.stats_cloak_acquired = 0
		self.stats_frames_invisible = 0
		self.stats_invisible_FIDs_inflicted = 0
		self.stats_invisible_FIDs_received = 0
		self.stats_invisible_item_deaths = 0
		self.stats_invisible_homing_bomb_evaded = 0

		self.stats_shield_acquired = 0
		self.stats_frames_with_shield_active = 0
		self.stats_shield_weapons_rebounded = 0

		self.stats_homing_bomb_acquired = 0
		self.stats_homing_bomb_activated = 0
		self.stats_homing_bomb_transferred = 0
		self.stats_homing_bomb_received = 0
		self.stats_homing_bomb_active_frames = 0
		self.stats_homing_bomb_kills = 0
		self.stats_homing_bomb_suicides = 0

		self.stats_gravity_acquired = 0
		self.stats_gravity_used = 0
		self.stats_frames_gravity_inverted = 0
		self.stats_frames_gravity_normal = 0
		self.stats_gravity_FIDs_inflicted = 0 

		self.duels_participated = 0
		self.matches_participated = 0
		self.stats_duels_survived = 0
		self.stats_matches_won = 0
		self.stats_matches_lost = 0
		self.stats_solo_matches_won = 0
		self.stats_solo_matches_lost = 0
		self.stats_matches_1v2_won = 0
		self.stats_matches_1v2_lost = 0
		self.stats_matches_1v3_won = 0
		self.stats_matches_1v3_lost = 0
		self.stats_matches_2v2_won = 0
		self.stats_matches_2v2_lost = 0
		self.stats_matches_3v1_won = 0
		self.stats_matches_3v1_lost = 0
		self.stats_matches_2v1_won = 0
		self.stats_matches_2v1_lost = 0

	def update_profile_stats(self):
		#STATS TO TRACK!!!!! These stats are kept for the match (however many duels). On Exit, OR on end of Duel, ninja profiles are updated.
		data_manager.user_profiles[self.profile]['Stats']['stats_FIDs_inflicted'] += self.stats_FIDs_inflicted
		data_manager.user_profiles[self.profile]['Stats']['stats_FIDs_received'] += self.stats_FIDs_received
		data_manager.user_profiles[self.profile]['Stats']['stats_FIDs_suicide'] += self.stats_FIDs_suicide
		data_manager.user_profiles[self.profile]['Stats']['stats_item_kills'] += self.stats_item_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_item_deaths'] += self.stats_item_deaths
		data_manager.user_profiles[self.profile]['Stats']['stats_ally_item_kill'] += self.stats_ally_item_kill
		data_manager.user_profiles[self.profile]['Stats']['stats_ally_FIDs_inflicted'] += self.stats_ally_FIDs_inflicted
		data_manager.user_profiles[self.profile]['Stats']['VP_earned'] += self.VP_earned
		data_manager.user_profiles[self.profile]['Stats']['wins_earned'] += self.wins_earned



		data_manager.user_profiles[self.profile]['Stats']['stats_x_pixels_travelled'] += self.stats_x_pixels_travelled
		data_manager.user_profiles[self.profile]['Stats']['stats_y_pixels_travelled'] += self.stats_y_pixels_travelled
		data_manager.user_profiles[self.profile]['Stats']['stats_jumps_performed'] += self.stats_jumps_performed
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_jumping'] += self.stats_frames_jumping
		data_manager.user_profiles[self.profile]['Stats']['stats_wall_jumps_performed'] += self.stats_wall_jumps_performed
		data_manager.user_profiles[self.profile]['Stats']['stats_rolls_performed'] += self.stats_rolls_performed
		data_manager.user_profiles[self.profile]['Stats']['stats_ducks_performed'] += self.stats_ducks_performed
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_rolling'] += self.stats_frames_rolling
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_falling'] += self.stats_frames_falling
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_running'] += self.stats_frames_running
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_idle'] += self.stats_frames_idle
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_smug'] += self.stats_frames_smug
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_ducking'] += self.stats_frames_ducking
		data_manager.user_profiles[self.profile]['Stats']['stats_knocks_received'] += self.stats_knocks_received
		data_manager.user_profiles[self.profile]['Stats']['stats_knocks_inflicted'] += self.stats_knocks_inflicted

		data_manager.user_profiles[self.profile]['Stats']['stats_shoes_acquired'] += self.stats_shoes_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_shoes_pixels_travelled'] += self.stats_shoes_pixels_travelled


		data_manager.user_profiles[self.profile]['Stats']['stats_laser_acquired'] += self.stats_laser_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_laser_fired'] += self.stats_laser_fired
		data_manager.user_profiles[self.profile]['Stats']['stats_laser_kills'] += self.stats_laser_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_laser_suicides'] += self.stats_laser_suicides
		data_manager.user_profiles[self.profile]['Stats']['stats_laser_double_kills'] += self.stats_laser_double_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_laser_triple_kills'] += self.stats_laser_triple_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_laser_vertical_kills'] += self.stats_laser_vertical_kills

		data_manager.user_profiles[self.profile]['Stats']['stats_wings_acquired'] += self.stats_wings_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_wing_double_jumps'] += self.stats_wing_double_jumps

		data_manager.user_profiles[self.profile]['Stats']['stats_skull_acquired'] += self.stats_skull_acquired

		data_manager.user_profiles[self.profile]['Stats']['stats_bomb_acquired'] += self.stats_bomb_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_bomb_thrown'] += self.stats_bomb_thrown
		data_manager.user_profiles[self.profile]['Stats']['stats_bomb_kills'] += self.stats_bomb_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_bomb_suicides'] += self.stats_bomb_suicides
		data_manager.user_profiles[self.profile]['Stats']['stats_bomb_double_kills'] += self.stats_bomb_double_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_bomb_triple_kills'] += self.stats_bomb_triple_kills

		data_manager.user_profiles[self.profile]['Stats']['stats_volt_acquired'] += self.stats_volt_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_volt_kills'] += self.stats_volt_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_volt_double_kills'] += self.stats_volt_double_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_volt_triple_kills'] += self.stats_volt_triple_kills

		data_manager.user_profiles[self.profile]['Stats']['stats_mine_acquired'] += self.stats_mine_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_mine_thrown'] += self.stats_mine_thrown
		data_manager.user_profiles[self.profile]['Stats']['stats_mine_kills'] += self.stats_mine_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_mine_suicides'] += self.stats_mine_suicides
		data_manager.user_profiles[self.profile]['Stats']['stats_mine_double_kills'] += self.stats_mine_double_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_mine_triple_kills'] += self.stats_mine_triple_kills

		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_acquired'] += self.stats_rocket_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_fired'] += self.stats_rocket_fired
		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_pixels_travelled'] += self.stats_rocket_pixels_travelled
		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_kills'] += self.stats_rocket_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_suicides'] += self.stats_rocket_suicides
		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_double_kills'] += self.stats_rocket_double_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_rocket_triple_kills'] += self.stats_rocket_triple_kills

		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_acquired'] += self.stats_portal_gun_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_fired'] += self.stats_portal_gun_fired
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_portals_created'] += self.stats_portal_gun_portals_created
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_ninjas_teleported'] += self.stats_portal_gun_ninjas_teleported
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_FIDs_inflicted'] += self.stats_portal_gun_FIDs_inflicted
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_FIDs_received'] += self.stats_portal_gun_FIDs_received
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_times_teleported'] += self.stats_portal_gun_times_teleported
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_distance_teleported'] += self.stats_portal_gun_distance_teleported
		data_manager.user_profiles[self.profile]['Stats']['stats_portal_gun_items_teleported'] += self.stats_portal_gun_items_teleported

		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_acquired'] += self.stats_ice_bomb_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_thrown'] += self.stats_ice_bomb_thrown
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_cubes_made'] += self.stats_ice_bomb_cubes_made
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_self_cubes'] += self.stats_ice_bomb_self_cubes
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_times_frozen'] += self.stats_ice_bomb_times_frozen
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_cube_FIDs'] += self.stats_ice_bomb_cube_FIDs
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_double_cubes'] += self.stats_ice_bomb_double_cubes
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_triple_cubes'] += self.stats_ice_bomb_triple_cubes
		data_manager.user_profiles[self.profile]['Stats']['stats_ice_bomb_quadruple_cubes'] += self.stats_ice_bomb_quadruple_cubes

		data_manager.user_profiles[self.profile]['Stats']['stats_cloak_acquired'] += self.stats_cloak_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_invisible'] += self.stats_frames_invisible
		data_manager.user_profiles[self.profile]['Stats']['stats_invisible_FIDs_inflicted'] += self.stats_invisible_FIDs_inflicted
		data_manager.user_profiles[self.profile]['Stats']['stats_invisible_FIDs_received'] += self.stats_invisible_FIDs_received
		data_manager.user_profiles[self.profile]['Stats']['stats_invisible_item_deaths'] += self.stats_invisible_item_deaths
		data_manager.user_profiles[self.profile]['Stats']['stats_invisible_homing_bomb_evaded'] += self.stats_invisible_homing_bomb_evaded

		data_manager.user_profiles[self.profile]['Stats']['stats_shield_acquired'] += self.stats_shield_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_with_shield_active'] += self.stats_frames_with_shield_active
		data_manager.user_profiles[self.profile]['Stats']['stats_shield_weapons_rebounded'] += self.stats_shield_weapons_rebounded

		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_acquired'] += self.stats_homing_bomb_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_activated'] += self.stats_homing_bomb_activated
		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_transferred'] += self.stats_homing_bomb_transferred
		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_received'] += self.stats_homing_bomb_received
		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_active_frames'] += self.stats_homing_bomb_active_frames
		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_kills'] += self.stats_homing_bomb_kills
		data_manager.user_profiles[self.profile]['Stats']['stats_homing_bomb_suicides'] += self.stats_homing_bomb_suicides

		data_manager.user_profiles[self.profile]['Stats']['stats_gravity_acquired'] += self.stats_gravity_acquired
		data_manager.user_profiles[self.profile]['Stats']['stats_gravity_used'] += self.stats_gravity_used
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_gravity_inverted'] += self.stats_frames_gravity_inverted
		data_manager.user_profiles[self.profile]['Stats']['stats_frames_gravity_normal'] += self.stats_frames_gravity_normal
		data_manager.user_profiles[self.profile]['Stats']['stats_gravity_FIDs_inflicted'] += self.stats_gravity_FIDs_inflicted


		data_manager.user_profiles[self.profile]['Stats']['duels_participated'] += self.duels_participated
		data_manager.user_profiles[self.profile]['Stats']['matches_participated'] += self.matches_participated
		data_manager.user_profiles[self.profile]['Stats']['stats_duels_survived'] += self.stats_duels_survived
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_won'] += self.stats_matches_won
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_lost'] += self.stats_matches_lost
		data_manager.user_profiles[self.profile]['Stats']['stats_solo_matches_won'] += self.stats_solo_matches_won
		data_manager.user_profiles[self.profile]['Stats']['stats_solo_matches_lost'] += self.stats_solo_matches_lost
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_1v2_won'] += self.stats_matches_1v2_won
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_1v2_lost'] += self.stats_matches_1v2_lost
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_1v3_won'] += self.stats_matches_1v3_won
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_1v3_lost'] += self.stats_matches_1v3_lost
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_2v2_won'] += self.stats_matches_2v2_won
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_2v2_lost'] += self.stats_matches_2v2_lost
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_3v1_won'] += self.stats_matches_3v1_won
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_3v1_lost'] += self.stats_matches_3v1_lost
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_2v1_won'] += self.stats_matches_2v1_won
		data_manager.user_profiles[self.profile]['Stats']['stats_matches_2v1_lost'] += self.stats_matches_2v1_lost


class SplashSprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image_list = []
		self.image_number = 0
		self.frame_counter = 0

		image = self.ninja.spritesheet.getImage(250, 49, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(299, 49, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(348, 49, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(397, 49, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(446, 49, 48, 48)
		self.image_list.append(image)

		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 4)

		self.visible = 0
		self.dirty = 1

		self.rect.bottom = 334

		self.inverted = False

	def update(self):
		if self.frame_counter == 0:
			self.dirty = 1
			self.image_number = 0
			i = self.image_list[self.image_number]
			if self.inverted is True:
				self.image = pygame.transform.flip(i, False, True)
			else:
				self.image = i


			self.visible = True
			self.rect.centerx = self.ninja.rect.centerx
			self.image 

			if self.rect.right > self.mallow.rect.right:
				self.image = self.image.copy()
				pygame.draw.rect(self.image, options.GREEN, (self.mallow.rect.right - self.rect.left,0, self.rect.right - self.mallow.rect.right,self.rect.height), 0)
			elif self.rect.left < self.mallow.rect.left:
				self.image = self.image.copy()
				pygame.draw.rect(self.image, options.GREEN, (0,0, self.mallow.rect.left - self.rect.left,self.rect.height), 0)


		if self.frame_counter >= 10:
			self.image_number += 1
			self.frame_counter = 1
			self.dirty = 1
			if self.image_number >= len(self.image_list):
				self.visible = 0
				self.ninja.lose()
				if self.ninja.swag in ('Bandana', 'Headband'):
					try:
						self.ninja.bandana.kill()
					except ValueError: 
						print('ValueError')


				self.image_number = 0
				self.frame_counter = 0
			else:
				i = self.image_list[self.image_number]
				if self.inverted is True:
					self.image = pygame.transform.flip(i, False, True)
				else:
					self.image = i

				if self.rect.right > self.mallow.rect.right:
					self.image = self.image.copy()
					pygame.draw.rect(self.image, options.GREEN, (self.mallow.rect.right - self.rect.left,0, self.rect.right - self.mallow.rect.right,self.rect.height), 0)
				elif self.rect.left < self.mallow.rect.left:
					self.image = self.image.copy()
					pygame.draw.rect(self.image, options.GREEN, (0,0, self.mallow.rect.left - self.rect.left,self.rect.height), 0)

		
		self.frame_counter += 1

		
		


		

		

	def reset(self):
		self.visible = 0
		self.image_number = 0
		self.frame_counter = 0
		self.dirty = 1

	def set_location(self, mallow):
		self.ninja.on_fire = False
		self.mallow = mallow

		self.ninja.shield_sprite.reset()
		self.ninja.volt_sprite.volt_timer = 1000 

		if mallow.inverted is False:
			self.rect.bottom = mallow.rect.top + 3
			self.inverted = False
			sprites.particle_generator.FID_particles((self.ninja.rect.centerx, self.rect.bottom), self.inverted, self.ninja)
		elif mallow.inverted is True:
			self.rect.top = mallow.rect.bottom - 3
			self.inverted = True
			sprites.particle_generator.FID_particles((self.ninja.rect.centerx, self.rect.top), self.inverted, self.ninja)

class Spawn_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image = pygame.Surface((24,48))
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 4)
		sprites.item_effects.add(self)

		self.visible = 0
		self.dirty = 1

		self.width_counter = 0
		self.frame_counter = 0
		self.status = 'idle'

		self.inverted_g = False

		self.particle_counter = 0
		self.moving_platform = None
	def update(self):
		if self.status == 'idle':
			pass

		elif self.status == 'build_up':
			self.frame_counter += 1

			if self.moving_platform != None:
				self.update_position()


			particlexy = (random.randrange(self.base_centerx - 18, self.base_centerx + 18, 1), self.base_centery)
			sprites.particle_generator.spawn_bottom_particles(particlexy, self.inverted_g, self.ninja.color, moving_platform = self.moving_platform)

			
			if self.frame_counter > 10:
				self.particle_counter += 1
				if self.particle_counter >= 5:
					self.particle_counter = 0
					particlexy = (random.randrange(self.base_centerx - 12, self.base_centerx + 12, 1), self.base_centery)
					sprites.particle_generator.spawn_vertical_particles(particlexy, self.inverted_g, self.ninja.color, moving_platform = self.moving_platform)


			if self.frame_counter > 30:
				self.status = 'spawn'
				self.frame_counter = 0

		elif self.status == 'spawn':
			self.frame_counter += 1
			self.width_counter += 1

			if self.moving_platform != None:
				self.update_position()

			particlexy = (random.randrange(self.base_centerx - 18, self.base_centerx + 18, 1), self.base_centery)
			sprites.particle_generator.spawn_bottom_particles(particlexy, self.inverted_g, self.ninja.color, moving_platform = self.moving_platform)

			self.particle_counter += 1
			if self.particle_counter >= 5:
				self.particle_counter = 0
				particlexy = (random.randrange(self.base_centerx - 12, self.base_centerx + 12, 1), self.base_centery)
				sprites.particle_generator.spawn_vertical_particles(particlexy, self.inverted_g, self.ninja.color, moving_platform = self.moving_platform)

			if self.frame_counter == 1:
				self.phase_ninja()

			if self.frame_counter > 1:
				if self.inverted_g is False:
					self.base_centery = self.ninja.rect.bottom
				else:
					self.base_centery = self.ninja.rect.top
				self.base_centerx = self.ninja.rect.centerx
			
			if self.frame_counter > 40:
				self.reset()

			self.ninja.update()

	def update_position(self):
		self.base_centerx = self.moving_platform.rect.centerx
		self.base_centery = self.moving_platform.rect.top
		self.ninja.rect.centerx = self.moving_platform.rect.centerx
		self.ninja.rect.bottom = self.moving_platform.rect.top
		self.ninja.set_true_xy('xy')

	def phase_ninja(self):
		if self.moving_platform != None:
			self.ninja_placement_xy = (self.moving_platform.rect.centerx, self.moving_platform.rect.top - 24)
		self.ninja.place_ninja(self.ninja_placement_xy, inverted_g = self.inverted_g)
		self.ninja.visible = 0
		self.ninja.visible_timer = 30
		self.ninja.visible_switch = True
		self.ninja.bandana.flip_visible('invisible')
		sprites.ninja_list.remove(self.ninja)
	
	def reset(self):
		sprites.ninja_list.add(self.ninja)
		if options.game_state == 'level' and sprites.countdown_timer.done is True: #in level give players 3 seconds of invincibility.
			self.ninja.shield_sprite.activate(spawn=True)
		self.visible = 0
		self.dirty = 1
		self.frame_counter = 0
		self.width_counter = 0
		self.status = 'idle'

		if len(sprites.gravity_objects) == 0:
			self.ninja.set_gravity()

		self.moving_platform = None
		self.inverted_g = False

		#self.ninja.name_bar.reset()
		#self.ninja.score_bar.reset()
		#self.ninja.stock_bar.reset()

	def activate(self, inverted_g, base_centerxy, ninja_placement_xy, moving_platform):
		self.status = 'build_up'
		self.inverted_g = inverted_g
		self.base_centerx = base_centerxy[0]
		self.base_centery = base_centerxy[1]
		self.ninja_placement_xy = ninja_placement_xy

		self.rect.centerx = self.base_centerx
		if inverted_g is False:
			self.rect.bottom = self.base_centery
		else:
			self.rect.top = self.base_centery

		self.moving_platform = moving_platform



class DeathSprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image_list = []
		self.volt_image_list = []
		self.big_image_list = []
		self.image_number = 0
		self.frame_counter = 0

		image = self.ninja.spritesheet.getImage(0, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(25, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(50, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(75, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(100, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(125, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(150, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(175, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(200, 295, 24, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(225, 295, 24, 48)
		self.image_list.append(image)

		image = self.ninja.spritesheet.getImage(429, 147, 24, 48)
		self.volt_image_list.append(image)
		image = self.ninja.spritesheet.getImage(454, 147, 24, 48)
		self.volt_image_list.append(image)

		self.big_image_list.append(self.image_list)
		self.big_image_list.append(self.volt_image_list)

		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 0)

		sprites.item_effects.add(self) #add here allows update without call from 'ninja'

		self.visible = 0
		self.dirty = 1

		self.inverted_g = False

		self.active = False

		self.death_type = None
		self.cause = None
		self.cause_rect = None
		self.cause_subtype = None

		self.base_image = None
		self.y_counter = 0
		self.x_counter = 0
		self.x_counter_change = 0
		self.y_counter_change = 0
		self.event_delay1 = 0
		self.event_delay2 = 0
		self.event_trigger1 = False
		self.event_trigger2 = False
		self.particle_list1 = []
		self.particle_list2 = []
		self.particle_list3 = []
		self.particle_list4 = []
		self.explosion_origin = None
		self.moving_platform = None
		self.platform_xmod = 0

		self.change_x = 0
		self.change_y = 0
		self.true_x = 0
		self.true_y = 0

	def update(self):

		if self.active is True:
			if self.moving_platform != None:
				if self.inverted_g is False:
					self.rect.bottom = self.moving_platform.rect.top
				else:
					self.rect.top = self.moving_platform.rect.bottom
				self.rect.centerx = self.moving_platform.rect.centerx + self.platform_xmod
				self.true_x = self.rect.centerx
				self.true_y = self.rect.centery
				self.dirty = 1

			if self.death_type == 'fire':
				if self.frame_counter == 0:
					self.dirty = 1

				elif self.frame_counter == 1:
					self.image = self.base_image.copy()
					self.dirty = 1
					#if self.inverted_g is True:
					#	i = self.image.copy()
					#	self.image = pygame.transform.flip(i,False,True)
					
					#turn mallow brown-black
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = 0
					while y <= self.image.get_height() - 1:
						x = 0
						while x <= self.image.get_width() - 1:
							color = self.image.unmap_rgb(array[x,y])
							if color == options.LIGHT_PURPLE:
								array[x,y] = options.LIGHT_BURNT
							elif color == options.PURPLE:
								array[x,y] = options.BURNT
							elif color == options.DARK_PURPLE:
									array[x,y] = options.DARK_BURNT
							elif color == options.OUTLINE_PURPLE:
									array[x,y] = options.OUTLINE_BURNT
							
							elif color == self.ninja.color[0]:
									array[x,y] = options.BLACK
							elif color == self.ninja.color[1]:
									array[x,y] = options.BLACK
							elif color == self.ninja.color[2]:
									array[x,y] = options.GREY_LIST[0]
							elif color == self.ninja.color[3]:
									array[x,y] = options.GREY_LIST[1]
							elif color == options.FACE:
									array[x,y] = options.GREY_LIST[1]

							x += 1
						y += 1
					self.image.unlock()
				
					'''
					elif self.frame_counter == 30:
					self.image = self.base_image.copy()
					self.dirty = 1
					#if self.inverted_g is True:
					#	i = self.image.copy()
					#	self.image = pygame.transform.flip(i,False,True)
					
					#turn mallow brown-black
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = 0
					while y <= self.image.get_height() - 1:
						x = 0
						while x <= self.image.get_width() - 1:
							color = self.image.unmap_rgb(array[x,y])
							if color == options.LIGHT_PURPLE:
								array[x,y] = options.LIGHT_BURNT
							elif color == options.PURPLE:
								array[x,y] = options.BURNT
							elif color == options.DARK_PURPLE:
									array[x,y] = options.DARK_BURNT
							elif color == options.OUTLINE_PURPLE:
									array[x,y] = options.OUTLINE_BURNT
							elif color == self.ninja.color[0]:
									array[x,y] = options.BLACK
							elif color == self.ninja.color[1]:
									array[x,y] = options.BLACK
							elif color == self.ninja.color[2]:
									array[x,y] = options.GREY_LIST[0]
							elif color == self.ninja.color[3]:
									array[x,y] = options.GREY_LIST[1]
							elif color == options.FACE:
									array[x,y] = options.GREY_LIST[1]

							x += 1
						y += 1
					self.image.unlock()
					'''

				elif self.frame_counter == 60:
						self.x_counter = self.rect.width - 1
						self.particle_list1 = []
						self.particle_list2 = []
						self.particle_list3 = []
						self.particle_list4 = []

				elif self.frame_counter > 61:
						self.dirty = 1
						self.image.lock()
						array = pygame.PixelArray(self.image)
						y = 0
						x = self.x_counter
						#decide how many of the particles to make.

			
						color_list = [options.BURNT, options.LIGHT_BURNT, options.DARK_BURNT, options.OUTLINE_BURNT, options.GREEN]
						if self.event_delay2 >= 2:	
							self.event_delay2 = 0
							if x >= 0:
								y = 0
								while y <= self.image.get_height() - 1:
									if self.rect.height == 48:
										choice = random.randrange(0,6,1)
									else:
										choice = random.randrange(0,2,1)
									color = self.image.unmap_rgb(array[x,y])
									if color in color_list:
										if color != options.GREEN:
											self.particle_list1.append((x,y))
									else:		
										array[x,y] = options.GREEN
										if choice == 1:
											sprites.particle_generator.single_dust_particles((self.rect.x + x, self.rect.y + y), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g)
									y += 1
							self.x_counter -= 1
						self.event_delay2 += 1
						self.image.unlock()
					
				if self.frame_counter == 120:
						if len(self.particle_list1) > 0:
							leftx = None
							rightx = None
							topy = None
							bottomy = None
							for coord in self.particle_list1:
								if leftx == None or coord[0] < leftx:
									leftx = coord[0]
								if rightx == None or coord[0] > rightx:
									rightx = coord[0]
								if topy == None or coord[1] < topy:
									topy = coord[1]
								if bottomy == None or coord[1] > bottomy:
									bottomy = coord[1]
							temp_rect = pygame.Rect(leftx + self.rect.x,topy + self.rect.y,rightx - leftx,bottomy - topy)
							sprites.particle_generator.tile_death_particles(temp_rect, 'burnt', self.inverted_g, 0)
						self.reset()

				

				if self.frame_counter < 30 and self.frame_counter != 0:
					sprites.particle_generator.fire_burn_particles(self, 6, 0)
					for ninja in sprites.ninja_list:
						if ninja != self.ninja:
							if ninja.collision_rect.colliderect(self.rect):
								ninja.set_fire()

				self.frame_counter += 1

			elif self.death_type == 'spikes':
				if self.frame_counter == 0:
					self.dirty = 1
					sprites.active_sprite_list.change_layer(self, sprites.active_sprite_list.get_layer_of_sprite(self.cause) - 1)
					self.x_counter = 0

				if self.frame_counter >= 0:
					self.dirty = 1
					self.image.lock()
					array = pygame.PixelArray(self.image)
					#y = 0
					#x = self.x_counter
					#decide how many of the particles to make.
					#color_list = self.ninja.color_list
					#if self.event_delay2 >= 2:	
					#self.event_delay2 = 0
					i = 0
					while i < 2:
						y = 0
						x = self.x_counter
						if x <= self.rect.width / 2:
							y = 0
							while y <= self.image.get_height() - 1:
								if self.rect.height == 48:
									choice = random.randrange(0,6,1)
								else:
									choice = random.randrange(0,2,1)
								color = self.image.unmap_rgb(array[x,y])
								#from left side:
								if color != options.GREEN:
									array[x,y] = options.GREEN
									if choice == 1:
										change_x = random.randrange(-10,-1,1) / 5
										change_y = random.randrange(-10,-5,1) / 5
										if self.inverted_g is True:
											change_y *= -1
										changexy = (change_x, change_y)
										sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + self.image.get_height() - y - 1), color, self.ninja, self.inverted_g, None, changexy, None)
								#from right side:
								color = self.image.unmap_rgb(array[self.rect.width - x - 1,y])
								if color != options.GREEN:
									array[self.rect.width - x - 1,y] = options.GREEN
									if choice == 1:
										change_x = random.randrange(1,10,1) / 7
										change_y = random.randrange(-10,-5,1) / 5
										if self.inverted_g is True:
											change_y *= -1
										changexy = (change_x, change_y)
										sprites.particle_generator.single_mallow_particles((self.rect.x + self.rect.width - x - 1, self.rect.y + self.image.get_height() - y - 1), color, self.ninja, self.inverted_g, None, changexy, None)

								y += 1
						self.x_counter += 1
						#self.event_delay2 += 1
						i += 1
					self.image.unlock()

				self.frame_counter += 1

				if self.x_counter > self.rect.width / 2:
					self.reset()

			elif self.death_type == 'metal suit':
				self.dirty = 1
				if self.cause.change_y != 0:
					self.event_trigger1 = True

				
				if self.event_trigger1 is True:
					self.event_delay1 += 1
					self.visible = 1
					self.dirty = 1
					#sprites.particle_generator.mine_death_particles(self.rect, self.inverted_g, self.ninja)
					y_dist = self.rect.height / (self.rect.height / 4)
					
					self.image.lock()
					array = pygame.PixelArray(self.image)
					i = 0
					attempt = 0
					while i < 10:
						color = (0,255,0)

						while color == (0,255,0) and attempt < 2:
							x = random.randrange(0,self.rect.width,1)
							if self.ninja.inverted_g is True:
								y = random.randrange(self.rect.height - (y_dist * self.event_delay1), self.rect.height - (y_dist * (self.event_delay1 - 1)),1)
							else:
								y = random.randrange(0 + (y_dist * (self.event_delay1 - 1)), 0 + (y_dist * self.event_delay1),1)
							color = self.image.unmap_rgb(array[x,y])
							attempt += 1
						if color != (0,255,0):
							temp_change_x = random.randrange(10,20,1) * 0.25
							if x < self.rect.width / 2:
								temp_change_x *= -1
							temp_change_y = random.randrange(-15,15,1) * 0.2
							other_temp_change_y = -8
							if self.ninja.inverted_g is False:
								temp_change_y *= -1
								other_temp_change_y *= -1
							sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + y), color, self.ninja, self.inverted_g, None, (temp_change_x, temp_change_y), None)
							sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + y), color, self.ninja, self.inverted_g, None, (0, other_temp_change_y), None)
						i += 1
						attempt = 0
					self.image.unlock()
							

					if self.ninja.inverted_g is True:
						pygame.draw.rect(self.image, (0,255,0),(0, self.rect.height - (y_dist * self.event_delay1),self.rect.width,y_dist),0)
					else:
						pygame.draw.rect(self.image, (0,255,0),(0, 0 + (y_dist * (self.event_delay1 - 1)),self.rect.width,y_dist),0)	

					if y_dist * self.event_delay1 >= self.rect.height:
						self.reset() 
					

				self.frame_counter += 1
				'''
				if self.cause.inverted_g is False:

					y_dist = self.cause.rect.bottom - self.rect.top
					temp_rect = pygame.Rect(0 + self.rect.x, self.y_counter + self.rect.y,self.rect.width,y_dist)
					sprites.particle_generator.metal_suit_death_particles(temp_rect, self.inverted_g, self.ninja)


					temp_rect = pygame.Rect(0, self.y_counter,self.rect.width,y_dist)
					pygame.draw.rect(self.image, (0,255,0),temp_rect,0)
					if self.y_counter + y_dist >= self.rect.height:
						self.event_trigger1 = True
					self.y_counter = y_dist #holds last endpoint to start at next time.


				if self.event_trigger1 is True:
					self.reset()
				'''

			elif self.death_type == 'volt':
				if self.event_trigger1 is False:
					if self.frame_counter >= 6:
						self.dirty = 1
						self.frame_counter = 0
						self.image_number += 1
						if self.image_number > 1:
							self.image_number = 0

					self.image = self.volt_image_list[self.image_number]

					if self.inverted_g is True:
						i = self.image.copy()
						self.image = pygame.transform.flip(i,False,True)

					if self.event_delay1 > 55:
						self.event_trigger1 = True
						self.frame_counter = 0

					self.frame_counter += 1
					self.event_delay1 += 1

				else:
					if self.frame_counter == 1:
						self.image = self.image_list[0].copy()
						self.dirty = 1
						if self.inverted_g is True:
							i = self.image.copy()
							self.image = pygame.transform.flip(i,False,True)
						#turn mallow brown-black
						self.image.lock()
						array = pygame.PixelArray(self.image)
						x = 0
						y = 0
						while y <= self.image.get_height() - 1:
							x = 0
							while x <= self.image.get_width() - 1:
								color = self.image.unmap_rgb(array[x,y])
								if color == options.LIGHT_PURPLE:
									array[x,y] = options.LIGHT_BURNT
								elif color == options.PURPLE:
									array[x,y] = options.BURNT
								elif color == options.DARK_PURPLE:
										array[x,y] = options.DARK_BURNT
								elif color == options.OUTLINE_PURPLE:
										array[x,y] = options.OUTLINE_BURNT
								elif color == self.ninja.color[0]:
										array[x,y] = options.BLACK
								elif color == self.ninja.color[1]:
										array[x,y] = options.BLACK
								elif color == self.ninja.color[2]:
										array[x,y] = options.GREY_LIST[0]
								elif color == self.ninja.color[3]:
										array[x,y] = options.GREY_LIST[1]
								elif color == options.FACE:
										array[x,y] = options.GREY_LIST[1]

								x += 1
							y += 1
						self.image.unlock()

					#if self.frame_counter > 30:
					#	self.reset()

					if self.frame_counter == 50:
						self.x_counter = self.rect.width - 1
						self.particle_list1 = []
						self.particle_list2 = []
						self.particle_list3 = []
						self.particle_list4 = []

					elif self.frame_counter > 50:
						self.dirty = 1
						self.image.lock()
						array = pygame.PixelArray(self.image)
						y = 0
						x = self.x_counter
						#decide how many of the particles to make.

			
						color_list = [options.BURNT, options.LIGHT_BURNT, options.DARK_BURNT, options.OUTLINE_BURNT, options.GREEN]
						if self.event_delay2 >= 2:	
							self.event_delay2 = 0
							if x >= 0:
								y = 0
								while y <= self.image.get_height() - 1:
									if self.rect.height == 48:
										choice = random.randrange(0,6,1)
									else:
										choice = random.randrange(0,2,1)
									color = self.image.unmap_rgb(array[x,y])
									if color in color_list:
										if color != options.GREEN:
											self.particle_list1.append((x,y))
									else:		
										array[x,y] = options.GREEN
										if choice == 1:
											sprites.particle_generator.single_dust_particles((self.rect.x + x, self.rect.y + y), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g)
									y += 1
							self.x_counter -= 1
						self.event_delay2 += 1
						self.image.unlock()
					
					if self.frame_counter == 100:
						if len(self.particle_list1) > 0:
							leftx = None
							rightx = None
							topy = None
							bottomy = None
							for coord in self.particle_list1:
								if leftx == None or coord[0] < leftx:
									leftx = coord[0]
								if rightx == None or coord[0] > rightx:
									rightx = coord[0]
								if topy == None or coord[1] < topy:
									topy = coord[1]
								if bottomy == None or coord[1] > bottomy:
									bottomy = coord[1]
							temp_rect = pygame.Rect(leftx + self.rect.x,topy + self.rect.y,rightx - leftx,bottomy - topy)
							sprites.particle_generator.tile_death_particles(temp_rect, 'burnt', self.inverted_g, 0)
						self.reset()
					self.frame_counter += 1

			elif self.death_type == 'laser':
				
				if self.frame_counter == 0:
					self.visible = True
					#turn mallow brown-black
					
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = 0
					y_mod = 0
					
					#Just saves some unecessary pixel operations. Only need to catch mallow. Also helps 'Mutant' Colors work.
					if self.image.get_height() == 48:
						if self.inverted_g is False:
							y = 18
							y_mod = 7
						else:
							y = 7
							y_mod = 18

					while y <= self.image.get_height() - 1 - y_mod:
						x = 0
						while x <= self.image.get_width() - 1:
							color = self.image.unmap_rgb(array[x,y])
							if color == options.LIGHT_PURPLE:
								array[x,y] = options.LIGHT_BURNT
							elif color == options.PURPLE:
								array[x,y] = options.BURNT
							elif color == options.DARK_PURPLE:
									array[x,y] = options.DARK_BURNT
							elif color == options.OUTLINE_PURPLE:
									array[x,y] = options.OUTLINE_BURNT

							x += 1
						y += 1
					self.image.unlock()
					
					if self.cause_subtype == 'horizontal': #horzontal laser:
						pygame.draw.rect(self.image, (0,255,0), (0,self.cause_rect.y - self.rect.y,self.rect.width,self.cause_rect.height), 0)
					elif self.cause_subtype == 'vertical':
						pygame.draw.rect(self.image, (0,255,0), (self.cause_rect.x - self.rect.x,0,self.cause.rect.width,self.rect.height), 0)
				
				
				self.frame_counter += 1
				if self.frame_counter > 30:
					self.dirty = 1
					

					#turn mallow brown-black
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = self.y_counter
					#decide how many of the particles to make.

					color_list = [options.BURNT, options.LIGHT_BURNT, options.DARK_BURNT, options.OUTLINE_BURNT, options.GREEN]
					
					if y <= self.image.get_height() / 2:
						if self.event_delay2 >= 1:
							self.event_delay2 = 0
							x = 0
							while x <= self.image.get_width() - 1:
								if self.rect.height == 48:
									choice = random.randrange(0,6,1)
								else:
									choice = random.randrange(0,2,1)
								color = self.image.unmap_rgb(array[x,y])
								if color not in color_list:
									array[x,y] = options.GREEN
									if choice == 1:
										sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + y), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g, None, None, None)
								color = self.image.unmap_rgb(array[x,self.image.get_height() - y - 1])
								if color not in color_list:
									array[x,self.image.get_height() - y - 1] = options.GREEN
									choice = random.randrange(0,10,1)
									if choice == 1:
										sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + self.image.get_height() - y - 1), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g, None, None, None)
								x += 1
							self.y_counter += 1
						self.event_delay2 += 1

					else:
						self.event_delay1 += 1
						if self.event_delay1 > 10:
							if self.image.get_height() == 48:
								temp_rect = pygame.Rect(self.rect.centerx - 10, self.rect.centery - 10, 20,20)
							elif self.image.get_height() == 24:
								temp_rect = pygame.Rect(self.rect.centerx - 10, self.rect.centery - 10, 20,20)

							sprites.particle_generator.tile_death_particles(temp_rect, 'burnt', self.inverted_g, 0)
							self.reset()
					self.image.unlock()

					

			elif self.death_type == 'saw':
				self.dirty = 1
				if self.frame_counter == 0:
					self.overlap_rect = self.rect.clip(self.cause.rect)
					#self.overlap_point = (self.overlap_rect.centerx,self.overlap_rect.centery)

				if options.update_state == 1:
					self.overlap_rect.x += self.cause.change_x
					self.overlap_rect.y += self.cause.change_y

				self.frame_counter += 1
				if self.frame_counter <= 60:

					self.explosion_origin = (self.cause.rect.centerx,self.cause.rect.centery)
					self.visible = True

					pygame.draw.circle(self.image, (0,255,0), (self.cause.rect.centerx - self.rect.x,self.cause.rect.centery - self.rect.y), 12, 0)
					#circle(Surface, color, pos, radius, width=0) -> Rect

					speed = 1
					if self.rect.centerx > self.cause.rect.centerx:
						self.rect.centerx -= speed
					elif self.rect.centerx < self.cause.rect.centerx:
						self.rect.centerx += speed

					if self.rect.centery > self.cause.rect.centery:
						self.rect.centery -= speed
					elif self.rect.centery < self.cause.rect.centery:
						self.rect.centery += speed
					self.true_x = self.rect.x
					self.true_y = self.rect.y
				
					i = 0
					while i < 2:
						temp_point = (random.randrange(self.overlap_rect.x,self.overlap_rect.x + self.overlap_rect.width,1) , random.randrange(self.overlap_rect.y,self.overlap_rect.y + self.overlap_rect.height,1))
						temp_color = random.choice((options.LIGHT_PURPLE, options.PURPLE, self.ninja.color[2], self.ninja.color[2], self.ninja.color[2]))
						
						if abs(self.rect.centery - self.cause_rect.centery) <= 2:
							y_mod = random.choice((-1,1))
						elif self.cause.rect.centery > self.overlap_rect.centery:
							y_mod = -1
						else:
							y_mod = 1

						speed = random.randrange(4,9,1)
						base_angle = math.sin((temp_point[0] - self.cause.rect.centerx)/(temp_point[1] - self.cause.rect.centery + 0.5))
						angle = base_angle #math.radians(random.randrange(30,60,1)) #* random.choice((1,-1))
						change_x = math.sin(angle) * speed 
						change_y = math.cos(angle) * speed * y_mod


						#if self.cause.rect.centery > self.overlap_rect.centery:
						#	change_y *= -1
						sprites.particle_generator.single_mallow_particles(temp_point,temp_color, self.ninja, self.inverted_g, temp_point, (change_x, change_y), None)
						sprites.particle_generator.single_mallow_particles(temp_point,temp_color, self.ninja, self.inverted_g, temp_point, (change_x, change_y), None)
						i += 1

				if self.frame_counter > 20:
					if abs(self.rect.centerx - self.cause_rect.centerx) <= 2 and abs(self.rect.centery - self.cause_rect.centery) <= 2:
						old_center = self.rect.center
						if self.rect.height < 10:
							self.reset()
						else:
							new_image = pygame.Surface((self.rect.width,self.rect.height-2))
							new_image.fill(options.GREEN)
							new_image.blit(self.image,(0,0) ,area=(0,0,self.rect.width,round(self.rect.height / 2)))
							new_image.blit(self.image,(0,round(self.rect.height / 2) - 1) ,area=(0,(self.rect.height / 2) + 1,self.rect.width,round(self.rect.height / 2)))
							new_image.set_colorkey(options.GREEN)
							self.image = new_image
							self.rect = self.image.get_rect()
							self.rect.center = old_center


						#self.ninja.frozen_image_small.blit(self.ninja.image, (0,0))
						#blit(source, dest, area=None, special_flags = 0)

				'''	
				if self.frame_counter > 20:

						array = pygame.PixelArray(self.image)
						x = 0
						y = self.y_counter
						#decide how many of the particles to make.
						
						if y <= self.image.get_height() / 2:
							x = 0
							while x <= self.image.get_width() - 1:
								choice = random.randrange(0,6,1)
								#if self.rect.height == 48:
								#	choice = random.randrange(0,6,1)
								#else:
								#	choice = random.randrange(0,2,1)
								color = self.image.unmap_rgb(array[x,y])
								if color != options.GREEN:
									array[x,y] = options.GREEN
									if choice == 1:
										sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + y), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g, None, None)
								color = self.image.unmap_rgb(array[x,self.image.get_height() - y - 1])
								if color != options.GREEN:
									array[x,self.image.get_height() - y - 1] = options.GREEN
									choice = random.randrange(0,6,1)
									if choice == 1:
										sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + self.image.get_height() - y - 1), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g, None, None)
								x += 1
							self.y_counter += 1
						else:
							self.reset()
				'''

			elif self.death_type == 'side boulder':
				self.dirty = 1
				if self.frame_counter == 0:
					old_bottom = self.rect.bottom
					old_x = self.rect.x
					self.image = self.base_image
					self.rect = self.image.get_rect()
					self.rect.x = old_x
					self.rect.bottom = old_bottom
					if self.cause.rect.centerx > self.rect.centerx:
						self.x_counter = self.rect.width - 1
						self.x_counter_change = -1
					else:
						self.x_counter = 0
						self.x_counter_change = 1
					
				self.image.lock()
				array = pygame.PixelArray(self.image)
				self.y_counter = 0
				i = 3
				while i > 0:
					while self.y_counter < self.rect.height - 1:
						#print(self.y_counter)
						color = self.image.unmap_rgb(array[self.x_counter, self.y_counter])
						if color != (0,255,0):
							temp_change_x = random.randrange(10,20,1) * 0.25 * self.x_counter_change
							temp_change_y = random.randrange(-15,15,1) * 0.2
							other_temp_change_y = -8
							if self.ninja.inverted_g is False:
								temp_change_y *= -1
								other_temp_change_y *= -1
							sprites.particle_generator.single_mallow_particles((self.rect.x + self.x_counter, self.rect.y + self.y_counter), color, self.ninja, self.inverted_g, None, (temp_change_x, temp_change_y), None)
							sprites.particle_generator.single_mallow_particles((self.rect.x + self.x_counter, self.rect.y + self.y_counter), color, self.ninja, self.inverted_g, None, (0, other_temp_change_y), None)
						self.y_counter += random.choice((2,3,4))
					pygame.draw.rect(self.image, (0,255,0), (self.x_counter,0,1,self.rect.height), 0)
					i -= 1
					self.x_counter += self.x_counter_change
				self.image.unlock()

				if self.x_counter_change > 0:
					if self.x_counter >= self.rect.width:
						self.reset() 
				else:
					if self.x_counter <= 0:
						self.reset()

					
				self.rect.x += self.x_counter_change
				self.frame_counter += 1

			elif self.death_type == 'explosion':
				
				if self.frame_counter == 0:
					self.explosion_origin = (self.cause.rect.centerx,self.cause.rect.centery)
					self.visible = True
					#turn mallow brown-black
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = 0
					while y <= self.image.get_height() - 1:
						x = 0
						while x <= self.image.get_width() - 1:
							color = self.image.unmap_rgb(array[x,y])
							if color == options.LIGHT_PURPLE:
								array[x,y] = options.LIGHT_BURNT
							elif color == options.PURPLE:
								array[x,y] = options.BURNT
							elif color == options.DARK_PURPLE:
									array[x,y] = options.DARK_BURNT
							elif color == options.OUTLINE_PURPLE:
									array[x,y] = options.OUTLINE_BURNT
							elif color == self.ninja.color[0]:
									array[x,y] = options.BLACK
							elif color == self.ninja.color[1]:
									array[x,y] = options.BLACK
							elif color == self.ninja.color[2]:
									array[x,y] = options.GREY_LIST[0]
							elif color == self.ninja.color[3]:
									array[x,y] = options.GREY_LIST[1]
							elif color == options.FACE:
									array[x,y] = options.GREY_LIST[1]

							x += 1
						y += 1
					self.image.unlock()

					#use 'completely BLUE' as code for area of explosion
					mod = 5
					if self.cause.type == 'mine':
						mod = -4
					pygame.draw.circle(self.image, (0,0,255), (self.cause.rect.centerx - self.rect.x,self.cause.rect.centery - self.rect.y), round((self.cause.rect.width - mod) / 2), 0)
					#circle(Surface, color, pos, radius, width=0) -> Rect

				
				elif self.frame_counter == 1:
					self.dirty = 1
					

					#turn mallow brown-black
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = 0
					#Divide particles into two subsequent frames.
					while y < self.rect.height:
						x = 0
						while x <= self.rect.width - 1:
							choice = random.randrange(0,6,1)
							color = self.image.unmap_rgb(array[x,y])
							if color == (0,0,255):
								array[x,y] = options.GREEN
								if choice == 1:
									i = random.choice((1,2,3,4))
									if i == 1:
										self.particle_list1.append((x,y))
									elif i == 2:
										self.particle_list2.append((x,y))
									elif i == 3:
										self.particle_list3.append((x,y))
									else:
										self.particle_list4.append((x,y))

							
							x += 1
						y += 1
					self.image.unlock()

				elif self.frame_counter == 2:
					for particle in self.particle_list1:
						sprites.particle_generator.single_mallow_particles((self.rect.x + particle[0], self.rect.y + particle[1]),random.choice((options.LIGHT_PURPLE, options.PURPLE, self.ninja.color[2])), self.ninja, self.inverted_g, self.explosion_origin, None, None)
				elif self.frame_counter == 3:
					for particle in self.particle_list2:
						sprites.particle_generator.single_mallow_particles((self.rect.x + particle[0], self.rect.y + particle[1]),random.choice((options.LIGHT_PURPLE, options.PURPLE, self.ninja.color[2])), self.ninja, self.inverted_g, self.explosion_origin, None, None)
				elif self.frame_counter == 4:
					for particle in self.particle_list3:
						sprites.particle_generator.single_mallow_particles((self.rect.x + particle[0], self.rect.y + particle[1]),random.choice((options.LIGHT_PURPLE, options.PURPLE, self.ninja.color[2])), self.ninja, self.inverted_g, self.explosion_origin, None, None)
				elif self.frame_counter == 5:
					for particle in self.particle_list4:
						sprites.particle_generator.single_mallow_particles((self.rect.x + particle[0], self.rect.y + particle[1]),random.choice((options.LIGHT_PURPLE, options.PURPLE, self.ninja.color[2])), self.ninja, self.inverted_g, self.explosion_origin, None, None)

				elif self.frame_counter == 50:
					self.x_counter = self.rect.width - 1
					self.particle_list1 = []
					self.particle_list2 = []
					self.particle_list3 = []
					self.particle_list4 = []

				elif self.frame_counter > 50:
					self.dirty = 1
					self.image.lock()
					array = pygame.PixelArray(self.image)
					y = 0
					x = self.x_counter
					#decide how many of the particles to make.

		
					color_list = [options.BURNT, options.LIGHT_BURNT, options.DARK_BURNT, options.OUTLINE_BURNT, options.GREEN, (1,1,1)] #(1,1,1) is for mutant MOUTH. Almost black.
					if self.event_delay1 >= 2:	
						self.event_delay1 = 0
						if x >= 0:
							y = 0
							while y <= self.image.get_height() - 1:
								if self.rect.height == 48:
									choice = random.randrange(0,6,1)
								else:
									choice = random.randrange(0,2,1)
								color = self.image.unmap_rgb(array[x,y])
								if color in color_list:
									if color != options.GREEN:
										self.particle_list1.append((x,y))
								else:		
									array[x,y] = options.GREEN
									if choice == 1:
										sprites.particle_generator.single_dust_particles((self.rect.x + x, self.rect.y + y), random.choice((self.ninja.color[1],self.ninja.color[2])), self.ninja, self.inverted_g)
								y += 1
						self.x_counter -= 1
					self.event_delay1 += 1
					self.image.unlock()
				
				if self.frame_counter == 120:
					if len(self.particle_list1) > 0:
						leftx = None
						rightx = None
						topy = None
						bottomy = None
						for coord in self.particle_list1:
							if leftx == None or coord[0] < leftx:
								leftx = coord[0]
							if rightx == None or coord[0] > rightx:
								rightx = coord[0]
							if topy == None or coord[1] < topy:
								topy = coord[1]
							if bottomy == None or coord[1] > bottomy:
								bottomy = coord[1]
						temp_rect = pygame.Rect(leftx + self.rect.x, topy + self.rect.y, rightx - leftx + 1, bottomy - topy + 1)
						sprites.particle_generator.tile_death_particles(temp_rect, 'burnt', self.inverted_g, 0)
					self.reset()
				self.frame_counter += 1

			elif self.death_type == 'mine':
				if self.frame_counter == 0:
					self.explosion_origin = (self.cause.rect.centerx,self.cause.rect.centery)
					self.visible = True
					#turn mallow brown-black
					self.image.lock()
					array = pygame.PixelArray(self.image)
					x = 0
					y = 0
					while y <= self.image.get_height() - 1:
						x = 0
						while x <= self.image.get_width() - 1:
							color = self.image.unmap_rgb(array[x,y])
							
							#if color == options.LIGHT_PURPLE:
							#	array[x,y] = options.LIGHT_BURNT
							#elif color == options.PURPLE:
							#	array[x,y] = options.BURNT
							#elif color == options.DARK_PURPLE:
							#		array[x,y] = options.DARK_BURNT
							#elif color == options.OUTLINE_PURPLE:
							#		array[x,y] = options.OUTLINE_BURNT
							#elif color == self.ninja.color[0]:
							#		array[x,y] = options.GREY_LIST[0]
							#elif color == self.ninja.color[1]:
							#		array[x,y] = options.GREY_LIST[0]
							#elif color == self.ninja.color[2]:
							#		array[x,y] = options.GREY_LIST[0]
							#elif color == self.ninja.color[3]:
							#		array[x,y] = options.GREY_LIST[0]
							#elif color == options.FACE:
							#		array[x,y] = options.GREY_LIST[1]

							x += 1
						y += 1
					self.image.unlock()
				
					
					self.change_x = self.ninja.change_x / 2
					if self.inverted_g is False:
						self.change_y = -9
					else:
						self.change_y = 9

					#move sprite
					self.true_x = self.rect.x
					self.true_y = self.rect.y

				
				if self.frame_counter > 0 and self.event_trigger1 is False:
					#adjust change_y with gravity:
					self.dirty = 1
					if self.inverted_g is False:
						self.change_y += options.change_g
						if self.change_y > options.max_g:
							self.change_y = options.max_g
					else:
						self.change_y += options.change_g * -1
						if self.change_y < options.max_g * -1:
							self.change_y = options.max_g * -1

					#move sprite
					self.true_x += self.change_x
					self.true_y += self.change_y

					self.rect.x = round(self.true_x)
					self.rect.y = round(self.true_y)

					
					rect_top = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 12)
					rect_bottom = pygame.Rect(self.rect.left, self.rect.bottom - 12, self.rect.width, 12)
					rect_left = pygame.Rect(self.rect.left, self.rect.top + 2, 5, self.rect.height - 4)
					rect_right = pygame.Rect(self.rect.right - 5, self.rect.top + 2, 5, self.rect.height - 4)

					for tile in sprites.tile_list:
						if tile.type == 'tile' or tile.type == 'mallow':
							if tile.rect.colliderect(self.rect):
								
								if self.change_y < 0:
									if tile.bottom_rect.colliderect(rect_top):
										self.rect.top = tile.rect.bottom
										#self.change_y = 0
										self.true_y = self.rect.y
										self.event_trigger2 = True
										break
								else:
									if tile.top_rect.colliderect(rect_bottom):
										self.rect.bottom = tile.rect.top
										#self.change_y = 0
										self.true_y = self.rect.y
										self.event_trigger2 = True
										break

					rect_top = pygame.Rect(self.rect.left + 3, self.rect.top, self.rect.width - 6, 8)
					rect_bottom = pygame.Rect(self.rect.left + 3, self.rect.bottom - 6, self.rect.width - 6, 6)
					rect_left = pygame.Rect(self.rect.left, self.rect.top + 2, 5, self.rect.height - 4)
					rect_right = pygame.Rect(self.rect.right - 5, self.rect.top + 2, 5, self.rect.height - 4)

					#now fix x direction
					for tile in sprites.tile_list:
						if tile.type == 'tile' or tile.type == 'mallow':
							if tile.rect.colliderect(self.rect):
								if self.change_x > 0:
									self.rect.right = tile.rect.left
								else:
									self.rect.left = tile.rect.right
								self.change_x = 0
								self.true_x = self.rect.x
								break
								



					#if self.inverted_g is False:
					#	if self.change_y > 0:
					#		self.event_trigger1 = True
					#else:
					#	if self.change_y < 0:
					#		self.event_trigger1 = True

				if (self.event_trigger2 is True and self.frame_counter >= 2) or self.frame_counter > 4: #hit roof, separate completely!
					#12345
					self.visible = 1
					self.dirty = 1
					#sprites.particle_generator.mine_death_particles(self.rect, self.inverted_g, self.ninja)
					#y_dist = self.rect.height / 24
					
					self.image.lock()
					array = pygame.PixelArray(self.image)
					
					y = 0
					while y < self.rect.height - 1:
						x = random.choice((0,1,2,3))
						while x < self.rect.width - 1:
							color = self.image.unmap_rgb(array[x,y])
							if color != (0,255,0):
								x_speed = (x - 12) / 6
								if x_speed < 0:
									x_mod = (random.randrange(-20,5,1) / 20)# * (13 - abs(x - 12)) / 13 
								else:
									x_mod = (random.randrange(-5,20,1) / 20)# * (13 - abs(x - 12)) / 13 

								if self.change_y < 0:
									y_mod = random.randrange(-20,0,1) / 5
								else:
									y_mod = random.randrange(0,20,1) / 5


								sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + y), color, self.ninja, self.inverted_g, None, (x_speed + x_mod,(self.change_y / 2) + y_mod), None)
								
							x += random.choice((3,4,5))
						y += 1
								

						#if self.ninja.inverted_g is False:
						#	pygame.draw.rect(self.image, (0,255,0),(0, self.rect.height - (y_dist * self.event_delay1),self.rect.width,y_dist),0)
						#else:
						#	pygame.draw.rect(self.image, (0,255,0),(0, 0 + (y_dist * (self.event_delay1 - 1)),self.rect.width,y_dist),0)	
					
					#Reset after creating particles
					self.image.unlock()
					self.reset() 


				'''
				if self.frame_counter > 10 or self.event_trigger1 is True:
					self.event_delay1 += 1
					self.visible = 1
					self.dirty = 1
					#sprites.particle_generator.mine_death_particles(self.rect, self.inverted_g, self.ninja)
					y_dist = self.rect.height / 24
					
					array = pygame.PixelArray(self.image)
					
					i = 0
					attempt = 0
					while i < 4:
						color = (0,255,0)

						while color == (0,255,0) and attempt < 2:
							x = random.randrange(0,self.rect.width,1)
							if self.ninja.inverted_g is False:
								y = random.randrange(self.rect.height - (y_dist * self.event_delay1), self.rect.height - (y_dist * (self.event_delay1 - 1)),1)
							else:
								y = random.randrange(0 + (y_dist * (self.event_delay1 - 1)), 0 + (y_dist * self.event_delay1),1)
							color = self.image.unmap_rgb(array[x,y])
							attempt += 1
						if color != (0,255,0):
							sprites.particle_generator.single_mallow_particles((self.rect.x + x, self.rect.y + y), color, self.ninja, self.inverted_g, None, (self.change_x,self.change_y * 0.7), None)
							
						i += 1
						attempt = 0
							

					if self.ninja.inverted_g is False:
						pygame.draw.rect(self.image, (0,255,0),(0, self.rect.height - (y_dist * self.event_delay1),self.rect.width,y_dist),0)
					else:
						pygame.draw.rect(self.image, (0,255,0),(0, 0 + (y_dist * (self.event_delay1 - 1)),self.rect.width,y_dist),0)	

					if y_dist * self.event_delay1 >= self.rect.height:
						self.reset() 
					#pygame.draw.rect(self.image, (0,255,0), (0,self.cause_rect.y - self.rect.y,self.rect.width,self.cause_rect.height), 0)
					
					#if self.event_delay1 >= 3:
					#	self.reset()
					
				'''

				self.frame_counter += 1
			

			else: #handles all 'non-handled' causes.
				if self.frame_counter == 0:
					self.image_number = 0
					self.image = self.image_list[self.image_number]
					self.visible = True

				self.image = self.image_list[self.image_number]

				if self.frame_counter >= 8:
					self.image_number += 1
					self.frame_counter = 1

				self.dirty = 1
				self.frame_counter += 1

				if self.image_number >= len(self.image_list) - 1:
					self.reset()
				else:
					if self.ninja.inverted_g is True:
						i = self.image.copy()
						self.image = pygame.transform.flip(i,False,True)

					if self.ninja.item == 'metal suit': #Make Mallow Metallic
						i = self.image.copy()
						i.lock()
						array = pygame.PixelArray(i)
						x = 0
						y = 0
						while y <= i.get_height() - 1:
							x = 0
							while x <= i.get_width() - 1:
								color = self.image.unmap_rgb(array[x,y])
								if color == (255,245,246):
									array[x,y] = (210,204,243)
								elif color == (210,145,255):
									array[x,y] = (163,146,212)
								elif color == (97,24,148):
									array[x,y] = (97,84,118)

								x += 1
							y += 1
						i.unlock()
						self.image = i

	def reset(self):
		self.visible = 0
		self.image_number = 0
		self.frame_counter = 0
		self.dirty = 1
		self.active = False
		self.death_type = None
		self.cause = None
		self.cause_rect = None
		self.cause_subtype = None
		self.base_image = None
		self.y_counter = 0
		self.x_counter = 0
		self.x_counter_change = 0
		self.y_counter_change = 0
		self.event_delay1 = 0
		self.event_delay2 = 0
		self.event_trigger1 = False
		self.event_trigger2 = False
		self.particle_list1 = []
		self.particle_list2 = []
		self.particle_list3 = []
		self.particle_list4 = []
		self.explosion_origin = None
		self.image = pygame.Surface((24,48)) #reset height after rolling mines etc
		self.rect = self.image.get_rect()
		self.moving_platform = None
		sprites.active_sprite_list.change_layer(self, 0)

	def activate_death_sprite(self, rect, death_type, cause):

		if sprites.shake_handler.current_shake < 3:
			sprites.shake_handler.current_shake = 3
		

		self.active = True
		self.inverted_g = self.ninja.inverted_g
		
		if options.death_animations == 'Off':
			self.death_type = None
		else:
			self.death_type = death_type
		
		self.cause = cause
		self.dirty = 1
		self.visible = 1
		self.ninja_rect = rect
		bottom = self.ninja_rect.bottom
		top = self.ninja_rect.top
		centerx = self.ninja_rect.centerx
		if self.cause != None:
			#following 2 only needed until all death types are logged.
			self.rect.centerx = centerx
			if self.inverted_g is False:
				self.rect.bottom = self.ninja_rect.bottom
			else:
				self.rect.top = self.ninja_rect.top
			

			self.cause_rect = self.cause.rect #pygame.Rect(self.cause.rect.x, self.cause.rect.y, self.cause.rect.width, self.cause.rect.height)
			if death_type == 'spikes':
				if self.ninja.rect.height == 48:
					self.base_image = self.image_list[0].copy()
					if self.ninja.inverted_g is True:
						self.base_image = pygame.transform.flip(self.base_image,False,True)
				else:
					self.base_image = self.ninja.image.copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom

			elif death_type == 'fire':
				if self.ninja.rect.height == 48:
					self.base_image = self.image_list[0].copy()
					if self.ninja.inverted_g is True:
						self.base_image = pygame.transform.flip(self.base_image,False,True)
				else:
					self.base_image = self.ninja.image.copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom

			elif death_type == 'laser':
				if self.ninja.rect.height == 48:
					self.base_image = self.image_list[0].copy()
					if self.ninja.inverted_g is True:
						self.base_image = pygame.transform.flip(self.base_image,False,True)
				else:
					self.base_image = self.ninja.image.copy()
				if self.cause.change_x != 0:
					self.cause_subtype = 'horizontal'
				else:
					self.cause_subtype = 'vertical'
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom
			elif self.death_type == 'metal suit':
				self.base_image = self.ninja.image.copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom
			
			elif self.death_type == 'side boulder':
				#ninja on left
				if self.ninja.rect.height == 24:
					self.base_image = self.ninja.image.copy()
				elif self.ninja.rect.centerx < self.cause.rect.centerx:
					if self.ninja.direction == 'right':
						self.base_image = self.ninja.knockback_left[0].copy()
					else:
						self.base_image = self.ninja.knockforward_left[0].copy()

				else: #ninja on right
					if self.ninja.direction == 'right':
						self.base_image = self.ninja.knockforward_right[0].copy()
					else:
						self.base_image = self.ninja.knockback_right[0].copy()

				if self.ninja.inverted_g is False:
					self.rect.bottom = self.ninja.rect.bottom
				else:
					self.rect.top = self.ninja.rect.top
				self.rect.x = self.ninja.rect.x
				if self.inverted_g is True:
					i = self.image.copy()
					self.image = pygame.transform.flip(i,False,True)

			elif self.death_type == 'volt':
				self.base_image = self.volt_image_list[0].copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				if self.ninja.inverted_g is False:
					self.rect.bottom = self.ninja.rect.bottom
				else:
					self.rect.top = self.ninja.rect.top
				self.rect.x = self.ninja.rect.x
				if self.inverted_g is True:
					i = self.image.copy()
					self.image = pygame.transform.flip(i,False,True)
			elif death_type == 'explosion':
				if self.ninja.rect.height == 48:
					self.base_image = self.image_list[0].copy()
					if self.ninja.inverted_g is True:
						self.base_image = pygame.transform.flip(self.base_image,False,True)
				else:
					self.base_image = self.ninja.image.copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom

			elif death_type == 'saw':
				'''
				if self.ninja.status == 'frozen':
					self.base_image = self.ninja.image.copy()
					if self.ninja.rect.height == 48:
						self.base_image.blit(self.ninja.ice_cube.ice_cube_big, (0,0))
					else:
						self.base_image.blit(self.ninja.ice_cube.ice_cube_small, (0,0))
				else:
				'''
				if self.ninja.rect.height == 48:
						self.base_image = self.image_list[0].copy()
						if self.ninja.inverted_g is True:
							self.base_image = pygame.transform.flip(self.base_image,False,True)
				else:
						self.base_image = self.ninja.image.copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom

			elif death_type == 'mine':
				if self.ninja.rect.height == 48:
					self.base_image = self.image_list[0].copy()
					if self.ninja.inverted_g is True:
						self.base_image = pygame.transform.flip(self.base_image,False,True)
				else:
					#self.base_image = self.ninja.image.copy()
					self.base_image = self.ninja.duck_neutral[1].copy()
				self.image = self.base_image
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.bottom = bottom

		#This will let moving platforms carry SOME death types along if the ninja was planted on one in death.
		if death_type in ('fire', 'laser', 'volt', 'explosion', None):
			#tile_list = sprites.quadrant_handler.get_quadrant(self.ninja)
			for tile in sprites.tile_list:
				if tile.type == 'platform':
					if tile.subtype == 'moving platform':
						if self.ninja.inverted_g is False:
							sticky_rect = pygame.Rect(tile.rect.x, tile.rect.top - 2, tile.rect.width,4)
						else:
							sticky_rect = pygame.Rect(tile.rect.x, tile.rect.bottom - 2, tile.rect.width,4)

						if self.ninja.rect_bottom.colliderect(sticky_rect):
							self.moving_platform = tile
							self.platform_xmod = self.ninja.rect.centerx - self.moving_platform.rect.centerx
							break

		

class Name_Bar_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.target = self.ninja

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 85)

		self.visible = 0
		self.dirty = 1

	def update(self):
		if self.visible == 1:
			if self.ninja.spawn_sprite.status == 'build_up':
				self.target = self.ninja.spawn_sprite
			else:
				self.target = self.ninja

			self.rect.bottom = self.target.rect.top
			self.rect.centerx = self.target.rect.centerx
			
			if self.rect.top < 0:
				self.rect.top = self.target.rect.bottom
				self.rect.centerx = self.target.rect.centerx
			self.dirty = 1

	def update_name(self):
		if self.ninja.profile == 'Guest':
			name = self.ninja.name
		else:
			name = self.ninja.profile

		text = sprites.font_16.render(name, 0,(self.ninja.color[2]))
		self.image = pygame.Surface((text.get_width() + 2, text.get_height() + 2))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)
		self.image.blit(text,(1,1))
		self.rect = self.image.get_rect()

		pixel_checks = ((-1,0),(-1,-1),(-1,1),(0,-1),(0,1),(1,0),(1,-1),(1,1))
		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.rect.height - 1:
			x = 0
			while x <= self.rect.width - 1:
				color = self.image.unmap_rgb(array[x,y])
				if color == self.ninja.color[2]: #find out if current pixel is colored.
					#if it is, check pixels around it. If they aren't colored, make them black.
					for pixel_check in pixel_checks:
						temp_x = x + pixel_check[0]
						temp_y = y + pixel_check[1]
						try:
							color = self.image.unmap_rgb(array[temp_x,temp_y])
							if color != self.ninja.color[2]:
								array[temp_x,temp_y] = (options.BLACK)
						except IndexError:
							pass
						
				x += 1
			y += 1
		array.close()
		self.image.unlock()
		self.reset()

	def activate(self):
		self.visible = 1
		if self.ninja.spawn_sprite.status == 'build_up':
			self.target = self.ninja.spawn_sprite
		else:
			self.target = self.ninja

		self.rect.bottom = self.ninja.rect.top
		self.rect.centerx = self.ninja.rect.centerx
		

	def reset(self):
		self.visible = 0
		self.dirty = 1

class Choice_Bar_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 90)

		self.visible = 0
		self.dirty = 1

	def update(self):
		if self.visible == 1:
			self.rect.bottom = self.ninja.rect.top
			self.rect.centerx = self.ninja.rect.centerx
			
			if self.rect.top < 0:
				self.rect.top = self.ninja.rect.bottom
				self.rect.centerx = self.ninja.rect.centerx
			self.dirty = 1

	def update_name(self):
		if self.ninja.profile == 'Guest':
			name = self.ninja.name
		else:
			name = self.ninja.profile

		text = sprites.font_16.render(name, 0,options.WHITE)
		self.image = pygame.Surface((76, text.get_height() + 4)) #76 tested. Fits max 9-character name nicely.
		self.image.fill(self.ninja.color[2])
		self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()
		self.image.blit(text,((self.image.get_width() / 2) - (text.get_width() / 2),3))
		
		
		self.base_image = self.image.copy()
		self.right_image = pygame.transform.rotate(self.base_image, -90)
		self.left_image = pygame.transform.rotate(self.base_image, 90)

		for image in (self.base_image,self.right_image,self.left_image):
			#Outline shadows of box
			width = image.get_width()
			height = image.get_height()
			pygame.draw.line(image, self.ninja.color[3], (0, 0), (width - 2, 0), 1)
			pygame.draw.line(image, self.ninja.color[1], (width - 1, height - 1), (width - 1, 1), 1)
			pygame.draw.line(image, self.ninja.color[1], (width - 1, height - 1), (1, height - 1), 1)
			pygame.draw.line(image, self.ninja.color[3], (0, 0), (0, height - 2), 1)

		self.reset()
		

	def activate(self, orientation, centerx, centery):
		if orientation == 'normal':
			self.image = self.base_image
		elif orientation == 'right':
			self.image = self.right_image
		elif orientation == 'left':
			self.image = self.left_image
		self.rect = self.image.get_rect()

		self.visible = 1
		self.rect.centery = centery
		self.rect.centerx = centerx
		self.dirty = 1
		
	def reset(self):
		self.visible = 0
		self.dirty = 1

class Score_Bar_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.name_bar = self.ninja.name_bar

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 85)

		self.visible = 0
		self.dirty = 1

	def update(self):
		if self.visible == 1:
			if self.name_bar.rect.centery < self.ninja.rect.centery:
				self.rect.bottom = self.name_bar.rect.top
				self.rect.centerx = self.name_bar.rect.centerx
			else:
				self.rect.top = self.name_bar.rect.bottom
				self.rect.centerx = self.name_bar.rect.centerx
			self.dirty = 1

	def update_score(self):
		if options.versus_mode == "Classic":
			if self.ninja.current_wins == 1:
				score = str(self.ninja.current_wins) + ' Pt'
			else:
				score = str(self.ninja.current_wins) + ' Pts'
		else:
			if self.ninja.current_VP == 1:
				score = str(self.ninja.current_VP) + ' Pt'
			else:
				score = str(self.ninja.current_VP) + ' Pts'

		text = sprites.font_12.render(score, 0,(self.ninja.color[2]))
		self.image = pygame.Surface((text.get_width() + 2, text.get_height() + 2))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)
		self.image.blit(text,(1,1))
		self.rect = self.image.get_rect()

		pixel_checks = ((-1,0),(-1,-1),(-1,1),(0,-1),(0,1),(1,0),(1,-1),(1,1))
		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.rect.height - 1:
			x = 0
			while x <= self.rect.width - 1:
				color = self.image.unmap_rgb(array[x,y])
				if color == self.ninja.color[2]: #find out if current pixel is colored.
					#if it is, check pixels around it. If they aren't colored, make them black.
					for pixel_check in pixel_checks:
						temp_x = x + pixel_check[0]
						temp_y = y + pixel_check[1]
						try:
							color = self.image.unmap_rgb(array[temp_x,temp_y])
							if color != self.ninja.color[2]:
								array[temp_x,temp_y] = (options.BLACK)
						except IndexError:
							pass
						
				x += 1
			y += 1

		array.close()
		self.image.unlock()
		self.reset()

	def activate(self):
		pass
		#self.visible = 1
		#self.rect.bottom = self.name_bar.rect.top
		#self.rect.centerx = self.name_bar.rect.centerx
		

	def reset(self):
		self.visible = 0
		self.dirty = 1

class Stock_Bar_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.name_bar = self.ninja.name_bar

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 85)

		self.visible = 0
		self.dirty = 1

		self.stock_timer = 0
		self.moving_platform = None
	def update(self):
		if self.visible == 1:
			if self.name_bar.visible == 1:
				if self.name_bar.rect.centery < self.ninja.rect.centery:
					self.rect.bottom = self.name_bar.rect.top
					self.rect.centerx = self.name_bar.rect.centerx
				else:
					self.rect.top = self.name_bar.rect.bottom
					self.rect.centerx = self.name_bar.rect.centerx

			else:
				if self.moving_platform != None:
					if self.ninja.spawn_sprite.inverted_g is False:
						self.rect.top = self.moving_platform.rect.top
					else:
						self.rect.bottom = self.moving_platform.rect.bottom
					self.rect.centerx = self.moving_platform.rect.centerx

			self.dirty = 1

			#keeps it a live a little longer
			if self.stock_timer > 0:
				self.stock_timer -= 1
				if self.stock_timer == 0:
					self.reset()

	def update_score(self):
		if options.versus_mode == 'Practice':
			score = ' x 99'
		else:
			score = ' x ' + str(self.ninja.lives)

		text = sprites.font_12.render(score, 0,(self.ninja.color[2]))
		self.image = pygame.Surface((text.get_width() + 16, text.get_height() + 2))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)
		self.image.blit(text,(15,1))
		self.rect = self.image.get_rect()

		pixel_checks = ((-1,0),(-1,-1),(-1,1),(0,-1),(0,1),(1,0),(1,-1),(1,1))
		self.image.lock()
		array = pygame.PixelArray(self.image)
		x = 0
		y = 0
		while y <= self.rect.height - 1:
			x = 0
			while x <= self.rect.width - 1:
				color = self.image.unmap_rgb(array[x,y])
				if color == self.ninja.color[2]: #find out if current pixel is colored.
					#if it is, check pixels around it. If they aren't colored, make them black.
					for pixel_check in pixel_checks:
						temp_x = x + pixel_check[0]
						temp_y = y + pixel_check[1]
						try:
							color = self.image.unmap_rgb(array[temp_x,temp_y])
							if color != self.ninja.color[2]:
								array[temp_x,temp_y] = (options.BLACK)
						except IndexError:
							pass
						
				x += 1
			y += 1

		array.close()
		self.image.unlock()
		self.reset()

		self.image.blit(self.ninja.stock_image, (1,0))


	def activate(self, source = 'name bar'):
		self.visible = 1
		if source == 'name bar':
			self.rect.bottom = self.name_bar.rect.top
			self.rect.centerx = self.name_bar.rect.centerx
		elif source == 'stock':
			if self.ninja.spawn_sprite.inverted_g is False:
				self.rect.top = self.ninja.spawn_sprite.rect.bottom
			else:
				self.rect.bottom = self.ninja.spawn_sprite.rect.top
			self.rect.centerx = self.ninja.spawn_sprite.rect.centerx

			self.stock_timer = 90

			if self.ninja.spawn_sprite.moving_platform != None:
				self.moving_platform = self.ninja.spawn_sprite.moving_platform
		

	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.stock_timer = 0
		self.moving_platform = None

class Text_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 85)

		self.frame_counter = 0
		self.visible = 0
		self.dirty = 1

	def update(self):
		if self.frame_counter > 0:
			self.frame_counter -= 1
			if self.frame_counter == 0:
				self.reset()

	def activate(self, text, color, centerxy, lifespan):
		self.image = menus.font_16.render(text, 0,color)
		self.rect = self.image.get_rect()
		self.rect.center = centerxy

		self.frame_counter = lifespan
			
		self.visible = 1


	def reset(self):
		self.visible = 0
		self.dirty = 1


class Controls_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image = pygame.Surface((130,55))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0


		self.jump_text = menus.font_16.render(" B : Jump/Select", 0,(options.WHITE))
		self.roll_text = menus.font_16.render(" B : Roll/Back", 0,(options.WHITE))
		self.item_text = menus.font_16.render(" B : Item", 0,(options.WHITE))

		self.image.blit(self.jump_text, (0,1))
		self.image.blit(self.roll_text, (0,19))
		self.image.blit(self.item_text, (0,37))

		self.little_base_image = self.image.copy()

		other_image = pygame.Surface((130,73))
		other_image.fill(options.GREEN)
		other_image.set_colorkey(options.GREEN)
		other_image.blit(self.jump_text, (0,1 + 18))
		other_image.blit(self.roll_text, (0,19 + 18))
		other_image.blit(self.item_text, (0,37 + 18))
		self.big_base_image = other_image.copy()


		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 90)

		self.visible = 0
		self.dirty = 1

	def update(self):
		pass
		#self.dirty = 1
		#self.visible = 1

	def update_buttons(self):
		#try:
		oldx = self.rect.x
		oldy = self.rect.y
		if options.game_state == 'pause':
			if self.ninja.profile == 'Guest':
				name = self.ninja.name
			else:
				name = self.ninja.profile

			text = menus.font_16.render(name + ':', 0,(self.ninja.color[2]))
			
			self.image = self.big_base_image.copy()
			self.rect = self.image.get_rect()

			self.image.blit(text, (4,1))
			mod = 18

		else:
			self.image = self.little_base_image.copy()
			self.rect = self.image.get_rect()
			mod = 0
		
		if (options.control_preferences['player1'] == 'keyboard' and self.ninja == sprites.player1) or (options.control_preferences['player2'] == 'keyboard' and self.ninja == sprites.player2):
			button = controls.input_handler.button_keyboard_z
			self.image.blit(button, (3,0 + mod))

			button = controls.input_handler.button_keyboard_x
			self.image.blit(button, (3,18 + mod))

			button = controls.input_handler.button_keyboard_c
			self.image.blit(button, (3,36 + mod))

		else: #uses gamepad
			button = self.ninja.gamepad_layout['button_jump_image']
			self.image.blit(button, (3,0 + mod))

			button = self.ninja.gamepad_layout['button_roll_image']
			self.image.blit(button, (3,18 + mod))

			button = self.ninja.gamepad_layout['button_item_image']
			self.image.blit(button, (3,36 + mod))

		self.dirty = 1
		self.rect.x = oldx
		self.rect.y = oldy
		#except:
		#	pass

	def activate(self, xy):
		self.update_buttons()
		self.visible = 1
		self.dirty = 1
		self.rect.x = xy[0]
		self.rect.y = xy[1]
		
		

	def reset(self):
		self.visible = 0
		self.dirty = 1

class Award_Screen_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.background = Award_Screen_Background_Sprite(self.ninja)

		self.image = pygame.Surface((130,245))
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, -1)

		self.visible = 0
		self.dirty = 1

	def update(self):
		pass

	def activate(self):
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, -6)
		self.visible = 1
		self.dirty = 1

	def reset(self):
		sprites.active_sprite_list.remove(self) #this group actually draws the sprites
		self.visible = 0
		self.dirty = 1

class Award_Screen_Background_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image = pygame.Surface((130,245))
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, -1)

		self.visible = 0
		self.dirty = 1

	def update(self):
		pass

	def activate(self):
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, -7)
		self.visible = 1
		self.dirty = 1

	def reset(self):
		sprites.active_sprite_list.remove(self) #this group actually draws the sprites
		self.visible = 0
		self.dirty = 1



class Feather_Effect_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja, number):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.number = number #holds number of sprite. Each ninja has an effect 1,2,3,4.

		self.image_list = []
		image = self.ninja.spritesheet.getImage(356, 196, 17, 7)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(356, 204, 17, 7)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(356, 212, 17, 7)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(356, 204, 17, 7)
		self.image_list.append(image)

		self.inverted_image_list = []
		image = self.ninja.spritesheet.getImage(356, 196, 17, 7)
		i = pygame.transform.flip(image,False,True)
		self.inverted_image_list.append(i)
		image = self.ninja.spritesheet.getImage(356, 204, 17, 7)
		i = pygame.transform.flip(image,False,True)
		self.inverted_image_list.append(i)
		image = self.ninja.spritesheet.getImage(356, 212, 17, 7)
		i = pygame.transform.flip(image,False,True)
		self.inverted_image_list.append(i)
		image = self.ninja.spritesheet.getImage(356, 204, 17, 7)
		i = pygame.transform.flip(image,False,True)
		self.inverted_image_list.append(i)

		self.image_number = random.choice((0,1,2,3))
		self.frame_counter = 0

		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)
		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.status = 'idle'
		self.inverted_g = False
		self.timer = 0
		self.centerpoint = 0
		self.true_rect_y = 0

	def update(self):
		if self.status == 'idle':
			pass

		elif self.status == 'active':
			self.dirty = 1
			self.frame_counter += 1
			self.timer += 1
			if self.frame_counter >= 14:
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number > len(self.image_list) - 1:
					self.image_number = 0
					if self.timer > 60:
						sprites.particle_generator.snow_particles(self.rect, self.inverted_g, 4)
						self.reset()

			if self.image_number in (0,2):
				if self.inverted_g is False:
					self.image = self.image_list[self.image_number]
					self.true_rect_y += 0.375
				else:
					self.image = self.inverted_image_list[self.image_number]
					self.true_rect_y -= 0.375
			else:
				if self.inverted_g is False:
					self.image = self.image_list[self.image_number]
					self.true_rect_y += 0.25
				else:
					self.image = self.inverted_image_list[self.image_number]
					self.true_rect_y -= 0.25
			self.rect.y = round(self.true_rect_y)




			if self.image_number in (0,2):
				self.rect.centerx == self.centerpoint
			elif self.image_number == 1:
				self.rect.centerx = self.centerpoint - 3
			elif self.image_number == 3:
				self.rect.centerx = self.centerpoint + 3



	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.status = 'idle'

	def activate(self):

		self.visible = 1
		self.dirty = 1
		self.status = 'active'
		self.inverted_g = self.ninja.inverted_g
		self.timer = 0
		self.image_number = random.choice((0,1,2,3))
		x_var = random.randrange(-16,16,1)
		y_var = random.randrange(-20,0,1)
		self.rect.centerx = self.ninja.rect.centerx + x_var
		if self.ninja.inverted_g is False:
			self.rect.top = self.ninja.rect.bottom + y_var
		else:
			self.rect.bottom = self.ninja.rect.top - y_var
		self.centerpoint = self.rect.centerx
		self.true_rect_y = self.rect.y

class Item_Effect_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja, number):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.number = number #holds number of sprite. Each ninja has an effect 0,1,2.

		self.image_dict = {0: None, 1: None, 2: None}
		self.image_number = 0
		self.frame_counter = 0

		self.image = pygame.Surface((0,0))
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		i = self.number * -1
		sprites.active_sprite_list.change_layer(self, i)

		self.alpha = (4 - self.number) * 50

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.store_switch = False

	def update(self):
		if self.ninja.item == 'shoes' and self.ninja in sprites.ninja_list and self.ninja.status != 'frozen':
			self.store_images(self.ninja.image, self.ninja.rect.centerx, self.ninja.rect.centery)
			if self.ninja.change_x == 0:
				self.visible = 0
				self.dirty = 1
			else:
				if self.store_switch is True:
					self.store_switch = False
					if self.image_dict[self.number] != None:
						self.image = self.image_dict[self.number][0]
						if options.transparency == 'on':
							self.image = self.image.copy()
							self.image.set_alpha(self.alpha)
						self.rect = self.image.get_rect()
						self.rect.centerx = self.image_dict[self.number][1]
						self.rect.centery = self.image_dict[self.number][2]
						self.visible = 1
						self.dirty = 1
				else:

					self.store_switch = True
		else:
			self.reset()

		

	def reset(self):
		self.visible = 0
		self.image_number = 0
		self.frame_counter = 0
		self.dirty = 1
		self.image_dict = {0: None, 1: None, 2: None}

	def store_images(self, image, centerx, centery):
		#shift the dict entries.
		self.image_dict[2] = self.image_dict[1]
		self.image_dict[1] = self.image_dict[0]

		#if self.ninja.inverted_g is True:
		#	image = pygame.transform.flip(image, False, True)

		self.image_dict[0] = (image, centerx, centery)

class Projectile_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja, number):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.number = number #holds number of sprite. Each ninja has an effect 0,1,2.
		self.type = 'laser'
		self.portal_delay = 0


		#Needed to help sort online play.
		self.online_ID = self.ninja.item_key_number
		self.ninja.item_dict[self.online_ID] = self
		self.ninja.item_key_number += 1

		self.predictive_collision_list = [] #holds list of ninjas scheduled to die next frame. They must die to keep games in line.



		self.image_number = 0
		self.frame_counter = 0

		self.image_list = []

		self.laser_image = self.ninja.spritesheet.getImage(275, 246, 24, 3)
		self.image_list.append(self.laser_image)

		image = self.laser_image.copy()
		self.laser_image_vertical = pygame.transform.rotate(image, 90)
		self.image_list.append(self.laser_image_vertical)

		self.laser_wall_right_1 = self.ninja.spritesheet.getImage(308, 246, 9, 9)
		self.image_list.append(self.laser_wall_right_1)

		self.laser_wall_right_2 = self.ninja.spritesheet.getImage(318, 246, 9, 9)
		self.image_list.append(self.laser_wall_right_2)
		
		self.laser_wall_left_1 = pygame.transform.flip(self.laser_wall_right_1.copy(), True, False)
		self.image_list.append(self.laser_wall_left_1)

		self.laser_wall_left_2 = pygame.transform.flip(self.laser_wall_right_2.copy(), True, False)
		self.image_list.append(self.laser_wall_left_2)

		image = self.laser_wall_left_1.copy()
		self.laser_wall_up_1 = pygame.transform.rotate(image, 90)
		self.image_list.append(self.laser_wall_up_1)

		image = self.laser_wall_left_2.copy()
		self.laser_wall_up_2 = pygame.transform.rotate(image, 90)
		self.image_list.append(self.laser_wall_up_2)

		image = self.laser_wall_left_1.copy()
		self.laser_wall_down_1 = pygame.transform.rotate(image, -90)
		self.image_list.append(self.laser_wall_down_1)

		image = self.laser_wall_left_2.copy()
		self.laser_wall_down_2 = pygame.transform.rotate(image, -90)
		self.image_list.append(self.laser_wall_down_2)


		self.ninja.big_image_list.append(self.image_list)
		


		self.image = self.laser_image
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.fire = False
		self.laser_speed = 13

		self.status = 'laser'
		self.frame_counter = 0
		self.timer = 0

		self.inverted_g = False

		self.change_x = 0
		self.change_y = 0
		self.true_x = 0
		self.true_y = 0
		self.kill_count = 0 #tracks multiple kills from one shot

	def update(self):
		if self.portal_delay > 0:
			self.portal_delay -= 1


		if self.fire is True:

			#kill ninjas scheduled to die. Only affects online things. Effort to keep things more aligned.
			for ninja in self.predictive_collision_list:
				if ninja.death_sprite.active is False:
					ninja.activate_death_sprite('laser', self)
					self.collect_stats(ninja) #collect/assign stats for kill

			self.predictive_collision_list = []

			self.boundary_check()
			if self.status == 'laser':
				self.visible = 1
				self.dirty = 1

				self.true_x += self.change_x
				self.true_y += self.change_y

				self.rect.x = round(self.true_x)
				self.rect.y = round(self.true_y)

				self.collision_check()

				for ninja in sprites.ninja_list:
					if ninja.shield_sprite.active is True:
						ninja.shield_sprite.collision_check(self)

				self.timer += 1
				if self.timer > 300: #fires for 5 seconds
					self.reset()
					self.timer = 0

			elif self.status == 'wall':
				self.visible = 1
				self.dirty = 1
				if self.frame_counter < 2:

					self.collision_check()
				if self.change_x > 0:
					if self.frame_counter == 0:
						self.image = self.laser_wall_right_1
					elif self.frame_counter ==2:
						self.image = self.laser_wall_right_2
					elif self.frame_counter == 4:
						self.visible = 0
					elif self.frame_counter == 5:
						self.reset()
				if self.change_x < 0:
					if self.frame_counter == 0:
						self.image = self.laser_wall_left_1
					elif self.frame_counter ==2:
						self.image = self.laser_wall_left_2
					elif self.frame_counter == 4:
						self.visible = 0
					elif self.frame_counter == 5:
						self.reset()
				if self.change_y < 0:
					if self.frame_counter == 0:
						self.image = self.laser_wall_down_1
					elif self.frame_counter ==2:
						self.image = self.laser_wall_down_2
					elif self.frame_counter == 4:
						self.visible = 0
					elif self.frame_counter == 5:
						self.reset()
				if self.change_y > 0:
					if self.frame_counter == 0:
						self.image = self.laser_wall_up_1
					elif self.frame_counter ==2:
						self.image = self.laser_wall_up_2
					elif self.frame_counter == 4:
						self.visible = 0
					elif self.frame_counter == 5:
						self.reset()
				self.frame_counter += 1

		else:
			self.reset()

		self.online_collision_list = []


	def boundary_check(self):
		if self.ninja.loop_physics is True:
			if self.rect.right < 0 and self.change_x < 0:
				self.rect.left = sprites.size[0]
				self.true_x = self.rect.x

			if self.rect.left > sprites.size[0] and self.change_x > 0:
				self.rect.right = 0
				self.true_x = self.rect.x


	def update_collision_rect(self):
		if self.change_x != 0: #horizontal
			self.collision_rect = pygame.Rect(self.rect.x,self.rect.centery,self.rect.width,1)
		elif self.change_y != 0: #vertical
			self.collision_rect = pygame.Rect(self.rect.centerx,self.rect.y,1,self.rect.height)

	def collision_check(self):
		self.update_collision_rect()

		laser = True

		#Make sure not on top of portal
		portal = False
		for item in sprites.active_items:
			if item.type == 'portal_gun_portal':
				if self.collision_rect.colliderect(item.collision_rect):
					if len(item.portal_gun.active_portal_list) == 2: #portal to teleport to!
						portal = True
						break


		if self.portal_delay == 0 and portal is False:
			for tile in sprites.tile_list:
				if tile.type == 'tile' or tile.type == 'mallow_wall':
					if self.rect.colliderect(tile.rect):
						self.status = 'wall'
						laser = False
						old_y = self.rect.centery
						old_x = self.rect.centerx
						if self.change_x > 0:
							self.image = self.laser_wall_right_1
							self.rect = self.image.get_rect()
							self.rect.x = tile.rect.x - self.rect.width
							self.rect.centery = old_y
							sprites.particle_generator.laser_particles((self.rect.right,self.rect.centery), 'horizontal', self.ninja.color[2])
						elif self.change_x < 0:
							self.image = self.laser_wall_left_1
							self.rect = self.image.get_rect()
							self.rect.left = tile.rect.right
							self.rect.centery = old_y
							sprites.particle_generator.laser_particles((self.rect.left,self.rect.centery), 'horizontal', self.ninja.color[2])

						elif self.change_y > 0:
							self.image = self.laser_wall_down_1
							self.rect = self.image.get_rect()
							self.rect.bottom = tile.rect.top
							self.rect.centerx = old_x
							sprites.particle_generator.laser_particles((self.rect.centerx,self.rect.bottom), 'vertical', self.ninja.color[2])
						elif self.change_y < 0:
							self.image = self.laser_wall_up_1
							self.rect = self.image.get_rect()
							self.rect.top = tile.rect.bottom
							self.rect.centerx = old_x
							sprites.particle_generator.laser_particles((self.rect.centerx,self.rect.top), 'vertical', self.ninja.color[2])

						self.true_x = self.rect.x
						self.true_y = self.rect.y
						break

		if laser is True:
			for ninja in sprites.ninja_list:
				if ninja.inverted_g is False:
					ninja_rect = pygame.Rect(ninja.rect.left + 4, ninja.rect.top + 5, ninja.rect.width - 8, ninja.rect.height - 5)
				else:
					ninja_rect = pygame.Rect(ninja.rect.left + 4, ninja.rect.top, ninja.rect.width - 8, ninja.rect.height - 5)
				if ninja != self.ninja:
					if self.collision_rect.colliderect(ninja_rect):
						if ninja.shield_sprite.active is False:
							#ninja.lose()
							if 1 == 1:
								ninja.activate_death_sprite('laser', self)
								
					 

								if options.game_state == 'level':
									try:
										self.ninja.stats_laser_kills += 1
										if self.ninja.color == ninja.color:
											self.ninja.stats_ally_item_kill += 1
										else:
											self.ninja.score_item_kills()
										self.kill_count += 1
										if self.kill_count == 2:
											self.ninja.stats_laser_double_kills += 1
										elif self.kill_count == 3:
											self.ninja.stats_laser_triple_kills += 1
										if self.change_y != 0: #vertical laser!
											self.ninja.stats_laser_vertical_kills += 1
									except AttributeError:
										print(5)
										pass

					

				if ninja == self.ninja: #can hit self after a couple of frames
					if self.timer >= 2:
						if self.collision_rect.colliderect(ninja_rect):
							if ninja.shield_sprite.active is False:
								if 1 == 1:
									#ninja.lose()
									ninja.activate_death_sprite('laser', self)
									if options.game_state == 'level':
										self.ninja.stats_laser_suicides += 1



				


				for item in sprites.active_items:
					if item != self:
						if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
							if item.status != '' and item.status != 'explode':
								if item.rect.colliderect(self.rect):
									item.explode()


				for enemy in sprites.enemy_list:
						if 'laser' in enemy.death_list:
							
							if (self.ninja != enemy and self.ninja not in enemy.subsprite_list) or self.frame_counter >= 2:
								if self.rect.colliderect(enemy.collision_dict['death']):
									enemy.destroy()

	def collect_stats(self, ninja): #used to collect stats for online kills
		if options.game_state == 'level':
			if ninja == self.ninja:
				self.ninja.stats_laser_suicides += 1
			else:
				try:
					self.ninja.stats_laser_kills += 1
					if self.ninja.color == ninja.color:
						self.ninja.stats_ally_item_kill += 1
					else:
						self.ninja.score_item_kills()
					self.kill_count += 1
					if self.kill_count == 2:
						self.ninja.stats_laser_double_kills += 1
					elif self.kill_count == 3:
						self.ninja.stats_laser_triple_kills += 1
					if self.change_y != 0: #vertical laser!
						self.ninja.stats_laser_vertical_kills += 1
				except AttributeError:
					print(5)
					pass
								

	def reset(self):
		self.online_collision_list = []
		self.kill_count = 0
		self.timer = 0
		self.visible = 0
		self.image_number = 0
		self.image = self.laser_image
		self.rect = self.image.get_rect()
		self.status = 'laser'
		self.frame_counter = 0
		self.dirty = 1
		self.fire = False
		self.change_x = 0
		self.change_y = 0
		try:
			sprites.active_items.remove(self)
		except ValueError:
			pass

	def attempt_fire(self):
			if self.fire is False:
				self.fire = True
				self.fire_laser()
				sounds.mixer.laser.play()
			else:
				if self == self.ninja.projectile1:
					self.ninja.projectile2.attempt_fire()
				elif self == self.ninja.projectile2:
					self.ninja.projectile3.attempt_fire()
				elif self == self.ninja.projectile3:
					self.ninja.projectile4.attempt_fire()
				elif self == self.ninja.projectile4:
					self.ninja.projectile5.attempt_fire()
				elif self == self.ninja.projectile5:
					self.ninja.projectile6.attempt_fire()

	def fire_laser(self, sensor_laser = False):
		self.kill_count = 0 #here, redundant from reset(), but allows online play stats to work.

		try:
			self.ninja.stats_laser_fired += 1
		except AttributeError:
			pass

		sprites.active_items.append(self)

		if self.ninja.direction == 'right':
			self.rect.left = self.ninja.rect.right - 28
			if self.ninja.inverted_g is False:
				self.rect.centery = self.ninja.rect.bottom - 21
			else:
				self.rect.centery = self.ninja.rect.top + 21
			self.change_x = self.laser_speed

		elif self.ninja.direction == 'left':
			self.rect.right = self.ninja.rect.left + 28
			if self.ninja.inverted_g is False:
				self.rect.centery = self.ninja.rect.bottom - 21
			else:
				self.rect.centery = self.ninja.rect.top + 21
			self.change_x = self.laser_speed * -1

		self.true_x = self.rect.x
		self.true_y = self.rect.y



	def fire_sensor_laser(self,direction):
		self.fire = True
		self.fire_laser(sensor_laser = True)
		sounds.mixer.laser.play()
		
		if direction == 'right':
			self.rect.left = self.ninja.rect.left - 12
			self.rect.centery = self.ninja.rect.centery
			self.change_x = self.laser_speed

		elif direction == 'left':
			self.rect.right = self.ninja.rect.right + 12
			self.rect.centery = self.ninja.rect.centery
			self.change_x = self.laser_speed * -1

		elif direction == 'up':
			self.image = self.laser_image_vertical
			self.rect = self.image.get_rect()
			self.rect.bottom = self.ninja.rect.bottom + 12
			self.rect.centerx = self.ninja.rect.centerx
			self.change_x = 0
			self.change_y = self.laser_speed * -1

		elif direction == 'down':
			self.image = self.laser_image_vertical
			self.rect = self.image.get_rect()
			self.rect.top = self.ninja.rect.top - 12
			self.rect.centerx = self.ninja.rect.centerx
			self.change_x = 0
			self.change_y = self.laser_speed

		self.true_x = self.rect.x
		self.true_y = self.rect.y

class Mine_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja, number):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.number = number #holds number of sprite. Each ninja has an effect 0,1,2.
		self.type = 'mine'
		self.portal_delay = 0
		self.image_number = 0
		self.frame_counter = 0

		#Needed to help sort online play.
		self.online_ID = self.ninja.item_key_number
		self.ninja.item_dict[self.online_ID] = self
		self.ninja.item_key_number += 1
		self.online_counter = 1

		#self.predictive_collision_list = [] #holds list of ninjas scheduled to die next frame. They must die to keep games in line.



		self.image_list_right = []
		image = self.ninja.spritesheet.getImage(293, 250, 14, 5)
		self.image_list_right.append(image)
		image = self.ninja.spritesheet.getImage(293, 256, 14, 5)
		self.image_list_right.append(image)
		image = self.ninja.spritesheet.getImage(293, 262, 14, 5)
		self.image_list_right.append(image)
		image = self.ninja.spritesheet.getImage(293, 268, 14, 5)
		self.image_list_right.append(image)
		image = self.ninja.spritesheet.getImage(293, 274, 14, 5)
		self.image_list_right.append(image)
		self.ninja.big_image_list.append(self.image_list_right)

		self.image_list_left = []
		image = self.ninja.spritesheet.getImage(293, 250, 14, 5)
		image = pygame.transform.flip(image, True, False)
		self.image_list_left.append(image)
		image = self.ninja.spritesheet.getImage(293, 256, 14, 5)
		image = pygame.transform.flip(image, True, False)
		self.image_list_left.append(image)
		image = self.ninja.spritesheet.getImage(293, 262, 14, 5)
		image = pygame.transform.flip(image, True, False)
		self.image_list_left.append(image)
		image = self.ninja.spritesheet.getImage(293, 268, 14, 5)
		image = pygame.transform.flip(image, True, False)
		self.image_list_left.append(image)
		image = self.ninja.spritesheet.getImage(293, 274, 14, 5)
		image = pygame.transform.flip(image, True, False)
		self.image_list_left.append(image)
		self.ninja.big_image_list.append(self.image_list_left)

		self.explosion_list = []
		image = self.ninja.spritesheet.getImage(412, 345, 14, 14)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(427, 345, 14, 14)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(442, 345, 14, 14)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(457, 345, 14, 14)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(472, 345, 14, 14)
		self.explosion_list.append(image)

		self.unarmed_explosion_list = []
		image = self.ninja.spritesheet.getImage(412, 360, 14, 14)
		self.unarmed_explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(427, 360, 14, 14)
		self.unarmed_explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(442, 360, 14, 14)
		self.unarmed_explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(457, 360, 14, 14)
		self.unarmed_explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(472, 360, 14, 14)
		self.unarmed_explosion_list.append(image)
		

		self.image = self.image_list_left[0]
		self.rect = self.image.get_rect()

		

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1



		self.status = "" #'', 'thrown', 'armed', 'explode'
		
		self.throw_speed = 1
		self.big_throw_speedx = 3
		self.big_throw_speedy = 3

		self.change_x = 0
		self.change_y = 0
		#self.change_g = 0.8 held in options now
		#self.max_g = 9
		self.inverted_g = False
		self.inverted_switch = False
		self.explosion_seed = random.randrange(0,10000,1)

		self.explode_type = None

		self.teleported = False
		self.kill_count = 0

		self.moving_platform = False
		self.last_status = None #holds type of status before explode/kill check. Decides if 'armed' explosion or 'regular' explosion.


	def update(self):
		self.moving_platform = False
		if self.portal_delay > 0:
			self.portal_delay -= 1

		if self.status == 'thrown':
			self.online_counter += 1

			self.visible = 1
			self.dirty = 1
			
			self.apply_gravity()

			self.true_x += self.change_x
			self.true_y += self.change_y

			self.rect.x = round(self.true_x)
			self.rect.y = round(self.true_y)


			self.tile_collision_check()
			self.unarmed_collision_check()

			for ninja in sprites.ninja_list:
					if ninja.shield_sprite.active is True:
						ninja.shield_sprite.collision_check(self)

			if self.change_x >= 0:
				self.image = self.image_list_right[self.image_number]
			else:
				self.image = self.image_list_left[self.image_number]

			if self.inverted_g is True:
				old_true_x = self.true_x
				old_true_y = self.true_y

				i = self.image.copy()
				self.image = pygame.transform.flip(i,False,True)
				self.image.get_rect

				self.true_x = old_true_x
				self.true_y = old_true_y
				self.rect.x = round(self.true_x)
				self.rect.y = round(self.true_y)

			self.frame_counter += 1
			if self.frame_counter == 4:
				self.image_number += 1

			if self.image_number > 1:
				self.image_number = 1


		if self.status == 'armed':
			self.visible = 1
			self.dirty = 1

			self.image = self.image_list_right[self.image_number]

			self.frame_counter += 1

			if self.frame_counter >= 20:
				self.frame_counter = 0
				self.image_number += 1
				i = len(self.image_list_right) - 1
				if self.image_number > i:
					self.image_number = i

			

			if self.inverted_g is True:
				old_true_x = self.true_x
				old_true_y = self.true_y

				i = self.image.copy()
				self.image = pygame.transform.flip(i,False,True)
				self.image.get_rect

				self.true_x = old_true_x
				self.true_y = old_true_y
				self.rect.x = round(self.true_x)
				self.rect.y = round(self.true_y)

			self.armed_collision_check()
			self.armed_visibility_check()
			self.inverted_check()

		if self.status == 'explode':
			self.visible = 1
			self.dirty = 1

			self.frame_counter += 1
			if self.frame_counter == 2:
				self.frame_counter = 0
				self.image_number += 1

			if self.image_number >= len(self.explosion_list):
				self.reset()
			else:
				if self.last_status == 'armed':
					self.image = self.explosion_list[self.image_number]
				else:
					self.image = self.unarmed_explosion_list[self.image_number]

			
			#push rope points based on collision center
			for rope in sprites.level_ropes:
				for point in rope.point_list:
					if self.rect.collidepoint(point.rect.center):
						point.explosion_force(self.rect.center)

			if self.inverted_g is True:
				old_true_x = self.true_x
				old_true_y = self.true_y

				i = self.image.copy()
				self.image = pygame.transform.flip(i,False,True)
				self.image.get_rect

				self.true_x = old_true_x
				self.true_y = old_true_y
				self.rect.x = round(self.true_x)
				self.rect.y = round(self.true_y)




			self.kill_check()

		self.boundary_check()

	def unarmed_collision_check(self):
		for ninja in sprites.ninja_list:
				if ninja.collision_rect.colliderect(self.rect):
					self.explode()


		for enemy in sprites.enemy_list:
				temp_rect = pygame.Rect(enemy.rect.x + 2, enemy.rect.y + 2, enemy.rect.width - 4, enemy.rect.height - 4)
				if temp_rect.colliderect(self.rect):
					self.explode()
					if 'explosion' in enemy.death_list:
						enemy.destroy()

					break



		for tile in sprites.tile_list:
			if tile.type == 'mallow':
				if tile.rect.colliderect(self.rect):
					if tile.inverted is False:
						if self.rect.bottom > tile.rect.top + 5:
							self.explode()

							break
					else:
						if self.rect.top < tile.rect.bottom - 5:
							self.explode()
							break

	def boundary_check(self):
		if self.ninja.loop_physics is True:
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

	def inverted_check(self): #check to see if it should 'fall again' if inverted.
		
		if self.inverted_switch != self.inverted_g:
			self.inverted_switch = self.inverted_g
			self.change_y = 0
			self.frame_number = 0
			self.image_numer = 1
			self.status = 'thrown'
			self.teleported = False #lets it be teleported again on gravity switch.
			self.portal_delay = 5 #allows it to escape current teleporter its on.


	def tile_collision_check(self):
		falling_rect = pygame.Rect(self.rect.x + 2, self.rect.top, self.rect.width - 4, self.rect.height)
		if self.inverted_g is False:
			armed_rect = pygame.Rect(self.rect.x, self.rect.bottom - 2, self.rect.width, 4)
		else:
			armed_rect = pygame.Rect(self.rect.x, self.rect.top -2, self.rect.width, 4)


		#Make sure not on top of portal
		portal = False
		for item in sprites.active_items:
			if item.type == 'portal_gun_portal':
				if self.rect.colliderect(item.collision_rect):
					if len(item.portal_gun.active_portal_list) == 2: #portal to teleport to!
						portal = True
						break

		if portal is False:
			tile_list = []
			for tile in sprites.tile_list:
				if tile.type == 'platform' or tile.type == 'tile':
					if tile.rect.colliderect(self.rect):
						tile_list.append(tile)
				if tile.type == 'mallow_wall':
					if tile.rect.colliderect(self.rect):
						if self.change_x > 0:
							self.rect.right = tile.rect.left
							self.true_x = self.rect.x
						elif self.change_x < 0:
							self.rect.left = tile.rect.right
							self.true_x = self.rect.x
						self.change_x = 0

			temp_list = [] #holds just tiles
			for tile in tile_list:
				if tile.type == 'tile':
					temp_list.append(tile)
			
			if len(temp_list) > 0:
					collision = True #assume collision to start
					first_tile_list = [] #make a list that whille eventually hold that first tile(s) contacted
					i = 0
					frame_division = 9
					base_position = self.rect.center
					x_change = float(self.change_x / frame_division)
					y_change = float(self.change_y / frame_division)
					while collision is True and i < 15:
						i += 1
						self.rect.center = base_position
						self.rect.x -= round(x_change * i)
						self.rect.y -= round(y_change * i)

						temp_temp_list = [] #temp list that will be turned into first_tile_list
						for tile in temp_list:
							if self.rect.colliderect(tile.rect):
								collision = True
								temp_temp_list.append(tile)
						if len(temp_temp_list) > 0:
							first_tile_list = temp_temp_list
						else:
							collision = False

					#now fix for all tiles in first_tile_list.
					#fix in x direction first. Mine should currently be JUST before a collision.
					if self.change_x > 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
							if tile.rect.colliderect(temp_rect):
								self.rect.right = tile.rect.left
								self.true_x = self.rect.x
								self.change_x = 0
								break

					elif self.change_x < 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.left - 1,self.rect.y,1,self.rect.height)
							if tile.rect.colliderect(temp_rect):
								self.rect.left = tile.rect.right
								self.true_x = self.rect.x
								self.change_x = 0
								break

					#Now fix y_direction. Mine should currently be JUST before a collision.
					if self.change_y > 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.x,self.rect.bottom,self.rect.width,1)
							if tile.rect.colliderect(temp_rect):
								self.rect.bottom = tile.rect.top
								self.true_y = self.rect.y
								if self.inverted_g is False:
									self.status = 'armed'
									sounds.mixer.mine.play()
									self.frame_counter = 0
									self.change_x = 0
									self.change_y = 0
								else:
									self.change_y = 0
								break

					elif self.change_y < 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.x,self.rect.top - 1,self.rect.width,1)
							if tile.rect.colliderect(temp_rect):
								self.rect.top = tile.rect.bottom
								self.true_y = self.rect.y
								if self.inverted_g is True:
									self.status = 'armed'
									sounds.mixer.mine.play()
									self.frame_counter = 0
									self.change_x = 0
									self.change_y = 0
								else:
									self.change_y = 0
								sounds.mixer.bounce.play()
								break
			#now for platforms
			if self.inverted_g is False:
				armed_rect = pygame.Rect(self.rect.x, self.rect.bottom - 2, self.rect.width, 4)
			else:
				armed_rect = pygame.Rect(self.rect.x, self.rect.top -2, self.rect.width, 4)
			for tile in tile_list:
				if tile.type == 'platform':
					if self.change_y > 0:
						if armed_rect.colliderect(tile.rect):
							if self.inverted_g is False:
								if self.rect.bottom <= tile.rect.top + 5: #got high enough
									self.rect.bottom = tile.rect.top
									self.true_y = self.rect.y
									self.status = 'armed'
									sounds.mixer.mine.play()
									self.frame_counter = 0
									self.change_x = 0
									self.change_y = 0
							else:
								pass #pass through platforms from bottom.

								#self.rect.top = tile.rect.bottom
								#self.true_y = self.rect.y
								#self.change_y = 0
							break
					elif self.change_y < 0:
						if armed_rect.colliderect(tile.rect):
							if self.inverted_g is True:
								if self.rect.top >= tile.rect.bottom - 5: #got high enough
									self.rect.top = tile.rect.bottom
									self.true_y = self.rect.y
									self.status = 'armed'
									sounds.mixer.mine.play()
									self.frame_counter = 0
									self.change_x = 0
									self.change_y = 0
							else:
								pass #pass through platforms from the bottom
								#self.rect.bottom = tile.rect.top
								#self.true_y = self.rect.y
								#self.change_y = 0
							break
		
		'''
		if self.portal_delay == 0:
			if self.inverted_g is False:
				armed_rect = pygame.Rect(self.rect.x, self.rect.bottom - 2, self.rect.width, 4)
				for tile in sprites.tile_list:
					if tile.type == 'platform' or tile.type == 'tile':
						if armed_rect.colliderect(tile.top_rect):
							self.status = 'armed'
							sounds.mixer.mine.play()
							self.frame_counter = 0
							self.change_x = 0
			else:
				armed_rect = pygame.Rect(self.rect.x, self.rect.top -2, self.rect.width, 4)
				for tile in sprites.tile_list:
					if tile.type == 'platform' or tile.type == 'tile':
						if armed_rect.colliderect(tile.bottom_rect):
							self.status = 'armed'
							sounds.mixer.mine.play()
							self.frame_counter = 0
							self.change_x = 0
		'''

			

	def arm_on_tile(self, tile):
		self.change_x = 0
		self.change_y = 0
		self.status = 'armed'
		sounds.mixer.mine.play()
		if tile.inverted_g is False:
			self.rect.bottom = tile.rect.top
			self.true_y = self.rect.y
		else:
			self.rect.top = tile.rect.bottom
			self.true_y = self.rect.y
		self.frame_counter = 0

	
	def armed_collision_check(self):
		for ninja in sprites.ninja_list:
			#make rect so it has to be 'bottom of ninja' that collides with the mine.
			#inja_rect = pygame.Rect(ninja.rect.x + 3, ninja.rect.y + ninja.rect.height - 5, ninja.rect.width - 6, 5)
			if ninja.rect_bottom.colliderect(self.rect):
					self.explode()

					break

		for enemy in sprites.enemy_list:
				if enemy.inverted_g is False:
					temp_rect = pygame.Rect(enemy.rect.x + 3, enemy.rect.bottom - 4, enemy.rect.width - 6, 4)
				else:
					temp_rect = pygame.Rect(enemy.rect.x + 3, enemy.rect.top, enemy.rect.width - 6, 4)
				if temp_rect.colliderect(self.rect):
					self.explode()

					if 'explosion' in enemy.death_list:
						enemy.destroy()
					break


		for item in sprites.active_items: #pressure sensitive for incoming items
			if item != self:
				if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
					if item.status != '' and item.status != 'explode':
						if item.rect.colliderect(self.rect):
							self.explode()

							break

	def armed_visibility_check(self):
		big_rect = pygame.Rect(self.rect.x - 15, self.rect.y, self.rect.width + 30, self.rect.height)
		med_rect = pygame.Rect(self.rect.x - 10, self.rect.y, self.rect.width + 20, self.rect.height)
		small_rect = pygame.Rect(self.rect.x - 5, self.rect.y, self.rect.width + 10, self.rect.height)
		for ninja in sprites.ninja_list:
			if ninja.inverted_g is False:
				ninja_rect = pygame.Rect(ninja.rect.x, ninja.rect.y + ninja.rect.height - 5, ninja.rect.width, 5)
			else:
				ninja_rect = pygame.Rect(ninja.rect.x, ninja.rect.y, ninja.rect.width, 5)
			if ninja_rect.colliderect(big_rect):
				i = 3
				if ninja_rect.colliderect(med_rect):
					i = 2
					if ninja_rect.colliderect(small_rect):
						i = 1

				if i < self.image_number:
					self.image_number = i



	def apply_gravity(self):
		if self.status != 'armed':
			if self.inverted_g is False:
				self.change_y += options.change_g

				if self.change_y > options.max_g:
					self.change_y = options.max_g
			else:
				self.change_y -= options.change_g

				if self.change_y < options.max_g * -1:
					self.change_y = options.max_g * -1

						

	def reset(self):
		self.kill_count = 0
		self.visible = 0
		self.image_number = 0
		self.frame_counter = 0
		self.dirty = 1
		self.status = "" #'', 'thrown', 'armed', 'explode'
		self.change_x = 0
		self.change_y = 0
		self.image = self.image_list_right[0]
		self.rect = self.image.get_rect()
		self.inverted_g = False
		self.inverted_switch = False
		self.teleported = False
		self.explosion_seed = random.randrange(0,10000,1)
		try:
			sprites.active_items.remove(self)
		except ValueError:
			pass

	def attempt_throw(self):
		if self.status == '':
			self.status = 'thrown'
			self.throw_mine()
			self.ninja.item = ''
		else:
			thrown = False
			for mine in self.ninja.mine_list:
				if mine.status == '':
					mine.attempt_throw()
					thrown = True
					break

			#all mines in action, randomly get rid of one.
			if thrown is False:
				mine = random.choice(self.ninja.mine_list)
				mine.reset()
				mine.attempt_throw()


	def throw_mine(self):
		self.ninja.stats_mine_thrown += 1
		throw_type = 'mine'
		if self.ninja.inverted_g is True:
			self.inverted_g = True
			self.inverted_switch = True
		else:
			self.inverted_g = False
			self.inverted_switch = False

		sprites.active_items.append(self)
		if self.ninja.status == 'jump':
			self.rect.centerx = self.ninja.rect.centerx
			if self.ninja.inverted_g is False:
				self.rect.top = self.ninja.rect.bottom
			else:
				self.rect.bottom = self.ninja.rect.top

			self.true_y = self.rect.y
			self.true_x = self.rect.x

			self.change_x = 0
			self.image = self.image_list_right[1]
			self.image_number = 1
			throw_type = 'mine_down'
			#for tile in sprites.tile_list:
			#	if tile.rect.colliderect(self.rect):
			#		self.rect.right = tile.rect.left


		else: #not jumping, all other scenarios:
			if self.ninja.direction == 'right':
				self.rect.left = self.ninja.rect.right
				if self.ninja.inverted_g is False:
					self.rect.centery = self.ninja.rect.bottom - 21
				else:
					self.rect.centery = self.ninja.rect.top + 21

				self.true_y = self.rect.y
				self.true_x = self.rect.x

				if self.ninja.status == 'right' or self.ninja.status == 'falling':
					self.change_x = self.big_throw_speedx
					if self.ninja.inverted_g is False:
						self.change_y = self.big_throw_speedy * -1
					else:
						self.change_y = self.big_throw_speedy
				else:
					self.change_x = self.throw_speed

				for tile in sprites.tile_list:
					if tile.type == 'tile':
						if tile.rect.colliderect(self.rect):
							self.rect.right = tile.rect.left
							self.true_x = self.rect.x

			elif self.ninja.direction == 'left':
				self.rect.right = self.ninja.rect.left
				if self.ninja.inverted_g is False:
					self.rect.centery = self.ninja.rect.bottom - 21
				else:
					self.rect.centery = self.ninja.rect.top + 21

				self.true_y = self.rect.y
				self.true_x = self.rect.x

				if self.ninja.status == 'left' or self.ninja.status == 'falling':
					self.change_x = self.big_throw_speedx * -1
					if self.ninja.inverted_g is False:
						self.change_y = self.big_throw_speedy * -1
					else:
						self.change_y = self.big_throw_speedy
				else:
					self.change_x = self.throw_speed * -1

				for tile in sprites.tile_list:
					if tile.type == 'tile':
						if tile.rect.colliderect(self.rect):
							self.rect.left = tile.rect.right
							self.true_x = self.rect.x

		if abs(self.change_y) == (self.throw_speed):
			throw_type = 'mine_slow'

		sprites.particle_generator.throw_item_particles((self.rect.centerx, self.rect.centery), self.change_x, self.change_y, self.inverted_g, throw_type)



	def explode(self):
		if sprites.shake_handler.current_shake < 2:
			sprites.shake_handler.current_shake = 2

		self.last_status = self.status
		sounds.mixer.explosion.play()
		self.status = 'explode'
		self.frame_counter = 0
		self.image_number = 0

		midtop = self.rect.midtop
		midbottom = self.rect.midbottom

		if self.last_status == 'armed':
			self.image = self.explosion_list[0]
		else:
			self.image = self.unarmed_explosion_list[0]
		self.rect = self.image.get_rect()
		
		if self.inverted_g is False:
			self.rect.midbottom = midbottom
		else:
			self.rect.midtop = midtop

		self.true_y = self.rect.y
		self.true_x = self.rect.x

		if self.last_status == 'armed':
			sprites.particle_generator.mine_explosion_particles(self.rect, self.inverted_g, self.explosion_seed, 'ash_finish')
		else:
			sprites.particle_generator.bomb_explosion_particles(self.rect, self.explosion_seed, self.inverted_g, 'ash_finish')

		#tile reaction(only triggered first frame)
		if self.inverted_g is False:
			collision_rect = pygame.Rect(self.rect.x -2, self.rect.bottom - 40, self.rect.width + 4, 60)
		else:
			collision_rect = pygame.Rect(self.rect.x -2, self.rect.top - 40, self.rect.width + 4, 60)
		for tile in sprites.tile_list: #unfreeze frozen tiles. Explode breakable tiles.
			if tile.type == 'tile' or tile.type == 'platform':
				if tile.rect.colliderect(collision_rect):
					if tile.breakable is True:
						tile.destroy(self)
					else:
						if tile.rect.top > collision_rect.top:
							tile.top_friction = 'normal'
							for particle in tile.attached_list:
								if particle.rect.centery <= tile.rect.centery:
									particle.image.fill(particle.color)
									particle.frozen = False
						if tile.rect.bottom < collision_rect.bottom:
							tile.bottom_friction = 'normal'
							for particle in tile.attached_list:
								if particle.rect.centery >= tile.rect.centery:
									particle.image.fill(particle.color)
									particle.frozen = False
						tile.apply_ice()

		for particle in sprites.active_particle_list:
			if particle.type in ('debris', 'mallow'):
				if particle.rect.colliderect(collision_rect):
					particle.image.fill(particle.color)
					particle.frozen = False

		for tile in sprites.tile_list:
			if tile.type == 'mallow':
				if tile.rect.colliderect(collision_rect):
					if tile.inverted is False:
						if self.rect.top < tile.rect.top:
							startxy = (self.rect.centerx, tile.rect.top + 3)
							sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, False, 1)
							break

					else:
						if self.rect.bottom > tile.rect.bottom:
							startxy = (self.rect.centerx, tile.rect.bottom - 3)
							sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, False, 1)
							break

		for enemy in sprites.enemy_list:
				if 'explosion' in enemy.death_list:
					if self.rect.colliderect(enemy.collision_dict['death']):
						enemy.destroy()

	def kill_check(self):
		if self.last_status == 'armed':
			collision_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		else:
			collision_rect = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, self.rect.height - 2)
		for ninja in sprites.ninja_list:
			#99999999
			if ninja.rect.colliderect(collision_rect):
					if ninja.shield_sprite.active is False:
						if self.last_status == 'armed':
							death_sprite_type = 'm'
							ninja.activate_death_sprite('mine', self)
						else:
							death_sprite_type = 'e'
							ninja.activate_death_sprite('explosion', self)
						if ninja == self.ninja:
							ninja.stats_mine_suicides += 1
						else:
							self.ninja.stats_mine_kills += 1
							if self.ninja.color == ninja.color:
								self.ninja.stats_ally_item_kill += 1
							else:
								self.ninja.score_item_kills()
							self.kill_count += 1
							if self.kill_count == 2:
								self.ninja.stats_mine_double_kills += 1
							elif self.kill_count == 3:
								self.ninja.stats_mine_triple_kills += 1


		for item in sprites.active_items:
			if item != self:
				if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
					if item.status != '' and item.status != 'explode':
						if item.rect.colliderect(collision_rect):
							item.explode()





	def collect_stats(self, ninja):
		if ninja == self.ninja:
			ninja.stats_mine_suicides += 1
		else:
			self.ninja.stats_mine_kills += 1
			if self.ninja.color == ninja.color:
				self.ninja.stats_ally_item_kill += 1
			else:
				self.ninja.score_item_kills()
			self.kill_count += 1
			if self.kill_count == 2:
				self.ninja.stats_mine_double_kills += 1
			elif self.kill_count == 3:
				self.ninja.stats_mine_triple_kills += 1

class Bomb_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja 
		self.type = 'bomb'
		self.subtype = 'Bomb'

		self.portal_delay = 0

		#Needed to help sort online play.
		self.online_ID = self.ninja.item_key_number
		self.ninja.item_dict[self.online_ID] = self
		self.ninja.item_key_number += 1
		self.online_counter = 0

		#self.predictive_collision_list = [] #holds list of ninjas scheduled to die next frame. They must die to keep games in line.



		self.image_number = 0
		self.frame_counter = 0

		self.left_image = []
		self.right_image = []
		
		image = self.ninja.spritesheet.getImage(275, 250, 8, 8)
		self.right_image.append(image)
		image = self.ninja.spritesheet.getImage(284, 250, 8, 8)
		self.right_image.append(image)
		image = self.ninja.spritesheet.getImage(275, 259, 8, 8)
		self.right_image.append(image)
		image = self.ninja.spritesheet.getImage(284, 259, 8, 8)
		self.right_image.append(image)

		image = self.ninja.spritesheet.getImage(284, 268, 8, 8)
		self.left_image.append(image)
		image = self.ninja.spritesheet.getImage(275, 268, 8, 8)
		self.left_image.append(image)
		image = self.ninja.spritesheet.getImage(284, 277, 8, 8)
		self.left_image.append(image)
		image = self.ninja.spritesheet.getImage(275, 277, 8, 8)
		self.left_image.append(image)

		self.ninja.big_image_list.append(self.left_image)
		self.ninja.big_image_list.append(self.right_image)

		self.image = self.left_image[0]
		self.rect = self.image.get_rect()

		self.explosion_list = []
		image = self.ninja.spritesheet.getImage(250, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(299, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(348, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(397, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(446, 295, 48, 48)
		self.explosion_list.append(image)

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.status = "" #"", "bomb", or 'explode'

		self.change_x = 0
		self.change_y = 0 

		self.true_x = 0
		self.true_y = 0
		#self.change_g = 0.8 #held in options now
		#self.max_g = 9

		self.bomb_throw_speed = 1
		self.short_throw_speed = 1
		self.long_throw_speed = 3
		self.jump_bomb_speed = 1

		self.bomb_timer = 0

		self.delay_timer = 0

		self.inverted_g = False

		self.explosion_seed = random.randrange(0,10000,1)

		self.kill_count = 0

		self.slow_switch = False
		self.moving_platform = False

	def update(self):
		self.moving_platform = False

		if self.portal_delay > 0:
			self.portal_delay -= 1

		if self.status == 'explode':
			#if self.frame_counter == 0:
			#	sprites.particle_generator.radial_explosion_particles(self.rect.center, self.inverted_g, self.explosion_seed)

			self.frame_counter += 1

			if self.frame_counter >= 3:
				self.frame_counter = 0
				self.image_number += 1

			if self.image_number >= len(self.explosion_list):
				self.reset()
			else:
				self.image = self.explosion_list[self.image_number]

			#push rope points based on collision center
			for rope in sprites.level_ropes:
				for point in rope.point_list:
					if self.rect.collidepoint(point.rect.center):
						point.explosion_force(self.rect.center)

			self.dirty = 1

			self.kill_check()

		elif self.status == 'bomb' and self.delay_timer >= 1:
			
			self.bomb_timer += 1
			self.frame_counter += 1

			
			if self.frame_counter >= 6:
				self.frame_counter = 0
				if self.change_x != 0:
					self.image_number += 1

				if self.image_number >= len(self.right_image):
					self.image_number = 1 #don't go to zero. That is just for through 'initial'

				if self.change_x > 0:
					self.image = self.right_image[self.image_number]
				elif self.change_x < 0:
					self.image = self.left_image[self.image_number]

				if self.inverted_g is True and self.change_x != 0:
					i = self.image.copy()
					self.image = pygame.transform.flip(i,False,True)

			self.visible = 1
			self.dirty = 1

			self.apply_gravity()

			#i = (90 - self.bomb_timer) / 90
			i = 1

			if self.bomb_timer > 60: #start slowing after first second
				self.bomb_throw_speed *= 0.99

			if self.change_x > 0:
				self.change_x = self.bomb_throw_speed
				self.change_x = round(self.change_x * i)
			if self.change_x < 0:
				self.change_x = self.bomb_throw_speed * -1
				self.change_x = round(self.change_x * i)

			self.true_x += self.change_x
			self.true_y += self.change_y
			
			self.rect.x = round(self.true_x)
			self.rect.y = round(self.true_y)

			self.collision_check()

			for ninja in sprites.ninja_list:
					if ninja.shield_sprite.active is True:
						ninja.shield_sprite.collision_check(self)

			if self.bomb_timer >= 180:
					self.explode()




		self.delay_timer += 1

		self.boundary_check()

	def boundary_check(self):
		if self.ninja.loop_physics is True:
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

	def kill_check(self):
		collision_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		for ninja in sprites.ninja_list:
			#999999999
			if ninja.rect.colliderect(collision_rect):
					if ninja.shield_sprite.active is False:
						ninja.activate_death_sprite('explosion', self)
						if options.game_state == 'level':
							try:
								if ninja == self.ninja:
									self.ninja.stats_bomb_suicides += 1
								else:
									self.ninja.stats_bomb_kills += 1
									if self.ninja.color == ninja.color:
										self.ninja.stats_ally_item_kill += 1
									else:
										self.ninja.score_item_kills()
									self.kill_count += 1
									if self.kill_count == 2:
										self.ninja.stats_bomb_double_kills += 1
									elif self.kill_count == 3:
										self.ninja.stats_bomb_triple_kills += 1
							except AttributeError:
								pass



		for item in sprites.active_items:
			if item != self:
				if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
					if item.status != '' and item.status != 'explode':
						if item.rect.colliderect(collision_rect):
							item.explode()


		for enemy in sprites.enemy_list:
				if 'explosion' in enemy.death_list:
					if self.rect.colliderect(enemy.collision_dict['death']):
						enemy.destroy()

	def collect_stats(self, ninja):
		if options.game_state == 'level':
			try:
				if ninja == self.ninja:
					self.ninja.stats_bomb_suicides += 1
				else:
					self.ninja.stats_bomb_kills += 1
					if self.ninja.color == ninja.color:
						self.ninja.stats_ally_item_kill += 1
					else:
						self.ninja.score_item_kills()
					self.kill_count += 1
					if self.kill_count == 2:
						self.ninja.stats_bomb_double_kills += 1
					elif self.kill_count == 3:
						self.ninja.stats_bomb_triple_kills += 1
			except AttributeError:
				pass


	def explode(self):
		
		if sprites.shake_handler.current_shake < 2:
			sprites.shake_handler.current_shake = 2
		sounds.mixer.explosion.play()
		self.status = 'explode'
		self.frame_counter = 0
		self.image_number = 0

		centerx = self.rect.centerx
		centery = self.rect.centery

		self.image = self.explosion_list[0]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery

		self.true_x = self.rect.x
		self.true_y = self.rect.y

		if self.subtype == 'ice_bomb':
			sprites.particle_generator.ice_bomb_explosion_particles(self.rect, self.inverted_g, 'snow_finish')
		elif self.subtype != 'ice_bomb': #not ICE bomb:
			sprites.particle_generator.bomb_explosion_particles(self.rect, self.explosion_seed, self.inverted_g, 'ash_finish')
			

		#tile reaction(only triggered first frame)
		collision_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		#build rect from explode rect perimeter points:
		#left = None
		#right = None
		#top = None
		#bottom = None
		#destroyed = False
		if self.subtype != 'ice_bomb':
			for tile in sprites.tile_list: #unfreeze frozen tiles
				if tile.type == 'tile' or tile.type == 'platform':
					if tile.rect.colliderect(collision_rect):
						if tile.breakable is True:
							tile.destroy(self)
						else:
							if tile.rect.top > collision_rect.top:
								tile.top_friction = 'normal'
								for particle in tile.attached_list:
									if particle.rect.centery <= tile.rect.centery:
										particle.image.fill(particle.color)
										particle.frozen = False
							if tile.rect.bottom < collision_rect.bottom:
								tile.bottom_friction = 'normal'
								for particle in tile.attached_list:
									if particle.rect.centery >= tile.rect.centery:
										particle.image.fill(particle.color)
										particle.frozen = False
							tile.apply_ice()

			for particle in sprites.active_particle_list:
				if particle.type in ('debris', 'mallow'):
					if particle.rect.colliderect(collision_rect):
						particle.image.fill(particle.color)
						particle.frozen = False

			for tile in sprites.tile_list:
				if tile.type == 'mallow':
					if tile.rect.colliderect(collision_rect):
						if tile.inverted is False:
							if self.rect.top < tile.rect.top:
								startxy = (self.rect.centerx, tile.rect.top + 3)
								sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, False, 1)
								break

						else:
							if self.rect.bottom > tile.rect.bottom:
								startxy = (self.rect.centerx, tile.rect.bottom - 3)
								sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, False, 1)
								break

			for item in sprites.active_items:
				if item != self:
					if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
						if item.status != '' and item.status != 'explode':
							if item.rect.colliderect(self.rect):
								item.explode()

								break




	def collision_check(self):
		if self.inverted_g is False:
			bomb_bottom = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
			bomb_top = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 5)
		else:
			bomb_top = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
			bomb_bottom = pygame.Rect(self.rect.x, self.rect.top, self.rect.width - 2, 5)


		#Make sure not on top of portal
		portal = False
		for item in sprites.active_items:
			if item.type == 'portal_gun_portal':
				if self.rect.colliderect(item.collision_rect):
					if len(item.portal_gun.active_portal_list) == 2: #portal to teleport to!
						portal = True
						break

		temp_list = []
		if portal is False:
			for tile in sprites.tile_list:
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
								sounds.mixer.bounce.play()

						elif tile.type == 'mallow':
								bomb_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4)
								if tile.rect.colliderect(bomb_rect):
									self.explode()

									break

			if self.inverted_g is False: #get updated collision rects for all 
				bomb_bottom = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
				bomb_top = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 5)
			else:
				bomb_top = pygame.Rect(self.rect.x, self.rect.bottom - 5, self.rect.width, 5)
				bomb_bottom = pygame.Rect(self.rect.x, self.rect.top, self.rect.width - 2, 5)
			
			tile_list = []
			for tile in temp_list:
				if tile.type == 'tile':
					tile_list.append(tile)
			
			if len(tile_list) > 0:
					collision = True #assume collision to start
					first_tile_list = [] #make a list that whille eventually hold that first tile(s) contacted
					i = 0
					frame_division = 9
					base_position = self.rect.center
					x_change = float(self.change_x / frame_division)
					y_change = float(self.change_y / frame_division)
					while collision is True and i < 15:
						i += 1
						self.rect.center = base_position
						self.rect.x -= round(x_change * i)
						self.rect.y -= round(y_change * i)

						temp_tile_list = [] #temp list that will be turned into first_tile_list
						for tile in tile_list:
							if self.rect.colliderect(tile.rect):
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
								self.rect.right = tile.rect.left
								self.change_x *= -1
								sounds.mixer.bounce.play()
								break

					elif self.change_x < 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.left - 1,self.rect.y,1,self.rect.height)
							if tile.rect.colliderect(temp_rect):
								self.rect.left = tile.rect.right
								self.change_x *= -1
								sounds.mixer.bounce.play()
								break

					#Now fix y_direction. bomb should currently be JUST before a collision.
					if self.change_y > 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.x,self.rect.bottom,self.rect.width,1)
							if tile.rect.colliderect(temp_rect):
								self.rect.bottom = tile.rect.top
								if self.inverted_g is False:
									self.change_y *= -0.85
								else:
									self.change_y *= -1
								sounds.mixer.bounce.play()
								break

					elif self.change_y < 0:
						for tile in first_tile_list:
							temp_rect = pygame.Rect(self.rect.x,self.rect.top - 1,self.rect.width,1)
							if tile.rect.colliderect(temp_rect):
								self.rect.top = tile.rect.bottom
								if self.inverted_g is True:
									self.change_y *= -0.85
								else:
									self.change_y *= -1
								sounds.mixer.bounce.play()
								break

					#Attempt to keep movement fluid by adding back on the postion 'cut off' but the collision code.
					base_position = self.rect.center
					collision = True
					#i is the same i as above.
					while i > 0 and collision is True:
						self.rect.center = base_position
						self.rect.x += round(self.change_x / frame_division * i * (1/3)) #the 2/3 modifier is just to reduce the amount of distance jump. Smooths out the aesthetics of not actually 'hitting the wall'. Balanced with 'maintaining most of the physics'.
						self.rect.y += round(self.change_y / frame_division * i * (1/3))
						collision = False
						for tile in sprites.tile_list:
							if tile.type == 'tile':
								if tile.rect.colliderect(self.rect):
									collision = True
									break
						i -= 1

					self.true_x = self.rect.x
					self.true_y = self.rect.y
			#now do platforms!
			for tile in temp_list:
				if tile.type == 'platform':
					if self.inverted_g is False and tile.top_open is True: #makes sure top isn't covered by another tile
						if bomb_bottom.colliderect(tile.top_rect) and self.change_y > 0:
							self.rect.bottom = tile.rect.top
							self.true_y = self.rect.y
							sounds.mixer.bounce.play()
							self.change_y *= -0.8
							break
							#bounce = True
					elif self.inverted_g is True and tile.bottom_open is True: #makes sure bottom of tile -inverted top- is available.
						if bomb_bottom.colliderect(tile.bottom_rect) and self.change_y < 0:
							self.rect.top = tile.rect.bottom
							self.true_y = self.rect.y
							sounds.mixer.bounce.play()
							self.change_y *= -0.8
							break

		if self.bomb_timer > 1:
			for ninja in sprites.ninja_list:
				#ninja_rect = pygame.Rect(ninja.rect.x + 2, ninja.rect.y + 2, ninja.rect.width - 4, ninja.rect.height - 4)
				if ninja.shield_sprite.active is False:
						if ninja.collision_rect.colliderect(self.rect):
							self.explode()

							break

			for enemy in sprites.enemy_list:
						temp_rect = pygame.Rect(enemy.rect.x + 2, enemy.rect.y + 2, enemy.rect.width - 4, enemy.rect.height - 4)
						if temp_rect.colliderect(self.rect):
							self.explode()

							break

		if self.status != 'explode':
			for item in sprites.active_items:
				if item != self:
					if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
						if item.status != '' and item.status != 'explode':
							if item.rect.colliderect(self.rect):
								item.explode()
								self.explode()

								break

	def apply_gravity(self):
		if self.inverted_g is False:
			self.change_y += options.change_g

			if self.change_y > options.max_g:
				self.change_y = options.max_g
		else:
			self.change_y -= options.change_g

			if self.change_y < options.max_g * -1:
				self.change_y = options.max_g * -1



	def throw_bomb(self):
		self.reset()

		if self.type == Ninja: #Cannons don't have stats!
			if self.subtype == 'ice_bomb':
				self.ninja.stats_ice_bomb_thrown += 1
			else:
				self.ninja.stats_bomb_thrown += 1
		
		throw_type = 'normal'
		sprites.active_items.append(self)
		self.status = 'bomb'
		self.image_number = 0
		self.frame_counter = 0
		self.bomb_timer = 0
		self.visible = 1
		self.inverted_g = self.ninja.inverted_g
		
		if (self.ninja.status == 'jump' or self.ninja.status == 'roll') and self.ninja.change_y != 0:
			self.change_x = 0
			self.image = self.right_image[1]
			if self.ninja.change_x > 0:
				self.image = self.right_image[1]
				self.bomb_throw_speed = self.jump_bomb_speed
				self.change_x = self.bomb_throw_speed

			elif self.ninja.change_x < 0:
				self.image = self.left_image[1]
				self.bomb_throw_speed = self.jump_bomb_speed
				self.change_x = self.bomb_throw_speed * -1
			else:
				self.image = self.right_image[1]
				self.change_x = 0

			self.rect = self.image.get_rect()
			if self.ninja.inverted_g is False: #drop down
				if self.ninja.change_y > 0:
					self.change_y = self.ninja.change_y
				self.change_y += 0.8
				self.rect.top= self.ninja.rect.bottom + 5
				self.rect.centerx = self.ninja.rect.centerx
				self.true_x = self.rect.x
				self.true_y = self.rect.y
				for tile in sprites.tile_list:
					if tile.rect.colliderect(self.rect):
						self.rect.bottom = tile.rect.top
						self.true_y = self.rect.y
			else: #drop straigt up
				if self.ninja.change_y < 0:
					self.change_y = self.ninja.change_y
				self.change_y -= 0.8
				self.rect.bottom= self.ninja.rect.top - 5
				self.rect.centerx = self.ninja.rect.centerx
				self.true_x = self.rect.x
				self.true_y = self.rect.y
				for tile in sprites.tile_list:
					if tile.rect.colliderect(self.rect):
						self.rect.top = tile.rect.bottom
						self.true_y = self.rect.y
			throw_type = 'bomb_down'

		else:
			if self.ninja.inverted_g is False:
				self.change_y = -3
			else:
				self.change_y = 3


			if self.ninja.direction == 'right':
				self.image = self.right_image[0]
				self.rect = self.image.get_rect()
				self.rect.left = self.ninja.rect.right
				self.rect.centery = self.ninja.rect.centery
				self.true_x = self.rect.x
				self.true_y = self.rect.y
				#if self.ninja.change_x == 0:
				if self.ninja.status == 'right' or self.ninja.status == 'falling':
					self.bomb_throw_speed = self.long_throw_speed
				else:
					self.bomb_throw_speed = self.short_throw_speed
					self.change_y *= 0.5
				self.change_x = self.bomb_throw_speed
				if self.ninja.change_x > 0:
					self.change_x += self.ninja.change_x

				for tile in sprites.tile_list: #prevent bomb from being thrown inside wall
					if tile.type == 'tile':
						if tile.rect.colliderect(self.rect):
							self.rect.right = tile.rect.left
							self.true_x = self.rect.x

			if self.ninja.direction == 'left':
				self.image = self.left_image[0]
				self.rect = self.image.get_rect()
				self.rect.right = self.ninja.rect.left
				self.rect.centery = self.ninja.rect.centery
				self.true_x = self.rect.x
				self.true_y = self.rect.y
				#if self.ninja.change_x == 0:
				if self.ninja.status == 'left' or self.ninja.status == 'falling':
					self.bomb_throw_speed = self.long_throw_speed
				else:
					self.bomb_throw_speed = self.short_throw_speed	
					self.change_y *= 0.5
				self.change_x = self.bomb_throw_speed * -1
				if self.ninja.change_x < 0:
					self.change_x += self.ninja.change_x

				for tile in sprites.tile_list: #prevent bomb from being thrown inside wall
					if tile.type == 'tile':
						if tile.rect.colliderect(self.rect):
							self.rect.left = tile.rect.right
							self.true_x = self.rect.x

		if self.subtype != 'cannon_bomb':
			sprites.particle_generator.throw_item_particles((self.rect.centerx, self.rect.centery), self.change_x, self.change_y, self.inverted_g, throw_type)


	def reset(self):
		self.online_counter = 0
		self.delay_timer = 0
		self.visible = 0
		self.dirty = 1
		self.change_x = 0
		self.change_y = 0
		self.status = ''
		self.bomb_timer = 0
		self.image = self.left_image[0]
		self.rect = self.image.get_rect()
		self.explosion_seed = random.randrange(0,10000,1)
		self.kill_count = 0
		try:
			sprites.active_items.remove(self)
		except ValueError:
			pass


class Ice_Bomb_Sprite(Bomb_Sprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		Bomb_Sprite.__init__(self, ninja)

		self.subtype = 'ice_bomb'

		self.left_image = []
		self.right_image = []
		
		image = self.ninja.spritesheet.getImage(304, 196, 12, 12)
		self.right_image.append(image)
		image = self.ninja.spritesheet.getImage(317, 196, 12, 12)
		self.right_image.append(image)
		image = self.ninja.spritesheet.getImage(330, 196, 12, 12)
		self.right_image.append(image)
		image = self.ninja.spritesheet.getImage(343, 196, 12, 12)
		self.right_image.append(image)

		image = self.ninja.spritesheet.getImage(343, 196, 12, 12)
		self.left_image.append(image)
		image = self.ninja.spritesheet.getImage(330, 196, 12, 12)
		self.left_image.append(image)
		image = self.ninja.spritesheet.getImage(317, 196, 12, 12)
		self.left_image.append(image)
		image = self.ninja.spritesheet.getImage(304, 196, 12, 12)
		self.left_image.append(image)

		self.ninja.big_image_list.append(self.left_image)
		self.ninja.big_image_list.append(self.right_image)

		self.image = self.left_image[0]
		self.rect = self.image.get_rect()

	
		temp_list = []
		for image in self.explosion_list:
			self.image.lock()
			array = pygame.PixelArray(image)
			array.replace((175,37,50), (72,101,222))
			array.replace((217,81,27), (57,152,233))
			array.replace((230,127,44), (77,196,235))
			array.replace((234,184,66), (162,230,244))
			array.close()
			self.image.unlock()

			i = image.copy()
			image = pygame.Surface((i.get_width() * 2, i.get_height() * 2))
			pygame.transform.scale2x(i, image)
			i = image.copy()
			image = pygame.Surface((i.get_width() * 2, i.get_height() * 2))
			pygame.transform.scale2x(i, image)
			image.set_colorkey((0,255,0))
			temp_list.append(image)
		self.explosion_list = temp_list

	def kill_check(self): #override base bomb kill check.
		if self.image_number == 1 and self.frame_counter == 1:
			self.freeze_check()

	def freeze_check(self):
		#000000000
		sounds.mixer.freeze.play()

		collision_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 6, self.rect.width - 12, self.rect.height - 12)
		for enemy in sprites.enemy_list:
				if enemy.freezable is True:
					if enemy.rect.colliderect(collision_rect):
						enemy.freeze()

		for ninja in sprites.ninja_list:
				if ninja.rect.colliderect(collision_rect):
					if ninja.status != 'frozen':
						
						if ninja == self.ninja:
							self.ninja.stats_ice_bomb_self_cubes += 1

						try:
							self.ninja.stats_ice_bomb_cubes_made += 1
						except AttributeError:
							pass


						self.kill_count += 1
						try:
							if self.kill_count == 2:
								self.ninja.stats_ice_bomb_double_cubes += 1
							
							if self.kill_count == 3:
								self.ninja.stats_ice_bomb_triple_cubes += 1

							if self.kill_count == 4:
								self.ninja.stats_ice_bomb_quadruple_cubes += 1

						except AttributeError:
							pass

						ninja.stats_ice_bomb_times_frozen += 1

					ninja.ice_cube.freeze_ninja()
					#555555555


		for tile in sprites.tile_list:
			if tile.type == 'tile' or tile.type == 'platform':
				if tile.rect.colliderect(collision_rect):
					if tile.rect.top > collision_rect.top:
						tile.top_friction = 'icy'
						for particle in tile.attached_list:
							if particle.rect.centery <= tile.rect.centery:
								particle.image.fill(options.ICE)
								particle.frozen = True
					if tile.rect.bottom < collision_rect.bottom:
						tile.bottom_friction = 'icy'
						for particle in tile.attached_list:
							if particle.rect.centery >= tile.rect.centery:
								particle.image.fill(options.ICE)
								particle.frozen = True
					tile.apply_ice()

		for particle in sprites.active_particle_list:
			if particle.type in ('debris', 'mallow'):
				if particle.rect.colliderect(collision_rect):
					particle.image.fill(options.ICE)
					particle.frozen = True

		for tile in sprites.tile_list:
				if tile.type == 'mallow':
					if tile.rect.colliderect(collision_rect):
						if tile.inverted is False:
							if self.rect.top < tile.rect.top:
								startxy = (self.rect.centerx, tile.rect.top + 3)
								sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, True, 1.1)
								break

						else:
							if self.rect.bottom > tile.rect.bottom:
								startxy = (self.rect.centerx, tile.rect.bottom - 3)
								sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, True, 1.1)
								break

	def collect_stats(self, ninja):
		if ninja == self.ninja:
			self.ninja.stats_ice_bomb_self_cubes += 1

			try:
				self.ninja.stats_ice_bomb_cubes_made += 1
			except AttributeError:
				pass


			self.kill_count += 1
			try:
				if self.kill_count == 2:
					self.ninja.stats_ice_bomb_double_cubes += 1
							
				if self.kill_count == 3:
					self.ninja.stats_ice_bomb_triple_cubes += 1

				if self.kill_count == 4:
					self.ninja.stats_ice_bomb_quadruple_cubes += 1

			except AttributeError:
				pass

			ninja.stats_ice_bomb_times_frozen += 1



class Volt_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)


		self.ninja = ninja


		#Needed to help sort online play.
		self.online_ID = self.ninja.item_key_number
		self.ninja.item_dict[self.online_ID] = self
		self.ninja.item_key_number += 1

		#self.predictive_collision_list = [] #holds list of ninjas scheduled to die next frame. They must die to keep games in line.


		self.image_number = 0
		self.frame_counter = 0

		self.image_list = []

		
		image = self.ninja.spritesheet.getImage(253, 98, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(302, 98, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(351, 98, 48, 48)
		self.image_list.append(image)


		#for image in self.image_list:
		#	image.fill(options.GREEN)

		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		#self.true_x = self.rect.x
		#self.true_y = self.rect.y

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.active = False
		self.volt_timer = 0
		self.kill_count = 0

		self.brief_delay = 0 #just used to avoid killing one in volt vs volt contact.
		self.delay_max = 60 #max brief_dealy

		self.particle_timer = 0

	def update(self):
		if self.active is True:

			self.visible = 1
			self.volt_timer += 1

			self.frame_counter += 1

			
			if self.particle_timer == 0:
				sprites.particle_generator.volt_main_particle(self, None)
				
			self.particle_timer += 1
			if self.particle_timer >= 25:
				self.particle_timer = 0


			if self.frame_counter >= 15:
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number >= len(self.image_list):
					self.image_number = 0

				self.image = self.image_list[self.image_number]

			self.rect.centerx = self.ninja.rect.centerx
			self.rect.centery = self.ninja.rect.centery

			self.dirty = 1

			self.collision_check()

			if self.volt_timer > 600:
					self.ninja.item = ''
					self.reset()

	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.active = False
		self.volt_timer = 0
		self.kill_count = 0
		self.particle_timer = 0

	def collision_check(self):
		collision_rect1 = pygame.Rect(self.rect.x + 12, self.rect.y, self.rect.width - 24, self.rect.height)
		collision_rect2 = pygame.Rect(self.rect.x + 4, self.rect.y + 10, self.rect.width - 8, self.rect.height - 20)
		
		if self.brief_delay > 0:
			self.brief_delay -= 1

		for ninja in sprites.ninja_list:
			if ninja != self.ninja:
				if collision_rect1.colliderect(ninja.rect) or collision_rect2.colliderect(ninja.rect):
					if ninja.volt_sprite.active is True:

							self.brief_delay = self.delay_max
							ninja.volt_sprite.brief_delay = self.delay_max
							sounds.mixer.volt.play()
							self.ninja.item = ''
							self.reset()
							ninja.volt_sprite.reset()
							ninja.item = ''

					else:
						if self.brief_delay == 0:
							sounds.mixer.volt.play()
							if ninja.shield_sprite.active is False:
									ninja.activate_death_sprite('volt', self)
									self.ninja.stats_volt_kills += 1
									if self.ninja.color == ninja.color:
										self.ninja.stats_ally_item_kill += 1
									else:
										self.ninja.score_item_kills()
									self.kill_count += 1
									if self.kill_count == 2:
										self.ninja.stats_volt_double_kills += 1
									elif self.kill_count == 3:
										self.ninja.stats_volt_triple_kills += 1


		for enemy in sprites.enemy_list:
				if 'volt' in enemy.death_list:
					if collision_rect1.colliderect(enemy.collision_dict['death']) or collision_rect2.colliderect(enemy.collision_dict['death']):
						enemy.destroy()

	def collect_stats(self, ninja):
		self.ninja.stats_volt_kills += 1
		if self.ninja.color == ninja.color:
			self.ninja.stats_ally_item_kill += 1
		else:
			self.ninja.score_item_kills()
		self.kill_count += 1
		if self.kill_count == 2:
			self.ninja.stats_volt_double_kills += 1
		elif self.kill_count == 3:
			self.ninja.stats_volt_triple_kills += 1

class Ice_Cube_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.ice_cube_big = self.ninja.spritesheet.getImage(228, 98, 24, 48)
		self.ice_cube_big.set_alpha(200)
		self.ice_cube_small = self.ninja.spritesheet.getImage(203, 98, 24, 24)
		self.ice_cube_small.set_alpha(200)

		self.image = self.ice_cube_big
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
			self.ninja.status = 'frozen'
			self.visible = 1
			self.dirty = 1
			self.cube_timer -= 1
			if self.cube_timer == 0:
				sprites.particle_generator.break_ice_particles(self.rect, self.ninja.inverted_g, 'snow_finish')
				sounds.mixer.shatter.play()
				self.reset()

			self.collision_check()

			self.rect.centerx = self.ninja.rect.centerx
			if self.ninja.inverted_g is False:
				self.rect.bottom = self.ninja.rect.bottom
			else:
				self.rect.top = self.ninja.rect.top

			

	def freeze_ninja(self):
		self.cube_timer = 300
		self.ninja.on_fire = False
		if self.ninja.status != 'frozen':
			sounds.mixer.freeze.play()
			if self.ninja.rect.height == 24:
				self.image = self.ice_cube_small
				self.rect = self.image.get_rect()

				self.ninja.frozen_image_small.fill((0,255,0))
				self.ninja.frozen_image_small.blit(self.ninja.image, (0,0))
				self.ninja.frozen_image = self.ninja.frozen_image_small


			else:
				self.image = self.ice_cube_big
				self.rect = self.image.get_rect()

				self.ninja.frozen_image_big.fill((0,255,0))
				self.ninja.frozen_image_big.blit(self.ninja.image, (0,0))
				self.ninja.frozen_image = self.ninja.frozen_image_big

			if self.ninja.inverted_g is True:
				self.ninja.frozen_image = pygame.transform.flip(self.ninja.frozen_image, False, True)
			self.ninja.frozen_image.set_colorkey((0,255,0))
			self.ninja.status = 'frozen'
			self.active = True
		

	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.active = False
		self.cube_timer = 0
		if self.ninja.status != 'lose':
			if self.ninja.rect.height == 24: #ninja was ducking/jumping
				self.ninja.status = 'jump'
			else: #ninja was upright
				self.ninja.status = 'idle'

	def collision_check(self):
		pass
		#moved to level collision check.

class Rocket_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja
		self.type = 'rocket'
		self.portal_delay = 0

		#Needed to help sort online play.
		self.online_ID = self.ninja.item_key_number
		self.ninja.item_dict[self.online_ID] = self
		self.ninja.item_key_number += 1
		self.online_counter = 0

		#self.predictive_collision_list = [] #holds list of ninjas scheduled to die next frame. They must die to keep games in line.


		self.image_number = 0
		self.frame_counter = 0

		self.up_image_list = []
		self.up_left_image_list = []
		self.up_right_image_list = []
		self.left_image_list = []
		self.right_image_list = []
		self.down_left_image_list = []
		self.down_right_image_list = []
		self.down_image_list = []

		self.up_up_right_image_list = []
		self.up_up_left_image_list = []
		self.up_right_right_image_list = []
		self.up_left_left_image_list = []
		self.down_down_right_image_list = []
		self.down_down_left_image_list = []
		self.down_right_right_image_list = []
		self.down_left_left_image_list = []

		#right weird angles:
		image = self.ninja.spritesheet.getImage(196, 198, 13, 20)
		self.up_up_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		self.up_up_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(224, 198, 13, 20)
		self.up_up_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		self.up_up_right_image_list.append(image)

		image = self.ninja.spritesheet.getImage(239, 204, 20, 14)
		self.up_right_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		self.up_right_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(283, 204, 20, 14)
		self.up_right_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		self.up_right_right_image_list.append(image)

		image = self.ninja.spritesheet.getImage(196, 198, 13, 20)
		image = pygame.transform.flip(image, False, True)
		self.down_down_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		image = pygame.transform.flip(image, False, True)
		self.down_down_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(224, 198, 13, 20)
		image = pygame.transform.flip(image, False, True)
		self.down_down_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		image = pygame.transform.flip(image, False, True)
		self.down_down_right_image_list.append(image)

		image = self.ninja.spritesheet.getImage(239, 204, 20, 14)
		image = pygame.transform.flip(image, False, True)
		self.down_right_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		image = pygame.transform.flip(image, False, True)
		self.down_right_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(283, 204, 20, 14)
		image = pygame.transform.flip(image, False, True)
		self.down_right_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		image = pygame.transform.flip(image, False, True)
		self.down_right_right_image_list.append(image)

		#left weird angles:
		image = self.ninja.spritesheet.getImage(196, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		self.up_up_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		self.up_up_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(224, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		self.up_up_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		self.up_up_left_image_list.append(image)

		image = self.ninja.spritesheet.getImage(239, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		self.up_left_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		self.up_left_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(283, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		self.up_left_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		self.up_left_left_image_list.append(image)

		image = self.ninja.spritesheet.getImage(196, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_down_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_down_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(224, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_down_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(210, 198, 13, 20)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_down_left_image_list.append(image)

		image = self.ninja.spritesheet.getImage(239, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_left_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_left_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(283, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_left_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(261, 204, 20, 14)
		image = pygame.transform.flip(image, True, False)
		image = pygame.transform.flip(image, False, True)
		self.down_left_left_image_list.append(image)


		image = self.ninja.spritesheet.getImage(253, 147, 13, 22)
		image = pygame.transform.rotate(image, 90)
		self.left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		image = pygame.transform.rotate(image, 90)
		self.left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(281, 147, 13, 22)
		image = pygame.transform.rotate(image, 90)
		self.left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		image = pygame.transform.rotate(image, 90)
		self.left_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 147, 13, 22)
		image = pygame.transform.rotate(image, -90)
		self.right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		image = pygame.transform.rotate(image, -90)
		self.right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(281, 147, 13, 22)
		image = pygame.transform.rotate(image, -90)
		self.right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		image = pygame.transform.rotate(image, -90)
		self.right_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 147, 13, 22)
		self.up_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		self.up_image_list.append(image)
		image = self.ninja.spritesheet.getImage(281, 147, 13, 22)
		self.up_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		self.up_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 147, 13, 22)
		image = pygame.transform.flip(image, False, True)
		self.down_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		image = pygame.transform.flip(image, False, True)
		self.down_image_list.append(image)
		image = self.ninja.spritesheet.getImage(281, 147, 13, 22)
		image = pygame.transform.flip(image, False, True)
		self.down_image_list.append(image)
		image = self.ninja.spritesheet.getImage(267, 147, 13, 22)
		image = pygame.transform.flip(image, False, True)
		self.down_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 187, 16, 16)
		self.up_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 187, 16, 16)
		self.up_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(287, 187, 16, 16)
		self.up_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 187, 16, 16)
		self.up_left_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 170, 16, 16)
		self.up_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 170, 16, 16)
		self.up_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(287, 170, 16, 16)
		self.up_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 170, 16, 16)
		self.up_right_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 187, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 187, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(287, 187, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_left_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 187, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_left_image_list.append(image)

		image = self.ninja.spritesheet.getImage(253, 170, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 170, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(287, 170, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_right_image_list.append(image)
		image = self.ninja.spritesheet.getImage(270, 170, 16, 16)
		image = pygame.transform.flip(image, False, True)
		self.down_right_image_list.append(image)

		self.ninja.big_image_list.append(self.up_image_list)
		self.ninja.big_image_list.append(self.up_left_image_list)
		self.ninja.big_image_list.append(self.up_right_image_list)
		self.ninja.big_image_list.append(self.left_image_list)
		self.ninja.big_image_list.append(self.right_image_list)
		self.ninja.big_image_list.append(self.down_left_image_list)
		self.ninja.big_image_list.append(self.down_right_image_list)
		self.ninja.big_image_list.append(self.down_image_list)
		self.ninja.big_image_list.append(self.up_up_right_image_list)
		self.ninja.big_image_list.append(self.up_up_left_image_list)
		self.ninja.big_image_list.append(self.up_right_right_image_list)
		self.ninja.big_image_list.append(self.up_left_left_image_list)
		self.ninja.big_image_list.append(self.down_down_right_image_list)
		self.ninja.big_image_list.append(self.down_down_left_image_list)
		self.ninja.big_image_list.append(self.down_right_right_image_list)
		self.ninja.big_image_list.append(self.down_left_left_image_list)

		self.explosion_list = []
		image = self.ninja.spritesheet.getImage(250, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(299, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(348, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(397, 295, 48, 48)
		self.explosion_list.append(image)
		image = self.ninja.spritesheet.getImage(446, 295, 48, 48)
		self.explosion_list.append(image)


		self.image = self.up_image_list[0]
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.status = '' #'', 'fired', 'explode'
		self.explode_timer = 0
		self.direction = 'up' #'up', 'left', 'right'

		self.true_x = 0 #holds true rectx... can be a decimal place.
		self.true_y = 0 #holds true recty... can be a decimal place.

		self.tail_point = (0,0) #holds 'tail' of rocket

		self.straight_speed = 2
		self.angle_speed = math.sin(math.radians(45)) * self.straight_speed

		self.big_angle_speed = abs(math.cos(math.radians(22.5))) * self.straight_speed
		self.small_angle_speed = abs(math.sin(math.radians(22.5))) * self.straight_speed

		self.angle = 0 #0 - 360. starts up. Helps select image.
		self.angle_change = 2.5

		self.up_input = False
		self.right_input = False
		self.down_input = False
		self.left_input = False
		
		self.channel = None #holds current channel of rocket sound.
		self.timer = 0

		self.explosion_seed = random.randrange(0,10000,1)
		self.kill_count = 0

		self.inverted_g = False #only used for creating particles
		self.explode_delay = 0


	def update(self):
		if self.portal_delay > 0:
			self.portal_delay -= 1

		if self.status == 'fired':
			self.timer += 1
			self.rotate()
			self.update_image()
			self.dirty = 1
			self.frame_counter += 1
			if self.frame_counter > 10:
				self.image_number += 1
				self.frame_counter = 0

			if self.image_number >= len(self.up_image_list):
				self.image_number = 0

			mod = 3 #offset for 'weird angle' smoke

			if self.direction == 'up':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)

				self.true_y -= self.straight_speed
				self.tail_point = (self.rect.centerx,self.rect.bottom)

			elif self.direction == 'up_up_left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_up_left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y -= self.big_angle_speed
				self.true_x -= self.small_angle_speed
				self.tail_point = (self.rect.right - mod, self.rect.bottom)

			elif self.direction == 'up_left_left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_left_left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y -= self.small_angle_speed
				self.true_x -= self.big_angle_speed
				self.tail_point = (self.rect.right, self.rect.bottom - mod)


			elif self.direction == 'up_left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y -= self.angle_speed
				self.true_x -= self.angle_speed
				self.tail_point = (self.rect.bottomright)

			elif self.direction == 'up_right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y -= self.angle_speed
				self.true_x += self.angle_speed
				self.tail_point = (self.rect.bottomleft)

			elif self.direction == 'up_right_right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_right_right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y -= self.small_angle_speed
				self.true_x += self.big_angle_speed
				self.tail_point = (self.rect.left, self.rect.bottom - mod)

			elif self.direction == 'up_up_right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.up_up_right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y -= self.big_angle_speed
				self.true_x += self.small_angle_speed
				self.tail_point = (self.rect.left + mod, self.rect.bottom)


			elif self.direction == 'left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)

				self.true_x -= self.straight_speed
				self.tail_point = (self.rect.midright)

			elif self.direction == 'right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)

				self.true_x+= self.straight_speed
				self.tail_point = (self.rect.midleft)

			elif self.direction == 'down_left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y += self.angle_speed
				self.true_x -= self.angle_speed
				self.tail_point = (self.rect.right, self.rect.top)


			elif self.direction == 'down_left_left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_left_left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y += self.small_angle_speed
				self.true_x -= self.big_angle_speed
				self.tail_point = (self.rect.right, self.rect.top + mod)

			elif self.direction == 'down_down_left':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_down_left_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y += self.big_angle_speed
				self.true_x -= self.small_angle_speed
				self.tail_point = (self.rect.right - mod, self.rect.top)

			elif self.direction == 'down_right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y += self.angle_speed
				self.true_x += self.angle_speed
				self.tail_point = (self.rect.left, self.rect.top)

			elif self.direction == 'down_right_right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_right_right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y += self.small_angle_speed
				self.true_x += self.big_angle_speed
				self.tail_point = (self.rect.left, self.rect.top + mod)

			elif self.direction == 'down_down_right':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_down_right_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)
				self.true_y += self.big_angle_speed
				self.true_x += self.small_angle_speed
				self.tail_point = (self.rect.left + mod, self.rect.top)

			elif self.direction == 'down':
				oldx = self.true_x
				oldy = self.true_y
				self.image = self.down_image_list[self.image_number]
				self.rect = self.image.get_rect()
				self.rect.centerx = round(oldx)
				self.rect.centery = round(oldy)

				self.true_y += self.straight_speed

				self.tail_point = (self.rect.centerx,self.rect.top)

			self.rect.centerx = round(self.true_x)
			self.rect.centery = round(self.true_y)

			self.ninja.stats_rocket_pixels_travelled += self.straight_speed


			#self.tail_point = (self.rect.centerx, self.rect.centery)
			sprites.particle_generator.rocket_particles(self.tail_point,self.direction)

			if self.ninja.status != 'rocket' and self.explode_delay == 0:
					self.explode_delay = 20
					#self.explode()
			
			if self.explode_delay > 0:
					self.explode_delay -= 1
					if self.explode_delay == 0:
						self.explode()


			self.collision_check()

			self.boundary_check()

			for ninja in sprites.ninja_list:
					if ninja.shield_sprite.active is True:
						ninja.shield_sprite.collision_check(self)


		
		elif self.status == 'explode':
			#self.frame_counter += 1

			#if self.frame_counter >= 3:
			self.image_number += 1

			sprites.particle_generator.radial_explosion_particles(self.rect.center, self.ninja.inverted_g, self.explosion_seed, 'smoke_finish')

			if self.image_number >= len(self.explosion_list):
				self.reset()
			else:
				self.image = self.explosion_list[self.image_number]

			self.dirty = 1

			#push rope points based on collision center
			for rope in sprites.level_ropes:
				for point in rope.point_list:
					if self.rect.collidepoint(point.rect.center):
						point.explosion_force(self.rect.center)

			self.kill_check()

	def boundary_check(self):
		if self.ninja.loop_physics is True:
			if self.rect.bottom < 0:
				if self.direction in ('up', 'up_left', 'up_up_left', 'up_left_left', 'up_right', 'up_up_right', 'up_right_right'):
					self.rect.top = sprites.size[1]
					self.true_x  = self.rect.centerx
					self.true_y = self.rect.centery

			if self.rect.top > sprites.size[1]:
				if self.direction in ('down', 'down_left', 'down_down_left', 'down_left_left', 'down_right', 'down_down_right', 'down_right_right'): 
					self.rect.bottom = 0
					self.true_x  = self.rect.centerx
					self.true_y = self.rect.centery

			if self.rect.right < 0 :
				if self.direction in ('left', 'up_left', 'up_left_left', 'up_up_left', 'down_left', 'down_down_left', 'down_left_left'):
					self.rect.left = sprites.size[0]
					self.true_x  = self.rect.centerx
					self.true_y = self.rect.centery

			if self.rect.left > sprites.size[0] :
				if self.direction in ('right', 'up_right', 'up_right_right', 'up_up_right', 'down_right', 'down_down_right', 'down_right_right'):
					self.rect.right = 0
					self.true_x  = self.rect.centerx
					self.true_y = self.rect.centery

	def reset(self):
		self.online_counter = 0
		self.explode_delay = 0
		self.kill_count = 0
		self.visible = 0
		self.dirty = 1
		self.status = ''
		self.explode_timer = 0
		self.direction = 'up'
		self.angle = 0
		self.up_input = False
		self.right_input = False
		self.down_input = False
		self.left_input = False
		self.timer = 0
		self.explosion_seed = random.randrange(0,10000,1)

		try:
			self.channel.stop()
		except:
			pass
			#print('rocket channel is inactive')

		try:
			sprites.active_items.remove(self)
		except ValueError:
			pass

	def fire_rocket(self):
		if self.status != 'fired':
			self.ninja.stats_rocket_fired += 1

			self.inverted_g = self.ninja.inverted_g

			sprites.active_items.append(self)

			if self.ninja.inverted_g is False:
				self.image = self.up_image_list[0]
				self.rect = self.image.get_rect()
				self.rect.bottom = self.ninja.rect.top + 24
				self.rect.centerx = self.ninja.rect.centerx
				self.angle = 0
				self.direction = 'up'
			else:
				self.image = self.down_image_list[0]
				self.rect = self.image.get_rect()
				self.rect.top = self.ninja.rect.bottom - 24
				self.rect.centerx = self.ninja.rect.centerx
				self.angle = 180
				self.direction = 'down'

			self.status = 'fired'
			self.visible = 1
			self.true_y = self.rect.centery
			self.true_x = self.rect.centerx
			self.ninja.item = ''
			self.timer = 0

			self.channel = sounds.mixer.rocket.play(loops=-1)

	def collision_check(self):
		for ninja in sprites.ninja_list:
				if ninja.shield_sprite.active is False:
					if ninja.collision_rect.colliderect(self.rect):
						if ninja != self.ninja:
							self.explode()

							break
						elif ninja == self.ninja and self.timer > 14:
							self.explode()

							break

		


		#only rocket owner can allow rocket to explode on tiles.
		if 1 == 1:

			for enemy in sprites.enemy_list:
				temp_rect = pygame.Rect(enemy.rect.x + 2, enemy.rect.y + 2, enemy.rect.width - 4, enemy.rect.height - 4)
				if temp_rect.colliderect(self.rect):
					self.explode()
					break


			for item in sprites.active_items:
				if item != self:
					if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
						if item.status != '' and item.status != 'explode':
							if item.rect.colliderect(self.rect):
								item.explode()
								self.explode()

								break
			
			#make sure no portal collision bofore doing tile checks
			check_tiles = True
			for item in sprites.active_items:
				if item.type == 'portal_gun_portal':
					if self.rect.colliderect(item.collision_rect):
						if len(item.portal_gun.active_portal_list) == 2: #portal to teleport to!
							check_tiles = False
							break

			if check_tiles is True and self.portal_delay == 0:
				for tile in sprites.tile_list:
					if tile.type == 'tile' or tile.type == 'mallow_wall' or tile.type == 'mallow':
						if tile.rect.colliderect(self.rect):
							self.explode()


	def explode(self):


		if sprites.shake_handler.current_shake < 2:
			sprites.shake_handler.current_shake = 2

		sounds.mixer.explosion.play()
		self.channel.stop()

		self.status = 'explode'
		self.frame_counter = 0
		self.image_number = 0

		centerx = self.rect.centerx
		centery = self.rect.centery

		self.image = self.explosion_list[0]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery

		if self.ninja.status == 'rocket':
			self.ninja.status = 'idle'

		#tile reaction(only triggered first frame)
		collision_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		for tile in sprites.tile_list: #unfreeze frozen tiles
			if tile.type == 'tile' or tile.type == 'platform':
				if tile.rect.colliderect(collision_rect):
					if tile.breakable is True:
						tile.destroy(self)
					else:
						if tile.rect.top > collision_rect.top:
							tile.top_friction = 'normal'
							for particle in tile.attached_list:
								if particle.rect.centery <= tile.rect.centery:
									particle.image.fill(particle.color)
									particle.frozen = False
						if tile.rect.bottom < collision_rect.bottom:
							tile.bottom_friction = 'normal'
							for particle in tile.attached_list:
								if particle.rect.centery >= tile.rect.centery:
									particle.image.fill(particle.color)
									particle.frozen = False
						tile.apply_ice()

		for particle in sprites.active_particle_list:
			if particle.type in ('debris', 'mallow'):
				if particle.rect.colliderect(collision_rect):
					particle.image.fill(particle.color)
					particle.frozen = False

		for tile in sprites.tile_list:
			if tile.type == 'mallow':
				if tile.rect.colliderect(collision_rect):
					if tile.inverted is False:
						if self.rect.top < tile.rect.top:
							startxy = (self.rect.centerx, tile.rect.top + 3)
							sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, False, 1)
							break

					else:
						if self.rect.bottom > tile.rect.bottom:
							startxy = (self.rect.centerx, tile.rect.bottom - 3)
							sprites.particle_generator.bomb_FID_particles(startxy, tile.inverted, self, False, 1)
							break

	def kill_check(self):
		collision_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6)
		for ninja in sprites.ninja_list:
			if ninja.rect.colliderect(collision_rect):
				if ninja.shield_sprite.active is False:
						ninja.activate_death_sprite('explosion', self)
						if self.ninja == ninja:
							self.ninja.stats_rocket_suicides += 1
						else:
							self.ninja.stats_rocket_kills += 1
							if self.ninja.color == ninja.color:
								self.ninja.stats_ally_item_kill += 1
							else:
								self.ninja.score_item_kills()
							self.kill_count += 1
							if self.kill_count == 2:
								self.ninja.stats_rocket_double_kills += 1
							elif self.kill_count == 3:
								self.ninja.stats_rocket_triple_kills += 1



		for item in sprites.active_items:
			if item != self:
				if item.type == 'bomb' or item.type == 'mine' or item.type == 'rocket':
					if item.status != '' and item.status != 'explode':
						if item.rect.colliderect(collision_rect):
							item.explode()


		for enemy in sprites.enemy_list:
				if 'explosion' in enemy.death_list:
					if collision_rect.colliderect(enemy.collision_dict['death']):
						enemy.destroy()



	def collect_stats(self, ninja):
		if self.ninja == ninja:
			self.ninja.stats_rocket_suicides += 1
		else:
			self.ninja.stats_rocket_kills += 1
			if self.ninja.color == ninja.color:
				self.ninja.stats_ally_item_kill += 1
			else:
				self.ninja.score_item_kills()
			self.kill_count += 1
			if self.kill_count == 2:
				self.ninja.stats_rocket_double_kills += 1
			elif self.kill_count == 3:
				self.ninja.stats_rocket_triple_kills += 1

	
	def rotate(self):
		if self.up_input is True and self.right_input is True:
			if self.angle >= 45 and self.angle <= 225:
				self.angle -= self.angle_change
			elif self.angle >= 225 or self.angle <= 45:
				self.angle += self.angle_change

		elif self.up_input is True and self.left_input is True:
			if self.angle >= 315 or self.angle <= 135:
				self.angle -= self.angle_change
			elif self.angle >= 135 and self.angle <= 315:
				self.angle += self.angle_change

		elif self.down_input is True and self.left_input is True:
			if self.angle >= 45 and self.angle <= 225:
				self.angle += self.angle_change
			elif self.angle <= 45 or self.angle >= 225:
				self.angle -= self.angle_change

		elif self.down_input is True and self.right_input is True:
			if self.angle >= 315 or self.angle <= 135:
				self.angle += self.angle_change
			elif self.angle >= 135 and self.angle <= 315:
				self.angle -= self.angle_change
		
		else:
			if self.up_input is True:
				if self.angle >= 0 and self.angle <= 180:
					self.angle -= self.angle_change
				elif self.angle >= 180 and self.angle <= 360:
					self.angle += self.angle_change

			if self.down_input is True:
				if self.angle >= 0 and self.angle <= 180:
					self.angle += self.angle_change
				elif self.angle >= 180 and self.angle <= 360:
					self.angle -= self.angle_change

			if self.left_input is True:
				if self.angle >= 270 or self.angle <= 90:
					self.angle -= self.angle_change
				elif self.angle <= 270 and self.angle >= 90:
					self.angle += self.angle_change

			if self.right_input is True:
				if self.angle >= 270 or self.angle <= 90:
					self.angle += self.angle_change
				elif self.angle <= 270 and self.angle >= 90:
					self.angle -= self.angle_change

	def update_image(self):
		if self.angle < 0:
			self.angle = 360 + self.angle

		elif self.angle > 360:
			self.angle -= 360

		if self.angle >= 348.75 or self.angle <= 11.25:
			self.direction = 'up'

		elif self.angle >= 11.25 and self.angle <= 33.75:
			self.direction = 'up_up_right'

		elif self.angle >= 33.75 and self.angle <= 56.25:
			self.direction = 'up_right'

		elif self.angle >= 56.25 and self.angle <= 78.75:
			self.direction = 'up_right_right'

		elif self.angle >= 78.75 and self.angle <= 101.25:
			self.direction = 'right'

		elif self.angle >= 101.25 and self.angle <= 123.75:
			self.direction = 'down_right_right'

		elif self.angle >= 123.75 and self.angle <= 146.25:
			self.direction = 'down_right'

		elif self.angle >= 146.25 and self.angle <= 168.75:
			self.direction = 'down_down_right'

		elif self.angle >= 168.75 and self.angle <= 191.25:
			self.direction = 'down'

		elif self.angle >= 191.25 and self.angle <= 213.75:
			self.direction = 'down_down_left'

		elif self.angle >= 213.75 and self.angle <= 236.25:
			self.direction = 'down_left'

		elif self.angle >= 236.25 and self.angle <= 258.75:
			self.direction = 'down_left_left'

		elif self.angle >= 258.75 and self.angle <= 281.25:
			self.direction = 'left'

		elif self.angle >= 281.25 and self.angle <= 303.75:
			self.direction = 'up_left_left'

		elif self.angle >= 303.75 and self.angle <= 326.25:
			self.direction = 'up_left'

		elif self.angle >= 326.25 and self.angle <= 348.75:
			self.direction = 'up_up_left'



class Shield_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, ninja):

		pygame.sprite.DirtySprite.__init__(self)

		self.ninja = ninja

		self.image_number = 0
		self.frame_counter = 0

		self.image_list = []

		
		image = self.ninja.spritesheet.getImage(328, 246, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(377, 246, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(426, 246, 48, 48)
		self.image_list.append(image)
		image = self.ninja.spritesheet.getImage(377, 246, 48, 48)
		self.image_list.append(image)

		self.ninja.big_image_list.append(self.image_list)

		self.image = self.image_list[0]
		self.rect = self.image.get_rect()

		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 2)

		sprites.item_effects.add(self) #this group holds the item for collision checks and updating.

		self.visible = 0
		self.dirty = 1

		self.active = False
		self.shield_timer = 0


	def update(self):
		if self.active is True:
			self.dirty = 1
			self.visible = 1
			self.shield_timer += 1

			self.frame_counter += 1

			if self.frame_counter >= 10:
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number >= len(self.image_list):
					self.image_number = 0

				self.image = self.image_list[self.image_number]

			self.rect.centerx = self.ninja.rect.centerx
			self.rect.centery = self.ninja.rect.centery

			
			#collision check passed off to each item
			#self.collision_check()

			if self.shield_timer > 600 or self.ninja.status == 'lose':
					self.reset()

	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.active = False
		self.shield_timer = 0

	def activate(self,spawn=False):
		self.shield_timer = 0
		self.active = True
		sounds.mixer.shield.play()

		if spawn is True: #shorter shield duration for spawn.
			self.shield_timer = 420 #normally 10 seconds. This makes it 3 seconds

	def collision_check(self, item):
		collision_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4)
		top_rect =  pygame.Rect(self.rect.x + 10, self.rect.y + 2, self.rect.width - 20, 10)
		bottom_rect =  pygame.Rect(self.rect.x + 10, self.rect.bottom -12, self.rect.width - 20, 10)
		left_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 2, 10, self.rect.height - 4)
		right_rect = pygame.Rect(self.rect.right - 15, self.rect.y + 2, 10, self.rect.height - 4)

		if item.type == 'laser':
			if (item.ninja != self.ninja) or (item.timer > 2): #don't want to collide with own shield. But want other lasers to bounce immediately.
				if item.rect.colliderect(collision_rect):
					self.ninja.stats_shield_weapons_rebounded += 1
					if item.timer <= 4:#makes rebounded lasers kill ninjas at short range.
						item.timer = 4 
					if item.change_x > 0:
						item.rect.right = self.rect.left
						item.true_x = item.rect.x
						item.change_x *= -1
						sprites.particle_generator.laser_particles((item.rect.right,item.rect.centery), 'horizontal', item.ninja.color[1])
					elif item.change_x < 0:
						item.rect.left = self.rect.right
						item.true_x = item.rect.x
						item.change_x *= -1
						sprites.particle_generator.laser_particles((item.rect.left,item.rect.centery), 'horizontal', item.ninja.color[1])
					elif item.change_y > 0:
						item.rect.bottom = self.rect.top
						item.true_y = item.rect.y
						item.change_y *= -1
						sprites.particle_generator.laser_particles((item.rect.centerx,item.rect.bottom), 'vertical', item.ninja.color[1])
					elif item.change_y < 0:
						item.rect.top = self.rect.bottom
						item.true_y = item.rect.y
						item.change_y *= -1
						sprites.particle_generator.laser_particles((item.rect.centerx,item.rect.top), 'vertical', item.ninja.color[1])

					#special scenrio when it hits multiple shields.
					for ninja in sprites.ninja_list:
						if ninja != self.ninja:
							if ninja.shield_sprite.active is True:
								other_collision_rect = pygame.Rect(ninja.shield_sprite.rect.x + 2, ninja.shield_sprite.rect.y + 2, ninja.shield_sprite.rect.width - 4, ninja.shield_sprite.rect.height - 4)
								if item.rect.colliderect(other_collision_rect):

									if ninja.rect.x > self.ninja.rect.x:
										if item.change_x > 0:
											old_x = ninja.shield_sprite.rect.left
										else:
											old_x = self.ninja.shield_sprite.rect.right
									else:
										if item.change_x > 0:
											old_x = self.ninja.shield_sprite.rect.left
										else:
											old_x = ninja.shield_sprite.rect.right

									if ninja.inverted_g is False:
										item.image = item.laser_image_vertical
										item.rect = item.image.get_rect()
										item.rect.bottom = self.rect.top
										item.rect.centerx = old_x
										item.true_x = item.rect.x
										item.true_y = item.rect.y
										item.change_y = -item.laser_speed
										item.change_x = 0
											
									else:
										item.image = item.laser_image_vertical
										item.rect = item.image.get_rect()
										item.rect.top = self.rect.bottom
										item.rect.centerx = old_x
										item.true_x = item.rect.x
										item.true_y = item.rect.y
										item.change_y = item.laser_speed
										item.change_x = 0

			item.collision_check() #bonus collision check to allow rebounded lasers change to kill immediately short range.

		if item.type == 'portal_gun_bubble':

			if item.rect.colliderect(collision_rect):
				self.ninja.stats_shield_weapons_rebounded += 1
				if item.rect.colliderect(top_rect):
					item.rect.bottom = self.rect.top
					item.true_y = item.rect.y
					item.direction = 'vertical'
					item.change_y = item.y_speed * -1
					item.change_x = item.x_speed

				elif item.rect.colliderect(bottom_rect):
					item.rect.top = self.rect.bottom
					item.true_y = item.rect.y
					item.direction = 'vertical'
					item.change_y = item.y_speed
					item.change_x = item.x_speed

				elif item.rect.colliderect(left_rect):
					item.rect.right = self.rect.left
					item.true_x = item.rect.x
					item.direction = 'horizontal'
					item.change_y = item.y_speed * -1
					item.change_x = item.x_speed * -1

				elif item.rect.colliderect(right_rect):
					item.rect.left = self.rect.right
					item.true_x = item.rect.x
					item.direction = 'horizontal'
					item.change_y = item.y_speed * -1
					item.change_x = item.x_speed
				item.base_x = self.rect.centerx
				item.base_y = self.rect.centery

		elif item.type == 'rocket' and item.status != '' and item.status != 'explode' and item.timer > 10:
			if item.rect.colliderect(collision_rect):
				item.timer = 5
				self.ninja.stats_shield_weapons_rebounded += 1
				if item.rect.colliderect(top_rect):
					item.rect.bottom = self.rect.top
					item.true_y = item.rect.y
					item.angle = 0

				elif item.rect.colliderect(bottom_rect):
					item.rect.top = self.rect.bottom
					item.true_y = item.rect.y
					item.angle = 180

				elif item.rect.colliderect(left_rect):
					item.rect.right = self.rect.left
					item.true_x = item.rect.x
					item.angle = 270

				elif item.rect.colliderect(right_rect):
					item.rect.left = self.rect.right
					item.true_x = item.rect.x
					item.angle = 90

				item.update_image()

		elif item.type == 'bomb' or item.type == 'mine':
			if item.status != 'explode':
				if item.rect.colliderect(collision_rect):
					self.ninja.stats_shield_weapons_rebounded += 1
					if item.rect.colliderect(top_rect):
						test_point = (item.rect.centerx,collision_rect.top - 1)
						explode = False
						for tile in sprites.tile_list:
							if tile.type == 'tile' or tile.type == 'platform':
								if tile.rect.collidepoint(test_point):
									item.explode()

									explode = True
									break
						if explode is False:
							item.rect.bottom = collision_rect.top
							item.true_y = item.rect.y
							item.change_y *= -1
							if item.change_y > -2:
								item.change_y = -2
							for tile in sprites.tile_list:
								if tile.type == 'tile' or tile.type == 'platform':
									if item.rect.colliderect(tile.rect):
										if item.rect.centerx < self.rect.centerx - 6:
											item.rect.centerx -= 3
											item.rect.top = tile.rect.bottom
											item.true_y = item.rect.y
											item.true_x = item.rect.x
										elif item.rect.centerx > self.rect.centerx + 6:
											item.rect.centerx += 3
											item.rect.top = tile.rect.bottom
											item.true_y = item.rect.y
											item.true_x = item.rect.x
										else:
											item.explode()

										break


					elif item.rect.colliderect(bottom_rect):
						test_point = (item.rect.centerx,collision_rect.bottom + 1)
						explode = False
						for tile in sprites.tile_list:
							if tile.type == 'tile' or tile.type == 'platform':
								if tile.rect.collidepoint(test_point):
									item.explode()

									explode = True
									break
						if explode is False:
							item.rect.top = collision_rect.bottom
							item.true_y = item.rect.y
							item.change_y *= -1
							if item.change_y < 2:
								item.change_y = 2
							for tile in sprites.tile_list:
								if tile.type == 'tile' or tile.type == 'platform':
									if item.rect.colliderect(tile.rect):
										if item.rect.centerx < self.rect.centerx - 6:
											item.rect.centerx -= 3
											item.rect.bottom = tile.rect.top
											item.true_y = item.rect.y
											item.true_x = item.rect.x
										elif item.rect.centerx > self.rect.centerx + 6:
											item.rect.centerx += 3
											item.rect.bottom = tile.rect.top
											item.true_y = item.rect.y
											item.true_x = item.rect.x
										else:
											item.explode()

										break



					elif item.rect.colliderect(left_rect):
						test_point = (collision_rect.left - 1,item.rect.centery)
						explode = False
						for tile in sprites.tile_list:
							if tile.type == 'tile' or tile.type == 'platform':
								if tile.rect.collidepoint(test_point):
									item.explode()

									explode = True
									break
						if explode is False:
							item.rect.right = collision_rect.left
							item.true_x = item.rect.x
							item.change_x *= -1
							if item.change_x > -2:
								item.change_x = -2
							for tile in sprites.tile_list:
								if tile.type == 'tile' or tile.type == 'platform':
									if item.rect.colliderect(tile.rect):
										if item.rect.centery <= self.rect.centery:
											item.rect.centery -= 3
										else:
											item.rect.centery += 3
										item.rect.left = tile.rect.right
										item.true_y = item.rect.y
										item.true_x = item.rect.x
										break

					elif item.rect.colliderect(right_rect):
						test_point = (collision_rect.right + 1,item.rect.centery)
						explode = False
						for tile in sprites.tile_list:
							if tile.type == 'tile' or tile.type == 'platform':
								if tile.rect.collidepoint(test_point):
									item.explode()

									explode = True
									break
						if explode is False:
							item.rect.left = collision_rect.right
							item.true_x = item.rect.x
							if item.change_x < 2:
								item.change_x = 2
							for tile in sprites.tile_list:
								if tile.type == 'tile' or tile.type == 'platform':
									if item.rect.colliderect(tile.rect):
										if item.rect.centery <= self.rect.centery:
											item.rect.centery -= 3
										else:
											item.rect.centery += 3
										item.rect.right = tile.rect.left
										item.true_y = item.rect.y
										item.true_x = item.rect.x
										break
