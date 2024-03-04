

import pygame
import random
import level
import sprites
import options
import os
import sys
import controls
import sounds
import data_manager
import rope_physics
import copy

if getattr(sys, 'frozen', False):
	Current_Path = sys._MEIPASS
else:
	Current_Path = str(os.path.dirname(__file__)) + str('/GameData/')

pygame.font.init()
matrix_font=pygame.font.Font(os.path.join(Current_Path, 'matrix.ttf'), 8)
#matrix_font=pygame.font.Font(os.path.join(Current_Path, 'busymatrix.ttf'), 8)
font_12=pygame.font.Font(os.path.join(Current_Path, 'ThinFont.ttf'), 16)
#font_12.set_bold(True)
font_16=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 16)
font_20=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 20)
font_30=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 30)
font_80=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 80)
font_120=pygame.font.Font(os.path.join(Current_Path, 'GameFont.ttf'), 120)

matrix_letter_list = []
matrix_dark_letter_list = []
matrix_light_letter_list = []
for letter in options.lower_case_list:
	letter_pic = matrix_font.render(letter, 0, options.MATRIX)
	matrix_letter_list.append(letter_pic)

	letter_pic = matrix_font.render(letter, 0, options.MATRIX_DARK)
	matrix_dark_letter_list.append(letter_pic)

	letter_pic = matrix_font.render(letter, 0, options.MATRIX_LIGHT)
	matrix_light_letter_list.append(letter_pic)

BLACK = (0,0,0)
WHITE = (255,255,255)

pause_sprite = None
pause_sprite_online_host = None
pause_sprite_online_guest = None
game_options_sprite = None
versus_options_sprite = None
versus_item_options_sprite = None
main_menu_sprite = None
versus_level_selection_sprite = None
instruction_booklet_sprite = None


def set_default_ninjas():
	sprites.player1.change_color(None, None, color_tuple = options.PURPLE_LIST, change_bandana = False)
	sprites.player1.bandana_color = options.RED_LIST
	sprites.player1.bandana.kill()
	sprites.player1.bandana = rope_physics.Bandana_Knot(sprites.player1, sprites.player1.bandana_color)

	sprites.player2.change_color(None, None, color_tuple = options.BLUE_LIST, change_bandana = False)
	sprites.player2.bandana_color = options.PURPLE_LIST
	sprites.player2.bandana.kill()
	sprites.player2.bandana = rope_physics.Bandana_Knot(sprites.player2, sprites.player2.bandana_color)

	sprites.player3.change_color(None, None, color_tuple = options.GREEN_LIST, change_bandana = False)
	sprites.player3.bandana_color = options.ORANGE_LIST
	sprites.player3.bandana.kill()
	sprites.player3.bandana = rope_physics.Bandana_Knot(sprites.player3, sprites.player3.bandana_color)

	sprites.player4.change_color(None, None, color_tuple = options.RED_LIST, change_bandana = False)
	sprites.player4.bandana_color = options.BLUE_LIST
	sprites.player4.bandana.kill()
	sprites.player4.bandana = rope_physics.Bandana_Knot(sprites.player4, sprites.player4.bandana_color)

def shift_glitch(image, direction):
	glitch_height = 10
	shift_list = []
	i = 0
	while i < 15:
		shift_list.append(random.randrange(3,360 - 3 - (glitch_height * 2),1))
		i+=1

	if direction == 'right':
		mod = -1
	else:
		mod = 1

	for point in shift_list:
		x_shift = random.randrange(-6,-2,1) * mod
		image.blit(image, (x_shift,point), area = (0,point,637,glitch_height))

		#smaller glitches above/below previous glitch
		x_shift = int(x_shift / 2)
		image.blit(image, (x_shift,point), area = (0,point - glitch_height,637,glitch_height))
		image.blit(image, (x_shift,point), area = (0,point + glitch_height,637,glitch_height))
		#blit(source, dest, area=None, special_flags = 0)

def vertical_glitch(image):
	#base_image = image.copy()
	glitch_height = random.choice((50,150,1))

	image.blit(image, (3,3), area = (3,3 + glitch_height,640-6,360 - 6 -glitch_height))

def move_vertical_glitch(image, glitch_height):
	base_image = image.copy()

	image.blit(base_image, (3,3), area = (3,3 + glitch_height,640-6,360 - 6 -glitch_height))
	image.blit(base_image, (3,360 - 6 -glitch_height), area = (3,3,640-6, 3 +  glitch_height))

def stripe_glitch(image):
	#line1_y = random.randrange(30,330,1)
	#line2_y = random.randrange(30,330,1)
	#line3_y = random.randrange(30,330,1)
	#y_change = random.randrange(-2,2,1)

	line1_y = random.choice((150,160,1))
	line2_y = random.choice((30,40,1))
	line3_y = random.choice((200,210,1))
	line4_y = random.choice((300,310,1))
	y_change = -5


	pygame.draw.line(image, options.BLACK, (3 , line1_y) , (640-6 , line1_y + y_change), 30)
	pygame.draw.line(image, options.BLACK, (3 , line2_y) , (640-6 , line2_y + y_change), 10)
	pygame.draw.line(image, options.WHITE, (3 , line3_y) , (640-6 , line3_y + y_change), 5)
	pygame.draw.line(image, options.BLACK, (3 , line4_y) , (640-6 , line4_y + y_change), 10)



def outline_text(text_image, text_color, outline_color):

		
		new_text = pygame.Surface((text_image.get_width() + 2, text_image.get_height() + 2))
		new_text.fill(options.GREEN)
		new_text.set_colorkey(options.GREEN)
		new_text.blit(text_image,(1,1))
		height = new_text.get_height()
		width = new_text.get_width()
		temp_color = text_color

		pixel_checks = ((-1,0),(-1,-1),(-1,1),(0,-1),(0,1),(1,0),(1,-1),(1,1))
		#drop shodow
		#pixel_checks = ((1,0),(1,1))
		new_text.lock()
		array = pygame.PixelArray(new_text)
		x = 0
		y = 0
		while y <= height - 1:
			x = 0
			while x <= width - 1:
				color = new_text.unmap_rgb(array[x,y])
				if color == temp_color: #find out if current pixel is colored.
					#if it is, check pixels around it. If they aren't colored, make them black.
					for pixel_check in pixel_checks:
						temp_x = x + pixel_check[0]
						temp_y = y + pixel_check[1]
						try:
							color = new_text.unmap_rgb(array[temp_x,temp_y])
							if color != temp_color:
								array[temp_x,temp_y] = (outline_color)
						except IndexError:
							pass
						
				x += 1
			y += 1

		array.close()
		new_text.unlock()

		return(new_text)

class Matrix_Bar(pygame.sprite.DirtySprite):
	def __init__(self, matrix_bar_list):
		pygame.sprite.DirtySprite.__init__(self)

		#self.image = pygame.Surface((10,360 + 50))
		self.image = pygame.Surface((10,250))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

		

		self.status = 'idle'

		self.matrix_bar_list = matrix_bar_list
		self.matrix_bar_list.append(self)

		self.x_start_list = []
		i = 0
		while i < 640:
			self.x_start_list.append(i)
			i += self.rect.width

		self.rect.bottom = random.randrange(0 - self.rect.height - 400, -40, 1) - 150
		self.true_y = self.rect.y
		self.get_x_position()

		self.change_y = 2


		self.dirty = 1
		self.visible = 1

		self.digit_list = []

		self.max_position = 0

		i = 0
		position = 0
		while i < self.rect.height:
			digit = Matrix_Bar_Digit(self,0, position)
			self.digit_list.append(digit)
			i += (digit.image.get_height()) + 1
			position += 1

		self.max_position = position

	def update(self):
		self.dirty += 1
		
		self.true_y += self.change_y #* options.DT

		self.rect.y = round(self.true_y)

		for digit in self.digit_list:
			if digit.rect.bottom < self.rect.top:
				digit.rect.y += self.rect.height
				digit.position = self.max_position
				for other_digit in self.digit_list:
					if digit != other_digit:
						other_digit.position -= 1

		#for digit in self.digit_list:
		#	digit.position -= round(self.change_y * options.DT)

		if self.rect.top > 360:
			self.get_x_position()
			self.rect.bottom = 0
			self.true_y = self.rect.y
			for digit in self.digit_list:
				#print(digit.position)
				#digit.position = digit.start_position
				digit.rect.top = self.rect.top + (digit.position * (digit.rect.height + 1))

	def reset(self):
		self.rect.bottom = random.randrange(0 - self.rect.height - 300, 60, 1) - 150
		self.true_y = self.rect.y
		self.get_x_position()
		for digit in self.digit_list:
			#print(digit.position)
			#digit.position = digit.start_position
			digit.rect.top = self.rect.top + (digit.position * (digit.rect.height + 1))

	def get_x_position(self):
		temp_list = self.x_start_list.copy()
		for bar in self.matrix_bar_list:
			temp_list.remove(bar.rect.x)
		self.rect.x = random.choice(temp_list)


class Matrix_Bar_Digit(pygame.sprite.DirtySprite):
	def __init__(self, matrix_bar, x, position):
		pygame.sprite.DirtySprite.__init__(self)

		self.matrix_bar = matrix_bar
		self.image = random.choice(matrix_letter_list)
		self.rect = self.image.get_rect()

		self.position = position

		self.rect.x = x
		self.rect.top = self.matrix_bar.rect.top + (self.position * (self.rect.height + 1))

		#self.true_y = round(self.rect.y)

		self.visible = 1
		self.dirty = 1
		self.image_number = 0

	def update(self, screen, x_start):
		#self.true_y -= self.matrix_bar.change_y * options.DT
		#self.position -= 1
		#if self.position < 0:
		#	self.position = self.matrix_bar.max_position
		#	self.image_number = random.randrange(0,len(matrix_letter_list) - 1,1)

		#height = self.rect.height
		#self.rect.y = self.matrix_bar.rect.y + (self.position / self.matrix_bar.change_y * height)

		'''
		if self.rect.y < 0:
			temp_bottom = 0
			for digit in self.matrix_bar.digit_list:
				if digit.rect.bottom > temp_bottom:
					temp_bottom = digit.rect.bottom - 3
			self.rect.top = temp_bottom
			self.true_y = self.rect.y
			self.image_number = random.randrange(0,len(matrix_letter_list) - 1,1)
		'''

		if screen != None:
			self.blit(screen,x_start)

	def blit(self,screen,x_start):
		if self.position > self.matrix_bar.max_position - 3:
			self.image = matrix_light_letter_list[self.image_number]
		elif self.position < 3:
			self.image = matrix_dark_letter_list[self.image_number]
		else:
			i = random.randrange(0,60,1)
			if i < 5:
				self.image_number = random.randrange(0,len(matrix_letter_list) - 1,1)
			self.image = matrix_letter_list[self.image_number]

		if x_start == None:
			x_mod = 0
		else:
			x_mod = x_start
		#blit to chosen screen based on current 'bar position.'
		if self.rect.bottom > 0 and self.rect.top < 360:	
			screen.blit(self.image, (self.matrix_bar.rect.centerx - (self.image.get_width() / 2) - x_mod, self.rect.y)) # + self.matrix_bar.rect.y))









class Intro_Handler():
	def __init__(self):

		'''
		self.intro_text = [
							' Hello.',
							'...',
							'...',
							' You Have Been Chosen.',
							' We Must Prepare.',
							' The Mallow Consumes.',
							' The Mallow is Coming.',
							' A Suit Has Been Created.',
							' A Living Weapon.',
							' A Weapon of Hope.',
							' Only One May Be Chosen.',
							' One Who Proves Worthy.',
							' I Exist Only To Choose.',
							' Please Hold Still...',
							' Biometric Scan Complete.',
							' Welcome to Me.',
							' Welcome to...'
							]
		
		self.intro_text = [
							' Hello.',
							' Your World is in Danger.',
							' The Mallow Consumes All.',
							' The Mallow is Coming.',
							' You Have Been Identified.',
							' You Have Potential.',
							' Your World Needs You.',
							' Please Hold Still.',
							' ...',
							' ...',
							' Biometric Scan Complete.',
							' VR Simulation Ready.',
							' Your Training Begins.',
							' Welcome to...'
							]
		'''
		self.intro_text = [
							' Earth is in Danger.',
							' We Must Prepare.',
							' Please Hold Still.',
							' ...',
							' ...',
							' Biometric Data Uploaded.',
							' Combat Simulation Ready.',
							' Welcome to...'
							]

		self.line_number = 0 #holds current text
		self.digit_number = 0 #holds current place in line string
		self.digit_timer = 0 #counts how long before next digit prints.
		self.line_delay_timer = 20 #counts downt after line prints. Only proceeds to next line once at 0.

		self.status = 'turn_on'

		self.BLACK = (0,0,0)
		self.text_bar = self.get_text_bar()

		self.static_image1 = pygame.Surface((640,360))
		self.static_image1.fill(options.LIGHT_PURPLE)
		x = 0
		y = 0
		while x < 640 - 1:
			while y < 360 - 1:
				color = random.choice((options.DARK_PURPLE, options.LIGHT_PURPLE))
				i = random.choice((True,False))
				if i is True:
					pygame.draw.rect(self.static_image1, options.DARK_PURPLE, (x,y,1,1), 0)
				y += 1
			y = 0
			x += 1

		self.static_image2 = pygame.Surface((640,360))
		
		self.static_image2.fill(options.LIGHT_PURPLE)
		x = 0
		y = 0
		while x < 640 - 1:
			while y < 360 - 1:
				color = random.choice((options.DARK_PURPLE, options.LIGHT_PURPLE))
				i = random.choice((True,False))
				if i is True:
					pygame.draw.rect(self.static_image2, options.DARK_PURPLE, (x,y,1,1), 0)
				y += 1
			y = 0
			x += 1



		self.transition_screen = False
		self.transition_number = 4

		self.intro_delay = 0 #intro only runs if it is 0. Otherwise counts down.

		self.turn_on_width = 0
		self.turn_on_height = 2
		self.turn_on_timer = 0
		self.turn_on_delay = 0
		self.height_timer = 0

		self.glitch_timer = 0

		self.matrix_bar_list = []
		i = 0
		#while i < 42:
		while i < 20:
			matrix_bar = Matrix_Bar(self.matrix_bar_list)
			#self.matrix_bar_list.append(matrix_bar)
			i += 1


	def update(self):
		#check for button presses


		controls.input_handler.get_gamepads()
		#if self.status != 'turn_on':
		#	if sprites.player1.menu_select_press is True:
		#		self.status = 'done'

				#choose input preference
				#if len(controls.input_handler.gamepads) == 0:
				#	options.control_preferences['player1'] = 'keyboard'
				

				#options.game_state = 'main_menu'
				#sprites.transition_screen.fade('explode_fade', True, options.GREEN)
				#sounds.mixer.shatter.play()


		if self.status == 'scan' and self.intro_delay == 0: #otherwise handled by scanner
			pass
		else:
			sprites.screen = Build_CPU_Screen(sprites.screen)
			
			#sprites.screen.fill(options.BLACK)
			
			for bar in self.matrix_bar_list:
				bar.update()
				for digit in bar.digit_list:
					digit.update(sprites.screen, None) #blits to sprites.screen from within update, based on bar position.
			#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

		if self.intro_delay > 0:
			self.intro_delay -= 1

		if self.intro_delay <= 0:

			pygame.draw.rect(sprites.screen, options.DARK_PURPLE, (5 + 320 + (self.text_bar.get_width() / 2), 180 - (self.text_bar.get_height() / 2),20, (self.text_bar.get_height())), 0)

			if self.status == 'turn_on':
				if self.turn_on_height <= 4:
					sprites.screen.fill(options.BLACK)
				self.turn_on_delay += 1
				if self.turn_on_delay == 60:
					sounds.mixer.cpu_on.play()
				if self.turn_on_delay > 60:
					self.turn_on_timer += 90

					if self.turn_on_timer > 320:
						self.turn_on_height = 4

					if self.turn_on_timer >= 30:
						if self.turn_on_timer < 640:
							self.turn_on_width = self.turn_on_timer
						else:
							self.turn_on_width = 640
							self.height_timer += 90
							if self.height_timer < 360:
								self.turn_on_height = self.height_timer
							else:
								self.turn_on_height = 360
								self.status = 'text'
						if self.turn_on_height <= 4:
							pygame.draw.rect(sprites.screen, options.DARK_PURPLE,(320 - int(self.turn_on_width / 2), 180 - int(self.turn_on_height / 2), self.turn_on_width,self.turn_on_height))
						else:
							pygame.draw.rect(sprites.screen, options.BLACK,(0,0, 640,180 - int(self.turn_on_height / 2)))
							pygame.draw.rect(sprites.screen, options.BLACK,(0,180 + int(self.turn_on_height / 2), 640,180 - int(self.turn_on_height / 2)))
							pygame.draw.rect(sprites.screen, options.DARK_PURPLE,(320 - int(self.turn_on_width / 2), 180 - int(self.turn_on_height / 2), self.turn_on_width,self.turn_on_height),4)
				#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

			elif self.status == 'text':
				if self.line_delay_timer > 0:
					self.line_delay_timer -= 1
					#still blit previous text.
				else:
					self.text_bar = self.get_text_bar()
					self.digit_timer += 1 # * options.DT

					if self.digit_timer > 4:
						self.digit_timer = 0
						self.digit_number += 1
						if self.digit_number >= len(self.intro_text[self.line_number]):
							self.line_delay_timer = 60
							self.digit_number = 0
							self.line_number += 1
							if self.line_number >= len(self.intro_text):
								self.line_number = 0
								self.status = 'done'
							if self.line_number == self.transition_number and self.transition_screen is False:
								self.status = 'scan'
								self.line_delay_timer = 0
								self.intro_delay = 15
						else:
							sounds.mixer.type.play()

				#new_text =  outline_text(self.text_bar, options.LIGHT_PURPLE, options.DARK_PURPLE)
				#sprites.screen.blit(new_text, (320 - (new_text.get_width() / 2), 180 - (new_text.get_height() / 2)))
				sprites.screen.blit(self.text_bar, (320 - (self.text_bar.get_width() / 2), 180 - (self.text_bar.get_height() / 2)))

				self.glitch_timer += 1 #* options.DT
				#print(self.glitch_timer)
				if (self.glitch_timer > 40 and self.glitch_timer < 45) or (self.glitch_timer > 60 and self.glitch_timer < 65):
					shift_glitch(sprites.screen, 'left')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

				if self.glitch_timer > 65 and self.glitch_timer < 70:
					vertical_glitch(sprites.screen)

				if self.glitch_timer > 75 and self.glitch_timer < 80:
					shift_glitch(sprites.screen, 'left')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

				if self.glitch_timer > 80 and self.glitch_timer < 90:
					i = ((self.glitch_timer - 80) / 10) * 360
					move_vertical_glitch(sprites.screen, i)
				if self.glitch_timer > 90 and self.glitch_timer < 100:
					i = ((self.glitch_timer - 90) / 10) * 360
					move_vertical_glitch(sprites.screen, i)
				

				if self.glitch_timer > 100 and self.glitch_timer < 105:
					shift_glitch(sprites.screen, 'left')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

				if self.glitch_timer > 105 and self.glitch_timer < 110:
					if self.glitch_timer % 2 == 0: #even number
						sprites.screen.blit(self.static_image1,(0,0))
					else:
						sprites.screen.blit(self.static_image2,(0,0))
					sprites.screen =  Build_Menu_Perimeter(sprites.screen)
				if self.glitch_timer > 110 and self.glitch_timer < 115:
					shift_glitch(sprites.screen, 'right')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

				if self.glitch_timer > 190 and self.glitch_timer < 195:
					shift_glitch(sprites.screen, 'right')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

				if self.glitch_timer > 200 and self.glitch_timer < 205:
					stripe_glitch(sprites.screen)

				if self.glitch_timer > 315 and self.glitch_timer < 320:
					shift_glitch(sprites.screen, 'right')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)
				
				if self.glitch_timer > 320 and self.glitch_timer < 325:
					vertical_glitch(sprites.screen)


				if self.glitch_timer > 495 and self.glitch_timer < 500:
					stripe_glitch(sprites.screen)
				if self.glitch_timer > 500 and self.glitch_timer < 505:
					vertical_glitch(sprites.screen)
				if self.glitch_timer > 505 and self.glitch_timer < 510:
					stripe_glitch(sprites.screen)

				if self.glitch_timer > 675 and self.glitch_timer < 680:
					shift_glitch(sprites.screen, 'left')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)
				if self.glitch_timer > 680 and self.glitch_timer < 685:
					vertical_glitch(sprites.screen)

				if self.glitch_timer > 685 and self.glitch_timer < 690:
					if self.glitch_timer % 2 == 0: #even number
						sprites.screen.blit(self.static_image1,(0,0))
					else:
						sprites.screen.blit(self.static_image2,(0,0))
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)
				if self.glitch_timer > 690 and self.glitch_timer < 695:
					shift_glitch(sprites.screen, 'right')
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)

				if self.glitch_timer > 695 and self.glitch_timer < 700:
					vertical_glitch(sprites.screen)


			elif self.status == 'done':
				sprites.screen.blit(self.text_bar, (320 - (self.text_bar.get_width() / 2), 180 - (self.text_bar.get_height() / 2)))
				if self.line_delay_timer > 0:
					self.line_delay_timer -= 1 # * options.DT
				else:
					options.game_state = 'main_menu'
					sprites.transition_screen.fade('explode_fade', True, options.GREEN)
					sounds.mixer.shatter.play()
					sounds.mixer.scan.stop()

			elif self.status == 'scan':
				self.line_delay_timer -= 1  #* options.DT
				if self.line_delay_timer <= 0:
					if self.transition_screen is False:
						self.transition_screen = not self.transition_screen
						#sprites.transition_screen.fade()
						#sprites.transition_screen.intro_activate()
						sprites.transition_screen.activate()
						sprites.transition_screen.intro_switch = True
					
					sprites.transition_screen.update()
					sprites.transition_screen.visible = 1 #hack.
					sprites.screen_objects.draw(sprites.screen)
					sprites.transition_screen.visible = 0 #hack

					if sprites.transition_screen.status == 'idle':
						self.status = 'text'
						self.intro_delay = 15
						self.text_bar = font_30.render('', 0, options.LIGHT_PURPLE)
				else:
					sprites.screen = Build_CPU_Screen(sprites.screen)
					for bar in self.matrix_bar_list:
						bar.update()
						#bar.image.fill(options.GREEN)
						if bar.rect.colliderect((320 - (self.text_bar.get_width() / 2), 180 - (self.text_bar.get_height() / 2), self.text_bar.get_width(),self.text_bar.get_height())):
							for digit in bar.digit_list:
								digit.update(sprites.screen, None) #blits to sprites.screen from within update, based on bar position.
								#bar.image.blit(digit.image,(0,digit.rect.y))
						#sprites.screen.blit(bar.image, (bar.rect.x, bar.rect.y))
					#sprites.screen =  Build_Menu_Perimeter(sprites.screen)
					sprites.screen.blit(self.text_bar, (320 - (self.text_bar.get_width() / 2), 180 - (self.text_bar.get_height() / 2)))


		'''
		#Just for raining code collection.
		if (self.intro_delay >= (60 * 30) - 10 and self.intro_delay <= (60 * 30)) or (self.intro_delay >= (60 * 10) - 10 and self.intro_delay <= (60 * 10)):
			shift_glitch(sprites.screen, 'right')
		if (self.intro_delay > (60 * 30) - 20 and self.intro_delay < (60 * 30) - 10) or (self.intro_delay > (60 * 10) - 20 and self.intro_delay < (60 * 10) - 10):
			print('made it')
			if self.glitch_timer % 2 == 0: #even number
				sprites.screen.blit(self.static_image1,(0,0))
			else:
				sprites.screen.blit(self.static_image2,(0,0))
		'''

	def get_text_bar(self):
		line = self.intro_text[self.line_number]
		text = ''
		i = 0
		while i <= self.digit_number:

			text = text + line[i]
			i += 1

		text_item = font_30.render(text, 0, options.LIGHT_PURPLE)
		#new_text =  outline_text(text_item, options.LIGHT_PURPLE, options.DARK_PURPLE)


		return(text_item)


intro_handler = Intro_Handler()


class Versus_Awards_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.text_screen = None #created to draw text on. Cleared each frame.

		self.another_game = True
		self.win_color = None
		self.done = False

		self.stats_dict = {} #ninjas are added in 'load menu'. Used to flip stats from stats to awards.

		self.P1_stats_screen = None
		self.P1_awards_screen = None
		self.P2_stats_screen = None
		self.P2_awards_screen = None
		self.P3_stats_screen = None
		self.P3_awards_screen = None
		self.P4_stats_screen = None
		self.P4_awards_screen = None
		self.done_screen = None

		self.MenuTitle = font_30.render("Simulation Analysis", 0,(WHITE))

		self.unlock_switch = False

		#self.fade_done = False
	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()
			self.done = False
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
		
		#check for gamepads regularly.
		controls.input_handler.get_gamepads()

		self.update_stats_screen()

		#just check on first pass
		if self.unlock_switch is False and sprites.transition_screen.status == 'idle':
			self.unlock_switch = True
			Ancalabro_loss = False
			for ninja in sprites.player_list:
				if ninja.profile == 'Ancalabro':
					if self.check_win(ninja) is False:
						Ancalabro_loss = True

			local_win = False
			for ninja in sprites.player_list:
					if self.check_win(ninja) is True:
						local_win = True
			
			#defeated Ancalabro! Give Prize
			if Ancalabro_loss is True and local_win is True:
				if options.PURPLE_LIST not in options.color_choices:
					options.color_choices.append(options.PURPLE_LIST)
					self.ancalabro_unlock = sprites.Unlock_Sprite('Purple', unlock_type = 'color')


		#draw things here
		i = 0
		while i < 60:
			sprites.menu_sprite_list.update()
			level.Collision_Check() #Handles Non-Tile collision checks
			sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
			sprites.tile_list.update()
			sprites.level_objects.update()
			sprites.item_effects.update()
			sprites.background_objects.update()
			sprites.visual_effects.update()
			sprites.screen_objects.update()
			i += options.current_fps

		
		sprites.active_sprite_list.draw(sprites.screen)

		sprites.screen.blit(self.MenuTitle, ((sprites.screen.get_width() / 2) - (self.MenuTitle.get_width() / 2), 5))

		
		for ninja in sprites.player_list:
			if ninja.dummy is True:
				if ninja == sprites.player2:
					self.stats_dict['Player2'] = self.stats_dict['Player1']
				if ninja == sprites.player3:
					self.stats_dict['Player3'] = self.stats_dict['Player1']
				if ninja == sprites.player4:
					self.stats_dict['Player4'] = self.stats_dict['Player1']

		if sprites.transition_screen.status == 'idle':
			if (sprites.player1.menu_left_press is True or sprites.player1.menu_right_press is True) and self.stats_dict['Player1'] != 'done':
				sounds.mixer.menu_move.play()
				if self.stats_dict['Player1'] == 'stats':
					self.stats_dict['Player1'] = 'awards'
				else:
					self.stats_dict['Player1'] = 'stats'

			if (sprites.player2.menu_left_press is True or sprites.player2.menu_right_press is True) and self.stats_dict['Player2'] != 'done':
				sounds.mixer.menu_move.play()
				if self.stats_dict['Player2'] == 'stats':
					self.stats_dict['Player2'] = 'awards'
				else:
					self.stats_dict['Player2'] = 'stats'

			if (sprites.player3.menu_left_press is True or sprites.player3.menu_right_press is True) and self.stats_dict['Player3'] != 'done':
				sounds.mixer.menu_move.play()
				if self.stats_dict['Player3'] == 'stats':
					self.stats_dict['Player3'] = 'awards'
				else:
					self.stats_dict['Player3'] = 'stats'

			if (sprites.player4.menu_left_press is True or sprites.player4.menu_right_press is True) and self.stats_dict['Player4'] != 'done':
				sounds.mixer.menu_move.play()
				if self.stats_dict['Player4'] == 'stats':
					self.stats_dict['Player4'] = 'awards'
				else:
					self.stats_dict['Player4'] = 'stats'

			if sprites.player1.menu_select_press is True:
				if self.stats_dict['Player1'] != 'done':
					sounds.mixer.menu_select.play()
				self.stats_dict['Player1'] = 'done'

			if sprites.player2.menu_select_press is True:
				if self.stats_dict['Player2'] != 'done':
					sounds.mixer.menu_select.play()
				self.stats_dict['Player2'] = 'done'

			if sprites.player3.menu_select_press is True:
				if self.stats_dict['Player3'] != 'done':
					sounds.mixer.menu_select.play()
				self.stats_dict['Player3'] = 'done'

			if sprites.player4.menu_select_press is True:
				if self.stats_dict['Player4'] != 'done':
					sounds.mixer.menu_select.play()
				self.stats_dict['Player4'] = 'done'

			if sprites.player1.menu_back_press is True:
				if self.stats_dict['Player1'] == 'done':
					self.stats_dict['Player1'] = 'stats'

			if sprites.player2.menu_back_press is True:
				if self.stats_dict['Player2'] == 'done':
					self.stats_dict['Player2'] = 'stats'

			if sprites.player3.menu_back_press is True:
				if self.stats_dict['Player3'] == 'done':
					self.stats_dict['Player3'] = 'stats'

			if sprites.player4.menu_back_press is True:
				if self.stats_dict['Player4'] == 'done':
					self.stats_dict['Player4'] = 'stats'
				
		
		if self.done is True:
				for ninja in sprites.player_list:
					ninja.collect_win_loss_stats(self.win_color)

				#level.level_builder.level_reset(light_reset = True)
				sprites.reset_sprites()
				#level.level_builder.level_reset()

				sounds.mixer.stop_song()
				sounds.mixer.change_song('music_menu.wav')
				sounds.mixer.start_song()
				options.game_state = 'versus_level_selection'
				
				self.menu_created = False


		if self.done is False:
			done = True
			for ninja in sprites.player_list:
				if self.stats_dict[ninja.name] != 'done':
					done = False
					break			
			if done is True:
				self.done = True #just lettin it loop one more time.
				for ninja in sprites.player_list:
					ninja.awards_screen_sprite.reset()
					ninja.awards_screen_sprite.background.reset()





	def check_win(self, ninja):
		win = False
		if options.versus_mode == 'Points':
			if ninja.current_VP >= options.versus_VP_required:
				win = True
		elif options.versus_mode == 'Classic':
			if ninja.current_wins >= options.versus_wins_required:
				win = True
		elif options.versus_mode == 'Stock':
			if ninja.lives >= 0:
				win = True

		return(win)

	def update_stats_screen(self):
		#self.text_screen.image.fill(options.GREEN) #fill text screen with green to be re-blitted
		#self.text_screen.dirty = 1

		if len(sprites.player_list) == 2:
			x = (sprites.screen.get_width() / 3, sprites.screen.get_width() / 3 * 2)
		elif len(sprites.player_list) == 3:
			x = (sprites.screen.get_width() / 5, sprites.screen.get_width() / 2, sprites.screen.get_width() / 5 * 4)
		elif len(sprites.player_list) == 4:
			#x = ((sprites.screen.get_width() / 5) - 40, (sprites.screen.get_width() / 5 * 2) - 15, (sprites.screen.get_width() / 5 * 3) + 15, (sprites.screen.get_width() / 5 * 4) + 40)
			x = (89,243,397,551)
		#create temp_list to get ninjas in order. (name is always player1 through 4)
		temp_list = []
		sprites.player1.awards_screen_sprite.background.image = Build_CPU_Screen(sprites.player1.awards_screen_sprite.background.image)
		for bar in  intro_handler.matrix_bar_list:
				if bar.rect.colliderect(sprites.player1.awards_screen_sprite.rect):
					for digit in bar.digit_list:
						digit.blit(sprites.player1.awards_screen_sprite.background.image, sprites.player1.awards_screen_sprite.rect.x) #blits to sprites.screen from within update, based on bar position.
		for ninja in sprites.player_list:
			temp_list.append(ninja)
			if ninja != sprites.player1:
				ninja.awards_screen_sprite.background.image = sprites.player1.awards_screen_sprite.background.image.copy()

		temp_list.sort(key=lambda ninja: ninja.player_number)

		i = 0
		for ninja in temp_list:
			ninja.awards_screen_sprite.rect.x = x[i] - 65
			ninja.awards_screen_sprite.rect.y = 50

			ninja.awards_screen_sprite.background.rect.x = x[i] - 65
			ninja.awards_screen_sprite.background.rect.y = 50
			
			
			if self.stats_dict[ninja.name] == 'stats':
				#ninja.awards_screen_sprite.image.blit(ninja.stats_screen, (0,0))
				ninja.awards_screen_sprite.image = ninja.stats_screen
			elif self.stats_dict[ninja.name] == 'awards':
				#ninja.awards_screen_sprite.image.blit(ninja.awards_screen, (0,0))
				ninja.awards_screen_sprite.image = ninja.awards_screen

			elif self.stats_dict[ninja.name] == 'done':
				#ninja.awards_screen_sprite.image.blit(self.done_screen, (0,0))
				ninja.awards_screen_sprite.image = self.done_screen

			ninja.awards_screen_sprite.dirty = 1


			i += 1

	def get_awards(self):
		shield_award = []
		for ninja in sprites.player_list:
			i = ninja.stats_frames_with_shield_active / 30 / ninja.duels_participated
			if i >= 0.75: #3/4 shields used per Duel
				if shield_award == [] or i > shield_award[1]:
					shield_award = [ninja, i]
		if shield_award != []:
			shield_award[0].stats_awards_list.append(('Most Insulated', (516,0,124,49)))

		shield_rebound_award = []
		for ninja in sprites.player_list:
			i = ninja.stats_shield_weapons_rebounded
			if i >= 1: #1 rebounds per level
				if shield_rebound_award == [] or i > shield_rebound_award[1]:
					shield_rebound_award = [ninja, i]
		if shield_rebound_award != []:
			shield_rebound_award[0].stats_awards_list.append(("I'm Rubber Award", (516,50,124,49)))

		shoes_award = []
		for ninja in sprites.player_list:
			i = ninja.stats_shoes_pixels_travelled / ninja.duels_participated
			if i >= 1000: 
				if shoes_award == [] or i > shoes_award[1]:
					shoes_award = [ninja, i]
		if shoes_award != []:
			shoes_award[0].stats_awards_list.append(("Ultra-Marathoner", (516,100,124,49)))


		laser_accuracy = []
		for ninja in sprites.player_list:
			if ninja.stats_laser_fired != 0:
				i = ninja.stats_laser_kills / ninja.stats_laser_fired * 100
				if i >= 80: 
					if ninja.stats_laser_fired >= 3:
						if laser_accuracy == [] or i > laser_accuracy[1]:
							laser_accuracy = [ninja, i]
		if laser_accuracy != []:
			laser_accuracy[0].stats_awards_list.append(("Marksmanship", (516,150,124,49)))

		vertical_laser = []
		for ninja in sprites.player_list:
			if ninja.stats_laser_fired != 0:
				i = ninja.stats_laser_vertical_kills
				if i >= 1: 
					if vertical_laser == [] or i > vertical_laser[1]:
						vertical_laser = [ninja, i]
		if vertical_laser != []:
			vertical_laser[0].stats_awards_list.append(("Trick Shot Award", (516,200,124,49)))

		suicide_list = [] #FIDS 
		for ninja in sprites.player_list:
				i = ninja.stats_FIDs_suicide
				if i >= 1: 
					if suicide_list == [] or i > suicide_list[1]:
						suicide_list = [ninja, i]
		if suicide_list != []:
			suicide_list[0].stats_awards_list.append(("Bold Strategy Award", (516,250,124,49)))

		suicide_list = [] #Skulls
		for ninja in sprites.player_list:
				i = ninja.stats_skull_acquired
				if i >= 1: 
					if suicide_list == [] or i > suicide_list[1]:
						suicide_list = [ninja, i]
		if suicide_list != []:
			suicide_list[0].stats_awards_list.append(("Most Gullible", (516,300,124,49)))

		suicide_mine_list = [] #mine_suicide
		for ninja in sprites.player_list:
				i = ninja.stats_mine_suicides
				if i >= 1: 
					if suicide_mine_list == [] or i > suicide_mine_list[1]:
						suicide_mine_list = [ninja, i]
		if suicide_mine_list != []:
			suicide_mine_list[0].stats_awards_list.append(("Poor Memory Award", (516,350,124,49)))

		suicide_laser_list = [] #laser_suicide
		for ninja in sprites.player_list:
				i = ninja.stats_laser_suicides
				if i >= 1: 
					if suicide_laser_list == [] or i > suicide_laser_list[1]:
						suicide_laser_list = [ninja, i]
		if suicide_laser_list != []:
			suicide_laser_list[0].stats_awards_list.append(("Nice Shot? Award", (391,0,124,49)))

		suicide_bomb_list = [] #bomb_suicide
		for ninja in sprites.player_list:
				i = ninja.stats_bomb_suicides
				if i >= 1: 
					if suicide_bomb_list == [] or i > suicide_bomb_list[1]:
						suicide_bomb_list = [ninja, i]
		if suicide_bomb_list != []:
			suicide_bomb_list[0].stats_awards_list.append(("Mr. Butterfingers", (391,50,124,49)))

		suicide_rocket_list = [] #rocket_suicide
		for ninja in sprites.player_list:
				i = ninja.stats_rocket_suicides
				if i >= 1: 
					if suicide_rocket_list == [] or i > suicide_rocket_list[1]:
						suicide_rocket_list = [ninja, i]
		if suicide_rocket_list != []:
			suicide_rocket_list[0].stats_awards_list.append(("Learner's Permit", (391,100,124,49)))

		suicide_homing_bomb_list = [] #homing bomb_suicide
		for ninja in sprites.player_list:
				i = ninja.stats_homing_bomb_suicides
				if i >= 1: 
					if suicide_homing_bomb_list == [] or i > suicide_homing_bomb_list[1]:
						suicide_homing_bomb_list = [ninja, i]
		if suicide_homing_bomb_list != []:
			suicide_homing_bomb_list[0].stats_awards_list.append(("Solo Hot Potato", (391,150,124,49)))

		triple_kill_list = [] #triple kill (all weapons)
		for ninja in sprites.player_list:
				i = ninja.stats_laser_triple_kills + ninja.stats_bomb_triple_kills + ninja.stats_mine_triple_kills + ninja.stats_rocket_triple_kills + ninja.stats_volt_triple_kills
				if i >= 1: 
					if triple_kill_list == [] or i > triple_kill_list[1]:
						triple_kill_list = [ninja, i]
		if triple_kill_list != []:
			triple_kill_list[0].stats_awards_list.append(("Triple Kill!", (391,200,124,49)))

		double_kill_list = [] #double kill (all weapons)
		for ninja in sprites.player_list:
				i = ninja.stats_laser_double_kills + ninja.stats_bomb_double_kills + ninja.stats_mine_double_kills + ninja.stats_rocket_double_kills + ninja.stats_volt_double_kills
				if i >= 1: 
					if 'Triple Kill!' not in ninja.stats_awards_list:
						if double_kill_list == [] or i > double_kill_list[1]:
							double_kill_list = [ninja, i]
		if double_kill_list != []:
			double_kill_list[0].stats_awards_list.append(("Double Kill!", (391,250,124,49)))

		poor_laser_accuracy_list = [] #Poor accuracy Laser
		for ninja in sprites.player_list:
			if ninja.stats_laser_fired > 3:
				i = ninja.stats_laser_kills / ninja.stats_laser_fired
				if i < 0.1:
						if poor_laser_accuracy_list == [] or i < poor_laser_accuracy_list[1]:
							poor_laser_accuracy_list = [ninja, i]
		if poor_laser_accuracy_list != []:
			poor_laser_accuracy_list[0].stats_awards_list.append(("Barn's Broad Side Award", (391,300,124,49)))

		laser_fired_list = [] #Laser Shots Fired
		for ninja in sprites.player_list:
				i = ninja.stats_laser_fired
				if i > 9 and i / ninja.duels_participated >= 2:
						if laser_fired_list == [] or i > laser_fired_list[1]:
							laser_fired_list = [ninja, i]
		if laser_fired_list != []:
			laser_fired_list[0].stats_awards_list.append(("Itchy Trigger Finger", (391,350,124,49)))

		wings_used_list = [] #wings_used + gravity_used
		for ninja in sprites.player_list:
				i = ninja.stats_wing_double_jumps + ninja.stats_gravity_used
				if i > 6:
						if wings_used_list == [] or i > wings_used_list[1]:
							wings_used_list = [ninja, i]
		if wings_used_list != []:
			wings_used_list[0].stats_awards_list.append(("Physics is Optional", (265,0,124,49)))

		bomb_and_mine_list = [] #Bomb/ Mine efficiency
		for ninja in sprites.player_list:
			if ninja.stats_bomb_kills + ninja.stats_mine_kills > 0:
				if (ninja.stats_bomb_thrown + ninja.stats_mine_thrown) == 0:
					i = 0
				else:
					i = (ninja.stats_bomb_kills + ninja.stats_mine_kills) / (ninja.stats_bomb_thrown + ninja.stats_mine_thrown)
				if ninja.stats_bomb_kills + ninja.stats_mine_kills >= 3 and i >= 0.5:
						if bomb_and_mine_list == [] or i > bomb_and_mine_list[1]:
							bomb_and_mine_list = [ninja, i]
		if bomb_and_mine_list != []:
			bomb_and_mine_list[0].stats_awards_list.append(("Demolition Tactician", (265,50,124,49)))

		volt_kill_list = [] #Volt kills
		for ninja in sprites.player_list:
				i = ninja.stats_volt_kills
				if i >= 3 and ninja.stats_volt_kills / ninja.duels_participated >= 0.5:
						if volt_kill_list  == [] or i > volt_kill_list[1]:
							volt_kill_list  = [ninja, i]
		if volt_kill_list  != []:
			volt_kill_list[0].stats_awards_list.append(("Lord of Olympus", (265,100,124,49)))

		award_list = [] #Rocket distance travelled
		for ninja in sprites.player_list:
				i = ninja.stats_rocket_pixels_travelled
				if i >= 1500:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Epic Fuel Budget", (265,150,124,49)))


		award_list = [] #Portal gun FIDS
		for ninja in sprites.player_list:
				i = ninja.stats_portal_gun_FIDs_inflicted
				if i >= 3:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("FID Wizard", (265,200,124,49)))

		award_list = [] #Portal distance_travelled
		for ninja in sprites.player_list:
				i = ninja.stats_portal_gun_distance_teleported
				if i >= 1500:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Master of Time/Space", (265,250,124,49)))

		award_list = [] #Portal most uses (self and items)
		for ninja in sprites.player_list:
				i = ninja.stats_portal_gun_times_teleported + ninja.stats_portal_gun_items_teleported
				if i >= 10:
					if i / ninja.duels_participated >= 2:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Tactical Wizard", (265,300,124,49)))


		award_list = [] #quadruple cube
		for ninja in sprites.player_list:
				i = ninja.stats_ice_bomb_quadruple_cubes
				if i >= 1:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Quadruple Cube!", (265,350,124,49)))

		award_list = [] #most ice cubes made
		for ninja in sprites.player_list:
				i = ninja.stats_ice_bomb_cubes_made
				if i >= 3:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Mr. Freeze Award", (140,0,124,49)))

		award_list = [] #most times frozen
		for ninja in sprites.player_list:
				i = ninja.stats_ice_bomb_self_cubes
				if i >= 3:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Cryogenic", (140,50,124,49)))

		award_list = [] #most frozen FIDs inflicted
		for ninja in sprites.player_list:
				i = ninja.stats_ice_bomb_cube_FIDs
				if i >= 1:
						#if i / ninja.duels_participated >= 0.5:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("FID On the Rocks", (140,100,124,49)))


		award_list = [] #invisible FIS inflicted
		for ninja in sprites.player_list:
				i = ninja.stats_invisible_FIDs_inflicted
				if i >= 1:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Stealth Assassin", (140,150,124,49)))


		award_list = [] #frame invisible
		for ninja in sprites.player_list:
				i = ninja.stats_frames_invisible
				if i >= 900:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Fashionable", (140,200,124,49)))

		award_list = [] #homing bombs evaded / eyes tricked.
		for ninja in sprites.player_list:
				i = ninja.stats_invisible_homing_bomb_evaded
				if i >= 1:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Now you see me...", (140,250,124,49)))


		award_list = [] #most cowardly
		for ninja in sprites.player_list:
				i = ninja.stats_frames_idle + ninja.stats_frames_ducking
				if i >= 900: #30 seconds
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Cowardly", (140,300,124,49)))


		award_list = [] #most homing bombs activated
		for ninja in sprites.player_list:
				i = ninja.stats_homing_bomb_activated
				if i >= 3:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Daring", (140,350,124,49)))


		award_list = [] #most wall_jumps + rolls
		for ninja in sprites.player_list:
				i = ninja.stats_wall_jumps_performed + ninja.stats_rolls_performed
				if i >= 20:
					if i / ninja.duels_participated >= 5:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Acrobatic", (641,0,124,49)))

		'''
		award_list = [] #most frantic
		for ninja in sprites.player_list:
				i = ninja.stats_frames_idle / ninja.duels_participated
				print(i)
				if i >= 20:
					if i / ninja.duels_participated >= 5:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append("Most Frantic")
		'''

		award_list = [] #most time_inverted
		for ninja in sprites.player_list:
				i = ninja.stats_frames_gravity_inverted
				if i >= 1500:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Topsy-Turvy Award", (641,50,124,49)))

		award_list = [] #most deadly (most combined FIDs + Kills)
		for ninja in sprites.player_list:
				i = (ninja.stats_FIDs_inflicted + ninja.stats_item_kills) / (ninja.duels_participated * (len(sprites.player_list) - 1))
				if (ninja.stats_FIDs_inflicted + ninja.stats_item_kills) >= 3:
					if i >= 0.33: #gets at least 1/3 of the available kills. Then the highest amonst them.
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Deadly", (641,100,124,49)))

		award_list = [] #mostly harmless
		for ninja in sprites.player_list:
				i = (ninja.stats_FIDs_inflicted + ninja.stats_item_kills) / (ninja.duels_participated * (len(sprites.player_list) - 1))
				if ninja.duels_participated >= 3:
					if i <= 0.05: #gets less than 5% of available kills. Then the lowest amonst them
						if award_list  == [] or i < award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Mostly Harmless", (641,150,124,49)))

		award_list = [] #most greedy/prepared
		for ninja in sprites.player_list:
				i = ninja.stats_shoes_acquired + ninja.stats_laser_acquired + ninja.stats_wings_acquired + ninja.stats_bomb_acquired + ninja.stats_volt_acquired + ninja.stats_mine_acquired + ninja.stats_rocket_acquired + ninja.stats_portal_gun_acquired + ninja.stats_ice_bomb_acquired + ninja.stats_cloak_acquired + ninja.stats_shield_acquired + ninja.stats_homing_bomb_acquired + ninja.stats_gravity_acquired
				if i >= 10:
					if i / ninja.duels_participated >= 5: 
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Most Prepared", (641,200,124,49)))

		award_list = [] #Least greedy/prepared
		for ninja in sprites.player_list:
				i = ninja.stats_shoes_acquired + ninja.stats_laser_acquired + ninja.stats_wings_acquired + ninja.stats_bomb_acquired + ninja.stats_volt_acquired + ninja.stats_mine_acquired + ninja.stats_rocket_acquired + ninja.stats_portal_gun_acquired + ninja.stats_ice_bomb_acquired + ninja.stats_cloak_acquired + ninja.stats_shield_acquired + ninja.stats_homing_bomb_acquired + ninja.stats_gravity_acquired
				if i / ninja.duels_participated <= 2: 
						if award_list  == [] or i < award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Least Prepared", (641,250,124,49)))


		award_list = [] #Most Knocks
		for ninja in sprites.player_list:
				i = ninja.stats_knocks_inflicted
				if i >= 20:
					if i / ninja.duels_participated >= 10: 
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Dueling Purist", (641,300,124,49)))

		award_list = [] #Best knock inflicted / received ratio
		for ninja in sprites.player_list:
			if ninja.stats_knocks_received != 0:
				i = ninja.stats_knocks_inflicted / ninja.stats_knocks_received
			else:
				i = ninja.stats_knocks_inflicted
			if i >= 3:
				if award_list  == [] or i > award_list[1]:
					award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Dueling Master", (641,350,124,49)))

		award_list = [] #Worst knock inflicted / received ratio
		for ninja in sprites.player_list:
			if ninja.stats_knocks_inflicted != 0:
				i = ninja.stats_knocks_received / ninja.stats_knocks_inflicted
			else:
				i = ninja.stats_knocks_received
			if i >= 3:
				if award_list  == [] or i > award_list[1]:
					award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Dueling Rookie", (766,0,124,49)))


		award_list = [] #Survives until end of 90% of duels. Min 3 duels.
		for ninja in sprites.player_list:
				i = ninja.stats_duels_survived / ninja.duels_participated
				if i >= 0.9:
					if ninja.duels_participated >= 3:
						if award_list  == [] or i > award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Ironman Award", (766,50,124,49)))


		award_list = [] #Survives until end of 10% of duels or less. Min 3 duels.
		for ninja in sprites.player_list:
				i = ninja.stats_duels_survived / ninja.duels_participated
				if i <= 0.1:
					if ninja.duels_participated >= 3:
						if award_list  == [] or i < award_list[1]:
							award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Snack Duty Award", (766,100,124,49)))


		award_list = [] #Wins. On Team. Contributes 90% of VP. Tiebreak is FIDS + Kills.
		for ninja in sprites.player_list:
			if ninja.current_VP >= options.versus_VP_required: #won!
				team = []
				for teammate in sprites.player_list:
					if teammate.color == ninja.color:
						team.append(teammate)
				if len(team) > 1: #on a team!
					i = ninja.VP_earned / ninja.current_VP
					if i >= 0.9:
						if options.versus_VP_required >= 3:
							if award_list  == [] or i > award_list[1]:
								award_list  = [ninja, i]
							elif i == award_list[1]:
								ninja_tiebreak = ninja.stats_FIDs_inflicted + ninja.stats_item_kills
								otherninja_tiebreak = award_list[0].stats_FIDs_inflicted + award_list[0].stats_item_kills
								if ninja_tiebreak > otherninja_tiebreak:
									award_list = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Team MVP", (766,150,124,49)))

		award_list = [] #Wins. On Team. Contributes 10% of VP or less.
		for ninja in sprites.player_list:
			if ninja.current_VP >= options.versus_VP_required: #won!
				team = []
				for teammate in sprites.player_list:
					if teammate.color == ninja.color:
						team.append(teammate)
				if len(team) > 1: #on a team!
					i = ninja.VP_earned / ninja.current_VP
					if i <= 0.1:
						if options.versus_VP_required >= 3:
							if award_list  == [] or i < award_list[1]:
								award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("#Carried", (766,200,124,49)))


		award_list = [] #Wins. Ridiculously Efficient Round
		for ninja in sprites.player_list:
			if ninja.current_VP >= options.versus_VP_required: #won!
				if ninja.stats_FIDs_received == 0 and ninja.stats_item_deaths == 0:
					if ninja.duels_participated >= 3:
						i = ninja.stats_FIDs_inflicted + ninja.stats_item_kills
						if i >= 3:
							if award_list  == [] or i > award_list[1]:
									award_list  = [ninja, i]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Earth's Champion", (766,250,124,49)))

		award_list = [] #Unsung Participant. No other awards
		for ninja in sprites.player_list:
			if len(ninja.stats_awards_list) == 0:
				if award_list  == []:
					award_list = [ninja, 0]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Unsung... Participant", (766,300,124,49)))

		award_list = [] #Unsung Participant. No other awards
		for ninja in sprites.player_list:
			if len(ninja.stats_awards_list) == 0:
				if award_list  == []:
					award_list = [ninja, 0]
		if award_list  != []:
			award_list[0].stats_awards_list.append(("Unsung Participant's +1", (766,350,124,49)))

		#AWARD IDEAS
		#garbage time
		#turncloack
		#shortest playtime (vs snack duty, which is fewest rounds survived.) - Most Distracted.
		#deaths by specific level weapons. ie. boulders (Indiana joke), Spike(), Flames (smores?), saw (Workplace Claim)
		#Solar flare awards. (most time confused, most luminous, ...solar flare deaths?)
		#Metal Suit awards. (time spent, stomps)
		#Most frames falling -adrenaline junkie - thrill seeker.
		#most times activating 'stomp' - fall from height) - Most impactful
		#upside down pole climb, most time on pole - Best Pole Moves
		#Most time with eye following - Most Alluring
		#Most death variety - most interesting demise list
		#Most Wins in Classic. -Most Likely to be Enslaved. Mightiest Gladiator.
		#Most times collided wall.
		#Turncloak (Teammate kills)
		#Most 'slide' frame. Least Friction.



		'''
		Least accurate / trigger happy (terible accuracy)
		Most Cowardly (time idle + time invisible + time ducking)
		Fetal Position Award. (most crouching)
		Most Frantic ()
		Most honorable (least shooting in back)
		Most dishonorable (Shoots layer in back)
		Shortest innings (short playing time before dying)
		Longest inning (long playing time before dying)
		Most devious (uses loop physics the best)
		Most reflective (bounces the most items via shield)
		Quick Draw Award (quickest kill of the round)
		Worst Accounting / least prepared? (hitting item button without having an item)
		Dueling Purist (Most FIDs. Few Kills)
		Longest shot (far laser)
		Trick shot (vertical laser... or portal kill)
		The One (Ridiculously efficient round)
		Turncloak (kills teammates)
		'''

		for ninja in sprites.player_list:
			print(ninja.name)
			print(ninja.stats_awards_list)
			while len(ninja.stats_awards_list) > 3:
				i = random.choice(ninja.stats_awards_list)
				ninja.stats_awards_list.remove(i)



	def load_menu(self):
		self.unlock_switch = False

		self.stats_dict = {}
		for ninja in sprites.player_list:
			self.stats_dict[ninja.name] = 'stats'
			ninja.awards_screen_sprite.activate()
			ninja.awards_screen_sprite.background.activate()

		self.get_awards() #go through stats and give out awards.

		sprites.reset_sprites() #reset all the contents of the sprites sprite groups.
		for ninja in sprites.ninja_list:
			sprites.ninja_list.remove(ninja)

		for ninja in sprites.player_list:
			sprites.ninja_list.add(ninja)

		for sprite in sprites.menu_sprite_list:
			active_sprite_list.remove(sprite)
			menu_sprite_list.remove(sprite)
		#sprites.menu_sprite_list.add(main_menu_sprite)
		#sprites.active_sprite_list.add(main_menu_sprite)

		background = level.Level_Background(-10, 'main_menu_background.png')
		#background_text = level.Level_Background(-8, 'main_menu.png')
		sprites.menu_sprite_list.add(background)
		#sprites.menu_sprite_list.change_layer(background, -10)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)
		#self.text_screen.image.fill(options.GREEN) #fill text screen with green to be re-blitted
		#self.text_screen.dirty = 1
		#background_text = level.Level_Background(-8, 'main_menu.png')

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		i = 'Greetings human. I will soon use this space to offer feedback on your duels in a condescending manner. For the good of Earth.'
		self.level_text = Screen_Text((10,310,sprites.size[0] - 20,50),i, 4)

		#create Mallow
		#mallow = level.Mallow ((0,330,640,30), False)
		'''
		i = 0
		while i < 640:
			mallow = level.Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		for ninja in sprites.ninja_list:
			ninja.lose(menu_use = True) #just takes ninjas out of active sprites list.
		
		#create temp_list to get ninjas in order. (name is always player1 through 4)
		temp_list = []
		for ninja in sprites.player_list:
			temp_list.append(ninja)
		temp_list.sort(key=lambda ninja: ninja.player_number)

		if len(sprites.player_list) == 2:
			x = (sprites.screen.get_width() / 3, sprites.screen.get_width() / 3 * 2)
		elif len(sprites.player_list) == 3:
			x = (sprites.screen.get_width() / 5, sprites.screen.get_width() / 2, sprites.screen.get_width() / 5 * 4)
		elif len(sprites.player_list) == 4:
			x = (89,243,397,551)


	
		self.done_screen = pygame.Surface((130,245))
		self.done_screen.fill(options.GREEN)
		self.done_screen =  Build_Menu_Perimeter(self.done_screen)
		self.done_screen.set_colorkey(options.GREEN)

		status_text = font_16.render('-Done-', 0,(WHITE))
		self.done_screen.blit(status_text, ((self.done_screen.get_width() / 2) - (status_text.get_width() / 2), 123 ))  #54 + (5 * 18)))

		i = 0
		for ninja in temp_list:
			#asdf

			#arrow1 = sprites.Menu_Arrow(((x[i] - 76), 180 + arrow_y_mod), 'left')
			#arrow1.activate()
			#arrow2 = sprites.Menu_Arrow(((x[i] + 75), 180 + arrow_y_mod), 'right')
			#arrow2.activate()

			

			tile = level.Platform(x[i] - 18, 35 + 48, 'classic', False)
			ninja.reset()
			ninja.place_ninja((x[i],50))

			arrow1 = sprites.Menu_Arrow((ninja.rect.centerx - 40, ninja.rect.centery + 30), 'left', ninja)
			arrow1.activate()
			arrow2 = sprites.Menu_Arrow((ninja.rect.centerx + 40, ninja.rect.centery + 30), 'right', ninja)
			arrow2.activate()

			ninja.awards_screen = pygame.Surface((130,245))
			ninja.awards_screen.fill(options.GREEN)
			ninja.awards_screen =  Build_Menu_Perimeter(ninja.awards_screen)
			ninja.awards_screen.set_colorkey(options.GREEN)
			ninja.stats_screen = ninja.awards_screen.copy()

			if ninja.profile == 'Guest':
				name = ninja.name
			else:
				name = ninja.profile
			nametext = font_16.render(name, 0,(ninja.color[2]))

			ninja.awards_screen.blit(nametext, (65 - (nametext.get_width() / 2), 45))
			ninja.stats_screen.blit(nametext, (65 - (nametext.get_width() / 2), 45))
			
			#Build Stats Screen For Ninja
			if options.versus_mode == 'Points':
				if ninja.current_VP >= options.versus_VP_required:
					text = 'Status: Victory'
				else:
					text = 'Status: Defeat'
			elif options.versus_mode == 'Classic':
				if ninja.current_wins >= options.versus_wins_required:
					text = 'Status: Victory'
				else:
					text = 'Status: Defeat'
			elif options.versus_mode == 'Stock':
				if ninja.lives >= 0:
					text = 'Status: Victory'
				else:
					text = 'Status: Defeat'
				print(ninja.lives)

			status_text = font_16.render(text, 0,(WHITE))
			ninja.stats_screen.blit(status_text, (65 - (status_text.get_width() / 2), 55 + (1 * 18)))

			stat_title1 = font_16.render('Duels Won: ' + str(ninja.stats_duels_survived), 0,(WHITE))
			ninja.stats_screen.blit(stat_title1, (65 - 46, 50 + (3 * 18)))

			stat_title1 = font_16.render('Inflicted:', 0,(WHITE))
			ninja.stats_screen.blit(stat_title1, (65 - 46, 55 + (4 * 18)))
			stat1 = font_16.render(' -Kills: ' + str(ninja.stats_item_kills), 0,(WHITE))
			ninja.stats_screen.blit(stat1, (65 - 46, 55 + (5 * 18)))
			stat2 = font_16.render(' -FIDs: ' + str(ninja.stats_FIDs_inflicted), 0,(WHITE))
			ninja.stats_screen.blit(stat2, (65 - 46, 55 + (6 * 18)))

			stat_title1 = font_16.render('Suffered:', 0,(WHITE))
			ninja.stats_screen.blit(stat_title1, (65 - 46, 60 + (7 * 18)))
			stat1 = font_16.render(' -Deaths: ' + str(ninja.stats_item_deaths), 0,(WHITE))
			ninja.stats_screen.blit(stat1, (65 - 46, 60 + (8 * 18)))
			stat2 = font_16.render(' -FIDs: ' + str(ninja.stats_FIDs_received), 0,(WHITE))
			ninja.stats_screen.blit(stat2, (65 - 46, 60 + (9 * 18)))

			#Build Awards Screen for Ninja
			q = len(sprites.player_list)

			
			ninja.rating = ninja.get_rating()
			
			status_text = font_16.render('Rating: ' + str(ninja.rating), 0,(WHITE))
			ninja.awards_screen.blit(status_text, (65 - (status_text.get_width() / 2), 55 + (1 * 18)))

			try:
				pic = ninja.stats_awards_list[0][1]
				award_pic = sprites.menu_sheet.getImage(pic[0], pic[1], pic[2], pic[3])
				ninja.awards_screen.blit(award_pic, (65 - 62, 104))
				#pygame.draw.rect(self.text_screen.image, options.DARK_PURPLE, (x[i] - 62, 154,124, 46),0)
				#award = font_12.render(ninja.stats_awards_list[0], 0,(WHITE))
				#self.text_screen.image.blit(award, (x[i] - (award.get_width() / 2), 165))
			except IndexError:
				print(IndexError)

			try:
				pic = ninja.stats_awards_list[1][1]
				award_pic = sprites.menu_sheet.getImage(pic[0], pic[1], pic[2], pic[3])
				ninja.awards_screen.blit(award_pic, (65 - 62, 150))
				#pygame.draw.rect(self.text_screen.image, options.DARK_PURPLE, (x[i] - 62, 200,124, 46),0)
				#award = font_12.render(ninja.stats_awards_list[1], 0,(WHITE))
				#self.text_screen.image.blit(award, (x[i] - (award.get_width() / 2), 210))
			except IndexError:
				pass

			try:
				pic = ninja.stats_awards_list[2][1]
				award_pic = sprites.menu_sheet.getImage(pic[0], pic[1], pic[2], pic[3])


				#award_pic = sprites.menu_sheet.getImage(766,350,124,49)
					
				ninja.awards_screen.blit(award_pic, (65 - 62, 196))
				#pygame.draw.rect(self.text_screen.image, options.DARK_PURPLE, (x[i] - 62, 246,124, 46),0)
				#award = font_12.render(ninja.stats_awards_list[2], 0,(WHITE))
				#self.text_screen.image.blit(award, (x[i] - (award.get_width() / 2), 255))
			except IndexError:
				pass

			#if self.stats_dict[ninja.name] == 'done':
			#	status_text = font_16.render('-Done-', 0,(WHITE))
			#	self.text_screen.image.blit(status_text, (x[i] - (status_text.get_width() / 2), 105 + (5 * 18)))


			i += 1





versus_awards_handler = Versus_Awards_Handler()


class Versus_Score_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.text_screen = None #created to draw text on. Cleared each frame.

		self.another_game = True
		self.win_color = None
		self.climb_list = []
		self.script_timer = 0
		self.kill_switch = 0 #turns to true as losers are sacrificed
		self.done_switch = False
		#self.fade_done = False
	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.another_game = True
			self.script_timer = 0
			self.kill_switch = False
			self.done_switch = False
			self.load_menu()
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			score_needed = self.check_score()
			if score_needed is False:
					self.next_level()
			else:
					pass
		
		#check for gamepads regularly.
		controls.input_handler.get_gamepads()



		self.run_script()
		self.update_score()

		#draw things here
		i = 0
		while i < 60:
			sprites.menu_sprite_list.update()
			level.Collision_Check() #Handles Non-Tile collision checks
			sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
			sprites.tile_list.update()
			sprites.level_objects.update()
			sprites.item_effects.update()
			sprites.level_ropes.update()
			sprites.background_objects.update()
			sprites.visual_effects.update()
			sprites.screen_objects.update()
			i += options.current_fps

		
		sprites.active_sprite_list.draw(sprites.screen)

		'''
		next_screen = False
		if options.versus_score_frequency == 'off':
			#pass through unless match is finished.
			if self.another_game is True:
				next_screen = True
			else:
				#if match is finished, wait until keypress
				if sprites.player1.menu_select_press is True or sprites.player2.menu_select_press is True or sprites.player3.menu_select_press is True or sprites.player4.menu_select_press is True:
					if self.done_switch is True:
						self.next_screen = True


		elif options.duel_counter < options.versus_score_frequency or (sprites.player1.menu_select_press is True or sprites.player2.menu_select_press is True or sprites.player3.menu_select_press is True or sprites.player4.menu_select_press is True):
			if self.done_switch is True:
				options.duel_counter = 0
			if self.done_switch is True or options.duel_counter < options.versus_score_frequency: 
				next_screen = True
		'''
				

			
		if sprites.player1.menu_select_press is True or sprites.player2.menu_select_press is True or sprites.player3.menu_select_press is True or sprites.player4.menu_select_press is True:
				if self.done_switch is True:
					sounds.mixer.menu_select.play()
					if self.another_game is True:
						self.next_level()
					elif self.another_game is False:
						self.awards_screen()

	def next_level(self):
		options.game_state = 'level'
		#options.game_mode = 'versus'
		level.level_builder.level_reset()
		#pygame.draw.rect(sprites.screen, BLACK, (0, 0, sprites.screen.get_width(), sprites.screen.get_height()), 0)
		self.menu_created = False



	def awards_screen(self):
		for ninja in sprites.player_list:
			ninja.collect_win_loss_stats(self.win_color)
			sounds.mixer.stop_song()
			sounds.mixer.change_song('music_menu.wav')
			sounds.mixer.start_song()
			options.game_state = 'versus_awards'
			#options.game_mode = 'versus'
			sprites.player1.reset()
			sprites.player2.reset()
			sprites.player3.reset()
			sprites.player4.reset()
			#sprites.player1.kill()
			#sprites.player2.kill()
			#sprites.player3.kill()
			#sprites.player4.kill()
			for sprite in sprites.tile_list: #kill previous level
				sprite.kill()
			self.menu_created = False
	
	def run_script(self):
		self.script_timer += 1

		if self.script_timer < 60:
			for ninja in self.climb_list:
				ninja.status = 'idle'

		if self.script_timer == 60:
			for ninja in self.climb_list:
				ninja.status = 'climb'
				if options.win_condition == 'Points':
					if ninja.current_VP > 0:
						ninja.up_press()
				elif options.win_condition == 'Wins':
					if ninja.current_wins > 0:
						ninja.up_press()

		for ninja in self.climb_list:
			dist = 244 - 48
			if options.win_condition == 'Points':
				climb_dist = (dist / options.versus_VP_required) * ninja.current_VP
			else:
				climb_dist = (dist / options.versus_wins_required) * ninja.current_wins
			
			if climb_dist > dist:
				climb_dist = dist
			stop_point = 320 - 48 -  climb_dist
			if ninja.rect.top <= stop_point:
				ninja.up_release()

		if self.script_timer > 60 and all(ninja.change_y == 0 for ninja in self.climb_list):
			self.done_switch = True

	def kill_losers(self):
		q = random.choice((1,2,3))


		for ninja in self.climb_list:
			if (options.win_condition == 'Points' and ninja.current_VP < options.versus_VP_required) or (options.win_condition == 'Wins' and ninja.current_wins < options.versus_wins_required):
				if q == 1:
					rect = pygame.Rect(ninja.rect.x,0,ninja.rect.width,360)
					for tile in sprites.tile_list:
						if tile.type != 'mallow' and tile.rect.colliderect(rect):
							if tile.type == 'platform':
								sprites.particle_generator.tile_death_particles(tile.rect, tile.style, tile.inverted_g, 0)
							elif tile.type == 'pole':
								sprites.particle_generator.pole_death_particles(tile.rect)
							tile.kill()

					ninja.status = 'falling'

				elif q == 2:
					sprites.active_items.append(ninja.bomb_sprite)
					ninja.bomb_sprite.bomb_throw_speed = ninja.bomb_sprite.short_throw_speed
					ninja.bomb_sprite.status = 'bomb'
					ninja.bomb_sprite.image_number = 1
					ninja.bomb_sprite.frame_counter = 0
					ninja.bomb_sprite.bomb_timer = 35
					ninja.bomb_sprite.visible = 1
					ninja.bomb_sprite.rect.centerx = ninja.rect.left - 40
					ninja.bomb_sprite.rect.bottom = 0
					ninja.bomb_sprite.change_x = ninja.bomb_sprite.bomb_throw_speed
					ninja.bomb_sprite.change_y = 0
					ninja.bomb_sprite.true_x = ninja.bomb_sprite.rect.x
					ninja.bomb_sprite.true_y = ninja.bomb_sprite.rect.y

				elif q == 3:
					ninja.projectile1.fire_laser()
					ninja.projectile1.fire = True
					choice = random.choice(('left','right'))
					if choice == 'left':
						ninja.projectile1.rect.left = 640
						ninja.projectile1.change_x = ninja.projectile1.laser_speed * -1
					else:
						ninja.projectile1.rect.right = 0
						ninja.projectile1.change_x = ninja.projectile1.laser_speed

					ninja.projectile1.rect.centery = ninja.rect.centery
					if ninja.projectile1.rect.top < 124:
						ninja.projectile1.rect.top = 124

					ninja.projectile1.true_x = ninja.projectile1.rect.x
					ninja.projectile1.true_y = ninja.projectile1.rect.y


	def update_score(self):
		self.text_screen.image.fill(options.GREEN) #fill text screen with green to be re-blitted
		self.text_screen.dirty = 1

		MenuItem1 = font_30.render("Current Score ", 0,(WHITE))
		if options.win_condition == 'Points':
			MenuItem2 = font_16.render('(' + str(options.versus_VP_required) + ' VP Required)', 0,(WHITE))
		else:
			MenuItem2 = font_16.render('(' + str(options.versus_wins_required) + ' Wins Required)', 0,(WHITE))

		self.text_screen.image.blit(MenuItem1, ((sprites.screen.get_width() / 2) - (MenuItem1.get_width() / 2), 5))
		self.text_screen.image.blit(MenuItem2, ((sprites.screen.get_width() / 2) - (MenuItem2.get_width() / 2), 5 + MenuItem1.get_height()))


		win_color = None
		#team_list = []
		#for ninja in sprites.player_list:
		#	if ninja.color not in team_list:
		#		team_list.append(ninja.color)

		if len(self.climb_list) == 1:
			x = (sprites.screen.get_width() / 2, 0)
		elif len(self.climb_list) == 2:
			x = (sprites.screen.get_width() / 3, sprites.screen.get_width() / 3 * 2)
		elif len(self.climb_list) == 3:
			x = (sprites.screen.get_width() / 4, sprites.screen.get_width() / 4 * 2, sprites.screen.get_width() / 4 * 3)
		elif len(self.climb_list) == 4:
			x = (sprites.screen.get_width() / 5, sprites.screen.get_width() / 5 * 2, sprites.screen.get_width() / 5 * 3, sprites.screen.get_width() / 5 * 4)

		i = 0
		self.another_game = True
		victory = False
		#while len(team_list) > i:
		for sprite in self.climb_list:
			#	if sprite.color == team_list[i]:

					dist = 244 - 48
					if options.win_condition == 'Points':
						climb_dist = (dist / options.versus_VP_required) * sprite.current_VP
					else:
						climb_dist = (dist / options.versus_wins_required) * sprite.current_wins
					#stop_point = 320 - 48 -  climb_dist
					#if ninja.rect.top <= stop_point:
					#	ninja.up_release()
					'''
					current_dist = (320 - sprite.rect.bottom) #platform to bottom of sprite.
					VP_per_dist = (options.versus_VP_required / dist)
					VP = int(current_dist * VP_per_dist)
					'''

					#VP = int((320 - sprite.rect.bottom) * (options.versus_VP_required / dist))
					#raw_VP = (320 - sprite.rect.bottom) * (options.versus_VP_required / dist)
					#if raw_VP % 1 > 0.95:
					#	VP += 1
					#if VP > sprite.current_VP:
					#	VP = sprite.current_VP
					#elif VP < sprite.current_VP:
					
					score = '??'

					if options.win_condition == 'Points':
						if sprite.status == 'climb' and sprite.change_y == 0:
							score = sprite.current_VP
						if score != '??' and score >= options.versus_VP_required:
							victory = True #triggers killing losers below
						if sprite.FID is True or sprite.status == 'falling' or sprite.status == 'lose':
							score = sprite.current_VP
						text = str(score)
						item = font_16.render(text, 0, sprite.color[2])
						self.text_screen.image.blit(item, (x[i] - (item.get_width() / 2), 56))
						
						if score != '??' and score >= options.versus_VP_required:
							self.another_game = False
							text = font_30.render('Winner!', 0, sprite.color[2])
							self.win_color = sprite.color
							#new_text = outline_text(text, sprite.color[2], options.WHITE)
							self.text_screen.image.blit(text, (x[i] - (text.get_width() / 2), 200))
							#def outline_text(text_image, text_color, outline_color
					elif options.win_condition == 'Wins':
						if sprite.status == 'climb' and sprite.change_y == 0:
							score = sprite.current_wins
						if score != '??' and score >= options.versus_wins_required:
							victory = True #triggers killing losers below
						if sprite.FID is True or sprite.status == 'falling' or sprite.status == 'lose':
							score = sprite.current_wins
						text = str(score)
						item = font_16.render(text, 0, sprite.color[2])
						self.text_screen.image.blit(item, (x[i] - (item.get_width() / 2), 56))
						
						if score != '??' and score >= options.versus_wins_required:
							self.another_game = False
							text = font_30.render('Winner!', 0, sprite.color[2])
							self.win_color = sprite.color
							#new_text = outline_text(text, sprite.color[2], options.WHITE)
							self.text_screen.image.blit(text, (x[i] - (text.get_width() / 2), 200))
							#def outline_text(text_image, text_color, outline_color
					i += 1

		if victory is True:
			if self.kill_switch is False:
				self.kill_switch = True
				self.kill_losers()

		if self.done_switch is True:
				if options.control_preferences['player1'] == 'keyboard':
					select_pic = controls.input_handler.button_keyboard_z
				else:
					select_pic = sprites.player1.gamepad_layout['button_jump_image']
				self.text_screen.image.blit(select_pic, (620,340))

	def check_score(self):
		score_needed = False

		if options.versus_score_frequency == 'Off':
			for ninja in sprites.ninja_list:
				if options.win_condition == 'Points':
					if ninja.current_VP >= options.versus_VP_required:
						score_needed = True
						break
				elif options.win_condition == 'Wins':
					if ninja.current_wins >= options.versus_wins_required:
						score_needed = True
						break

		else:
			for ninja in sprites.ninja_list:
				if options.win_condition == 'Points':
					if ninja.current_VP >= options.versus_VP_required:
						score_needed = True
						break
				elif options.win_condition == 'Wins':
					if ninja.current_wins >= options.versus_wins_required:
						score_needed = True
						break
			
			options.duel_counter += 1
			if options.duel_counter == options.versus_score_frequency:
				options.duel_counter = 0
				score_needed = True

		return(score_needed)

	def load_menu(self):
		#client.online_handler.message_list = []

		sprites.reset_sprites() #reset all the contents of the sprites sprite groups.
		for ninja in sprites.ninja_list:
			sprites.ninja_list.remove(ninja)

		for ninja in sprites.player_list:
			sprites.ninja_list.add(ninja)

		for sprite in sprites.menu_sprite_list:
			active_sprite_list.remove(sprite)
			menu_sprite_list.remove(sprite)
		#sprites.menu_sprite_list.add(main_menu_sprite)
		#sprites.active_sprite_list.add(main_menu_sprite)

		background = level.Level_Background(-10, 'main_menu_background.png')
		#background_text = level.Level_Background(-8, 'main_menu.png')
		sprites.menu_sprite_list.add(background)
		#sprites.menu_sprite_list.change_layer(background, -10)
		background.dirty = 1

		self.text_screen = level.Level_Background(10, options.GREEN)
		self.text_screen.image.fill(options.GREEN) #fill text screen with green to be re-blitted
		self.text_screen.dirty = 1
		#background_text = level.Level_Background(-8, 'main_menu.png')

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))



		#create Mallow
		mallow = level.Mallow ((0,330,640,30), False)
		'''
		i = 0
		while i < 640:
			mallow = level.Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		for ninja in sprites.ninja_list:
			ninja.lose(menu_use = True) #just takes ninjas out of active sprites list.
		
		self.text_screen.image.fill(options.GREEN) #fill text screen with green to be re-blitted
		self.text_screen.dirty = 1

		MenuItem1 = font_30.render("Current Score ", 0,(WHITE))
		MenuItem2 = font_16.render('(' + str(options.versus_VP_required) + ' VP Required)', 0,(WHITE))

		self.text_screen.image.blit(MenuItem1, ((sprites.screen.get_width() / 2) - (MenuItem1.get_width() / 2), 5))
		self.text_screen.image.blit(MenuItem2, ((sprites.screen.get_width() / 2) - (MenuItem2.get_width() / 2), 5 + MenuItem1.get_height()))

		self.climb_list = []
		win_color = None
		#team_list = []
		for ninja in sprites.player_list:
			add = True
			for otherninja in self.climb_list:
				if ninja.color == otherninja.color:
					add = False
					break
			if add is True:
				self.climb_list.append(ninja)


		if len(self.climb_list) == 1:
			x = (sprites.screen.get_width() / 2, 0)
		elif len(self.climb_list) == 2:
			x = (sprites.screen.get_width() / 3, sprites.screen.get_width() / 3 * 2)
		elif len(self.climb_list) == 3:
			x = (sprites.screen.get_width() / 4, sprites.screen.get_width() / 4 * 2, sprites.screen.get_width() / 4 * 3)
		elif len(self.climb_list) == 4:
			x = (sprites.screen.get_width() / 5, sprites.screen.get_width() / 5 * 2, sprites.screen.get_width() / 5 * 3, sprites.screen.get_width() / 5 * 4)

		i = 0
		self.another_game = True
		#self.climb_list = []
		#while len(team_list) > i:
		#	for sprite in sprites.team_list:
				#sprite.current_VP = random.choice((100,99)) #testing purposes.
		#		if sprite.color == team_list[i]:
					#text = str('??')
		for sprite in self.climb_list:
					item = font_16.render('??', 0, sprite.color[2])
					self.text_screen.image.blit(item, (x[i] - (item.get_width() / 2), 56))
					#if sprite.current_VP >= options.versus_VP_required:
					#	self.another_game = False
					#	text = font_30.render('Winner!', 0, sprite.color[1])
					#	self.win_color = sprite.color
					#	self.text_screen.image.blit(text, (x[i] - (text.get_width() / 2), 200))

					sprite.reset()
					sprite.place_ninja((x[i],272))
					#self.climb_list.append(sprite)
					tile = level.Platform(x[i] - 18, 320, 'classic', False)
					pole = level.Pole(x[i], 65, 5, 4)
					i += 1


versus_score_handler = Versus_Score_Handler()

'''
def versus_score():
	

	screen = sprites.screen

	pygame.draw.rect(screen, BLACK, (0, 0, screen.get_width(), screen.get_height()), 0)


	MenuItem1 = font_30.render("Versus Score", 0,(WHITE))
	screen.blit(MenuItem1, ((screen.get_width() / 2) - (MenuItem1.get_width() / 2), 20))

	win_color = None

	team_list = []
	for ninja in sprites.player_list:
		if ninja.color not in team_list:
			team_list.append(ninja.color)

	if len(team_list) == 2:
		x = (screen.get_width() / 3, screen.get_width() / 3 * 2)
	elif len(team_list) == 3:
		x = (screen.get_width() / 4, screen.get_width() / 4 * 2, screen.get_width() / 4 * 3)
	elif len(team_list) == 4:
		x = (screen.get_width() / 5, screen.get_width() / 5 * 2, screen.get_width() / 5 * 3, screen.get_width() / 5 * 4)

	i = 0
	another_game = True
	while len(team_list) > i:
		for sprite in sprites.player_list:
			if sprite.color == team_list[i]:
				text = str(sprite.current_VP) + "/" + str(options.versus_VP_required)
				item = font_30.render(text, 0, sprite.color[1])
				screen.blit(item, (x[i] - (item.get_width() / 2), 100))
				if sprite.current_VP >= options.versus_VP_required:
					another_game = False
					text = font_30.render('Winner!', 0, sprite.color[1])
					win_color = sprite.color
					screen.blit(text, (x[i] - (text.get_width() / 2), 200))
				image = sprite.idle_right[1]
				screen.blit(image, (x[i] - (image.get_width() / 2), 150))

				break
		i += 1



	if sprites.player1.menu_select_press is True or sprites.player2.menu_select_press is True or sprites.player3.menu_select_press is True or sprites.player4.menu_select_press is True:
		if another_game is True:
			options.game_state = 'level'
			options.game_mode = 'versus'
			level.level_builder.level_reset()
			pygame.draw.rect(screen, BLACK, (0, 0, screen.get_width(), screen.get_height()), 0)
		elif another_game is False:
			for ninja in sprites.player_list:
				ninja.collect_win_loss_stats(win_color)
			sounds.mixer.stop_song()
			sounds.mixer.change_song('music_menu.wav')
			sounds.mixer.start_song()
			options.game_state = 'player_select'
			options.game_mode = 'versus'
			sprites.player1.reset()
			sprites.player2.reset()
			sprites.player3.reset()
			sprites.player4.reset()
			sprites.player1.kill()
			sprites.player2.kill()
			sprites.player3.kill()
			sprites.player4.kill()
			for sprite in sprites.tile_list: #kill previous level
				sprite.kill()
'''

class Main_Menu_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.script_choice = 0
		self.script_timer = -10
		self.fade_done = False
		self.intro_switch = False
		self.add_menu = False
	def update(self):
		if self.menu_created is False:
			if self.intro_switch is False:
				self.intro_switch = True
			else:
				sprites.transition_screen.fade('swipe_down', True, options.GREEN)
				self.script_timer = 0
			self.menu_created = True
			self.load_menu()
			self.script_choice = random.choice((1,2))

		if self.add_menu is True:
			self.add_menu = False
			sprites.menu_sprite_list.add(main_menu_sprite)
			sprites.active_sprite_list.add(main_menu_sprite)
			
			
		
		#check for gamepads regularly
		if options.game_state == 'main_menu': #in case source is instruction booklet
			controls.input_handler.get_gamepads()

			if sprites.player1.gamepad_config == False:
				if sprites.player1.menu_left_press is True:
					main_menu_sprite.scroll('left')
					if controls.input_handler.gamepad1_ninja == sprites.player1 and options.control_preferences['player1'] == 'gamepad':
						self.p1_gamepad_setup()
					sprites.player1.controls_sprite.update_buttons()

				if sprites.player1.menu_right_press is True:
					main_menu_sprite.scroll('right')
					if controls.input_handler.gamepad1_ninja == sprites.player1 and options.control_preferences['player1'] == 'gamepad':
						self.p1_gamepad_setup()
					sprites.player1.controls_sprite.update_buttons()

				if sprites.player1.menu_up_press is True:
					main_menu_sprite.scroll('up')
					if controls.input_handler.gamepad1_ninja == sprites.player1 and options.control_preferences['player1'] == 'gamepad':
						self.p1_gamepad_setup()
					sprites.player1.controls_sprite.update_buttons()
						

				if sprites.player1.menu_down_press is True:
					main_menu_sprite.scroll('down')
					if controls.input_handler.gamepad1_ninja == sprites.player1 and options.control_preferences['player1'] == 'gamepad':
						self.p1_gamepad_setup()
					sprites.player1.controls_sprite.update_buttons()

				if sprites.player1.menu_select_press is True:
					if controls.input_handler.gamepad1_ninja == sprites.player1 and options.control_preferences['player1'] == 'gamepad':
						self.p1_gamepad_setup()

					if main_menu_sprite.menu_list[main_menu_sprite.vertical_selection][0] == 'Settings':
						sounds.mixer.menu_select.play()
						self.menu_created = False
						options.game_state = 'game_options'

					elif main_menu_sprite.menu_list[main_menu_sprite.vertical_selection][0] == 'Instructions':
						sounds.mixer.menu_select.play()
						#self.menu_created = False
						options.game_state = 'instructions'

					elif main_menu_sprite.menu_list[main_menu_sprite.vertical_selection][0] == 'Quit':
						sounds.mixer.menu_select.play()
						options.exit = True

					elif main_menu_sprite.menu_list[main_menu_sprite.vertical_selection][0] == 'Versus':
						sounds.mixer.menu_select.play()
						options.game_mode = 'versus'
						self.menu_created = False

						message = options.server_message[1]
						if message != None:
							choice_handler.activate([sprites.player1], message, next_game_state = 'player_select', signed = True)
							options.server_message = (options.server_message[0],None)
							data_manager.data_handler.save_data()
						else:
							options.game_state = 'player_select'
						#66666666666666

						#self.menu_created = False
						#options.game_state = 'player_select'
						#options.game_mode = 'versus'

					elif main_menu_sprite.menu_list[main_menu_sprite.vertical_selection][0] == 'Co-op': #not currently a choice
						sounds.mixer.menu_select.play()
						self.menu_created = False
						options.game_state = 'player_select'
						options.game_mode = 'coop'

					elif main_menu_sprite.menu_list[main_menu_sprite.vertical_selection][0] == 'Online':
						sounds.mixer.menu_select.play()
						self.menu_created = False
						options.game_state = 'player_select'
						options.game_mode = 'online'



				

		# Update the player and other sprites as needed
		i = 0
		while i < 60:
			sprites.menu_sprite_list.update()
			level.Collision_Check() #Handles Non-Tile collision checks
			sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
			sprites.tile_list.update()
			sprites.level_objects.update()
			sprites.item_effects.update()
			sprites.background_objects.update()
			sprites.visual_effects.update()
			i += options.current_fps
			sprites.screen_objects.update()

			self.run_script()
			
		

		#for bar in  intro_handler.matrix_bar_list:
		#		#if options.game_state == 'main_menu':
		#		bar.update()

		sprites.active_sprite_list.draw(sprites.screen)

		

	def p1_gamepad_setup(self):
		if len(controls.input_handler.gamepads) > 0:
			controls.input_handler.p1_gamepad_setup()

	def run_script(self):
		self.script_timer += 1
		#print(self.script_timer)


		self.script_choice = 1
		if self.script_choice == 1:
			if self.script_timer < 90 and self.script_timer >= 0:
				sprites.player1.right_press()
				sprites.player3.left_press()



			if self.script_timer == 90:
				sprites.player3.roll_press()

			if self.script_timer > 90 and self.script_timer < 185: #and self.script_timer < 111:
				sprites.player1.left_press()

			if self.script_timer > 90 and self.script_timer < 148:
				sprites.player3.left_press()
			if self.script_timer == 148:
				sprites.player3.left_release()	

			if self.script_timer == 185:
				sprites.player1.roll_press()

			if self.script_timer == 185:
				sprites.player3.jump_press()
				
			
			if self.script_timer == 163:
				sprites.player2.left_press()
				sprites.player2.left_release()
				sprites.player2.item = 'laser'
				sprites.player2.item_press()

			
			if self.script_timer == 249:
				sprites.player3.left_release()
			if self.script_timer > 249 and self.script_timer < 392:	
				sprites.player3.right_press()
			

			if self.script_timer == 314:
				sprites.player3.jump_press()

			if self.script_timer == 350:
				sprites.player3.item = 'ice bomb'
				sprites.player3.item_press()
			if self.script_timer == 354:
				sprites.player3.jump_press()
			if self.script_timer == 392:
				sprites.player3.right_release()

			if self.script_timer == 310 or self.script_timer == 350:
				sprites.player2.item_press()

			if self.script_timer > 410 and self.script_timer < 555:
				sprites.player3.right_press()
			if self.script_timer == 555:
				sprites.player3.right_release()
			
			if self.script_timer == 417:
				self.frozen_background.visible = 1

			if self.script_timer == 550:
				sprites.player1.reset()
				#sprites.player1.change_color('left', 5)
				sprites.player1.status = 'right'
				sprites.player1.place_ninja((395 + 50,0))
				sprites.player1.rect.bottom = 0
				sprites.player1.rect.centerx = 395
				sprites.player1.direction = 'right'
				sprites.player1.roll_press()
				#sprites.player1.change_x = 2

			if self.script_timer == 570:
				sprites.player1.status = 'jump'

			if self.script_timer == 575:
				sprites.player1.change_x = 0

			if self.script_timer == 577:
				sprites.player1.item = 'bomb'
				sprites.player1.item_press()

			if self.script_timer == 592:
				sprites.player4.status = 'right'
				sprites.player4.place_ninja((192 + 46,0))
				sprites.player4.rect.bottom = 0
				sprites.player4.rect.centerx = 192
				sprites.player4.roll_press()
				#sprites.player4.change_x = 2

			if self.script_timer == 612:
				sprites.player4.status = 'jump'


			if self.script_timer == 620:
				sprites.player4.item = 'laser'
				sprites.player4.item_press()

			if self.script_timer == 640:
				sprites.player1.item = 'shield'
				sprites.player1.item_press()

			if self.script_timer == 660:
				sprites.player1.smug = True

			if self.script_timer > 800:
				#just to stop them from eventually looping back
				sprites.player3.rect.y = 600
				sprites.player2.rect.y = 600
				sprites.player4.rect.y = 600



	def load_menu(self):

		sprites.player1.controls_sprite.activate((12,270))
		
		sprites.reset_sprites() #reset all the contents of the sprites sprite groups.

		sprites.menu_sprite_list.add(main_menu_sprite)
		sprites.active_sprite_list.add(main_menu_sprite)

		version_sprite = Version_Sprite(options.version)

		background = level.Level_Background(-10, 'main_menu_background.png')
		background_text = level.Level_Background(-8, 'main_menu.png')
		self.frozen_background = level.Level_Background(-7, 'main_menu_frozen.png')
		self.frozen_background.visible = 0
		sprites.menu_sprite_list.add(background)
		sprites.menu_sprite_list.change_layer(background, -10)
		background.dirty = 1

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))



		#create Mallow
		mallow = level.Mallow ((0,330,640,30), False)
		'''
		i = 0
		while i < 640:
			mallow = level.Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		sprites.active_sprite_list.add(sprites.player1)
		sprites.active_sprite_list.add(sprites.player2)
		sprites.active_sprite_list.add(sprites.player3)
		sprites.active_sprite_list.add(sprites.player4)


		#sprites.player1.rect.center = (90,90)
		#sprites.player2.rect.center = (552,90)
		#sprites.player3.rect.center = (230,90)
		#sprites.player4.rect.center = (600,600)

		sprites.player1.place_ninja((90,100))
		sprites.player2.place_ninja((552,100))
		sprites.player3.place_ninja((280,100))
		sprites.player4.place_ninja((600,600))

		sprites.player2.direction = 'left'
		sprites.player3.direction = 'left'

		set_default_ninjas()

		'''
		sprites.player1.change_color(None, None, color_tuple = options.PURPLE_LIST, change_bandana = False)
		sprites.player1.bandana_color = options.RED_LIST
		sprites.player1.bandana.kill()
		sprites.player1.bandana = rope_physics.Bandana_Knot(sprites.player1, sprites.player1.bandana_color)

		sprites.player2.change_color(None, None, color_tuple = options.BLUE_LIST, change_bandana = False)
		sprites.player2.bandana_color = options.PURPLE_LIST
		sprites.player2.bandana.kill()
		sprites.player2.bandana = rope_physics.Bandana_Knot(sprites.player2, sprites.player2.bandana_color)

		sprites.player3.change_color(None, None, color_tuple = options.GREEN_LIST, change_bandana = False)
		sprites.player3.bandana_color = options.ORANGE_LIST
		sprites.player3.bandana.kill()
		sprites.player3.bandana = rope_physics.Bandana_Knot(sprites.player3, sprites.player3.bandana_color)

		sprites.player4.change_color(None, None, color_tuple = options.RED_LIST, change_bandana = False)
		sprites.player4.bandana_color = options.BLUE_LIST
		sprites.player4.bandana.kill()
		sprites.player4.bandana = rope_physics.Bandana_Knot(sprites.player4, sprites.player4.bandana_color)
		'''

		#sprites.player1.change_color('left', 0)
		#sprites.player2.change_color('left', 1)
		#sprites.player3.change_color('left', 6)
		#sprites.player4.change_color('left', 3)

		#create Tiles on tops of words
		tile = level.Tile(69, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(84, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(117, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(100, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(132, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(164, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(145, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(188, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(207, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(240, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(220, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(254, 127, 'classic', False)
		tile.visible = 0

		tile = level.Tile(264, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(264, 160, 'classic', False)
		tile.visible = 0
		tile = level.Tile(264, 184, 'classic', False)
		tile.visible = 0
		tile = level.Tile(288, 184, 'classic', False)
		tile.visible = 0
		tile = level.Tile(312, 184, 'classic', False)
		tile.visible = 0

		tile = level.Tile(316, 184, 'classic', False)
		tile.visible = 0
		tile = level.Tile(316, 160, 'classic', False)
		tile.visible = 0
		tile = level.Tile(316, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(316, 127, 'classic', False)
		tile.visible = 0

		tile = level.Tile(330, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(340, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(340, 160, 'classic', False)
		tile.visible = 0
		tile = level.Tile(340, 184, 'classic', False)
		tile.visible = 0
		tile = level.Tile(364, 184, 'classic', False)
		tile.visible = 0
		tile = level.Tile(388, 184, 'classic', False)
		tile.visible = 0

		tile = level.Tile(392, 184, 'classic', False)
		tile.visible = 0
		tile = level.Tile(392, 160, 'classic', False)
		tile.visible = 0
		tile = level.Tile(392, 136, 'classic', False)
		tile.visible = 0

		tile = level.Tile(401, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(425, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(444, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(477, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(465, 136, 'classic', False)
		tile.visible = 0

		tile = level.Tile(491, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(505, 136, 'classic', False)
		tile.visible = 0
		tile = level.Tile(524, 127, 'classic', False)
		tile.visible = 0
		tile = level.Tile(540, 127, 'classic', False)
		tile.visible = 0








		'''
		i = 0
		while i < 14:
			
			platform = level.Platform(65  + (i * 36), 127, 'classic', False)
			platform.visible = 0
			i += 1
		'''

		#Create two small platforms on top of the 'Es'
		platform = level.Platform(65  + (0 * 36), 64, 'classic', False)
		platform.rect = pygame.Rect(226,64,23,7)
		platform.top_rect = pygame.Rect(platform.rect.x, platform.rect.y, platform.rect.width,5) 
		platform.visible = 0
		sprites.quadrant_handler.join_quadrants(platform)

		platform2 = level.Platform(65  + (0 * 36), 64, 'classic', False)
		platform2.rect = pygame.Rect(434,64,23,7)
		platform2.top_rect = pygame.Rect(platform2.rect.x, platform2.rect.y, platform2.rect.width,5) 
		platform2.visible = 0
		sprites.quadrant_handler.join_quadrants(platform2)


		count = 0
		while count < 20:
			#platform = level.Tile(0 - 18, sprites.size[1] - (24 * count), 'classic')
			#platform2 = level.Tile(sprites.size[0] - 6, sprites.size[1] - (24 * count), 'classic')

			platform = level.Tile(-12, sprites.size[1] - (24 * count), 'menu', False)
			platform2 = level.Tile(sprites.size[0] - 12, sprites.size[1] - (24 * count), 'menu', False)

			count += 1

		for tile in sprites.tile_list:
			if tile.type == 'tile':
				tile.check_sides(mid_level = True)

		sounds.mixer.change_song('music_menu.wav')
		sounds.mixer.start_song()

		#for sprite in sprites.active_sprite_list:
		#	print(sprite)


main_menu_handler = Main_Menu_Handler()

class Version_Sprite(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self, text):
		#constructor functionf
		pygame.sprite.DirtySprite.__init__(self)

		#the following serves some function, but mostly just replicates ninja.
		
		self.type = 'version_sprite'

		self.image = font_12.render(text, 0,(options.WHITE))
		self.rect = self.image.get_rect()
		
		self.rect.right = 563
		self.rect.y = 215


		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 0)
		sprites.background_objects.add(self)

		self.dirty = 1


	def update(self):

		pass

class Player_Select_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.text_screen = None #created to draw text on. Cleared each frame.

		self.arrow_list = []

		self.custom_menu_choices = ('Customize_Gamepad', 'Accessory', 'Avatar', 'Profile')

		self.source = 'main menu'

		self.online_options = ('Host', 'Join')
		self.online_selection = 0
		self.online_status = 'offline' #'offline' or 'online'
		self.dot_counter = 0
		self.dots = '   '
		self.max_player = 4
		self.error_timer = 0 #used to time brief messages.

		self.ping_counter = 0

		self.match_select_number = 0


		#self.fade_done = False
	def update(self):		
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			#sprites.transition_screen.fade('swipe_down', True, options.GREEN)
		

		#zzz Online Stuff Here:
		#self.online_status = 'online':
		#	if sprites.player1.menu_status == 'team select' and client.online_handler.online_type == 'host':
		#		self.ping_counter += 1
		#		if self.ping_counter == 2:

		#Online Stuff HEre
		#if client.online_handler.online is True:


		#check for gamepads regularly.
		controls.input_handler.get_gamepads()

		self.text_screen.image.fill(options.GREEN) #fill text screen with green to be re-blitted
		self.text_screen.dirty = 1

		if sprites.player1.menu_up_press is True and sprites.player1.gamepad_config == False:
			if sprites.player1.menu_status == 'profile select':
				sprites.player1.profile_number -= 1
				if sprites.player1.profile_number < 0:
					sprites.player1.profile_number = len(options.profile_list) - 1
			elif sprites.player1.menu_status == 'new profile':
				sprites.player1.text_number -= 1
				sprites.player1.text_blink = 0
				if sprites.player1.text_number < 0:
					sprites.player1.text_number = len(options.upper_case_list) - 1
			elif sprites.player1.menu_status == 'team select':
				sprites.player1.bandana.headband.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player1.menu_status == 'customize':
				sprites.player1.custom_menu_row -= 1
				if sprites.player1.custom_menu_row < 0:
					sprites.player1.custom_menu_row = len(self.custom_menu_choices) - 1
			elif sprites.player1.menu_status in ('online select', 'online exit'):
				self.online_selection -= 1
				if self.online_selection < 0:
					self.online_selection = len(self.online_options) - 1
			elif sprites.player1.menu_status == 'match list':
				self.match_select_number -= 1
				if self.match_select_number < 0:
					self.match_select_number = len(client.online_handler.current_match_list) - 1

		elif sprites.player1.menu_down_press is True and sprites.player1.gamepad_config == False:
			if sprites.player1.menu_status == 'profile select':
				sprites.player1.profile_number += 1
				if sprites.player1.profile_number > len(options.profile_list) - 1:
					sprites.player1.profile_number = 0
			elif sprites.player1.menu_status == 'new profile':
				sprites.player1.text_number += 1
				sprites.player1.text_blink = 0
				if sprites.player1.text_number  > len(options.upper_case_list) - 1:
					sprites.player1.text_number = 0
			elif sprites.player1.menu_status == 'team select':
				sprites.player1.bandana.headband.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player1.menu_status == 'customize':
				sprites.player1.custom_menu_row += 1
				if sprites.player1.custom_menu_row > len(self.custom_menu_choices) - 1:
					sprites.player1.custom_menu_row = 0
			elif sprites.player1.menu_status in ('online select', 'online exit'):
				self.online_selection += 1
				if self.online_selection > len(self.online_options) - 1:
					self.online_selection = 0
			elif sprites.player1.menu_status == 'match list':
				self.match_select_number += 1
				if self.match_select_number > len(client.online_handler.current_match_list) - 1:
					self.match_select_number = 0


		if sprites.player2.menu_up_press is True and sprites.player2.gamepad_config == False:
			if sprites.player2.menu_status == 'profile select':
				sprites.player2.profile_number -= 1
				if sprites.player2.profile_number < 0:
					sprites.player2.profile_number = len(options.profile_list) - 1
			elif sprites.player2.menu_status == 'new profile':
				sprites.player2.text_number -= 1
				sprites.player2.text_blink = 0
				if sprites.player2.text_number < 0:
					sprites.player2.text_number = len(options.upper_case_list) - 1
			elif sprites.player2.menu_status == 'team select':
				sprites.player2.bandana.headband.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player2.menu_status == 'customize':
				sprites.player2.custom_menu_row -= 1
				if sprites.player2.custom_menu_row < 0:
					sprites.player2.custom_menu_row = len(self.custom_menu_choices) - 1

		elif sprites.player2.menu_down_press is True and sprites.player2.gamepad_config == False:
			if sprites.player2.menu_status == 'profile select':
				sprites.player2.profile_number += 1
				if sprites.player2.profile_number > len(options.profile_list) - 1:
					sprites.player2.profile_number = 0
			elif sprites.player2.menu_status == 'new profile':
				sprites.player2.text_number += 1
				sprites.player2.text_blink = 0
				if sprites.player2.text_number  > len(options.upper_case_list) - 1:
					sprites.player2.text_number = 0
			elif sprites.player2.menu_status == 'team select':
				sprites.player2.bandana.headband.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player2.menu_status == 'customize':
				sprites.player2.custom_menu_row += 1
				if sprites.player2.custom_menu_row > len(self.custom_menu_choices) - 1:
					sprites.player2.custom_menu_row = 0

		if sprites.player3.menu_up_press is True and sprites.player3.gamepad_config == False:
			if sprites.player3.menu_status == 'profile select':
				sprites.player3.profile_number -= 1
				if sprites.player3.profile_number < 0:
					sprites.player3.profile_number = len(options.profile_list) - 1
			elif sprites.player3.menu_status == 'new profile':
				sprites.player3.text_number -= 1
				sprites.player3.text_blink = 0
				if sprites.player3.text_number < 0:
					sprites.player3.text_number = len(options.upper_case_list) - 1
			elif sprites.player3.menu_status == 'team select':
				sprites.player3.bandana.headband.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player3.menu_status == 'customize':
				sprites.player3.custom_menu_row -= 1
				if sprites.player3.custom_menu_row < 0:
					sprites.player3.custom_menu_row = len(self.custom_menu_choices) - 1

		elif sprites.player3.menu_down_press is True and sprites.player3.gamepad_config == False:
			if sprites.player3.menu_status == 'profile select':
				sprites.player3.profile_number += 1
				if sprites.player3.profile_number > len(options.profile_list) - 1:
					sprites.player3.profile_number = 0
			elif sprites.player3.menu_status == 'new profile':
				sprites.player3.text_number += 1
				sprites.player3.text_blink = 0
				if sprites.player3.text_number  > len(options.upper_case_list) - 1:
					sprites.player3.text_number = 0
			elif sprites.player3.menu_status == 'team select':
				sprites.player3.bandana.headband.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player3.menu_status == 'customize':
				sprites.player3.custom_menu_row += 1
				if sprites.player3.custom_menu_row > len(self.custom_menu_choices) - 1:
					sprites.player3.custom_menu_row = 0

		if sprites.player4.menu_up_press is True and sprites.player4.gamepad_config == False:
			if sprites.player4.menu_status == 'profile select':
				sprites.player4.profile_number -= 1
				if sprites.player4.profile_number < 0:
					sprites.player4.profile_number = len(options.profile_list) - 1
			elif sprites.player4.menu_status == 'new profile':
				sprites.player4.text_number -= 1
				sprites.player4.text_blink = 0
				if sprites.player4.text_number < 0:
					sprites.player4.text_number = len(options.upper_case_list) - 1
			elif sprites.player4.menu_status == 'team select':
				sprites.player4.bandana.headband.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player4.menu_status == 'customize':
				sprites.player4.custom_menu_row -= 1
				if sprites.player4.custom_menu_row < 0:
					sprites.player4.custom_menu_row = len(self.custom_menu_choices) - 1

		elif sprites.player4.menu_down_press is True and sprites.player4.gamepad_config == False:
			if sprites.player4.menu_status == 'profile select':
				sprites.player4.profile_number += 1
				if sprites.player4.profile_number > len(options.profile_list) - 1:
					sprites.player4.profile_number = 0
			elif sprites.player4.menu_status == 'new profile':
				sprites.player4.text_number += 1
				sprites.player4.text_blink = 0
				if sprites.player4.text_number  > len(options.upper_case_list) - 1:
					sprites.player4.text_number = 0
			elif sprites.player4.menu_status == 'team select':
				sprites.player4.bandana.headband.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player4.menu_status == 'customize':
				sprites.player4.custom_menu_row += 1
				if sprites.player4.custom_menu_row > len(self.custom_menu_choices) - 1:
					sprites.player4.custom_menu_row = 0

		if sprites.player1.menu_left_press is True and sprites.player1.gamepad_config == False:
			if sprites.player1.menu_status == 'team select':
				sprites.player1.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player1.menu_status == 'new profile':
				if len(sprites.player1.profile_text) > 0:
					sprites.player1.profile_text = sprites.player1.profile_text[:-1]
					#sprites.player1.text_number = 0
			elif sprites.player1.menu_status == 'customize':
				if sprites.player1.custom_menu_row == 1:
					self.scroll_swag(sprites.player1, 'left')
				elif sprites.player1.custom_menu_row == 2:
					self.scroll_avatar(sprites.player1, 'left')


		elif sprites.player1.menu_right_press is True and sprites.player1.gamepad_config == False:
			if sprites.player1.menu_status == 'team select':
				sprites.player1.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player1.menu_status == 'new profile':
				if len(sprites.player1.profile_text) <= 7:
					if sprites.player1.text_case == 'lowercase':
						sprites.player1.profile_text += options.lower_case_list[sprites.player1.text_number]
					elif sprites.player1.text_case == 'uppercase':
						sprites.player1.profile_text += options.upper_case_list[sprites.player1.text_number]
					#sprites.player1.text_number = 0
			elif sprites.player1.menu_status == 'customize':
				if sprites.player1.custom_menu_row == 1:
					self.scroll_swag(sprites.player1, 'right')
				elif sprites.player1.custom_menu_row == 2:
					self.scroll_avatar(sprites.player1, 'right')

		if sprites.player2.menu_left_press is True and sprites.player2.gamepad_config == False:
			if sprites.player2.menu_status == 'team select':
				sprites.player2.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player2.menu_status == 'new profile':
				if len(sprites.player2.profile_text) > 0:
					sprites.player2.profile_text = sprites.player2.profile_text[:-1]
					#sprites.player2.text_number = 0
			elif sprites.player2.menu_status == 'customize':
				if sprites.player2.custom_menu_row == 1:
					self.scroll_swag(sprites.player2, 'left')
				elif sprites.player2.custom_menu_row == 2:
					self.scroll_avatar(sprites.player2, 'left')

		elif sprites.player2.menu_right_press is True and sprites.player2.gamepad_config == False:
			if sprites.player2.menu_status == 'team select':
				sprites.player2.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player2.menu_status == 'new profile':
				if len(sprites.player2.profile_text) <= 7:
					if sprites.player2.text_case == 'lowercase':
						sprites.player2.profile_text += options.lower_case_list[sprites.player2.text_number]
					elif sprites.player2.text_case == 'uppercase':
						sprites.player2.profile_text += options.upper_case_list[sprites.player2.text_number]
					#sprites.player2.text_number = 0
			elif sprites.player2.menu_status == 'customize':
				if sprites.player2.custom_menu_row == 1:
					self.scroll_swag(sprites.player2, 'right')
				elif sprites.player2.custom_menu_row == 2:
					self.scroll_avatar(sprites.player2, 'right')

		if sprites.player3.menu_left_press is True and sprites.player3.gamepad_config == False:
			if sprites.player3.menu_status == 'team select':
				sprites.player3.change_color('left', None)
				sounds.mixer.menu_move.play()
			elif sprites.player3.menu_status == 'new profile':
				if len(sprites.player3.profile_text) > 0:
					sprites.player3.profile_text = sprites.player3.profile_text[:-1]
					#sprites.player3.text_number = 0
			elif sprites.player3.menu_status == 'customize':
				if sprites.player3.custom_menu_row == 1:
					self.scroll_swag(sprites.player3, 'left')
				elif sprites.player3.custom_menu_row == 2:
					self.scroll_avatar(sprites.player3, 'left')

		elif sprites.player3.menu_right_press is True and sprites.player3.gamepad_config == False:
			if sprites.player3.menu_status == 'team select':
				sprites.player3.change_color('right', None)
				sounds.mixer.menu_move.play()
			elif sprites.player3.menu_status == 'new profile':
				if len(sprites.player3.profile_text) <= 7:
					if sprites.player3.text_case == 'lowercase':
						sprites.player3.profile_text += options.lower_case_list[sprites.player3.text_number]
					elif sprites.player3.text_case == 'uppercase':
						sprites.player3.profile_text += options.upper_case_list[sprites.player3.text_number]
					#sprites.player3.text_number = 0
			elif sprites.player3.menu_status == 'customize':
				if sprites.player3.custom_menu_row == 1:
					self.scroll_swag(sprites.player3, 'right')
				elif sprites.player3.custom_menu_row == 2:
					self.scroll_avatar(sprites.player3, 'right')

		if sprites.player4.menu_left_press is True and sprites.player4.gamepad_config == False:
			if sprites.player4.menu_status == 'team select':
				sprites.player4.change_color('left', None)
				sounds.mixer.menu_back.play()
			elif sprites.player4.menu_status == 'new profile':
				if len(sprites.player4.profile_text) > 0:
					sprites.player4.profile_text = sprites.player4.profile_text[:-1]
					#sprites.player4.text_number = 0
			elif sprites.player4.menu_status == 'customize':
				if sprites.player4.custom_menu_row == 1:
					self.scroll_swag(sprites.player4, 'left')
				elif sprites.player4.custom_menu_row == 2:
					self.scroll_avatar(sprites.player4, 'left')

		elif sprites.player4.menu_right_press is True and sprites.player4.gamepad_config == False:
			if sprites.player4.menu_status == 'team select':
				sprites.player4.change_color('right', None)
				sounds.mixer.menu_back.play()
			elif sprites.player4.menu_status == 'new profile':
				if len(sprites.player4.profile_text) <= 7:
					if sprites.player4.text_case == 'lowercase':
						sprites.player4.profile_text += options.lower_case_list[sprites.player4.text_number]
					elif sprites.player4.text_case == 'uppercase':
						sprites.player4.profile_text += options.upper_case_list[sprites.player4.text_number]
					#sprites.player4.text_number = 0
			elif sprites.player4.menu_status == 'customize':
				if sprites.player4.custom_menu_row == 1:
					self.scroll_swag(sprites.player4, 'right')
				elif sprites.player4.custom_menu_row == 2:
					self.scroll_avatar(sprites.player4, 'right')

		if sprites.player1.menu_back_press is True and sprites.player1.gamepad_config == False:
			sprites.player1.text_sprite.reset()
			if sprites.player1.menu_status == 'ready':
				sprites.player1.menu_status = 'team select'
				#sounds.mixer.menu_move.play()
			elif sprites.player1.menu_status == 'online select':
				sprites.player1.menu_status = 'team select'
				self.online_status = 'offline'
				self.error_timer = 0
			elif sprites.player1.menu_status == 'team select':
					if sprites.player1 in sprites.ninja_list:
						sprites.player1.menu_status = 'join'
						sprites.ninja_list.remove(sprites.player1)
						sprites.active_sprite_list.remove(sprites.player1)
						sprites.player_list.remove(sprites.player1)
						sprites.player1.activate_death_sprite('skull', sprites.player1)
						sprites.player1.lose()
						sounds.mixer.menu_move.play()
			elif sprites.player1.menu_status == 'join':
				options.game_state = 'main_menu'
				self.menu_created = False
					
			elif sprites.player1.menu_status == 'new profile':
				sprites.player1.menu_status = 'profile select'
				sprites.player1.text_sprite.reset()
			elif sprites.player1.menu_status == 'profile select':
				sprites.player1.menu_status = 'customize'
			elif sprites.player1.menu_status == 'customize':
				sprites.player1.menu_status = 'team select'

			elif sprites.player1.menu_status == 'match list':
				sprites.player1.menu_status = 'online select'
				self.online_status = 'offline'
				self.error_timer = 0

		if sprites.player2.menu_back_press is True and sprites.player2.gamepad_config == False:
			sprites.player2.text_sprite.reset()
			if sprites.player2.menu_status == 'ready':
				sprites.player2.menu_status = 'team select'
				sounds.mixer.menu_move.play()
			elif sprites.player2.menu_status == 'team select':
				self.remove_ninja(sprites.player2, online_trigger = True)
				'''
				sprites.player2.menu_status = 'join'
				sprites.ninja_list.remove(sprites.player2)
				sprites.active_sprite_list.remove(sprites.player2)
				sprites.player_list.remove(sprites.player2)
				sounds.mixer.menu_move.play()
				sprites.player2.activate_death_sprite('skull', sprites.player2)
				sprites.player2.lose()
				'''
					
			elif sprites.player2.menu_status == 'new profile':
				sprites.player2.menu_status = 'profile select'
				sprites.player2.text_sprite.reset()
			elif sprites.player2.menu_status == 'profile select':
				sprites.player2.menu_status = 'customize'
			elif sprites.player2.menu_status == 'customize':
				sprites.player2.menu_status = 'team select'

		if sprites.player3.menu_back_press is True and sprites.player3.gamepad_config == False:
			sprites.player3.text_sprite.reset()
			if sprites.player3.menu_status == 'ready':
				sprites.player3.menu_status = 'team select'
				sounds.mixer.menu_move.play()
			elif sprites.player3.menu_status == 'team select':
				if sprites.player3 in sprites.ninja_list:
					sprites.player3.menu_status = 'join'
					sprites.ninja_list.remove(sprites.player3)
					sprites.active_sprite_list.remove(sprites.player3)
					sprites.player_list.remove(sprites.player3)
					sounds.mixer.menu_move.play()
					sprites.player3.activate_death_sprite('skull', sprites.player3)
					sprites.player3.lose()
			elif sprites.player3.menu_status == 'new profile':
				sprites.player3.menu_status = 'profile select'
				sprites.player3.text_sprite.reset()
			elif sprites.player3.menu_status == 'profile select':
				sprites.player3.menu_status = 'customize'
			elif sprites.player3.menu_status == 'customize':
				sprites.player3.menu_status = 'team select'

		if sprites.player4.menu_back_press is True and sprites.player4.gamepad_config == False:
			sprites.player4.text_sprite.reset()
			if sprites.player4.menu_status == 'ready':
				sprites.player4.menu_status = 'team select'
				sounds.mixer.menu_move.play()
			elif sprites.player4.menu_status == 'team select':
				if sprites.player4 in sprites.ninja_list:
					sprites.player4.menu_status = 'join'
					sprites.ninja_list.remove(sprites.player4)
					sprites.active_sprite_list.remove(sprites.player4)
					sprites.player_list.remove(sprites.player4)
					sounds.mixer.menu_move.play()
					sprites.player4.activate_death_sprite('skull', sprites.player4)
					sprites.player4.lose()
			elif sprites.player4.menu_status == 'new profile':
				sprites.player4.menu_status = 'profile select'
				sprites.player4.text_sprite.reset()
			elif sprites.player4.menu_status == 'profile select':
				sprites.player4.menu_status = 'customize'
			elif sprites.player4.menu_status == 'customize':
				sprites.player4.menu_status = 'team select'

		ready_delay = False #creates one loop delay from ready, prevents messages being displayed too soon.
		if sprites.player1.menu_select_press is True and sprites.player1.gamepad_config == False:
			sprites.player1.text_sprite.reset()
			if sprites.player1 not in sprites.ninja_list and sprites.player1.spawn_sprite.status == 'idle':
				
				self.set_gamepad_layout(sprites.player1)
				if sprites.player1.bandana.headband.status == 'free':
					sprites.player1.bandana.crumble()
				sprites.player_list.add(sprites.player1)
				sprites.player1.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4) - 24 ), phase_in = True)



			if sprites.player1.menu_status == 'join':
				sprites.player1.menu_status = 'team select'
				sounds.mixer.menu_select.play()
				if self.check_taken(sprites.player1, sprites.player1.profile): #check if profile is taken. If so, switch to guest
					sprites.player1.profile = 'Player1'
			elif sprites.player1.menu_status == 'team select':
				sprites.player1.menu_status = 'ready'
				sounds.mixer.menu_select.play()
				ready_delay = True

			elif sprites.player1.menu_status == 'profile select':
				sounds.mixer.menu_select.play()
				if sprites.player1.profile_number == 0: #-New Profile-
					sprites.player1.menu_status = 'new profile'
					sprites.player1.profile_text = ''
					sprites.player1.text_case = 'uppercase'
					sprites.player1.text_number = 0
				else:
					if self.check_taken(sprites.player1, options.profile_list[sprites.player1.profile_number]):
						sprites.player1.text_sprite.activate('Profile in Use', options.RED_LIST[2], (sprites.player1.rect.centerx - 5, sprites.player1.rect.top - 10), 60)
					else:
						sprites.player1.profile = options.profile_list[sprites.player1.profile_number]
						sprites.player1.menu_status = 'customize'

			elif sprites.player1.menu_status == 'new profile':
					if sprites.player1.text_case == 'lowercase':
						name_text = sprites.player1.profile_text + options.lower_case_list[sprites.player1.text_number]
					elif sprites.player1.text_case == 'uppercase':
						name_text = sprites.player1.profile_text + options.upper_case_list[sprites.player1.text_number]
					if name_text in options.profile_list:
						sprites.player1.text_sprite.activate('Profile Name Taken', options.RED_LIST[2], (640 / 4,100), 60)
					elif name_text.lower() == 'ancalabro':
						sprites.player1.text_sprite.activate('You Are Not Worthy', options.RED_LIST[2], (640 / 4,100), 60)
					elif name_text not in (options.profile_list):
						sounds.mixer.menu_select.play()
						options.profile_list.append(name_text)
						data_manager.data_handler.user_profile_dict[name_text] = copy.deepcopy(data_manager.data_handler.base_profile)
						data_manager.data_handler.save_data()

						sprites.player1.menu_status = 'profile select'
						sprites.player1.profile_number = options.profile_list.index(name_text)
						sprites.player1.text_sprite.reset()
						
			elif sprites.player1.menu_status == 'customize':
				if sprites.player1.custom_menu_row == 0:
					sounds.mixer.menu_select.play()
					if sprites.player1 in controls.input_handler.gamepad_ninja_list:
						self.set_gamepad_layout(sprites.player1, custom=True)
					else:
						sprites.player1.text_sprite.activate('Gamepads Only', options.RED_LIST[2], (sprites.player1.rect.centerx,sprites.player1.rect.bottom + 42), 60)
				elif sprites.player1.custom_menu_row == 3:
					sounds.mixer.menu_select.play()
					sprites.player1.menu_status = 'profile select'

			elif sprites.player1.menu_status == 'online select':
				if client.online_handler.port_forward_working:
					self.online_status = 'port forward error'
					
				if self.online_selection == 0: #Host
					sounds.mixer.menu_select.play()
					sprites.player1.menu_status = 'team select'
					#self.online_status = 'online'

				elif self.online_selection == 1: #Join
					sounds.mixer.menu_select.play()
					#sprites.player1.menu_status = 'team select'
					#self.online_status = 'online'
					sprites.player1.menu_status = 'match list'


			elif sprites.player1.menu_status == 'online exit':
				if self.online_selection == 0: #EXIT

					sounds.mixer.menu_select.play()
					sprites.player1.menu_status = 'team select'
					self.online_status = 'offline'
					
					for ninja in sprites.player_list:
						if ninja.online_type == 'online':
							ninja.reset_name()
							ninja.online_type = 'local'
							ninja.menu_status = 'join'
							sprites.ninja_list.remove(ninja)
							sprites.active_sprite_list.remove(ninja)
							sprites.player_list.remove(ninja)
							sounds.mixer.menu_move.play()
							ninja.activate_death_sprite('skull', ninja)
							ninja.lose()

					
				elif self.online_selection == 1: #Return
					sounds.mixer.menu_select.play()
					sprites.player1.menu_status = 'team select'
					#self.online_status = 'online'
					#sprites.player1.menu_status = 'match list'
					#quick_match_thread = threading.Thread(target=client.online_handler.get_match_list, args=())
					#quick_match_thread.start()

			elif sprites.player1.menu_status == 'match list':
				try:
					

					
					
					sprites.player1.menu_status = 'team select'
					sounds.mixer.menu_select.play()

				except IndexError: #like, no matches!
					pass

			
			sprites.player1.direction = 'right'

			#first player only can start match. If online, only IF also the host.
			if ready_delay is False and sprites.player1.menu_status == 'ready':
				if len(sprites.ninja_list) > 1 or sprites.player2.spawn_sprite.status != 'idle' or sprites.player3.spawn_sprite.status != 'idle' or sprites.player4.spawn_sprite.status != 'idle':
					if all(sprite.menu_status == 'ready' for sprite in sprites.ninja_list) is False or sprites.player2.spawn_sprite.status != 'idle' or sprites.player3.spawn_sprite.status != 'idle' or sprites.player4.spawn_sprite.status != 'idle':
						sprites.player1.text_sprite.activate('Not All Players Are Ready.', options.RED_LIST[2], (sprites.player1.rect.centerx + 5, 10), 120)

				
				elif len(sprites.ninja_list) == 1:
					sprites.player1.text_sprite.activate('3 Practice Dummies Added!', options.RED_LIST[2], (320, 13), 120)
					sounds.mixer.menu_select.play()
					options.game_state = 'versus_level_selection'
					self.menu_created = False
					#Only One Player! Add Dummy Ninjas:
					if sprites.player1.color == options.ORANGE_LIST:
						dummy_color = options.GREY_LIST
					else:
						dummy_color = options.ORANGE_LIST

					for dummy in (sprites.player2, sprites.player3, sprites.player4):
						dummy.color = dummy_color
						dummy.dummy = True
						dummy.swag = 'None'
						dummy.set_avatar(avatar = 'Dummy')
						sprites.player_list.add(dummy)

			if ready_delay is False and len(sprites.ninja_list) > 1:
					if all(sprite.menu_status == 'ready' for sprite in sprites.ninja_list) is True:
						i = []
						for sprite in sprites.ninja_list:
							if sprite.color not in i:
								i.append(sprite.color)
							if len(i) > 1:
									sounds.mixer.menu_select.play()
									if options.game_mode == 'versus':
										options.game_state = 'versus_level_selection'
											
									elif options.game_mode == 'coop':
										options.game_state = 'coop_level_selection'
									elif options.game_mode == 'online':
										options.game_state = 'online_menu'
										#options.online = True #used to control main loop flow
									self.menu_created = False

									#sprites.transition_screen.fade(None, False, options.BLACK)

									break

						if len(i) <= 1:
							sprites.player1.text_sprite.activate('Two Teams/Colors Required.', options.RED_LIST[2], (sprites.player1.rect.centerx + 5, 10), 120)


		if sprites.player2.menu_select_press is True and sprites.player2.gamepad_config == False:
			sprites.player2.text_sprite.reset()
			if sprites.player2 not in sprites.ninja_list and sprites.player2.spawn_sprite.status == 'idle':
				self.set_gamepad_layout(sprites.player2)
				if sprites.player2.bandana.headband.status == 'free':
					sprites.player2.bandana.crumble()
				sprites.player_list.add(sprites.player2)
				sprites.player2.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4) - 24 ), phase_in = True)


				#sprites.ninja_list.add(sprites.player2)
				#sprites.active_sprite_list.add(sprites.player2)
				#sprites.active_sprite_list.change_layer(sprites.player2, 1)
				#sprites.player_list.add(sprites.player2)
				#sprites.player2.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4) - 24 ))
				#make fade in
				#sprites.player2.visible = 0
				#sprites.player2.visible_timer = 10
				#sprites.player2.visible_switch = True
				#sprites.player2.bandana.flip_visible('invisible')

			if sprites.player2.menu_status == 'join':
				sprites.player2.menu_status = 'team select'
				sounds.mixer.menu_select.play()
				if self.check_taken(sprites.player2, sprites.player2.profile): #check if profile is taken. If so, switch to guest
					sprites.player2.profile = 'Player2'


			elif sprites.player2.menu_status == 'team select':
				sprites.player2.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			elif sprites.player2.menu_status == 'profile select':
				sounds.mixer.menu_select.play()
				if sprites.player2.profile_number == 0: #-New Profile-
					sprites.player2.menu_status = 'new profile'
					sprites.player2.profile_text = ''
					sprites.player2.text_case = 'uppercase'
					sprites.player2.text_number = 0
				else:
					if self.check_taken(sprites.player2, options.profile_list[sprites.player2.profile_number]):
						sprites.player2.text_sprite.activate('Profile in Use', options.RED_LIST[2], (sprites.player2.rect.centerx + 5, sprites.player2.rect.top - 10), 60)
					else:
						sprites.player2.profile = options.profile_list[sprites.player2.profile_number]
						sprites.player2.menu_status = 'customize'

			elif sprites.player2.menu_status == 'new profile':
					if sprites.player2.text_case == 'lowercase':
						name_text = sprites.player2.profile_text + options.lower_case_list[sprites.player2.text_number]
					elif sprites.player2.text_case == 'uppercase':
						name_text = sprites.player2.profile_text + options.upper_case_list[sprites.player2.text_number]
					if name_text in options.profile_list:
						sprites.player2.text_sprite.activate('Profile Name Taken', options.RED_LIST[2], (640 / 4 * 3,100), 60)
					elif name_text.lower() == 'ancalabro':
						sprites.player2.text_sprite.activate('You Are Not Worthy', options.RED_LIST[2], (640 / 4 * 3,100), 60)
					elif name_text not in (options.profile_list):
						sounds.mixer.menu_select.play()
						options.profile_list.append(name_text)
						data_manager.data_handler.user_profile_dict[name_text] = copy.deepcopy(data_manager.data_handler.base_profile)
						data_manager.data_handler.save_data()

						sprites.player2.menu_status = 'profile select'
						sprites.player2.profile_number = options.profile_list.index(name_text)
						sprites.player2.text_sprite.reset()

			elif sprites.player2.menu_status == 'customize':
				if sprites.player2.custom_menu_row == 0:
					sounds.mixer.menu_select.play()
					if sprites.player2 in controls.input_handler.gamepad_ninja_list:
						self.set_gamepad_layout(sprites.player2, custom=True)
					else:
						sprites.player2.text_sprite.activate('Gamepads Only', options.RED_LIST[2], (sprites.player2.rect.centerx,sprites.player2.rect.bottom + 42), 60)

				elif sprites.player2.custom_menu_row == 3:
					sounds.mixer.menu_select.play()
					sprites.player2.menu_status = 'profile select'

			sprites.player2.direction = 'left'



		if sprites.player3.menu_select_press is True and sprites.player3.gamepad_config == False:
			sprites.player3.text_sprite.reset()
			if sprites.player3 not in sprites.ninja_list and sprites.player3.spawn_sprite.status == 'idle':
				self.set_gamepad_layout(sprites.player3)
				if sprites.player3.bandana.headband.status == 'free':
					sprites.player3.bandana.crumble()
				sprites.player_list.add(sprites.player3)
				sprites.player3.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4 * 3) - 24 ), phase_in = True)
				'''
				sprites.ninja_list.add(sprites.player3)
				sprites.active_sprite_list.add(sprites.player3)
				sprites.active_sprite_list.change_layer(sprites.player3, 1)
				sprites.player_list.add(sprites.player3)
				sprites.player3.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4 * 3) - 24 ))
				#make fade in
				sprites.player3.visible = 0
				sprites.player3.visible_timer = 10
				sprites.player3.visible_switch = True
				sprites.player3.bandana.flip_visible('invisible')
				'''
			if sprites.player3.menu_status == 'join':
				sprites.player3.menu_status = 'team select'
				if self.check_taken(sprites.player3, sprites.player3.profile): #check if profile is taken. If so, switch to guest
					sprites.player3.profile = 'Player3'
				sounds.mixer.menu_select.play()
			elif sprites.player3.menu_status == 'team select':
				sprites.player3.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			elif sprites.player3.menu_status == 'profile select':
				sounds.mixer.menu_select.play()
				if sprites.player3.profile_number == 0: #-New Profile-
					sprites.player3.menu_status = 'new profile'
					sprites.player3.profile_text = ''
					sprites.player3.text_case = 'uppercase'
					sprites.player3.text_number = 0
				else:
					if self.check_taken(sprites.player3, options.profile_list[sprites.player3.profile_number]):
						sprites.player3.text_sprite.activate('Profile in Use', options.RED_LIST[2], (sprites.player3.rect.centerx - 5, sprites.player3.rect.top - 10), 60)
					else:
						sprites.player3.profile = options.profile_list[sprites.player3.profile_number]
						sprites.player3.menu_status = 'customize'


			elif sprites.player3.menu_status == 'new profile':
					if sprites.player3.text_case == 'lowercase':
						name_text = sprites.player3.profile_text + options.lower_case_list[sprites.player3.text_number]
					elif sprites.player3.text_case == 'uppercase':
						name_text = sprites.player3.profile_text + options.upper_case_list[sprites.player3.text_number]
					if name_text in options.profile_list:
						sprites.player3.text_sprite.activate('Profile Name Taken', options.RED_LIST[2], (640 / 4 * 3,280), 60)
					elif name_text.lower() == 'ancalabro':
						sprites.player3.text_sprite.activate('You Are Not Worthy', options.RED_LIST[2], (640 / 4 * 3,280), 60)
					elif name_text not in (options.profile_list):
						sounds.mixer.menu_select.play()
						options.profile_list.append(name_text)
						data_manager.data_handler.user_profile_dict[name_text] = copy.deepcopy(data_manager.data_handler.base_profile)
						data_manager.data_handler.save_data()

						sprites.player3.menu_status = 'profile select'
						sprites.player3.profile_number = options.profile_list.index(name_text)
						sprites.player3.text_sprite.reset()

			elif sprites.player3.menu_status == 'customize':
				if sprites.player3.custom_menu_row == 0:
					sounds.mixer.menu_select.play()
					if sprites.player3 in controls.input_handler.gamepad_ninja_list:
						self.set_gamepad_layout(sprites.player3, custom=True)
					else:
						sprites.player3.text_sprite.activate('Gamepads Only', options.RED_LIST[2], (sprites.player3.rect.centerx,sprites.player3.rect.bottom + 42), 60)
				elif sprites.player3.custom_menu_row == 3:
					sounds.mixer.menu_select.play()
					sprites.player3.menu_status = 'profile select'

			sprites.player3.direction = 'right'

		if sprites.player4.menu_select_press is True and sprites.player4.gamepad_config == False:
			sprites.player4.text_sprite.reset()
			self.set_gamepad_layout(sprites.player4)
			if sprites.player4 not in sprites.ninja_list and sprites.player4.spawn_sprite.status == 'idle':
				if sprites.player4.bandana.headband.status == 'free':
					sprites.player4.bandana.crumble()
				sprites.player_list.add(sprites.player4)
				sprites.player4.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4 * 3) - 24 ), phase_in = True)

				'''
				sprites.ninja_list.add(sprites.player4)
				sprites.active_sprite_list.add(sprites.player4)
				sprites.active_sprite_list.change_layer(sprites.player4, 1)
				sprites.player_list.add(sprites.player4)
				sprites.player4.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4 * 3) - 24 ))
				#make fade in
				sprites.player4.visible = 0
				sprites.player4.visible_timer = 10
				sprites.player4.visible_switch = True
				sprites.player4.bandana.flip_visible('invisible')
				'''

			if sprites.player4.menu_status == 'join':
				sprites.player4.menu_status = 'team select'
				sounds.mixer.menu_select.play()
				if self.check_taken(sprites.player4, sprites.player4.profile): #check if profile is taken. If so, switch to guest
					sprites.player4.profile = 'Player4'
			elif sprites.player4.menu_status == 'team select':
				sprites.player4.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			elif sprites.player4.menu_status == 'profile select':
				sounds.mixer.menu_select.play()
				if sprites.player4.profile_number == 0: #-New Profile-
					sprites.player4.menu_status = 'new profile'
					sprites.player4.profile_text = ''
					sprites.player4.text_case = 'uppercase'
					sprites.player4.text_number = 0
				else:
					if self.check_taken(sprites.player4, options.profile_list[sprites.player4.profile_number]):
						sprites.player4.text_sprite.activate('Profile in Use', options.RED_LIST[2], (sprites.player4.rect.centerx + 5, sprites.player4.rect.top - 10), 60)
					else:
						sprites.player4.profile = options.profile_list[sprites.player4.profile_number]
						sprites.player4.menu_status = 'customize'

			elif sprites.player4.menu_status == 'new profile':
					if sprites.player4.text_case == 'lowercase':
						name_text = sprites.player4.profile_text + options.lower_case_list[sprites.player4.text_number]
					elif sprites.player4.text_case == 'uppercase':
						name_text = sprites.player4.profile_text + options.upper_case_list[sprites.player4.text_number]
					if name_text in options.profile_list:
						sprites.player4.text_sprite.activate('Profile Name Taken', options.RED_LIST[2], (640 / 4 * 3,280), 60)
					elif name_text.lower() == 'ancalabro':
						sprites.player4.text_sprite.activate('You Are Not Worthy', options.RED_LIST[2], (640 / 4 * 3,280), 60)
					elif name_text not in (options.profile_list):
						sounds.mixer.menu_select.play()
						options.profile_list.append(name_text)
						data_manager.data_handler.user_profile_dict[name_text] = copy.deepcopy(data_manager.data_handler.base_profile)
						data_manager.data_handler.save_data()

						sprites.player4.menu_status = 'profile select'
						sprites.player4.profile_number = options.profile_list.index(name_text)
						sprites.player4.text_sprite.reset()

			elif sprites.player4.menu_status == 'customize':
				if sprites.player4.custom_menu_row == 0:
					sounds.mixer.menu_select.play()
					if sprites.player4 in controls.input_handler.gamepad_ninja_list:
						self.set_gamepad_layout(sprites.player4, custom=True)
					else:
						sprites.player4.text_sprite.activate('Gamepads Only', options.RED_LIST[2], (sprites.player4.rect.centerx,sprites.player4.rect.bottom + 42), 60)
					
				elif sprites.player4.custom_menu_row == 3:
					sounds.mixer.menu_select.play()
					sprites.player4.menu_status = 'profile select'

			sprites.player4.direction = 'left'

		if sprites.player1.menu_x_press is True and sprites.player1.gamepad_config == False:
			sprites.player1.text_sprite.reset()
			if sprites.player1.menu_status == 'team select':
				sounds.mixer.menu_select.play()
				sprites.player1.menu_status = 'customize'
					


		if sprites.player2.menu_x_press is True and sprites.player2.gamepad_config == False:
			sprites.player2.text_sprite.reset()
			if sprites.player2.menu_status == 'team select':
				sounds.mixer.menu_select.play()
				sprites.player2.menu_status = 'customize'
					

		if sprites.player3.menu_x_press is True and sprites.player3.gamepad_config == False:
			sprites.player3.text_sprite.reset()
			if sprites.player3.menu_status == 'team select':
				sounds.mixer.menu_select.play()
				sprites.player3.menu_status = 'customize'

					
		if sprites.player4.menu_x_press is True and sprites.player4.gamepad_config == False:
			sprites.player4.text_sprite.reset()
			if sprites.player4.menu_status == 'team select':
				sounds.mixer.menu_select.play()
				sprites.player4.menu_status = 'customize'
					

		if controls.input_handler.press1 is True:
			if sprites.player1 not in sprites.ninja_list:
				sprites.ninja_list.add(sprites.player1)
				sprites.active_sprite_list.add(sprites.player1)
				sprites.active_sprite_list.change_layer(sprites.player1, 1)
				sprites.player_list.add(sprites.player1)
				sprites.player1.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4) - 24 ))
			if sprites.player1.menu_status == 'join':
				sprites.player1.menu_status = 'team select'
				sounds.mixer.menu_select.play()
			elif sprites.player1.menu_status == 'team select':
				sprites.player1.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			sprites.player1.direction = 'right'

		if controls.input_handler.press2 is True:
			if sprites.player2 not in sprites.ninja_list:
				sprites.ninja_list.add(sprites.player2)
				sprites.active_sprite_list.add(sprites.player2)
				sprites.active_sprite_list.change_layer(sprites.player2, 1)
				sprites.player_list.add(sprites.player2)
				sprites.player2.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4) - 24 ))
			if sprites.player2.menu_status == 'join':
				sprites.player2.menu_status = 'team select'
				sounds.mixer.menu_select.play()
			elif sprites.player2.menu_status == 'team select':
				sprites.player2.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			sprites.player2.direction = 'left'

		if controls.input_handler.press3 is True:
			if sprites.player3 not in sprites.ninja_list:
				sprites.ninja_list.add(sprites.player3)
				sprites.active_sprite_list.add(sprites.player3)
				sprites.active_sprite_list.change_layer(sprites.player3, 1)
				sprites.player_list.add(sprites.player3)
				sprites.player3.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4 * 3) - 24 ))
			if sprites.player3.menu_status == 'join':
				sprites.player3.menu_status = 'team select'
				sounds.mixer.menu_select.play()
			elif sprites.player3.menu_status == 'team select':
				sprites.player3.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			sprites.player3.direction = 'right'

		if controls.input_handler.press4 is True:
			if sprites.player4 not in sprites.ninja_list:
				sprites.ninja_list.add(sprites.player4)
				sprites.active_sprite_list.add(sprites.player4)
				sprites.active_sprite_list.change_layer(sprites.player4, 1)
				sprites.player_list.add(sprites.player4)
				sprites.player4.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4 * 3) - 24 ))
			if sprites.player4.menu_status == 'join':
				sprites.player4.menu_status = 'team select'
				sounds.mixer.menu_select.play()
			elif sprites.player4.menu_status == 'team select':
				sprites.player4.menu_status = 'ready'
				sounds.mixer.menu_select.play()
			sprites.player4.direction = 'left'

		if sprites.player1.menu_y_press is True and sprites.player1.gamepad_config == False:
			sprites.player1.text_sprite.reset()
			if sprites.player1.menu_status == 'team select':
				sounds.mixer.menu_select.play()
				message = 'To enjoy online play, please download the most current version. Thanks for playing!'
				choice_handler.activate([sprites.player1], message, next_game_state = 'player_select', signed = True)

			
			elif sprites.player1.menu_status == 'new profile':
				sounds.mixer.menu_select.play()
				if sprites.player1.text_case == 'lowercase':
					sprites.player1.text_case = 'uppercase'
				else:
					sprites.player1.text_case = 'lowercase'

		if sprites.player2.menu_y_press is True and sprites.player2.gamepad_config == False:
			sprites.player2.text_sprite.reset()
			#if sprites.player2.menu_status == 'team select':
			#	sprites.player2.menu_status = 'profile select'
			if sprites.player2.menu_status == 'new profile':
				sounds.mixer.menu_select.play()
				if sprites.player2.text_case == 'lowercase':
					sprites.player2.text_case = 'uppercase'
				else:
					sprites.player2.text_case = 'lowercase'

		if sprites.player3.menu_y_press is True and sprites.player3.gamepad_config == False:
			sprites.player3.text_sprite.reset()
			#if sprites.player3.menu_status == 'team select':
			#	sprites.player3.menu_status = 'profile select'
			if sprites.player3.menu_status == 'new profile':
				sounds.mixer.menu_select.play()
				if sprites.player3.text_case == 'lowercase':
					sprites.player3.text_case = 'uppercase'
				else:
					sprites.player3.text_case = 'lowercase'

		if sprites.player4.menu_y_press is True and sprites.player4.gamepad_config == False:
			sprites.player4.text_sprite.reset()
			#if sprites.player4.menu_status == 'team select':
			#	sprites.player4.menu_status = 'profile select'
			if sprites.player4.menu_status == 'new profile':
				sounds.mixer.menu_select.play()
				if sprites.player4.text_case == 'lowercase':
					sprites.player4.text_case = 'uppercase'
				else:
					sprites.player4.text_case = 'lowercase'


		JoinText = font_16.render('Press A to Join', 0,(options.WHITE))
		ColorText = font_16.render('Select Team', 0, (options.WHITE))
		ReadyText = font_30.render('-Ready-', 0, (options.WHITE))

		if sprites.player1.menu_status == 'join':
			P1_Text = JoinText
		elif sprites.player1.menu_status in ('team select', 'profile select', 'new profile', 'customize', 'online select', 'online exit', 'match list'):
			P1_Text = ColorText
		elif sprites.player1.menu_status == 'ready':
			P1_Text = ReadyText

			if sprites.player1.spawn_sprite.status == 'idle':
				x_offset = 0
				y_offset = 0
				StartText = font_16.render('Press A to Start Match', 0,(options.WHITE))
				self.text_screen.image.blit(StartText, ((sprites.screen.get_width() / 4) - (StartText.get_width() / 2) - x_offset, ((sprites.screen.get_height() / 4) + 30 - y_offset)))

				if options.control_preferences['player1'] == 'keyboard':
					select_pic = controls.input_handler.button_keyboard_z
				else:
					select_pic = sprites.player1.gamepad_layout['button_jump_image']
				self.text_screen.image.blit(select_pic, ((sprites.screen.get_width() / 4) - (StartText.get_width() / 2) - x_offset + 45, ((sprites.screen.get_height() / 4) + 30 - y_offset - 2)))


		if sprites.player2.menu_status == 'join':
			P2_Text = JoinText
		elif sprites.player2.menu_status in ('team select', 'profile select', 'new profile', 'customize'):
			P2_Text = ColorText
		elif sprites.player2.menu_status == 'ready':
			P2_Text = ReadyText

		if sprites.player3.menu_status == 'join':
			P3_Text = JoinText
		elif sprites.player3.menu_status in ('team select', 'profile select', 'new profile', 'customize'):
			P3_Text = ColorText
		elif sprites.player3.menu_status == 'ready':
			P3_Text = ReadyText

		if sprites.player4.menu_status == 'join':
			P4_Text = JoinText
		elif sprites.player4.menu_status in ('team select', 'profile select', 'new profile', 'customize'):
			P4_Text = ColorText
		elif sprites.player4.menu_status == 'ready':
			P4_Text = ReadyText
		
		#PRint Text
		if sprites.player1.menu_status != 'ready':
			self.text_screen.image.blit(P1_Text, ((sprites.screen.get_width() / 4) - (P1_Text.get_width() / 2), ((sprites.screen.get_height() / 4) + 20)))
		self.text_screen.image.blit(P2_Text, ((sprites.screen.get_width() / 4 * 3) - (P2_Text.get_width() / 2), ((sprites.screen.get_height() / 4) + 20)))
		self.text_screen.image.blit(P3_Text, ((sprites.screen.get_width() / 4) - (P3_Text.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20)))
		self.text_screen.image.blit(P4_Text, ((sprites.screen.get_width() / 4 * 3) - (P4_Text.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20)))

		#Add 'Button Pics'
		#Get offset for A button.
		x = 0
		for item in font_16.metrics('Press '):
			x += 8
		a_pic = sprites.level_sheet.getImage(0,228,17,17)
		c_key_pic = controls.input_handler.button_keyboard_c
		z_key_pic = controls.input_handler.button_keyboard_z #sprites.level_sheet.getImage(0,282,17,17)
		x_offset = ((a_pic.get_width() - 8) / 2) - 1
		y_offset = (a_pic.get_height() - 16) / 2

		#get other button pics:
		y_pic = controls.input_handler.p1_gamepad['button_jump_image'] #sprites.level_sheet.getImage(0,210,17,17)
		y_key_pic = controls.input_handler.button_keyboard_y #sprites.level_sheet.getImage(18,300,17,17)
		#self.text_screen.image.blit(y_pic,(320 - (options_text.get_width() / 2) + x - x_offset,5 - y_offset))

		if sprites.player1.menu_status == 'join':
			if sprites.player1 == controls.input_handler.gamepad1_ninja:
				temp_pic = sprites.player1.gamepad_layout['button_jump_image']
			else:
				temp_pic = z_key_pic
			#control_preferences = {'player1' : 'gamepad', 'player2' : 'gamepad'}
			self.text_screen.image.blit(temp_pic, ((sprites.screen.get_width() / 4) - (P1_Text.get_width() / 2) - x_offset + x, ((sprites.screen.get_height() / 4) + 20 - y_offset)))
		if sprites.player2.menu_status == 'join':
			if sprites.player2 in (controls.input_handler.gamepad1_ninja, controls.input_handler.gamepad2_ninja):
				temp_pic = sprites.player2.gamepad_layout['button_jump_image']
			else:
				temp_pic = z_key_pic
			self.text_screen.image.blit(temp_pic, ((sprites.screen.get_width() / 4 * 3) - (P2_Text.get_width() / 2) - x_offset + x, ((sprites.screen.get_height() / 4) + 20 - y_offset)))
		if sprites.player3.menu_status == 'join':
			a_pic = sprites.player3.gamepad_layout['button_jump_image']
			self.text_screen.image.blit(a_pic, ((sprites.screen.get_width() / 4) - (P3_Text.get_width() / 2) - x_offset + x, ((sprites.screen.get_height() / 4 * 3) + 20 - y_offset)))
		if sprites.player4.menu_status == 'join':
			a_pic = sprites.player4.gamepad_layout['button_jump_image']
			self.text_screen.image.blit(a_pic, ((sprites.screen.get_width() / 4 * 3) - (P4_Text.get_width() / 2) - x_offset + x, ((sprites.screen.get_height() / 4 * 3) + 20 - y_offset)))


		if sprites.player1.menu_status != 'join':
			ProfileText = font_16.render(sprites.player1.profile, 0,(options.WHITE))
			self.text_screen.image.blit(ProfileText, ((sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) - 70)))
			if sprites.player1.menu_status == 'team select':
				if self.online_status == 'online':
					online_text = 'Port Forwarding Error.'
					ProfileText = font_12.render(online_text, 0,(options.WHITE))
					self.text_screen.image.blit(ProfileText, ((sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), 1))
				elif self.online_status == 'online':
					pass

				elif self.online_status in ('error', 'port forward error'):
					pass




				#if client.online_handler.web_address != None and client.online_handler.client_ip != None and options.current_version is True:
				ProfileText = font_16.render('Y : Online', 0,(options.WHITE))
				self.text_screen.image.blit(ProfileText, (100 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21)))
				
				ProfileText = font_16.render('X : Customize', 0,(options.WHITE))
				self.text_screen.image.blit(ProfileText, (-100 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21)))
				
				if sprites.player1 == controls.input_handler.gamepad1_ninja:
					temp_pic = sprites.player1.gamepad_layout['button_menu_image']
					other_temp_pic = sprites.player1.gamepad_layout['button_item_image']
				else:
					temp_pic = y_key_pic
					other_temp_pic = c_key_pic
				
				#if client.online_handler.web_address != None and client.online_handler.client_ip != None and options.current_version is True:
				self.text_screen.image.blit(temp_pic, (108 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21 - y_offset)))
				self.text_screen.image.blit(other_temp_pic, (-103 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21 - y_offset)))
		if sprites.player2.menu_status != 'join':
			ProfileText = font_16.render(sprites.player2.profile, 0,(options.WHITE))
			self.text_screen.image.blit(ProfileText, ((sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) - 70)))
			if sprites.player2.menu_status == 'team select':
				#ProfileText = font_16.render('Y : Profile', 0,(options.WHITE))
				#self.text_screen.image.blit(ProfileText, (110 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21)))
				ProfileText = font_16.render('X : Customize', 0,(options.WHITE))
				self.text_screen.image.blit(ProfileText, (-90 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21)))
				
				if sprites.player2 in (controls.input_handler.gamepad1_ninja, controls.input_handler.gamepad2_ninja):
					#temp_pic = sprites.player2.gamepad_layout['button_menu_image']
					other_temp_pic = sprites.player2.gamepad_layout['button_item_image']
				else:
					#temp_pic = y_key_pic
					other_temp_pic = c_key_pic
				#self.text_screen.image.blit(temp_pic, (115 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21 - y_offset)))
				self.text_screen.image.blit(other_temp_pic, (-93 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4) + 20 + 21 - y_offset)))
		if sprites.player3.menu_status != 'join':
			ProfileText = font_16.render(sprites.player3.profile, 0,(options.WHITE))
			self.text_screen.image.blit(ProfileText, ((sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) - 70)))
			if sprites.player3.menu_status == 'team select':
				#ProfileText = font_16.render('Y : Profile', 0,(options.WHITE))
				#self.text_screen.image.blit(ProfileText, (100 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20)))
				ProfileText = font_16.render('X : Customize', 0,(options.WHITE))
				self.text_screen.image.blit(ProfileText, (-100 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20)))
				

				#y_pic = sprites.player3.gamepad_layout['button_menu_image']
				x_pic = sprites.player3.gamepad_layout['button_item_image']
				#self.text_screen.image.blit(y_pic, (105 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20 - y_offset)))
				self.text_screen.image.blit(x_pic, (-103 + (sprites.screen.get_width() / 4) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20 - y_offset)))
				
		if sprites.player4.menu_status != 'join':
			ProfileText = font_16.render(sprites.player4.profile, 0,(options.WHITE))
			self.text_screen.image.blit(ProfileText, ((sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) - 70)))
			if sprites.player4.menu_status == 'team select':
				#ProfileText = font_16.render('Y : Profile', 0,(options.WHITE))
				#self.text_screen.image.blit(ProfileText, (110 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20)))
				ProfileText = font_16.render('X : Customize', 0,(options.WHITE))
				self.text_screen.image.blit(ProfileText, (-90 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20)))
				
				#y_pic = sprites.player4.gamepad_layout['button_menu_image']
				x_pic = sprites.player4.gamepad_layout['button_item_image']
				#self.text_screen.image.blit(y_pic, (115 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20 - y_offset)))
				self.text_screen.image.blit(x_pic, (-93 + (sprites.screen.get_width() / 4 * 3) - (ProfileText.get_width() / 2), ((sprites.screen.get_height() / 4 * 3) + 20 + 20 - y_offset)))


		if sprites.player1.menu_status == 'profile select':
			image = self.profile_select_image(sprites.player1,(5,5))
			self.text_screen.image.blit(image,(5,5))
		elif sprites.player1.menu_status == 'new profile':
			image = self.new_profile_image(sprites.player1,(5,5))
			self.text_screen.image.blit(image,(5,5))
		elif sprites.player1.menu_status == 'customize':
			image = self.customize(sprites.player1,(5,5))
			self.text_screen.image.blit(image,(5,5))
		elif sprites.player1.menu_status == 'online select':
			image = self.online_menu(sprites.player1,(5,5))
			self.text_screen.image.blit(image,(5,5))
		elif sprites.player1.menu_status == 'online exit':
			image = self.online_exit_menu(sprites.player1,(5,5))
			self.text_screen.image.blit(image,(5,5))
		elif sprites.player1.menu_status == 'match list':
			image = self.match_list_menu(sprites.player1,(5,5))
			self.text_screen.image.blit(image,(5,5))


		if sprites.player2.menu_status == 'profile select':
			image = self.profile_select_image(sprites.player2,(320 + 12 + 5,5))
			self.text_screen.image.blit(image,(320 + 12 + 5,5))
		elif sprites.player2.menu_status == 'new profile':
			image = self.new_profile_image(sprites.player2,(320 + 12 + 5,5))
			self.text_screen.image.blit(image,(320 + 12 + 5,5))
		elif sprites.player2.menu_status == 'customize':
			image = self.customize(sprites.player2,(320 + 12 + 5,5))
			self.text_screen.image.blit(image,(320 + 12 + 5,5))

		if sprites.player3.menu_status == 'profile select':
			image = self.profile_select_image(sprites.player3,(5,185))
			self.text_screen.image.blit(image,(5,185))
		elif sprites.player3.menu_status == 'new profile':
			image = self.new_profile_image(sprites.player3,(5,185))
			self.text_screen.image.blit(image,(5,185))
		elif sprites.player3.menu_status == 'customize':
			image = self.customize(sprites.player3,(5,185))
			self.text_screen.image.blit(image,(5,185))


		if sprites.player4.menu_status == 'profile select':
			image = self.profile_select_image(sprites.player4,(325 + 12,185))
			self.text_screen.image.blit(image,(325 + 12,185))
		elif sprites.player4.menu_status == 'new profile':
			image = self.new_profile_image(sprites.player4,(325 + 12,185))
			self.text_screen.image.blit(image,(325 + 12,185))
		elif sprites.player4.menu_status == 'customize':
			image = self.customize(sprites.player4,(325 + 12,185))
			self.text_screen.image.blit(image,(325 + 12,185))

		self.update_arrows()

		#draw things here
		i = 0
		while i < 60:
			if i < 30:
				sprites.screenshot_handler.update()
			sprites.menu_sprite_list.update()
			level.Collision_Check() #Handles Non-Tile collision checks
			sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
			sprites.tile_list.update()
			sprites.level_objects.update()
			sprites.item_effects.update()
			sprites.background_objects.update()
			sprites.visual_effects.update()
			sprites.screen_objects.update()
			i += options.current_fps

		

		sprites.active_sprite_list.draw(sprites.screen)

		for bar in  intro_handler.matrix_bar_list:
			bar.update()
			for digit in bar.digit_list:
				digit.update(None,None)


	def remove_ninja(self, ninja, online_trigger = False):
			if ninja in sprites.ninja_list:
				ninja.menu_status = 'join'
				sprites.ninja_list.remove(ninja)
				sprites.active_sprite_list.remove(ninja)
				sprites.player_list.remove(ninja)
				sounds.mixer.menu_move.play()
				ninja.activate_death_sprite('skull', ninja)
				ninja.lose()


	def set_gamepad_layout(self, ninja, custom=False):
		map_attempt = False
		if controls.input_handler.gamepad1_ninja == ninja:
			gamepad = controls.input_handler.p1_gamepad
			pad_number = 0
			map_attempt = True
		elif controls.input_handler.gamepad2_ninja == ninja:
			gamepad = controls.input_handler.p2_gamepad
			pad_number = 1
			map_attempt = True
		elif controls.input_handler.gamepad3_ninja == ninja:
			gamepad = controls.input_handler.p3_gamepad
			pad_number = 2
			map_attempt = True
		elif controls.input_handler.gamepad4_ninja == ninja:
			gamepad = controls.input_handler.p4_gamepad
			pad_number = 3
			map_attempt = True

		if map_attempt == True:
			if ninja == sprites.player1:
				centerxy = (160,90)
			elif ninja == sprites.player2:
				centerxy = (480,90)
			elif ninja == sprites.player3:
				centerxy = (160,270)
			elif ninja == sprites.player4:
				centerxy = (480,270)

			if len(controls.input_handler.gamepads) > pad_number:
				controls.input_handler.reset_menu_controls()
				
				try:
					gamepad = data_manager.data_handler.gamepad_layout_dict[controls.input_handler.gamepads[pad_number].get_name()].copy()
					controls.input_handler.get_images(gamepad)
				except:
					gamepad_name = controls.input_handler.gamepads[pad_number].get_name()
					if controls.input_handler.os in ('Windows', 'Linux'):
						customize = True
						for text in ('Logitech', 'F710', 'F310', 'logitech', 'xbox', 'XBOX', 'Xbox'):
							if text in gamepad_name:
								#if gamepad_name in ('Logitech', 'logitech', 'xbox', 'XBOX', 'Xbox'):
								gamepad = data_manager.data_handler.gamepad_layout_dict['xbox'].copy()
								data_manager.data_handler.gamepad_layout_dict[gamepad_name] = gamepad.copy()
								controls.input_handler.get_images(gamepad)
								customize = False
								break
						if customize is True:
							gamepad_customizer = controls.Gamepad_Customizer(controls.input_handler, ninja, centerxy, controls.input_handler.gamepads[pad_number], gamepad)


					elif controls.input_handler.os == 'Darwin':
						if 'Logitech' in gamepad_name:
							gamepad = data_manager.data_handler.gamepad_layout_dict['mac_log'].copy()
							data_manager.data_handler.gamepad_layout_dict[gamepad_name] = gamepad.copy()
							controls.input_handler.get_images(gamepad)
						elif 'Playstation' in gamepad_name or 'playstation' in gamepad_name:
							gamepad = data_manager.data_handler.gamepad_layout_dict['mac_ps'].copy()
							data_manager.data_handler.gamepad_layout_dict[gamepad_name] = gamepad.copy()
							controls.input_handler.get_images(gamepad)
						else:
							gamepad_customizer = controls.Gamepad_Customizer(controls.input_handler, ninja, centerxy, controls.input_handler.gamepads[pad_number], gamepad)
					else:
						gamepad_customizer = controls.Gamepad_Customizer(controls.input_handler, ninja, centerxy, controls.input_handler.gamepads[pad_number], gamepad)


		if custom is True:
			gamepad_customizer = controls.Gamepad_Customizer(controls.input_handler, ninja, centerxy, controls.input_handler.gamepads[pad_number], gamepad, custom=True)

	def scroll_swag(self, ninja, direction):
		swag_list = data_manager.data_handler.user_profile_dict[ninja.profile]['Swag']

		current_position = swag_list.index(ninja.swag)

		if direction == 'left':
			current_position -= 1
			if current_position < 0:
				current_position = len(swag_list) - 1
		elif direction == 'right':
			current_position += 1
			if current_position > len(swag_list) - 1:
				current_position = 0

		ninja.swag = swag_list[current_position]
		ninja.bandana.kill()
		ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.color)

		#Bandanas parts currently removed in ROPE PHYSICS.

	def scroll_avatar(self, ninja, direction):
		avatar_list = data_manager.data_handler.user_profile_dict[ninja.profile]['Avatar']

		current_position = avatar_list.index(ninja.avatar)

		if direction == 'left':
			current_position -= 1
			if current_position < 0:
				current_position = len(avatar_list) - 1
		elif direction == 'right':
			current_position += 1
			if current_position > len(avatar_list) - 1:
				current_position = 0

		ninja.avatar = avatar_list[current_position]

		ninja.set_avatar()


		#moved to within the Ninja class
		'''
		if ninja.avatar == 'Ninja':
			ninja.spritesheet = sprites.SpriteSheet("ninjasheet.png")

		elif ninja.avatar == 'Robot':
			ninja.spritesheet = sprites.SpriteSheet("robotsheet.png")

		elif ninja.avatar == 'Dummy':
			ninja.spritesheet = sprites.SpriteSheet("dummysheet.png")

		elif ninja.avatar == 'Skull':
			ninja.spritesheet = sprites.SpriteSheet("skullsheet.png")

		ninja.build_ninja()
		'''

	def update_arrows(self):
		for arrow in self.arrow_list:
			if arrow.ninja == sprites.player1:
				if sprites.player1.menu_status == 'team select' and arrow.menu == 'team select':
					if arrow.visible == 0:
						arrow.activate()
				elif sprites.player1.menu_status == 'customize' and arrow.menu == 'customize':
					pass
				else:
					if arrow.visible == 1:
						arrow.reset()

			elif arrow.ninja == sprites.player2:
				if sprites.player2.menu_status == 'team select' and arrow.menu == 'team select':
					if arrow.visible == 0:
						arrow.activate()
				elif sprites.player2.menu_status == 'customize' and arrow.menu == 'customize':
					pass
				else:
					if arrow.visible == 1:
						arrow.reset()

			elif arrow.ninja == sprites.player3:
				if sprites.player3.menu_status == 'team select' and arrow.menu == 'team select':
					if arrow.visible == 0:
						arrow.activate()
				elif sprites.player3.menu_status == 'customize' and arrow.menu == 'customize':
					pass
				else:
					if arrow.visible == 1:
						arrow.reset()

			elif arrow.ninja == sprites.player4:
				if sprites.player4.menu_status == 'team select' and arrow.menu == 'team select':
					if arrow.visible == 0:
						arrow.activate()
				elif sprites.player4.menu_status == 'customize' and arrow.menu == 'customize':
					pass
				else:
					if arrow.visible == 1:
						arrow.reset()


	def check_taken(self, ninja, profile):
		taken = False
		for otherninja in sprites.ninja_list:
			if ninja != otherninja and otherninja.profile == profile:
				taken = True
				break

		if profile == 'Guest':
			taken = False

		return(taken)


	def new_profile_image(self, ninja, xy):
		gamepad = ninja.gamepad_layout
		'''
		if ninja == sprites.player1:
			gamepad = controls.input_handler.p1_gamepad
		elif ninja == sprites.player2:
			gamepad = controls.input_handler.p2_gamepad
		elif ninja == sprites.player3:
			gamepad = controls.input_handler.p3_gamepad
		elif ninja == sprites.player4:
			gamepad = controls.input_handler.p4_gamepad
		'''

		mod = 1
		if ninja == sprites.player2:
			mod = 2
		elif ninja == sprites.player3:
			mod = 3
		elif ninja == sprites.player4:
			mod = 4

		x_shift = 50 * mod
		image = pygame.Surface((320 - 12 - 10, 180 - 24 - 10))
		image = Build_CPU_Screen(image)
		for bar in  intro_handler.matrix_bar_list:
			#bar.update()
			if bar.rect.colliderect((xy[0],xy[1],320 - 12 - 10, 180 - 24 - 10)):
				for digit in bar.digit_list:
					digit.blit(image, x_shift) #blits to sprites.screen from within update, based on bar position.
		image = Build_Menu_Perimeter(image)

		#image.fill(options.BLACK)
		#pygame.draw.rect(image, options.DARK_PURPLE, (0,0,image.get_width() - 1, image.get_height() - 1), 2)
		#pygame.draw.rect(image, options.LIGHT_PURPLE, (2,2,image.get_width() - 4, image.get_height() - 4), 1)

		if ninja.text_case == 'lowercase':
			name = ninja.profile_text + options.lower_case_list[ninja.text_number]
		elif ninja.text_case == 'uppercase':
			name = ninja.profile_text + options.upper_case_list[ninja.text_number]

		text = font_16.render(name, 0,(options.DARK_PURPLE))
		if ninja.text_blink > 15:
			pygame.draw.rect(text, options.GREEN, (text.get_width() - 8,0,8,16),0)
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2)))

		ninja.text_blink += 1
		if ninja.text_blink > 30:
			ninja.text_blink = 0

		Scroll_Text = font_16.render('? Change Letter', 0,(options.WHITE))
		image.blit(Scroll_Text, (0 + 10, 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make scroll_pic 'key_scroll'
			scroll_pic = controls.input_handler.button_keyboard_up_down #sprites.level_sheet.getImage(0,318,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make scroll_pic 'key_scroll'
			scroll_pic = controls.input_handler.button_keyboard_up_down #sprites.level_sheet.getImage(0,318,17,17)
		else:
			scroll_pic = controls.input_handler.button_gamepad_up_down #sprites.level_sheet.getImage(0,246,17,17)
		image.blit(scroll_pic, (0 + 7, 9))
		
		Forward_Back_Text = font_16.render('? Forward/Back', 0,(options.WHITE))
		image.blit(Forward_Back_Text, (image.get_width() - Forward_Back_Text.get_width() - 10, 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'key forward back'
			forward_back_pic = controls.input_handler.button_keyboard_left_right #sprites.level_sheet.getImage(0,336,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'key forward back'
			forward_back_pic = controls.input_handler.button_keyboard_left_right #sprites.level_sheet.getImage(0,336,17,17)
		else:
			forward_back_pic = controls.input_handler.button_gamepad_left_right #sprites.level_sheet.getImage(0,264,17,17)
		image.blit(forward_back_pic, (image.get_width() - Forward_Back_Text.get_width() - 13,  9))
		
		Select_Text = font_16.render('A Accept', 0,(options.WHITE))
		image.blit(Select_Text, (0 + 10, image.get_height() - Select_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'z'
			a_pic = sprites.level_sheet.getImage(0,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'z'
			a_pic = sprites.level_sheet.getImage(0,282,17,17)
		else:
			a_pic = ninja.gamepad_layout['button_jump_image'] #sprites.level_sheet.getImage(0,228,17,17)
		image.blit(a_pic, (0 + 7, image.get_height() - Select_Text.get_height() - 11))

		Back_Text = font_16.render('B Back', 0,(options.WHITE))
		image.blit(Back_Text, ( image.get_width() - Back_Text.get_width() - 10, image.get_height() - Select_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		else:
			b_pic = ninja.gamepad_layout['button_roll_image'] #sprites.level_sheet.getImage(18,210,17,17)
		image.blit(b_pic, ( image.get_width() - Back_Text.get_width() - 13, image.get_height() - Select_Text.get_height() - 11))

		if ninja.text_case == 'lowercase':
			temp_text = 'Y Uppercase'
		else:
			temp_text = 'Y Lowercase'
		Caps_Text = font_16.render(temp_text, 0, (options.WHITE))
		image.blit(Caps_Text, ( (image.get_width() / 2) - (Caps_Text.get_width() / 2), image.get_height() - Select_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make y_pic 'key y'
			y_pic = sprites.level_sheet.getImage(18,300,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make y_pic 'key y'
			y_pic = sprites.level_sheet.getImage(18,300,17,17)
		else:
			y_pic = ninja.gamepad_layout['button_menu_image'] #sprites.level_sheet.getImage(18,300,17,17)
			#y_pic = sprites.level_sheet.getImage(0,210,17,17)
		image.blit(y_pic, ( (image.get_width() / 2) - (Caps_Text.get_width() / 2) - 3, image.get_height() - Select_Text.get_height() - 11))



		return image

	def match_list_menu(self, ninja, xy):
		gamepad = ninja.gamepad_layout

		mod = 1
		if ninja == sprites.player2:
			mod = 2
		elif ninja == sprites.player3:
			mod = 3
		elif ninja == sprites.player4:
			mod = 4
		x_shift = 50 * mod

		image = pygame.Surface((320 - 12 - 10, 180 - 24 - 10))
		#image.fill(options.BLACK)
		#pygame.draw.rect(image, options.DARK_PURPLE, (0,0,image.get_width() - 1, image.get_height() - 1), 2)
		#pygame.draw.rect(image, options.LIGHT_PURPLE, (2,2,image.get_width() - 4, image.get_height() - 4), 1)

		image = Build_CPU_Screen(image)
		for bar in  intro_handler.matrix_bar_list:
			#bar.update()
			if bar.rect.colliderect((xy[0],xy[1],320 - 12 - 10, 180 - 24 - 10)):
				for digit in bar.digit_list:
					digit.blit(image, x_shift) #blits to sprites.screen from within update, based on bar position.
		image = Build_Menu_Perimeter(image)





		return image

	def online_exit_menu(self, ninja, xy):
		gamepad = ninja.gamepad_layout


		mod = 1
		coord_mod = (5,5)
		if ninja == sprites.player2:
			mod = 2
			coord_mod = (320 + 12 + 5,5)
		elif ninja == sprites.player3:
			mod = 3
			coord_mod = (5,185)
		elif ninja == sprites.player4:
			mod = 4
			coord_mod = (325 + 12,185)
		x_shift = 50 * mod

		image = pygame.Surface((320 - 12 - 10, 180 - 24 - 10))
		#image.fill(options.BLACK)
		#pygame.draw.rect(image, options.DARK_PURPLE, (0,0,image.get_width() - 1, image.get_height() - 1), 2)
		#pygame.draw.rect(image, options.LIGHT_PURPLE, (2,2,image.get_width() - 4, image.get_height() - 4), 1)

		image = Build_CPU_Screen(image)
		for bar in  intro_handler.matrix_bar_list:
			#bar.update()
			if bar.rect.colliderect((xy[0],xy[1],320 - 12 - 10, 180 - 24 - 10)):
				for digit in bar.digit_list:
					digit.blit(image, x_shift) #blits to sprites.screen from within update, based on bar position.
		image = Build_Menu_Perimeter(image)

		if self.online_selection == 0:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = font_16.render('Quit Session', 0,(color))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) - 10))
		if self.online_selection == 0: #add 'press A'
			if ninja in controls.input_handler.gamepad_ninja_list:
				button = ninja.gamepad_layout['button_jump_image']
			else:
				button = controls.input_handler.button_keyboard_z
			#image.blit(button, ((image.get_width() / 2) - (text.get_width() / 2) - 22, (image.get_height() / 2) - (text.get_height() / 2) - 12))
			image.blit(button, ((image.get_width() / 2) + (text.get_width() / 2) + 5, (image.get_height() / 2) - (text.get_height() / 2) - 12))

		if self.online_selection == 1:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = font_16.render('Return', 0,(color))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) + 10))
		if self.online_selection == 1: #add 'press A'
			if ninja in controls.input_handler.gamepad_ninja_list:
				button = ninja.gamepad_layout['button_jump_image']
			else:
				button = controls.input_handler.button_keyboard_z
			#image.blit(button, ((image.get_width() / 2) - (text.get_width() / 2) - 22, (image.get_height() / 2) - (text.get_height() / 2) + 8))
			image.blit(button, ((image.get_width() / 2) + (text.get_width() / 2) + 5, (image.get_height() / 2) - (text.get_height() / 2) + 8))

		
		Back_Text = font_16.render('B Back', 0,(options.WHITE))

		image.blit(Back_Text, ( image.get_width() - Back_Text.get_width() - 10, image.get_height() - Back_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		else:
			b_pic = ninja.gamepad_layout['button_roll_image'] #sprites.level_sheet.getImage(18,210,17,17)
		image.blit(b_pic, ( image.get_width() - Back_Text.get_width() - 13, image.get_height() - Back_Text.get_height() - 11))

		return image

	def online_menu(self, ninja, xy):
		gamepad = ninja.gamepad_layout


		mod = 1
		coord_mod = (5,5)
		if ninja == sprites.player2:
			mod = 2
			coord_mod = (320 + 12 + 5,5)
		elif ninja == sprites.player3:
			mod = 3
			coord_mod = (5,185)
		elif ninja == sprites.player4:
			mod = 4
			coord_mod = (325 + 12,185)
		x_shift = 50 * mod

		image = pygame.Surface((320 - 12 - 10, 180 - 24 - 10))
		#image.fill(options.BLACK)
		#pygame.draw.rect(image, options.DARK_PURPLE, (0,0,image.get_width() - 1, image.get_height() - 1), 2)
		#pygame.draw.rect(image, options.LIGHT_PURPLE, (2,2,image.get_width() - 4, image.get_height() - 4), 1)

		image = Build_CPU_Screen(image)
		for bar in  intro_handler.matrix_bar_list:
			#bar.update()
			if bar.rect.colliderect((xy[0],xy[1],320 - 12 - 10, 180 - 24 - 10)):
				for digit in bar.digit_list:
					digit.blit(image, x_shift) #blits to sprites.screen from within update, based on bar position.
		image = Build_Menu_Perimeter(image)

		if self.online_selection == 0:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = font_16.render('Host', 0,(color))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) - 10))
		if self.online_selection == 0: #add 'press A'
			if ninja in controls.input_handler.gamepad_ninja_list:
				button = ninja.gamepad_layout['button_jump_image']
			else:
				button = controls.input_handler.button_keyboard_z
			#image.blit(button, ((image.get_width() / 2) - (text.get_width() / 2) - 22, (image.get_height() / 2) - (text.get_height() / 2) - 12))
			image.blit(button, ((image.get_width() / 2) + (text.get_width() / 2) + 5, (image.get_height() / 2) - (text.get_height() / 2) - 12))

		if self.online_selection == 1:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = font_16.render('Join', 0,(color))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) + 10))
		if self.online_selection == 1: #add 'press A'
			if ninja in controls.input_handler.gamepad_ninja_list:
				button = ninja.gamepad_layout['button_jump_image']
			else:
				button = controls.input_handler.button_keyboard_z
			#image.blit(button, ((image.get_width() / 2) - (text.get_width() / 2) - 22, (image.get_height() / 2) - (text.get_height() / 2) + 8))
			image.blit(button, ((image.get_width() / 2) + (text.get_width() / 2) + 5, (image.get_height() / 2) - (text.get_height() / 2) + 8))

		
		Back_Text = font_16.render('B Back', 0,(options.WHITE))

		image.blit(Back_Text, ( image.get_width() - Back_Text.get_width() - 10, image.get_height() - Back_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		else:
			b_pic = ninja.gamepad_layout['button_roll_image'] #sprites.level_sheet.getImage(18,210,17,17)
		image.blit(b_pic, ( image.get_width() - Back_Text.get_width() - 13, image.get_height() - Back_Text.get_height() - 11))

		return image

	def customize(self, ninja, xy):
		gamepad = ninja.gamepad_layout
		'''
		if ninja == sprites.player1:
			gamepad = controls.input_handler.p1_gamepad
		elif ninja == sprites.player2:
			gamepad = controls.input_handler.p2_gamepad
		elif ninja == sprites.player3:
			gamepad = controls.input_handler.p3_gamepad
		elif ninja == sprites.player4:
			gamepad = controls.input_handler.p4_gamepad
		'''

		#coord_mod = (5,5)
		#coord_mod = (320 + 12 + 5,5)
		#coord_mod = (5,185)
		#coord_mod = (325 + 12,185)

		mod = 1
		coord_mod = (5,5)
		if ninja == sprites.player2:
			mod = 2
			coord_mod = (320 + 12 + 5,5)
		elif ninja == sprites.player3:
			mod = 3
			coord_mod = (5,185)
		elif ninja == sprites.player4:
			mod = 4
			coord_mod = (325 + 12,185)
		x_shift = 50 * mod

		image = pygame.Surface((320 - 12 - 10, 180 - 24 - 10))
		#image.fill(options.BLACK)
		#pygame.draw.rect(image, options.DARK_PURPLE, (0,0,image.get_width() - 1, image.get_height() - 1), 2)
		#pygame.draw.rect(image, options.LIGHT_PURPLE, (2,2,image.get_width() - 4, image.get_height() - 4), 1)

		image = Build_CPU_Screen(image)
		for bar in  intro_handler.matrix_bar_list:
			#bar.update()
			if bar.rect.colliderect((xy[0],xy[1],320 - 12 - 10, 180 - 24 - 10)):
				for digit in bar.digit_list:
					digit.blit(image, x_shift) #blits to sprites.screen from within update, based on bar position.
		image = Build_Menu_Perimeter(image)

		if ninja.custom_menu_row == 0:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = font_16.render('Customize Gamepad', 0,(color))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) - 30))
		if ninja.custom_menu_row == 0: #add 'press A'
			if ninja in controls.input_handler.gamepad_ninja_list:
				button = ninja.gamepad_layout['button_jump_image']
			else:
				button = controls.input_handler.button_keyboard_z
			image.blit(button, ((image.get_width() / 2) - (text.get_width() / 2) - 22, (image.get_height() / 2) - (text.get_height() / 2) - 31))
			image.blit(button, ((image.get_width() / 2) + (text.get_width() / 2) + 5, (image.get_height() / 2) - (text.get_height() / 2) - 31))

		if ninja.custom_menu_row == 1:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = 'Accessory: ' + ninja.swag
		accessory_text = font_16.render(text, 0,(color))
		image.blit(accessory_text, ((image.get_width() / 2) - (accessory_text.get_width() / 2), (image.get_height() / 2) - (accessory_text.get_height() / 2) - 10))
		
		if ninja.custom_menu_row == 2:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = 'Avatar: ' + ninja.avatar
		avatar_text = font_16.render(text, 0,(color))
		image.blit(avatar_text, ((image.get_width() / 2) - (avatar_text.get_width() / 2), (image.get_height() / 2) - (avatar_text.get_height() / 2) + 10))

		if ninja.custom_menu_row == 3:
			color = options.DARK_PURPLE
		else:
			color = options.WHITE
		text = 'Profile: ' + ninja.profile
		profile_text = font_16.render(text, 0,(color))
		image.blit(profile_text, ((image.get_width() / 2) - (profile_text.get_width() / 2), (image.get_height() / 2) - (profile_text.get_height() / 2) + 30))
		if ninja.custom_menu_row == 3: #add 'press A'
			if ninja in controls.input_handler.gamepad_ninja_list:
				button = ninja.gamepad_layout['button_jump_image']
			else:
				button = controls.input_handler.button_keyboard_z
			image.blit(button, ((image.get_width() / 2) - (profile_text.get_width() / 2) - 22, (image.get_height() / 2) - (profile_text.get_height() / 2) + 31))
			image.blit(button, ((image.get_width() / 2) + (profile_text.get_width() / 2) + 5, (image.get_height() / 2) - (profile_text.get_height() / 2) + 31))

		#Make Arrows At Right Levelt
		if ninja.custom_menu_row == 1:
			for arrow in self.arrow_list:
				if arrow.ninja == ninja and arrow.menu == 'customize':
					if arrow.visible == 0:
						arrow.activate()
					
					arrow.rect.centery = coord_mod[1] + (image.get_height() / 2) - 11
					if arrow.direction == 'left':
						arrow.rect.right = coord_mod[0] + (image.get_width() / 2) - (accessory_text.get_width() / 2) - 5
					if arrow.direction == 'right':
						arrow.rect.left = coord_mod[0] + (image.get_width() / 2) + (accessory_text.get_width() / 2) + 5

		elif ninja.custom_menu_row == 2:
			for arrow in self.arrow_list:
				if arrow.ninja == ninja and arrow.menu == 'customize':
					if arrow.visible == 0:
						arrow.activate()
					
					arrow.rect.centery = coord_mod[1] + (image.get_height() / 2) + 9
					if arrow.direction == 'left':
						arrow.rect.right = coord_mod[0] + (image.get_width() / 2) - (avatar_text.get_width() / 2) - 5
					if arrow.direction == 'right':
						arrow.rect.left = coord_mod[0] + (image.get_width() / 2) + (avatar_text.get_width() / 2) + 5

		else:
			for arrow in self.arrow_list:
				if arrow.ninja == ninja and arrow.menu == 'customize':
					arrow.reset()


		'''
		i = ninja.profile_number - 1
		if i < 0:
			i = len(options.profile_list) - 1
		text = font_16.render(options.profile_list[i], 0,(options.LIGHT_PURPLE))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) - 5 -(text.get_height())))

		i = ninja.profile_number + 1
		if i > len(options.profile_list) - 1:
			i = 0
		text = font_16.render(options.profile_list[i], 0,(options.LIGHT_PURPLE))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) + 5 +(text.get_height())))
		'''
		#Select_Text = font_16.render('A Select', 0,(options.WHITE))
		Back_Text = font_16.render('B Back', 0,(options.WHITE))

		image.blit(Back_Text, ( image.get_width() - Back_Text.get_width() - 10, image.get_height() - Back_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		else:
			b_pic = ninja.gamepad_layout['button_roll_image'] #sprites.level_sheet.getImage(18,210,17,17)
		image.blit(b_pic, ( image.get_width() - Back_Text.get_width() - 13, image.get_height() - Back_Text.get_height() - 11))

		return image

	def profile_select_image(self, ninja, xy):
		gamepad = ninja.gamepad_layout
		'''
		if ninja == sprites.player1:
			gamepad = controls.input_handler.p1_gamepad
		elif ninja == sprites.player2:
			gamepad = controls.input_handler.p2_gamepad
		elif ninja == sprites.player3:
			gamepad = controls.input_handler.p3_gamepad
		elif ninja == sprites.player4:
			gamepad = controls.input_handler.p4_gamepad
		'''

		temp_profile_list = options.profile_list.copy()

		mod = 1
		if ninja == sprites.player2:
			mod = 2
		elif ninja == sprites.player3:
			mod = 3
		elif ninja == sprites.player4:
			mod = 4
		x_shift = 50 * mod

		image = pygame.Surface((320 - 12 - 10, 180 - 24 - 10))
		#image.fill(options.BLACK)
		#pygame.draw.rect(image, options.DARK_PURPLE, (0,0,image.get_width() - 1, image.get_height() - 1), 2)
		#pygame.draw.rect(image, options.LIGHT_PURPLE, (2,2,image.get_width() - 4, image.get_height() - 4), 1)

		image = Build_CPU_Screen(image)
		for bar in  intro_handler.matrix_bar_list:
			#bar.update()
			if bar.rect.colliderect((xy[0],xy[1],320 - 12 - 10, 180 - 24 - 10)):
				for digit in bar.digit_list:
					digit.blit(image, x_shift) #blits to sprites.screen from within update, based on bar position.
		image = Build_Menu_Perimeter(image)

		text = font_16.render(options.profile_list[ninja.profile_number], 0,(options.DARK_PURPLE))
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2)))

		i = ninja.profile_number - 1
		if i < 0:
			i = len(options.profile_list) - 1
		text = font_16.render(options.profile_list[i], 0,(options.LIGHT_PURPLE))
		if len(options.profile_list) > 1:
			image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) - 5 -(text.get_height())))

		i = ninja.profile_number + 1
		if i > len(options.profile_list) - 1:
			i = 0

		text = font_16.render(options.profile_list[i], 0,(options.LIGHT_PURPLE))
		if len(options.profile_list) > 1:
			image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2) + 5 +(text.get_height())))

		Select_Text = font_16.render('A Select', 0,(options.WHITE))
		Back_Text = font_16.render('B Back', 0,(options.WHITE))

		image.blit(Select_Text, (0 + 10, image.get_height() - Select_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'z'
			a_pic = sprites.level_sheet.getImage(0,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'z'
			a_pic = sprites.level_sheet.getImage(0,282,17,17)
		else:
			a_pic = ninja.gamepad_layout['button_jump_image'] #sprites.level_sheet.getImage(0,228,17,17)
		image.blit(a_pic, (0 + 7, image.get_height() - Select_Text.get_height() - 11))

		image.blit(Back_Text, ( image.get_width() - Back_Text.get_width() - 10, image.get_height() - Select_Text.get_height() - 10))
		if ninja == sprites.player1 and options.control_preferences['player1'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		elif ninja == sprites.player2 and options.control_preferences['player2'] == 'keyboard':
			#make a_pic 'x'
			b_pic = sprites.level_sheet.getImage(18,282,17,17)
		else:
			b_pic = ninja.gamepad_layout['button_roll_image'] #sprites.level_sheet.getImage(18,210,17,17)
		image.blit(b_pic, ( image.get_width() - Back_Text.get_width() - 13, image.get_height() - Select_Text.get_height() - 11))

		return image


	def spawn_ninja(self, ninja):
		#currently only used for online play
		ninja.menu_status = 'team select'
		if ninja == sprites.player1:
			if sprites.player1 not in sprites.ninja_list and sprites.player1.spawn_sprite.status == 'idle':
				self.set_gamepad_layout(sprites.player1)
				if sprites.player1.bandana.headband.status == 'free':
					sprites.player1.bandana.crumble()
				sprites.player_list.add(sprites.player1)
				sprites.player1.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4) - 24 ), phase_in = True)
				'''
				try:
					ninja.bandana.headband.update()
				except:
					pass
				try:
					ninja.bandana.update()
				except:
					pass
				'''
		elif ninja == sprites.player2:
			if sprites.player2 not in sprites.ninja_list and sprites.player2.spawn_sprite.status == 'idle':
				self.set_gamepad_layout(sprites.player2)
				if sprites.player2.bandana.headband.status == 'free':
					sprites.player2.bandana.crumble()
				sprites.player_list.add(sprites.player2)
				sprites.player2.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4) - 24 ), phase_in = True)
				'''
				try:
					ninja.bandana.headband.update()
				except:
					pass
				try:
					ninja.bandana.update()
				except:
					pass
				'''

		elif ninja == sprites.player3:
			if sprites.player3 not in sprites.ninja_list and sprites.player3.spawn_sprite.status == 'idle':
				self.set_gamepad_layout(sprites.player3)
				if sprites.player3.bandana.headband.status == 'free':
					sprites.player3.bandana.crumble()
				sprites.player_list.add(sprites.player3)
				sprites.player3.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4 * 3) - 24 ), phase_in = True)
				'''
				try:
					ninja.bandana.headband.update()
				except:
					pass
				try:
					ninja.bandana.update()
				except:
					pass
				'''
					
		elif ninja == sprites.player4:
			if sprites.player4 not in sprites.ninja_list and sprites.player4.spawn_sprite.status == 'idle':
				if sprites.player4.bandana.headband.status == 'free':
					sprites.player4.bandana.crumble()
				sprites.player_list.add(sprites.player4)
				sprites.player4.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4 * 3) - 24 ), phase_in = True)
				'''
				try:
					ninja.bandana.headband.update()
				except:
					pass
				try:
					ninja.bandana.update()
				except:
					pass
				'''

	def load_menu(self):


		for ninja in (sprites.player1, sprites.player2, sprites.player3, sprites.player4):
			if ninja.color not in options.color_choices:
				ninja.change_color(None, None, color_tuple = random.choice(options.color_choices), change_bandana = False)

			if ninja.bandana_color not in options.bandana_color_choices:
				ninja.bandana_color = random.choice(options.bandana_color_choices)
				ninja.bandana.kill()
				#ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.bandana_color)

			#sprites.player1.bandana_color = options.RED_LIST
			#sprites.player1.bandana.kill()
			#sprites.player1.bandana = rope_physics.Bandana_Knot(sprites.player1, sprites.player1.bandana_color)

			if ninja.dummy is True:
				ninja.dummy = False
				sprites.player_list.remove(ninja)
				if ninja == sprites.player2:
					ninja.color = options.BLUE_LIST
					ninja.swag = 'Bandana'
					ninja.set_avatar(avatar = 'Robot')
					ninja.bandana_color = options.PURPLE_LIST
					ninja.bandana.kill()
					ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.bandana_color)
				elif ninja == sprites.player3:
					ninja.color = options.GREEN_LIST
					ninja.swag = 'Bandana'
					ninja.set_avatar(avatar = 'Mutant')
					ninja.bandana_color = options.ORANGE_LIST
					ninja.bandana.kill()
					ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.bandana_color)
				elif ninja == sprites.player4:
					ninja.color = options.RED_LIST
					ninja.swag = 'Bandana'
					ninja.set_avatar(avatar = 'Cyborg')
					ninja.bandana_color = options.BLUE_LIST
					ninja.bandana.kill()
					ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.bandana_color)
				'''				
					color_choices = options.color_choices.copy()
					color_choices.remove(sprites.player1.color)
					for dummy in (sprites.player2, sprites.player3, sprites.player4):
						dummy.color = random.choice(color_choices)
						color_choices.remove(dummy.color)
						dummy.dummy = True
						dummy.swag = 'None'
						dummy.set_avatar(avatar = 'Dummy')
						sprites.player_list.add(dummy)
				'''

		options.inverted_g = False

		sprites.player1.custom_menu_row = 0
		sprites.player2.custom_menu_row = 0
		sprites.player3.custom_menu_row = 0
		sprites.player4.custom_menu_row = 0

		sprites.player1.menu_status = 'join'
		sprites.player2.menu_status = "join"
		sprites.player3.menu_status = "join"
		sprites.player4.menu_status = "join"

		sprites.player1.controls_sprite.reset()
		sprites.reset_sprites() #reset all the contents of the sprites sprite groups.

		try: #just here to help it along in case of 'message'
			sprites.active_sprite_list.remove(main_menu_sprite)
			sprites.menu_sprite_list.remove(main_menu_sprite)
		except:
			pass

		for sprite in sprites.menu_sprite_list:
			sprites.active_sprite_list.remove(sprite)
			sprites.menu_sprite_list.remove(sprite)
		#sprites.menu_sprite_list.add(main_menu_sprite)
		#sprites.active_sprite_list.add(main_menu_sprite)

		background = level.Level_Background(-10, 'main_menu_background.png')
		#background.image.fill((0,200,0))
		
		#background_text = level.Level_Background(-8, 'main_menu.png')
		sprites.menu_sprite_list.add(background)
		#sprites.menu_sprite_list.change_layer(background, -10)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)
		self.text_screen = level.Level_Background(10, options.GREEN)
		#background_text = level.Level_Background(-8, 'main_menu.png')

		


		
		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))
		



		#create Mallow
		mallow = level.Mallow ((0,330,640,30), False)
		'''
		i = 0
		while i < 640:
			mallow = level.Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		for ninja in sprites.ninja_list:
			ninja.lose() #just takes ninjas out of active sprites list.
		

		self.arrow_list = []
		#Create Arrows for customize menu:
		for ninja in (sprites.player1, sprites.player2, sprites.player3, sprites.player4):
			arrow = sprites.Menu_Arrow((0,0), 'left', ninja, 'customize')
			self.arrow_list.append(arrow)
			arrow = sprites.Menu_Arrow((0,0), 'right', ninja, 'customize')
			self.arrow_list.append(arrow)
		
		#Create Arrows for team select
		tile = level.Platform((sprites.screen.get_width() / 4) - 18, sprites.screen.get_height() / 4, 'classic', False)
		arrow = sprites.Menu_Arrow((tile.rect.centerx - 55, tile.rect.centery + 22), 'left', sprites.player1, 'team select')
		self.arrow_list.append(arrow)
		arrow = sprites.Menu_Arrow((tile.rect.centerx + 55, tile.rect.centery + 22), 'right', sprites.player1, 'team select')
		self.arrow_list.append(arrow)

		tile = level.Platform((sprites.screen.get_width() / 4) - 18, sprites.screen.get_height() / 4 * 3, 'classic', False)
		arrow = sprites.Menu_Arrow((tile.rect.centerx - 55, tile.rect.centery + 22), 'left', sprites.player3, 'team select')
		self.arrow_list.append(arrow)
		arrow = sprites.Menu_Arrow((tile.rect.centerx + 55, tile.rect.centery + 22), 'right', sprites.player3, 'team select')
		self.arrow_list.append(arrow)

		tile = level.Platform((sprites.screen.get_width() / 4 * 3) - 18, sprites.screen.get_height() / 4, 'classic', False)
		arrow = sprites.Menu_Arrow((tile.rect.centerx - 55, tile.rect.centery + 22), 'left', sprites.player2, 'team select')
		self.arrow_list.append(arrow)
		arrow = sprites.Menu_Arrow((tile.rect.centerx + 55, tile.rect.centery + 22), 'right', sprites.player2, 'team select')
		self.arrow_list.append(arrow)

		tile = level.Platform((sprites.screen.get_width() / 4 * 3) - 18, sprites.screen.get_height() / 4 * 3, 'classic', False)
		arrow = sprites.Menu_Arrow((tile.rect.centerx - 55, tile.rect.centery + 22), 'left', sprites.player4, 'team select')
		self.arrow_list.append(arrow)
		arrow = sprites.Menu_Arrow((tile.rect.centerx + 55, tile.rect.centery + 22), 'right', sprites.player4, 'team select')
		self.arrow_list.append(arrow)
		
		count = 0
		while count * 24 < 640:
			platform = level.Tile(-4 + (count * 24), (sprites.size[1] / 2) - 24, 'classic', False)
			count += 1

		count = 0
		while count * 24 < 360:
			platform = level.Tile((sprites.size[0] / 2) - 12, 0 + (count * 24), 'classic', False)
			count += 1


		for tile in sprites.tile_list:
			if tile.type == 'tile':
				tile.check_sides(mid_level = True)

		if self.source != 'main menu':
			self.source = 'main menu'
			for ninja in sprites.player_list:
				#aaaaaaaaaaaaaaaaaaaaaaaaaa
				#ninja.menu_select_press = True
				if ninja == sprites.player1:
					sprites.player1.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4) - 24 ), phase_in = True)
					sprites.player1.menu_status = 'team select'
				if ninja == sprites.player2:
					sprites.player2.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4) - 24 ), phase_in = True)
					sprites.player2.menu_status = 'team select'
				if ninja == sprites.player3:
					sprites.player3.place_ninja((sprites.screen.get_width() / 4, (sprites.screen.get_height() / 4 * 3) - 24 ), phase_in = True)
					sprites.player3.menu_status = 'team select'
				if ninja == sprites.player4:
					sprites.player4.place_ninja((sprites.screen.get_width() / 4 * 3, (sprites.screen.get_height() / 4 * 3) - 24 ), phase_in = True)
					sprites.player4.menu_status = 'team select'
		else:
			for ninja in sprites.player_list:
				sprites.player_list.remove(ninja)

player_select_handler = Player_Select_Handler()

'''
def player_select():
	#check for gamepads regularly.
	controls.input_handler.get_gamepads()

	screen = sprites.screen
	starting_positions = [(100,30), (540,30), (100,290), (540,290)]

	pygame.draw.rect(screen, BLACK, (0, 0, screen.get_width(), screen.get_height()), 0)
	pygame.draw.line(screen, WHITE, (screen.get_width() / 2 , 0) , (screen.get_width() / 2 , screen.get_height()), 2)
	pygame.draw.line(screen, WHITE, (0 , screen.get_height() / 2) , (screen.get_width() , screen.get_height() / 2), 2)

	JoinText = font_30.render('Press Start', 0,(WHITE))
	ColorText = font_30.render('Select Team', 0, (WHITE))
	ReadyText = font_30.render('Ready!', 0, (WHITE))

	if sprites.player1.menu_status == 'join':
		P1_Text = JoinText
	elif sprites.player1.menu_status == 'team select':
		P1_Text = ColorText
	elif sprites.player1.menu_status == 'ready':
		P1_Text = ReadyText

	if sprites.player2.menu_status == 'join':
		P2_Text = JoinText
	elif sprites.player2.menu_status == 'team select':
		P2_Text = ColorText
	elif sprites.player2.menu_status == 'ready':
		P2_Text = ReadyText

	if sprites.player3.menu_status == 'join':
		P3_Text = JoinText
	elif sprites.player3.menu_status == 'team select':
		P3_Text = ColorText
	elif sprites.player3.menu_status == 'ready':
		P3_Text = ReadyText

	if sprites.player4.menu_status == 'join':
		P4_Text = JoinText
	elif sprites.player4.menu_status == 'team select':
		P4_Text = ColorText
	elif sprites.player4.menu_status == 'ready':
		P4_Text = ReadyText


	
	screen.blit(P1_Text, ((screen.get_width() / 4) - (P1_Text.get_width() / 2), ((screen.get_height() / 4) + 30)))
	screen.blit(P2_Text, ((screen.get_width() / 4 * 3) - (P2_Text.get_width() / 2), ((screen.get_height() / 4) + 30)))
	screen.blit(P3_Text, ((screen.get_width() / 4) - (P3_Text.get_width() / 2), ((screen.get_height() / 4 * 3) + 30)))
	screen.blit(P4_Text, ((screen.get_width() / 4 * 3) - (P4_Text.get_width() / 2), ((screen.get_height() / 4 * 3) + 30)))

	if sprites.player1.menu_y_press is True:
		options.game_state = 'versus_options'

	if sprites.player1.menu_left_press is True:
		if sprites.player1.menu_status == 'team select':
			sprites.player1.change_color('left', None)
			sounds.mixer.menu_move.play()
	elif sprites.player1.menu_right_press is True:
		if sprites.player1.menu_status == 'team select':
			sprites.player1.change_color('right', None)
			sounds.mixer.menu_move.play()

	if sprites.player2.menu_left_press is True:
		if sprites.player2.menu_status == 'team select':
			sprites.player2.change_color('left', None)
			sounds.mixer.menu_move.play()
	elif sprites.player2.menu_right_press is True:
		if sprites.player2.menu_status == 'team select':
			sprites.player2.change_color('right', None)
			sounds.mixer.menu_move.play()

	if sprites.player3.menu_left_press is True:
		if sprites.player3.menu_status == 'team select':
			sprites.player3.change_color('left', None)
			sounds.mixer.menu_move.play()
	elif sprites.player3.menu_right_press is True:
		if sprites.player3.menu_status == 'team select':
			sprites.player3.change_color('right', None)
			sounds.mixer.menu_move.play()

	if sprites.player4.menu_left_press is True:
		if sprites.player4.menu_status == 'team select':
			sprites.player4.change_color('left', None)
			sounds.mixer.menu_back.play()
	elif sprites.player4.menu_right_press is True:
		if sprites.player4.menu_status == 'team select':
			sprites.player4.change_color('right', None)
			sounds.mixer.menu_back.play()

	if sprites.player1.menu_back_press is True:
		if sprites.player1.menu_status == 'ready':
			sprites.player1.menu_status = 'team select'
			sounds.mixer.menu_move.play()
		elif sprites.player1.menu_status == 'team select':
			sprites.player1.menu_status = 'join'
			sprites.ninja_list.remove(sprites.player1)
			sprites.active_sprite_list.remove(sprites.player1)
			sprites.player_list.remove(sprites.player1)
			sounds.mixer.menu_move.play()
		elif sprites.player1.menu_status == 'join':
			options.game_state = 'main_menu'

	if sprites.player2.menu_back_press is True:
		if sprites.player2.menu_status == 'ready':
			sprites.player2.menu_status = 'team select'
			sounds.mixer.menu_move.play()
		elif sprites.player2.menu_status == 'team select':
			sprites.player2.menu_status = 'join'
			sprites.ninja_list.remove(sprites.player2)
			sprites.active_sprite_list.remove(sprites.player2)
			sprites.player_list.remove(sprites.player2)
			sounds.mixer.menu_move.play()

	if sprites.player3.menu_back_press is True:
		if sprites.player3.menu_status == 'ready':
			sprites.player3.menu_status = 'team select'
			sounds.mixer.menu_move.play()
		elif sprites.player3.menu_status == 'team select':
			sprites.player3.menu_status = 'join'
			sprites.ninja_list.remove(sprites.player3)
			sprites.active_sprite_list.remove(sprites.player3)
			sprites.player_list.remove(sprites.player3)
			sounds.mixer.menu_move.play()

	if sprites.player4.menu_back_press is True:
		if sprites.player4.menu_status == 'ready':
			sprites.player4.menu_status = 'team select'
			sounds.mixer.menu_move.play()
		elif sprites.player4.menu_status == 'team select':
			sprites.player4.menu_status = 'join'
			sprites.ninja_list.remove(sprites.player4)
			sprites.active_sprite_list.remove(sprites.player4)
			sprites.player_list.remove(sprites.player4)
			sounds.mixer.menu_move.play()


	if sprites.player1.menu_select_press is True:
		if sprites.player1 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player1)
			sprites.active_sprite_list.add(sprites.player1)
			sprites.active_sprite_list.change_layer(sprites.player1, 1)
			sprites.player_list.add(sprites.player1)
			sprites.player1.place_ninja((screen.get_width() / 4, (screen.get_height() / 4) - 24 ))
		if sprites.player1.menu_status == 'join':
			sprites.player1.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player1.menu_status == 'team select':
			sprites.player1.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player1.direction = 'right'

		#first player only can start match
		if len(sprites.ninja_list) > 1:
			if all(sprite.menu_status == 'ready' for sprite in sprites.ninja_list) is True:
				i = []
				for sprite in sprites.ninja_list:
					if sprite.color not in i:
						i.append(sprite.color)
						if len(i) > 1:
							sounds.mixer.menu_select.play()
							options.game_state = 'versus_level_selection'
							options.game_mode = 'versus'

							pygame.draw.rect(screen, BLACK, (0, 0, screen.get_width(), screen.get_height()), 0)

							break

	if sprites.player2.menu_select_press is True:
		if sprites.player2 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player2)
			sprites.active_sprite_list.add(sprites.player2)
			sprites.active_sprite_list.change_layer(sprites.player2, 1)
			sprites.player_list.add(sprites.player2)
			sprites.player2.place_ninja((screen.get_width() / 4 * 3, (screen.get_height() / 4) - 24 ))
		if sprites.player2.menu_status == 'join':
			sprites.player2.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player2.menu_status == 'team select':
			sprites.player2.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player2.direction = 'left'



	if sprites.player3.menu_select_press is True:
		if sprites.player3 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player3)
			sprites.active_sprite_list.add(sprites.player3)
			sprites.active_sprite_list.change_layer(sprites.player3, 1)
			sprites.player_list.add(sprites.player3)
			sprites.player3.place_ninja((screen.get_width() / 4, (screen.get_height() / 4 * 3) - 24 ))
		if sprites.player3.menu_status == 'join':
			sprites.player3.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player3.menu_status == 'team select':
			sprites.player3.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player3.direction = 'right'

	if sprites.player4.menu_select_press is True:
		if sprites.player4 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player4)
			sprites.active_sprite_list.add(sprites.player4)
			sprites.active_sprite_list.change_layer(sprites.player4, 1)
			sprites.player_list.add(sprites.player4)
			sprites.player4.place_ninja((screen.get_width() / 4 * 3, (screen.get_height() / 4 * 3) - 24 ))
		if sprites.player4.menu_status == 'join':
			sprites.player4.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player4.menu_status == 'team select':
			sprites.player4.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player4.direction = 'left'


	if controls.input_handler.press1 is True:
		if sprites.player1 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player1)
			sprites.active_sprite_list.add(sprites.player1)
			sprites.active_sprite_list.change_layer(sprites.player1, 1)
			sprites.player_list.add(sprites.player1)
			sprites.player1.place_ninja((screen.get_width() / 4, (screen.get_height() / 4) - 24 ))
		if sprites.player1.menu_status == 'join':
			sprites.player1.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player1.menu_status == 'team select':
			sprites.player1.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player1.direction = 'right'

	if controls.input_handler.press2 is True:
		if sprites.player2 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player2)
			sprites.active_sprite_list.add(sprites.player2)
			sprites.active_sprite_list.change_layer(sprites.player2, 1)
			sprites.player_list.add(sprites.player2)
			sprites.player2.place_ninja((screen.get_width() / 4 * 3, (screen.get_height() / 4) - 24 ))
		if sprites.player2.menu_status == 'join':
			sprites.player2.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player2.menu_status == 'team select':
			sprites.player2.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player2.direction = 'left'

	if controls.input_handler.press3 is True:
		if sprites.player3 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player3)
			sprites.active_sprite_list.add(sprites.player3)
			sprites.active_sprite_list.change_layer(sprites.player3, 1)
			sprites.player_list.add(sprites.player3)
			sprites.player3.place_ninja((screen.get_width() / 4, (screen.get_height() / 4 * 3) - 24 ))
		if sprites.player3.menu_status == 'join':
			sprites.player3.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player3.menu_status == 'team select':
			sprites.player3.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player3.direction = 'right'

	if controls.input_handler.press4 is True:
		if sprites.player4 not in sprites.ninja_list:
			sprites.ninja_list.add(sprites.player4)
			sprites.active_sprite_list.add(sprites.player4)
			sprites.active_sprite_list.change_layer(sprites.player4, 1)
			sprites.player_list.add(sprites.player4)
			sprites.player4.place_ninja((screen.get_width() / 4 * 3, (screen.get_height() / 4 * 3) - 24 ))
		if sprites.player4.menu_status == 'join':
			sprites.player4.menu_status = 'team select'
			sounds.mixer.menu_select.play()
		elif sprites.player4.menu_status == 'team select':
			sprites.player4.menu_status = 'ready'
			sounds.mixer.menu_select.play()
		sprites.player4.direction = 'left'



	for sprite in sprites.tile_list:
		sprite.dirty = 1

	#screen.fill(BLACK)
	sprites.ninja_list.update()
	sprites.ninja_list.draw(screen)
	sprites.tile_list.draw(screen)
'''
class Game_Options_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()
			
			


		controls.input_handler.get_gamepads()

		if sprites.player1.menu_left_press is True:
			game_options_sprite.scroll('left')

			if game_options_sprite.vertical_selection == 0: #music
				options.music_volume = game_options_sprite.menu_list[0][1][game_options_sprite.selection_list[0]] * 0.1
				sounds.mixer.update_music_volume()

			if game_options_sprite.vertical_selection == 1: #effects
				options.effects_volume = game_options_sprite.menu_list[1][1][game_options_sprite.selection_list[1]] * 0.1
				sounds.mixer.update_effects_volume()

			elif game_options_sprite.vertical_selection == 6: #effects
				options.FPS_counter = game_options_sprite.menu_list[6][1][game_options_sprite.selection_list[6]]
				sounds.mixer.update_effects_volume()

			elif game_options_sprite.vertical_selection == 3: #effects
				if game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]] == 'keyboard' and game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]] == 'keyboard':
					game_options_sprite.scroll('down', sound = False)
					game_options_sprite.scroll('left', sound = False)
					game_options_sprite.scroll('up', sound = False)

			elif game_options_sprite.vertical_selection == 4: #effects
				if game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]] == 'keyboard' and game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]] == 'keyboard':
					game_options_sprite.scroll('up', sound = False)
					game_options_sprite.scroll('left', sound = False)
					game_options_sprite.scroll('down', sound = False)

		if sprites.player1.menu_right_press is True:
			game_options_sprite.scroll('right')

			if game_options_sprite.vertical_selection == 0: #music
				options.music_volume = game_options_sprite.menu_list[0][1][game_options_sprite.selection_list[0]] * 0.1
				sounds.mixer.update_music_volume()

			elif game_options_sprite.vertical_selection == 1: #effects
				options.effects_volume = game_options_sprite.menu_list[1][1][game_options_sprite.selection_list[1]] * 0.1
				sounds.mixer.update_effects_volume()

			elif game_options_sprite.vertical_selection == 6: #effects
				options.FPS_counter = game_options_sprite.menu_list[6][1][game_options_sprite.selection_list[6]]
				sounds.mixer.update_effects_volume()

			elif game_options_sprite.vertical_selection == 3: #effects
				if game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]] == 'keyboard' and game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]] == 'keyboard':
					game_options_sprite.scroll('down', sound = False)
					game_options_sprite.scroll('left', sound = False)
					game_options_sprite.scroll('up', sound = False)

			elif game_options_sprite.vertical_selection == 4: #effects
				if game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]] == 'keyboard' and game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]] == 'keyboard':
					game_options_sprite.scroll('up', sound = False)
					game_options_sprite.scroll('left', sound = False)
					game_options_sprite.scroll('down', sound = False)

		if sprites.player1.menu_up_press is True:
			game_options_sprite.scroll('up')

		if sprites.player1.menu_down_press is True:
			game_options_sprite.scroll('down')

		if sprites.player1.menu_back_press is True:
				options.game_state = 'main_menu'
				self.reset()
				sounds.mixer.menu_select.play()

				#build/change options.py settings.

				options.music_volume = round(game_options_sprite.menu_list[0][1][game_options_sprite.selection_list[0]] * 0.1, 1)
				options.effects_volume = round(game_options_sprite.menu_list[1][1][game_options_sprite.selection_list[1]] * 0.1, 1)

				#P1 Input keyboard vs Gamepad
				options.control_preferences['player1'] = game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]]
				#P2 Input keyboard vs Gamepad
				options.control_preferences['player2'] = game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]]

				options.FPS_counter = game_options_sprite.menu_list[6][1][game_options_sprite.selection_list[6]]
				options.rope_physics = game_options_sprite.menu_list[7][1][game_options_sprite.selection_list[7]]
				options.bandana_physics = game_options_sprite.menu_list[8][1][game_options_sprite.selection_list[8]]
				options.visual_effects = game_options_sprite.menu_list[9][1][game_options_sprite.selection_list[9]]
				options.screen_shake = game_options_sprite.menu_list[10][1][game_options_sprite.selection_list[10]]


				if options.visual_effects == 'High':
					options.death_animations = 'On'
					options.particles = 'High'
					options.background_effects = 'High'
				elif options.visual_effects == 'Low':
					options.death_animations = 'On'
					options.particles = 'Low'
					options.background_effects = 'Low'
				elif options.visual_effects == 'Off':
					options.death_animations = 'Off'
					options.particles = 'Off'
					options.background_effects = 'Off'

				if options.bandana_physics == 'On':
					for ninja in (sprites.player1, sprites.player2, sprites.player3, sprites.player4):
						ninja.swag = 'Bandana'
						ninja.bandana.kill()
						ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.color)
						ninja.bandana.kill()

				#need to turn down current built up shake.
				sprites.shake_handler.current_shake = 0
				controls.input_handler.get_gamepads()


		if sprites.player1.menu_select_press is True:
			#Check if 'Return' is selected
			if game_options_sprite.menu_list[game_options_sprite.vertical_selection][0] in ('Accept', 'Credits'):
				if game_options_sprite.menu_list[game_options_sprite.vertical_selection][0] == 'Accept':
					options.game_state = 'main_menu'
				else:
					options.game_state = 'game_credits'
				self.reset()
				sounds.mixer.menu_select.play()

				#build/change options.py settings.

				options.music_volume = round(game_options_sprite.menu_list[0][1][game_options_sprite.selection_list[0]] * 0.1, 1)
				options.effects_volume = round(game_options_sprite.menu_list[1][1][game_options_sprite.selection_list[1]] * 0.1, 1)

				#P1 Input keyboard vs Gamepad
				options.control_preferences['player1'] = game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]]
				#P2 Input keyboard vs Gamepad
				options.control_preferences['player2'] = game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]]

				options.FPS_counter = game_options_sprite.menu_list[6][1][game_options_sprite.selection_list[6]]
				options.rope_physics = game_options_sprite.menu_list[7][1][game_options_sprite.selection_list[7]]
				options.bandana_physics = game_options_sprite.menu_list[8][1][game_options_sprite.selection_list[8]]
				options.visual_effects = game_options_sprite.menu_list[9][1][game_options_sprite.selection_list[9]]
				options.screen_shake = game_options_sprite.menu_list[10][1][game_options_sprite.selection_list[10]]


				if options.visual_effects == 'High':
					options.death_animations = 'On'
					options.particles = 'High'
					options.background_effects = 'High'
				elif options.visual_effects == 'Low':
					options.death_animations = 'On'
					options.particles = 'Low'
					options.background_effects = 'Low'
				elif options.visual_effects == 'Off':
					options.death_animations = 'Off'
					options.particles = 'Off'
					options.background_effects = 'Off'

				#options.death_animations = game_options_sprite.menu_list[9][1][game_options_sprite.selection_list[9]]
				#options.particles = game_options_sprite.menu_list[10][1][game_options_sprite.selection_list[10]]
				#options.background_effects = game_options_sprite.menu_list[11][1][game_options_sprite.selection_list[11]]

				if options.bandana_physics == 'On':
					for ninja in (sprites.player1, sprites.player2, sprites.player3, sprites.player4):
						ninja.swag = 'Bandana'
						ninja.bandana.kill()
						ninja.bandana = rope_physics.Bandana_Knot(ninja, ninja.color)
						ninja.bandana.kill()

				#need to turn down current built up shake.
				sprites.shake_handler.current_shake = 0
				controls.input_handler.get_gamepads()


		

				'''
				('FPS Counter', [options.FPS_counter, get_opposite(options.FPS_counter)]),
				('Rope Physics', [options.rope_physics, get_opposite(options.rope_physics)]),
				('Bandana Physics', [options.bandana_physics, get_opposite(options.bandana_physics)]),
				('Death Animations', [options.death_animations, get_opposite(options.death_animations)]),
				('Particle Effects', ['High', 'Low', 'Off']),
				('Background Effects', ['High', 'Low', 'Off']),
				('_space_', ['']),
				('Accept', [''])
				'''

				data_manager.data_handler.save_data()


				controls.input_handler.gamepad1_update_controls()
				controls.input_handler.gamepad2_update_controls()
				controls.input_handler.gamepad3_update_controls()
				controls.input_handler.gamepad4_update_controls()



		#draw things here
		i = 0
		while i < 60:
			sprites.screen_objects.update()
			sprites.menu_sprite_list.update()
			sprites.active_sprite_list.draw(sprites.screen)
			i += options.current_fps



		


	def reset(self):
		self.menu_created = False
		#controls.input_handler.get_gamepads()
		#controls.input_handler.p1_gamepad_setup()
		#controls.input_handler.set_P1_controls = False
		
		#sprites.active_sprite_list.remove(game_options_sprite)
		#sprites.menu_sprite_list.remove(game_options_sprite)
		#sprites.screen_objects.remove(game_options_sprite)

	def load_menu(self):
		sprites.player1.controls_sprite.reset()
		sprites.reset_sprites()

		try:
			credits_handler.credits_sprite.kill()
			credits_handler.background.kill()
		except:
			pass

		game_options_sprite.vertical_selection = 0
		done = False
		while done is False:
			if game_options_sprite.vertical_selection == 0:
				while round(game_options_sprite.menu_list[0][1][game_options_sprite.selection_list[0]] * 0.1, 1) != round(options.music_volume, 1):
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 1:
				while round(game_options_sprite.menu_list[1][1][game_options_sprite.selection_list[1]] * 0.1, 1) != round(options.effects_volume, 1):
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 3:
				while game_options_sprite.menu_list[3][1][game_options_sprite.selection_list[3]] != options.control_preferences['player1']:
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 4:
				while game_options_sprite.menu_list[4][1][game_options_sprite.selection_list[4]] != options.control_preferences['player2']:
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 6:
				while game_options_sprite.menu_list[6][1][game_options_sprite.selection_list[6]] != options.FPS_counter:
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 7:
				while game_options_sprite.menu_list[7][1][game_options_sprite.selection_list[7]] != options.rope_physics:
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 8:
				while game_options_sprite.menu_list[8][1][game_options_sprite.selection_list[8]] != options.bandana_physics:
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 9:
				while game_options_sprite.menu_list[9][1][game_options_sprite.selection_list[9]] != options.visual_effects:
					game_options_sprite.scroll('right', sound = False)

			elif game_options_sprite.vertical_selection == 10:
				while game_options_sprite.menu_list[10][1][game_options_sprite.selection_list[10]] != options.screen_shake:
					game_options_sprite.scroll('right', sound = False)





			game_options_sprite.scroll('down', sound = False)
			if game_options_sprite.vertical_selection == 0:
				done = True


		
		sprites.menu_sprite_list.add(game_options_sprite)
		sprites.active_sprite_list.add(game_options_sprite)
		game_options_sprite.vertical_selection = 0



game_options_handler = Game_Options_Handler()
	

class Credits_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

		self.event_counter = 0

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()
		
		self.background.image = Build_CPU_Screen(self.background.image)
		self.background.dirty = 1
		for bar in intro_handler.matrix_bar_list:
			bar.update()
			for digit in bar.digit_list:
				digit.update(self.background.image, None) #blits to sprites.screen from within update, based on bar position.
			


		controls.input_handler.get_gamepads()




		if sprites.player1.menu_up_press is True:
			pass

		if sprites.player1.menu_down_press is True:
			pass

		if sprites.player1.menu_back_press is True or sprites.player1.menu_select_press is True:
				options.game_state = 'game_options'
				self.reset()
				sounds.mixer.menu_select.play()

		#Random Credit Events
		self.event_counter += 1

		if self.event_counter == 60 * 5:
			sprites.effects_screen.gravity(self.background)
			sounds.mixer.gravity.play()

		for ninja in sprites.ninja_list:
			if ninja.status == 'right':
				ninja.right_press()
			elif ninja.status == 'left':
				ninja.left_press()
			elif ninja.status == 'falling':
				if ninja.direction == 'right':
					ninja.right_press()
				elif ninja.direction == 'left':
					ninja.left_press()
			i = random.randrange(0,250,1)
			if i == 100:
				choice = random.choice((0,0,0,1,2,2,2))
				if choice == 0:
					ninja.left_release()
					ninja.right_press()
				elif choice == 1:
					ninja.left_release()
					ninja.right_release()
				elif choice == 2:
					ninja.right_release()
					ninja.left_press()

		for ninja in sprites.ninja_list:
			if ninja.item == 'shield':
				ninja.item_press()

			if ninja.item in ('bomb','ice_bomb'):
				choice = random.randrange(0,60,1)
				if choice == 30:
					ninja.item_press()

			if ninja.item == 'laser':
				choice = random.randrange(0,60*3,1)
				if choice == 30:
					ninja.item_press()

		if self.event_counter > 60 * 10:
			self.event_counter = 0




		#draw things here
		i = 0
		while i < 60:
			if sprites.effects_screen.status == 'gravity':
				sprites.effects_screen.update()
			else:
				sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
				sprites.enemy_list.update()
				sprites.item_effects.update()

				level.Collision_Check() #Handles Non-Tile collision checks

				sprites.tile_list.update()
				sprites.level_objects.update()
							
				sprites.level_ropes.update()
				sprites.background_objects.update()
				sprites.gravity_objects.update()
				sprites.visual_effects.update()
				sprites.screen_objects.update()


			
			#sprites.screen_objects.update()
			sprites.menu_sprite_list.update()
			i += options.current_fps
		
		sprites.active_sprite_list.draw(sprites.screen)



		


	def reset(self):
		self.event_counter = 0
		self.menu_created = False
		
		#self.credits_sprite.kill()
		#self.background.kill()
		#controls.input_handler.set_P1_controls = False
		
		#sprites.active_sprite_list.remove(game_options_sprite)
		#sprites.menu_sprite_list.remove(game_options_sprite)
		#sprites.screen_objects.remove(game_options_sprite)

	def load_menu(self):
		sprites.player1.controls_sprite.reset()


		set_default_ninjas()


		sprites.reset_sprites()

		self.credits_sprite = Credits_Sprite()

		tile = level.Tile(50, 50, 'classic', False)
		tile = level.Tile(640 - 50 - 24, 50, 'classic', False)

		tile = level.Tile(50, 360 - 50 - 24, 'classic', False)
		tile = level.Tile(640-50-24, 360 -50 - 24, 'classic', False)

		for tile in sprites.tile_list:
			for tile in sprites.tile_list:
				if tile.type == 'tile':
					tile.check_sides(mid_level = True)

		options.level_builder = level.level_builder
		options.level_builder.item_options = ('volt', 'laser', 'shield', 'bomb', 'ice bomb')
		item_spawner_left = level.Classic_Item_Spawner('left', (0,(sprites.size[1] / 2) - 15))
		item_spawner_right = level.Classic_Item_Spawner('right', (sprites.size[0] - 36,(sprites.size[1] / 2) - 15))

		
		#sprites.menu_sprite_list.add(game_options_sprite)
		#sprites.active_sprite_list.add(game_options_sprite)
		game_options_sprite.vertical_selection = 0

		self.background = level.Level_Background(-10, options.BLACK)
		sprites.menu_sprite_list.add(self.background)

		sprites.player1.place_ninja((random.randrange(0,640), random.randrange(0,360)))
		sprites.player2.place_ninja((random.randrange(0,640), random.randrange(0,360)))
		sprites.player3.place_ninja((random.randrange(0,640), random.randrange(0,360)))
		sprites.player4.place_ninja((random.randrange(0,640), random.randrange(0,360)))

		for ninja in sprites.ninja_list:
				choice = random.choice((0,1,2))
				if choice == 0:
					ninja.left_release()
					ninja.right_press()
				elif choice == 1:
					ninja.left_release()
					ninja.right_release()
				elif choice == 2:
					ninja.right_release()
					ninja.left_press()

		for ninja in sprites.ninja_list:
			ninja.loop_physics = True
		options.loop_physics = True



credits_handler = Credits_Handler()

class Credits_Sprite(pygame.sprite.DirtySprite):
	#you can jump up through platforms
	def __init__(self):
		#constructor functionf
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.image.load(os.path.join(Current_Path, 'credits.png')).convert()  
		self.image.set_colorkey(options.GREEN) 
		self.rect = self.image.get_rect()

		'''
		y = 5
		while y < self.rect.height:
			pygame.draw.line(self.image, options.BLACK, (0,y),(self.rect.width,y),2)
			y+=5
		'''


		self.rect.centerx = 320
		self.rect.top = 0
		self.dirty = 1

		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 0)
		sprites.screen_objects.add(self)

		self.change_y = 2
		self.true_y = self.rect.y

		self.move_seal = False

		self.dirty = 1

		self.unlocked = False

	def update(self):
		#keyboard input
		self.move_seal = False

		key = pygame.key.get_pressed()
		if key[pygame.K_DOWN]:
			self.move_seal = True
			self.dirty = 1
			self.true_y -= self.change_y
		elif key[pygame.K_UP]:
			self.move_seal = True
			self.dirty = 1
			self.true_y += self.change_y

		#gamepad input:
		try:
			y = 0
			if abs(controls.input_handler.gamepads[0].get_axis(controls.input_handler.p1_gamepad['stick_UD'])) > 0.5:
					if abs(controls.input_handler.gamepads[0].get_axis(controls.input_handler.p1_gamepad['stick_UD'])) / controls.input_handler.gamepads[0].get_axis(controls.input_handler.p1_gamepad['stick_UD']) ==  controls.input_handler.p1_gamepad['stick_U']:
						self.move_seal = True
						self.dirty = 1
						self.true_y += self.change_y
					else:
						self.move_seal = True
						self.dirty = 1
						self.true_y -= self.change_y
		except:
			pass

		if self.move_seal is False and sprites.transition_screen.status == 'idle':
			self.true_y -= 0.5
			self.dirty = 1



		self.rect.y = int(self.true_y)
		#correct if too far
		if self.rect.top > 0:
			self.rect.top = 0
			self.true_y = self.rect.y

		if self.rect.bottom < 360:
			self.rect.bottom = 360
			self.true_y = self.rect.y

			if self.unlocked is False:
				self.unlocked = True
				if 'Dummy' not in data_manager.data_handler.base_profile['Avatar']:
					self.test_thing = sprites.Unlock_Sprite('Dummy', unlock_type = 'avatar')


class Versus_Level_Selection_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.text_screen = None
		self.random_text = ['You have selected a RANDOM training scenario. Your arrogant human brain must foolishly consider yourself... ready.',
							'RANDOM combat training has been selected. Prepare yourself for the unkown.',
							'A RANDOM combat training scenario has been prepared. Resultant FID is... 93.7 percent likely.'
							]

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()

		#check for gamepads regularly.
		controls.input_handler.get_gamepads()




		#put menu controls / logic
		if sprites.player1.menu_y_press is True:
			sounds.mixer.menu_select.play()
			options.game_state = 'versus_options'
			self.reset()


			#if sprites.player1.menu_x_press is True:
			#	options.game_state = 'versus_mode'
			#	self.reset()

		if options.stage_selection == 'Single Stage Choice':
				if sprites.player1.menu_left_press is True:
					versus_level_selection_sprite.scroll('left')
					versus_level_selection_sprite.update()
					if options.stage_selection == 'Single Stage Choice':
						i = versus_level_selection_sprite.current_level.level_description
						self.level_text.reset(i)
					

				if sprites.player1.menu_right_press is True:
					versus_level_selection_sprite.scroll('right')
					versus_level_selection_sprite.update()
					if options.stage_selection == 'Single Stage Choice':
						i = versus_level_selection_sprite.current_level.level_description
						self.level_text.reset(i)

				if sprites.player1.menu_up_press is True:
					versus_level_selection_sprite.scroll('up')
					versus_level_selection_sprite.update()
					if options.stage_selection == 'Single Stage Choice':
						i = versus_level_selection_sprite.current_level.level_description
						self.level_text.reset(i)

				if sprites.player1.menu_down_press is True:
					versus_level_selection_sprite.scroll('down')
					versus_level_selection_sprite.update()
					if options.stage_selection == 'Single Stage Choice':
						i = versus_level_selection_sprite.current_level.level_description
						self.level_text.reset(i)


		if sprites.player1.menu_select_press is True:
					#if versus_level_selection_sprite.current_level.level_name != 'TBA':
					versus_level_selection_sprite.build_level()
					if options.game_state == 'level':
						self.reset()
						#sounds.mixer.menu_select.play()
					


		if sprites.player1.menu_back_press is True:
				options.game_state = 'player_select'
				options.game_mode = 'versus'
				self.reset()
				player_select_handler.source = 'back press'

		i = 0
		while i < 60:
			sprites.tile_list.update()
			sprites.menu_sprite_list.update()
			sprites.background_objects.update()
			sprites.screen_objects.update()
			i += options.current_fps

		
		sprites.active_sprite_list.draw(sprites.screen)

	def reset(self):
		self.menu_created = False

	def start_online_match(self, new_match = True):
		if new_match is True:
			options.duel_counter = 0
			sprites.reset_sprites()
			self.reset()
			versus_level_selection_sprite.build_level()
			sounds.mixer.menu_select.play()
			for ninja in sprites.player_list:
				ninja.reset_stats()
		else:
			sprites.reset_sprites()
			options.game_state = 'level'
			level.level_builder.level_reset()

	def load_menu(self):

		
		for ninja in sprites.player_list:
			ninja.current_wins = 0
			ninja.current_VP = 0
		

		sprites.reset_sprites() #reset all the contents of the sprites sprite groups.

		self.text_screen = level.Level_Background(-6, options.GREEN)
		self.text_screen.image.fill(options.GREEN)

		options_text = font_16.render("  : Versus Options", 0,(WHITE))
		self.text_screen.image.blit(options_text, (640 - 10 - (options_text.get_width()), 5))

		#mode_text = font_16.render("  : {} Mode".format(options.versus_mode), 0,(WHITE))
		#self.text_screen.image.blit(mode_text, (85, 5))
		
		if options.control_preferences['player1'] == 'keyboard':
			#make y_pic 'key y'
			options_pic = controls.input_handler.button_keyboard_y #sprites.level_sheet.getImage(18,300,17,17)
			#mode_pic = controls.input_handler.button_keyboard_c #sprites.level_sheet.getImage(18,300,17,17)
		else:
			options_pic = controls.input_handler.p1_gamepad['button_menu_image'] #sprites.level_sheet.getImage(0,210,17,17)
			#mode_pic = controls.input_handler.p1_gamepad['button_item_image']

		x_offset = 0
		y_offset = (options_pic.get_height() - 16) / 2

		self.text_screen.image.blit(options_pic,(640 - 10 - (options_text.get_width()) + x_offset,5 - y_offset))
		#self.text_screen.image.blit(mode_pic,(85 + x_offset,5 - y_offset))

		background = level.Level_Background(-10, 'main_menu_background.png')
		sprites.menu_sprite_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		#sprites.player1.visible = 0
		#sprites.player2.visible = 0
		#sprites.player3.visible = 0
		#sprites.player4.visible = 0


		#for sprite in sprites.menu_sprite_list:
		#	sprites.menu_sprite_list.remove(sprite)
				#create Mallow
		'''
		i = 0
		while i < 640:
			mallow = level.Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		versus_level_selection_sprite.load() #arranges levels
		sprites.menu_sprite_list.add(versus_level_selection_sprite)
		sprites.active_sprite_list.add(versus_level_selection_sprite)

		for level_icon in versus_level_selection_sprite.level_list:
			sprites.menu_sprite_list.add(level_icon)
			sprites.active_sprite_list.add(level_icon)

		sprites.menu_sprite_list.add(versus_level_selection_sprite.selection_sprite)
		sprites.active_sprite_list.add(versus_level_selection_sprite.selection_sprite)

		if options.stage_selection != 'Single Stage Choice':
			i = random.choice(self.random_text)
		else:
			i = versus_level_selection_sprite.current_level.level_description

		self.level_text = Screen_Text((10,305,sprites.size[0] - 20,50),i, 4)

		#sounds.mixer.change_song('music_classic.wav')
		#sounds.mixer.background_music.set_volume(options.music_volume)
		#sounds.mixer.background_music.play()


versus_level_selection_handler = Versus_Level_Selection_Handler()


class Coop_Level_Selection_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.text_screen = None
		self.random_text = ['You have selected a RANDOM training scenario. Your arrogant human brain must foolishly consider yourself... ready.',
							'RANDOM combat training has been selected. Prepare yourself for the unkown.',
							'A RANDOM combat training scenario has been prepared. Resultant FID is... 93.7 percent likely.'
							]

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()

		#check for gamepads regularly.
		controls.input_handler.get_gamepads()

		#put menu controls / logic
		if sprites.player1.menu_y_press is True:
			options.game_state = 'versus_options'
			self.reset()

		if options.stage_selection == 'Single Stage Choice':
			if sprites.player1.menu_left_press is True:
				coop_level_selection_sprite.scroll('left')
				coop_level_selection_sprite.update()
				if options.stage_selection == 'Single Stage Choice':
					i = coop_level_selection_sprite.current_level.level_description
					self.level_text.reset(i)
				

			if sprites.player1.menu_right_press is True:
				coop_level_selection_sprite.scroll('right')
				coop_level_selection_sprite.update()
				if options.stage_selection == 'Single Stage Choice':
					i = coop_level_selection_sprite.current_level.level_description
					self.level_text.reset(i)

			if sprites.player1.menu_up_press is True:
				coop_level_selection_sprite.scroll('up')
				coop_level_selection_sprite.update()
				if options.stage_selection == 'Single Stage Choice':
					i = coop_level_selection_sprite.current_level.level_description
					self.level_text.reset(i)

			if sprites.player1.menu_down_press is True:
				coop_level_selection_sprite.scroll('down')
				coop_level_selection_sprite.update()
				if options.stage_selection == 'Single Stage Choice':
					i = coop_level_selection_sprite.current_level.level_description
					self.level_text.reset(i)


		if sprites.player1.menu_select_press is True:
			if coop_level_selection_sprite.current_level.level_name != 'TBA':
				options.duel_counter = 0
				sprites.reset_sprites()
				self.reset()
				coop_level_selection_sprite.build_level()
				sounds.mixer.menu_select.play()
				for ninja in sprites.player_list:
					ninja.reset_stats()
				


		if sprites.player1.menu_back_press is True:
			options.game_state = 'player_select'
			player_select_handler.source = 'back press'
			#options.game_mode = 'versus'
			self.reset()

		i = 0
		while i < 60:
			sprites.tile_list.update()
			sprites.menu_sprite_list.update()
			sprites.background_objects.update()
			sprites.screen_objects.update()
			i += options.current_fps

		
		sprites.active_sprite_list.draw(sprites.screen)

	def reset(self):
		self.menu_created = False

	def load_menu(self):

		

		sprites.reset_sprites() #reset all the contents of the sprites sprite groups.

		self.text_screen = level.Level_Background(-6, options.GREEN)
		self.text_screen.image.fill(options.GREEN)

		options_text = font_16.render("Press Y for Versus Options", 0,(WHITE))
		self.text_screen.image.blit(options_text, (320 - (options_text.get_width() / 2), 5))
		
		x = 0
		for item in font_16.metrics('Press '):
			x += 8
		if options.control_preferences['player1'] == 'keyboard':
			#make y_pic 'key y'
			y_pic = controls.input_handler.button_keyboard_y #sprites.level_sheet.getImage(18,300,17,17)
		else:
			y_pic = controls.input_handler.p1_gamepad['button_menu_image'] #sprites.level_sheet.getImage(0,210,17,17)
		x_offset = (y_pic.get_width() - 8) / 2
		y_offset = (y_pic.get_height() - 16) / 2
		self.text_screen.image.blit(y_pic,(320 - (options_text.get_width() / 2) + x - x_offset,5 - y_offset))


		background = level.Level_Background(-10, 'main_menu_background.png')
		sprites.menu_sprite_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		#sprites.player1.visible = 0
		#sprites.player2.visible = 0
		#sprites.player3.visible = 0
		#sprites.player4.visible = 0


		#for sprite in sprites.menu_sprite_list:
		#	sprites.menu_sprite_list.remove(sprite)
				#create Mallow
		'''
		i = 0
		while i < 640:
			mallow = level.Mallow(0 + i, 330, False)
			i += mallow.rect.width
		'''

		sprites.menu_sprite_list.add(coop_level_selection_sprite)
		sprites.active_sprite_list.add(coop_level_selection_sprite)
		if options.stage_selection != 'Single Stage Choice':
			i = random.choice(self.random_text)
		else:
			i = versus_level_selection_sprite.current_level.level_description

		self.level_text = Screen_Text((10,300,sprites.size[0] - 20,50),i, 4)


coop_level_selection_handler = Coop_Level_Selection_Handler()


class Versus_Options_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()


		controls.input_handler.get_gamepads()

		if 1 == 1:
			if sprites.player1.menu_left_press is True:
				versus_options_sprite.scroll('left')
				if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] not in ('Return', 'Item Options'):
					if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] in ('Game Mode', 'Stage Selection'):
						self.update_text()
					self.update_options()

			if sprites.player1.menu_right_press is True:
				versus_options_sprite.scroll('right')
				if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] != 'Return':
					if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] in ('Game Mode', 'Stage Selection'):
						self.update_text()
					self.update_options()

			if sprites.player1.menu_up_press is True:
				versus_options_sprite.scroll('up')
				self.update_text()

			if sprites.player1.menu_down_press is True:
				versus_options_sprite.scroll('down')
				self.update_text()

			if sprites.player1.menu_select_press is True:
				#Check if 'Return' is selected
				if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Return':


					sounds.mixer.menu_select.play()
					options.game_state = 'versus_level_selection'
					self.reset()
					self.update_options()
					sprites.versus_match_sprite.update_text()


				if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Item Options':
					sounds.mixer.menu_select.play()
					options.game_state = 'versus_item_options'
					versus_item_options_sprite.origin_state = 'versus_options'
					self.reset()
					self.update_options()



			if sprites.player1.menu_back_press is True:


				sounds.mixer.menu_select.play()
				options.game_state = 'versus_level_selection'
				self.reset()
				self.update_options()
				sprites.versus_match_sprite.update_text()




		i = 0
		while i < 60:
			sprites.screen_objects.update()
			sprites.menu_sprite_list.update()
			sprites.background_objects.update()
			i += options.current_fps

		
		sprites.active_sprite_list.draw(sprites.screen)
		

	def update_text(self):
		text = ''

		if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Return':
			text = 'Return to the level selection screen with the current settings.'

		elif versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Game Mode':
			if versus_options_sprite.menu_list[0][1][versus_options_sprite.selection_list[0]] == 'Classic':
				text = ' A match consisting of multiple duels. Emerge victorious by collecting the most duel wins. A duel win is awarded to the final Ninja Warrior or team left standing.'
			elif versus_options_sprite.menu_list[0][1][versus_options_sprite.selection_list[0]] == 'Points':
				text = ' A match consisting of multiple duels. Emerge victorious by collecting the most Points (pts). One point is awarded for each kill. One point is deducted for each FID (Fluid Induced Dissolution).'

		elif versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Stage Selection':
			if versus_options_sprite.menu_list[1][1][versus_options_sprite.selection_list[1]] == 'Choice':
				text = 'The stage is selected from the level selection screen. The stage remains constant for the duration of the match.'
			elif versus_options_sprite.menu_list[1][1][versus_options_sprite.selection_list[1]] == 'Random':
				text = 'The stage is randomly at the beginning of each duel throughout the match.'

		elif versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Victory':
			text = 'Determines how many points/wins are required to win a match.'

		elif versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Score Frequency':
			text = 'Determines how often the score screen is displayed.'

		elif versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Item Options':
			text = 'Select this menu option to customize the level weapons that spawn in most levels.'

		
		self.screen_text.reset(text)

		#333333333333333


	def update_options(self):
		
			if versus_options_sprite.menu_list[0][1][versus_options_sprite.selection_list[0]] == 'Classic':
				options.versus_mode = 'Classic'
				
				options.versus_wins_required =  versus_options_sprite.menu_list[2][1][versus_options_sprite.selection_list[2]]


			elif versus_options_sprite.menu_list[0][1][versus_options_sprite.selection_list[0]] == 'Points':
				options.versus_mode = 'Points'
				options.versus_VP_required =  versus_options_sprite.menu_list[2][1][versus_options_sprite.selection_list[2]]

			
			if versus_options_sprite.menu_list[1][1][versus_options_sprite.selection_list[1]] == 'Choice':
				options.stage_selection = 'Single Stage Choice'
			elif versus_options_sprite.menu_list[1][1][versus_options_sprite.selection_list[1]] == 'Random':
				options.stage_selection = 'Random Each Duel'

			
			options.versus_score_frequency = versus_options_sprite.menu_list[3][1][versus_options_sprite.selection_list[3]]


		#	menus.versus_options_sprite = menus.Menu_Selection_Sprite('versus_options',(
		#	('Game Mode', ['Wins', 'Points']), 
		#	('Victory', [5,6,7,8,9,10,15,20,30,40,50,75,100,1,2,3,4]), 
		#	('Stage Selection', ['Choice', 'Random'] ),
		#	('Score Frequency', ['off',1,3,5,10] ),
		#	('Item Options', [''] ),
		#	('_space_', [''] ),
		#	('Return', [''] )
		#	),



	def reset(self):
		self.menu_created = False
		#sprites.active_sprite_list.remove(versus_options_sprite)
		#sprites.menu_sprite_list.remove(versus_options_sprite)

	def load_menu(self):
		

		'''
		temp_background_image = sprites.screen.copy()
		temp_background_image.fill((100,100,100), special_flags = pygame.BLEND_RGBA_SUB)


		versus_options_sprite.background_image = temp_background_image
		versus_item_options_sprite.background_image = temp_background_image
		'''

		

		sprites.reset_sprites()


		self.text_screen = level.Level_Background(-6, options.GREEN)
		self.text_screen.image.fill(options.GREEN)


		text = font_30.render('Versus Options', 0,options.LIGHT_PURPLE)
		height =  text.get_height() + 4
		width = text.get_width() + 4
		image = pygame.Surface((width,height))
		image.fill(options.GREEN)
		image.set_colorkey(options.GREEN)
		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2)))
		image = outline_text(image, options.LIGHT_PURPLE, options.DARK_PURPLE)

		#title_text = font_30.render("Versus Options", 0,(WHITE))
		self.text_screen.image.blit(image,(320 - (image.get_width() / 2), 20))



		background = level.Level_Background(-10, 'main_menu_background.png')
		sprites.menu_sprite_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		
		sprites.menu_sprite_list.add(versus_options_sprite)
		sprites.active_sprite_list.add(versus_options_sprite)

		self.screen_text = Screen_Text((10,360 - 100,620,90),'', 4, start_height = 10)
		#sprites.active_sprite_list.change_layer(self.screen_text, 205)
		sprites.temp_menu_list.add(self.screen_text)

		self.update_options()
		self.update_text()



versus_options_handler = Versus_Options_Handler()

class Online_Menu_Handler():
	#zzzzzzz
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

		self.menu_status = 'main'
		self.ping_counter = 0
		self.counter = 0
		self.current_player_count = 0
		self.dot_counter = 0 #jsut for 'waiting' dot
		self.current_dots = 1 #1, 2, or 3

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()

		self.dot_counter += 1
		if self.dot_counter >= 30:
			self.dot_counter = 0
			self.current_dots += 1
			if self.current_dots > 3:
				self.current_dots = 1
			

		if self.menu_status == 'main':
			controls.input_handler.get_gamepads()

			if sprites.player1.menu_left_press is True:
				online_menu_sprite.scroll('left')

			if sprites.player1.menu_right_press is True:
				online_menu_sprite.scroll('right')

			if sprites.player1.menu_up_press is True:
				online_menu_sprite.scroll('up')

			if sprites.player1.menu_down_press is True:
				online_menu_sprite.scroll('down')

			if sprites.player1.menu_select_press is True:
				#Check if 'Return' is selected
				if online_menu_sprite.menu_list[online_menu_sprite.vertical_selection][0] == 'Return':
					sounds.mixer.menu_select.play()
					options.game_state = 'player_select'
					self.reset()

				elif online_menu_sprite.menu_list[online_menu_sprite.vertical_selection][0] == 'Host Match':
					pass


				elif online_menu_sprite.menu_list[online_menu_sprite.vertical_selection][0] == 'Join Match':
					pass


				elif online_menu_sprite.menu_list[online_menu_sprite.vertical_selection][0] == 'Quick Match':
					pass

					

			if sprites.player1.menu_back_press is True:
				sounds.mixer.menu_select.play()
				options.game_state = 'player_select'
				self.reset()

		elif self.menu_status == 'waiting':

			controls.input_handler.get_gamepads()

			if sprites.player1.menu_back_press is True:


				self.load_main()






		elif self.menu_status == 'starting':
			'''
			controls.input_handler.get_gamepads()

			if sprites.player1.menu_back_press is True:
				remove_self_thread = threading.Thread(target=client.online_handler.remove_self_quick_match(self), args=())
				remove_self_thread.start()

				self.load_main
			'''


			self.counter += 1
			if self.counter > 60 * 3.5:
				options.stage_selection = 'Random Each Duel'

				
				print('starting')
				print(sprites.player_list)
				print(sprites.ninja_list)
				print(self.current_player_count)

				
				if len(sprites.player_list) < self.current_player_count:
					sprites.player_list.add(sprites.player1)
				if len(sprites.player_list) < self.current_player_count:
					sprites.player_list.add(sprites.player2)
				if len(sprites.player_list) < self.current_player_count:
					sprites.player_list.add(sprites.player3)
				if len(sprites.player_list) < self.current_player_count:
					sprites.player_list.add(sprites.player4)
				'''
					for ninja in sprites.ninja_list:
						print('made it')
						if ninja not in sprites.player_list:
							print('made it 1')
							sprites.player_list.add(ninja)
							print(len(sprites.player_list))
							print(self.current_player_count)
							break
				'''
				

				#begin!
				options.duel_counter = 0
				sprites.reset_sprites()
				self.reset()
				versus_level_selection_sprite.build_level()
				sounds.mixer.menu_select.play()
				for ninja in sprites.player_list:
					ninja.reset_stats()

		i = 0
		while i < 60:
			sprites.screen_objects.update()
			sprites.menu_sprite_list.update()
			sprites.background_objects.update()
			i += options.current_fps

		
		sprites.active_sprite_list.draw(sprites.screen)

	def reset(self):
		self.menu_created = False
		#sprites.active_sprite_list.remove(versus_options_sprite)
		#sprites.menu_sprite_list.remove(versus_options_sprite)

	def load_waiting(self):
		online_menu_sprite.visible = False
		self.counter = 0
		self.menu_status = 'waiting'

	def load_starting(self):
		online_menu_sprite.visible = False
		self.counter = 9
		self.menu_status = 'starting'

	def load_main(self):
		online_menu_sprite.visible = True
		self.menu_status = 'main'

	def load_menu(self):
		

		self.menu_status = 'main' #main, waiting
		self.ping_counter = 0
		self.counter = 0
		options.current_match_key = None
		self.current_player_count = len(sprites.player_list)
		

		'''
		temp_background_image = sprites.screen.copy()
		temp_background_image.fill((100,100,100), special_flags = pygame.BLEND_RGBA_SUB)


		versus_options_sprite.background_image = temp_background_image
		versus_item_options_sprite.background_image = temp_background_image
		'''

		

		sprites.reset_sprites()

		background = level.Level_Background(-10, 'main_menu_background.png')
		sprites.menu_sprite_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		self.level_text = Screen_Text((200,75,sprites.size[0] - 400,360 - 150),'', 4) #blank
		sprites.active_sprite_list.change_layer(self.level_text, 0)

		
		sprites.menu_sprite_list.add(online_menu_sprite)
		sprites.active_sprite_list.add(online_menu_sprite)
		online_menu_sprite.visible = True



online_menu_handler = Online_Menu_Handler()


class Versus_Mode_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.last_mode = None
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			self.menu_created = True
			self.load_menu()
			


		controls.input_handler.get_gamepads()

		if sprites.player1.menu_left_press is True:
			versus_mode_sprite.scroll('left')

		if sprites.player1.menu_right_press is True:
			versus_mode_sprite.scroll('right')

		if sprites.player1.menu_up_press is True:
			versus_mode_sprite.scroll('up')

		if sprites.player1.menu_down_press is True:
			versus_mode_sprite.scroll('down')

		if sprites.player1.menu_back_press is True:
			sounds.mixer.menu_select.play()
			self.reset()
			options.game_state = 'versus_level_selection'

		if sprites.player1.menu_select_press is True:
			#Check if 'Return' is selected

			#if versus_mode_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Accept':
			#	sounds.mixer.menu_select.play()
			#	options.game_state = 'versus_level_selection'
			#	self.reset()
			if versus_mode_sprite.menu_list[versus_mode_sprite.vertical_selection][0] == 'Classic':
				sounds.mixer.menu_select.play()
				options.versus_mode = 'Classic'
				self.reset()
				options.game_state = 'versus_level_selection'

			elif versus_mode_sprite.menu_list[versus_mode_sprite.vertical_selection][0] == 'Points':
				sounds.mixer.menu_select.play()
				options.versus_mode = 'Points'
				self.reset()
				options.game_state = 'versus_level_selection'

			elif versus_mode_sprite.menu_list[versus_mode_sprite.vertical_selection][0] == 'Stock':
				sounds.mixer.menu_select.play()
				options.versus_mode = 'Stock'
				self.reset()
				options.game_state = 'versus_level_selection'

			elif versus_mode_sprite.menu_list[versus_mode_sprite.vertical_selection][0] == 'Tutorial':
				sounds.mixer.menu_select.play()
				options.versus_mode = 'Tutorial'
				self.reset()
				options.game_state = 'level'
				level.level_builder.current_level = level.level_builder.versus_dict['Tutorial']
				level.level_builder.level_reset()

			elif versus_mode_sprite.menu_list[versus_mode_sprite.vertical_selection][0] == 'Practice':
				sounds.mixer.menu_select.play()
				options.versus_mode = 'Practice'
				self.reset()
				options.game_state = 'versus_level_selection'

		
		'''
		if sprites.player1.menu_back_press is True:
			sounds.mixer.menu_select.play()
			options.game_state = 'versus_level_selection'
			self.reset()
			#self.update_options()
		'''

		i = 0
		while i < 60:
			sprites.screen_objects.update()
			sprites.menu_sprite_list.update()
			sprites.background_objects.update()
			i += options.current_fps

		self.update_text()


		sprites.active_sprite_list.draw(sprites.screen)


	def update_text(self):
		mode = versus_mode_sprite.menu_list[versus_mode_sprite.vertical_selection][0]

		if mode != self.last_mode: #changed selection.
			if mode == 'Classic':
				text = 'A match consisting of multiple duels. Emerge victorious by collecting the most duel wins. A duel win is awarded to the final Ninja Warrior left standing. By default the match is won by earning 3 duel wins.'
			if mode == 'Points':
				text = 'A match consisting of multiple duels. Emerge victorious by collecting the most Victory Points (VP). By default 1 VP is awarded for each kill, FID inflicted, or duel win.'
			elif mode == 'Stock':
				text = 'A match consisting of a single duel. Combatants respawn following each death, so long as they have lives remaining. Emerge victorious by being the final Ninja Warrior left standing. By default Ninja Warriors begin with 3 lives.'
			elif mode == 'Practice':
				text = 'In Practice Mode Ninja Warriors respawn on death indefinitely, and a winner is never declared. Weapon options to be accessed from the pause menu. A great place for new Ninja Warriors to polish their skills.'
			elif mode == 'Tutorial':
				text = 'The Codename Mallow Tutorial Mode instructs new recruits, honing a basic dueling skill set. A great place to begin for new Ninja Warriors.'

			self.screen_text.reset(text)


		self.last_mode = mode



	def reset(self):
		self.menu_created = False
		sprites.active_sprite_list.remove(versus_mode_sprite)
		sprites.menu_sprite_list.remove(versus_mode_sprite)

	def load_menu(self):

		self.last_mode = None

		sprites.reset_sprites()

		self.text_screen = level.Level_Background(-6, options.GREEN)
		self.text_screen.image.fill(options.GREEN)

		back_text = font_16.render("  : Back", 0,(WHITE))
		self.text_screen.image.blit(back_text, (640 - 85 - (back_text.get_width()), 5))

		select_text = font_16.render("  : Select", 0,(WHITE))
		self.text_screen.image.blit(select_text, (85, 5))
		
		if options.control_preferences['player1'] == 'keyboard':
			#make y_pic 'key y'
			select_pic = controls.input_handler.button_keyboard_z #sprites.level_sheet.getImage(18,300,17,17)
			back_pic = controls.input_handler.button_keyboard_x #sprites.level_sheet.getImage(18,300,17,17)
		else:
			select_pic = controls.input_handler.p1_gamepad['button_jump_image'] #sprites.level_sheet.getImage(0,210,17,17)
			back_pic = controls.input_handler.p1_gamepad['button_roll_image']

		x_offset = 0
		y_offset = (select_pic.get_height() - 16) / 2

		self.text_screen.image.blit(back_pic,(640 - 85 - (back_text.get_width()) + x_offset,5 - y_offset))
		self.text_screen.image.blit(select_pic,(85 + x_offset,5 - y_offset))

		title_text = font_30.render("Game Modes", 0,(WHITE))
		self.text_screen.image.blit(title_text,(320 - (title_text.get_width() / 2), 85))



		background = level.Level_Background(-10, 'main_menu_background.png')
		sprites.menu_sprite_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		
		sprites.menu_sprite_list.add(versus_mode_sprite)
		sprites.active_sprite_list.add(versus_mode_sprite)

		self.screen_text = Screen_Text((10,360 - 100,620,90),'', 4)
		#sprites.active_sprite_list.change_layer(self.screen_text, 205)
		sprites.temp_menu_list.add(self.screen_text)



versus_mode_handler = Versus_Mode_Handler()


class Versus_Item_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

		self.title_text = self.get_title_text()

		self.y_text = text = font_16.render('0 : Toggle All On/Off', 0, options.WHITE)

		self.item_text_dict = {'laser' : 'The Laser item is fired horizontally across the stage. Disintegrates most opponents on contact. Unimpeded by organic materials. 3 Uses.',
								'x' : "The X item cannot be collected by Codename Mallow Ninjas. Rather, the X item bubble destroys stage platforms on contact.",
								'shoes' : 'The Shoes item immediately grants the wearer a significant boost in speed, at the expense of control. Does not expire.',
								'wings' : 'The Wings item allows Codename Mallow Ninjas the use of a second jump that may be triggered once while jumping. Does not expire.',
								'skull' : 'System memory does not contain any data on the Skull item. It likely grants Ninjas "Super Skeleton Power" on contact.',
								'bomb' : 'The Bomb bounces in the direction thrown before exploding. Thrown forward or downward (while jumping). Each Ninja may only have one active bomb at a time. 3 uses.',
								'volt' : 'Immediately surrounds the user with a powerful electric charge. Destroys most opponents on contact. DOES NOT protect user from harm. Lasts 10 earth seconds.',
								'mine' : 'Thrown forward or downward (while jumping). Turns near invisible once planted, and explodes on physical contact. Single use.',
								'rocket' : 'Hold down the -item- button to fire the Rocket item, while using directional input to steer. Explodes on contact or button release. Single use.',
								'portal gun' : "FULL VERSION ONLY. The Portal Gun creates up to 2 portals when fired against a tile/platform. The portals can be used to transport most matter between their locations. Fired forward or upward. 3 uses.",
								'ice bomb' : 'The Ice Bomb bounces in the direction thrown before exploding. Thrown forward or downward (while jumping). Temporarily freezes enemies in cubes of solid ice. Single Use.',
								'cloak' : 'The Cloak item can grant the user near perfect invisibilty. Can be toggled on/off by the user. Voids most health insurance policies. 3 uses.',
								'shield' : 'The Shield item grants the user temporary protection from most dangers. Can also reflect some attacks. Lasts 10 earth seconds once triggered. Single use.',
								'homing bomb' : 'FULL VERSION ONLY. Once activated, the homing bomb follows the user for 10 earth seconds before detonating. Can be transferred to other Ninjas via physical contact. Single use.',
								'gravity' : 'FULL VERSION ONLY. The Gravity item inverts the level gravity on use. Also inverts the polarity of level gravity fields. Not available in all stages. 3 uses.',
								'metal suit' : "FULL VERSION ONLY. The Metal Suit item grants the user greatly increased mass. Thie provides great advantage in melee encounters, at the expense of foot speed. Grants temporary access to the deadly 'Metal Pound' aerial attack. Does not expire.",
								'solar flare' : "FULL VERSION ONLY. Once triggered, the Solar Flare item charges briefly emmiting a fiercly bright flash. Causes oppenents to be disoriented for 5 earth seconds. Single use."
								}

		'''
		self.item_text_dict = {'laser' : 'The Laser item is fired horizontally across the stage. Disintegrates most opponents on contact. Unimpeded by organic materials. 3 Uses.',
								'x' : "The 'X' item cannot be collected by Codename Mallow Ninjas. Rather, the 'X' item bubble destrouys stage platforms on contact.",
								'shoes' : 'The Shoes item immediately grants the wearer a significant boost in foot speed. This is at the expense of control. Does not expire.',
								'wings' : 'The Wings item allows Codename Mallow Ninjas the use of a second jump that may be triggerd once while jumping. Does not expire.',
								'skull' : "My system memory does not contain any data on the Skull item. I calculate that it likely grants Ninjas 'Super Skeleton Power' on contact.",
								'bomb' : 'The Bomb bounces in the direction thrown before exploding. Thrown forward or downward (while jumping). Each Ninja may only have one active bomb at a time. 3 uses.',
								'volt' : 'Immediately surrounds the user with a powerful electric charge. Destroys most opponents on contact. DOES NOT protect user from harm. Lasts 10 seconds.',
								'mine' : 'Thrown forward or downward (while jumping). Turns near invisible once planted, and explodes on physical contact. Single use.',
								'rocket' : 'Hold down the -item- button to fire the Rocket item, while using directional input to steer. Explodes on contact or button release. Single use.',
								'portal gun' : "The Portal Gun creates up to 2 portals when fired against a tile/platform. The portals can be used to transport most matter between their locations. Fired forward or upward. 3 uses.",
								'ice bomb' : 'The Ice Bomb bounces in the direction thrown before exploding. Thrown forward or downward (while jumping). Temporarily freezes enemies in cubes of solid ice. Single Use.',
								'cloak' : 'The Cloak item can grant the user near perfect invisibilty. Can be toggled on/off by the user. Use voids most health insurance policies. 3 uses.',
								'shield' : 'The Shield item grants the user temporary protection from most dangers. Can also reflect some attacks. Lasts 10 seconds once triggered. Single use.',
								'homing bomb' : 'Once activated, the homing bomb follows the user for 10 seconds before detonating. Can be transferred to other Ninjas via physical contact. Single use.',
								'gravity' : 'The Gravity item inverts the level gravity on use. Also inverts the polarity of level gravity fields. Not available in all stages. 3 uses.',
								'metal suit' : "The Metal Suit item grants the user greatly increased mass. Thie provides great advantage in melee encounters, at the expense of foot speed. Grants temporary access to the deadly 'Metal Pound' aerial attack. Does not expire.",
								'solar flare' : "Once triggered, the Solar Flare item charges briefly emmiting a fiercly bright flash. Causes oppenents to be disoriented for 5 seconds. Single use."
								}
		'''


		self.last_item = None

	def update(self):
		if self.menu_created is False:
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			#sprites.transition_screen.fade(None, True, options.GREEN)
			self.menu_created = True
			self.load_menu()
			


		controls.input_handler.get_gamepads()

		#44444444444444444444444

		if sprites.player1.menu_left_press is True:
			versus_item_options_sprite.scroll('left', columns = True)

		if sprites.player1.menu_right_press is True:
			versus_item_options_sprite.scroll('right', columns = True)

		if sprites.player1.menu_up_press is True:
			versus_item_options_sprite.scroll('up')

		if sprites.player1.menu_down_press is True:
			versus_item_options_sprite.scroll('down')

		if sprites.player1.menu_y_press is True:
			versus_item_options_sprite.y_press()

		if sprites.player1.menu_select_press is True:
			#Check if 'Return' is selected
			if versus_item_options_sprite.menu_list[versus_item_options_sprite.vertical_selection][0] == 'Return':
				#sprites.transition_screen.fade_image_cheat()
				sprites.transition_screen.fade('swipe_down', True, options.GREEN)
				sounds.mixer.menu_select.play()
				#options.game_state = 'versus_options'
				options.game_state = versus_item_options_sprite.origin_state
				self.update_options()
				self.reset()

			else:
				versus_item_options_sprite.scroll('right') #only two options, could be 'right' or 'left'

		if sprites.player1.menu_back_press is True:
			#sprites.transition_screen.fade_image_cheat()
			sprites.transition_screen.fade('swipe_down', True, options.GREEN)
			sounds.mixer.menu_select.play()
			#options.game_state = 'versus_options'
			options.game_state = versus_item_options_sprite.origin_state
			self.update_options()
			self.reset()


		i = 0
		while i < 60:
			sprites.temp_menu_list.update()
			sprites.transition_screen.update()

			'''
			for sprite in sprites.temp_menu_list:
				sprite.update()
			
			sprites.screen_objects.update()
			sprites.menu_sprite_list.update()
			sprites.level_objects.update()
			sprites.background_objects.update()
			'''
			i += options.current_fps

		versus_item_options_sprite.image.blit(self.title_text, (320 - (self.title_text.get_width() / 2),20))
		versus_item_options_sprite.image.blit(self.y_text, (640 - self.y_text.get_width() - 5,5))
		versus_item_options_sprite.image.blit(self.y_button_image, (640 - self.y_text.get_width() - 6,4))

		sprites.active_sprite_list.draw(sprites.screen)

	def get_title_text(self):
		text = font_30.render('Item Options', 0,options.LIGHT_PURPLE)

		height =  text.get_height() + 4
		width = text.get_width() + 4


		image = pygame.Surface((width,height))
		image.fill(options.GREEN)
		image.set_colorkey(options.GREEN)

		image.blit(text, ((image.get_width() / 2) - (text.get_width() / 2), (image.get_height() / 2) - (text.get_height() / 2)))

		image = outline_text(image, options.LIGHT_PURPLE, options.DARK_PURPLE)

		return(image)

	def update_options(self):
		
		i = versus_item_options_sprite.menu_list[0][0] #'x' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[0][1][versus_item_options_sprite.selection_list[0]]
		i = versus_item_options_sprite.menu_list[1][0] #'shoes' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[1][1][versus_item_options_sprite.selection_list[1]]
		i = versus_item_options_sprite.menu_list[2][0] #'laser' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[2][1][versus_item_options_sprite.selection_list[2]]
		i = versus_item_options_sprite.menu_list[3][0] #'wings' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[3][1][versus_item_options_sprite.selection_list[3]]
		i = versus_item_options_sprite.menu_list[4][0] #skull' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[4][1][versus_item_options_sprite.selection_list[4]]
		i = versus_item_options_sprite.menu_list[5][0] #'bomb' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[5][1][versus_item_options_sprite.selection_list[5]]
		i = versus_item_options_sprite.menu_list[6][0] #'volt' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[6][1][versus_item_options_sprite.selection_list[6]]
		i = versus_item_options_sprite.menu_list[7][0] #'mine' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[7][1][versus_item_options_sprite.selection_list[7]]
		i = versus_item_options_sprite.menu_list[8][0] #'rocket' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[8][1][versus_item_options_sprite.selection_list[8]]
		

		i = versus_item_options_sprite.menu_list[9][0] #'shield' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[9][1][versus_item_options_sprite.selection_list[9]]
		i = versus_item_options_sprite.menu_list[10][0] #'ice bomb' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[10][1][versus_item_options_sprite.selection_list[10]]
		i = versus_item_options_sprite.menu_list[11][0] #'cloak' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[11][1][versus_item_options_sprite.selection_list[11]]
		

		i = versus_item_options_sprite.menu_list[12][0] #'portal gun' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[12][1][versus_item_options_sprite.selection_list[12]]
		i = versus_item_options_sprite.menu_list[13][0] #'homing bomb' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[13][1][versus_item_options_sprite.selection_list[13]]
		i = versus_item_options_sprite.menu_list[14][0] #'metal suit' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[14][1][versus_item_options_sprite.selection_list[14]]
		i = versus_item_options_sprite.menu_list[15][0] #'folar flare' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[15][1][versus_item_options_sprite.selection_list[15]]
		i = versus_item_options_sprite.menu_list[16][0] #'gravity' on/off
		options.items_dict[i] = versus_item_options_sprite.menu_list[16][1][versus_item_options_sprite.selection_list[16]]

	def reset(self):
		self.menu_created = False

		sprites.temp_menu_list.remove(versus_item_options_sprite)
		sprites.active_sprite_list.remove(versus_item_options_sprite)

		for sprite in sprites.temp_menu_list:
			sprite.kill()

		self.last_item = None
		#sprites.active_sprite_list.remove(versus_item_options_sprite)
		#sprites.menu_sprite_list.remove(versus_item_options_sprite)

		#update item bubbles if in level
		for sprite in sprites.level_objects:
			if sprite.type in ('spawn_point', 'classic_spawn_point'):
				for bubble in sprite.bubble_list:
					if bubble.item_locked is False:
						bubble.item_options = []
						for item in options.items_dict:
							if options.items_dict[item] == 'on' and item not in options.banned_items:
								bubble.item_options.append(item)
						if bubble.visible is True:
							if bubble.item not in bubble.item_options:
								bubble.queue_pop = True
						#Bonus for clssic_Spawn_point mid spawn:
						if sprite.type == 'classic_spawn_point':
							if sprite.status == 'spawn':
								sprite.reset()
		
		#now for the mallow wall
		for sprite in sprites.tile_list:
			if sprite.type == 'mallow_wall':
				for bubble in sprite.bubble_list:
					bubble.item_options = []
					for item in options.items_dict:
						if options.items_dict[item] == 'on' and item not in options.banned_items:
							bubble.item_options.append(item)
					if bubble.visible is True:
						if bubble.item not in bubble.item_options:
							bubble.queue_pop = True

	def update_screen_text(self, item):
		if self.last_item != item:
			try:
				text = self.item_text_dict[item[0]]
			except:
				text = ''

			self.screen_text.reset(text)

		self.last_item = item

	def load_menu(self):
		self.last_item = None

		#temp_menu_sprites = pygame.sprite.LayeredDirty() #holds sprites for menus occasionally (versus items)
		#temp_menu_sprites.clear(sprites.screen, sprites.background)

		#if versus_item_options_sprite.origin_state == 'versus_options': 
		#sprites.reset_sprites()

		sprites.temp_menu_list.add(versus_item_options_sprite)
		sprites.active_sprite_list.add(versus_item_options_sprite)
		sprites.active_sprite_list.change_layer(versus_item_options_sprite, 200)

		versus_item_options_sprite.bubble_switch = True #Triggers creation of item bubbles based on menu text.

		background = level.Level_Background(190, 'main_menu_background.png')
		sprites.temp_menu_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		sprites.active_sprite_list.change_layer(background_laser, 195)
		sprites.temp_menu_list.add(background_laser)
		background_laser = level.Background_Laser('vertical', (156,120))
		sprites.active_sprite_list.change_layer(background_laser, 195)
		sprites.temp_menu_list.add(background_laser)
		background_laser = level.Background_Laser('vertical', (75,240))
		sprites.active_sprite_list.change_layer(background_laser, 195)
		sprites.temp_menu_list.add(background_laser)

		background_laser = level.Background_Laser('horizontal', (0,77))
		sprites.active_sprite_list.change_layer(background_laser, 195)
		sprites.temp_menu_list.add(background_laser)
		background_laser = level.Background_Laser('horizontal', (213,239))
		sprites.active_sprite_list.change_layer(background_laser, 195)
		sprites.temp_menu_list.add(background_laser)
		background_laser = level.Background_Laser('horizontal', (427,320))
		sprites.active_sprite_list.change_layer(background_laser, 195)
		sprites.temp_menu_list.add(background_laser)

		self.screen_text = Screen_Text((10,360 - 100,620,90),'', 4)
		sprites.active_sprite_list.change_layer(self.screen_text, 205)
		sprites.temp_menu_list.add(self.screen_text)

		if sprites.player1 == controls.input_handler.gamepad1_ninja:
			self.y_button_image = sprites.player1.gamepad_layout['button_menu_image']
		else:
			self.y_button_image = controls.input_handler.button_keyboard_y

		versus_item_options_sprite.set_options()

		'''
		sprites.menu_sprite_list.add(versus_item_options_sprite)
		sprites.active_sprite_list.add(versus_item_options_sprite)

		versus_item_options_sprite.bubble_switch = True #Triggers creation of item bubbles based on menu text.

		background = level.Level_Background(-10, 'main_menu_background.png')
		sprites.menu_sprite_list.add(background)
		background.dirty = 1

		#self.text_screen = level.Level_Background(-6, options.GREEN)

		background_laser = level.Background_Laser('vertical', (480,0))
		background_laser = level.Background_Laser('vertical', (156,120))
		background_laser = level.Background_Laser('vertical', (75,240))

		background_laser = level.Background_Laser('horizontal', (0,77))
		background_laser = level.Background_Laser('horizontal', (213,239))
		background_laser = level.Background_Laser('horizontal', (427,320))

		self.screen_text = Screen_Text((10,360 - 100,620,90),'', 4)

		if sprites.player1 == controls.input_handler.gamepad1_ninja:
			self.y_button_image = sprites.player1.gamepad_layout['button_menu_image']
		else:
			self.y_button_image = controls.input_handler.button_keyboard_y
		'''

versus_item_handler = Versus_Item_Handler()

'''
def versus_options():
	#check for gamepads regularly.
	controls.input_handler.get_gamepads()

	if sprites.player1.menu_left_press is True:
		versus_options_sprite.scroll('left')

	if sprites.player1.menu_right_press is True:
		versus_options_sprite.scroll('right')

	if sprites.player1.menu_up_press is True:
		versus_options_sprite.scroll('up')

	if sprites.player1.menu_down_press is True:
		versus_options_sprite.scroll('down')

	if sprites.player1.menu_select_press is True:
		#Check if 'Return' is selected
		if versus_options_sprite.menu_list[versus_options_sprite.vertical_selection][0] == 'Return':
			sounds.mixer.menu_select.play()
			options.game_state = 'versus_level_selection'


			#build/change options.py settings.

			options.versus_wins_needed = versus_options_sprite.menu_list[0][1][versus_options_sprite.selection_list[0]]
			options.platform_density = versus_options_sprite.menu_list[1][1][versus_options_sprite.selection_list[1]]
			options.item_spawn_rate = versus_options_sprite.menu_list[2][1][versus_options_sprite.selection_list[2]]

			i = versus_options_sprite.menu_list[4][0] #'x' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[4][1][versus_options_sprite.selection_list[4]]
			i = versus_options_sprite.menu_list[5][0] #'shoes' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[5][1][versus_options_sprite.selection_list[5]]
			i = versus_options_sprite.menu_list[6][0] #'laser' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[6][1][versus_options_sprite.selection_list[6]]
			i = versus_options_sprite.menu_list[7][0] #'wings' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[7][1][versus_options_sprite.selection_list[7]]
			i = versus_options_sprite.menu_list[8][0] #skull' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[8][1][versus_options_sprite.selection_list[8]]
			i = versus_options_sprite.menu_list[9][0] #'bomb' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[9][1][versus_options_sprite.selection_list[9]]
			i = versus_options_sprite.menu_list[10][0] #'volt' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[10][1][versus_options_sprite.selection_list[10]]
			i = versus_options_sprite.menu_list[11][0] #'mine' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[11][1][versus_options_sprite.selection_list[11]]
			i = versus_options_sprite.menu_list[12][0] #'rocket' on/off
			options.items_dict[i] = versus_options_sprite.menu_list[12][1][versus_options_sprite.selection_list[12]]


	screen = sprites.screen

	for sprite in sprites.menu_sprite_list:
		sprites.menu_sprite_list.remove(sprite)

	sprites.menu_sprite_list.add(versus_options_sprite)

	sprites.menu_sprite_list.update()
	sprites.menu_sprite_list.draw(screen)
'''
class Instruction_Booklet_Sprite(pygame.sprite.DirtySprite):
	def __init__(self):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.image_list = []
		# Load the sprite sheet.
		image = pygame.image.load(os.path.join(Current_Path, 'InstructionBookletCover.png')).convert()
		self.image_list.append(image)
		image = pygame.image.load(os.path.join(Current_Path, 'InstructionBookletPage1-2.png')).convert()
		self.image_list.append(image)
		image = pygame.image.load(os.path.join(Current_Path, 'InstructionBookletPage3-4.png')).convert()
		self.image_list.append(image)
		image = pygame.image.load(os.path.join(Current_Path, 'InstructionBookletPage5-6.png')).convert()
		self.image_list.append(image)


		self.image_number = 0
		self.image = self.image_list[self.image_number]

		self.glitch_timer = 0
		self.page_direction = 0 #0 means no move locked.

		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()

		controls.input_handler.get_gamepads()

		if self.page_direction == 0: #no moved locked
			if sprites.player1.menu_left_press is True:
				if self.image_number != 0:
					if options.screen_shake == 'On':
						self.page_direction = -1
						self.glitch_timer = 10
						#self.scroll(-1)
					else:
						self.scroll(-1)

			if sprites.player1.menu_right_press is True:
				if self.image_number != len(self.image_list) - 1:
					if options.screen_shake == 'On':
						self.page_direction = 1
						self.glitch_timer = 10
						#self.scroll(1)
					else:
						self.scroll(1)

		if sprites.player1.menu_back_press is True:
			sounds.mixer.menu_select.play()
			controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
			options.game_state = 'main_menu'
			main_menu_handler.add_menu = True
			self.reset()

		
		if self.glitch_timer != 0:
			self.glitch_timer -= 1
			
			
			if (self.page_direction == 0 and self.glitch_timer >= 7) or (self.page_direction != 0 and self.glitch_timer <= 2): #static
				self.image = self.image.copy()
				if self.glitch_timer % 2 == 0: #even number
					self.image.blit(intro_handler.static_image1,(0,0))
					self.dirty = 1
				else:
					self.image.blit(intro_handler.static_image2,(0,0))
					self.dirty = 1

			
			else:
				choice = random.choice((1,2))
				if choice == 0:
					self.image = self.image_list[self.image_number].copy()
					vertical_glitch(self.image)
					self.dirty = 1
				elif choice == 1:
					self.image = self.image_list[self.image_number].copy()
					shift_glitch(self.image, 'left')
					self.dirty = 1
				elif choice == 2:
					self.image = self.image_list[self.image_number].copy()
					shift_glitch(self.image, 'right')
					self.dirty = 1

			if self.glitch_timer == 0:
				if self.page_direction != 0:
					self.scroll(self.page_direction)
					self.page_direction = 0
				else:	
					self.image = self.image_list[self.image_number].copy()
					self.dirty = 1

		main_menu_handler.update()

		'''
		#sprites.background_objects.update()
		i = 0
		while i < 60:
			#sprites.menu_sprite_list.update()
			#sprites.transition_screen.update()	
			i += options.current_fps




		sprites.active_sprite_list.draw(sprites.screen)
		'''


	def scroll(self, number):
		last_number = self.image_number 

		self.image_number += number
		if self.image_number < 0:
			self.image_number = 0
		if self.image_number > len(self.image_list) - 1:
			self.image_number = len(self.image_list) - 1

		if last_number != self.image_number:
			if options.screen_shake == 'On':
				self.glitch_timer = 10
			
			self.image = self.image_list[self.image_number]
			self.rect = self.image.get_rect()
			self.rect.center = (320,180)

			if self.image_number == 0:
				self.left_arrow.reset()

			else:
				self.left_arrow.activate((self.rect.left - 15, self.rect.centery))

			if self.image_number == len(self.image_list) - 1:
				self.right_arrow.reset()
			else:
				self.right_arrow.activate((self.rect.right + 15, self.rect.centery))

			self.dirty = 1





	def reset(self):
		self.visible = 0
		self.dirty = 1
		self.menu_created = False
		sprites.active_sprite_list.remove(self)
		#sprites.menu_sprite_list.remove(self)

		#sprites.player1.controls_sprite.reset()
		#sprites.player2.controls_sprite.reset()
		#sprites.player3.controls_sprite.reset()
		#sprites.player4.controls_sprite.reset()
		sprites.pause_background.reset()

		self.left_arrow.kill()
		self.right_arrow.kill()

	def load_menu(self):
		if options.screen_shake == 'On':
			self.glitch_timer = 10
		self.page_direction = 0

		self.image_number = 0
		self.image = self.image_list[self.image_number]
		self.rect = self.image.get_rect()
		self.rect.center = (320,180)
		self.dirty = 1
		self.visible = 1

		for sprite in sprites.menu_sprite_list:
			sprites.menu_sprite_list.remove(sprite)


		self.left_arrow = sprites.Menu_Arrow((self.rect.left - 15, self.rect.centery), 'left', None, None)
		sprites.background_objects.add(self.left_arrow)
		sprites.active_sprite_list.add(self.left_arrow)
		sprites.active_sprite_list.change_layer(self.left_arrow, 90)

		self.right_arrow = sprites.Menu_Arrow((self.rect.right + 15, self.rect.centery), 'right', None, None)
		self.right_arrow.activate()
		sprites.background_objects.add(self.right_arrow)
		sprites.active_sprite_list.add(self.right_arrow)
		sprites.active_sprite_list.change_layer(self.right_arrow, 90)


		#sprites.menu_sprite_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self, 90)
		

		sprites.pause_background.activate()




class Pause_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()

		controls.input_handler.get_gamepads()

		for ninja in sprites.player_list:
			if ninja.menu_up_press is True:
				if options.pause_item_options is False:
					pause_sprite.scroll('up')
				else:
					pause_sprite_items.scroll('up')

			if ninja.menu_down_press is True:
				if options.pause_item_options is False:
					pause_sprite.scroll('down')
				else:
					pause_sprite_items.scroll('down')

			if ninja.menu_select_press is True:
				if options.pause_item_options is False:
					if pause_sprite.menu_list[pause_sprite.vertical_selection][0] == 'Quit Game':
						sounds.mixer.menu_select.play()

						if options.game_mode == 'versus':
							options.game_state = 'versus_level_selection'
						else:
							options.game_state = 'coop_level_selection'
						#sounds.mixer.change_song('music_menu.wav')
						#sounds.mixer.start_song()

						self.reset()
						level.level_builder.level_reset()


						#sounds.mixer.background_music.stop()
						sounds.mixer.change_song('music_menu.wav')
						sounds.mixer.start_song()

					elif pause_sprite.menu_list[pause_sprite.vertical_selection][0] == 'Resume':
						sounds.mixer.menu_select.play()
						controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
						options.game_state = 'level'
						self.reset()

				else:
					if pause_sprite_items.menu_list[pause_sprite_items.vertical_selection][0] == 'Quit Game':
						sounds.mixer.menu_select.play()
						
						if options.game_mode == 'versus':
							options.game_state = 'versus_level_selection'
						elif options.game_mode == 'online':
							options.game_state = 'player_select'
						else:
							options.game_state = 'coop_level_selection'
						#sounds.mixer.change_song('music_menu.wav')
						#sounds.mixer.start_song()

						self.reset()
						level.level_builder.level_reset()
						
						#sounds.mixer.background_music.stop()
						sounds.mixer.change_song('music_menu.wav')
						sounds.mixer.start_song()
						#sounds.mixer.background_music.set_volume(options.music_volume)
						#sounds.mixer.background_music.play()

						#9999999

					elif pause_sprite_items.menu_list[pause_sprite_items.vertical_selection][0] == 'Item Options':
						sounds.mixer.menu_select.play()
						sprites.transition_screen.fade('swipe_down', True, options.GREEN)
						controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
						options.game_state = 'versus_item_options'
						versus_item_options_sprite.origin_state = 'pause'
						self.reset()

					elif pause_sprite_items.menu_list[pause_sprite_items.vertical_selection][0] == 'Resume':
						sounds.mixer.menu_select.play()
						controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
						options.game_state = 'level'
						self.reset()



		#sprites.background_objects.update()
		i = 0
		while i < 60:
			sprites.menu_sprite_list.update()
			sprites.transition_screen.update()	
			i += options.current_fps




		sprites.active_sprite_list.draw(sprites.screen)


	def reset(self):
		sprites.versus_match_sprite.reset()
		self.menu_created = False
		sprites.active_sprite_list.remove(pause_sprite)
		sprites.menu_sprite_list.remove(pause_sprite)
		sprites.active_sprite_list.remove(pause_sprite_items)
		sprites.menu_sprite_list.remove(pause_sprite_items)
		#sounds.mixer.background_music.play()
		if options.game_state == 'level':
			pygame.mixer.unpause()

		sprites.player1.controls_sprite.reset()
		sprites.player2.controls_sprite.reset()
		sprites.player3.controls_sprite.reset()
		sprites.player4.controls_sprite.reset()
		sprites.pause_background.reset()

	def load_menu(self):
		

		for sprite in sprites.menu_sprite_list:
			sprites.menu_sprite_list.remove(sprite)

		
		if options.pause_item_options is True:
			sprites.versus_match_sprite.activate()
			sprites.menu_sprite_list.add(pause_sprite_items) #use special pause sprite with items options.
			sprites.active_sprite_list.add(pause_sprite_items)
			sprites.active_sprite_list.change_layer(pause_sprite_items, 90)
		else:
			sprites.versus_match_sprite.activate()
			sprites.menu_sprite_list.add(pause_sprite)
			sprites.active_sprite_list.add(pause_sprite)
			sprites.active_sprite_list.change_layer(pause_sprite, 90)
		
		pause_sprite.visible = 1
		#sounds.mixer.background_music.stop()
		pygame.mixer.pause()

		if sprites.player1 in sprites.player_list:
			sprites.player1.controls_sprite.activate((12,280))

		if sprites.player2 in sprites.player_list:
			sprites.player2.controls_sprite.activate((12 + sprites.player2.controls_sprite.rect.width + 30,280))

		if sprites.player3 in sprites.player_list:
			sprites.player3.controls_sprite.activate((640 - 12 - (sprites.player3.controls_sprite.rect.width * 2) - 30,280))

		if sprites.player4 in sprites.player_list:
			sprites.player4.controls_sprite.activate((640 - 12 - sprites.player4.controls_sprite.rect.width,280))

		sprites.pause_background.activate()

pause_handler = Pause_Handler()

class Online_Pause_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		self.current_pause_sprite = None

		
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()



		#sprites.background_objects.update()
		#i = 0
		#while i < 60:
		#	sprites.menu_sprite_list.update()
		#	sprites.transition_screen.update()	
		#	i += options.current_fps

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
				sprites.menu_sprite_list.update()
				#sprites.transition_screen.update()	

				
				sprites.ninja_list.update() #Tile collision checks handled within each ninja.self
				sprites.enemy_list.update()

				if sprites.countdown_timer.done is True:
					level.Collision_Check() #Handles Non-Tile collision checks

				sprites.tile_list.update()
								
				if sprites.countdown_timer.level_go is True:
					sprites.level_objects.update()
				sprites.item_effects.update()
				sprites.level_ropes.update()
				sprites.background_objects.update()
				sprites.gravity_objects.update()
				sprites.visual_effects.update()
				sprites.screen_objects.update()



			i += options.current_fps
			#if i < 60:
			#controls.input_handler.update() #need to update controls a second time to keep movement/frames the same
				

		controls.input_handler.get_gamepads()

		for ninja in sprites.player_list:
			if ninja.online_type == 'local':
				if ninja.menu_up_press is True:
					self.current_pause_sprite.scroll('up')

				if ninja.menu_down_press is True:
					self.current_pause_sprite.scroll('down')

				if ninja.menu_select_press is True:
					if self.current_pause_sprite.menu_list[self.current_pause_sprite.vertical_selection][0] == 'Level Select':
							sounds.mixer.menu_select.play()
							options.game_state = 'versus_level_selection'
							self.reset()
							level.level_builder.level_reset()
							#sounds.mixer.background_music.stop()
							sounds.mixer.change_song('music_menu.wav')
							sounds.mixer.start_song()
							



					elif self.current_pause_sprite.menu_list[self.current_pause_sprite.vertical_selection][0] == 'Resume':
							self.reset()
							sounds.mixer.menu_select.play()
							controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
							options.game_state = 'level'
							

					elif self.current_pause_sprite.menu_list[self.current_pause_sprite.vertical_selection][0] == 'Quit Online':

							self.reset()
							sounds.mixer.menu_select.play()
							options.game_state = 'main_menu'
							#options.game_state = 'player_select'
							

							level.level_builder.level_reset()
							#sounds.mixer.background_music.stop()
							sounds.mixer.change_song('music_menu.wav')
							sounds.mixer.start_song()



							for ninja in sprites.player_list:
								if ninja.online_type == 'online':
									ninja.reset_name()
									ninja.online_type = 'local'
									ninja.menu_status = 'join'
									sprites.ninja_list.remove(ninja)
									sprites.active_sprite_list.remove(ninja)
									sprites.player_list.remove(ninja)
									#sounds.mixer.menu_move.play()
									ninja.activate_death_sprite('skull', ninja)
									ninja.lose()



		sprites.active_sprite_list.draw(sprites.screen)


	def reset(self):
		sprites.versus_match_sprite.reset()
		self.menu_created = False
		sprites.active_sprite_list.remove(self.current_pause_sprite)
		sprites.menu_sprite_list.remove(self.current_pause_sprite)
		sprites.active_sprite_list.remove(self.current_pause_sprite)
		sprites.menu_sprite_list.remove(self.current_pause_sprite)
		#sounds.mixer.background_music.play()
		#if options.game_state == 'level':
		#	pygame.mixer.unpause()

		sprites.player1.controls_sprite.reset()
		sprites.player2.controls_sprite.reset()
		sprites.player3.controls_sprite.reset()
		sprites.player4.controls_sprite.reset()
		sprites.pause_background.reset()

	def load_menu(self):
		

		for sprite in sprites.menu_sprite_list:
			sprites.menu_sprite_list.remove(sprite)

		
		sprites.versus_match_sprite.activate()
		sprites.menu_sprite_list.add(pause_sprite_online_host)
		sprites.active_sprite_list.add(pause_sprite_online_host)
		pause_sprite_online_host.visible = 1
		self.current_pause_sprite = pause_sprite_online_host


		sprites.active_sprite_list.change_layer(self.current_pause_sprite, 90)
		
		
		#sounds.mixer.background_music.stop()
		#pygame.mixer.pause()

		if sprites.player1 in sprites.player_list:
			if sprites.player1.online_type == 'local':
				sprites.player1.controls_sprite.activate((12,280))

		if sprites.player2 in sprites.player_list:
			if sprites.player2.online_type == 'local':
				sprites.player2.controls_sprite.activate((12 + sprites.player2.controls_sprite.rect.width + 30,280))

		if sprites.player3 in sprites.player_list:
			if sprites.player3.online_type == 'local':
				sprites.player3.controls_sprite.activate((640 - 12 - (sprites.player3.controls_sprite.rect.width * 2) - 30,280))

		if sprites.player4 in sprites.player_list:
			if sprites.player4.online_type == 'local':
				sprites.player4.controls_sprite.activate((640 - 12 - sprites.player4.controls_sprite.rect.width,280))

		sprites.pause_background.activate()

online_pause_handler = Online_Pause_Handler()

'''
class Tutorial_Pause_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()

		controls.input_handler.get_gamepads()

		for ninja in sprites.player_list:
			if ninja.menu_up_press is True:
				pause_sprite.scroll('up')

			if ninja.menu_down_press is True:
				pause_sprite.scroll('down')

			if ninja.menu_select_press is True:
				if pause_sprite.menu_list[pause_sprite.vertical_selection][0] == 'Quit Game':
					sounds.mixer.menu_select.play()
					#sounds.mixer.change_song('music_menu.wav')
					#sounds.mixer.start_song()
					options.game_state = 'main_menu'
					self.reset()
					sounds.mixer.background_music.stop()

				elif pause_sprite.menu_list[pause_sprite.vertical_selection][0] == 'Resume':
					sounds.mixer.menu_select.play()
					controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
					options.game_state = 'level'
					self.reset()


		sprites.menu_sprite_list.update()
		sprites.active_sprite_list.draw(sprites.screen)


	def reset(self):
		sprites.versus_match_sprite.reset()
		self.menu_created = False
		sprites.active_sprite_list.remove(pause_sprite)
		sprites.menu_sprite_list.remove(pause_sprite)
		#sounds.mixer.background_music.play()
		pygame.mixer.unpause()

		sprites.player1.controls_sprite.reset()
		sprites.player2.controls_sprite.reset()
		sprites.player3.controls_sprite.reset()
		sprites.player4.controls_sprite.reset()
		sprites.pause_background.reset()

	def load_menu(self):
		sprites.versus_match_sprite.activate()

		for sprite in sprites.menu_sprite_list:
			sprites.menu_sprite_list.remove(sprite)

		sprites.menu_sprite_list.add(pause_sprite)
		sprites.active_sprite_list.add(pause_sprite)
		sprites.active_sprite_list.change_layer(pause_sprite, 90)
		pause_sprite.visible = 1
		#sounds.mixer.background_music.stop()
		pygame.mixer.pause()

		if sprites.player1 in sprites.player_list:
			sprites.player1.controls_sprite.activate((12,280))

		if sprites.player2 in sprites.player_list:
			sprites.player2.controls_sprite.activate((12 + sprites.player2.controls_sprite.rect.width + 30,280))

		if sprites.player3 in sprites.player_list:
			sprites.player3.controls_sprite.activate((640 - 12 - (sprites.player3.controls_sprite.rect.width * 2) - 30,280))

		if sprites.player4 in sprites.player_list:
			sprites.player4.controls_sprite.activate((640 - 12 - sprites.player4.controls_sprite.rect.width,280))

		sprites.pause_background.activate()

tutorial_pause_handler = Tutorial_Pause_Handler()
'''		

class Choice_Handler():
	def __init__(self):
		self.menu_created = False #menu needs to be loaded.
		#self.script_choice = 0
		#self.script_timer = 0
		#self.fade_done = False

		self.text = '' #holds text for question / choice
		self.response_text = None
		self.player_list = [] #holds which players will be choosing

		self.choice_left = None #can be image OR text OR ninja (will then build image and use name_sprite)
		self.choice_right = None
		self.choice_top = None
		self.choice_bottom = None

		#create lists to hold ninjas in each choice. Ordered.
		self.top_list = []
		self.bottom_list = []
		self.left_list = []
		self.right_list = []

		self.stock = 4 #how many times each choice can be selected
		self.status = 'text' #test or response

		self.rect = pygame.Rect(320 - 160,100 - 8,320,150 + 16)

		self.text_dict = {
							'Stage1_1.0' : 'To maximize your potential as a team, a leader must be chosen from amongst you. Please select who you believe would best fill this role.'.format('Ancalabro')
							
							}

	def update(self):
		if self.menu_created is False:
			self.menu_created = True
			self.load_menu()

		controls.input_handler.get_gamepads()

		if self.next_game_state == 'player_select':
			if sprites.player1.menu_select_press is True:
				#print('made it')
				#print(self.choice_text.status)
				if self.choice_text.status == 'done':
					self.reset()

				elif self.choice_text.status == 'active':
					self.choice_text.finish_text_bars()

				
		else:
			for ninja in sprites.player_list:
				if ninja.menu_select_press is True:
					if self.choice_text.status == 'active':
						self.choice_text.finish_text_bars()

					else: #done
						if self.status == 'response':
							self.reset()

		for ninja in self.player_list:
			
			#if ninja.menu_up_press is True:
			#	pause_sprite.scroll('up')

			#if ninja.menu_down_press is True:
			#	pause_sprite.scroll('down')

			if self.choice_text.status == 'done':
				if ninja.menu_up_press is True and len(self.top_list) < self.stock and self.choice_top != None:
					self.top_list.append(ninja)
					for ninja in self.top_list:
						i = self.top_list.index(ninja)
						ninja.choice_bar.activate('normal', self.top_dict[len(self.top_list)][i][0], self.top_dict[len(self.top_list)][i][1])
					self.player_list.remove(ninja)
					for arrow in self.arrow_list:
						if arrow.rect.colliderect(ninja.choice_bar.rect):
							arrow.rect.centery = ninja.choice_bar.rect.top - 11
							arrow.dirty = 1

				elif ninja.menu_down_press is True and len(self.bottom_list) < self.stock and self.choice_bottom != None:
					self.bottom_list.append(ninja)
					for ninja in self.bottom_list:
						i = self.bottom_list.index(ninja)
						ninja.choice_bar.activate('normal', self.bottom_dict[len(self.bottom_list)][i][0], self.bottom_dict[len(self.bottom_list)][i][1])
					self.player_list.remove(ninja)
					for arrow in self.arrow_list:
						if arrow.rect.colliderect(ninja.choice_bar.rect):
							arrow.rect.centery = ninja.choice_bar.rect.bottom + 10
							arrow.dirty = 1

				elif ninja.menu_left_press is True and len(self.left_list) < self.stock and self.choice_left != None:
					self.left_list.append(ninja)
					for ninja in self.left_list:
						i = self.left_list.index(ninja)
						ninja.choice_bar.activate('left', self.left_dict[len(self.left_list)][i][0], self.left_dict[len(self.left_list)][i][1])
					self.player_list.remove(ninja)
					for arrow in self.arrow_list:
						if arrow.rect.colliderect(ninja.choice_bar.rect):
							arrow.rect.centerx = ninja.choice_bar.rect.left - 11
							arrow.dirty = 1

				elif ninja.menu_right_press is True and len(self.right_list) < self.stock and self.choice_right != None:
					self.right_list.append(ninja)
					for ninja in self.right_list:
						i = self.right_list.index(ninja)
						ninja.choice_bar.activate('right', self.right_dict[len(self.right_list)][i][0], self.right_dict[len(self.right_list)][i][1])
					self.player_list.remove(ninja)
					for arrow in self.arrow_list:
						if arrow.rect.colliderect(ninja.choice_bar.rect):
							arrow.rect.centerx = ninja.choice_bar.rect.right + 10
							arrow.dirty = 1


		if len(self.player_list) == 0 and self.status == 'text':
			self.done_timer += 1
			if self.done_timer > 120:
				if self.response_text != None:
					self.done_timer = 0
					self.activate_response()
				else:
					self.reset()


		#sprites.background_objects.update()
		i = 0
		while i < 60:
			self.choice_text.update()
			for choice in self.choice_list:
				if choice != None:
					choice.update()
			for arrow in self.arrow_list:
				self.update_arrow(arrow)
			i += options.current_fps


		

		#draw 'skip' if text isn't complete yet:
		if self.choice_text.status == 'active':
			skip_text = font_16.render('0 : Skip', 0,(options.WHITE))
			self.choice_text.image.blit(skip_text, (self.rect.width - skip_text.get_width() - 10, self.rect.height- skip_text.get_height() - 5))
				
			if sprites.player1 == controls.input_handler.gamepad1_ninja:
				temp_pic = sprites.player1.gamepad_layout['button_jump_image']
			else:
				temp_pic = controls.input_handler.button_keyboard_z
				#temp_pic = controls.input_handler.button_keyboard_z
			self.choice_text.image.blit(temp_pic, (self.rect.width - skip_text.get_width() - 10 - 2, self.rect.height- skip_text.get_height() - 5 - 1))
		
		elif self.choice_text.status == 'done':
			done_text = font_16.render('0 : Done', 0,(options.WHITE))
			self.choice_text.image.blit(done_text, (self.rect.width - done_text.get_width() - 10, self.rect.height- done_text.get_height() - 5))
				
			if sprites.player1 == controls.input_handler.gamepad1_ninja:
				temp_pic = sprites.player1.gamepad_layout['button_jump_image']
			else:
				temp_pic = temp_pic = controls.input_handler.button_keyboard_z
				#temp_pic = controls.input_handler.button_keyboard_z
			self.choice_text.image.blit(temp_pic, (self.rect.width - done_text.get_width() - 10 - 2, self.rect.height- done_text.get_height() - 5 - 1))

		sprites.active_sprite_list.draw(sprites.screen)

	def update_arrow(self, arrow):
		arrow.update()

		if arrow.rect.centerx < self.choice_text.rect.left:
			if len(self.left_list) >= self.stock:
				arrow.visible = 0

		elif arrow.rect.centerx > self.choice_text.rect.right:
			if len(self.right_list) >= self.stock:
				arrow.visible = 0

		elif arrow.rect.centery < self.choice_text.rect.top:
			if len(self.top_list) >= self.stock:
				arrow.visible = 0

		elif arrow.rect.centery > self.choice_text.rect.bottom:
			if len(self.bottom_list) >= self.stock:
				arrow.visible = 0
	
	def activate(self, player_list, text, next_game_state = None, signed = False, level_create = False, response_text = None, stock = 4, choice_left = None, choice_right = None, choice_top = None, choice_bottom = None):
		sprites.active_sprite_list.change_layer(sprites.transition_screen, 88)

		sprites.transition_screen.dirty = 1

		self.signed = signed

		options.game_state = 'choice'

		self.next_game_state = next_game_state
		self.level_create = level_create

		#lock in qustion text
		self.text_key = text #hold this to help craft responses
		try:
			self.text = self.text_dict[text]#'Greetings Humans. This demonstration is for Social Media purposes only. Were this not simply to appease the Twitterverse, the presented Options would be more visually interesting and combat relevant.'
		except KeyError:
			self.text = text
		self.response_text = response_text

		self.stock = stock

		self.choice_list = []
		self.arrow_list = []

	
		if choice_left != None:
			if choice_left in (sprites.player1, sprites.player2 ,sprites.player3, sprites.player4) and choice_left not in sprites.player_list:
				self.choice_left = None
			else:
				self.choice_left = Choice_Sprite('left', self.rect, choice_left)
				self.choice_list.append(self.choice_left)
				
				arrow = sprites.Menu_Arrow((self.rect.left - 11,self.rect.centery), 'left', None)
				self.arrow_list.append(arrow)
		else:
			self.choice_left = None

		if choice_right != None:
			if choice_right in (sprites.player1, sprites.player2 ,sprites.player3, sprites.player4) and choice_right not in sprites.player_list:
				self.choice_right = None
			else:
				self.choice_right = Choice_Sprite('right', self.rect, choice_right)
				self.choice_list.append(self.choice_right)

				arrow = sprites.Menu_Arrow((self.rect.right + 10,self.rect.centery), 'right', None)
				self.arrow_list.append(arrow)
		else:
			self.choice_right = None

		if choice_top != None:
			if choice_top in (sprites.player1, sprites.player2 ,sprites.player3, sprites.player4) and choice_top not in sprites.player_list:
				self.choice_top = None
			else:
				self.choice_top = Choice_Sprite('top', self.rect, choice_top)
				self.choice_list.append(self.choice_top)

				arrow = sprites.Menu_Arrow((self.rect.centerx, self.rect.top - 11), 'up', None)
				self.arrow_list.append(arrow)
		else:
			self.choice_top = None

		if choice_bottom != None:
			if choice_bottom in (sprites.player1, sprites.player2 ,sprites.player3, sprites.player4) and choice_bottom not in sprites.player_list:
				self.choice_bottom = None
			else:
				self.choice_bottom = Choice_Sprite('bottom', self.rect, choice_bottom)
				self.choice_list.append(self.choice_bottom)

				arrow = sprites.Menu_Arrow((self.rect.centerx, self.rect.bottom + 10), 'down', None)
				self.arrow_list.append(arrow)
		else:
			self.choice_bottom = None


		#Add in players to be quized.
		self.player_list = []
		for ninja in player_list:
			self.player_list.append(ninja)

		self.done_timer = 0

	def activate_response(self):

		self.status = 'response'

		for arrow in self.arrow_list:
			arrow.visible = 0 #kill()

		choice_list = [self.top_list, self.bottom_list, self.left_list, self.right_list]
		choice_list.sort(key=lambda x: -len(x))

		if choice_list[0] == self.top_list:
			choice = self.choice_top
		elif choice_list[0] == self.bottom_list:
			choice = self.choice_bottom
		elif choice_list[0] == self.left_list:
			choice = self.choice_left
		elif choice_list[0] == self.right_list:
			choice = self.choice_right


		#Now search for appropriate response.
		
		if self.text_key == 'Stage1_1.0':

			
			
			#One player ranked leader. Mission to protect them.
			if len(choice_list[0]) > len(choice_list[1]):
				self.response_text = "A leader has been chosen. For Earth to survive {0}'s life must be protected above all else. To win the next training exercise, {0} must survive. The rest of you may perish at at your leisure.".format(choice.choice.profile)#(self.left_choice.ninja.name)
			else: #No winner. Robot Leader. Mission to protect them.
				self.response_text =  "As I predicted, none of you appear worthy. I have created a Robot Ninja that is more suited to the role. To win the next training exercise, this Robot must survive. The rest of you may perish at your leisure."

		self.choice_text.kill()
		self.choice_text = Screen_Text(self.rect,self.response_text, 4)


	def reset(self):
		#sprites.versus_match_sprite.reset()
		self.choice_text.kill()

		self.status = 'text' #test or response

		for arrow in self.arrow_list:
			arrow.kill()

		for sprite in self.choice_list:
			sprite.kill()

		self.menu_created = False
		#sprites.active_sprite_list.remove(pause_sprite)
		#sprites.menu_sprite_list.remove(pause_sprite)
		#sounds.mixer.background_music.play()
		#pygame.mixer.unpause()

		'''
		sprites.player1.controls_sprite.reset()
		sprites.player2.controls_sprite.reset()
		sprites.player3.controls_sprite.reset()
		sprites.player4.controls_sprite.reset()
		'''
		sprites.pause_background.reset()
		options.game_state = self.next_game_state

		for ninja in sprites.player_list:
			ninja.choice_bar.reset()

		if self.level_create is True:
			if options.game_mode == 'coop':
				coop.level_builder.level_create()
				#Now reset position of all matrix bars. Allows them to 'start from top again'
				for bar in intro_handler.matrix_bar_list:
					bar.reset()

		sprites.player1.controls_sprite.reset()
		sprites.player2.controls_sprite.reset()
		sprites.player3.controls_sprite.reset()
		sprites.player4.controls_sprite.reset()

	def load_menu(self):

		#sprites.versus_match_sprite.activate()

		for sprite in sprites.menu_sprite_list:
			sprites.menu_sprite_list.remove(sprite)

		for arrow in self.arrow_list:
			arrow.activate()

		
		#i = 'This screen will be used for me to collect information. To reply, each player must hold their directionl input in the direction of their preferred answer. Do you understand?'
		
		self.choice_text = Screen_Text(self.rect,self.text, 4, signed = self.signed)
		sprites.pause_background.activate()

		#Create placement dictaionaries for the ninja choice_sprites
		self.top_dict = {4:[(self.choice_text.rect.centerx - 38,  self.choice_text.rect.top - 11),(self.choice_text.rect.centerx + 38,  self.choice_text.rect.top - 11),(self.choice_text.rect.centerx - 38 - 38 - 38,  self.choice_text.rect.top - 11),( self.choice_text.rect.centerx + 38 + 38 + 38,  self.choice_text.rect.top - 11)],
						3:[(self.choice_text.rect.centerx - 0,  self.choice_text.rect.top - 11),(self.choice_text.rect.centerx + 38 + 38,  self.choice_text.rect.top - 11),(self.choice_text.rect.centerx - 38 - 38,  self.choice_text.rect.top - 11)],
						2:[(self.choice_text.rect.centerx - 38,  self.choice_text.rect.top - 11),(self.choice_text.rect.centerx + 38,  self.choice_text.rect.top - 11)],
						1:[(self.choice_text.rect.centerx - 0,  self.choice_text.rect.top - 11)]
						} 

		self.bottom_dict = {4:[(self.choice_text.rect.centerx - 38,  self.choice_text.rect.bottom + 10),(self.choice_text.rect.centerx + 38,  self.choice_text.rect.bottom + 10),(self.choice_text.rect.centerx - 38 - 38 - 38,  self.choice_text.rect.bottom + 10),( self.choice_text.rect.centerx + 38 + 38 + 38,  self.choice_text.rect.bottom + 10)],
						3:[(self.choice_text.rect.centerx - 0,  self.choice_text.rect.bottom + 10),(self.choice_text.rect.centerx + 38 + 38,  self.choice_text.rect.bottom + 10),(self.choice_text.rect.centerx - 38 - 38,  self.choice_text.rect.bottom + 10)],
						2:[(self.choice_text.rect.centerx - 38,  self.choice_text.rect.bottom + 10),(self.choice_text.rect.centerx + 38,  self.choice_text.rect.bottom + 10)],
						1:[(self.choice_text.rect.centerx - 0,  self.choice_text.rect.bottom + 10)]
						} 

		self.left_dict = {4:[(self.choice_text.rect.left - 11,  self.choice_text.rect.centery - 38),(self.choice_text.rect.left - 11,  self.choice_text.rect.centery + 38),(self.choice_text.rect.left - 11 - 21,  self.choice_text.rect.centery - 38),(self.choice_text.rect.left - 11 - 21,  self.choice_text.rect.centery + 38)],
						3:[(self.choice_text.rect.left - 11,  self.choice_text.rect.centery - 38),(self.choice_text.rect.left - 11,  self.choice_text.rect.centery + 38),(self.choice_text.rect.left - 11 - 21,  self.choice_text.rect.centery)],
						2:[(self.choice_text.rect.left - 11,  self.choice_text.rect.centery - 38),(self.choice_text.rect.left - 11,  self.choice_text.rect.centery + 38)],
						1:[(self.choice_text.rect.left - 11,  self.choice_text.rect.centery)],
						} 

		self.right_dict = {4:[(self.choice_text.rect.right + 10,  self.choice_text.rect.centery - 38),(self.choice_text.rect.right + 10,  self.choice_text.rect.centery + 38),(self.choice_text.rect.right + 10 + 21,  self.choice_text.rect.centery - 38),(self.choice_text.rect.right + 10 + 21,  self.choice_text.rect.centery + 38)],
						3:[(self.choice_text.rect.right + 10,  self.choice_text.rect.centery - 38),(self.choice_text.rect.right + 10,  self.choice_text.rect.centery + 38),(self.choice_text.rect.right + 10 + 21,  self.choice_text.rect.centery)],
						2:[(self.choice_text.rect.right + 10,  self.choice_text.rect.centery - 38),(self.choice_text.rect.right + 10,  self.choice_text.rect.centery + 38)],
						1:[(self.choice_text.rect.right + 10,  self.choice_text.rect.centery)],
						} 

		#create lists to hold ninjas in each choice. Ordered.
		self.top_list = []
		self.bottom_list = []
		self.left_list = []
		self.right_list = []


choice_handler = Choice_Handler()

class Choice_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, choice_position, source_rect, choice):

		pygame.sprite.DirtySprite.__init__(self)

		self.image_list = []
		self.image_number = 0
		self.frame_counter = 0

		self.choice = choice

		#self.choice_top = Choice_Sprite('top', self.rect, choice_top)
		if isinstance(choice, pygame.sprite.DirtySprite):
			self.image_list = []
			for ninja_image in choice.idle_right:
				if choice_position in ('left', 'right'):
					if choice.name_bar.rect.width > 24:
						width = choice.name_bar.rect.width
					else:
						width = 24
					height = choice.name_bar.rect.height + 48
					image = pygame.Surface((width, height))
					image.fill(options.GREEN)
					image.set_colorkey(options.GREEN)
					image.blit(ninja_image, (round(width / 2) - 12, 0))
					image.blit(choice.name_bar.image, (round((width / 2) - (choice.name_bar.rect.width / 2)), height - choice.name_bar.rect.height))
					self.image_list.append(image)
				else: #top or bottom
					width = 24 + (choice.name_bar.rect.width * 2) + 6
					height = 48
					image = pygame.Surface((width, height))
					image.fill(options.GREEN)
					image.set_colorkey(options.GREEN)
					image.blit(ninja_image, (round(width / 2) - 12, 0))
					if choice_position == 'top':
						image.blit(choice.name_bar.image, (width - choice.name_bar.rect.width, height - choice.name_bar.rect.height + 3))
					else: #'bottom'
						image.blit(choice.name_bar.image, (0, 0))
					self.image_list.append(image)

			self.image = self.image_list[0]
			self.rect = self.image.get_rect()
			'''
			if choice == 'Player1':
				self.image_list = sprites.player1.idle_right
				self.image = self.image_list[0]
				self.rect = self.image.get_rect()
			elif choice == 'Player2':
				self.image_list = sprites.player2.idle_right
				self.image = self.image_list[0]
				self.rect = self.image.get_rect()
			elif choice == 'Player3':
				self.image_list = sprites.player3.idle_right
				self.image = self.image_list[0]
				self.rect = self.image.get_rect()
			elif choice == 'Player4':
				self.image_list = sprites.player4.idle_right
				self.image = self.image_list[0]
				self.rect = self.image.get_rect()
			'''
			

			'''
			self.image = pygame.Surface((28,28))
			self.image.fill(options.GREEN)
			self.image.set_colorkey(options.GREEN)
			self.image.blit(sprites.player1.idle_right[0], (3,3)) #, area=None, special_flags=0)
			self.image = Build_Menu_Perimeter(self.image)
			self.rect = self.image.get_rect()
			self.image_list.append(self.image)
			'''
		
		else: #Write Text Provided
			self.image = font_20.render(choice, 0, options.LIGHT_PURPLE)
			self.image = outline_text(self.image, options.LIGHT_PURPLE, options.DARK_PURPLE)
			self.rect = self.image.get_rect()
			self.image_list.append(self.image)
		
		if choice_position == 'left':
			self.rect.left = 5
			self.rect.centery = source_rect.centery
		elif choice_position == 'right':
			self.rect.right = 640 - 5
			self.rect.centery = source_rect.centery
		elif choice_position == 'top':
			self.rect.top = 5
			self.rect.centerx = source_rect.centerx
		elif choice_position == 'bottom':
			self.rect.bottom = 360 - 5
			self.rect.centerx = source_rect.centerx

		

		sprites.screen_objects.add(self)
		sprites.active_sprite_list.add(self) #this group actually draws the sprites
		sprites.active_sprite_list.change_layer(self, 90)

		self.visible = 1
		self.dirty = 1

	def update(self):
		self.frame_counter += 1
		if self.frame_counter > 14:
			self.frame_counter = 0
			self.image_number += 1
			if self.image_number > len(self.image_list) - 1:
				self.image_number = 0
			self.image = self.image_list[self.image_number]
			self.dirty = 1

'''
def pause():
	#check for gamepads regularly.
	controls.input_handler.get_gamepads()
	pause_sprite.visible = 1

	if sprites.player1.menu_up_press is True:
		pause_sprite.scroll('up')

	if sprites.player1.menu_down_press is True:
		pause_sprite.scroll('down')

	if sprites.player1.menu_select_press is True:
		if pause_sprite.menu_list[pause_sprite.vertical_selection][0] == 'Quit Game':
			sounds.mixer.menu_select.play()
			#sounds.mixer.change_song('music_menu.wav')
			#sounds.mixer.start_song()
			options.game_state = 'main_menu'
		elif pause_sprite.menu_list[pause_sprite.vertical_selection][0] == 'Resume':
			sounds.mixer.menu_select.play()
			controls.input_handler.remove_controls() #takes away movement keys from 'before pause'
			options.game_state = 'level'
			pause_sprite.visible = 0
			pause_sprite.dirty = 1

	screen = sprites.screen

	for sprite in sprites.menu_sprite_list:
		sprites.menu_sprite_list.remove(sprite)

	sprites.menu_sprite_list.add(pause_sprite)


	sprites.menu_sprite_list.update()
	for sprite in sprites.active_sprite_list:
		sprite.dirty = 1
	sprites.active_sprite_list.draw(screen)
'''



class Menu_Selection_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, menu_name, menu_list, font, size, y_mod):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.menu_name = menu_name
		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)
		self.PURPLE = (210,102,255)
		self.GREEN = (0,255,0)

		self.menu_list = menu_list #holds dict of menu text & possible choices

		#format is (('options', [1,2,3]), ('options', ['on','off']), ('test', [8,2,4]))

		self.font = font

		i = 40
		for item in self.menu_list:
			i += 30

		if size == None:
			width = sprites.size[0]
			height = sprites.size[1]
		else:
			width = size[0]
			height = size[1]



		self.image = pygame.Surface((width, height))
		self.image.fill(self.GREEN)
		self.image.set_colorkey(self.GREEN) 
		self.rect = self.image.get_rect()

		self.rect.centerx = sprites.size[0] / 2
		self.rect.centery = (sprites.size[1] / 2) + y_mod

		self.vertical_selection = 0 #which item is being selected

		self.selection_list = []
		i = 0
		for entry in self.menu_list:
			self.selection_list.append(0)
			i += 1


		#active_sprite_list.add(self)
		#active_sprite_list.change_layer(self, 5)

		self.dirty = 1

		self.bubble_switch = False #for item_options_sprite. Triggers bubble build.
		self.background_image = None

		self.items_all_on = False #used to toggle all items on/off


	def update(self):
		self.text_color = options.LIGHT_PURPLE
		self.selection_color = options.DARK_PURPLE

		#if self.menu_name in ('pause', 'versus_options', 'versus_item_options', 'game_options'):
		if self.menu_name in ('pause', 'game_options'):
			self.dirty = 1
			#self.image.fill(options.BLACK)
			#pygame.draw.rect(self.image, options.LIGHT_PURPLE, (0,0,self.rect.width,self.rect.height + 1), 7)
			#pygame.draw.rect(self.image, options.DARK_PURPLE, (0,0,self.rect.width - 1,self.rect.height), 4)
			self.image = Build_CPU_Screen(self.image)
			for bar in intro_handler.matrix_bar_list:
				bar.update()
				for digit in bar.digit_list:
					digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
			if self.menu_name == 'pause':
				self.image =  Build_Menu_Perimeter(self.image)

		elif self.menu_name in ('main_menu'):
			self.image.fill(options.GREEN)
			#self.image.fill(self.GREEN)

		elif self.menu_name in ('versus_options', 'versus_item_options'):
			self.image.fill(options.GREEN)
			#self.image.blit(self.background_image, (0,0))

		#pygame.draw.rect(self.image, self.WHITE, (0,0,self.rect.width,self.rect.height), 10)

		i = 0
		while i < len(self.menu_list):
			if self.menu_list[i][0] == '_space_':
				text = ''
			elif self.menu_list[i][1][0] == '':
				text = str(self.menu_list[i][0])
			else:
				text = str(self.menu_list[i][0]) + ": " + str(self.menu_list[i][1][self.selection_list[i]])

				#333333333333
				if self.menu_name == 'versus_options':
					if self.menu_list[i][0] == 'Victory':
						if self.menu_list[i][1][self.selection_list[i]] == 1:
							if options.versus_mode == 'Classic':
								text += ' Win'
							else:
								text += ' Pt'
						else:
							if options.versus_mode == 'Classic':
								text += ' Wins'
							else:
								text += ' Pts'

					if self.menu_list[i][0] == 'Score Frequency':
						if self.menu_list[i][1][self.selection_list[i]] == 'Off':
							pass
						elif self.menu_list[i][1][self.selection_list[i]] == 1:
							text += ' Duel'
						else:
							text += ' Duels'



			if i == self.vertical_selection:
				color = self.selection_color
			else:
				color = self.text_color

			MenuItem = font_20.render(text, 0,(color))

			if self.menu_name == 'versus_item_options':
				if i < 7:
					y_start = 80 + (i * (MenuItem.get_height() + 2))
					x_start = 50
				elif i < 14:
					y_start = 80 + (i * (MenuItem.get_height() + 2)) - ((7 * (MenuItem.get_height() + 2)))
					x_start = 220

				else:
					y_start = 80 + (i * (MenuItem.get_height() + 2)) - ((14 * (MenuItem.get_height() + 2)))
					x_start = 420

				'''
				if i < 7:
					y_start = 15 + (i * (MenuItem.get_height() + 2))
					x_start = 35
				else:
					y_start = 15 + (i * (MenuItem.get_height() + 2)) - ((10 * (MenuItem.get_height() + 2)))
					x_start = 185
				'''

			elif self.menu_name == 'versus_options':
				y_start = (self.rect.height / 2) - (MenuItem.get_height() * len(self.menu_list) / 2) + (i * (MenuItem.get_height() + 2) - 20)
				x_start = 50

			else:
				y_start = (self.rect.height / 2) - (MenuItem.get_height() * len(self.menu_list) / 2) + (i * (MenuItem.get_height() + 2))
				x_start = (self.rect.width / 2) - (MenuItem.get_width() / 2)

				if self.menu_name == 'main_menu':
					if i == 4:
						y_start -= 15

				elif self.menu_name == 'versus_mode':
					y_start -= 100

				elif self.menu_name == 'game_options':
					y_start -= 10

			self.image.blit(MenuItem, (x_start, y_start))
			if self.menu_name == 'versus_item_options':
				if color == self.selection_color:
					if options.control_preferences['player1'] == 'keyboard':
						button_image = controls.input_handler.button_keyboard_z
					else:
						button_image = sprites.player1.gamepad_layout['button_jump_image']
					self.image.blit(button_image, (x_start + MenuItem.get_width() + 4, y_start + 1))

					#check bubble visibility, in case of status change.
					temp_rect = pygame.Rect(x_start - 5, y_start, 5,5)
					for bubble in sprites.level_objects:
						if bubble.type == 'item_bubble':
							if bubble.rect.colliderect(temp_rect):
								if str(self.menu_list[i][1][self.selection_list[i]]) == 'off':
									bubble.visible = False
								else:
									bubble.visible = True

					versus_item_handler.update_screen_text([self.menu_list[i][0]])

				if self.bubble_switch is True:
					item = [self.menu_list[i][0]]
					if item not in (['_space_'], ['Return']):
						bubble = level.Item_Bubble(None, item)
						sprites.active_sprite_list.change_layer(bubble, 205)
						bubble.force_place((x_start - 3 - (bubble.rect.width / 2),y_start + (bubble.rect.height / 2) + 2), item)
						sprites.temp_menu_list.add(bubble)
						if str(self.menu_list[i][1][self.selection_list[i]]) == 'off':
							bubble.visible = False
			i += 1

		if self.bubble_switch is True:
			self.bubble_switch = False


					
	def reset(self):
		pass

	def set_options(self):
		self.selection_list = []
		i = 0
		while i < len(self.menu_list) - 1:
			key = self.menu_list[i][0]
			try:
				if options.items_dict[key] == 'off':
					switch = 1 #off
				else:
					switch = 0 #on

				self.selection_list.append(switch)
			except:
				print('not a real key')

			i += 1




		#if str(self.menu_list[i][1][self.selection_list[i]]) == 'off': 

	def y_press(self):
		self.dirty = 1

		if self.menu_name == 'versus_item_options':
			if self.items_all_on is True:
					new_list = []
					#for entry in self.selection_list:
					

					#4444444444444444444
					#demo line to lock out changes!!!
					keys_list = options.items_dict.keys()
					for entry in self.menu_list:
						if entry[0] in ('x', 'shoes', 'laser', 'wings', 'skull', 'bomb', 'volt', 'mine', 'rocket', 'ice bomb', 'cloak', 'shield'):
							if entry[0] in keys_list:
								new_list.append(0)
						

						else:
							if entry[0] in keys_list:
								new_list.append(1)
					self.selection_list = new_list
				
					#for bubble in sprites.level_objects:
					#	if bubble in sprites.temp_menu_list:
					#		if bubble.type == 'item_bubble':
					#			bubble.visible = True

					self.bubble_switch = True

					self.items_all_on = False


			else:
				new_list = []
				for entry in self.selection_list:
					new_list.append(1)
				self.selection_list = new_list

				for bubble in sprites.level_objects:
					if bubble in sprites.temp_menu_list:
						if bubble.type == 'item_bubble':
							bubble.visible = False

				self.items_all_on = True


				#format is (('options', [1,2,3]), ('options', ['on','off']), ('test', [8,2,4]))


	def scroll(self, direction, columns = False, blank = False, sound = True):
		self.dirty = 1

		if direction == 'down':
			if blank is False and sound is True:
				sounds.mixer.menu_move.play()
			self.vertical_selection += 1
			if self.vertical_selection >= len(self.menu_list):
				self.vertical_selection = 0

			if self.menu_list[self.vertical_selection][0] == '_space_':
				self.scroll('down', blank = True)


		elif direction == 'up':
			if blank is False and sound is True:
				sounds.mixer.menu_move.play()
			self.vertical_selection -= 1
			if self.vertical_selection <  0:
				self.vertical_selection = len(self.menu_list) - 1

			if self.menu_list[self.vertical_selection][0] == '_space_':
				self.scroll('up', blank = True)

		elif direction == 'left':
			if columns is True:
				sounds.mixer.menu_move.play()
				if self.vertical_selection < 7:
					self.vertical_selection += 14	
				else:
					self.vertical_selection -= 7	

				#if self.vertical_selection >= len(self.menu_list):
				#	self.vertical_selection = len(self.menu_list) - 1 - self.vertical_selection

				if  self.vertical_selection > len(self.menu_list) - 1 or self.menu_list[self.vertical_selection][0] == '_space_':
					self.vertical_selection = len(self.menu_list) - 1
			else:		
				if len(self.menu_list[self.vertical_selection][1]) > 1:
					if sound is True:
						sounds.mixer.menu_move.play()
				#selection_list format is (('options', [1,2,3]), ('options', ['on','off']), ('test', [8,2,4]))
				i = self.selection_list[self.vertical_selection] - 1
				if i < 0:
					i = len(self.menu_list[self.vertical_selection][1]) - 1
				self.selection_list[self.vertical_selection] = i			


		elif direction == 'right':
			if columns is True:
				if sound is True:
					sounds.mixer.menu_move.play()
				if self.vertical_selection < 14:	
					self.vertical_selection += 7
				else:
					self.vertical_selection -= 14
				#if self.vertical_selection >= len(self.menu_list):
				#	self.vertical_selection = len(self.menu_list) - 1 - self.vertical_selection

				if  self.vertical_selection > len(self.menu_list) - 1 or self.menu_list[self.vertical_selection][0] == '_space_':
					self.vertical_selection = len(self.menu_list) - 1
			else:
				if len(self.menu_list[self.vertical_selection][1]) > 1:
					if sound is True:
						sounds.mixer.menu_move.play()
				#selection_list format is (('options', [1,2,3]), ('options', ['on','off']), ('test', [8,2,4]))
				i = self.selection_list[self.vertical_selection] + 1
				if i > len(self.menu_list[self.vertical_selection][1]) - 1:
					i = 0
				self.selection_list[self.vertical_selection] = i

class Level_Selection_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, mode):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)
		self.mode = mode #'versus' or 'coop'
		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)
		self.PURPLE = (210,102,255)
		self.GREEN = (0,255,0)

		self.image = pygame.Surface((sprites.size[0], sprites.size[1]))
		self.image.fill(self.GREEN)
		self.image.set_colorkey(self.GREEN) 
		self.rect = self.image.get_rect()

		self.rect.x = 0
		self.rect.y = 0

		self.selection_sprite = Selection_Sprite()

		'''
		if self.mode == 'versus':
			self.level1 = Versus_Level_Icon('Classic', 'A duel for survival and glory amongst warriors from worlds the Mallow has conquered. We must defend Earth from this fate.')
			self.level2 = Versus_Level_Icon('Olympus', 'Ancient earth literature speaks of a great power hidden at the peak of Mount Olympus. Harnessing this power could be... useful.')
			self.level3 = Versus_Level_Icon('Crucible', '')
			self.level4 = Versus_Level_Icon('Paradox', '')
			self.level5 = Versus_Level_Icon('Tartarus', '')
			self.level6 = Versus_Level_Icon('Mystic Cavern', '')
			self.level7 = Versus_Level_Icon('Falls', '')
			self.level8 = Versus_Level_Icon('Pump', '')
			self.level9 = Versus_Level_Icon('Labyrinth', 'The human INTERNET circa 1984 suggests that human warriors often duel in ancient temples. I have assembled a likely combat scenario.')
			self.level10 = Versus_Level_Icon('Ice', '')
			self.level11 = Versus_Level_Icon('Space', '')
			self.level12 = Versus_Level_Icon('Testing', '')
			#self.level12 = Versus_Level_Icon('TBA', '')
		'''

		self.unlocked_level_list = ['The Colliseum', 'Mt Olympus', 'Retro Falls']

		if options.demo is False:
			self.unlocked_level_list = ['The Colliseum', 'Mt Olympus', 'Retro Falls', 'Testing', 'The Crucible', 'Dimension M', 'Densinium Caves', 'Decrepit Tower', 'Secret Lab', 'Ancient Tomb', 'Frozen Ruins', 'Moon Base 7',]


		if self.mode == 'versus':
			self.level1 = Versus_Level_Icon(self, 'The Colliseum', 'The ultimate dueling simulation in which to claim Ninja Supremacy. Only the most cunning of Ninja Warriors shall emerge victorious.')
			self.level2 = Versus_Level_Icon(self,'Mt Olympus', 'Harness the power hidden at the peak of Mt Olympus to secure victory. Research shows training at simulated altitude builds character.')
			self.level3 = Versus_Level_Icon(self,'Retro Falls', 'A simple training simulation involving earth waterfalls. WARNING - simulation gravitational errors have not been fully rectified.')
			self.level4 = Versus_Level_Icon(self,'Decrepit Tower', 'The Decrepit Tower stage will be made available in the Codename Mallow full release.')
			self.level5 = Versus_Level_Icon(self,'The Crucible', 'The Crucible stage will be made available in the Codename Mallow full release.') # 'My advanced predictive algorithms suggest that the Crucible itself shall emerge victorious in the next duel.')
			self.level6 = Versus_Level_Icon(self,'Dimension M', 'The Dimension M stage will be made available in the Codename Mallow full release.')
			self.level7 = Versus_Level_Icon(self,'Densinium Caves', 'The Densinium Caves stage will be made available in the Codename Mallow full release.')
			self.level8 = Versus_Level_Icon(self,'Secret Lab', 'The Secret Lab stage will be made available in the Codename Mallow full release.')
			self.level9 = Versus_Level_Icon(self,'Ancient Tomb', 'The Ancient Tomb stage will be made available in the Codename Mallow full release.') #'The human INTERNET circa 1984 suggests that human warriors often duel in ancient temples. I have assembled a likely combat scenario.')
			self.level10 = Versus_Level_Icon(self,'Frozen Ruins', 'The Frozen Ruins stage will be made available in the Codename Mallow full release.')
			self.level11 = Versus_Level_Icon(self,'Moon Base 7', 'The Moon Base 7 stage will be made available in the Codename Mallow full release.')
			self.level12 = Versus_Level_Icon(self,'Testing', 'While details on this stage remain shrouded in mystery, it is destined to be "BRUTAL!".')
			#self.level12 = Versus_Level_Icon('TBA', '')

		elif self.mode == 'coop':
			self.level1 = Versus_Level_Icon(self, 'Stage 1', 'A most basic combat introduction.')
			self.level2 = Versus_Level_Icon(self, 'TBA', '')
			self.level3 = Versus_Level_Icon(self, 'TBA', '')
			self.level4 = Versus_Level_Icon(self, 'TBA', '')
			self.level5 = Versus_Level_Icon(self, 'TBA', '')
			self.level6 = Versus_Level_Icon(self, 'TBA', '')
			self.level7 = Versus_Level_Icon(self, 'TBA', '')
			self.level8 = Versus_Level_Icon(self, 'TBA', '')
			self.level9 = Versus_Level_Icon(self, 'TBA', '')
			self.level10 = Versus_Level_Icon(self, 'TBA', '')
			self.level11 = Versus_Level_Icon(self, 'TBA', '')
			self.level12 = Versus_Level_Icon(self, 'TBA', '')

		self.level_list = ((self.level1, self.level2, self.level3, self.level4),
							(self.level5, self.level6, self.level7, self.level8),
							(self.level9, self.level10, self.level11, self.level12))

		self.row_number = 0
		self.column_number = 0

		self.current_level = None
		self.find_selected_level()

		self.dirty = 1

	def update(self):
		self.find_selected_level()
	
	def load(self):
		self.find_selected_level()

		x = 0
		y = 0

		for item in self.level_list:
			for level in item:
				centerx = (640 / 8) * ((x * 2) + 1)
				x_pos = centerx  - (level.rect.width / 2)

				centery = (280 / 6) * ((y * 2) + 1)
				y_pos = 20 + centery  - (level.rect.height / 2)


				#self.image.blit(level.image, (x_pos,  y_pos))

				level.rect.x = x_pos
				level.rect.y = y_pos

				x +=1
			x = 0
			y += 1

	def find_selected_level(self):
		for row in self.level_list:
			for level in row:
				if options.stage_selection == 'Single Stage Choice':
					level.selected = False
				else:
					level.selected = True
				#level.image.fill(options.LIGHT_PURPLE)
				#level.image.blit(level.IconText, ((level.rect.width / 2) - (level.IconText.get_width() / 2), (level.rect.height / 2) - (level.IconText.get_height() / 2)))
				
				#if options.stage_selection != 'Single Stage Choice':
				#	pygame.draw.rect(level.image, options.DARK_PURPLE, (0,0,level.rect.width - 1, level.rect.height - 1), 4)

		current_selection = self.level_list[self.row_number][self.column_number]
		
		#current_selection.image.fill(options.DARK_PURPLE)
		#current_selection.image.blit(current_selection.IconText, ((current_selection.rect.width / 2) - (current_selection.IconText.get_width() / 2), (current_selection.rect.height / 2) - (current_selection.IconText.get_height() / 2)))
		#pygame.draw.rect(current_selection.image, options.DARK_PURPLE, (0,0,current_selection.rect.width - 1, current_selection.rect.height - 1), 4)
		current_selection.selected = True
		self.current_level = current_selection

		self.selection_sprite.rect.x = current_selection.rect.x - 3
		self.selection_sprite.rect.y = current_selection.rect.y - 3

	def scroll(self, direction):
		sounds.mixer.menu_move.play()
		self.dirty = 1

		if direction == 'down':
			self.row_number += 1
			if self.row_number > 2:
				self.row_number = 0

		elif direction == 'up':
			self.row_number -= 1
			if self.row_number <  0:
				self.row_number = 2

		elif direction == 'left':
			self.column_number -= 1
			if self.column_number < 0:
				self.column_number = 3			


		elif direction == 'right':
			self.column_number += 1
			if self.column_number > 3:
				self.column_number = 0

	def build_level(self):
		if options.stage_selection == 'Single Stage Choice':
			if self.current_level.level_name in self.unlocked_level_list:
				sounds.mixer.menu_select.play()
				options.duel_counter = 0
				sprites.reset_sprites()
				for ninja in sprites.player_list:
					ninja.reset_stats()
					ninja.current_VP = 0
					ninja.current_wins = 0

				i = level.level_builder.versus_dict[self.current_level.level_name]
				level.level_builder.current_level = i
				
				level.level_builder.level_reset()
				sounds.mixer.stop_song()
				options.game_state = 'level'
		else:
			sounds.mixer.menu_select.play()
			options.duel_counter = 0
			sprites.reset_sprites()
			for ninja in sprites.player_list:
				ninja.reset_stats()
				ninja.current_VP = 0
				ninja.current_wins = 0

			level.level_builder.level_reset()
			sounds.mixer.stop_song()
			options.game_state = 'level'

		'''
		if options.game_mode == 'coop':
			sounds.mixer.stop_song()
			options.game_state = 'level'
			i = coop.level_builder.coop_dict[self.current_level.level_name]
			coop.level_builder.current_level = i

			coop.level_builder.level_clear()
			
			choice_handler.activate(sprites.player_list, 'Stage1_1.0', level_create = True, response_text = 'test', choice_left=sprites.player1, choice_right=sprites.player2, choice_top=sprites.player3, choice_bottom=sprites.player4)
			

			#coop.level_builder.level_create()
s
		else: #'versus'
			if options.stage_selection == 'Single Stage Choice':
				if self.current_level.level_name in self.unlocked_level_list:
					i = level.level_builder.versus_dict[self.current_level.level_name]
					level.level_builder.current_level = i
					level.level_builder.level_reset()
					sounds.mixer.stop_song()
					options.game_state = 'level'
			else:
				sounds.mixer.stop_song()
				options.game_state = 'level'
				key = None
				while key not in self.unlocked_level_list:
					key = random.choice(list(level.level_builder.versus_dict))
				i = level.level_builder.versus_dict[key]
				level.level_builder.current_level = i
				level.level_builder.level_reset()

		for ninja in sprites.ninja_list:
			ninja.current_VP = 0
			ninja.current_wins = 0
			#ninja.reset_stats()
			ninja.matches_participated += 1
		'''


class Selection_Sprite(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)

		#self.frame_counter = 0
		#self.line_width = 3
		#self.width_mod = 1
		
		self.image = pygame.Surface((146,86))
		self.image.fill(options.GREEN)
		self.image.set_colorkey(options.GREEN)
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, options.DARK_PURPLE, (1,1,self.rect.width - 2, self.rect.height - 2), 3)
		self.rect.x = 0
		self.rect.y = 0
		self.dirty = 1

		

		sprites.menu_sprite_list.add(self)
		sprites.active_sprite_list.add(self)
		sprites.active_sprite_list.change_layer(self,5)


	def update(self):
		self.dirty = 1

		if options.stage_selection == 'Single Stage Choice':
			self.visible = 1
		else:
			self.visible = 0
		
		'''
		self.frame_counter += 1
		if self.frame_counter == 2:
			self.frame_counter = 0
			self.line_width += self.width_mod
			if self.line_width > 3:
				self.line_width = 3
				self.width_mod *= -1
			elif self.line_width < 1:
				self.line_width = 1
				self.width_mod *= -1

			self.image.fill(options.GREEN)
			pygame.draw.rect(self.image, options.DARK_PURPLE, (1,1,self.rect.width - 4, self.rect.height - 4), self.line_width)
		'''

class Versus_Level_Icon(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, level_selection_sprite, level_name, level_description):
		pygame.sprite.DirtySprite.__init__(self)

		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)
		self.PURPLE = (210,102,255)
		self.GREEN = (0,255,0)

		self.level_name = level_name
		self.level_description = level_description

		self.level_selection_sprite = level_selection_sprite

		iconsheet = sprites.SpriteSheet("leveliconsheet.png")

		image_dict = {	'The Colliseum' : [(0,0), (141,0), (282,0), (423,0)],
						'Mt Olympus' : [(0,81), (141,81), (282,81), (423,81)],
						'The Crucible' : [(0,162), (141,162), (282,162), (423,162)],
						'Dimension M' : [(0,243), (141,243), (282,243), (423,243)],
						'Decrepit Tower' : [(0,324), (141,324), (282,324), (423,324)],
						'Densinium Caves' : [(0,405), (141,405), (282,405), (423,405)],
						'Retro Falls' : [(0,486), (141,486), (282,486), (423,486)],
						'Secret Lab' : [(0,567), (141,567), (282,567), (423,567)],
						'Ancient Tomb' : [(0,647), (141,647), (282,647), (423,647)],
						'Frozen Ruins' : [(0,728), (141,728), (282,728), (423,728)],
						'Moon Base 7' : [(0,809), (141,809), (282,809), (423,809)],
						'Testing' : [(0,890), (141,890), (282,890), (423,890)],
						'Stage 1' : [(0,0), (141,0), (282,0), (423,0)],
						'TBA' : [(0,0), (141,0), (282,0), (423,0)],

						}

		
		self.image_list = []
		self.image_number = 0

		if image_dict[self.level_name] == None:
			#self.image = pygame.Surface((128,72))
			self.image = pygame.Surface((140,80))
			self.image.fill(self.WHITE)
			self.image.set_colorkey(self.GREEN) 
			self.rect = self.image.get_rect()

			if self.level_name in self.level_selection_sprite.unlocked_level_list:
				name_text = self.level_name
			else:
				name_text = 'LOCKED'

			self.IconText = font_16.render(name_text, 0,(self.BLACK))
			self.image.blit(self.IconText, ((self.rect.width / 2) - (self.IconText.get_width() / 2), (self.rect.height / 2) - (self.IconText.get_height() / 2)))
			self.image_list.append(self.image)

		else:
			coords_list = image_dict[self.level_name]
			for coords in coords_list:
				image = iconsheet.getImage(coords[0], coords[1],140,80)
				

				if self.level_name in self.level_selection_sprite.unlocked_level_list:
					name_text = self.level_name
				else:
					name_text = '-locked-'

				self.IconText = font_16.render(name_text, 0,(self.WHITE))
				self.IconText = outline_text(self.IconText, self.WHITE, self.BLACK)
				image.blit(self.IconText, ((image.get_width() / 2) - (self.IconText.get_width() / 2), image.get_height() - self.IconText.get_height()))
				
				if self.level_name not in self.level_selection_sprite.unlocked_level_list:
					image.fill((50,50,50), special_flags = pygame.BLEND_RGBA_SUB)
				self.image_list.append(image)

			self.dark_image = self.image_list[0].copy()
			if self.level_name in self.level_selection_sprite.unlocked_level_list:
				self.dark_image.fill((50,50,50), special_flags = pygame.BLEND_RGBA_SUB)

			self.image = self.dark_image
			self.rect = self.image.get_rect()

		self.rect.x = 0
		self.rect.y = 0

		self.selected = False #called from elsewhrre.


		self.dirty = 1
		self.frame_counter = 0

		self.currently_selected = False #used LOCALLY in update


	def update(self):
		if self.level_selection_sprite.current_level == self or options.stage_selection == 'Random Each Duel':
			if self.currently_selected is False:
				self.currently_selected = True
				self.image = self.image_list[self.image_number]
				self.dirty = 1
			
			self.frame_counter += 1
			if self.frame_counter == 30:
				self.frame_counter = 0
				self.image_number += 1
				if self.image_number >= len(self.image_list):
					self.image_number = 0

				self.image = self.image_list[self.image_number]
				self.dirty = 1

		else:
			if self.currently_selected is True:
				self.currently_selected = False
				self.frame_counter = 0
				self.image_number = 0
				self.image = self.dark_image
				self.dirty = 1


class Screen_Text(pygame.sprite.DirtySprite):

	#place Ninja attributes here

	def __init__(self, rect, text, size, speed = 2,ai=None, start_height = None, signed = False):
		#constructor function
		pygame.sprite.DirtySprite.__init__(self)

		self.start_height = start_height

		self.ai = ai #only has ai if controlled by Codename_Mallow CPU
		self.speed = speed
		self.image = pygame.Surface((rect[2],rect[3]))
		self.rect = self.image.get_rect()

		self.type = 'screen text'

		self.image = Build_CPU_Screen(self.image)
		self.image = Build_Menu_Perimeter(self.image)
		
		self.line1_text = ''
		self.line2_text = ''
		self.line3_text = ''
		self.line4_text = ''
		self.line5_text = ''
		self.line6_text = ''
		self.line7_text = ''

		self.line_size = 66 #max number of digits
		self.line_size = round((rect[2] / 540) * 63)
		
		self.line_total = 7

		self.base_text = text #holds the whole string
		if len(self.base_text) > 0:
			self.create_lines(text)

		if signed is True:
			self.line_total += 1
			if self.line1_text == '':
				self.line1_text = '-Ancalabro'
			elif self.line2_text == '':
				self.line2_text = '-Ancalabro'
			elif self.line3_text == '':
				self.line3_text = '-Ancalabro'
			elif self.line4_text == '':
				self.line4_text = '-Ancalabro'
			elif self.line5_text == '':
				self.line5_text = '-Ancalabro'
			elif self.line6_text == '':
				self.line6_text = '-Ancalabro'
			elif self.line7_text == '':
				self.line7_text = '-Ancalabro'


		#self.text_list = text.split()#breaks string into list of single words.
		self.size = size

		self.rect.x = rect[0]
		self.rect.y = rect[1]

		self.digit_number = 0 #holds current digit in current_line
		self.line_number = 1 #corresponds to which text bar to create.
		self.digit_timer = 0 #counts how long before next digit prints.

		self.text_bar1 = None
		self.text_bar2 = None
		self.text_bar3 = None
		self.text_bar4 = None
		self.text_bar5 = None
		self.text_bar6 = None
		self.text_bar7 = None

		self.status = 'active' #'active' or 'done'

		sprites.background_objects.add(self)
		sprites.active_sprite_list.add(self)
		if self.ai == None:
			sprites.active_sprite_list.change_layer(self,100)
		else:
			sprites.active_sprite_list.change_layer(self,5)



	def update(self):
			
			#if self.ai == None or sprites.countdown_timer.done is True:	
			if self.ai != None:
				self.ai.update()
			if self.status == 'active':
				self.dirty = 1
				self.image = Build_CPU_Screen(self.image)
				#asdf
				if self.ai == None or sprites.transition_screen.status == 'idle':
					for bar in intro_handler.matrix_bar_list:
						bar.update()
						for digit in bar.digit_list:
							digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
				self.image = Build_Menu_Perimeter(self.image)
				#pygame.draw.rect(self.image, options.DARK_PURPLE, (0,0,self.rect.width - 1, self.rect.height - 1), 2)
				#pygame.draw.rect(self.image, options.LIGHT_PURPLE, (2,2,self.rect.width - 4, self.rect.height - 4), 1)

				#self.current_text_bar = self.get_text_bar()

				#self.build_text_bar
				if len(self.base_text) > 0 and self.base_text != None and (sprites.transition_screen.status == 'idle' and sprites.countdown_timer.status == 'idle'): #sprites.countdown_timer.done is False:
					self.get_text_bars()

					#Calculate appropriate start height of first line. Will keep things centered vertically.
					if self.start_height == None:
						start_height = (self.image.get_height() / 2) - (self.text_bar1.get_height() / 2) - (((self.text_bar1.get_height() + 3) / 2) * (self.line_total - 1))
					else:
						start_height = self.start_height

					if self.text_bar1 != None:
						#self.image.blit(self.text_bar1, (14,7))
						self.image.blit(self.text_bar1, (14,start_height))

					if self.text_bar2 != None:
						#self.image.blit(self.text_bar2, (14,7 + self.text_bar1.get_height() + 3))
						self.image.blit(self.text_bar2, (14,start_height + self.text_bar1.get_height() + 3))

					if self.text_bar3 != None:
						#self.image.blit(self.text_bar3, (14,7 + ((self.text_bar1.get_height()+ 3) * 2)))
						self.image.blit(self.text_bar3, (14,start_height + ((self.text_bar1.get_height()+ 3) * 2)))

					if self.text_bar4 != None:
						#self.image.blit(self.text_bar4, (14,7 + ((self.text_bar1.get_height()+ 3) * 3)))
						self.image.blit(self.text_bar4, (14,start_height + ((self.text_bar1.get_height()+ 3) * 3)))

					if self.text_bar5 != None:
						#self.image.blit(self.text_bar5, (14,7 + ((self.text_bar1.get_height()+ 3) * 4)))
						self.image.blit(self.text_bar5, (14,start_height + ((self.text_bar1.get_height()+ 3) * 4)))

					if self.text_bar6 != None:
						#self.image.blit(self.text_bar6, (14,7 + ((self.text_bar1.get_height()+ 3) * 5)))
						self.image.blit(self.text_bar6, (14,start_height + ((self.text_bar1.get_height()+ 3) * 5)))

					if self.text_bar7 != None:
						#self.image.blit(self.text_bar6, (14,7 + ((self.text_bar1.get_height()+ 3) * 5)))
						self.image.blit(self.text_bar7, (14,start_height + ((self.text_bar1.get_height()+ 3) * 6)))

					self.digit_timer += 1 # * options.DT

					if self.digit_timer >= self.speed:
						self.digit_timer = 0
						self.digit_number += 1
						if self.digit_number >= self.current_line_length():
							self.digit_number = 0
							self.line_number += 1
							if self.line_number > 7:
								self.status = 'done'
						else:
							pass #Took typing sound away. Too distracting from rad music.
							#sounds.mixer.type.play()
			else: #inactive. Regurgitate last message.
				self.dirty = 1
				self.image = Build_CPU_Screen(self.image)
				for bar in intro_handler.matrix_bar_list:
					bar.update()
					for digit in bar.digit_list:
						digit.update(self.image, None) #blits to sprites.screen from within update, based on bar position.
				self.image = Build_Menu_Perimeter(self.image)

				#Calculate appropriate start height of first line. Will keep things centered vertically.
				if self.start_height == None:
					start_height = (self.image.get_height() / 2) - (self.text_bar1.get_height() / 2) - (((self.text_bar1.get_height() + 3) / 2) * (self.line_total - 1))
				else:
					start_height = self.start_height

				if self.text_bar1 != None:
					self.image.blit(self.text_bar1, (14,start_height))

				if self.text_bar2 != None:
					self.image.blit(self.text_bar2, (14,start_height + self.text_bar1.get_height() + 3))
				
				if self.text_bar3 != None:
					self.image.blit(self.text_bar3, (14,start_height + ((self.text_bar1.get_height()+ 3) * 2)))

				if self.text_bar4 != None:
					self.image.blit(self.text_bar4, (14,start_height + ((self.text_bar1.get_height()+ 3) * 3)))

				if self.text_bar5 != None:
					self.image.blit(self.text_bar5, (14,start_height + ((self.text_bar1.get_height()+ 3) * 4)))

				if self.text_bar6 != None:
					self.image.blit(self.text_bar6, (14,start_height + ((self.text_bar1.get_height()+ 3) * 5)))

				if self.text_bar7 != None:
					self.image.blit(self.text_bar7, (14,start_height + ((self.text_bar1.get_height()+ 3) * 6)))

		
	def current_line_length(self):
		if self.line_number == 1:
			length = len(self.line1_text)
		elif self.line_number == 2:
			length = len(self.line2_text)
		elif self.line_number == 3:
			length = len(self.line3_text)
		elif self.line_number == 4:
			length = len(self.line4_text)
		elif self.line_number == 5:
			length = len(self.line5_text)
		elif self.line_number == 6:
			length = len(self.line6_text)
		elif self.line_number == 7:
			length = len(self.line7_text)

		return(length)
	def create_lines(self,text):
		self.line1_text = ''
		self.line2_text = ''
		self.line3_text = ''
		self.line4_text = ''
		self.line5_text = ''
		self.line6_text = ''
		self.line7_text = ''

		base_text = text
		#print(base_text)
		while len(base_text) > self.line_size:
			i = self.line_size
			while base_text[i] != ' ':
				i -= 1

			if self.line1_text == '':
				self.line1_text = base_text[:i]
			elif self.line2_text == '':
				self.line2_text = base_text[:i]
			elif self.line3_text == '':
				self.line3_text = base_text[:i]
			elif self.line4_text == '':
				self.line4_text = base_text[:i]
			elif self.line5_text == '':
				self.line5_text = base_text[:i]
			elif self.line6_text == '':
				self.line6_text = base_text[:i]
			elif self.line7_text == '':
				self.line7_text = base_text[:i]

			base_text = base_text[i:]

		if self.line1_text == '':
			self.line1_text = base_text
		elif self.line2_text == '':
			self.line2_text = base_text
		elif self.line3_text == '':
			self.line3_text = base_text
		elif self.line4_text == '':
			self.line4_text = base_text
		elif self.line5_text == '':
			self.line5_text = base_text
		elif self.line6_text == '':
			self.line6_text = base_text
		elif self.line7_text == '':
			self.line7_text = base_text

		if len(self.line1_text) > 0:
			if self.line1_text[0] == ' ':
				self.line1_text = self.line1_text[1:]
			if self.line1_text[-1] == ' ':
				self.line1_text = self.line1_text[:-1]
			self.line_total = 1

		if len(self.line2_text) > 0:
			if self.line2_text[0] == ' ':
				self.line2_text = self.line2_text[1:]
			if self.line2_text[-1] == ' ':
				self.line2_text = self.line2_text[:-1]
			self.line_total = 2

		if len(self.line3_text) > 0:
			if self.line3_text[0] == ' ':
				self.line3_text = self.line3_text[1:]
			if self.line3_text[-1] == ' ':
				self.line3_text = self.line3_text[:-1]
			self.line_total = 3

		if len(self.line4_text) > 0:
			if self.line4_text[0] == ' ':
				self.line4_text = self.line4_text[1:]
			if self.line4_text[-1] == ' ':
				self.line4_text = self.line4_text[:-1]
			self.line_total = 4

		if len(self.line5_text) > 0:
			if self.line5_text[0] == ' ':
				self.line5_text = self.line5_text[1:]
			if self.line5_text[-1] == ' ':
				self.line5_text = self.line5_text[:-1]
			self.line_total = 5

		if len(self.line6_text) > 0:
			if self.line6_text[0] == ' ':
				self.line6_text = self.line6_text[1:]
			if self.line6_text[-1] == ' ':
				self.line6_text = self.line6_text[:-1]
			self.line_total = 6

		if len(self.line7_text) > 0:
			if self.line7_text[0] == ' ':
				self.line7_text = self.line7_text[1:]
			if self.line7_text[-1] == ' ':
				self.line7_text = self.line7_text[:-1]
			self.line_total = 7

		#print(self.line1_text)
		#print(self.line2_text)
		#print(self.line3_text)


	def reset(self, text):
		self.status = 'active'
		self.text_bar1 = None
		self.text_bar2 = None
		self.text_bar3 = None
		self.text_bar4 = None
		self.text_bar5 = None
		self.text_bar6 = None
		self.text_bar7 = None

		self.digit_number = 0 #holds current digit in current_line
		self.line_number = 1 #corresponds to which text bar to create.
		self.digit_timer = 0 #counts how long before next digit prints.


		self.base_text = text #holds the whole string
		if len(self.base_text) > 0:
			self.create_lines(text)



	def get_text_bars(self):
		if self.line_number == 1:
			base_text = self.line1_text
		elif self.line_number == 2:
			base_text = self.line2_text
		elif self.line_number == 3:
			base_text = self.line3_text
		elif self.line_number == 4:
			base_text = self.line4_text
		elif self.line_number == 5:
			base_text = self.line5_text
		elif self.line_number == 6:
			base_text = self.line6_text
		elif self.line_number == 7:
			base_text = self.line7_text
		

		if len(base_text) > 0:
			text = ''
			i = 0
			while i <= self.digit_number:

				text = text + base_text[i]
				i += 1

			if self.line_number == 1:
				self.text_bar1 = font_16.render(text, 0, options.LIGHT_PURPLE)
			elif self.line_number == 2:
				self.text_bar2 = font_16.render(text, 0, options.LIGHT_PURPLE)
			elif self.line_number == 3:
				self.text_bar3 = font_16.render(text, 0, options.LIGHT_PURPLE)
			elif self.line_number == 4:
				self.text_bar4 = font_16.render(text, 0, options.LIGHT_PURPLE)
			elif self.line_number == 5:
				self.text_bar5 = font_16.render(text, 0, options.LIGHT_PURPLE)
			elif self.line_number == 6:
				self.text_bar6 = font_16.render(text, 0, options.LIGHT_PURPLE)
			elif self.line_number == 7:
				self.text_bar7 = font_16.render(text, 0, options.LIGHT_PURPLE)

	def kill(self): #override sprite.kill()
		if self.ai != None:
			self.ai.pre_kill()
		super(Screen_Text, self).kill()
		
	def finish_text_bars(self):
		i = 1
		while i <= 7:
			if i == 1:
				base_text = self.line1_text
			elif i == 2:
				base_text = self.line2_text
			elif i == 3:
				base_text = self.line3_text
			elif i == 4:
				base_text = self.line4_text
			elif i == 5:
				base_text = self.line5_text
			elif i == 6:
				base_text = self.line6_text
			elif i == 7:
				base_text = self.line7_text
			

			if len(base_text) > 0:
				text = ''
				text = base_text
				self.line_number = i
				self.digit_number = len(base_text)

				if i == 1:
					self.text_bar1 = font_16.render(text, 0, options.LIGHT_PURPLE)
				elif i == 2:
					self.text_bar2 = font_16.render(text, 0, options.LIGHT_PURPLE)
				elif i == 3:
					self.text_bar3 = font_16.render(text, 0, options.LIGHT_PURPLE)
				elif i == 4:
					self.text_bar4 = font_16.render(text, 0, options.LIGHT_PURPLE)
				elif i == 5:
					self.text_bar5 = font_16.render(text, 0, options.LIGHT_PURPLE)
				elif i == 6:
					self.text_bar6 = font_16.render(text, 0, options.LIGHT_PURPLE)
				elif i == 7:
					self.text_bar7 = font_16.render(text, 0, options.LIGHT_PURPLE)

			i += 1 
		self.status = 'done'

def Build_Menu_Perimeter(surface):
	image = surface#.copy()

	top_left_corner = sprites.menu_sheet.getImage(0,0,3,3)
	top_right_corner = sprites.menu_sheet.getImage(0,4,3,3)
	bottom_left_corner = sprites.menu_sheet.getImage(0,8,3,3)
	bottom_right_corner = sprites.menu_sheet.getImage(0,12,3,3)
	vertical_bar = sprites.menu_sheet.getImage(0,16,3,1)
	horizontal_bar = sprites.menu_sheet.getImage(1,18,1,3)

	image.blit(top_left_corner, (0,0))
	image.blit(top_right_corner, (image.get_width() - 3,0))
	image.blit(bottom_left_corner, (0,image.get_height() - 3))
	image.blit(bottom_right_corner, (image.get_width() - 3,image.get_height() - 3))

	x = 3
	while x < image.get_width() - 3:
		image.blit(horizontal_bar, (x,0))
		image.blit(horizontal_bar, (x,image.get_height() - 3))
		x += 1

	y = 3
	while y < image.get_height() - 3:
		image.blit(vertical_bar, (0,y))
		image.blit(vertical_bar, (image.get_width() - 3,y))
		y += 1

	return(image)


def Build_CPU_Screen(surface):
	image = surface#.copy()

	dark_color = (43,33,65)
	light_color = (38,37,41)
	color_switch = True
	thickness = 3
	options.y_offset += 0.1 * options.DT
	#image.fill(dark_color)

	y = int(options.y_offset)
	if options.y_offset >= 0:
		y = -6
		options.y_offset = -6
	
	while y < image.get_height():
		if color_switch is True:
			color = light_color
			color_switch = False
		else:
			color = dark_color
			color_switch = True
		#if color == light_color:
		pygame.draw.rect(image, color, (0,0 + y,image.get_width(),thickness), 0)
		y += thickness

	return(image)
'''
def Build_CPU_Screen(surface):
	image = surface#.copy()

	dark_color = (48,29,69)
	light_color = (38,37,41)
	color_switch = True
	thickness = 3
	image.fill(dark_color)

	return(image)
'''

