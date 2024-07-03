import pygame
import math
import sys
import dsa
import dms
import coa
import random
import json
import os

# Initialize Pygame
pygame.init()

# Set up the initial screen dimensions
screen_width = 1365
screen_height = 710
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Set the title of the window
pygame.display.set_caption("Hangman")


letters = []
lletters = []
llletters = []
guessed = []
gguessed = []
ggguessed = []
bubbles = []
letter_sounds = {}
hangman_status = 0
hhangman_status = 0
hhhangman_status = 0
score = 0
sscore = 0
ssscore = 0
words_guessed = 0
wwords_guessed = 0
wwwords_guessed = 0
GAP = 15
word_index = 0
wword_index = 0
wwword_index = 0
words = dsa.wor
wwords = coa.wor
wwwords = dms.wor
word = words[word_index]
wword = wwords[wword_index]
wwword = wwwords[wwword_index]
clock = pygame.time.Clock()
RADIUS = 30
images = []
iimages = []
iiimages = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

for j in range(7):
    iimage = pygame.image.load("hangman" + str(j) + ".png")
    iimages.append(iimage)

for k in range(7):
    iiimage = pygame.image.load("hangman" + str(k) + ".png")
    iiimages.append(iiimage)

font = pygame.font.SysFont("arialblack", 60)
title_font = pygame.font.SysFont('comicsans', 70)
word_font = pygame.font.SysFont('comicsans', 60)
WORD_FONT = pygame.font.SysFont('comicsans', 70)
LETTER_FONT = pygame.font.SysFont('arial', 40)

win_sound = pygame.mixer.Sound("win.mp3")  # Adjust the file name as per your sound file
sad_sound = pygame.mixer.Sound("sadhorn.mp3")  # Adjust the file name as per your sound file

startx = round((screen_width - (RADIUS * 2 + GAP) * 13) / 2)
starty = 550
A = 65
for i in range(26):
    x = startx + GAP * 13 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])
    letter = chr(65 + i)
    sound_file = "A.mp3"  # Adjust the file name format as per your sound files
    letter_sounds[letter] = pygame.mixer.Sound(sound_file)

for j in range(26):
    xx = startx + GAP * 13 + ((RADIUS * 2 + GAP) * (j % 13))
    yy = starty + ((j // 13) * (GAP + RADIUS * 2))
    lletters.append([xx, yy, chr(A + j), True])
    lletter = chr(65 + j)
    sound_file = "A.mp3"  # Adjust the file name format as per your sound files
    letter_sounds[lletter] = pygame.mixer.Sound(sound_file)

for k in range(26):
    xxx = startx + GAP * 13 + ((RADIUS * 2 + GAP) * (k % 13))
    yyy = starty + ((k // 13) * (GAP + RADIUS * 2))
    llletters.append([xxx, yyy, chr(A + k), True])
    llletter = chr(65 + k)
    sound_file = "A.mp3"  # Adjust the file name format as per your sound files
    letter_sounds[llletter] = pygame.mixer.Sound(sound_file)

# Load background images
background_image_1 = pygame.image.load('desk.jpg')  # Change 'background1.jpg' to your image file path for first screen
background_image_2 = pygame.image.load('1.png')       # Change 'background2.jpg' to your image file path for second screen
nested_screen1_image = pygame.image.load('gg.jpg') # Change 'nested_screen1.jpg' to your image file path for nested screen 1
nested_screen2_image = pygame.image.load('gg.jpg')  # Change 'nested_screen2.jpg' to your image file path for nested screen 2
nested_screen3_image = pygame.image.load('gg.jpg')  # Change 'nested_screen3.jpg' to your image file path for nested screen 3


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class Bubble:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = BLUE
        self.speed = random.randint(5, 5)

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        # Draw filled circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw outlined circle to give the 3D effect
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)

# Define Button class
class Button:
    def __init__(self, text, image_path, position, size):
        self.text = text
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha() if image_path else None
        self.image = pygame.transform.scale(self.image, size) if self.image else None
        self.position = position
        self.size = size
        self.font = pygame.font.Font("Lacquer-Regular.ttf", 75)  # Change "Lacquer-Regular.ttf" to the path of your font file

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.position)
        else:
            transparent_surface = pygame.Surface(self.size, pygame.SRCALPHA)
            transparent_surface.fill((0, 0, 0, 0))  # Fill with transparent color
            screen.blit(transparent_surface, self.position)
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2))
            screen.blit(text_surface, text_rect)
