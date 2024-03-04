import pygame
import options
import sprites
import os
import sys

if getattr(sys, 'frozen', False):
	Current_Path = sys._MEIPASS
else:
	Current_Path = str(os.path.dirname(__file__)) + str('/GameData/')

mixer = None

class Sound_Mixer():

	#place Ninja attributes here

	def __init__(self):
		self.background_music = None #holds the current background music for whatever level/screen
		self.channel = None #to hold whichever channel the background music plays
		
		#sounds.mixer.channel = sounds.mixer.background_music.play(loops=-1)

		self.sound_list = []

		self.menu_move = pygame.mixer.Sound(os.path.join(Current_Path, 'menu_move.wav'))
		self.sound_list.append(self.menu_move)

		self.menu_select = pygame.mixer.Sound(os.path.join(Current_Path, 'menu_select.wav'))
		self.sound_list.append(self.menu_select)

		self.menu_back = pygame.mixer.Sound(os.path.join(Current_Path, 'menu_move.wav'))
		self.sound_list.append(self.menu_back)

		self.countdown_beep = pygame.mixer.Sound(os.path.join(Current_Path, 'countdown_beep.wav'))
		self.sound_list.append(self.countdown_beep)

		self.countdown_go = pygame.mixer.Sound(os.path.join(Current_Path, 'countdown_go.wav'))
		self.sound_list.append(self.countdown_go)

		self.type = pygame.mixer.Sound(os.path.join(Current_Path, 'type3.wav'))
		self.sound_list.append(self.type)

		self.scan = pygame.mixer.Sound(os.path.join(Current_Path, 'scan2.wav'))
		self.sound_list.append(self.scan)
		
		self.jump = pygame.mixer.Sound(os.path.join(Current_Path, 'jump.wav'))
		self.sound_list.append(self.jump)

		self.FID = pygame.mixer.Sound(os.path.join(Current_Path, 'FID.wav'))
		self.sound_list.append(self.FID)

		self.death = pygame.mixer.Sound(os.path.join(Current_Path, 'death.wav'))
		self.sound_list.append(self.death)

		self.knocked = pygame.mixer.Sound(os.path.join(Current_Path, 'knocked.wav'))
		self.sound_list.append(self.knocked)

		self.laser = pygame.mixer.Sound(os.path.join(Current_Path, 'laser.wav'))
		self.sound_list.append(self.laser)

		self.portal_gun_fire = pygame.mixer.Sound(os.path.join(Current_Path, 'portal_gun_fire.wav'))
		self.sound_list.append(self.portal_gun_fire)

		self.portal_gun_portal = pygame.mixer.Sound(os.path.join(Current_Path, 'portal_gun_portal.wav'))
		self.sound_list.append(self.portal_gun_portal)

		self.portal_gun_teleport = pygame.mixer.Sound(os.path.join(Current_Path, 'portal_gun_teleport.wav'))
		self.sound_list.append(self.portal_gun_teleport)

		self.explosion = pygame.mixer.Sound(os.path.join(Current_Path, 'explosion.wav'))
		self.sound_list.append(self.explosion)

		self.freeze = pygame.mixer.Sound(os.path.join(Current_Path, 'freeze.wav'))
		self.sound_list.append(self.freeze)

		self.shatter = pygame.mixer.Sound(os.path.join(Current_Path, 'shatter.wav'))
		self.sound_list.append(self.shatter)

		self.bounce = pygame.mixer.Sound(os.path.join(Current_Path, 'bounce.wav'))
		self.sound_list.append(self.bounce)

		self.rocket = pygame.mixer.Sound(os.path.join(Current_Path, 'rocket.wav'))
		self.sound_list.append(self.rocket)

		self.gravity = pygame.mixer.Sound(os.path.join(Current_Path, 'gravity.wav'))
		self.sound_list.append(self.gravity)

		self.mine = pygame.mixer.Sound(os.path.join(Current_Path, 'mine.wav'))
		self.sound_list.append(self.mine)

		self.collect_item = pygame.mixer.Sound(os.path.join(Current_Path, 'collect_item.wav'))
		self.sound_list.append(self.collect_item)

		self.activate_metal_suit = pygame.mixer.Sound(os.path.join(Current_Path, 'activate_metal_suit.wav'))
		self.sound_list.append(self.activate_metal_suit)

		self.shield = pygame.mixer.Sound(os.path.join(Current_Path, 'shield.wav'))
		self.sound_list.append(self.shield)

		self.cloak = pygame.mixer.Sound(os.path.join(Current_Path, 'cloak.wav'))
		self.sound_list.append(self.cloak)

		self.volt = pygame.mixer.Sound(os.path.join(Current_Path, 'volt.wav'))
		self.sound_list.append(self.volt)

		self.heavy_step = pygame.mixer.Sound(os.path.join(Current_Path, 'heavy_step.wav'))
		self.sound_list.append(self.heavy_step)
		
		self.block_break = pygame.mixer.Sound(os.path.join(Current_Path, 'block_break.wav'))
		self.sound_list.append(self.block_break)

		self.metal_pound = pygame.mixer.Sound(os.path.join(Current_Path, 'metal_pound.wav'))
		self.sound_list.append(self.metal_pound)

		self.solar_flare = pygame.mixer.Sound(os.path.join(Current_Path, 'solar_flare.wav'))
		self.sound_list.append(self.solar_flare)

		self.cpu_on = pygame.mixer.Sound(os.path.join(Current_Path, 'cpu_on.wav'))
		self.sound_list.append(self.cpu_on)

		#sounds to be loaded on only certain levels
		self.cannon = None
		self.sound_list.append(self.cannon)

		self.big_laser = None
		self.sound_list.append(self.big_laser)

		self.big_ice_laser = None
		self.sound_list.append(self.big_ice_laser)

		self.trap_click = None
		self.sound_list.append(self.trap_click)

		self.boulder_bounce = None
		self.sound_list.append(self.boulder_bounce)

		self.spike_trap = None
		self.sound_list.append(self.spike_trap)

		self.fire_trap = None
		self.sound_list.append(self.fire_trap)

		self.saw = None
		self.sound_list.append(self.saw)

		self.update_effects_volume()

	def update_music_volume(self):
		self.background_music.set_volume(options.music_volume)

	def update_effects_volume(self):
		for sound in self.sound_list:
			if sound != None:
				sound.set_volume(options.effects_volume)

	def change_song(self, song_name):
		if self.channel != None:
			self.channel.stop()
		self.background_music = pygame.mixer.Sound(os.path.join(Current_Path, song_name))
		self.background_music.set_volume(options.music_volume) #set default to full volume. Changed as needed.
		#sounds.channel = sounds.mixer.background_music.play(loops=-1)

	def start_song(self):
		self.channel = self.background_music.play(loops=-1)


	def stop_song(self):
		if self.channel != None:
			self.channel.stop()

	def load_temp_sound(self, sound_name):
		if sound_name == 'cannon':
			if self.cannon == None:
				self.cannon = pygame.mixer.Sound(os.path.join(Current_Path, 'cannon.wav'))
				self.cannon.set_volume(options.effects_volume)

		elif sound_name == 'big_laser':
			if self.big_laser == None:
				self.big_laser = pygame.mixer.Sound(os.path.join(Current_Path, 'biglaser.wav'))
				self.big_laser.set_volume(options.effects_volume)

		elif sound_name == 'big_ice_laser':
			if self.big_ice_laser == None:
				self.big_ice_laser = pygame.mixer.Sound(os.path.join(Current_Path, 'big_ice_laser.wav'))
				self.big_ice_laser.set_volume(options.effects_volume)

		elif sound_name == 'trap_click':
			if self.trap_click == None:
				self.trap_click = pygame.mixer.Sound(os.path.join(Current_Path, 'trap_click.wav'))

		elif sound_name == 'boulder_bounce':
			if self.boulder_bounce == None:
				self.boulder_bounce = pygame.mixer.Sound(os.path.join(Current_Path, 'boulder_bounce.wav'))
				self.boulder_bounce.set_volume(options.effects_volume)

		elif sound_name == 'spike_trap':
			if self.spike_trap == None:
				self.spike_trap = pygame.mixer.Sound(os.path.join(Current_Path, 'spike_trap.wav'))
				self.spike_trap.set_volume(options.effects_volume)

		elif sound_name == 'saw':
			if self.saw == None:
				self.saw = pygame.mixer.Sound(os.path.join(Current_Path, 'saw.wav'))
				self.saw.set_volume(options.effects_volume)

		elif sound_name == 'fire_trap':
			if self.fire_trap == None:
				self.fire_trap = pygame.mixer.Sound(os.path.join(Current_Path, 'fire_trap.wav'))
				self.fire_trap.set_volume(options.effects_volume)

	def clear_temp_sounds(self):
		self.cannon = None
		self.big_laser = None
		self.big_ice_laser = None
		self.trap_click = None
		self.boulder_bounce = None
		self.fire_trap = None
		self.saw = None



