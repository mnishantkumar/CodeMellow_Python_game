import pygame
import shelve
import dbm
import controls
import options
import copy
import sys
import os

if getattr(sys, 'frozen', False):
	Current_Path = os.path.dirname(sys.executable)
else:
	Current_Path = str(os.path.dirname(__file__))# + str('/GameData/')

#base gamepad layouts
data_handler = None

class Data_Handler():

	#place Ninja attributes here

	def __init__(self):


		self.gamepad_layout_dict = {}


		xbox_layout = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
						'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
						'button_start' :  7,
						'button_menu' : 3, 'button_menu_image' : 'xbox_y',
						'button_jump' : 0, 'button_jump_image' : 'xbox_a',
						'button_roll' : 1, 'button_roll_image' : 'xbox_b',
						'button_item' : 2, 'button_item_image' : 'xbox_x',
						'sensitivity' : 0.5
						}
		
		mac_logitech = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
						'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
						'button_start' :  9,
						'button_menu' : 3, 'button_menu_image' : 'xbox_y',
						'button_jump' : 1, 'button_jump_image' : 'xbox_a',
						'button_roll' : 2, 'button_roll_image' : 'xbox_b',
						'button_item' : 0, 'button_item_image' : 'xbox_x',
						'sensitivity' : 0.5
						}

		mac_playstation = {'dpad' : 0, 'dpad_LR' : 0, 'dpad_L' : -1, 'dpad_R': 1, 'dpad_UD' : 1, 'dpad_U' : 1, 'dpad_D' : -1,
						'stick_LR' : 0, 'stick_R' : 1, 'stick_L' : -1, 'stick_UD' : 1, 'stick_U' : -1, 'stick_D' : 1,
						'button_start' :  9,
						'button_menu' : 3, 'button_menu_image' : 'ps_triangle',
						'button_jump' : 1, 'button_jump_image' : 'ps_x',
						'button_roll' : 2, 'button_roll_image' : 'ps_square',
						'button_item' : 0, 'button_item_image' : 'ps_circle',
						'sensitivity' : 0.5
						}


		self.gamepad_layout_dict['xbox'] = xbox_layout
		self.gamepad_layout_dict['mac_log'] = mac_logitech
		self.gamepad_layout_dict['mac_ps'] = mac_playstation


		self.user_profile_dict = {}
		'''sample user profile'''
		self.base_profile = {
					'gamepad_layouts' : {},
					'Swag' : ['Bandana', 'Headband', 'None'],
					'Avatar' : ['Ninja', 'Robot', 'Mutant', 'Cyborg'],
					'Unlocks' : {'test' : None},
					'Options' : {'test' : None},
					'Stats' : {
								'stats_FIDs_inflicted' : 0,
								'stats_FIDs_received' : 0,
								'stats_FIDs_suicide' : 0,
								'stats_item_kills' : 0,
								'stats_item_deaths' : 0,
								'stats_ally_item_kill' : 0,
								'stats_ally_FIDs_inflicted' : 0,
								'VP_earned' : 0,
								'wins_earned' : 0,

								'stats_x_pixels_travelled' : 0,
								'stats_y_pixels_travelled' : 0,
								'stats_jumps_performed' : 0,
								'stats_frames_jumping' : 0,
								'stats_wall_jumps_performed' : 0,
								'stats_rolls_performed' : 0,
								'stats_ducks_performed' : 0,
								'stats_frames_rolling' : 0,
								'stats_frames_falling' : 0,
								'stats_frames_running' : 0,
								'stats_frames_idle' : 0,
								'stats_frames_smug' : 0,
								'stats_frames_ducking' : 0,
								'stats_knocks_received' : 0,
								'stats_knocks_inflicted' : 0,


								'stats_shoes_acquired' : 0,
								'stats_shoes_pixels_travelled' : 0,


								'stats_laser_acquired' : 0,
								'stats_laser_fired' : 0,
								'stats_laser_kills' : 0,
								'stats_laser_suicides' : 0,
								'stats_laser_double_kills' : 0,
								'stats_laser_triple_kills' : 0,
								'stats_laser_vertical_kills' : 0,

								'stats_wings_acquired' : 0,
								'stats_wing_double_jumps' : 0,

								'stats_skull_acquired' : 0,

								'stats_bomb_acquired' : 0,
								'stats_bomb_thrown' : 0,
								'stats_bomb_kills' : 0,
								'stats_bomb_suicides' : 0,
								'stats_bomb_double_kills' : 0,
								'stats_bomb_triple_kills' : 0,

								'stats_volt_acquired' : 0,
								'stats_volt_kills' : 0,
								'stats_volt_double_kills' : 0,
								'stats_volt_triple_kills' : 0,

								'stats_mine_acquired' : 0,
								'stats_mine_thrown' : 0,
								'stats_mine_kills' : 0,
								'stats_mine_suicides' : 0,
								'stats_mine_double_kills' : 0,
								'stats_mine_triple_kills' : 0,

								'stats_rocket_acquired' : 0,
								'stats_rocket_fired' : 0,
								'stats_rocket_pixels_travelled' : 0,
								'stats_rocket_kills' : 0,
								'stats_rocket_suicides' : 0,
								'stats_rocket_double_kills' : 0,
								'stats_rocket_triple_kills' : 0,

								'stats_portal_gun_acquired' : 0,
								'stats_portal_gun_fired' : 0,
								'stats_portal_gun_portals_created' : 0,
								'stats_portal_gun_ninjas_teleported' : 0,
								'stats_portal_gun_FIDs_inflicted' : 0,
								'stats_portal_gun_FIDs_received' : 0,
								'stats_portal_gun_times_teleported' : 0,
								'stats_portal_gun_distance_teleported' : 0,
								'stats_portal_gun_items_teleported' : 0,

								'stats_ice_bomb_acquired' : 0,
								'stats_ice_bomb_thrown' : 0,
								'stats_ice_bomb_cubes_made' : 0,
								'stats_ice_bomb_self_cubes' : 0,
								'stats_ice_bomb_times_frozen' : 0,
								'stats_ice_bomb_cube_FIDs' : 0,
								'stats_ice_bomb_double_cubes' : 0,
								'stats_ice_bomb_triple_cubes' : 0,
								'stats_ice_bomb_quadruple_cubes' : 0,

								'stats_cloak_acquired' : 0,
								'stats_frames_invisible' : 0,
								'stats_invisible_FIDs_inflicted' : 0,
								'stats_invisible_FIDs_received' : 0,
								'stats_invisible_item_deaths' : 0,
								'stats_invisible_homing_bomb_evaded' : 0,

								'stats_shield_acquired' : 0,
								'stats_frames_with_shield_active' : 0,
								'stats_shield_weapons_rebounded' : 0,

								'stats_homing_bomb_acquired' : 0,
								'stats_homing_bomb_activated' : 0,
								'stats_homing_bomb_transferred' : 0,
								'stats_homing_bomb_received' : 0,
								'stats_homing_bomb_active_frames' : 0,
								'stats_homing_bomb_kills' : 0,
								'stats_homing_bomb_suicides' : 0,

								'stats_gravity_acquired' : 0,
								'stats_gravity_used' : 0,
								'stats_frames_gravity_inverted' : 0,
								'stats_frames_gravity_normal' : 0,
								'stats_gravity_FIDs_inflicted' : 0,

								'duels_participated' : 0,
								'matches_participated' : 0,
								'stats_duels_survived' : 0,
								'stats_matches_won' : 0,
								'stats_matches_lost' : 0,
								'stats_solo_matches_won' : 0,
								'stats_solo_matches_lost' : 0,
								'stats_matches_1v2_won' : 0,
								'stats_matches_1v2_lost' : 0,
								'stats_matches_1v3_won' : 0,
								'stats_matches_1v3_lost' : 0,
								'stats_matches_2v2_won' : 0,
								'stats_matches_2v2_lost' : 0,
								'stats_matches_3v1_won' : 0,
								'stats_matches_3v1_lost' : 0,
								'stats_matches_2v1_won' : 0,
								'stats_matches_2v1_lost' : 0

								}
				}




	def load_data(self):

		shelfFile = shelve.open(os.path.join(Current_Path, 'game_data'))

		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			self.user_profile_dict = shelfFile['user_profile_dict']
			options.profile_list = ['-New Profile-']
			for key in self.user_profile_dict.keys():
				options.profile_list.append(key)
			#constants.game_settings = shelfFile['game_settings']
		except KeyError:
			pass
		

		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			self.gamepad_layout_dict = shelfFile['gamepad_layout_dict']
			#constants.game_settings = shelfFile['game_settings']
		except KeyError:
			pass

		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			self.base_profile = shelfFile['base_profile']
			#constants.game_settings = shelfFile['game_settings']
		except KeyError:
			pass

		
		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			self.game_settings = shelfFile['game_settings']
			
			options.music_volume = self.game_settings[0]
			options.effects_volume = self.game_settings[1]
			options.FPS_counter = self.game_settings[2]
			options.rope_physics = self.game_settings[3]
			options.bandana_physics = self.game_settings[4]
			options.screen_shake = self.game_settings[5]
			options.visual_effects = self.game_settings[6]
			options.background_effects = self.game_settings[7]
			options.death_animations = self.game_settings[8]
			options.particles = self.game_settings[9]
			#options.control_preferences['player1'] = self.game_settings[10]
			#options.control_preferences['player2'] = self.game_settings[11]

		except KeyError:
			pass

		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			options.server_message = shelfFile['server_message']
			#constants.game_settings = shelfFile['game_settings']
		except KeyError:
			pass

		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			options.color_choices = shelfFile['color_choices']
			#constants.game_settings = shelfFile['game_settings']
		except KeyError:
			pass

		try: #After we have created a save file it should load properly. Before we have created data this should just be passed over.
			options.bandana_color_choices = shelfFile['bandana_color_choices']
			#constants.game_settings = shelfFile['game_settings']
		except KeyError:
			pass



		if 'Player1' not in self.user_profile_dict.keys():	
			self.user_profile_dict['Player1'] = copy.deepcopy(self.base_profile)
			#options.profile_list.append('Player1')

		if 'Player2' not in self.user_profile_dict.keys():	
			self.user_profile_dict['Player2'] = copy.deepcopy(self.base_profile)
			#options.profile_list.append('Player2')

		if 'Player3' not in self.user_profile_dict.keys():	
			self.user_profile_dict['Player3'] = copy.deepcopy(self.base_profile)
			#options.profile_list.append('Player3')

		if 'Player4' not in self.user_profile_dict.keys():	
			self.user_profile_dict['Player4'] = copy.deepcopy(self.base_profile)
			#options.profile_list.append('Player4')

		#if 'Ancalabro' not in self.user_profile_dict.keys():	
		#	self.user_profile_dict['Ancalabro'] = copy.deepcopy(self.base_profile)
		#	options.profile_list.append('Ancalabro')


		shelfFile.close()

	def save_data(self):

		shelfFile = shelve.open(os.path.join(Current_Path, 'game_data'))
		
		
		shelfFile['base_profile'] = self.base_profile

		shelfFile['user_profile_dict'] = self.user_profile_dict
		shelfFile['gamepad_layout_dict'] = self.gamepad_layout_dict

		shelfFile['server_message'] = options.server_message
		shelfFile['color_choices'] = options.color_choices
		shelfFile['bandana_color_choices'] = options.bandana_color_choices
		
		shelfFile['game_settings'] = [options.music_volume,
									options.effects_volume,
									options.FPS_counter,
									options.rope_physics,
									options.bandana_physics,
									options.screen_shake,
									options.visual_effects,
									options.background_effects,
									options.death_animations,
									options.particles,
									#options.control_preferences['player1'],
									#options.control_preferences['player2']
										]		

		shelfFile.close()