# Create buttons for first screen
next_button_screen1 = Button(" ", 'start_btn.png', (screen_width - 750, screen_height - 600), (300, 150))
exit_button_screen1 = Button(" ", 'exit_btn.png', (screen_width - 350, screen_height - 600), (300, 150))

# Create buttons for second screen
next_button1_screen2 = Button("DSA", None, (screen_width - 1250, screen_height - 600), (300, 150))

next_button2_screen2 = Button("DBMS", None, (screen_width  - 800, screen_height - 600), (300, 150))
next_button3_screen2 = Button("COA", None, (screen_width  - 350, screen_height - 600), (300, 150))
back_button_screen2 = Button(" ", 'back1.png', (1220, screen_height - 700), (90, 50))
back_button_nested_screen1 = Button(" ", 'back1.png', (1280, screen_height - 700), (90, 50))
back_button_nested_screen2 = Button(" ", 'back1.png', (1280, screen_height - 700), (90, 50))
back_button_nested_screen3 = Button(" ", 'back1.png', (1280, screen_height - 700), (90, 50))


# Load sound files for each nested screen
sound_nested_screen1 = pygame.mixer.Sound('coa.mp3')  # Change 'sound_nested_screen1.wav' to the path of your sound file for nested screen 1
sound_nested_screen2 = pygame.mixer.Sound('dms.mp3')  # Change 'sound_nested_screen2.wav' to the path of your sound file for nested screen 2
sound_nested_screen3 = pygame.mixer.Sound('Dsa.mp3')  # Change 'sound_nested_screen3.wav' to the path of your sound file for nested screen 3
sound_screen1 = pygame.mixer.Sound('B.mp3')  # Change 'sound_screen1.wav' to the path of your sound file for screen 1
sound_screen2 = pygame.mixer.Sound('B.mp3')  # Change 'sound_screen2.wav' to the path of your sound file for screen 2
click_sound = pygame.mixer.Sound('A.mp3')  # Change 'click_sound.wav' to the path of your click sound file


# Define screen constants for nested screens
NESTED_SCREEN_1 = 1
NESTED_SCREEN_2 = 2
NESTED_SCREEN_3 = 3

class ResetButton(Button):
    def __init__(self, text, image_path, position, size):
        super().__init__(text, image_path, position, size)

    def handle_click(self, mmouse_pos):
        if self.position[0] < mmouse_pos[0] < self.position[0] + self.size[0] and \
                self.position[1] < mmouse_pos[1] < self.position[1] + self.size[1]:
            reset_game() # Call the reset_game function when the reset button is clicked

class RResetButton(Button):
    def __init__(self, text, image_path, position, size):
        super().__init__(text, image_path, position, size)

    def handle_click(self, mmmouse_pos):
        if self.position[0] < mmmouse_pos[0] < self.position[0] + self.size[0] and \
                self.position[1] < mmmouse_pos[1] < self.position[1] + self.size[1]:
            rreset_game() # Call the reset_game function when the reset button is clicked

class RRResetButton(Button):
    def __init__(self, text, image_path, position, size):
        super().__init__(text, image_path, position, size)

    def handle_click(self, mmmmouse_pos):
        if self.position[0] < mmmmouse_pos[0] < self.position[0] + self.size[0] and \
                self.position[1] < mmmmouse_pos[1] < self.position[1] + self.size[1]:
            rrreset_game() # Call the reset_game function when the reset button is clicked

def reset_game():
    global hangman_status, guessed, word, letters, score, word_index
    # Reset all game-related variables to their initial state
    hangman_status = 0
    guessed = []
    word_index = 0
    score = 0
    word = words[word_index]
    letters = [[x, y, ltr, True] for x, y, ltr, visible in letters]

def rreset_game():
    global hhangman_status, gguessed, wword, lletters, sscore, wword_index
    # Reset all game-related variables to their initial state
    hhangman_status = 0
    gguessed = []
    wword_index = 0
    sscore = 0
    wword = wwords[wword_index]
    lletters = [[xx, yy, lltr, True] for xx, yy, lltr, vvisible in lletters]

