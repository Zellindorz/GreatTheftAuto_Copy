# Importing packages
import json
import random
import pygame as pg
import sys
import time
import math
from pygame import mixer
pg.init()

# Display settings
WIDTH, HEIGHT = 1300, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Great Theft Auto")
clock = pg.time.Clock()


# ---UTILITY FUNCTIONS---

def get_image(path, size):
    # Imports, loads, and scales an image (Matin)
    return pg.transform.scale(pg.image.load(path).convert_alpha(), size)

def play_audio(track_path, period):
    # Loads and plays audio either temporarily or indefinitely (Matin)
    pg.mixer.music.load(track_path)
    pg.mixer.music.set_volume(audio)
    if period == "y":
        pg.mixer.music.play(-1)
    elif period == "n":
        pg.mixer.music.play()

def draw_text(text, font, color, x, y, center=False):
    # Writes text easily (ChatGPT)
    text_display = font.render(text, True, color)
    text_rect = text_display.get_rect(center=(x,y)) if center else (x,y)
    screen.blit(text_display, text_rect)

def handle_events():
    # Handles quitting the game and clicking k to save the game (Julian)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_k:
                save_game_state()
    return True

def save_game_state():
    # Saves the money, audio, and brightness in gamesave.json (Julian)
    print("Saving game...")
    game_state = {
        'brightness': brightness,
        'audio': audio,
        'money': money_total,
    }
    # Save the game state to a JSON file
    with open('gamesave.json', 'w') as f:
        json.dump(game_state, f)

def load_game_state():
    # Loads the money, audio, and brightness from gamesave.json (Julian, ChatGPT)
    try:
        with open('gamesave.json', 'r') as f:
            print("Loading save state...")
            game_state = json.load(f)
            # Restore the saved game state
            global audio, brightness, money_total
            brightness = game_state['brightness']
            audio = game_state['audio']
            money_total = game_state['money']
            print("Game state loaded successfully!")

    except FileNotFoundError:
        print("Save file not found, resetting save...")
        return False
    return True


# ---VARIABLES---

# Font variables & constant variables
SMALL_FONT1 = pg.font.SysFont("impact", 30)
SMALL_FONT2 = pg.font.SysFont("impact", 50)
SMALL_FONT3 = pg.font.SysFont("impact", 60)
SHOOTER_WIDTH = 800
SHOOTER_HEIGHT = 600
SHOOTER_ACTIVE = False
ROBBERY_SUCCESSFUL = False
MED_FONT = pg.font.SysFont("impact", 70)
BIG_FONT = pg.font.SysFont("impact", 130)
ARTIFACT_SIZE = (100,100)
CHARACTER_SIZE = (100, 100)
BACKGROUND_SIZE = (1302, 802)
SIGN_SIZE = (150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Image & asset variables
# Character images
character_img = get_image(r"character_guy.png", CHARACTER_SIZE)
crazy_img = get_image(r"crazy_skin.png", CHARACTER_SIZE)
astronaut_img = get_image(r"astronaut_skin.png", CHARACTER_SIZE)
akimbo_img = get_image(r"akimbo_skin.png", CHARACTER_SIZE)
wizard_img = get_image(r"wizard_skin.png", CHARACTER_SIZE)
guard_img = get_image(r"guard_bat.png", (75, 75))

# General backgruonds
background_image = get_image(r"gta_background2.webp", (WIDTH,HEIGHT))
crosswalk_img = get_image(r"crosswalk.png", BACKGROUND_SIZE)
shop_img = get_image(r"shop_img2.png", BACKGROUND_SIZE)
settings_background = get_image(r"settings_background.jpg",BACKGROUND_SIZE)
cutscene_background = get_image(r"bank_cutscene_img.webp",BACKGROUND_SIZE)
bank_victory_img = get_image(r'bank_victory_img.webp', (50, 50))
gta_game_over = get_image(r'gta_game_over.png', (50, 50))
chasedown_background = get_image(r'chasedown_background.png', (50, 50))
road = get_image(r'road.png', (50, 50))

# Bank image tiles
bank_img_bottom_middle = get_image(r"bank_tile_1.png", BACKGROUND_SIZE)
bank_img_bottom_right = get_image(r"bank_tile_2.png", BACKGROUND_SIZE)
bank_img_top_right = get_image(r"bank_tile_3.png", BACKGROUND_SIZE)
bank_img_top_middle = get_image(r"bank_tile_4.png", BACKGROUND_SIZE)
bank_img_top_left = get_image(r"bank_tile_5.png", BACKGROUND_SIZE)
bank_img_bottom_left = get_image(r"bank_tile_6.png", BACKGROUND_SIZE)

# Artifact images
artifact_1 = get_image(r"Artifact_1.webp", ARTIFACT_SIZE)
artifact_2 = get_image(r"Artifact_2.webp", ARTIFACT_SIZE)
artifact_3 = get_image(r"Artifact_3.webp", ARTIFACT_SIZE)
artifact_4 = get_image(r"Artifact_4.webp", ARTIFACT_SIZE)
artifact_5 = get_image(r"Artifact_5.webp", ARTIFACT_SIZE)
artifact_6 = get_image(r"Artifact_6.webp", ARTIFACT_SIZE)
artifact_7 = get_image(r"Artifact_7.webp", ARTIFACT_SIZE)
artifact_8 = get_image(r"Artifact_8.webp", ARTIFACT_SIZE)
artifact_9 = get_image(r"Artifact_9.webp", ARTIFACT_SIZE)
artifact_10 = get_image(r"Artifact_10.webp", ARTIFACT_SIZE)

# Car images
car_image = get_image(r"car.png", (400,400))
escape_car = get_image(r'escape_car.png', (50, 50))
escape_car = get_image(r'escape_car.png', (50, 50))

# Decal images
shop_sign = get_image(r"shop_sign_img.png", SIGN_SIZE)
shop_arrow = get_image(r"arrow2_img.png", SIGN_SIZE)
menu_sign = get_image(r"menu_img.png", SIGN_SIZE)
menu_arrow = get_image(r"arrow1_img.png", SIGN_SIZE)

# Miscellaneous images
settings_gear = get_image(r"menu_gear.png", (100, 100))
stopwatch_img = get_image(r'stopwatch.webp', (50, 50))
waterballoons = get_image(r'waterballoon.png', (50, 50))
cash_bags = get_image(r'cash_bags.png', (50, 50))

# Title images
great_text = get_image(r'great_text.png', BACKGROUND_SIZE)
theft_text = get_image(r'theft_text.png', BACKGROUND_SIZE)
auto_text = get_image(r'auto_text.png', BACKGROUND_SIZE)

# Global variables
# Important
game_state = "menu"
x, y = 650, 400 # Player position
velocity = 10
keys = pg.key.get_pressed()

# Setting variables
audio = 0.5
brightness = 0.8
typewritering = True
paused = False

# Character variables
character_custom = character_img
is_custom_skin = 0
character_menu_bug_fix = False

# Time variables
timer = 0
last_time = 0
total_timer = int(pg.time.get_ticks()/ 1000)
time_adder = 0

# Powerup variables
chance_powerup = 2
room_powerup = 0
room_num = 0

# Money variable
money_total = 0
money_stolen = 0
artifact_count = 0

# Guard variables
guard1_x = 300
guard1_y = 100

guard2_x = 1000
guard2_y = 100

guard3_x = 1000
guard3_y = 700

guard4_x = 300
guard4_y = 700


# ---MAIN MENU---

play_audio("gta_song.mp3", "y")

def menu():
    # Generates main menu screen (Henry, Matin, Julian)
    global chance_powerup, room_powerup
    chance_powerup = 2
    room_powerup = random.randint(1, 6)
    mouse_pos = pg.mouse.get_pos()
    
    screen.blit(background_image, (0, 0))
    overlay = pg.Surface((600, 800), pg.SRCALPHA)
    overlay.fill((20, 20, 20, 180))
    screen.blit(overlay, (365, 20))
    
    title_positions = [
        ("great_text.png", (300, 120), (490, 40)),
        ("theft_text.png", (300, 120), (570, 140)),
        ("auto_text.png", (300, 100), (500, 260))
    ]
    
    for image_name, size, pos in title_positions:
        glow_surf = get_image(image_name, (size[0] + 10, size[1] + 10))
        glow_surf.set_alpha(100)
        screen.blit(glow_surf, (pos[0] - 5, pos[1] - 5))
        main_image = get_image(image_name, size)
        screen.blit(main_image, pos)

    buttons = [
        ("Start", (540, 400, 250, 50), (255, 215, 0), (230, 199, 2)),
        ("Instructions", (540, 500, 250, 50), (255, 140, 0), (224, 124, 0)),
        ("Quit", (540, 600, 250, 50), (255, 0, 0), (222, 16, 2))
    ]
    
    for text, rect, color, hover_color in buttons:
        button_rect = pg.Rect(rect)
        is_hover = button_rect.collidepoint(mouse_pos)

        if is_hover:
            glow_surf = pg.Surface((rect[2] + 10, rect[3] + 10), pg.SRCALPHA)
            pg.draw.rect(glow_surf, (*color, 50), (0, 0, rect[2] + 10, rect[3] + 10), border_radius=10)
            screen.blit(glow_surf, (rect[0] - 5, rect[1] - 5))
        
        shadow_rect = button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pg.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=8)
        
        button_color = hover_color if is_hover else color
        pg.draw.rect(screen, button_color, button_rect, border_radius=8)
        text_surface = SMALL_FONT1.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    settings_pos = (1150, 50)
    if pg.Rect(*settings_pos, 100, 100).collidepoint(mouse_pos):
        glow_surf = pg.Surface((120, 120), pg.SRCALPHA)
        glow_surf.blit(settings_gear, (10, 10))
        glow_surf.set_alpha(100)
        screen.blit(glow_surf, (1140, 40))
    screen.blit(settings_gear, settings_pos)
    
    start_button = pg.Rect(530, 400, 250, 50)
    instructions_button = pg.Rect(530, 500, 250, 50)
    quit_button = pg.Rect(530, 600, 250, 50)
    settings_button = pg.Rect(1150, 50, 100, 100)
    
    brightness_surface()
    Artifact.reset_game()
    handle_menu_events(start_button, quit_button, instructions_button, settings_button)

