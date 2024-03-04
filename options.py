
import pygame

LIGHT_PURPLE = (254,246,248)
PURPLE = (193,156,244)
DARK_PURPLE = (125,92,220)
OUTLINE_PURPLE = (50,24,108)
MALLOW_LIST = (OUTLINE_PURPLE,DARK_PURPLE,PURPLE,LIGHT_PURPLE,)

LIGHT_BURNT = (160,140,102)
BURNT = (96,71,38)
DARK_BURNT = (66,45,24)
OUTLINE_BURNT = (40,33,26)

YELLOW = (234,184,66)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
FACE = (255,255,255) #just a shade off 'light purple'
ALMOST_BLACK = (51,47,58) #used as black in some of the levels. Ie. lab level.

FIRE_RED = (175,37,50)
FIRE_ORANGE = (210,108,58)
FIRE_YELLOW = (210,172,58)
FIRE_SMOKE = (94,88,114)

ICE = (150,218,255)

MATRIX = (61,46,82)
MATRIX_LIGHT = (99,80,154)
MATRIX_DARK = (43,33,65)

BROWN_ROPE_LIGHT = (161,118,99)
BROWN_ROPE_MEDIUM = (104,66,58)
BROWN_ROPE_DARK = (66,43,40)

WHITE_ROPE_LIGHT = (241,239,253)
WHITE_ROPE_MEDIUM = (209,209,239)
WHITE_ROPE_DARK = (158,153,205)

BLACK_ROPE_LIGHT = (105,103,131)
BLACK_ROPE_MEDIUM = (60,69,63)
BLACK_ROPE_DARK = (31,30,32)

#Ninja Colors:
BLUE_LIST = ((30,32,110), (72,101,222), (57,152,233), (162,230,244))
RED_LIST = ((87,11,42), (175,37,50), (204,74,95), (241,133,174))
GREEN_LIST = ((14,62,46), (36,108,61), (109,180,102), (202,243,153))
PINK_LIST = ((83,22,108), (185,88,206), (212,133,241), (238,183,247))
GREY_LIST = ((51,49,57), (94,88,114), (159,153,205), (210,209,239))
PURPLE_LIST = ((51,24,108), (79,36,136), (126,92,220), (194,156,244))
#ORANGE_LIST = ((83,31,19), (230,127,44), (234,184,66), (243,197, 147))
ORANGE_LIST = ((83,31,19), (177,81,29), (230,127,44), (234,184,66))

#color_choices = [RED_LIST, GREEN_LIST, BLUE_LIST, PINK_LIST, GREY_LIST, PURPLE_LIST, ORANGE_LIST]
color_choices = [RED_LIST, GREEN_LIST, BLUE_LIST, PINK_LIST, GREY_LIST, ORANGE_LIST]

bandana_color_choices = [RED_LIST, GREEN_LIST, BLUE_LIST, PINK_LIST, GREY_LIST, PURPLE_LIST, ORANGE_LIST]
#bandana_color_choices = [RED_LIST, GREEN_LIST, BLUE_LIST, PINK_LIST, GREY_LIST, ORANGE_LIST]

y_offset = 0 #used to scroll the cpu screens throughout the game
glitch_timer = 0

DT = 1 #Delta time kept here

update_state = 1 #1 or 2. Controls updating background sprites. Divides updates.

change_g = 0.3
max_g = 5.1
base_max_g = 5.1
loop_physics = False
inverted_g = False

demo = True
version = 'Demo v0.00'
#version = 'Demo v0.00'
current_version = True

fps = 'Auto'
#fps = 30
auto_fps = 60
current_fps = 60

#server_message = (0,'Thank you for playing the Codename Mallow demo! Please remember: few things in life are more important than defeating your friends and achieving Ninja Supremacy. I wish you all the best on your journey.')
server_message = (0, None)

#screen_resolution = (640, 360)
screen_resolution = (1280, 720)
#screen_resolution = (1920, 1080)

level_builder = None #flips between versus and coop as needed

size_list = [(640,360),(1280,720),(1920,1080)]

blit_frame = True

fullscreen = False


#used to divide ropes into 3 groups. Splits some of the collisoin groups. Allows for more rope joints without breaking FPS
rope_number = 1

test_counter = 0 #purely for testing.

#holds current state of game. controls menu flow etc.
game_state = 'intro' #intro, main_menu, player_select, level, versus_item_options, versus_options, pause, 'versus_level_selection'
#game_state = 'game_options'
game_mode = 'none' #'versus', 'coop'
online = False
versus_mode = 'Classic' #Classic, Points, Stock, Practice, Tutorial
win_condition = 'versus' #'Tutorial', 'Stock', 'Wins', 'Points', 'Practice'
pause_item_options = False #True will give access to item options from pause menu.
banned_items = [] #list of items not available in some levels.


