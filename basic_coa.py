import pygame
import math
import coa
import sys
import time
pygame.init()
WIDTH, HEIGHT = 1365,710 
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Make the screen resizable
pygame.display.set_caption("Hangman !")

background_image = pygame.image.load("gg.jpg")  # Replace "background_image.jpg" with the path to your image
background_image_original = background_image.copy()  # Store a copy of the original image
background_rect = background_image.get_rect()
win_sound = pygame.mixer.Sound("win.mp3")  # Adjust the file name as per your sound file
sad_sound = pygame.mixer.Sound("sadhorn.mp3")  # Adjust the file name as per your sound file

def resize_background_image():
    new_width = screen.get_width()
    new_height = screen.get_height()
    return pygame.transform.scale(background_image, (new_width, new_height))

background_image = resize_background_image()  # Initial resize
background_rect = background_image.get_rect()

RADIUS = 30
GAP = 15
letters = []
letter_sounds = {}


startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 550
A = 65
for i in range(26):
    x = startx + GAP * 13 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])
    letter = chr(65 + i)
    sound_file = "A.mp3"  # Adjust the file name format as per your sound files
    letter_sounds[letter] = pygame.mixer.Sound(sound_file)


guessed = []
hangman_status = 0

word_index = 0

words = coa.wor
word = words[word_index]

font = pygame.font.SysFont("arialblack", 60)
letter_font = pygame.font.SysFont('comicsans', 40)
word_font = pygame.font.SysFont('comicsans', 60)
title_font = pygame.font.SysFont('comicsans', 70)

LETTER_FONT = pygame.font.SysFont('arial', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 70)
TEXT_COL = (255, 255, 255)

images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 30
clock = pygame.time.Clock()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def ddraw():
    screen.blit(background_image, background_rect)  # Draw the background image
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
    pygame.display.update()

def display_message(message, show_word=False):
    global screen, word, word_font, BLACK, WIDTH, HEIGHT
    screen.fill((0, 255, 255))
    text = word_font.render(message, 1, BLACK)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    if show_word:
        word_text = word_font.render(f"Correct word was : {word}", 1, BLACK)
        word_rect = word_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        screen.blit(word_text, word_rect)
    pygame.display.update()


def display_score():
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, 1,BLACK)
    screen.blit(score_surface, (50, 10))

def display_question_and_word(word):
    question = coa.word_questions.get(word, "No question available")
    font_size = min(30, int(1000 / len(question)))  # Adjust divisor as needed
    font_size = max(font_size, 40)  # Set a minimum font size
    question_font = pygame.font.SysFont('comicsans', font_size)
    
    words = question.split()
    lines = []
    current_line = ""
    for word in words:
        if question_font.size(current_line + " " + word)[0] < WIDTH - 100:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    
    lines.append(current_line.strip())
    
    dsa_text_height = title_font.size("DSA")[1]
    question_y = 10 + dsa_text_height + 20  # Adjust spacing as needed
    
    for i, line in enumerate(lines):
        question_surface = question_font.render(line, 1, BLACK)
        question_x = (WIDTH - question_surface.get_width()) / 2
        screen.blit(question_surface, (question_x, question_y + i * (font_size + 5)))

def display_total_score(total_score):
    global WIDTH, HEIGHT, screen, font, BLACK
    screen.fill((255, 255, 255))  # Fill the screen with white color
    total_score_text = f"Total Score: {total_score}"  # Total score message
    total_score_surface = font.render(total_score_text, 1, BLACK)  # Render the total score text
    total_score_rect = total_score_surface.get_rect(center=(WIDTH/2, HEIGHT/2))  # Get the rectangle of the total score text
    screen.blit(total_score_surface, total_score_rect)  # Blit the total score text onto the screen
    pygame.display.update()  # Update the display


def main():
    global hangman_status, guessed, word, letters, score, word_index, WIDTH, HEIGHT, screen, background_image, background_rect
    run = True
    hangman_status = 0
    score = 0
    words_guessed = 0  # Counter to track the number of words guessed correctly
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
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
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                background_image = resize_background_image()
                background_rect = background_image.get_rect()
                
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
                    if WIDTH/2 - 100 < m_x < WIDTH/2 + 100 and HEIGHT/2 + 100 - 50 < m_y < HEIGHT/2 + 100 + 50:
                       score = 0
                       hangman_status = 0
                       guessed = []
                       word_index = 0
                       word = words[word_index]
                       letters = [[x, y, ltr, True] for x, y, ltr, visible in letters]

        display_score()
        pygame.display.update()
        clock.tick(60)
        
        if words_guessed == 3:  # Check if three words have been guessed correctly
            run = False  # Set run to False to end the game

    display_total_score(score)  # Display total score on a new screen after the game loop ends
    pygame.time.delay(3000)  # Delay for 3 seconds before quitting
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main() 