def rrreset_game():
    global hhhangman_status, ggguessed, wwword, llletters, ssscore, wwword_index
    # Reset all game-related variables to their initial state
    hhhangman_status = 0
    ggguessed = []
    wwword_index = 0
    ssscore = 0
    wwword = wwwords[wwword_index]
    llletters = [[xxx, yyy, llltr, True] for xxx, yyy, llltr, vvvisible in llletters]

reset_button = ResetButton("Reset", 'reset.png', (screen_width - 150, 25), (50, 30))
rreset_button = RResetButton("Reset", 'reset.png', (screen_width - 150, 25), (50, 30))
rrreset_button = RRResetButton("Reset", 'reset.png', (screen_width - 150, 25), (50, 30))

def play_sound_nested_screen(screen_type):
    if screen_type == NESTED_SCREEN_1:
        sound_nested_screen1.play()
    elif screen_type == NESTED_SCREEN_2:
        sound_nested_screen2.play()
    elif screen_type == NESTED_SCREEN_3:
        sound_nested_screen3.play()


# Function to handle button clicks for first screen
def handle_button_click_screen1(mouse_pos):
    if next_button_screen1.position[0] < mouse_pos[0] < next_button_screen1.position[0] + next_button_screen1.size[0] and \
            next_button_screen1.position[1] < mouse_pos[1] < next_button_screen1.position[1] + next_button_screen1.size[1]:
        click_sound.play()
        return 1
    elif exit_button_screen1.position[0] < mouse_pos[0] < exit_button_screen1.position[0] + exit_button_screen1.size[0] and \
            exit_button_screen1.position[1] < mouse_pos[1] < exit_button_screen1.position[1] + exit_button_screen1.size[1]:
        click_sound.play()
        pygame.quit()
        sys.exit()
    return 0



def display_total_score(total_score):
    global screen_width, screen_height, screen, font, BLACK, bubbles
    screen.fill((255, 255, 255))  # Fill the screen with white colo    # Draw
    total_score_text = f"Total Score: {total_score}"  # Total score message
    total_score_surface = font.render(total_score_text, 1, BLACK)  # Render the total score text
    total_score_rect = total_score_surface.get_rect(center=(screen_width/2, screen_height/2))  # Get the rectangle of the total score text
    screen.blit(total_score_surface, total_score_rect)  # Blit the total score text onto the screen
    pygame.display.update()  # Update the display

    pygame.display.flip()
     
def ddisplay_total_score(ttotal_score):
    global screen_width, screen_height, screen, font, BLACK, bubbles
    screen.fill((255, 255, 255))  # Fill the screen with white colo    # Draw
    total_score_text = f"Total Score: {ttotal_score}"  # Total score message
    total_score_surface = font.render(total_score_text, 1, BLACK)  # Render the total score text
    total_score_rect = total_score_surface.get_rect(center=(screen_width/2, screen_height/2))  # Get the rectangle of the total score text
    screen.blit(total_score_surface, total_score_rect)  # Blit the total score text onto the screen
    pygame.display.update()  # Update the display

    pygame.display.flip()

def dddisplay_total_score(tttotal_score):
    global screen_width, screen_height, screen, font, BLACK, bubbles
    screen.fill((255, 255, 255))  # Fill the screen with white colo    # Draw
    total_score_text = f"Total Score: {tttotal_score}"  # Total score message
    total_score_surface = font.render(total_score_text, 1, BLACK)  # Render the total score text
    total_score_rect = total_score_surface.get_rect(center=(screen_width/2, screen_height/2))  # Get the rectangle of the total score text
    screen.blit(total_score_surface, total_score_rect)  # Blit the total score text onto the screen
    pygame.display.update()  # Update the display

    pygame.display.flip()