#profile_list = ['-New Profile-', 'Guest', 'Ancalabro', 'PlugWorld', 'Hour', 'TertiaryMap']
profile_list = ['-New Profile-']

upper_case_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','.']
lower_case_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.']

###BELOW THIS IS HELD IN THE VERSUS OPTIONS###
#holds various options
versus_VP_required = 5 #Numbers 1-10
versus_VP_per_weapon_kill = '+1' #'Ego Only', '+1', '+2'
versus_VP_per_duel_win = 'Ego Only' #'Ego Only', '+1 For Last Human/Team Left Standing','+1 For Each Human Left Standing','+2 For Last Human/Team Left Standing','+2 For Each Human Left Standing'
versus_VP_per_FID_received = '-1' #'Ego Only', '-1', '-2', 'Reset to 0'
versus_VP_per_FID_inflicted = 'Ego Only' #'Ego Only', '+1', '+2''

versus_wins_required = 5

#versus_points_earned =  '+1 Last Human/Team Standing' #, '+1 For Last Human/Team Standing', '+1 For Each Human Left Standing', '+1 For Each Weapon Kill'.
#FID_effect = 'Ego Only' #, ['Ego Only', 'Points -1', 'Points to 0', 'Points +1 for Inflictor'

#Visual settings
FPS_counter = 'Off'
rope_physics = 'On'
bandana_physics = 'On'
screen_shake = 'On'

visual_effects = 'High' #ecompasses backgraound_effects, death_anmiations, and particles now!
background_effects = 'High' #'High', 'Low', or 'Off'.'
death_animations = 'On'
particles = 'High' #'High',' 'Low', 'Off'


stage_selection = 'Single Stage Choice' #'Single Stage Choice', 'Single Stage Random', 'Random Each Duel'
platform_density = 'Normal' #very low, low, normal, high, very high
item_spawn_rate = 'Normal' #off, very low, low, normal, high, very high
versus_score_frequency = 5 #'Off', 1,3,5,10 ---How often score is shown.
duel_counter = 0 #counts duels. Resets to 0. Used to count until score frequency.

#hold active/inactive items:
items_dict = {'x' : 'on', 'shoes' : 'on', 'laser' : 'on', 'wings' : 'on', 'skull' : 'on', 'bomb' : 'on', 'volt' : 'on', 'mine' : 'on', 'rocket' : 'on', 'portal gun' : 'off', 'ice bomb' : 'on', 'cloak' : 'on', 'shield' : 'on','homing bomb' : 'off','gravity' : 'off', 'metal suit' : 'off', 'solar flare' : 'off'}
#items_dict = {'x' : 'off', 'shoes' : 'off', 'laser' : 'on', 'wings' : 'off', 'skull' : 'off', 'bomb' : 'off', 'volt' : 'off', 'mine' : 'off', 'rocket' : 'off', 'portal gun' : 'off', 'ice bomb' : 'off', 'cloak' : 'off', 'shield' : 'off','homing bomb' : 'off','gravity' : 'off', 'metal suit' : 'off', 'solar flare' : 'off'}


win_timer = 360#180 #how long you need to survive after 'win' to be credited with a win.
big_lasers = 'on' #on or off

max_lives = 5

music_volume = 0.3
effects_volume = 0.3

#Old, not mused anymore
player1_controls = 'x-input'
player2_controls = 'x-input'
player3_controls = 'x-input'
player4_controls = 'x-input'

#gamepad1_config = False #Now handled in 'Ninja'
#gamepad2_config = False
#gamepad3_config = False
#gamepad4_config = False


###BELOW THIS IS HELD IN THE MAIN MENU OPTIONS###
#hold control preferences:  ---'gamepad' or 'keyboard'
control_preferences = {'player1' : 'gamepad', 'player2' : 'gamepad'}
#control_preferences = {'player1' : 'keyboard', 'player2' : 'keyboard'}
#control_preferences = {'player1' : 'gamepad', 'player2' : 'keyboard'}
#control_preferences = {'player1' : 'keyboard', 'player2' : 'gamepad'}

#Graphics effects
transparency = 'on'


#how many sticky particles before they start disappearing
max_sticky_particles = 500

#screen_resolution = '1280x720' #Supported: 640x360, 1280x720, 1280x800,
#screen_resolution = '1280x720' #Supported: 640x360, 1280x720, 1280x800,

#decides when game exit
exit = False
