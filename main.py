#Demo v0.00


import os
import pygame
import random
import sounds
import ninja
import level
import menus
import sprites
import options
import controls
import data_manager
import time
import math

import logging




def main():

	pygame.mixer.pre_init(44100,-16,2, 2048)
	#pygame.mixer.pre_init(44100,-16,2, 2048)

	pygame.init() 
	pygame.joystick.quit()

	pygame.mixer.init()
	pygame.mixer.set_num_channels(16)
	sounds.mixer = sounds.Sound_Mixer()

	#logging.basicConfig(filename='test.log', level = logging.INFO)

	pygame.joystick.init()
	options.gamepads = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
	for gamepad in options.gamepads:
		gamepad.init()

	
	i = sprites.create_players() #goes into sprites.py and creates players. Allows them to be held in sprites to py.
	sprites.player1 = i[0]
	sprites.player2 = i[1]
	sprites.player3 = i[2]
	sprites.player4 = i[3]

	controls.input_handler = controls.Input_Handler()
	data_manager.data_handler = data_manager.Data_Handler()

	level.level_builder = level.Level_Builder()
	#coop.level_builder = coop.Level_Builder()

	def get_opposite(current):
		opposite = ""
		if current == 'on':
			opposite = 'off'
		elif current == 'off':
			opposite = 'on'
		elif current == 'On':
			opposite = 'Off'
		elif current == 'Off':
			opposite = 'On'
		elif current == 'keyboard':
			opposite = 'gamepad'
		elif current == 'gamepad':
			opposite = 'keyboard'
		elif current == 'x-input':
			opposite = 'd-input'
		elif current == 'd-input':
			opposite = 'x-input'
		return opposite


	menus.instruction_booklet_sprite = menus.Instruction_Booklet_Sprite()
	menus.versus_level_selection_sprite = menus.Level_Selection_Sprite('versus')
	menus.coop_level_selection_sprite = menus.Level_Selection_Sprite('coop')
	menus.pause_sprite = menus.Menu_Selection_Sprite('pause',(('Resume', ['']), ('Quit Game', [''])), menus.font_30, (200,150), 0)
	menus.pause_sprite_items = menus.Menu_Selection_Sprite('pause',(('Resume', ['']), ('Item Options', ['']), ('Quit Game', [''])), menus.font_30, (200,150), 0)
	menus.pause_sprite_online_host = menus.Menu_Selection_Sprite('pause',(('Resume', ['']), ('Level Select', ['']), ('Quit Online', [''])), menus.font_30, (200,150), 0)
	menus.pause_sprite_online_guest = menus.Menu_Selection_Sprite('pause',(('Resume', ['']), ('Quit Online', [''])), menus.font_30, (200,150), 0)
	sprites.active_sprite_list.add(menus.pause_sprite)
	sprites.active_sprite_list.change_layer(menus.pause_sprite, 10)
	menus.pause_sprite.visible = 0

	menus.main_menu_sprite = menus.Menu_Selection_Sprite('main_menu',(('Versus', ['']), ('Settings', ['']), ('Instructions', ['']), ('Quit', [''])), menus.font_30, None, 100)

	menus.online_menu_sprite = menus.Menu_Selection_Sprite('online_menu',(('Quick Match', ['']), ('Host Match', ['']), ('Join Match', ['']), ('_space_', ['']), ('Return', [''])), menus.font_30, None, 0)

	menus.game_options_sprite = menus.Menu_Selection_Sprite('game_options',(
																('Music Volume', [3,4,5,6,7,8,9,10,0,1,2] ),
																('Sound FX Volume', [3,4,5,6,7,8,9,10,0,1,2] ),
																('_space_', ['']),
																('Player 1 Input Preference', [options.control_preferences['player1'], get_opposite(options.control_preferences['player1'])]),
																('Player 2 Input Preference', [options.control_preferences['player2'], get_opposite(options.control_preferences['player2'])]),
																('_space_', ['']),
																('FPS Counter', [options.FPS_counter, get_opposite(options.FPS_counter)]),
																('Rope Physics', [options.rope_physics, get_opposite(options.rope_physics)]),
																('Bandana Physics', [options.bandana_physics, get_opposite(options.bandana_physics)]),
																('Visual Effects', ['High', 'Off', 'Low']),
																('Screen Shake', [options.screen_shake, get_opposite(options.screen_shake)]),
																('_space_', ['']),
																('Credits', ['']),
																('_space_', ['']),
																('Accept', [''])

																), menus.font_20, None, 0)

	menus.versus_mode_sprite = menus.Menu_Selection_Sprite('versus_mode',(('Classic', ['']), ('Points', ['']), ('Stock', ['']), ('Practice', ['']), ('Tutorial', [''])), menus.font_30, None, 100)

	menus.versus_options_sprite = menus.Menu_Selection_Sprite('versus_options',(
																('Game Mode', ['Classic', 'Points']), 
																('Stage Selection', ['Choice', 'Random'] ),
																('Victory', [5,6,7,8,9,10,15,20,30,40,50,75,100,1,2,3,4]), 
																('Score Frequency', [5,10,'Off',1,2] ),
																('Item Options', [''] ),
																('_space_', [''] ),
																('Return', [''] )
																),
																	menus.font_20, None, 0)

	menus.versus_item_options_sprite = menus.Menu_Selection_Sprite('versus_item_options',(	
																('x', [ 'on', 'off' ] ),
																('shoes', [ 'on', 'off' ] ),
																('laser', [ 'on', 'off' ] ),
																('wings', [ 'on', 'off' ] ),
																('skull', [ 'on', 'off' ] ),
																('bomb', [ 'on', 'off' ] ),
																('volt', [ 'on', 'off' ] ),
																('mine', [ 'on', 'off' ] ),
																('rocket', [ 'on', 'off' ] ),
																('shield', [ 'on', 'off' ] ),
																('ice bomb', [ 'on', 'off' ] ),
																('cloak', [ 'on', 'off' ] ),
																('portal gun', [ 'off', 'off' ] ),
																('homing bomb', [ 'off', 'off' ] ),
																('metal suit', [ 'off', 'off' ] ),
																('solar flare', [ 'off', 'off' ] ),
																('gravity', ['off', 'off' ] ),

																('_space_', [''] ),
																('_space_', [''] ),
																('_space_', [''] ),
																('Return', [''] )
																),
																	menus.font_20, None, 0)



	#small screen
	#sprites.screen = pygame.Surface((sprites.size[0], sprites.size[1]))
	#size = (640,360)
	#big_screen = pygame.display.set_mode(size) 

	#actual work

	sprites.screen = pygame.Surface((sprites.size[0], sprites.size[1]))
	#os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

	
	sprites.big_screen = pygame.display.set_mode(options.screen_resolution, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
	options.fullscreen = True

	#sprites.big_screen = pygame.display.set_mode(options.screen_resolution, pygame.NOFRAME)
	
	#sprites.big_screen = pygame.display.set_mode(options.screen_resolution)
	#options.fullscreen = False
	
	sprites.shake_screen = pygame.Surface((sprites.size[0], sprites.size[1]))





	#sprites.screen = pygame.display.set_mode((640,360), pygame.FULLSCREEN)
	
	#sprites.screen = pygame.display.set_mode((640,360), pygame.FULLSCREEN)
	#big_screen = pygame.display.set_mode((640,360))

	#the whole level. Much larger than the screen.
	#level_canvas = pygame.Surface((1200, 1200))
	
	#pygame.display.set_caption("Duel") 

	#create groups to hold sprites

	
	# Used to manage how fast the screen updates 
	clock = pygame.time.Clock()

	pygame.mouse.set_visible(False)

	#block unwanted events from event queue to keep the path clear
	pygame.event.set_allowed(None)
	pygame.event.set_allowed((pygame.KEYDOWN, pygame.KEYUP, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION, pygame.JOYAXISMOTION))
	#pygame.event.set_allowed((pygame.KEYDOWN, pygame.KEYUP, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP))


	#put background music on to start
	#sounds.mixer.change_song('music_menu.wav')
	#sounds.mixer.background_music.set_volume(options.music_volume)
	#sounds.mixer.start_song()

	data_manager.data_handler.load_data() #load all saved things

	options.game_state = 'none'
	game_delay = 0

	blit_switch = True

	fps_adjustor = 0 #if hits 5 need to flip up or down between 30/60 fps.


	# Main Program Loop
	while options.exit is False:
		#try:

			if options.update_state == 1:
				options.update_state = 2
			else:
				options.update_state = 1

			controls.input_handler.update()
			

			if options.game_state == 'intro':
				menus.intro_handler.update()

			#elif options.game_state == 'main_menu_controls':
			#	controls.

			elif options.game_state == 'none':
				game_delay += 1
				if game_delay >= 0:
					options.game_state = 'intro'

			elif options.game_state == 'main_menu':
				menus.main_menu_handler.update()

			elif options.game_state == 'instructions':
				menus.instruction_booklet_sprite.update()

			elif options.game_state == 'player_select':
				menus.player_select_handler.update()
				#menus.player_select()

			elif options.game_state == 'online_menu':
				menus.online_menu_handler.update()
				#menus.player_select()


			elif options.game_state == 'versus_options':
				#menus.versus_options()
				menus.versus_options_handler.update()

			elif options.game_state == 'versus_mode':
				#menus.versus_options()
				menus.versus_mode_handler.update()


			elif options.game_state == 'versus_item_options':
				#menus.versus_options()
				menus.versus_item_handler.update()

			elif options.game_state == 'versus_level_selection':
				menus.versus_level_selection_handler.update()
				#menus.versus_level_selection()

			elif options.game_state == 'coop_level_selection':
				menus.coop_level_selection_handler.update()

			elif options.game_state == 'game_options':
				menus.game_options_handler.update()
				#menus.game_options()

			elif options.game_state == 'game_credits':
				menus.credits_handler.update()
				#menus.game_options()


			elif options.game_state == 'pause':
				menus.pause_handler.update()
				'''
				if options.win_condition == 'tutorial':
					menus.tutorial_pause_handler.update()
				else:
					menus.pause_handler.update()
				'''

			elif options.game_state == 'online_pause':
				menus.online_pause_handler.update()

			elif options.game_state == 'choice':
				menus.choice_handler.update() 

			elif options.game_state == 'versus_score':
				menus.versus_score_handler.update()
				#menus.versus_score()

			elif options.game_state == 'versus_awards':
				menus.versus_awards_handler.update()
				#menus.versus_score()
			

			elif options.game_state == 'level': #main loop

			
				# Update the player and other sprites as needed
				
				
				i = 0
				while i < 60:
						if i == 0:					
							sprites.screenshot_handler.update()
					
						if options.current_fps == 60 or i > 0:
							options.blit_frame = True
						else:
							options.blit_frame = False
							

						if sprites.effects_screen.status == 'gravity':
							sprites.effects_screen.update()
						else:
							sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
							sprites.enemy_list.update()
							sprites.item_effects.update()


							sprites.tile_list.update()
							if sprites.countdown_timer.level_go is True:
								sprites.level_objects.update()
							
							sprites.level_ropes.update()
							sprites.background_objects.update()
							sprites.gravity_objects.update()
							sprites.visual_effects.update()
							sprites.screen_objects.update()

							if sprites.countdown_timer.done is True:
								level.Collision_Check() #Handles Non-Tile collision checks

						
						i += options.current_fps
						if i < 60:
							controls.input_handler.update() #need to update controls a second time to keep movement/frames the same
				

				
			
				
				
				
			
				'''ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT'''        
				sprites.active_sprite_list.draw(sprites.screen)

			i = round(clock.get_fps())

			#Get Current FPS:
			if options.fps == 'Auto':
				options.current_fps = options.auto_fps
			
			
			
			if options.fps == 'Auto':
				time = clock.get_rawtime()
				if time == 0:
					frame_fps = 60
				else:
					frame_fps = round(1 / (time / 1000))

				if options.current_fps == 60:
					if frame_fps < 58:
						fps_adjustor += 1
					else:
						fps_adjustor = 0

					if fps_adjustor >= 2:
						fps_adjustor = 0
						options.auto_fps = 30
						options.current_fps = 30

				elif options.current_fps == 30:
					if frame_fps >= 60:
						fps_adjustor += 1
					else:
						fps_adjustor = 0

					if fps_adjustor >= 5:
						fps_Adjustor = 0
						options.auto_fps = 60
						options.current_fps = 60
			

			
			
			#clock.tick(options.current_fps)
			clock.tick_busy_loop(options.current_fps)
			#clock.tick()
			

			if options.screen_shake == 'On':
				shake_shift = sprites.shake_handler.update_shake()
				sprites.shake_screen.blit(sprites.screen, shake_shift)
				pygame.transform.scale(sprites.shake_screen, options.screen_resolution, sprites.big_screen)
				
			else:
				pygame.transform.scale(sprites.screen, options.screen_resolution, sprites.big_screen)

			
			#sprites.big_screen.blit(sprites.screen,  (0,0))
	
			#FPS COUNTER:			
			if options.FPS_counter == 'On':
				if i < options.current_fps - 5:
					color = (255,0,0)
				elif i < options.current_fps - 2:
					color = (255,255, 0)
				else:
					color = (0,255,0)
				fps_text = menus.font_16.render(str(i),0,color)#, options.BLACK)
				sprites.big_screen.blit(fps_text,(0,0))
			

			# Go ahead and update the screen with what we've drawn. 
			pygame.display.flip()



			#check for a win!
			level.check_win()

		#except Exception as e:
		#	logging.info(str(e))
		#	options.exit = True


	pygame.quit ()

if __name__ == "__main__":
	main()