# Function to handle button clicks for second screen
def handle_button_click_screen2(mouse_pos):
    if next_button1_screen2.position[0] < mouse_pos[0] < next_button1_screen2.position[0] + next_button1_screen2.size[0] and \
            next_button1_screen2.position[1] < mouse_pos[1] < next_button1_screen2.position[1] + next_button1_screen2.size[1]:
        click_sound.play()
        return NESTED_SCREEN_1
    elif next_button2_screen2.position[0] < mouse_pos[0] < next_button2_screen2.position[0] + next_button2_screen2.size[0] and \
            next_button2_screen2.position[1] < mouse_pos[1] < next_button2_screen2.position[1] + next_button2_screen2.size[1]:
        click_sound.play()
        return NESTED_SCREEN_2
    elif next_button3_screen2.position[0] < mouse_pos[0] < next_button3_screen2.position[0] + next_button3_screen2.size[0] and \
            next_button3_screen2.position[1] < mouse_pos[1] < next_button3_screen2.position[1]+next_button3_screen2.size[1]:
        click_sound.play()
        return NESTED_SCREEN_3
    elif back_button_screen2.position[0] < mouse_pos[0] < back_button_screen2.position[0] + back_button_screen2.size[0] and \
            back_button_screen2.position[1] < mouse_pos[1] < back_button_screen2.position[1] + back_button_screen2.size[1]:
        click_sound.play()
        return -1  # Negative value to represent back button
    return 0
def handle_button_click_nested_screen(screen_type, mouse_pos):
    if screen_type is None:
        return 0
    elif screen_type == NESTED_SCREEN_1:
         
        if back_button_nested_screen1.position[0] < mouse_pos[0] < back_button_nested_screen1.position[0] + back_button_nested_screen1.size[0] and \
                back_button_nested_screen1.position[1] < mouse_pos[1] < back_button_nested_screen1.position[1] + back_button_nested_screen1.size[1]:
            display_total_score(score)  # Display total score on a new screen after the game loop ends
            pygame.time.delay(3000)
            return -1  # Indicates back button is clicked
    elif screen_type == NESTED_SCREEN_2:
        if back_button_nested_screen2.position[0] < mouse_pos[0] < back_button_nested_screen2.position[0] + back_button_nested_screen2.size[0] and \
                back_button_nested_screen2.position[1] < mouse_pos[1] < back_button_nested_screen2.position[1] + back_button_nested_screen2.size[1]:
            display_total_score(ssscore)  # Display total score on a new screen after the game loop ends
            pygame.time.delay(3000)
            return -1  # Indicates back button is clicked
    elif screen_type == NESTED_SCREEN_3:
        if back_button_nested_screen3.position[0] < mouse_pos[0] < back_button_nested_screen3.position[0] + back_button_nested_screen3.size[0] and \
                back_button_nested_screen3.position[1] < mouse_pos[1] < back_button_nested_screen3.position[1] + back_button_nested_screen3.size[1]:
            display_total_score(sscore)  # Display total score on a new screen after the game loop ends
            pygame.time.delay(3000)
            return -1  # Indicates back button is clicked
    return 0

def bubble():
    if random.randint(1, 100) < 5:  # Adjust the frequency of bubbles
            bubble = Bubble(random.randint(0, screen_width), screen_height, random.randint(10, 30))
            bubbles.append(bubble)
        # Update bubbles
    for bubble in bubbles:
        bubble.move()
    for bubble in bubbles: 
        bubble.draw(screen)
    pygame.display.update()

def ddraw():
    display_score()
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    screen.blit(text, (500, 300))
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    screen.blit(images[hangman_status], (100, 300))
    display_question_and_word(word)
    back_button_nested_screen1.draw(screen)
    reset_button.draw(screen)
    bubble()
    pygame.display.update()

def dddraw():
    ddisplay_score()
    ddisplay_word = ""
    for lletter in wword:
        if lletter in gguessed:
            ddisplay_word += lletter + " "
        else:
            ddisplay_word += "_ "
    ttext = WORD_FONT.render(ddisplay_word, 1, BLACK)
    screen.blit(ttext, (500, 300))
    for lletter in lletters:
        xx, yy, lltr, vvisible = lletter
        if vvisible:
            pygame.draw.circle(screen, BLACK, (xx, yy), RADIUS, 3)
            ttext = LETTER_FONT.render(lltr, 1, BLACK)
            screen.blit(ttext, (xx - ttext.get_width() / 2, yy - ttext.get_height() / 2))
    screen.blit(iimages[hhangman_status], (100, 300))
    ddisplay_question_and_word(wword)
    back_button_nested_screen3.draw(screen)
    rreset_button.draw(screen)
    bubble()
    pygame.display.update()