def handle_menu_events(start_button, quit_button, instructions_button, settings_button):
    # Handles buttons and redirects in the menu (Henry)
    global game_state
    global x,y
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            if start_button.collidepoint(mouse_pos):
                print("Starting game...")
                x, y = 650, 400
                game_state = "crosswalk"
                pg.mixer.music.stop()
                play_audio("city_background.mp3", "y")

            if settings_button.collidepoint(mouse_pos):
                print("Settings...")
                game_state = "settings"
                pg.mixer.music.stop()
                play_audio("elevator_music.mp3", "y")

            if instructions_button.collidepoint(mouse_pos):
                print("Instructions...")
                game_state = "instructions"
                
            if quit_button.collidepoint(mouse_pos):
                print("Quitting game...")
                save_game_state()
                print("Saving...")
                pg.quit()
                sys.exit()

class Button():
    # Handles buttons in the settings (Julian)
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def brightness_surface():
    # Handles brightness everywhere (Matin)
    brightness_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    brightness_surface.fill((0, 0, 0, int((1 - brightness) * 200)))  # Darken screen
    screen.blit(brightness_surface, (0, 0))

def settings():
    # Changes audio, brightness, and loads gamesave file + credits (Julian)
    global audio, brightness
    
    volume_slider_rect = pg.Rect(350, HEIGHT // 2 - 25, 300, 10)
    brightness_slider_rect = pg.Rect(350, HEIGHT // 2 + 50, 300, 10)
    volume_knob_rect = pg.Rect(0, 0, 20, 30)
    brightness_knob_rect = pg.Rect(0, 0, 20, 30)
    options = pg.mixer.Sound("elevator_music.mp3")
    dragging_volume = False
    dragging_brightness = False

    while True:
        screen.blit(settings_background, (0, 0))
        mouse_pos = pg.mouse.get_pos()

        overlay = pg.Surface((WIDTH - 200, HEIGHT - 200))
        overlay.fill((20, 20, 20))
        overlay.set_alpha(200)
        screen.blit(overlay, (100, 100))

        title_text = "SETTINGS"
        title_shadow = BIG_FONT.render(title_text, True, (0, 0, 0))
        title = BIG_FONT.render(title_text, True, (255, 215, 0))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 2, 120))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 118))

        buttons = [
            Button(None, (WIDTH//2 - 400, HEIGHT - 100), "Back", MED_FONT, BLACK, (255, 215, 0)),
            Button(None, (WIDTH//2, HEIGHT - 100), "Credits", MED_FONT, BLACK, (255, 215, 0)),
            Button(None, (WIDTH//2 + 400, HEIGHT - 100), "Load Game", MED_FONT, BLACK, (255, 215, 0))
        ]

        volume_text = SMALL_FONT2.render(f"VOLUME: {int(audio * 100)}%", True, (255, 255, 255))
        pg.draw.rect(screen, (100, 100, 100), volume_slider_rect)
        pg.draw.rect(screen, (255, 215, 0), (volume_slider_rect.x, volume_slider_rect.y, 
                    volume_slider_rect.width * audio, volume_slider_rect.height))
        volume_knob_x = int(volume_slider_rect.x + audio * volume_slider_rect.width)
        volume_knob_rect.center = (volume_knob_x, volume_slider_rect.y + volume_slider_rect.height // 2)
        pg.draw.rect(screen, (255, 255, 255), volume_knob_rect)
        screen.blit(volume_text, (volume_slider_rect.x + 320, volume_slider_rect.y - 30))

        brightness_text = SMALL_FONT2.render(f"BRIGHTNESS: {int(brightness * 100)}%", True, (255, 255, 255))
        pg.draw.rect(screen, (100, 100, 100), brightness_slider_rect)
        pg.draw.rect(screen, (255, 215, 0), (brightness_slider_rect.x, brightness_slider_rect.y,
                    brightness_slider_rect.width * brightness, brightness_slider_rect.height))
        brightness_knob_x = int(brightness_slider_rect.x + brightness * brightness_slider_rect.width)
        brightness_knob_rect.center = (brightness_knob_x, brightness_slider_rect.y + brightness_slider_rect.height // 2)
        pg.draw.rect(screen, (255, 255, 255), brightness_knob_rect)
        screen.blit(brightness_text, (brightness_slider_rect.x + 320, brightness_slider_rect.y - 30)) 

        for button in buttons:
            button.changeColor(mouse_pos)
            button.update(screen)

        brightness_surface()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if volume_knob_rect.collidepoint(mouse_pos):
                    dragging_volume = True
                elif brightness_knob_rect.collidepoint(mouse_pos):
                    dragging_brightness = True
                elif buttons[0].checkForInput(mouse_pos): 
                    options.stop()
                    pg.mixer.music.play(-1)
                    return "menu"
                elif buttons[1].checkForInput(mouse_pos):  
                    return "credits"
                elif buttons[2].checkForInput(mouse_pos):  
                    load_game_state()
                    return "menu"

            if event.type == pg.MOUSEBUTTONUP:
                dragging_volume = dragging_brightness = False
            
            if event.type == pg.MOUSEMOTION:
                if dragging_volume and volume_slider_rect.collidepoint(event.pos):
                    relative_x = event.pos[0] - volume_slider_rect.x
                    audio = max(0, min(1, relative_x / volume_slider_rect.width))
                    pg.mixer.music.set_volume(audio)
                    options.set_volume(audio)
                elif dragging_brightness and brightness_slider_rect.collidepoint(event.pos):
                    relative_x = event.pos[0] - brightness_slider_rect.x
                    brightness = max(0, min(1, relative_x / brightness_slider_rect.width))
        pg.display.update()

def credits():
    # Shows the credits (Julian)
    while True:
        screen.blit(settings_background, (0, 0))
        mouse_pos = pg.mouse.get_pos()

        overlay = pg.Surface((WIDTH - 200, HEIGHT - 200))
        overlay.fill((20, 20, 20))
        overlay.set_alpha(200)
        screen.blit(overlay, (100, 100))

        title_text = "CREDITS"
        title_shadow = BIG_FONT.render(title_text, True, (0, 0, 0))
        title = BIG_FONT.render(title_text, True, (255, 215, 0))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 2, 120))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 118))

        # Credits content
        credits_text = [
            "Game Development Team",
            "Lead Developers: Matin, Julian, Henry",
            "Art Director: Julian, Henry, Matin",
            "Sound Design: Henry, Matin, Julian",
            "",
            "Special Thanks",
            "Chat GPT",
            "Youtube",
            "The Internet"
        ]

        y_offset = 250 
        spacing = 45 

        for i, text in enumerate(credits_text):
            color = (255, 215, 0) if i == 0 or i == 5 else (255, 255, 255)
            text_surface = SMALL_FONT1.render(text, True, color)
            screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_offset))
            y_offset += spacing

        back_button = Button(None, (WIDTH//2, HEIGHT - 100), "Back", MED_FONT, BLACK, (255, 215, 0))
        back_button.changeColor(mouse_pos)
        back_button.update(screen)

        brightness_surface()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    return "settings"

        pg.display.update()

def typewriter_text(text, font, surface, position):
    # Generates typewriting graphic for instructions (Henry, Julian, ChatGPT)
    global typewritering
    x, y = position
    text_surface = ""
    for char in text:
        text_surface += char
        rendered_text = font.render(text_surface, True, (WHITE))
        surface.blit(rendered_text, (x, y))
        time.sleep(0.0012) 
        pg.display.update()
        if typewritering == True:
            continue
        else:
            break

def instructions():
    # Instructions page explaining how to play and what to do (Henry, Julian, ChatGPT)
    global typewritering, game_state
    mouse_pos = pg.mouse.get_pos()
    
    screen.blit(background_image, (0,0))
    current_time = pg.time.get_ticks()
    parallax_offset = math.sin(current_time * 0.001) * 5

    main_box = pg.Surface((1150, 650), pg.SRCALPHA)
    gradient_color = (20, 20, 20, 180)
    main_box.fill(gradient_color)
    screen.blit(main_box, (95, 100))
    
    header_text = "INSTRUCTIONS"
    header_font = pg.font.Font(None, 68)
    header_shadow = header_font.render(header_text, True, (0, 0, 0))
    header_main = header_font.render(header_text, True, (255, 215, 0))
    screen.blit(header_shadow, (152 + parallax_offset, 122))
    screen.blit(header_main, (150 + parallax_offset, 120))

    instructions_text = [
        ("Welcome to Great Theft Auto!", SMALL_FONT2),
        ("You need to forcefully borrow some money from the bank.", SMALL_FONT1),
        ("There are guards that protect the money!", SMALL_FONT1),
        ("Try to avoid the guards and grab as many artifacts as you can.", SMALL_FONT1),
        ("The cops will arrive quickly so go in and go out as fast as you can.", SMALL_FONT1),
        ("Buy speed boost and skins in the shop to help your journey.", SMALL_FONT1),
        ("Movement Keys:", SMALL_FONT3),
        ("W", SMALL_FONT3),
        ("A   S   D", SMALL_FONT3)
    ]

    positions = [
        (150,200), (150,260), (150,300), (150,340),
        (150,380), (150,420), (150,460), (200,540), (150,620)
    ]

    wborder = pg.Surface((70, 75), pg.SRCALPHA)
    wborder.fill((0, 0, 0, 130))
    screen.blit(wborder, (190, 540))
    
    asdborder = pg.Surface((195, 80), pg.SRCALPHA)
    asdborder.fill((0, 0, 0, 100))
    screen.blit(asdborder, (135, 615))

    if typewritering:
        for text, font in instructions_text:
            typewriter_text(text, font, screen, positions[instructions_text.index((text, font))])
        typewritering = False
    else:
        for (text, font), position in zip(instructions_text, positions):
            text_display = font.render(text, True, WHITE)
            screen.blit(text_display, position)

    back_button = pg.Rect(530, 650, 250, 50)
    mouse_hover = back_button.collidepoint(mouse_pos)
    
    if mouse_hover:
        glow_surf = pg.Surface((260, 60), pg.SRCALPHA)
        pg.draw.rect(glow_surf, (255, 215, 0, 50), (0, 0, 260, 60), border_radius=10)
        screen.blit(glow_surf, (525, 645))
    
    button_color = (255, 215, 0) if not mouse_hover else (230, 199, 2)
    pg.draw.rect(screen, button_color, back_button, border_radius=8)
    
    back_text = SMALL_FONT1.render("Back", True, BLACK)
    text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, text_rect)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if back_button.collidepoint(mouse_pos):
                play_audio("gta_song.mp3", "y")
                game_state = "menu"
    
    brightness_surface()


# ---GAME PHASE 1--- (BANK ROBBERY)

# Guards
def guard1(x_cord, y_cord):
    # Guard characters that move towards the player and causes the player to lose if they collide (Matin)
    global guard1_x
    global guard1_y
    global game_state
    speed = 8
    
    dx = x - x_cord + 50
    dy = y - y_cord + 60
    dist = math.sqrt(dx * dx + dy * dy)
    
    if artifact_count > 0:
        if dist > 0:
            dx /= dist
            dy /= dist
            x_cord += dx * speed
            y_cord += dy * speed

    angle = math.degrees(math.atan2(y - y_cord, x - x_cord))
    guard_rotation = pg.transform.rotate(guard_img, -angle)

    guard_rect = guard_rotation.get_rect(center=(x_cord-50, y_cord-50))
    screen.blit(guard_rotation, guard_rect.center)

    if artifact_count > 0 and dist < 10:
        guard_collide = pg.Rect.colliderect(character_profile(), guard_rect)
        if guard_collide:
            game_state = "game_over"
    
    return x_cord, y_cord

def guard2(x_cord, y_cord):
    # Guard characters that move towards the player and causes the player to lose if they collide (Matin)
    global guard2_x
    global guard2_y
    global game_state
    speed = 3
    
    dx = x - x_cord + 50
    dy = y - y_cord + 60
    dist = math.sqrt(dx * dx + dy * dy)
    
    if artifact_count > 0:
        if dist > 0:
            dx /= dist
            dy /= dist
            x_cord += dx * speed
            y_cord += dy * speed
    
    angle = math.degrees(math.atan2(y - y_cord, x - x_cord))
    guard_rotation = pg.transform.rotate(guard_img, -angle)

    guard_rect = guard_rotation.get_rect(center=(x_cord-50, y_cord-50))
    screen.blit(guard_rotation, guard_rect.center)

    if artifact_count > 0 and dist < 10:
        guard_collide = pg.Rect.colliderect(character_profile(), guard_rect)
        if guard_collide:
            game_state = "game_over"
    
    return x_cord, y_cord

def guard3(x_cord, y_cord):
    # Guard characters that move towards the player and causes the player to lose if they collide (Matin)
    global guard3_x
    global guard3_y
    global game_state
    speed = 5
    
    dx = x - x_cord + 50
    dy = y - y_cord + 60
    dist = math.sqrt(dx * dx + dy * dy)
    
    if artifact_count > 0:
        if dist > 0:
            dx /= dist
            dy /= dist
            x_cord += dx * speed
            y_cord += dy * speed
    
    angle = math.degrees(math.atan2(y - y_cord, x - x_cord))
    guard_rotation = pg.transform.rotate(guard_img, -angle)

    guard_rect = guard_rotation.get_rect(center=(x_cord-50, y_cord-50))
    screen.blit(guard_rotation, guard_rect.center)

    if artifact_count > 0 and dist < 10:
        guard_collide = pg.Rect.colliderect(character_profile(), guard_rect)
        if guard_collide:
            game_state = "game_over"
    
    return x_cord, y_cord

def guard4(x_cord, y_cord):
    # Guard characters that move towards the player and causes the player to lose if they collide (Matin)
    global guard4_x
    global guard4_y
    global game_state
    speed = 7

    dx = x - x_cord + 50
    dy = y - y_cord + 60
    dist = math.sqrt(dx * dx + dy * dy)

    if artifact_count > 0:
        if dist > 0:
            dx /= dist
            dy /= dist
            x_cord += dx * speed
            y_cord += dy * speed
    
    angle = math.degrees(math.atan2(y - y_cord, x - x_cord))
    guard_rotation = pg.transform.rotate(guard_img, -angle)

    guard_rect = guard_rotation.get_rect(center=(x_cord-50, y_cord-50))
    screen.blit(guard_rotation, guard_rect.center)

    if artifact_count > 0 and dist < 10:
        guard_collide = pg.Rect.colliderect(character_profile(), guard_rect)
        if guard_collide:
            game_state = "game_over"
    
    return x_cord, y_cord

class Artifact:
    # Ables artifacts to be picked up and stolen to add money to character (Matin)
    global last_time
    def __init__(self, img, pos, price, room):
        self.img = img
        self.pos = pos
        self.rect = pg.Rect(pos, ARTIFACT_SIZE)
        self.price = price
        self.room = room
        self.stolen = False
    
    def is_colliding(self, other):
        if self.stolen or self.room != game_state:
            return False
        return self.rect.colliderect(other)
    
    def pickup(self):
        global money_stolen, artifact_count
        if (artifact_count >= 11): return

        self.stolen = True
        money_stolen += self.price

        artifact_count += 1

    def draw(self, screen):
        if self.stolen or self.room != game_state:
            return
        screen.blit(self.img, self.pos)

    def reset_game():
        for artifact in artifacts:
            artifact.stolen = False

# Artifacts
artifacts = [
    Artifact(artifact_1, (310, 608), 100, "bank_top_middle"),
    Artifact(artifact_2, (1010, 608), 100, "bank_top_middle"),
    Artifact(artifact_3, (225, 608), 100, "bank_top_left"),
    Artifact(artifact_4, (1010, 608), 100, "bank_top_left"),
    Artifact(artifact_5, (225, 480), 100, "bank_bottom_left"),
    Artifact(artifact_6, (225, 150), 100, "bank_bottom_left"),
    Artifact(artifact_7, (985, 610), 100, "bank_top_right"),
    Artifact(artifact_8, (985, 360), 100, "bank_top_right"),
    Artifact(artifact_9, (895, 525), 100, "bank_bottom_right"),
    Artifact(artifact_10, (895, 125), 100, "bank_bottom_right")
]

def artifact_logic():
    transparent_guy_rect = pg.Surface((100, 100), pg.SRCALPHA)
    if character_menu_bug_fix == False:
        character_rect = screen.blit(transparent_guy_rect, (x, y))
    elif character_menu_bug_fix == True:
        character_rect = character_profile()

    for artifact in artifacts:
        if (artifact.is_colliding(character_rect)):
            artifact.pickup()
        artifact.draw(screen)

# Character logic

def character_profile():
    # Generates the character on the screen and face the direction of the mouse (Matin)
    global x, y
    mouse_pos = pg.mouse.get_pos()

    # Character rotation
    angle = math.degrees(math.atan2(mouse_pos[1] - y - 50, mouse_pos[0] - x - 60))
    character_rotation = pg.transform.rotate(character_custom, -angle)
    character = screen.blit(character_rotation, (x, y))

    return character
def character_movement():
    # Allows the character to move around (Matin)
    keys = pg.key.get_pressed()
    global x, y

    if keys[pg.K_w] and y > 0:
        y -= velocity
    if keys[pg.K_s] and y < HEIGHT - 100:
        y += velocity
    if keys[pg.K_a] and x > 0:
        x -= velocity
    if keys[pg.K_d] and x < WIDTH - 100:
        x += velocity
    if keys[pg.K_ESCAPE]:
        return

# Sensor detection

def sensors(left, right, up, down, state_left, state_right, state_up, state_down):
    # Detects room changes and teleports the player to the correct room
    global x, y
    global game_state
    character_rect = character_profile()

    # Detects collision with sensor
    left_collide = right_collide = down_collide = up_collide = False
    if left:
        left_sensor = pg.Rect((0, 0, 15, 800))
        left_collide = pg.Rect.colliderect(character_rect, left_sensor) 
    if right:
        right_sensor = pg.Rect((1290, 0, 15, 800))
        right_collide = pg.Rect.colliderect(character_rect, right_sensor) 
    if up:
        up_sensor = pg.Rect((0, 0, 1300, 15))
        up_collide = pg.Rect.colliderect(character_rect, up_sensor) 
    if down:
        down_sensor = pg.Rect((0, 785, 1300, 15))
        down_collide = pg.Rect.colliderect(character_rect, down_sensor)
    
    # Teleports player to the correct room if collision is detected
    if left_collide:
        x = WIDTH - 175
        game_state = state_left
    elif right_collide:
        x = 175
        game_state = state_right
    elif up_collide:
        y = HEIGHT - 175
        game_state = state_up
    elif down_collide:
        y = 175
        game_state = state_down

# Powerup functions

def stopwatch_collision():
    # Detects collision between player and stopwatch (Matin)
    if time_adder != 5:
        stopwatch = screen.blit(stopwatch_img, (650, 400))
        stopwatch_collide = pg.Rect.colliderect(character_profile(), stopwatch)
        if stopwatch_collide:
            return int(5)
        else:
            return int(0)
    else:
        return int(0)

def powerup(room_num):
    # Spawns the stopwatch in the correct room and adds 5 seconds if collisision is detected (Matin)
    if chance_powerup == 2:
        if room_powerup == 1 and room_num == 1:
            return stopwatch_collision()
        elif room_powerup == 2 and room_num == 2:
            return stopwatch_collision()
        elif room_powerup == 3 and room_num == 3:
            return stopwatch_collision()
        elif room_powerup == 4 and room_num == 4:
            return stopwatch_collision()
        elif room_powerup == 5 and room_num == 5:
            return stopwatch_collision()
        elif room_powerup == 6 and room_num == 6:
            return stopwatch_collision()
        else:
            return int(0)
    elif chance_powerup == 1:
        print("trash")
        return int(0)

def overlay():
    # The HUD that tells the player their total money and money they've stolen (Matin)
    global bullets, money_total, money_stolen, last_time, timer, time_adder
    
    # Create semi-transparent white box background
    overlay_box = pg.Surface((300, 150))
    overlay_box.fill((255, 255, 255))
    overlay_box.set_alpha(130)
    screen.blit(overlay_box, (10, 10))
    
    # Stylish gold color for money text
    money_color = (255, 215, 0)
    shadow_color = (60, 60, 60)
    shadow_offset = 2
    
    stopwatch_object = powerup(room_num)
    if stopwatch_object == 5:
        time_adder = 5

    # Enhanced text rendering with shadows
    overlay_details = [
        (f"TOTAL: ${money_total}", (30, 30)),
        (f"STOLEN: ${money_stolen}", (30, 90))
    ]

    for text, position in overlay_details:
        shadow_text = SMALL_FONT2.render(text, True, shadow_color)
        screen.blit(shadow_text, (position[0] + shadow_offset, position[1] + shadow_offset))
        
        # Draw main text
        title = SMALL_FONT2.render(text, True, money_color)
        screen.blit(title, position)

    if artifact_count == 0:
        last_time = pg.time.get_ticks() / 1000

    if artifact_count > 0:
        if timer >= 0:
            timer_count = pg.time.get_ticks() / 1000
            timer = (10 + time_adder) - (timer_count - last_time)
            
            # Enhanced timer display with red color for urgency
            text = f"TIME: {timer // 1 + 1}s"
            
            # Timer shadow
            timer_shadow = SMALL_FONT2.render(text, True, shadow_color)
            screen.blit(timer_shadow, (502, 82))
            
            timer_color = (255, 0, 0) if timer <= 5 else (255, 255, 255)
            timer_text = SMALL_FONT2.render(text, True, timer_color)
            screen.blit(timer_text, (500, 80))

        if timer < 0:
            return "game_over"

# Game loss and game win

def game_over():
    # The game ends because of a loss, all money is lost and everything is reset (Matin, Julian)
    # Reset game variables
    global money_total, money_stolen, artifact_count, bullets, x, y
    global guard1_x, guard1_y, guard2_x, guard2_y, guard3_x, guard3_y, guard4_x, guard4_y
    global game_state, timer, chance_powerup, room_powerup

    # Load and scale game over background
    game_over_bg = pg.image.load("gta_game_over.png")
    game_over_bg = pg.transform.scale(game_over_bg, (WIDTH, HEIGHT))
    screen.blit(game_over_bg, (0, 0))

    # Create semi-transparent overlay box
    overlay_surface = pg.Surface((1302, 802))
    overlay_surface.fill((0, 0, 0))
    overlay_surface.set_alpha(180)
    screen.blit(overlay_surface, (-1, -1))

    # Render text
    lose_text = MED_FONT.render("YOU LOST!", True, (255, 0, 0))
    return_text = MED_FONT.render("Press SPACE to return to the street", True, WHITE)
    
    # Center the text
    screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(return_text, (WIDTH//2 - return_text.get_width()//2, HEIGHT//2 + 20))

    # Reset all game variables
    money_total = money_stolen = artifact_count = 0
    bullets = 7
    x, y = 650, 400
    guard1_x, guard1_y = 300, 100
    guard2_x, guard2_y = 1000, 100
    guard3_x, guard3_y = 1000, 700
    guard4_x, guard4_y = 300, 700
    timer = 0
    chance_powerup = random.randint(1, 2)
    room_powerup = random.randint(1, 6)

    # Check for space key
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        pg.mixer.music.stop()
        play_audio("city_background.mp3", "y")
        Artifact.reset_game()
        return "crosswalk"

def game_ending():
    # The game ends because of a win, all money is gained and everything is reset (Matin)
    # Load and display background
    pg.mixer.music.load("heist_music.mp3","y")
    pg.mixer.music.play(-1)
    global money_stolen, money_total, bullets, artifact_count
    global x, y, guard1_x, guard1_y, guard2_x, guard2_y
    global guard3_x, guard3_y, guard4_x, guard4_y
    global game_state, artifact_count, timer
    global chance_powerup
    global room_powerup
    
    # Load and display background
    victory_bg = pg.image.load("bank_victory_img.webp")
    victory_bg = pg.transform.scale(victory_bg, (WIDTH, HEIGHT))
    screen.blit(victory_bg, (0, 0))
    
    # Create semi-transparent overlay for better text visibility
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Custom GTA-style font rendering with shadow effect
    escaped_text = BIG_FONT.render("HEIST SUCCESSFUL", True, (255, 215, 0))
    artifact_text = MED_FONT.render(f"ARTIFACTS STOLEN: {counter}", True, WHITE)
    money_text = MED_FONT.render(f"CASH ACQUIRED: ${counter * 100}", True, (50, 205, 50))
    continue_text = pg.font.Font(None, 36).render("PRESS SPACE TO BEGIN ESCAPE", True, WHITE)
    
    # Add shadow effect to text
    shadow_offset = 3
    escaped_shadow = BIG_FONT.render("HEIST SUCCESSFUL", True, BLACK)
    artifact_shadow = MED_FONT.render(f"ARTIFACTS STOLEN: {counter}", True, BLACK)
    money_shadow = MED_FONT.render(f"CASH ACQUIRED: ${counter * 100}", True, BLACK)
    
    # Center all text elements
    center_x = WIDTH // 2
    screen.blit(escaped_shadow, (center_x - escaped_text.get_width()//2 + shadow_offset, 150 + shadow_offset))
    screen.blit(escaped_text, (center_x - escaped_text.get_width()//2, 150))
    
    screen.blit(artifact_shadow, (center_x - artifact_text.get_width()//2 + shadow_offset, 300 + shadow_offset))
    screen.blit(artifact_text, (center_x - artifact_text.get_width()//2, 300))
    
    screen.blit(money_shadow, (center_x - money_text.get_width()//2 + shadow_offset, 400 + shadow_offset))
    screen.blit(money_text, (center_x - money_text.get_width()//2, 400))
    
    # Add pulsing effect to continue text
    pulse = abs(math.sin(pg.time.get_ticks() * 0.003)) * 255
    continue_text.set_alpha(int(pulse))
    screen.blit(continue_text, (center_x - continue_text.get_width()//2, 500))
    
    # Reset game variables
    chance_powerup = random.randint(1, 2)
    room_powerup = random.randint(1, 6) 
    timer = 0
    money_total += money_stolen
    money_stolen = 0
    x, y = 650, 400
    artifact_count = 0
    
    # Reset guard positions
    guard1_x, guard1_y = 300, 100
    guard2_x, guard2_y = 1000, 100
    guard3_x, guard3_y = 1000, 700
    guard4_x, guard4_y = 300, 700
    
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        game_state = "shooter"
        shooter_game = ShooterGame(screen, money_stolen)
        Artifact.reset_game()
        return game_state
    
    save_game_state()

# Map generation

def crosswalk():
    # The prologue before the bank heist. Allows you to go back to menu, go to shop, or enter the bank (Matin)
    global character_menu_bug_fix
    global room_num
    global chance_powerup
    global room_powerup
    global time_adder
    time_adder = 0
    chance_powerup = 2
    room_powerup = random.randint(1, 6) 
    room_num = 0
    screen.blit(crosswalk_img, (-1,-1))
    character_rect = character_profile()
    overlay()
    character_movement()

    # Graphics
    shop_crosswalk_sign = screen.blit(shop_sign, (100, 440))
    shop_crosswalk_arrow = screen.blit(shop_arrow, (100, 530))
    menu_crosswalk_sign = screen.blit(menu_sign, (1100, 440))
    menu_crosswalk_arrow = screen.blit(menu_arrow, (1100, 530))
    car = screen.blit(car_image, (450, 480))

    left_sensor = pg.Rect((15, 475, 15, 800))
    left_collide = pg.Rect.colliderect(character_rect, left_sensor) 
    if left_collide:
        return "shop"
    right_sensor = pg.Rect((1290, 0, 15, 800))
    right_collide = pg.Rect.colliderect(character_rect, right_sensor) 
    if right_collide:
        mixer.music.stop()
        play_audio("gta_song.mp3", "y")
        character_menu_bug_fix = False
        return "menu"
    up_sensor = pg.Rect((530, 75, 250, 15))
    if pg.Rect.colliderect(character_rect, up_sensor):
        mixer.music.stop()
        play_audio("heist_music.mp3", "y")
        return "cutscene"
    brightness_surface()
    
def shop():
    # Items can be bought by going over them and clicking E (Matin, Henry)
    global x, y
    global character_custom
    global astronaut_img
    global akimbo_img
    global is_custom_skin
    global money_total
    global velocity

    keys = pg.key.get_pressed()
    screen.blit(shop_img, (-1, -1))

    new_x, new_y = x, y
    if keys[pg.K_a]:
        new_x -= 5
    if keys[pg.K_d]:
        new_x += 5
    if keys[pg.K_w]:
        new_y -= 5
    if keys[pg.K_s]:
        new_y += 5

    character_movement()
    character_rect = character_profile()

    # Create white box for money display
    money_box = pg.Surface((400, 150))
    money_box.fill((255, 255, 255))

    # Render only total money text
    money_text = MED_FONT.render(f"${money_total}", True, (WHITE))
    screen.blit(money_text, (WIDTH//2 - money_text.get_width()//2, 30))

    chest1 = pg.draw.rect(screen, (255, 105, 25), (50, 50, 100, 100))
    chest2 = pg.draw.rect(screen, (170, 255, 35), (1100, 50, 100, 100))
    chest3 = pg.draw.rect(screen, (190, 125, 255), (50, 200, 100, 100))
    chest4 = pg.draw.rect(screen, (210, 135, 55), (1100, 200, 100, 100))

    price1_text = SMALL_FONT1.render("$400", True, (0, 0, 0))
    screen.blit(price1_text, (60, 80))
    price1 = 400

    price2_text = SMALL_FONT1.render("$600", True, (0, 0, 0))
    screen.blit(price2_text, (1110, 80))
    price2 = 600

    price3_text = SMALL_FONT1.render("$1000", True, (0, 0, 0))
    screen.blit(price3_text, (60, 230))
    price3 = 1000

    price4_text = SMALL_FONT1.render("$1500", True, (0, 0, 0))
    screen.blit(price4_text, (1110, 230))
    price4 = 1500

    if keys[pg.K_e]:
        if (character_rect.colliderect(chest1)) and money_total >= price1 and is_custom_skin != 1:
            money_total -= price1
            is_custom_skin = 1
        if (character_rect.colliderect(chest2)) and money_total >= price2 and is_custom_skin != 2:
            money_total -= price2
            is_custom_skin = 2
        if (character_rect.colliderect(chest3)) and money_total >= price3 and is_custom_skin != 3:
            money_total -= price3
            is_custom_skin = 3
        if (character_rect.colliderect(chest4)) and money_total >= price4 and is_custom_skin != 4:
            money_total -= price4
            is_custom_skin = 4
    
    if is_custom_skin == 1:
        character_custom = astronaut_img
        velocity = 14
    elif is_custom_skin == 2:
        character_custom = akimbo_img
        velocity = 16
    elif is_custom_skin == 3:
        character_custom = wizard_img
        velocity = 18
    elif is_custom_skin == 4:
        character_custom = crazy_img
        velocity = 20

    right_sensor = pg.Rect(1290, 460, 15, 800)
    if character_rect.colliderect(right_sensor):
        return "crosswalk"

    brightness_surface()

def cutscene():
    # Creates a descriptive cutscene that explains what to do in the bank (Julian, ChatGPT)
    global game_state, x, y
    
    screen.blit(cutscene_background, (0, 0))

    # Stylish overlay
    overlay = pg.Surface((WIDTH - 200, HEIGHT - 200))
    overlay.fill((20, 20, 20))
    overlay.set_alpha(200)
    screen.blit(overlay, (100, 100))

    # Title with shadow
    title_text = "THE HEIST BEGINS"
    title_shadow = BIG_FONT.render(title_text, True, (0, 0, 0))
    title = BIG_FONT.render(title_text, True, (255, 215, 0))
    screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 2, 120))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 118))

    # Cutscene text with enhanced styling
    texts = [
        "You enter the bank... The heist begins!",
        "Collect artifacts and avoid guards!"
    ]
    
    y_offset = 250
    for text in texts:
        text_surface = SMALL_FONT2.render(text, True, WHITE)
        screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_offset))
        y_offset += 60

    # Enhanced buttons
    buttons = [
        ("START HEIST", (530, 400, 250, 50), (255, 215, 0), (230, 199, 2)),
        ("GO BACK", (530, 500, 250, 50), (255, 0, 0), (222, 16, 2))
    ]
    
    mouse_pos = pg.mouse.get_pos()
    
    for text, rect, color, hover_color in buttons:
        button_rect = pg.Rect(rect)
        is_hover = button_rect.collidepoint(mouse_pos)
        
        # Button glow effect on hover
        if is_hover:
            glow_surf = pg.Surface((rect[2] + 10, rect[3] + 10), pg.SRCALPHA)
            pg.draw.rect(glow_surf, (*color, 50), (0, 0, rect[2] + 10, rect[3] + 10), border_radius=10)
            screen.blit(glow_surf, (rect[0] - 5, rect[1] - 5))
        
        # Main button with shadow
        shadow_rect = button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pg.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=8)
        
        button_color = hover_color if is_hover else color
        pg.draw.rect(screen, button_color, button_rect, border_radius=8)
        
        # Button text with shadow
        text_main = SMALL_FONT1.render(text, True, BLACK)
        text_rect = text_main.get_rect(center=button_rect.center)
        screen.blit(text_main, text_rect)

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.Rect(530, 400, 250, 50).collidepoint(mouse_pos):
                game_state = "bank_bottom_middle"
                y = HEIGHT - 185
            elif pg.Rect(530, 500, 250, 50).collidepoint(mouse_pos):
                game_state = "crosswalk"
                y = 185

    brightness_surface()
    pg.display.update()


def pause_screen():
    # Pauses the game, able to change audio and brightness (Julian)
    global audio, brightness, game_state
    global paused
    
    volume_slider_rect = pg.Rect(350, HEIGHT // 2 - 25, 300, 10)
    brightness_slider_rect = pg.Rect(350, HEIGHT // 2 + 50, 300, 10)
    volume_knob_rect = pg.Rect(0, 0, 20, 30)
    brightness_knob_rect = pg.Rect(0, 0, 20, 30)
    dragging_volume = False
    dragging_brightness = False
    
    while True:
        mouse_pos = pg.mouse.get_pos()
        screen.blit(settings_background, (0, 0))

        overlay = pg.Surface((WIDTH - 200, HEIGHT - 200))
        overlay.fill((20, 20, 20))
        overlay.set_alpha(200)
        screen.blit(overlay, (100, 100))

        title_text = "PAUSED"
        title_shadow = BIG_FONT.render(title_text, True, (0, 0, 0))
        title = BIG_FONT.render(title_text, True, (255, 215, 0))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 2, 120))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 118))

        volume_text = SMALL_FONT2.render(f"VOLUME: {int(audio * 100)}%", True, (255, 255, 255))
        pg.draw.rect(screen, (100, 100, 100), volume_slider_rect)
        pg.draw.rect(screen, (255, 215, 0), (volume_slider_rect.x, volume_slider_rect.y, 
                    volume_slider_rect.width * audio, volume_slider_rect.height))
        volume_knob_x = int(volume_slider_rect.x + audio * volume_slider_rect.width)
        volume_knob_rect.center = (volume_knob_x, volume_slider_rect.y + volume_slider_rect.height // 2)
        pg.draw.rect(screen, (255, 255, 255), volume_knob_rect)
        screen.blit(volume_text, (volume_slider_rect.x + 420, volume_slider_rect.y - 30))

        brightness_text = SMALL_FONT2.render(f"BRIGHTNESS: {int(brightness * 100)}%", True, (255, 255, 255))
        pg.draw.rect(screen, (100, 100, 100), brightness_slider_rect)
        pg.draw.rect(screen, (255, 215, 0), (brightness_slider_rect.x, brightness_slider_rect.y,
                    brightness_slider_rect.width * brightness, brightness_slider_rect.height))
        brightness_knob_x = int(brightness_slider_rect.x + brightness * brightness_slider_rect.width)
        brightness_knob_rect.center = (brightness_knob_x, brightness_slider_rect.y + brightness_slider_rect.height // 2)
        pg.draw.rect(screen, (255, 255, 255), brightness_knob_rect)
        screen.blit(brightness_text, (brightness_slider_rect.x + 420, brightness_slider_rect.y - 30))

        resume_text = SMALL_FONT2.render("Press ESC to Resume", True, (255, 215, 0))
        resume_shadow = SMALL_FONT2.render("Press ESC to Resume", True, (0, 0, 0))
        screen.blit(resume_shadow, (WIDTH//2 - resume_shadow.get_width()//2 + 2, HEIGHT - 200))
        screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT - 202))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                else:
                    return True

            if event.type == pg.MOUSEBUTTONDOWN:
                if volume_knob_rect.collidepoint(mouse_pos):
                    dragging_volume = True
                elif brightness_knob_rect.collidepoint(mouse_pos):
                    dragging_brightness = True
            
            if event.type == pg.MOUSEBUTTONUP:
                dragging_volume = dragging_brightness = False
            
            if event.type == pg.MOUSEMOTION:
                if dragging_volume and volume_slider_rect.collidepoint(event.pos):
                    relative_x = event.pos[0] - volume_slider_rect.x
                    audio = max(0, min(1, relative_x / volume_slider_rect.width))
                    pg.mixer.music.set_volume(audio)
                elif dragging_brightness and brightness_slider_rect.collidepoint(event.pos):
                    relative_x = event.pos[0] - brightness_slider_rect.x
                    brightness = max(0, min(1, relative_x / brightness_slider_rect.width))

        brightness_surface()
        pg.display.update()

# Bank tiles

def bank_bottom_middle():
    # Tile 5 of the bank map, where you enter (Matin)
    screen.blit(bank_img_bottom_middle, (-1,-1))
    character_rect = character_profile()
    global money_total
    global money_stolen
    global game_state
    global character_menu_bug_fix
    global counter
    global guard1_x
    global guard1_y
    global guard2_x
    global guard2_y
    global guard3_x
    global guard3_y
    global guard4_x
    global guard4_y
    global room_num
    room_num = 5
    guard1_x, guard1_y = guard1(guard1_x, guard1_y)
    guard2_x, guard2_y = guard2(guard2_x, guard2_y)
    guard3_x, guard3_y = guard3(guard3_x, guard3_y)
    guard4_x, guard4_y = guard4(guard4_x, guard4_y)
    character_movement()
    # Teleports player to the correct room if collision is detected
    down_sensor = pg.Rect((580, 780, 150, 15))
    down_collide = pg.Rect.colliderect(character_rect, down_sensor) 
    if down_collide and artifact_count == 0:
        mixer.music.stop()
        play_audio("city_background.mp3", "y")
        character_menu_bug_fix = False
        return "crosswalk"
    if down_collide and artifact_count > 0:
        counter = artifact_count
        return "game_ending"
    left_sensor = pg.Rect((0, 0, 15, 800))
    left_collide = pg.Rect.colliderect(character_rect, left_sensor) 
    right_sensor = pg.Rect((1290, 0, 15, 800))
    right_collide = pg.Rect.colliderect(character_rect, right_sensor) 
    up_sensor = pg.Rect((0, 0, 1300, 15))
    up_collide = pg.Rect.colliderect(character_rect, up_sensor) 
    down_sensor = pg.Rect((0, 785, 1300, 15))
    down_collide = pg.Rect.colliderect(character_rect, down_sensor)
    
    if left_collide:
        return "bank_bottom_left"
    elif right_collide:
        return "bank_bottom_right"
    elif up_collide:
        return "bank_top_middle"
    overlay()
    brightness_surface()

def bank_bottom_right():
    # Tile 6 of the bank map, holds 2 artifacts (Matin)
    screen.blit(bank_img_bottom_right, (-1,-1))
    character_movement()
    global room_num
    room_num = 6
    
    global guard1_x, guard1_y, guard2_x, guard2_y, guard3_x, guard3_y, guard4_x, guard4_y
    guard1_x, guard1_y = guard1(guard1_x, guard1_y)
    guard2_x, guard2_y = guard2(guard2_x, guard2_y)
    guard3_x, guard3_y = guard3(guard3_x, guard3_y)
    guard4_x, guard4_y = guard4(guard4_x, guard4_y)
    
    overlay()
    brightness_surface()
    sensors(True, False, True, False, "bank_bottom_middle", None, "bank_top_right", None)

def bank_top_right():
    # Tile 3 of the bank map, holds 2 artifacts (Matin)
    screen.blit(bank_img_top_right, (-1,-1))
    character_movement()
    global room_num
    room_num = 3
    
    global guard1_x, guard1_y, guard2_x, guard2_y, guard3_x, guard3_y, guard4_x, guard4_y
    guard1_x, guard1_y = guard1(guard1_x, guard1_y)
    guard2_x, guard2_y = guard2(guard2_x, guard2_y)
    guard3_x, guard3_y = guard3(guard3_x, guard3_y)
    guard4_x, guard4_y = guard4(guard4_x, guard4_y)
    
    overlay()
    brightness_surface()
    sensors(True, False, False, True, "bank_top_middle", None, None, "bank_bottom_right")

def bank_top_middle():
    # Tile 2 of the bank map, holds 2 artifacts (Matin)
    screen.blit(bank_img_top_middle, (-1,-1))
    character_movement()
    global room_num
    room_num = 2

    global guard1_x, guard1_y, guard2_x, guard2_y, guard3_x, guard3_y, guard4_x, guard4_y
    guard1_x, guard1_y = guard1(guard1_x, guard1_y)
    guard2_x, guard2_y = guard2(guard2_x, guard2_y)
    guard3_x, guard3_y = guard3(guard3_x, guard3_y)
    guard4_x, guard4_y = guard4(guard4_x, guard4_y)
    
    overlay()
    brightness_surface()
    sensors(True, True, False, True, "bank_top_left", "bank_top_right", None, "bank_bottom_middle")

def bank_top_left():
    # Tile 1 of the bank map, holds 2 artifacts (Matin)
    screen.blit(bank_img_top_left, (-1,-1))
    character_movement()
    global room_num
    room_num = 1
    
    global guard1_x, guard1_y, guard2_x, guard2_y, guard3_x, guard3_y, guard4_x, guard4_y
    guard1_x, guard1_y = guard1(guard1_x, guard1_y)
    guard2_x, guard2_y = guard2(guard2_x, guard2_y)
    guard3_x, guard3_y = guard3(guard3_x, guard3_y)
    guard4_x, guard4_y = guard4(guard4_x, guard4_y)
    
    overlay()
    brightness_surface()
    sensors(False, True, False, True, None, "bank_top_middle", None, "bank_bottom_left")

def bank_bottom_left():
    # Tile 4 of the bank map, holds 2 artifacts (Matin)
    screen.blit(bank_img_bottom_left, (-1,-1))
    character_movement()
    global room_num
    room_num = 3
    
    global guard1_x, guard1_y, guard2_x, guard2_y, guard3_x, guard3_y, guard4_x, guard4_y
    guard1_x, guard1_y = guard1(guard1_x, guard1_y)
    guard2_x, guard2_y = guard2(guard2_x, guard2_y)
    guard3_x, guard3_y = guard2(guard3_x, guard3_y)
    guard4_x, guard4_y = guard4(guard4_x, guard4_y)

    overlay()
    brightness_surface()
    sensors(False, True, True, False, None, "bank_bottom_middle", "bank_top_left", None)

# ---GAME PHASE 2--- (CAR CHASE)

class ShooterGame:
    # Car chase game after the first game phase (Julian)
    def __init__(self, screen, money_stolen):
        pg.mixer.music.load("heist_music.mp3","y")
        pg.mixer.music.play(-1)
        self.screen = screen
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT // 2
        self.player_speed = 7
        self.score = 0
        self.health = 10
        self.font = pg.font.Font(None, 36)
        self.cash_spawn_timer = 0
        self.money_stolen = money_stolen
        self.game_won = False 
        self.win_message_timer = 0 

        # Load and scale images
        self.player_img = pg.image.load("escape_car.png")
        self.player_img = pg.transform.scale(self.player_img, (60, 100))

        self.cop_img = pg.image.load("cop_car.png")
        self.cop_img = pg.transform.scale(self.cop_img, (60, 100))

        self.bullet_img = pg.image.load("waterballoon.png")
        self.bullet_img = pg.transform.scale(self.bullet_img, (20, 20))

        self.background = pg.image.load("chasedown_background.png")
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))

        self.road = pg.image.load("road.png")
        self.road = pg.transform.scale(self.road, (505, HEIGHT))

        self.cash_img = pg.image.load("cash_bags.png")
        self.cash_img = pg.transform.scale(self.cash_img, (30, 30))

        self.road_left = (WIDTH - 700) // 2 + 100
        self.road_right = self.road_left + 505

        self.big_font = pg.font.Font(None, 72)
        
        # Background scrolling variables
        self.bg_y1 = 0
        self.bg_y2 = -HEIGHT
        self.scroll_speed = 5

        self.survival_timer = 0
        self.game_duration = 20 

        self.cops = [
            {'x': WIDTH // 4, 'direction': 1},
            {'x': WIDTH // 2, 'direction': -1},
            {'x': 3 * WIDTH // 4, 'direction': 1}
        ]
        self.cop_speed = 3

        self.bullets = []
        self.cash_bags = []

    def handle_events(self):
        keys = pg.key.get_pressed()
        if self.game_won:
            if self.win_message_timer > 180:  # Only return after showing win screen for 3 seconds
                return "crosswalk"
            return None
                
        if keys[pg.K_a] and self.player_x > self.road_left + 50:  # Left barrier
            self.player_x -= self.player_speed
        if keys[pg.K_d] and self.player_x < self.road_right - 50:  # Right barrier
            self.player_x += self.player_speed
        if keys[pg.K_w] and self.player_y > 20:
            self.player_y -= self.player_speed
        if keys[pg.K_s] and self.player_y < HEIGHT - 100:
            self.player_y += self.player_speed
        return None

    def update(self):
        if self.game_won:
            self.win_message_timer += 1
            if self.win_message_timer > 180:  # 3 seconds at 60 FPS
                return "crosswalk"
            return None

        self.survival_timer += 1/60

        if self.survival_timer >= self.game_duration:
            self.game_won = True
            return None

        # Update cops movement
        if self.cops[0]['x'] < self.road_left + 50:
            for cop in self.cops:
                cop['x'] = random.randint(self.road_left + 50, self.road_right - 50)

        for cop in self.cops:
            new_x = cop['x'] + cop['direction'] * self.cop_speed
            if new_x > self.road_left + 50 and new_x < self.road_right - 50:
                cop['x'] = new_x
            else:
                cop['direction'] *= -1
                
            # Enhanced shooting in final 5 seconds
            if self.game_duration - self.survival_timer <= 5:
                if random.random() < 0.06:  # Triple shooting chance
                    for _ in range(3):  # Shoot 3 bullets at once
                        self.bullets.append({
                            'x': cop['x'],
                            'y': HEIGHT - 50,
                            'speed': 7
                        })
            else:
            # Normal shooting
                if random.random() < 0.02:
                    self.bullets.append({
                        'x': cop['x'],
                        'y': HEIGHT - 50,
                        'speed': 7
                    })

        # Update bullets
        for bullet in self.bullets[:]:
            bullet['y'] -= bullet['speed']
            if bullet['y'] < 0 or bullet['y'] > HEIGHT:
                self.bullets.remove(bullet)

        # Spawn cash bags
        self.cash_spawn_timer += 1

        if self.cash_spawn_timer >= 30:
            self.cash_spawn_timer = 0
            self.cash_bags.append({
                'x': random.randint(self.road_left + 50, self.road_right - 50),
                'y': random.randint(50, HEIGHT - 100)
            })
        # Check collisions with cash
        for cash in self.cash_bags[:]:
            if (abs(self.player_x - cash['x']) < 30 and 
                abs(self.player_y - cash['y']) < 30):
                self.cash_bags.remove(cash)
                self.score += 20

        # Check bullet collisions with player
        for bullet in self.bullets[:]:
            if (abs(self.player_x - bullet['x']) < 20 and 
                abs(self.player_y - bullet['y']) < 20):
                self.bullets.remove(bullet)
                self.health -= 1
                self.score -= 30

    def get_final_money(self):
        global money_stolen
        if self.survival_timer >= self.game_duration:
            return self.money_stolen + self.score
        return 0  

    def draw(self):
        # Draw background first
        self.screen.blit(self.background, (0, self.bg_y1))
        self.screen.blit(self.background, (0, self.bg_y2))
        
        # Update background scroll
        self.bg_y1 += self.scroll_speed
        self.bg_y2 += self.scroll_speed
        
        if self.bg_y1 >= HEIGHT:
            self.bg_y1 = -HEIGHT
        if self.bg_y2 >= HEIGHT:
            self.bg_y2 = -HEIGHT

        # Draw road
        self.screen.blit(self.road, (self.road_left, 0))

        # Draw game elements
        player_rotated = pg.transform.rotate(self.player_img, 0)
        self.screen.blit(player_rotated, (self.player_x - 30, self.player_y - 50))
        
        cop_rotated = pg.transform.rotate(self.cop_img, 180)
        for cop in self.cops:
            self.screen.blit(cop_rotated, (cop['x'] - 30, HEIGHT - 100))
        
        for bullet in self.bullets:
            self.screen.blit(self.bullet_img, (int(bullet['x'] - 10), int(bullet['y'] - 10)))
        
        for cash in self.cash_bags:
            self.screen.blit(self.cash_img, (cash['x'] - 15, cash['y'] - 15))
        
        # Draw HUD
        total_cash = self.money_stolen + self.score
        score_text = self.font.render(f'Total Cash: ${total_cash}', True, (255, 255, 255))
        health_text = self.font.render(f'Health: {self.health}', True, (255, 255, 255))
        timer_text = self.font.render(f'Time: {int(self.game_duration - self.survival_timer)}s', True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 50))
        self.screen.blit(timer_text, (10, 90))

        # Check win condition and draw win screen
        if self.game_won:
            # Create semi-transparent overlay
            overlay = pg.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))

            # Draw win text with shadow
            win_text = self.big_font.render("YOU WIN!", True, (255, 215, 0))
            win_shadow = self.big_font.render("YOU WIN!", True, (0, 0, 0))
            
            text_width = win_text.get_width()
            text_height = win_text.get_height()
            
            shadow_pos = (WIDTH//2 - text_width//2 - 2, HEIGHT//2 - text_height//2 - 2)
            text_pos = (WIDTH//2 - text_width//2, HEIGHT//2 - text_height//2)
            
            self.screen.blit(win_shadow, shadow_pos)
            self.screen.blit(win_text, text_pos)
            
            escape_text = self.font.render("Escape Successful!", True, (255, 255, 255))
            escape_pos = (WIDTH//2 - escape_text.get_width()//2, HEIGHT//2 + 40)
            self.screen.blit(escape_text, escape_pos)
            pg.mixer.music.stop()

def main():
     # Manages the state changes (Matin, Henry, Julian)
    global game_state
    global x, y
    global money_stolen
    global money_total
    global paused
    running = True
    shooter_game = None
    while running:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_game_state()
                print("Saving...")
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if paused == False:
                        paused = True

        if not paused:
            if game_state == "menu":
                menu()
                running = handle_events()
            elif game_state == "settings":
                result = settings()
                if result == "menu":
                    pg.mixer.music.stop()
                    play_audio("gta_song.mp3", "y")
                    game_state = "menu"
                elif result == "credits": 
                    game_state = "credits"
            elif game_state == "credits":
                result = credits()
                if result == "settings":
                        game_state = "settings"

            elif game_state == "instructions":
                instructions()
                running = handle_events()     

            elif game_state == "crosswalk":
                result = crosswalk()
                if result == "shop":
                    x = WIDTH - 185
                    game_state = "shop"
                if result == "menu":
                    x, y = 650, 400
                    game_state = "menu"
                if result == "bank_bottom_middle":
                    y = HEIGHT - 185
                    game_state = "bank_bottom_middle"
                if result == "cutscene":
                    game_state = "cutscene"
                running = handle_events()

            elif game_state == "shop":
                result = shop()
                if result == "crosswalk":
                    x = 150
                    game_state = "crosswalk"
                running = handle_events()

            elif game_state == "cutscene":
                cutscene()
                running = handle_events()
            
            elif game_state == "bank_bottom_middle":
                result = bank_bottom_middle()
                if result == "crosswalk":
                    y = 185
                    game_state = "crosswalk"
                if result == "bank_bottom_left":
                    x = WIDTH - 185
                    game_state = "bank_bottom_left"
                if result == "bank_bottom_right":
                    x = 185
                    game_state = "bank_bottom_right"
                if result == "bank_top_middle":
                    y = HEIGHT - 185
                    game_state = "bank_top_middle"
                if result == "game_ending":
                    game_state = "game_ending"
                running = handle_events()

            elif game_state == "bank_bottom_right":
                bank_bottom_right()
                running = handle_events()

            elif game_state == "bank_top_right":
                bank_top_right()
                running = handle_events()
            
            elif game_state == "bank_top_middle":
                bank_top_middle()
                running = handle_events()

            elif game_state == "bank_top_left":
                bank_top_left()
                running = handle_events()
            
            elif game_state == "bank_bottom_left":
                bank_bottom_left()
                running = handle_events()

            elif game_state == "shooter":
                if shooter_game is None:
                    shooter_game = ShooterGame(screen, money_stolen)

                result = shooter_game.handle_events()
                update_result = shooter_game.update()
                shooter_game.draw()  # Make sure draw is called before checking results

                if result == "crosswalk" or update_result == "crosswalk":
                    money_total += shooter_game.score  
                    game_state = "crosswalk"
                    shooter_game = None
                    x = 650
                    y = 400
                    continue

                if shooter_game.health <= 0:
                    game_state = "game_over"
                    shooter_game = None

                running = handle_events()

            elif game_state == "game_ending":
                result = game_ending()
                if result == "crosswalk":
                    game_state = "crosswalk"
                    x = 650
                    y = 400
                running = handle_events()

            elif game_state == "game_over":
                result = game_over()
                if result == "crosswalk":
                    game_state = "crosswalk"
                    x = 650
                    y = 400
                running = handle_events()
            
            artifact_logic()

            if artifact_count > 0:
                result_overlay = overlay()
                if result_overlay == "game_over":
                    game_state = "game_over"
            
        if paused:
            paused = pause_screen()
        pg.display.flip()
        clock.tick(60)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()