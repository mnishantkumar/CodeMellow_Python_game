#import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame
import options
import random
import sprites
import menus
import data_manager
import copy
import platform


input_handler = None

class Input_Handler():

	#place Ninja attributes here

	def __init__(self):
		#constructor function
		self.os = platform.system()

		#print(platform.system())
		#print(platform.release())
		#print(platform.version())

		self.gamepads = [] #ordered list of gamepads
		self.random_gamepads = [] #gamepads as automatically brought in by cpu.
		self.gamepad_ids = [] #game ids, used for sorting. Found in order of 'button press'
		self.check_gamepads_counter = 0 #used in player select/intro/main menu to check for sytem gamepads 1x/2 seconds.

		#images for buttons.
		self.button_xbox_a = sprites.level_sheet.getImage(0,228,17,17)
		self.button_xbox_x = sprites.level_sheet.getImage(18,228,17,17)
		self.button_xbox_b = sprites.level_sheet.getImage(18,210,17,17)
		self.button_xbox_y = sprites.level_sheet.getImage(0,210,17,17)

		self.button_nintendo_a = sprites.level_sheet.getImage(72,318,17,17)
		self.button_nintendo_x = sprites.level_sheet.getImage(90,318,17,17)
		self.button_nintendo_b = sprites.level_sheet.getImage(90,300,17,17)
		self.button_nintendo_y = sprites.level_sheet.getImage(72,300,17,17)

		self.button_ps_circle = sprites.level_sheet.getImage(36,300,17,17)
		self.button_ps_x = sprites.level_sheet.getImage(36,318,17,17)
		self.button_ps_triangle = sprites.level_sheet.getImage(54,300,17,17)
		self.button_ps_square = sprites.level_sheet.getImage(54,318,17,17)

		self.button_generic_1 = sprites.level_sheet.getImage(72,264,17,17)
		self.button_generic_2 = sprites.level_sheet.getImage(72,282,17,17)
		self.button_generic_3 = sprites.level_sheet.getImage(90,282,17,17)
		self.button_generic_4 = sprites.level_sheet.getImage(90,264,17,17)

		self.button_keyboard_z = sprites.level_sheet.getImage(0,282,17,17)
		self.button_keyboard_x = sprites.level_sheet.getImage(18,282,17,17)
		self.button_keyboard_c = sprites.level_sheet.getImage(0,300,17,17)
		self.button_keyboard_y = sprites.level_sheet.getImage(18,300,17,17)




		self.button_dict = {
							'xbox_a' : self.button_xbox_a,
							'xbox_x' : self.button_xbox_x,
							'xbox_b' : self.button_xbox_b,
							'xbox_y' : self.button_xbox_y,

							'nintendo_a' : self.button_nintendo_a,
							'nintendo_x' : self.button_nintendo_x,
							'nintendo_b' : self.button_nintendo_b,
							'nintendo_y' : self.button_nintendo_y,

							'ps_circle' : self.button_ps_circle,
							'ps_x' : self.button_ps_x,
							'ps_triangle' : self.button_ps_triangle,
							'ps_square' : self.button_ps_square,

							'generic_1' : self.button_generic_1,
							'generic_2' : self.button_generic_2,
							'generic_3' : self.button_generic_3,
							'generic_4' : self.button_generic_4
							}





		self.button_keyboard_left_right = sprites.level_sheet.getImage(0,336,17,17)
		self.button_keyboard_up_down = sprites.level_sheet.getImage(0,318,17,17)

		self.button_gamepad_left_right = sprites.level_sheet.getImage(0,264,17,17)
		self.button_gamepad_up_down = sprites.level_sheet.getImage(0,246,17,17)

		self.gamepad1_ninja = None
		self.gamepad2_ninja = None
		self.gamepad3_ninja = None
		self.gamepad4_ninja = None
		self.gamepad_ninja_list = [self.gamepad1_ninja, self.gamepad2_ninja, self.gamepad3_ninja, self.gamepad4_ninja]

		self.keyboard1_ninja = None
		self.keyboard2_ninja = None

		self.gamepad1_last_hat = (0,0)
		self.gamepad2_last_hat = (0,0)
		self.gamepad3_last_hat = (0,0)
		self.gamepad4_last_hat = (0,0)
		self.gamepad1_last_stick = (0,0)
		self.gamepad2_last_stick = (0,0)
		self.gamepad3_last_stick = (0,0)
		self.gamepad4_last_stick = (0,0)

		self.gamepad1_stick0allowed = True
		self.gamepad1_stick1allowed = True
		self.gamepad1_hat0allowed = True
		self.gamepad1_hat1allowed = True

		self.gamepad2_stick0allowed = True
		self.gamepad2_stick1allowed = True
		self.gamepad2_hat0allowed = True
		self.gamepad2_hat1allowed = True

		self.gamepad3_stick0allowed = True
		self.gamepad3_stick1allowed = True
		self.gamepad3_hat0allowed = True
		self.gamepad3_hat1allowed = True

		self.gamepad4_stick0allowed = True
		self.gamepad4_stick1allowed = True
		self.gamepad4_hat0allowed = True
		self.gamepad4_hat1allowed = True

		self.gamepad1_update_controls()
		self.gamepad2_update_controls()
		self.gamepad3_update_controls()
		self.gamepad4_update_controls()

		self.press1 = False
		self.press2 = False
		self.press3 = False
		self.press4 = False

		#Defaults to Xbox Controls. Can be changed.
		self.p1_gamepad = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
							'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
							'button_start' :  7,
							'button_menu' : 3, 'button_menu_image' : self.button_xbox_y,
							'button_jump' : 0, 'button_jump_image' : self.button_xbox_a,
							'button_roll' : 1, 'button_roll_image' : self.button_xbox_b,
							'button_item' : 2, 'button_item_image' : self.button_xbox_x,
							'sensitivity' : 0.5
							}

		self.p2_gamepad = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
							'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
							'button_start' :  7,
							'button_menu' : 3, 'button_menu_image' : self.button_xbox_y,
							'button_jump' : 0, 'button_jump_image' : self.button_xbox_a,
							'button_roll' : 1, 'button_roll_image' : self.button_xbox_b,
							'button_item' : 2, 'button_item_image' : self.button_xbox_x,
							'sensitivity' : 0.5
							}

		self.p3_gamepad = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
							'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
							'button_start' :  7,
							'button_menu' : 3, 'button_menu_image' : self.button_xbox_y,
							'button_jump' : 0, 'button_jump_image' : self.button_xbox_a,
							'button_roll' : 1, 'button_roll_image' : self.button_xbox_b,
							'button_item' : 2, 'button_item_image' : self.button_xbox_x,
							'sensitivity' : 0.5
							}

		self.p4_gamepad = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
							'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
							'button_start' :  7,
							'button_menu' : 3, 'button_menu_image' : self.button_xbox_y,
							'button_jump' : 0, 'button_jump_image' : self.button_xbox_a,
							'button_roll' : 1, 'button_roll_image' : self.button_xbox_b,
							'button_item' : 2, 'button_item_image' : self.button_xbox_x,
							'sensitivity' : 0.5
							}



		self.set_P1_controls = False #locks out controls until SOMEBODY hits a botton, who then becomes 1st player.

		self.delay = 30  #how many frames of delay required before another button press is allowed. 60 frames is one second.


	def update(self):
		#game_state can be 'main_menu', 'player_select', 'level'

		if self.set_P1_controls is False:
			
			for event in pygame.event.get(): # User did something. Leave this in to handle mice clicks.
				#print(event)
				if event.type == pygame.QUIT:
					options.exit = True

				elif event.type == pygame.JOYBUTTONDOWN or (options.game_state == 'main_menu' and event.type in (pygame.JOYAXISMOTION, pygame.JOYHATMOTION)):
					i = self.random_gamepads[event.joy].get_id()
					try:
						player = self.gamepad_ids.index(i)
					except ValueError: #pass 'no player' until gamepad is assigned.
						player = None
					
					if player == 0:
						self.set_P1_controls = True
						menus.intro_handler.status = 'done'
						#Have menu settings also get this preference.
						if options.control_preferences['player1'] != 'gamepad':
							options.control_preferences['player1'] = 'gamepad'
							menus.game_options_sprite.vertical_selection = 5
							i = menus.game_options_sprite.selection_list[5] + 1
							if i > len(menus.game_options_sprite.menu_list[5][1]) - 1:
								i = 0
							menus.game_options_sprite.selection_list[5] = i

							#sprites.player1.controls_sprite.update_buttons()
						if len(self.random_gamepads) == 1: #only ONE gamepad. Default player2 to keyboard.
							if options.control_preferences['player2'] != 'keyboard':
								options.control_preferences['player2'] = 'keyboard'
								menus.game_options_sprite.vertical_selection = 6
								i = menus.game_options_sprite.selection_list[6] + 1
								if i > len(menus.game_options_sprite.menu_list[6][1]) - 1:
									i = 0

						#Load controls based on gamepad name. Otherwise configure controller.

						
						#gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)

						self.p1_gamepad_setup()
						'''
						try:
							self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()].copy()
							self.get_images(self.p1_gamepad)
						except:
							gamepad_name = self.gamepads[0].get_name()
							if self.os in ('Windows', 'Linux'):
								customize = True
								for text in ('Logitech', 'F710', 'F310', 'logitech', 'xbox', 'XBOX', 'Xbox'):
									if text in gamepad_name:
										#if gamepad_name in ('Logitech', 'logitech', 'xbox', 'XBOX', 'Xbox'):
										self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict['xbox'].copy()
										data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()] = self.p1_gamepad.copy()
										self.get_images(self.p1_gamepad)
										customize = False
										break
								if customize is True:
									print(gamepad_name)
									gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)


							elif self.os == 'Darwin':
								if 'Logitech' in gamepad_name:
									self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict['mac_log'].copy()
									data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()] = self.p1_gamepad.copy()
									self.get_images(self.p1_gamepad)
								elif 'Playstation' in gamepad_name or 'playstation' in gamepad_name:
									self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict['mac_ps'].copy()
									data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()] = self.p1_gamepad.copy()
									self.get_images(self.p1_gamepad)
								else:
									gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)

							else:
								gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)
						'''	
					
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						options.exit = True
					else:
						self.set_P1_controls = True
						menus.intro_handler.status = 'done'
						#Have menu settings also get this preference.
						if options.control_preferences['player1'] != 'keyboard':
							options.control_preferences['player1'] = 'keyboard'
							menus.game_options_sprite.vertical_selection = 5
							i = menus.game_options_sprite.selection_list[5] + 1
							if i > len(menus.game_options_sprite.menu_list[5][1]) - 1:
								i = 0
							menus.game_options_sprite.selection_list[5] = i

		elif options.game_state == 'level': #move ninjas accordingly
				self.reset_menu_controls() #needs to be here for pause menu
				#find out who's pressing what and react accordingly.
				key = pygame.key.get_pressed()
				#Player1
				if key[pygame.K_ESCAPE]:
					game_on = False

				if sprites.countdown_timer.done is True and sprites.effects_screen.status != 'gravity': #allow controls if countdown timer is done.

					if self.keyboard1_ninja != None:
						if key[pygame.K_DOWN]:
							self.keyboard1_ninja.down_press()

						if key[pygame.K_LEFT]:
							if self.keyboard1_ninja.confused is False:
								self.keyboard1_ninja.left_press()
							else:
								self.keyboard1_ninja.right_press()

						if key[pygame.K_RIGHT]:
							if self.keyboard1_ninja.confused is False:
								self.keyboard1_ninja.right_press()
							else:
								self.keyboard1_ninja.left_press()

						if key[pygame.K_UP]:
							self.keyboard1_ninja.up_press()
					
					if self.keyboard2_ninja != None:
						if key[pygame.K_s]:
							self.keyboard2_ninja.down_press()

						if key[pygame.K_a]:
							if self.keyboard2_ninja.confused is False:
								self.keyboard2_ninja.left_press()
							else:
								self.keyboard2_ninja.right_press()

						if key[pygame.K_d]:
							if self.keyboard2_ninja.confused is False:
								self.keyboard2_ninja.right_press()
							else:
								self.keyboard2_ninja.left_press()

						if key[pygame.K_w]:
							self.keyboard2_ninja.up_press()

					#player1 movement
					if len(self.gamepads) > 0 and self.gamepad1_ninja != None:
						
						
						hat = self.gamepads[0].get_hat(self.p1_gamepad['dpad'])
						sensitivity = self.p1_gamepad['sensitivity']
						x = 0
						y = 0
						#ASDF
						if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_LR'])) > sensitivity:
							if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_LR'])) / self.gamepads[0].get_axis(self.p1_gamepad['stick_LR']) ==  self.p1_gamepad['stick_L']:
								x = -1
							else:
								x = 1
						if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_UD'])) > sensitivity:
							if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_UD'])) / self.gamepads[0].get_axis(self.p1_gamepad['stick_UD']) ==  self.p1_gamepad['stick_U']:
								y = 1
							else:
								y = -1
						stick = (x, y)
						if self.gamepad1_last_hat != hat or self.gamepad1_last_stick != stick:
							self.gamepad1_ninja.left_release()
							self.gamepad1_ninja.right_release()
							self.gamepad1_ninja.jump_release()
							self.gamepad1_ninja.down_release()
							self.gamepad1_ninja.up_release()
						if hat[self.p1_gamepad['dpad_LR']] == self.p1_gamepad['dpad_R'] or stick[0] == 1:
							if self.gamepad1_ninja.confused is False:
								self.gamepad1_ninja.right_press()
							else:
								self.gamepad1_ninja.left_press()
						if hat[self.p1_gamepad['dpad_LR']] == self.p1_gamepad['dpad_L'] or stick[0] == -1:
							if self.gamepad1_ninja.confused is False:
								self.gamepad1_ninja.left_press()
							else:
								self.gamepad1_ninja.right_press()
						if hat[self.p1_gamepad['dpad_UD']] == self.p1_gamepad['dpad_U'] or stick[1] == 1:
							self.gamepad1_ninja.up_press()
						if hat[self.p1_gamepad['dpad_UD']] == self.p1_gamepad['dpad_D'] or stick[1] == -1:
							self.gamepad1_ninja.down_press()
						self.gamepad1_last_hat = hat
						self.gamepad1_last_stick = stick

					#player 2 movement
					if len(self.gamepads) > 1 and self.gamepad2_ninja != None:
						hat = self.gamepads[1].get_hat(self.p2_gamepad['dpad'])
						sensitivity = self.p2_gamepad['sensitivity']
						x = 0
						y = 0
						if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_LR'])) > sensitivity:
							if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_LR'])) / self.gamepads[1].get_axis(self.p2_gamepad['stick_LR']) ==  self.p2_gamepad['stick_L']:
								x = -1
							else:
								x = 1
						if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_UD'])) > sensitivity:
							if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_UD'])) / self.gamepads[1].get_axis(self.p2_gamepad['stick_UD']) ==  self.p2_gamepad['stick_U']:
								y = 1
							else:
								y = -1
						stick = (x, y)
						if self.gamepad2_last_hat != hat or self.gamepad2_last_stick != stick:
							self.gamepad2_ninja.left_release()
							self.gamepad2_ninja.right_release()
							self.gamepad2_ninja.jump_release()
							self.gamepad2_ninja.down_release()
							self.gamepad2_ninja.up_release()
						if hat[self.p2_gamepad['dpad_LR']] == self.p2_gamepad['dpad_R'] or stick[0] == 1:
							if self.gamepad2_ninja.confused is False:
								self.gamepad2_ninja.right_press()
							else:
								self.gamepad2_ninja.left_press()
						if hat[self.p2_gamepad['dpad_LR']] == self.p2_gamepad['dpad_L'] or stick[0] == -1:
							if self.gamepad2_ninja.confused is False:
								self.gamepad2_ninja.left_press()
							else:
								self.gamepad2_ninja.right_press()
						if hat[self.p2_gamepad['dpad_UD']] == self.p2_gamepad['dpad_U'] or stick[1] == 1:
							self.gamepad2_ninja.up_press()
						if hat[self.p2_gamepad['dpad_UD']] == self.p2_gamepad['dpad_D'] or stick[1] == -1:
							self.gamepad2_ninja.down_press()
						self.gamepad2_last_hat = hat
						self.gamepad2_last_stick = stick

					#player 3 
					if len(self.gamepads) > 2 and self.gamepad3_ninja != None:
						hat = self.gamepads[2].get_hat(self.p3_gamepad['dpad'])
						sensitivity = self.p3_gamepad['sensitivity']
						x = 0
						y = 0
						if abs(self.gamepads[2].get_axis(self.p2_gamepad['stick_LR'])) > sensitivity:
							if abs(self.gamepads[2].get_axis(self.p2_gamepad['stick_LR'])) / self.gamepads[2].get_axis(self.p3_gamepad['stick_LR']) ==  self.p3_gamepad['stick_L']:
								x = -1
							else:
								x = 1
						if abs(self.gamepads[2].get_axis(self.p2_gamepad['stick_UD'])) > sensitivity:
							if abs(self.gamepads[2].get_axis(self.p2_gamepad['stick_UD'])) / self.gamepads[2].get_axis(self.p3_gamepad['stick_UD']) ==  self.p3_gamepad['stick_U']:
								y = 1
							else:
								y = -1

						stick = (x, y)
						if self.gamepad3_last_hat != hat or self.gamepad3_last_stick != stick:
							self.gamepad3_ninja.left_release()
							self.gamepad3_ninja.right_release()
							self.gamepad3_ninja.jump_release()
							self.gamepad3_ninja.down_release()
							self.gamepad3_ninja.up_release()
						if hat[self.p3_gamepad['dpad_LR']] == self.p3_gamepad['dpad_R'] or stick[0] == 1:
							if self.gamepad3_ninja.confused is False:
								self.gamepad3_ninja.right_press()
							else:
								self.gamepad3_ninja.left_press()
						if hat[self.p3_gamepad['dpad_LR']] == self.p3_gamepad['dpad_L'] or stick[0] == -1:
							if self.gamepad3_ninja.confused is False:
								self.gamepad3_ninja.left_press()
							else:
								self.gamepad3_ninja.right_press()
						if hat[self.p3_gamepad['dpad_UD']] == self.p3_gamepad['dpad_U'] or stick[1] == 1:
							self.gamepad3_ninja.up_press()
						if hat[self.p3_gamepad['dpad_UD']] == self.p3_gamepad['dpad_D'] or stick[1] == -1:
							self.gamepad3_ninja.down_press()
						self.gamepad3_last_hat = hat
						self.gamepad3_last_stick = stick

					#player 4 movement
					if len(self.gamepads) > 3 and self.gamepad4_ninja != None:
						hat = self.gamepads[3].get_hat(self.p4_gamepad['dpad'])
						sensitivity = self.p4_gamepad['sensitivity']
						x = 0
						y = 0
						if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_LR'])) > sensitivity:
							if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_LR'])) / self.gamepads[3].get_axis(self.p4_gamepad['stick_LR']) ==  self.p4_gamepad['stick_L']:
								x = -1
							else:
								x = 1
						if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_UD'])) > sensitivity:
							if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_UD'])) / self.gamepads[3].get_axis(self.p4_gamepad['stick_UD']) ==  self.p4_gamepad['stick_U']:
								y = 1
							else:
								y = -1

						stick = (x, y)
						if self.gamepad4_last_hat != hat or self.gamepad4_last_stick != stick:
							self.gamepad4_ninja.left_release()
							self.gamepad4_ninja.right_release()
							self.gamepad4_ninja.jump_release()
							self.gamepad4_ninja.down_release()
							self.gamepad4_ninja.up_release()
						if hat[self.p4_gamepad['dpad_LR']] == self.p4_gamepad['dpad_R'] or stick[0] == 1:
							if self.gamepad4_ninja.confused is False:
								self.gamepad4_ninja.right_press()
							else:
								self.gamepad4_ninja.left_press()
						if hat[self.p4_gamepad['dpad_LR']] == self.p4_gamepad['dpad_L'] or stick[0] == -1:
							if self.gamepad4_ninja.confused is False:
								self.gamepad4_ninja.left_press()
							else:
								self.gamepad4_ninja.right_press()
						if hat[self.p4_gamepad['dpad_UD']] == self.p4_gamepad['dpad_U'] or stick[1] == 1:
							self.gamepad4_ninja.up_press()
						if hat[self.p4_gamepad['dpad_UD']] == self.p4_gamepad['dpad_D'] or stick[1] == -1:
							self.gamepad4_ninja.down_press()
						self.gamepad4_last_hat = hat
						self.gamepad4_last_stick = stick

				#next, handle single press and single release input
				for event in pygame.event.get(): # User did something. Leave this in to handle mice clicks.
					#print(event)
					if event.type == pygame.QUIT:
						options.exit = True

						
					#Handles Cadence for player1 and player2. Based on mouse clicks'''
					elif event.type == pygame.MOUSEBUTTONDOWN:
						print('mouse button activate!')

					elif event.type == pygame.JOYBUTTONDOWN:

						i = self.random_gamepads[event.joy].get_id()
						try:
							player = self.gamepad_ids.index(i)
						except ValueError: #pass 'no player' until gamepad is assigned.
							player = None

						if player == 0:							
							if event.button == self.p1_gamepad['button_start']:
								if sprites.transition_screen.status == 'idle':
									self.gamepad1_ninja.menu_start_press = True
									options.game_state = 'pause'

							if sprites.countdown_timer.done is True: #allow controls if countdown timer is done.
								if event.button == self.p1_gamepad['button_jump']:
									self.gamepad1_ninja.jump_press()

								elif event.button == self.p1_gamepad['button_roll']:
									self.gamepad1_ninja.roll_press()

								elif event.button == self.p1_gamepad['button_item']:
									self.gamepad1_ninja.item_press()

						elif player == 1:
							if event.button == self.p2_gamepad['button_start']:
								if sprites.transition_screen.status == 'idle':
									self.gamepad1_ninja.menu_start_press = True
									options.game_state = 'pause'

							if sprites.countdown_timer.done is True: #allow controls if countdown timer is done.
								if event.button == self.p2_gamepad['button_jump']:
									self.gamepad2_ninja.jump_press()

								elif event.button == self.p2_gamepad['button_roll']:
									self.gamepad2_ninja.roll_press()

								elif event.button == self.p2_gamepad['button_item']:
									self.gamepad2_ninja.item_press()

						elif player == 2:
							if event.button == self.p3_gamepad['button_start']:
								if sprites.transition_screen.status == 'idle':
									self.gamepad1_ninja.menu_start_press = True
									options.game_state = 'pause'

							if sprites.countdown_timer.done is True: #allow controls if countdown timer is done.
								if event.button == self.p3_gamepad['button_jump']:
									self.gamepad3_ninja.jump_press()

								elif event.button == self.p3_gamepad['button_roll']:
									self.gamepad3_ninja.roll_press()

								elif event.button == self.p3_gamepad['button_item']:
									self.gamepad3_ninja.item_press()

						elif player == 3:
							if event.button == self.p4_gamepad['button_start']:
								if sprites.transition_screen.status == 'idle':
									self.gamepad1_ninja.menu_start_press = True
									options.game_state = 'pause'

							if sprites.countdown_timer.done is True: #allow controls if countdown timer is done.
								if event.button == self.p4_gamepad['button_jump']:
									self.gamepad4_ninja.jump_press()

								elif event.button == self.p4_gamepad['button_roll']:
									self.gamepad4_ninja.roll_press()

								elif event.button == self.p4_gamepad['button_item']:
									self.gamepad4_ninja.item_press()

					elif event.type == pygame.JOYBUTTONUP:

						i = self.random_gamepads[event.joy].get_id()
						try:
							player = self.gamepad_ids.index(i)
						except ValueError: #pass 'no player' until gamepad is assigned.
							player = None

						if sprites.countdown_timer.done is True: #allow controls if countdown timer is done.
							if player == 0:
								if event.button == self.p1_gamepad['button_jump']:
									self.gamepad1_ninja.jump_release()
							elif player == 1:
								if event.button == self.p2_gamepad['button_jump']:
									self.gamepad2_ninja.jump_release()
							elif player == 2:
								if event.button == self.p3_gamepad['button_jump']:
									self.gamepad3_ninja.jump_release()
							elif player == 3:
								if event.button == self.p4_gamepad['button_jump']:
									self.gamepad4_ninja.jump_release()

							if player == 0:
								if event.button == self.p1_gamepad['button_item']:
									self.gamepad1_ninja.item_release()
							elif player == 1:
								if event.button == self.p2_gamepad['button_item']:
									self.gamepad2_ninja.item_release()
							elif player == 2:
								if event.button == self.p3_gamepad['button_item']:
									self.gamepad3_ninja.item_release()
							elif player == 3:
								if event.button == self.p4_gamepad['button_item']:
									self.gamepad4_ninja.item_release()


					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							options.exit = True

						#Handle screen toggling
						if event.key == pygame.K_MINUS or event.key == pygame.K_F11:
							size = (sprites.big_screen.get_width(), sprites.big_screen.get_height())
							if options.fullscreen is True:
								options.fullscreen = False
								sprites.big_screen = pygame.display.set_mode(size)
							else:
								options.fullscreen = True
								sprites.big_screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

						if event.key == pygame.K_TAB:
							mods = pygame.key.get_mods()
							if mods & pygame.KMOD_LALT:
								if options.fullscreen is True:
									size = (sprites.big_screen.get_width(), sprites.big_screen.get_height())
									options.fullscreen = False
									sprites.big_screen = pygame.display.set_mode(size)

						if event.key == pygame.K_t:
							if options.demo is False:
								#sprites.screenshot_handler.capture(timer = 300, target_ninja = sprites.player1)
								sprites.screenshot_handler.capture(timer = 300, target = 'top left')

						if self.keyboard1_ninja != None:
								if event.key == pygame.K_RETURN:
									if sprites.transition_screen.status == 'idle':
										self.keyboard1_ninja.menu_start_press = True
										options.game_state = 'pause'
								if event.key == pygame.K_l:
									if sprites.transition_screen.status == 'idle':
										self.keyboard1_ninja.menu_start_press = True
										#menus.choice_handler.activate(sprites.player_list, 'Stage1_1.0', response_text = 'test', choice_left=sprites.player1, choice_right=sprites.player2, choice_top=sprites.player3, choice_bottom=sprites.player4)
										menus.choice_handler.activate(sprites.player_list, 'just testing this text', choice_left='Ready', choice_right='Good', choice_top='Nope', choice_bottom='Understood')
										

								if sprites.countdown_timer.done is True and sprites.effects_screen.status != 'gravity': #allow controls if countdown timer is done.

									if event.key == pygame.K_z:
										self.keyboard1_ninja.jump_press()

									if event.key == pygame.K_x:
										self.keyboard1_ninja.roll_press()

									if event.key == pygame.K_c:
										self.keyboard1_ninja.item_press()

									if event.key == pygame.K_g:
										if options.demo is False:
											sprites.effects_screen.glitch_screen()
									
									if event.key == pygame.K_i:
										if options.demo is False:
											for ninja in sprites.ninja_list:
												if ninja.visible == 1:
													#self.visible = 0
													ninja.visible_timer = 10
													ninja.visible_switch = False
												else:
													#self.visible = 1
													ninja.visible_timer = 10
													ninja.visible_switch = True


									if event.key == pygame.K_p:
										if options.demo is False:
											sprites.particle_generator.ice_bomb_explosion_particles(pygame.Rect(random.randrange(100,400,1),random.randrange(50,300,1),10,10), True, 'snow_finish')
											sprites.particle_generator.ice_bomb_explosion_particles(pygame.Rect(random.randrange(100,400,1),random.randrange(50,300,1),10,10), True, 'snow_finish')
											#sprites.particle_generator.ice_bomb_explosion_particles(pygame.Rect(random.randrange(100,400,1),random.randrange(50,300,1),10,10), True, 'snow_finish')
											#sprites.particle_generator.ice_bomb_explosion_particles(pygame.Rect(random.randrange(100,400,1),random.randrange(50,300,1),10,10), True, 'snow_finish')
											sprites.particle_generator.bubble_pop_particles(((100,100)))
											sprites.particle_generator.bubble_pop_particles(((150,150)))
											#sprites.particle_generator.bubble_pop_particles(((200,200)))
											#sprites.particle_generator.bubble_pop_particles(((250,250)))
									if event.key == pygame.K_0:
										if options.demo is False:
											gbarrier = False
											for item in sprites.level_objects:
												try:
													if item.type == 'gravity_barrier':
														if item.opposite is True:
															item.opposite = False
														else:
															item.opposite = True
														item.switch_tiles()

														break
												except AttributeError:
													pass
													 
												
											if gbarrier is False:
												options.inverted_g = not options.inverted_g
												for ninja in sprites.ninja_list:
													if ninja.inverted_g is False:
														ninja.invert_g()
													else:
														ninja.revert_g()


												for ninja in sprites.player_list:
													if ninja not in sprites.ninja_list:
														ninja.death_sprite.inverted_g = not ninja.death_sprite.inverted_g

												
												for sprite in sprites.gravity_effects:
													sprite.invert_g(None)

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
															#print('made it!!!!')
															#print(item.type)
															item.inverted_g = False
														else:
															#print('made it!!!!')
															#print(item.type)
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

						if self.keyboard2_ninja != None:
								if sprites.countdown_timer.done is True and sprites.effects_screen.status != 'gravity': #allow controls if countdown timer is done.
									if event.key == pygame.K_q:
										self.keyboard2_ninja.jump_press()

									if event.key == pygame.K_e:
										self.keyboard2_ninja.roll_press()

									if event.key == pygame.K_r:
										self.keyboard2_ninja.item_press()

					


					elif event.type == pygame.KEYUP:
						#p1
						if sprites.countdown_timer.done is True and sprites.effects_screen.status != 'gravity': #allow controls if countdown timer is done.
							if self.keyboard1_ninja != None:
								if event.key == pygame.K_c:
									self.keyboard1_ninja.item_release()

								if event.key == pygame.K_UP:
									self.keyboard1_ninja.up_release()
									
								if event.key == pygame.K_DOWN:
									self.keyboard1_ninja.down_release()

								if event.key == pygame.K_x:
									self.keyboard1_ninja.jump_release()

								if event.key == pygame.K_LEFT:
									self.keyboard1_ninja.left_release()
									self.keyboard1_ninja.right_release()

								if event.key == pygame.K_RIGHT:
									self.keyboard1_ninja.right_release()
									self.keyboard1_ninja.left_release()

							if self.keyboard2_ninja != None:
								if event.key == pygame.K_r:
									self.keyboard2_ninja.item_release()

								if event.key == pygame.K_w:
									self.keyboard2_ninja.up_release()
									
								if event.key == pygame.K_s:
									self.keyboard2_ninja.down_release()

								if event.key == pygame.K_q:
									self.keyboard2_ninja.jump_release()

								if event.key == pygame.K_a:
									self.keyboard2_ninja.left_release()
									self.keyboard2_ninja.right_release()

								if event.key == pygame.K_d:
									self.keyboard2_ninja.right_release()
									self.keyboard2_ninja.left_release()
			#else:
			#	pygame.event.clear()

		else: #use menu controls
			self.reset_menu_controls() #resets menu controls for each ninja
			#find out who's pressing what and react accordingly.
			temp_list = [sprites.player1, sprites.player2, sprites.player3, sprites.player4]
			for ninja in temp_list:
				if ninja.menu_press_delay > 0:
					ninja.menu_press_delay -= 1

			#player1 movement
			if len(self.gamepads) > 0 and self.gamepad1_ninja != None:

				hat = self.gamepads[0].get_hat(self.p1_gamepad['dpad'])
				sensitivity = self.p1_gamepad['sensitivity']
				sensitivity = 0.7
				x = 0
				y = 0
				
				if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_LR'])) > sensitivity:
					if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_LR'])) / self.gamepads[0].get_axis(self.p1_gamepad['stick_LR']) ==  self.p1_gamepad['stick_L']:
						x = -1
					else:
						x = 1
				if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_UD'])) > sensitivity:
					if abs(self.gamepads[0].get_axis(self.p1_gamepad['stick_UD'])) / self.gamepads[0].get_axis(self.p1_gamepad['stick_UD']) ==  self.p1_gamepad['stick_U']:
						y = 1
					else:
						y = -1
				stick = (x,y)
				if x == 0:
					self.gamepad1_stick0allowed = True
				if y == 0:
					self.gamepad1_stick1allowed = True

				if hat[self.p1_gamepad['dpad_LR']] == 0:
					self.gamepad1_hat0allowed = True
				if hat[self.p1_gamepad['dpad_UD']] == 0:
					self.gamepad1_hat1allowed = True

				if self.gamepad1_stick0allowed is True:
					if stick[0] == 1:
						self.gamepad1_ninja.menu_right_press = True
						self.gamepad1_stick0allowed = False
					elif stick[0] == -1:
						self.gamepad1_ninja.menu_left_press = True
						self.gamepad1_stick0allowed = False
				if self.gamepad1_stick1allowed is True:
					if stick[1] == 1:
						self.gamepad1_ninja.menu_up_press = True
						self.gamepad1_stick1allowed = False
					elif stick[1] == -1:
						self.gamepad1_ninja.menu_down_press = True
						self.gamepad1_stick1allowed = False

				if self.gamepad1_hat0allowed is True:
					if hat[self.p1_gamepad['dpad_LR']] == self.p1_gamepad['dpad_R']:
						self.gamepad1_ninja.menu_right_press = True
						self.gamepad1_hat0allowed = False
					elif hat[self.p1_gamepad['dpad_LR']] == self.p1_gamepad['dpad_L']:
						self.gamepad1_ninja.menu_left_press = True
						self.gamepad1_hat0allowed = False
	
				if self.gamepad1_hat1allowed is True:
					if hat[self.p1_gamepad['dpad_UD']] == self.p1_gamepad['dpad_U']:
						self.gamepad1_ninja.menu_up_press = True
						self.gamepad1_hat1allowed = False
					elif hat[self.p1_gamepad['dpad_UD']] == self.p1_gamepad['dpad_D']:
						self.gamepad1_ninja.menu_down_press = True
						self.gamepad1_hat1allowed = False


			#player 2 movement
			if len(self.gamepads) > 1 and self.gamepad2_ninja != None:
				hat = self.gamepads[1].get_hat(self.p2_gamepad['dpad'])
				sensitivity = self.p2_gamepad['sensitivity']
				sensitivity = 0.7
				x = 0
				y = 0
				if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_LR'])) > sensitivity:
					if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_LR'])) / self.gamepads[1].get_axis(self.p2_gamepad['stick_LR']) ==  self.p2_gamepad['stick_L']:
						x = -1
					else:
						x = 1
				if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_UD'])) > sensitivity:
					if abs(self.gamepads[1].get_axis(self.p2_gamepad['stick_UD'])) / self.gamepads[1].get_axis(self.p2_gamepad['stick_UD']) ==  self.p2_gamepad['stick_U']:
						y = 1
					else:
						y = -1
				stick = (x,y)


				if x == 0:
					self.gamepad2_stick0allowed = True
				if y == 0:
					self.gamepad2_stick1allowed = True

				if hat[0] == 0:
					self.gamepad2_hat0allowed = True
				if hat[1] == 0:
					self.gamepad2_hat1allowed = True

				if self.gamepad2_stick0allowed is True:
					if stick[0] == 1:
						self.gamepad2_ninja.menu_right_press = True
						self.gamepad2_stick0allowed = False
					elif stick[0] == -1:
						self.gamepad2_ninja.menu_left_press = True
						self.gamepad2_stick0allowed = False
				if self.gamepad2_stick1allowed is True:
					if stick[1] == 1:
						self.gamepad2_ninja.menu_up_press = True
						self.gamepad2_stick1allowed = False
					elif stick[1] == -1:
						self.gamepad2_ninja.menu_down_press = True
						self.gamepad2_stick1allowed = False

				if self.gamepad2_hat0allowed is True:
					if hat[self.p2_gamepad['dpad_LR']] == self.p2_gamepad['dpad_R']:
						self.gamepad2_ninja.menu_right_press = True
						self.gamepad2_hat0allowed = False
					elif hat[self.p2_gamepad['dpad_LR']] == self.p2_gamepad['dpad_L']:
						self.gamepad2_ninja.menu_left_press = True
						self.gamepad2_hat0allowed = False
	
				if self.gamepad2_hat1allowed is True:
					if hat[self.p2_gamepad['dpad_UD']] == self.p2_gamepad['dpad_U']:
						self.gamepad2_ninja.menu_up_press = True
						self.gamepad2_hat1allowed = False
					elif hat[self.p2_gamepad['dpad_UD']] == self.p2_gamepad['dpad_D']:
						self.gamepad2_ninja.menu_down_press = True
						self.gamepad2_hat1allowed = False

			#player 3 movement
			if len(self.gamepads) > 2 and self.gamepad3_ninja != None:
				hat = self.gamepads[2].get_hat(self.p3_gamepad['dpad'])
				sensitivity = self.p3_gamepad['sensitivity']
				sensitivity = 0.7
				x = 0
				y = 0
				if abs(self.gamepads[2].get_axis(self.p3_gamepad['stick_LR'])) > sensitivity:
					if abs(self.gamepads[2].get_axis(self.p3_gamepad['stick_LR'])) / self.gamepads[2].get_axis(self.p3_gamepad['stick_LR']) ==  self.p3_gamepad['stick_L']:
						x = -1
					else:
						x = 1
				if abs(self.gamepads[2].get_axis(self.p3_gamepad['stick_UD'])) > sensitivity:
					if abs(self.gamepads[2].get_axis(self.p3_gamepad['stick_UD'])) / self.gamepads[2].get_axis(self.p3_gamepad['stick_UD']) ==  self.p3_gamepad['stick_U']:
						y = 1
					else:
						y = -1
				stick = (x,y)

				if x == 0:
					self.gamepad3_stick0allowed = True
				if y == 0:
					self.gamepad3_stick1allowed = True

				if hat[0] == 0:
					self.gamepad3_hat0allowed = True
				if hat[1] == 0:
					self.gamepad3_hat1allowed = True

				if self.gamepad3_stick0allowed is True:
					if stick[0] == 1:
						self.gamepad3_ninja.menu_right_press = True
						self.gamepad3_stick0allowed = False
					elif stick[0] == -1:
						self.gamepad3_ninja.menu_left_press = True
						self.gamepad3_stick0allowed = False
				if self.gamepad3_stick1allowed is True:
					if stick[1] == 1:
						self.gamepad3_ninja.menu_up_press = True
						self.gamepad3_stick1allowed = False
					elif stick[1] == -1:
						self.gamepad3_ninja.menu_down_press = True
						self.gamepad3_stick1allowed = False

				if self.gamepad3_hat0allowed is True:
					if hat[self.p3_gamepad['dpad_LR']] == self.p3_gamepad['dpad_R']:
						self.gamepad3_ninja.menu_right_press = True
						self.gamepad3_hat0allowed = False
					elif hat[self.p3_gamepad['dpad_LR']] == self.p3_gamepad['dpad_L']:
						self.gamepad3_ninja.menu_left_press = True
						self.gamepad3_hat0allowed = False
	
				if self.gamepad3_hat1allowed is True:
					if hat[self.p3_gamepad['dpad_UD']] == self.p3_gamepad['dpad_U']:
						self.gamepad3_ninja.menu_up_press = True
						self.gamepad3_hat1allowed = False
					elif hat[self.p3_gamepad['dpad_UD']] == self.p3_gamepad['dpad_D']:
						self.gamepad3_ninja.menu_down_press = True
						self.gamepad3_hat1allowed = False

			#player 4 movement
			if len(self.gamepads) > 3 and self.gamepad4_ninja != None:
				hat = self.gamepads[3].get_hat(self.p4_gamepad['dpad'])
				sensitivity = self.p4_gamepad['sensitivity']
				sensitivity = 0.7
				x = 0
				y = 0
				if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_LR'])) > sensitivity:
					if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_LR'])) / self.gamepads[3].get_axis(self.p4_gamepad['stick_LR']) ==  self.p4_gamepad['stick_L']:
						x = -1
					else:
						x = 1
				if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_UD'])) > sensitivity:
					if abs(self.gamepads[3].get_axis(self.p4_gamepad['stick_UD'])) / self.gamepads[3].get_axis(self.p4_gamepad['stick_UD']) ==  self.p4_gamepad['stick_U']:
						y = 1
					else:
						y = -1
				stick = (x,y)

				if x == 0:
					self.gamepad4_stick0allowed = True
				if y == 0:
					self.gamepad4_stick1allowed = True

				if hat[0] == 0:
					self.gamepad4_hat0allowed = True
				if hat[1] == 0:
					self.gamepad4_hat1allowed = True

				if self.gamepad4_stick0allowed is True:
					if stick[0] == 1:
						self.gamepad4_ninja.menu_right_press = True
						self.gamepad4_stick0allowed = False
					elif stick[0] == -1:
						self.gamepad4_ninja.menu_left_press = True
						self.gamepad4_stick0allowed = False
				if self.gamepad4_stick1allowed is True:
					if stick[1] == 1:
						self.gamepad4_ninja.menu_up_press = True
						self.gamepad4_stick1allowed = False
					elif stick[1] == -1:
						self.gamepad4_ninja.menu_down_press = True
						self.gamepad4_stick1allowed = False

				if self.gamepad4_hat0allowed is True:
					if hat[self.p4_gamepad['dpad_LR']] == self.p4_gamepad['dpad_R']:
						self.gamepad4_ninja.menu_right_press = True
						self.gamepad4_hat0allowed = False
					elif hat[self.p4_gamepad['dpad_LR']] == self.p4_gamepad['dpad_L']:
						self.gamepad4_ninja.menu_left_press = True
						self.gamepap4_hat0allowed = False
	
				if self.gamepad4_hat1allowed is True:
					if hat[self.p4_gamepad['dpad_UD']] == self.p4_gamepad['dpad_U']:
						self.gamepad4_ninja.menu_up_press = True
						self.gamepad4_hat1allowed = False
					elif hat[self.p4_gamepad['dpad_UD']] == self.p4_gamepad['dpad_D']:
						self.gamepad4_ninja.menu_down_press = True
						self.gamepad4_hat1allowed = False

			#next, handle single press and single release input
			for event in pygame.event.get(): # User did something. Leave this in to handle mice clicks.
				#if event.type == pygame.JOYAXISMOTION:	
				#	if event.axis == 1 or event.axis == 0:
				#		if abs(event.value) > 0.5:
				#			print('AXIS')
				#			print(event.axis)
				#			print(round(event.value))
				if event.type == pygame.QUIT:
					options.exit = True
						
				#Handles Cadence for player1 and player2. Based on mouse clicks'''
				elif event.type == pygame.MOUSEBUTTONDOWN:
					print('mouse button activate!')

				elif event.type == pygame.JOYBUTTONDOWN:
						
						i = self.random_gamepads[event.joy].get_id()

						try:
							player = self.gamepad_ids.index(i)
						except ValueError: #pass 'no player' until gamepad is assigned.
							player = None
				
				
						if player == 0:
							if event.button == self.p1_gamepad['button_start']:
								self.gamepad1_ninja.menu_start_press = True
							if event.button == self.p1_gamepad['button_menu']:
								self.gamepad1_ninja.menu_y_press = True
							if event.button == self.p1_gamepad['button_jump']:
								self.gamepad1_ninja.menu_select_press = True

							elif event.button == self.p1_gamepad['button_roll']:
								self.gamepad1_ninja.menu_back_press = True

							elif event.button == self.p1_gamepad['button_item']:
								self.gamepad1_ninja.menu_x_press = True


						elif player == 1:
							if event.button == self.p2_gamepad['button_start']:
								self.gamepad2_ninja.menu_start_press = True
							if event.button == self.p2_gamepad['button_menu']:
								self.gamepad2_ninja.menu_y_press = True
							if event.button == self.p2_gamepad['button_jump']:
								self.gamepad2_ninja.menu_select_press = True

							elif event.button == self.p2_gamepad['button_roll']:
								self.gamepad2_ninja.menu_back_press = True

							elif event.button == self.p2_gamepad['button_item']:
								self.gamepad2_ninja.menu_x_press = True


						elif player == 2:
							if event.button == self.p3_gamepad['button_start']:
								self.gamepad3_ninja.menu_start_press = True
							if event.button == self.p3_gamepad['button_menu']:
								self.gamepad3_ninja.menu_y_press = True
							if event.button == self.p3_gamepad['button_jump']:
								self.gamepad3_ninja.menu_select_press = True

							elif event.button == self.p3_gamepad['button_roll']:
								self.gamepad3_ninja.menu_back_press = True

							elif event.button == self.p3_gamepad['button_item']:
								self.gamepad3_ninja.menu_x_press = True

						elif player == 3:
							if event.button == self.p4_gamepad['button_start']:
								self.gamepad4_ninja.menu_start_press = True
							if event.button == self.p4_gamepad['button_menu']:
								self.gamepad4_ninja.menu_y_press = True
							if event.button == self.p4_gamepad['button_jump']:
								self.gamepad4_ninja.menu_select_press = True

							elif event.button == self.p4_gamepad['button_roll']:
								self.gamepad4_ninja.menu_back_press = True

							elif event.button == self.p4_gamepad['button_item']:
								self.gamepad4_ninja.menu_x_press = True


				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						options.exit = True

					#Handle screen toggling
					if event.key == pygame.K_MINUS or event.key == pygame.K_F11:
						size = (sprites.big_screen.get_width(), sprites.big_screen.get_height())
						if options.fullscreen is True:
							options.fullscreen = False
							sprites.big_screen = pygame.display.set_mode(options.screen_resolution)
						else:
							options.fullscreen = True
							sprites.big_screen = pygame.display.set_mode(options.screen_resolution, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

					if event.key == pygame.K_TAB:
						mods = pygame.key.get_mods()
						if mods & pygame.KMOD_LALT:
							if options.fullscreen is True:
								size = (sprites.big_screen.get_width(), sprites.big_screen.get_height())
								options.fullscreen = False
								#sprites.big_screen = pygame.display.set_mode(size)
								sprites.big_screen = pygame.display.set_mode(options.screen_resolution)
							
					if event.key == pygame.K_t:
						if options.demo is False:
							sprites.screenshot_handler.capture(timer = 400, target = 'top left')

					if event.key == pygame.K_g:
						if options.demo is False:
							sprites.effects_screen.glitch_screen()

					if event.key == pygame.K_6:
						pygame.joystick.quit()
						pygame.joystick.init()


					if event.key == pygame.K_1:
						if options.demo is False:
							self.press1 = True
					if event.key == pygame.K_2:
						if options.demo is False:
							self.press2 = True
					if event.key == pygame.K_3:
						if options.demo is False:
							self.press3 = True
					if event.key == pygame.K_4:
						if options.demo is False:
							self.press4 = True
					if event.key == pygame.K_7:
						if options.demo is False:
							sprites.shake_handler.current_shake += sprites.shake_handler.shake_growth

					if self.keyboard1_ninja != None:
						if event.key == pygame.K_y:
							self.keyboard1_ninja.menu_y_press = True

						if event.key == pygame.K_RETURN:
							self.keyboard1_ninja.menu_start_press = True

						if event.key == pygame.K_DOWN:
							self.keyboard1_ninja.menu_down_press = True

						if event.key == pygame.K_UP:
							self.keyboard1_ninja.menu_up_press = True

						if event.key == pygame.K_LEFT:
							self.keyboard1_ninja.menu_left_press = True

						if event.key == pygame.K_RIGHT:
							self.keyboard1_ninja.menu_right_press = True

						if event.key == pygame.K_z:
							self.keyboard1_ninja.menu_select_press = True

						if event.key == pygame.K_x:
							self.keyboard1_ninja.menu_back_press = True

						if event.key == pygame.K_c:
							self.keyboard1_ninja.menu_x_press = True

					if self.keyboard2_ninja != None:
						if event.key == pygame.K_s:
							self.keyboard2_ninja.menu_down_press = True

						if event.key == pygame.K_w:
							self.keyboard2_ninja.menu_up_press = True

						if event.key == pygame.K_a:
							self.keyboard2_ninja.menu_left_press = True

						if event.key == pygame.K_d:
							self.keyboard2_ninja.menu_right_press = True

						if event.key == pygame.K_q:
							self.keyboard2_ninja.menu_select_press = True

						if event.key == pygame.K_e:
							self.keyboard2_ninja.menu_back_press = True

						if event.key == pygame.K_r:
							self.keyboard2_ninja.menu_x_press = True

	def p1_gamepad_setup(self):
		try:
			self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()].copy()
			self.get_images(self.p1_gamepad)
		except:
			gamepad_name = self.gamepads[0].get_name()
			print('gamepad_name')
			print(gamepad_name)
			if self.os in ('Windows', 'Linux'):
				customize = True
				for text in ('Logitech', 'F710', 'F310', 'logitech', 'xbox', 'XBOX', 'Xbox'):
					if text in gamepad_name:
						#if gamepad_name in ('Logitech', 'logitech', 'xbox', 'XBOX', 'Xbox'):
						self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict['xbox'].copy()
						data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()] = self.p1_gamepad.copy()
						self.get_images(self.p1_gamepad)
						customize = False
						break
				if customize is True:
					print(gamepad_name)
					gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)


			elif self.os == 'Darwin':
				if 'Logitech' in gamepad_name:
					self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict['mac_log'].copy()
					data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()] = self.p1_gamepad.copy()
					self.get_images(self.p1_gamepad)
				elif 'Playstation' in gamepad_name or 'playstation' in gamepad_name:
					self.p1_gamepad = data_manager.data_handler.gamepad_layout_dict['mac_ps'].copy()
					data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()] = self.p1_gamepad.copy()
					self.get_images(self.p1_gamepad)
				else:
					gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)
			else:
				gamepad_customizer = Gamepad_Customizer(self, sprites.player1, (320,270), self.gamepads[0], self.p1_gamepad)

	def gamepad1_update_controls(self):
		if options.player1_controls == 'x-input':
			self.player1_start = 7
			self.player1_y = 3
			self.player1_a = 0
			self.player1_b = 1
			self.player1_x = 2

		elif options.player1_controls == 'd-input':
			self.player1_start = 9
			self.player1_y = 3
			self.player1_a = 1
			self.player1_b = 2
			self.player1_x = 0

	def gamepad2_update_controls(self):
		if options.player2_controls == 'x-input':
			self.player2_start = 7
			self.player2_y = 3
			self.player2_a = 0
			self.player2_b = 1
			self.player2_x = 2

		elif options.player2_controls == 'd-input':
			self.player2_start = 9
			self.player2_y = 3
			self.player2_a = 1
			self.player2_b = 2
			self.player2_x = 0

	def gamepad3_update_controls(self):
		if options.player3_controls == 'x-input':
			self.player3_start = 7
			self.player3_y = 3
			self.player3_a = 0
			self.player3_b = 1
			self.player3_x = 2

		elif options.player3_controls == 'd-input':
			self.player3_start = 9
			self.player3_y = 3
			self.player3_a = 1
			self.player3_b = 2
			self.player3_x = 0

	def gamepad4_update_controls(self):
		if options.player4_controls == 'x-input':
			self.player4_start = 7
			self.player4_y = 3
			self.player4_a = 0
			self.player4_b = 1
			self.player4_x = 2

		elif options.player1_controls == 'd-input':
			self.player4_start = 9
			self.player4_y = 3
			self.player4_a = 1
			self.player4_b = 2
			self.player4_x = 0

	def remove_controls(self):
		for ninja in sprites.ninja_list:
			ninja.left_release()
			ninja.right_release()
			ninja.jump_release()
			ninja.down_release()
			ninja.up_release()

	def reset_menu_controls(self):
		temp_list = [sprites.player1, sprites.player2, sprites.player3, sprites.player4]
		for sprite in temp_list:
			sprite.menu_up_press = False
			sprite.menu_down_press = False
			sprite.menu_left_press = False
			sprite.menu_right_press = False

			sprite.menu_select_press = False
			sprite.menu_back_press = False

			sprite.menu_start_press = False
			sprite.menu_y_press = False
			sprite.menu_x_press = False

			self.press1 = False
			self.press2 = False
			self.press3 = False
			self.press4 = False

	def get_gamepads(self):
		#print(sprites.player1.profile)
		#print()	

		'''
		if options.game_state in ('intro', 'main_menu', 'player_select'):
			#pygame.joystick.quit()
			#pygame.joystick.init()

			self.check_gamepads_counter += 1
			if self.check_gamepads_counter >= 60:
				self.check_gamepads_counter = 0	
				pygame.joystick.quit()
				pygame.joystick.init()
		'''


		#pygame.joystick.init()
		self.random_gamepads = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		for gamepad in self.random_gamepads:
			gamepad.init()

		#sort gamepads in order of id
		#self.random_gamepads.sort(key = lambda gamepad : gamepad.get_id())

		if len(self.random_gamepads) > len(self.gamepads):
			for gamepad in self.random_gamepads:
				if gamepad.get_id() not in self.gamepad_ids:
					if  1 in (gamepad.get_button(0), gamepad.get_button(1), gamepad.get_button(2), gamepad.get_button(3), gamepad.get_button(4)):
						self.gamepad_ids.append(gamepad.get_id())
						self.gamepads.append(gamepad)	

						#First button press goes by without menus 'picking it up.' Feed through identical event ot get noticed :)
						event = pygame.event.Event(pygame.JOYBUTTONDOWN,{'joy' : gamepad.get_id(), 'button' : 0})
						pygame.event.post(event)

					elif round(gamepad.get_axis(0)) == 1 or round(gamepad.get_axis(0)) == -1:
						self.gamepad_ids.append(gamepad.get_id())
						self.gamepads.append(gamepad)

					elif round(gamepad.get_axis(1)) == 1 or round(gamepad.get_axis(1)) == -1:
						self.gamepad_ids.append(gamepad.get_id())
						self.gamepads.append(gamepad)


		#apply gamepads to each player. Assumes preference is 'gamepads'
		if options.control_preferences['player1'] == 'gamepad' and options.control_preferences['player2'] == 'gamepad':
			self.gamepad1_ninja = sprites.player1
			self.gamepad2_ninja = sprites.player2
			self.gamepad3_ninja = sprites.player3
			self.gamepad4_ninja = sprites.player4


			self.keyboard1_ninja = sprites.player1
			self.keyboard2_ninja = sprites.player2

		elif options.control_preferences['player1'] == 'keyboard' and options.control_preferences['player2'] == 'gamepad':
			self.gamepad1_ninja = sprites.player2
			self.gamepad2_ninja = sprites.player3
			self.gamepad3_ninja = sprites.player4
			self.gamepad4_ninja = None

			self.keyboard1_ninja = sprites.player1
			self.keyboard2_ninja = None

		elif options.control_preferences['player1'] == 'gamepad' and options.control_preferences['player2'] == 'keyboard':
			self.gamepad1_ninja = sprites.player1
			self.gamepad2_ninja = sprites.player3
			self.gamepad3_ninja = sprites.player4
			self.gamepad4_ninja = None

			self.keyboard1_ninja = sprites.player2
			self.keyboard2_ninja = None

		elif options.control_preferences['player1'] == 'keyboard' and options.control_preferences['player2'] == 'keyboard':
			self.gamepad1_ninja = sprites.player3
			self.gamepad2_ninja = sprites.player4
			self.gamepad3_ninja = None
			self.gamepad4_ninja = None

			self.keyboard1_ninja = sprites.player1
			self.keyboard2_ninja = sprites.player2

		#self.keyboard1_ninja = sprites.player1
		#self.keyboard2_ninja = sprites.player2


		
		#Update gamepad layouts for all players if saved versions exist.
		
		#print(len(data_manager.data_handler.user_profile_dict[self.gamepad1_ninja.profile]['gamepad_layouts'].keys()))

		try:
			print(data_manager.data_handler.user_profile_dict['AAAAAA']['gamepad_layouts'][self.gamepads[0].get_name()]['button_jump_image'])
			print(data_manager.data_handler.user_profile_dict['BBBBBC']['gamepad_layouts'][self.gamepads[0].get_name()]['button_jump_image'])
			print(data_manager.data_handler.user_profile_dict['A']['gamepad_layouts'][self.gamepads[0].get_name()]['button_jump_image'])
			print(data_manager.data_handler.user_profile_dict['C']['gamepad_layouts'][self.gamepads[0].get_name()]['button_jump_image'])
		except:
			pass

		if self.gamepad1_ninja != None: # and self.gamepad1_ninja.profile != 'Guest':
			try:
				self.p1_gamepad = copy.deepcopy(data_manager.data_handler.user_profile_dict[self.gamepad1_ninja.profile]['gamepad_layouts'][self.gamepads[0].get_name()])
				#print(self.p1_gamepad['button_menu_image'])
				self.get_images(self.p1_gamepad)
				#print('made0')

			except:
				try:
					#print('made1')
					self.p1_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()])
					self.get_images(self.p1_gamepad)
				except:
					pass
		else:
			try:
				#print('made 2')
				self.p1_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[0].get_name()])
				self.get_images(self.p1_gamepad)
			except:
				pass

		
		if self.gamepad2_ninja != None: # and self.gamepad2_ninja.profile != 'Guest':
			try:
				self.p2_gamepad = copy.deepcopy(data_manager.data_handler.user_profile_dict[self.gamepad2_ninja.profile]['gamepad_layouts'][self.gamepads[1].get_name()])
				#print(self.p1_gamepad['button_menu_image'])
				self.get_images(self.p2_gamepad)
				#print('made0')

			except:
				try:
					#print('made1')
					self.p2_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[1].get_name()])
					self.get_images(self.p2_gamepad)
				except:
					pass
		else:
			try:
				#print('made 2')
				self.p2_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[1].get_name()])
				self.get_images(self.p2_gamepad)
			except:
				pass


		if self.gamepad3_ninja != None: # and self.gamepad3_ninja.profile != 'Guest':
			try:
				self.p3_gamepad = copy.deepcopy(data_manager.data_handler.user_profile_dict[self.gamepad3_ninja.profile]['gamepad_layouts'][self.gamepads[2].get_name()])
				#print(self.p1_gamepad['button_menu_image'])
				self.get_images(self.p3_gamepad)
				#print('made0')

			except:
				try:
					#print('made1')
					self.p3_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[2].get_name()])
					self.get_images(self.p3_gamepad)
				except:
					pass
		else:
			try:
				#print('made 2')
				self.p3_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[2].get_name()])
				self.get_images(self.p3_gamepad)
			except:
				pass


		
		if self.gamepad4_ninja != None: # and self.gamepad4_ninja.profile != 'Guest':
			try:
				self.p4_gamepad = copy.deepcopy(data_manager.data_handler.user_profile_dict[self.gamepad4_ninja.profile]['gamepad_layouts'][self.gamepads[3].get_name()])
				#print(self.p1_gamepad['button_menu_image'])
				self.get_images(self.p4_gamepad)
				#print('made0')

			except:
				try:
					#print('made1')
					self.p4_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[3].get_name()])
					self.get_images(self.p4_gamepad)
				except:
					pass
		else:
			try:
				#print('made 2')
				self.p4_gamepad = copy.deepcopy(data_manager.data_handler.gamepad_layout_dict[self.gamepads[3].get_name()])
				self.get_images(self.p4_gamepad)
			except:
				pass


		#link appropriat layouts to ninjas
		if self.gamepad1_ninja != None:
			self.gamepad1_ninja.gamepad_layout = self.p1_gamepad.copy()
		if self.gamepad2_ninja != None:
			self.gamepad2_ninja.gamepad_layout = self.p2_gamepad.copy()
		if self.gamepad3_ninja != None:
			self.gamepad3_ninja.gamepad_layout = self.p3_gamepad.copy()
		if self.gamepad4_ninja != None:
			self.gamepad4_ninja.gamepad_layout = self.p4_gamepad.copy()

		self.gamepad_ninja_list = [self.gamepad1_ninja, self.gamepad2_ninja, self.gamepad3_ninja, self.gamepad4_ninja]
		

		



	def get_images(self, gamepad):
		gamepad['button_menu_image'] = self.button_dict[gamepad['button_menu_image']]
		gamepad['button_jump_image'] = self.button_dict[gamepad['button_jump_image']]
		gamepad['button_roll_image'] = self.button_dict[gamepad['button_roll_image']]
		gamepad['button_item_image'] = self.button_dict[gamepad['button_item_image']]