def ddddraw():
    dddisplay_score()
    dddisplay_word = ""
    for llletter in wwword:
        if llletter in ggguessed:
            dddisplay_word += llletter + " "
        else:
            dddisplay_word += "_ "
    tttext = WORD_FONT.render(dddisplay_word, 1, BLACK)
    screen.blit(tttext, (500, 300))
    for llletter in llletters:
        xxx, yyy, llltr, vvvisible = llletter
        if vvvisible:
            pygame.draw.circle(screen, BLACK, (xxx, yyy), RADIUS, 3)
            tttext = LETTER_FONT.render(llltr, 1, BLACK)
            screen.blit(tttext, (xxx - tttext.get_width() / 2, yyy - tttext.get_height() / 2))
    screen.blit(iiimages[hhhangman_status], (100, 300))
    dddisplay_question_and_word(wwword)
    back_button_nested_screen2.draw(screen)
    rrreset_button.draw(screen)
    bubble()
    pygame.display.update()

def display_message(message, show_word=False):
    global screen, word, word_font, BLACK, screen_width, screen_height
    screen.fill((0, 255, 255))
    text = word_font.render(message, 1, BLACK)
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(text, text_rect)
    if show_word:
        word_text = word_font.render(f"Correct word was : {word}", 1, BLACK)
        word_rect = word_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(word_text, word_rect)
    pygame.display.update()

def ddisplay_message(message, show_word=False):
    global screen, wword, word_font, BLACK, screen_width, screen_height
    screen.fill((0, 255, 255))
    text = word_font.render(message, 1, BLACK)
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(text, text_rect)
    if show_word:
        word_text = word_font.render(f"Correct word was : {wword}", 1, BLACK)
        word_rect = word_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(word_text, word_rect)
    pygame.display.update()

def dddisplay_message(message, show_word=False):
    global screen, wwword, word_font, BLACK, screen_width, screen_height
    screen.fill((0, 255, 255))
    text = word_font.render(message, 1, BLACK)
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(text, text_rect)
    if show_word:
        word_text = word_font.render(f"Correct word was : {wwword}", 1, BLACK)
        word_rect = word_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(word_text, word_rect)
    pygame.display.update()

def display_score():
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, 1,BLACK)
    screen.blit(score_surface, (50, 10))

def ddisplay_score():
    score_text = f"Score: {sscore}"
    score_surface = font.render(score_text, 1,BLACK)
    screen.blit(score_surface, (50, 10))

def dddisplay_score():
    score_text = f"Score: {ssscore}"
    score_surface = font.render(score_text, 1,BLACK)
    screen.blit(score_surface, (50, 10))

def display_question_and_word(word):
    question = dsa.word_questions.get(word, "No question available")
    font_size = min(30, int(1000 / len(question)))  # Adjust divisor as needed
    font_size = max(font_size, 40)  # Set a minimum font size
    question_font = pygame.font.SysFont('comicsans', font_size)
    
    words = question.split()
    lines = []
    current_line = ""
    for word in words:
        if question_font.size(current_line + " " + word)[0] < screen_width - 100:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    
    lines.append(current_line.strip())
    
    dsa_text_height = title_font.size("DSA")[1]
    question_y = 10 + dsa_text_height + 20  # Adjust spacing as needed
    
    for i, line in enumerate(lines):
        question_surface = question_font.render(line, 1, BLACK)
        question_x = (screen_width - question_surface.get_width()) / 2
        screen.blit(question_surface, (question_x, question_y + i * (font_size + 5)))

def ddisplay_question_and_word(wword):
    qquestion = coa.word_questions.get(wword, "No question available")
    font_size = min(30, int(1000 / len(qquestion)))  # Adjust divisor as needed
    font_size = max(font_size, 40)  # Set a minimum font size
    question_font = pygame.font.SysFont('comicsans', font_size)
    
    wwords = qquestion.split()
    llines = []
    current_line = ""
    for wword in wwords:
        if question_font.size(current_line + " " + wword)[0] < screen_width - 100:
            current_line += " " + wword
        else:
            llines.append(current_line.strip())
            current_line = wword
    
    llines.append(current_line.strip())
    
    dsa_text_height = title_font.size("COA")[1]
    question_y = 10 + dsa_text_height + 20  # Adjust spacing as needed
    
    for j, line in enumerate(llines):
        question_surface = question_font.render(line, 1, BLACK)
        question_x = (screen_width - question_surface.get_width()) / 2
        screen.blit(question_surface, (question_x, question_y + j * (font_size + 5)))