class Gamepad_Customizer(pygame.sprite.DirtySprite):

	def __init__(self, input_handler, ninja, centerxy, gamepad, gamepad_layout, custom=False):
		pygame.sprite.DirtySprite.__init__(self)

		self.input_handler = input_handler
		self.ninja = ninja
		self.gamepad = gamepad
		self.gamepad_layout = gamepad_layout

		self.custom = custom #True if saving custom controls to user profile

		self.image = pygame.Surface((200,180))
		self.rect = self.image.get_rect()
		self.rect.centerx = centerxy[0] #320 (320,180)
		self.rect.centery = centerxy[1] #180

		self.xbox_layout = pygame.Surface((51,51))
		self.xbox_layout.fill(options.GREEN)
		self.xbox_layout.set_colorkey(options.GREEN)
		self.xbox_layout.blit(self.input_handler.button_xbox_y, (17,0))
		self.xbox_layout.blit(self.input_handler.button_xbox_x, (0,17))
		self.xbox_layout.blit(self.input_handler.button_xbox_b, (17 + 17,17))
		self.xbox_layout.blit(self.input_handler.button_xbox_a, (17,17 + 17))

		self.generic_layout = pygame.Surface((51,51))
		self.generic_layout.fill(options.GREEN)
		self.generic_layout.set_colorkey(options.GREEN)
		self.generic_layout.blit(self.input_handler.button_generic_4, (17,0))
		self.generic_layout.blit(self.input_handler.button_generic_1, (0,17))
		self.generic_layout.blit(self.input_handler.button_generic_3, (17 + 17,17))
		self.generic_layout.blit(self.input_handler.button_generic_2, (17,17 + 17))

		self.nintendo_layout = pygame.Surface((51,51))
		self.nintendo_layout.fill(options.GREEN)
		self.nintendo_layout.set_colorkey(options.GREEN)
		self.nintendo_layout.blit(self.input_handler.button_nintendo_x, (17,0))
		self.nintendo_layout.blit(self.input_handler.button_nintendo_y, (0,17))
		self.nintendo_layout.blit(self.input_handler.button_nintendo_a, (17 + 17,17))
		self.nintendo_layout.blit(self.input_handler.button_nintendo_b, (17,17 + 17))

		self.ps_layout = pygame.Surface((51,51))
		self.ps_layout.fill(options.GREEN)
		self.ps_layout.set_colorkey(options.GREEN)
		self.ps_layout.blit(self.input_handler.button_ps_triangle, (17,0))
		self.ps_layout.blit(self.input_handler.button_ps_square, (0,17))
		self.ps_layout.blit(self.input_handler.button_ps_circle, (17 + 17,17))
		self.ps_layout.blit(self.input_handler.button_ps_x, (17,17 + 17))

		self.checkmark = sprites.level_sheet.getImage(36,336,50,50)
		self.checkmark.set_colorkey(options.GREEN)

		self.check = False
		self.check_timer = 0

		self.status = 'layout'

		#status - layout, botton1, button2, button3, button4, buttonpause, dpad, joystick
		

		self.title_text = menus.font_16.render(self.ninja.name + " Gamepad", 0,(options.WHITE))

		#layout stuff
		self.layout_text = menus.font_16.render("Select Gamepad Layout", 0,(options.WHITE))
		self.position_dict = {1 :  ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) - 35 - 5, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) - 30 - 5),
							2 : ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) - 35 - 5, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) + 30 - 5) , 
							3 : ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) + 35 - 5, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) - 30 - 5), 
							4 : ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) + 35 - 5, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) + 30 - 5) }
		self.position_number = 1
		self.row = 0
		self.column = 0
		self.position_list = [(1,2),(3,4)]

		self.controls_dict = {1 : 'xbox',		
							2 : 'Playstation',
							3: 'Nintendo',
							4: 'Generic'}

		self.button_images = []

		#button stuff
		self.button_press_text = menus.font_16.render("Press the ? Button", 0,(options.WHITE))
		self.button_start_press_text = menus.font_16.render("Press the START Button", 0,(options.WHITE))

		self.jump_press_text = menus.font_16.render("Press Jump/Select", 0,(options.WHITE))
		self.roll_press_text = menus.font_16.render("Press Roll/Back", 0,(options.WHITE))
		self.item_press_text = menus.font_16.render("Press Use Item", 0,(options.WHITE))
		self.menu_press_text = menus.font_16.render("Press Menu Function", 0,(options.WHITE))
		#self.start_press_text = menus.font_16.render("Press Start", 0,(options.WHITE))

		self.stick_left_text = menus.font_16.render("Hold Control Stick Left", 0,(options.WHITE))
		self.stick_up_text = menus.font_16.render("Hold Control Stick Up", 0,(options.WHITE))

		self.dpad_left_text = menus.font_16.render("Hold D-Pad Left", 0,(options.WHITE))
		self.dpad_up_text = menus.font_16.render("Hold D-Pad Up", 0,(options.WHITE))

		self.hold_counter = 0 #used to count button holds.
		self.last_hold = None #used to store last hold

		self.skip_text = menus.font_16.render("Press B to Skip", 0,(options.WHITE))




		self.mapped_buttons = []
		self.mapped_button_dict = {}

		self.direction_delay = 0 #Just used to sneak around weird Mac double press issues.



		sprites.active_sprite_list.add(self)
		sprites.screen_objects.add(self)
		sprites.active_sprite_list.change_layer(self, 100)

		self.dirty = 1
		self.visible = 1


		#Info to collect.
		self.gamepad_name = None

		self.base_controls = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
							'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
							'button_start' :  7,
							'button_menu' : 3, 'button_menu_image' : self.input_handler.button_xbox_y,
							'button_jump' : 0, 'button_jump_image' : self.input_handler.button_xbox_a,
							'button_roll' : 1, 'button_roll_image' : self.input_handler.button_xbox_b,
							'button_item' : 2, 'button_item_image' : self.input_handler.button_xbox_x,
							'sensitivity' : 0.5
							}


		#Just used to lock out main menu controls
		self.ninja.gamepad_config = True

		#self.status = 'stick_left'

	def update(self):
		
		if self.status != 'idle':
			self.dirty = 1
			x_shift = 0
			self.image = menus.Build_CPU_Screen(self.image)
			for bar in  menus.intro_handler.matrix_bar_list:
				#Bars updated in 'main_menu_handler' for simplicity.
				#if options.game_state == 'main_menu':
				#	bar.update()
				if bar.rect.colliderect(0,0,self.rect.width, self.rect.height):
					for digit in bar.digit_list:
						digit.blit(self.image, x_shift) #blits to sprites.screen from within update, based on bar position.
			self.image = menus.Build_Menu_Perimeter(self.image)
			self.image.blit(self.title_text, (self.rect.centerx - self.rect.left - (self.title_text.get_width() / 2), 10))

		if self.status == 'layout':
			if self.direction_delay > 0:
				self.direction_delay -= 1


			if self.check is False:
				if self.direction_delay == 0:
					if self.ninja.menu_left_press is True:
						self.direction_delay = 5
						if self.column == 0:
							self.column = 1
						else:
							self.column = 0
					if self.ninja.menu_right_press is True:
						self.direction_delay = 5
						if self.column == 0:
							self.column = 1
						else:
							self.column = 0
					if self.ninja.menu_down_press is True:
						self.direction_delay = 5
						if self.row == 0:
							self.row = 1
						else:
							self.row = 0
					if self.ninja.menu_up_press is True:
						self.direction_delay = 5
						if self.row == 0:
							self.row = 1
						else:
							self.row = 0
					self.position_number = self.position_list[self.column][self.row]

				if self.ninja.menu_select_press is True or self.ninja.menu_back_press is True or self.ninja.menu_start_press is True or self.ninja.menu_y_press is True or self.ninja.menu_x_press is True:
					self.check = True


					#{1 : 'xbox',		
					#2 : 'Playstation',
					#3: 'Nintendo',
					#4: 'Generic'}

					if self.position_number == 1:
						self.button_images = (self.input_handler.button_xbox_a, self.input_handler.button_xbox_x, self.input_handler.button_xbox_b, self.input_handler.button_xbox_y)
					elif self.position_number == 2:
						self.button_images = (self.input_handler.button_ps_x, self.input_handler.button_ps_square, self.input_handler.button_ps_circle, self.input_handler.button_ps_triangle)
					elif self.position_number == 3:
						self.button_images = (self.input_handler.button_nintendo_a, self.input_handler.button_nintendo_x, self.input_handler.button_nintendo_b, self.input_handler.button_nintendo_y)
					elif self.position_number == 4:
						self.button_images = (self.input_handler.button_generic_1, self.input_handler.button_generic_2, self.input_handler.button_generic_3, self.input_handler.button_generic_4)


			self.image.blit(self.xbox_layout, ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) - 35, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) - 30) )
			self.image.blit(self.ps_layout, ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) - 35, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) + 30) )
			self.image.blit(self.nintendo_layout, ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) + 35, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) - 30) )
			self.image.blit(self.generic_layout, ((self.rect.width/2) - (self.xbox_layout.get_width() / 2) + 35, (self.rect.height/2) - (self.xbox_layout.get_height() / 2) + 30) )
			self.image.blit(self.layout_text, (self.rect.centerx - self.rect.left - (self.layout_text.get_width() / 2), self.rect.height - self.layout_text.get_height() - 10))

			pygame.draw.rect(self.image, options.DARK_PURPLE, (self.position_dict[self.position_number][0],self.position_dict[self.position_number][1],self.xbox_layout.get_width() + 9, self.xbox_layout.get_height() +9), 2)
			if self.check is True:
				self.image.blit(self.checkmark, (self.position_dict[self.position_number][0] + 5 ,self.position_dict[self.position_number][1] + 5))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.gamepad_name = self.gamepad.get_name()
					self.status = 'button0'

		elif self.status == 'button0':
			if self.check is False:
				button_total = self.gamepad.get_numbuttons()
				i = 0
				while i < button_total - 1:
					if self.gamepad.get_button(i) == 1:
						self.check = True
						#store bottons
						self.mapped_buttons.append(i)
						self.mapped_button_dict[i] = self.button_images[0]
						break
					i += 1
			
			self.image.blit(self.button_press_text, (self.rect.centerx - self.rect.left - (self.button_press_text.get_width() / 2), (self.rect.height / 2)))
			self.image.blit(self.button_images[0], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'button1'

		elif self.status == 'button1':
			if self.check is False:
				button_total = self.gamepad.get_numbuttons()
				i = 0
				while i < button_total - 1:
					if self.gamepad.get_button(i) == 1 and i not in self.mapped_buttons:
						self.check = True
						#store bottons
						self.mapped_buttons.append(i)
						self.mapped_button_dict[i] = self.button_images[1]
						break
					i += 1
			
			self.image.blit(self.button_press_text, (self.rect.centerx - self.rect.left - (self.button_press_text.get_width() / 2), (self.rect.height / 2)))
			self.image.blit(self.button_images[1], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'button2'

		elif self.status == 'button2':
			if self.check is False:
				button_total = self.gamepad.get_numbuttons()
				i = 0
				while i < button_total - 1:
					if self.gamepad.get_button(i) == 1 and i not in self.mapped_buttons:
						self.check = True
						#store bottons
						self.mapped_buttons.append(i)
						self.mapped_button_dict[i] = self.button_images[2]
						break
					i += 1
			
			self.image.blit(self.button_press_text, (self.rect.centerx - self.rect.left - (self.button_press_text.get_width() / 2), (self.rect.height / 2)))
			self.image.blit(self.button_images[2], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'button3'

		elif self.status == 'button3':
			if self.check is False:
				button_total = self.gamepad.get_numbuttons()
				i = 0
				while i < button_total - 1:
					if self.gamepad.get_button(i) == 1 and i not in self.mapped_buttons:
						self.check = True
						#store bottons
						self.mapped_buttons.append(i)
						self.mapped_button_dict[i] = self.button_images[3]
						break
					i += 1
			
			self.image.blit(self.button_press_text, (self.rect.centerx - self.rect.left - (self.button_press_text.get_width() / 2), (self.rect.height / 2)))
			self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'buttonStart'

		elif self.status == 'buttonStart':
			if self.check is False:
				button_total = self.gamepad.get_numbuttons()
				i = 0
				while i < button_total - 1:
					if self.gamepad.get_button(i) == 1 and i not in self.mapped_buttons:
						self.check = True
						#store bottons
						self.base_controls['button_start'] = i
						break
					i += 1
			
			self.image.blit(self.button_start_press_text, (self.rect.centerx - self.rect.left - (self.button_start_press_text.get_width() / 2), (self.rect.height / 2)))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'set_jump'

		elif self.status == 'set_jump':
			if self.check is False:
				for button in self.mapped_buttons:
					if self.gamepad.get_button(button) == 1:
						self.check = True
						#store bottons in config
						self.mapped_buttons.remove(button)
						self.base_controls['button_jump'] = button
						self.base_controls['button_jump_image'] = self.mapped_button_dict[button]
						break
			
			self.image.blit(self.jump_press_text, (self.rect.centerx - self.rect.left - (self.jump_press_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65 - 11))
				self.image.blit(self.base_controls['button_jump_image'], ((self.rect.width / 2) - (self.base_controls['button_jump_image'].get_width() / 2),self.rect.height - 15 - 8))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'set_roll'


		elif self.status == 'set_roll':
			if self.check is False:
				for button in self.mapped_buttons:
					if self.gamepad.get_button(button) == 1:
						self.check = True
						#store bottons in config
						self.mapped_buttons.remove(button)
						self.base_controls['button_roll'] = button
						self.base_controls['button_roll_image'] = self.mapped_button_dict[button]
						#self.gamepad_layout['button_roll'] = button
						break
			
			self.image.blit(self.roll_press_text, (self.rect.centerx - self.rect.left - (self.roll_press_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65 - 11))
				self.image.blit(self.base_controls['button_roll_image'], ((self.rect.width / 2) - (self.base_controls['button_roll_image'].get_width() / 2),self.rect.height - 15 - 8))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'set_item'

		elif self.status == 'set_item':
			if self.check is False:
				for button in self.mapped_buttons:
					if self.gamepad.get_button(button) == 1:
						self.check = True
						#store bottons in config
						self.mapped_buttons.remove(button)
						self.base_controls['button_item'] = button
						self.base_controls['button_item_image'] = self.mapped_button_dict[button]
						break
			
			self.image.blit(self.item_press_text, (self.rect.centerx - self.rect.left - (self.item_press_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65 - 11))
				self.image.blit(self.base_controls['button_item_image'], ((self.rect.width / 2) - (self.base_controls['button_item_image'].get_width() / 2),self.rect.height - 15 - 8))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'set_menu'

		elif self.status == 'set_menu':
			if self.check is False:
				for button in self.mapped_buttons:
					if self.gamepad.get_button(button) == 1:
						self.check = True
						#store bottons in config
						self.mapped_buttons.remove(button)
						self.base_controls['button_menu'] = button
						self.base_controls['button_menu_image'] = self.mapped_button_dict[button]
						break
			
			self.image.blit(self.menu_press_text, (self.rect.centerx - self.rect.left - (self.menu_press_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65 - 11))
				self.image.blit(self.base_controls['button_menu_image'], ((self.rect.width / 2) - (self.base_controls['button_menu_image'].get_width() / 2),self.rect.height - 15 - 8))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'stick_left'
			
		
		elif self.status == 'stick_left':
			if self.check is False:
				stick_total = self.gamepad.get_numaxes()
				i = 0
				while i <= stick_total - 1:
					#zzzzzzzzzz
					if i in (0,1) and round(self.gamepad.get_axis(i)) in (-1, 1):
						if self.last_hold != None and self.last_hold == round(self.gamepad.get_axis(i)):
							self.hold_counter += 1
						else:
							self.hold_counter = 0
						self.last_hold = round(self.gamepad.get_axis(i))

						if self.hold_counter > 60:
							self.check = True

							#store bottons
							self.base_controls['stick_LR'] = i
							self.base_controls['stick_L'] = self.last_hold
							self.base_controls['stick_R'] = self.last_hold * -1

							self.hold_counter = 0
							self.last_hold = None

							break
					i += 1

				if self.gamepad.get_button(self.base_controls['button_roll']) == 1:
					self.check = True

			
			self.image.blit(self.stick_left_text, (self.rect.centerx - self.rect.left - (self.stick_left_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'stick_up'

			else:
				self.image.blit(self.skip_text, ((self.rect.width / 2) - (self.skip_text.get_width() / 2),self.rect.height - 30))
				self.image.blit(self.base_controls['button_roll_image'], ((self.rect.width / 2) - 16,self.rect.height - 31))
				

		elif self.status == 'stick_up':
			if self.check is False:
				stick_total = self.gamepad.get_numaxes()
				i = 0
				while i <= stick_total - 1:

					if i in (0,1) and round(self.gamepad.get_axis(i)) in (-1, 1):
						if self.last_hold != None and self.last_hold == round(self.gamepad.get_axis(i)) and i != self.base_controls['stick_LR']:
							self.hold_counter += 1
						else:
							self.hold_counter = 0
						self.last_hold = round(self.gamepad.get_axis(i))

						if self.hold_counter > 60:
							self.check = True

							#store bottons
							self.base_controls['stick_UD'] = i
							self.base_controls['stick_U'] = self.last_hold
							self.base_controls['stick_D'] = self.last_hold * -1

							self.hold_counter = 0
							self.last_hold = None

							break
					i += 1

				if self.gamepad.get_button(self.base_controls['button_roll']) == 1:
					self.check = True
			
			self.image.blit(self.stick_up_text, (self.rect.centerx - self.rect.left - (self.stick_up_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'dpad_left'
			else:
				self.image.blit(self.skip_text, ((self.rect.width / 2) - (self.skip_text.get_width() / 2),self.rect.height - 30))
				self.image.blit(self.base_controls['button_roll_image'], ((self.rect.width / 2) - 16,self.rect.height - 31))
				



		elif self.status == 'dpad_left':
			if self.check is False:
				dpad_total = self.gamepad.get_numhats()
				i = 0
				while i <= dpad_total - 1:

					if self.gamepad.get_hat(i) != (0,0):
						if self.last_hold != None and self.last_hold == self.gamepad.get_hat(i):
							self.hold_counter += 1
						else:
							self.hold_counter = 0
						self.last_hold = self.gamepad.get_hat(i)

						if self.hold_counter > 60:
							self.check = True

							#store bottons
							#'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,

							self.base_controls['dpad'] = i
							if self.last_hold[0] != 0:
								temp_value = 0 #self.last_hold[1]
							else:
								temp_value = 1 #self.last_hold[0]
							self.base_controls['dpad_LR'] = temp_value
							self.base_controls['dpad_L'] = self.last_hold[temp_value]
							self.base_controls['dpad_R'] = self.last_hold[temp_value] * -1

							self.hold_counter = 0
							self.last_hold = None

							break
					i += 1

				if self.gamepad.get_button(self.base_controls['button_roll']) == 1:
					self.check = True
			
			self.image.blit(self.dpad_left_text, (self.rect.centerx - self.rect.left - (self.dpad_left_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'dpad_up'

			else:
				self.image.blit(self.skip_text, ((self.rect.width / 2) - (self.skip_text.get_width() / 2),self.rect.height - 30))
				self.image.blit(self.base_controls['button_roll_image'], ((self.rect.width / 2) - 16,self.rect.height - 31))
				

		elif self.status == 'dpad_up':
			if self.check is False:
				dpad_total = self.gamepad.get_numhats()
				i = 0
				while i <= dpad_total - 1:
					if self.base_controls['dpad_LR'] == 0:
						other_hat = 1
					else:
						other_hat = 0
					if self.gamepad.get_hat(i) != (0,0) and self.gamepad.get_hat(i)[other_hat] != 0:
						if self.last_hold != None and self.last_hold == self.gamepad.get_hat(i) and i == self.base_controls['dpad']:
							self.hold_counter += 1
						else:
							self.hold_counter = 0
						self.last_hold = self.gamepad.get_hat(i)

						if self.hold_counter > 60:
							self.check = True

							#store bottons
							#'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,

							if self.last_hold[0] != 0:
								temp_value = 0 #self.last_hold[1]
							else:
								temp_value = 1 #self.last_hold[0]
							self.base_controls['dpad_UD'] = temp_value
							self.base_controls['dpad_U'] = self.last_hold[temp_value]
							self.base_controls['dpad_D'] = self.last_hold[temp_value] * -1

							self.hold_counter = 0
							self.last_hold = None

							break
					i += 1

				if self.gamepad.get_button(self.base_controls['button_roll']) == 1:
					self.check = True

			self.image.blit(self.dpad_up_text, (self.rect.centerx - self.rect.left - (self.dpad_up_text.get_width() / 2), (self.rect.height / 2) - 5))
			#self.image.blit(self.button_images[3], ((self.rect.width / 2) + 3, (self.rect.height / 2) - 1))

			if self.check is True:
				self.image.blit(self.checkmark, ((self.rect.width / 2) - (self.checkmark.get_width() / 2),self.rect.height - 65))
				self.check_timer += 1 * (60 / options.current_fps)
				if self.check_timer >= 60:
					self.check = False
					self.check_timer = 0
					self.status = 'done'
			else:
				self.image.blit(self.skip_text, ((self.rect.width / 2) - (self.skip_text.get_width() / 2),self.rect.height - 30))
				self.image.blit(self.base_controls['button_roll_image'], ((self.rect.width / 2) - 16,self.rect.height - 31))
				
		
		
		elif self.status == 'done':
			self.gamepad_layout = self.base_controls.copy()
			self.ninja.gamepad_config = False #Used for locking out regular menu controls
			self.ninja.gamepad_layout = self.gamepad_layout
			
			#Save current profile for future use
			self.convert_images(self.base_controls)
			if self.custom is True: #and self.ninja.profile != 'Guest':
				data_manager.data_handler.user_profile_dict[self.ninja.profile]['gamepad_layouts'][self.gamepad.get_name()] = copy.deepcopy(self.base_controls)
			elif self.custom is False:
				data_manager.data_handler.gamepad_layout_dict[self.gamepad.get_name()] = copy.deepcopy(self.base_controls)
			
			self.ninja.controls_sprite.update_buttons()
			
			data_manager.data_handler.save_data()

			self.kill()

	def convert_images(self, base_controls):
		for key in self.input_handler.button_dict.keys():
			if self.input_handler.button_dict[key] == base_controls['button_menu_image']:
				base_controls['button_menu_image'] = key
			elif self.input_handler.button_dict[key] == base_controls['button_jump_image']:
				base_controls['button_jump_image'] = key
			elif self.input_handler.button_dict[key] == base_controls['button_roll_image']:
				base_controls['button_roll_image'] = key
			elif self.input_handler.button_dict[key] == base_controls['button_item_image']:
				base_controls['button_item_image'] = key