def dddisplay_question_and_word(wwword):
    qqquestion = dms.word_questions.get(wwword, "No question available")
    font_size = min(30, int(1000 / len(qqquestion)))  # Adjust divisor as needed
    font_size = max(font_size, 40)  # Set a minimum font size
    question_font = pygame.font.SysFont('comicsans', font_size)
    
    wwwords = qqquestion.split()
    lllines = []
    current_line = ""
    for wwword in wwwords:
        if question_font.size(current_line + " " + wwword)[0] < screen_width - 100:
            current_line += " " + wwword
        else:
            lllines.append(current_line.strip())
            current_line = wwword
    
    lllines.append(current_line.strip())
    
    dsa_text_height = title_font.size("DMS")[1]
    question_y = 10 + dsa_text_height + 20  # Adjust spacing as needed
    
    for k, line in enumerate(lllines):
        question_surface = question_font.render(line, 1, BLACK)
        question_x = (screen_width - question_surface.get_width()) / 2
        screen.blit(question_surface, (question_x, question_y + k * (font_size + 5)))


def save_game_state():
    game_state = {
        "word_index": word_index,
        "guessed": guessed,
        "score": score,
        "hangman_status": hangman_status,
        "wword_index": wword_index,
        "gguessed": gguessed,
        "sscore": sscore,
        "hhangman_status": hhangman_status,
        "wwword_index": wwword_index,
        "ggguessed": ggguessed,
        "ssscore": ssscore,
        "hhhangman_status": hhhangman_status
        # Add more data to save as needed
    }
    with open("game_state.json", "w") as file:
        json.dump(game_state, file)

# Function to load game state from a file
def load_game_state():
    try:
        # Get a list of all files in the directory
        files = os.listdir()
        # Filter out files that are not JSON files
        json_files = [file for file in files if file.endswith(".json")]
        # Sort JSON files by modification time in descending order
        sorted_files = sorted(json_files, key=lambda x: os.path.getmtime(x), reverse=True)
        # Load data from the most recent JSON file
        if sorted_files:
            with open(sorted_files[0], "r") as file:
                game_state = json.load(file)
            return game_state
        else:
            return None
    except FileNotFoundError:
        return None

# Check if there is a saved game state
saved_game_state = load_game_state()
if saved_game_state:
    # Load data from saved game state
    word_index = saved_game_state.get("word_index", 0)
    guessed = saved_game_state.get("guessed", [])
    score = saved_game_state.get("score", 0)
    hangman_status = saved_game_state.get("hangman_status", 0)
    word = words[word_index]
    wword_index = saved_game_state.get("wword_index", 0)
    gguessed = saved_game_state.get("gguessed", [])
    sscore = saved_game_state.get("sscore", 0)
    hhangman_status = saved_game_state.get("hhangman_status", 0)
    wword = wwords[wword_index]
    wwword_index = saved_game_state.get("wwword_index", 0)
    ggguessed = saved_game_state.get("ggguessed", [])
    ssscore = saved_game_state.get("ssscore", 0)
    hhhangman_status = saved_game_state.get("hhhangman_status", 0)
    wwword = wwwords[wwword_index]
    # Add more variables to load as needed

# Main loop
current_screen = 1  # Start with the first screen
current_nested_screen = None  # No nested screen initially
sound_channel_screen1 = None  # Sound channel for screen 1
sound_channel_screen2 = None  # Sound channel for screen 2
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_state()
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update screen dimensions if window is resized
            screen_width, screen_height = event.dict['size']
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if current_screen == 1:
                result = handle_button_click_screen1(mouse_pos)
                if result == 1:
                    current_screen = 2
                    if sound_channel_screen2 is not None:
                        sound_channel_screen2.stop()  # Stop sound playback for screen 2
                    sound_channel_screen1 = sound_screen1.play()  # Play sound for screen 1
            elif current_screen == 2:
                if current_nested_screen is None:
                    result = handle_button_click_screen2(mouse_pos)
                    if result == NESTED_SCREEN_1:
                        current_nested_screen = NESTED_SCREEN_1
                        if sound_channel_screen1 is not None:
                            sound_channel_screen1.stop()  # Stop sound playback for screen 1
                        sound_channel_screen2 = sound_nested_screen1.play()  # Play sound for nested screen 1
                    elif result == NESTED_SCREEN_2:
                        current_nested_screen = NESTED_SCREEN_2
                        if sound_channel_screen1 is not None:
                            sound_channel_screen1.stop()  # Stop sound playback for screen 1
                        sound_channel_screen2 = sound_nested_screen2.play()  # Play sound for nested screen 2
                    elif result == NESTED_SCREEN_3:
                        current_nested_screen = NESTED_SCREEN_3
                        if sound_channel_screen1 is not None:
                            sound_channel_screen1.stop()  # Stop sound playback for screen 1
                        sound_channel_screen2 = sound_nested_screen3.play()  # Play sound for nested screen 3
                    elif result == -1:
                        current_screen = 1  # Go back to the first screen
                        if sound_channel_screen1 is not None:
                            sound_channel_screen1.stop()  # Stop sound playback for screen 1
                else:
                    result = handle_button_click_nested_screen(current_nested_screen, mouse_pos)
                    if result == -1:
                        current_nested_screen = None  # Close the nested screen
                        if sound_channel_screen2 is not None:
                            sound_channel_screen2.stop()  # Stop sound playback for screen 2
                        sound_channel_screen1 = sound_screen2.play()  # Play sound for screen 2
                  
                        
    # Draw current screen
    if current_screen == 1:
        screen.blit(pygame.transform.scale(background_image_1, (screen_width, screen_height)), (0, 0))
        next_button_screen1.draw(screen)
        exit_button_screen1.draw(screen)
    elif current_screen == 2:
        screen.blit(pygame.transform.scale(background_image_2, (screen_width, screen_height)), (0, 0))
        next_button1_screen2.draw(screen)
        next_button2_screen2.draw(screen)
        next_button3_screen2.draw(screen)
        back_button_screen2.draw(screen)

        if current_nested_screen is not None:
            # Draw nested screen based on current_nested_screen value
            if current_nested_screen == NESTED_SCREEN_1:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        m_x, m_y = pygame.mouse.get_pos()
                        mmouse_pos = pygame.mouse.get_pos()
                        reset_button.handle_click(mmouse_pos)
                        for letter in letters:
                            x, y, ltr, visible = letter
                            if visible:
                                dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                                if dis < RADIUS:
                                    letter[3] = False
                                    guessed.append(ltr)
                                    if ltr in letter_sounds:  
                                        letter_sounds[ltr].play()  
                                    if ltr not in word:
                                        hangman_status += 1
                screen.blit(pygame.transform.scale(nested_screen1_image, (screen_width, screen_height)), (0, 0))                                                        
                ddraw()
                pygame.display.update()

                won = True
                for letter in word:
                    if letter not in guessed:
                        won = False
                        break
                if won:
                    words_guessed += 1  # Increment the counter
                    score += 1
                    guessed = []
                    word_index = (word_index + 1) % len(words)
                    word = words[word_index]
                    hangman_status = 0
                    letters = [[x, y, ltr, True] for x, y, ltr, visible in letters]
                    display_message("You Won")
                    win_sound.play()
                    pygame.time.delay(3000)

                if hangman_status == 6:
                    guessed = []
                    hangman_status = 0
                    letters = [[x, y, ltr, True] for x, y, ltr, visible in letters]
                    display_message(f"You Lost", show_word=True)
                    sad_sound.play()
                    pygame.time.delay(3000)
                    word_index = (word_index + 1) % len(words)
                    word = words[word_index] 

                if score == -1:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            m_x, m_y = pygame.mouse.get_pos()
                            if screen_width/2 - 100 < m_x < screen_width/2 + 100 and screen_height/2 + 100 - 50 < m_y < screen_height/2 + 100 + 50:
                                score = 0
                                hangman_status = 0
                                guessed = []
                                word_index = 0
                                word = words[word_index]
                                letters = [[x, y, ltr, True] for x, y, ltr, visible in letters]
                clock.tick(60)

            elif current_nested_screen == NESTED_SCREEN_2:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mmm_x, mmm_y = pygame.mouse.get_pos()
                        mmmmouse_pos = pygame.mouse.get_pos()
                        rrreset_button.handle_click(mmmmouse_pos)
                        for llletter in llletters:
                            xxx, yyy, llltr, vvvisible = llletter
                            if vvvisible:
                                dddis = math.sqrt((xxx - mmm_x) ** 2 + (yyy - mmm_y) ** 2)
                                if dddis < RADIUS:
                                    llletter[3] = False
                                    ggguessed.append(llltr)
                                    if llltr in letter_sounds:  
                                        letter_sounds[llltr].play()  
                                    if llltr not in wwword:
                                        hhhangman_status += 1
                screen.blit(pygame.transform.scale(nested_screen3_image, (screen_width, screen_height)), (0, 0))
                ddddraw()
                pygame.display.update()

                won = True
                for llletter in wwword:
                    if llletter not in ggguessed:
                        won = False
                        break
                if won:
                    wwwords_guessed += 1  # Increment the counter
                    ssscore += 1
                    ggguessed = []
                    wwword_index = (wwword_index + 1) % len(wwwords)
                    wwword = wwwords[wwword_index]
                    hhhangman_status = 0
                    llletters = [[xxx, yyy, llltr, True] for xxx, yyy, llltr, vvvisible in llletters]
                    ddisplay_message("You Won")
                    win_sound.play()
                    pygame.time.delay(3000)

                if hhhangman_status == 6:
                    ggguessed = []
                    hhhangman_status = 0
                    llletters = [[xxx, yyy, llltr, True] for xxx, yyy, llltr, vvvisible in llletters]
                    dddisplay_message(f"You Lost", show_word=True)
                    sad_sound.play()
                    pygame.time.delay(3000)
                    wwword_index = (wwword_index + 1) % len(wwwords)
                    wwword = wwwords[wwword_index] 

                if ssscore == -1:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mmm_x, mmm_y = pygame.mouse.get_pos()
                            if screen_width/2 - 100 < m_x < screen_width/2 + 100 and screen_height/2 + 100 - 50 < m_y < screen_height/2 + 100 + 50:
                                ssscore = 0
                                hhhangman_status = 0
                                ggguessed = []
                                wwword_index = 0
                                wwword = wwwords[wwword_index]
                                llletters = [[xxx, yyy, llltr, True] for xxx, yyy, llltr, vvvisible in llletters]
                clock.tick(60)
            elif current_nested_screen == NESTED_SCREEN_3:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mm_x, mm_y = pygame.mouse.get_pos()
                        mmmouse_pos = pygame.mouse.get_pos()
                        rreset_button.handle_click(mmmouse_pos)
                        for lletter in lletters:
                            xx, yy, lltr, vvisible = lletter
                            if vvisible:
                                ddis = math.sqrt((xx - mm_x) ** 2 + (yy - mm_y) ** 2)
                                if ddis < RADIUS:
                                    lletter[3] = False
                                    gguessed.append(lltr)
                                    if lltr in letter_sounds:  
                                        letter_sounds[lltr].play()  
                                    if lltr not in wword:
                                        hhangman_status += 1
                screen.blit(pygame.transform.scale(nested_screen3_image, (screen_width, screen_height)), (0, 0))
                dddraw()
                pygame.display.update()

                won = True
                for lletter in wword:
                    if lletter not in gguessed:
                        won = False
                        break
                if won:
                    wwords_guessed += 1  # Increment the counter
                    sscore += 1
                    gguessed = []
                    wword_index = (wword_index + 1) % len(wwords)
                    wword = wwords[wword_index]
                    hhangman_status = 0
                    lletters = [[xx, yy, lltr, True] for xx, yy, lltr, vvisible in lletters]
                    display_message("You Won")
                    win_sound.play()
                    pygame.time.delay(3000)

                if hhangman_status == 6:
                    gguessed = []
                    hhangman_status = 0
                    lletters = [[xx, yy, lltr, True] for xx, yy, lltr, vvisible in lletters]
                    ddisplay_message(f"You Lost", show_word=True)
                    sad_sound.play()
                    pygame.time.delay(3000)
                    wword_index = (wword_index + 1) % len(wwords)
                    wword = wwords[wword_index] 

                if sscore == -1:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mm_x, mm_y = pygame.mouse.get_pos()
                            if screen_width/2 - 100 < m_x < screen_width/2 + 100 and screen_height/2 + 100 - 50 < m_y < screen_height/2 + 100 + 50:
                                sscore = 0
                                hhangman_status = 0
                                gguessed = []
                                wword_index = 0
                                wword = wwords[wword_index]
                                lletters = [[xx, yy, lltr, True] for xx, yy, lltr, vvisible in lletters]
                clock.tick(60)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()