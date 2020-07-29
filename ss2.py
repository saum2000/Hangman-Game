import pygame
import math
import random
from words import word_list

pygame.init()

screen = pygame.display.set_mode((725, 575))
pygame.display.set_caption("hangman")

# buttons
rad = 20
gap = 15
letters = []
startx = round((725 - (rad * 2 + gap) * 13) / 2)
starty = 450
A = 65
for i in range(26):
    x = startx + gap * 2 + ((rad * 2 + gap) * (i % 13))
    y = starty + ((i // 13) * (gap + rad * 2))
    letters.append([x, y, chr(A + i), True])

#fonts
FONT = pygame.font.SysFont("comicsans", 35)
WORD_FONT = pygame.font.SysFont("comicsans", 45)

#images
bg = pygame.image.load("bg.jpg")
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
tries = 0
word = random.choice(word_list).upper()
guessed = []

FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    screen.blit(bg, (0, 0))

    # draw title
    text = WORD_FONT.render("HANGMAN", 1, (0,0,255))
    screen.blit(text,(300, 60))

    # draw letter
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, (0, 0, 0))
    screen.blit(text, (350, 200))

    # draw button
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, (0, 0, 0), (x, y), rad, 3)
            text = FONT.render(ltr, 1, (0, 0, 0))
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    screen.blit(images[tries], (130, 200))
    pygame.display.update()


def display_msg(message):
    pygame.time.delay(1000)
    screen.blit(bg,(0, 0))
    text = FONT.render(message, 1, (0, 0, 0))
    screen.blit(text, (70, 100))
    pygame.display.update()
    pygame.time.delay(3000)


while run:
    clock.tick(FPS)
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x - mx) ** 2 + (y - my) ** 2)
                    if dist < rad:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            tries += 1
    draw()
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    if won:
        display_msg("Congratulations, you won! Time to celebrate")
        break
    if tries == 6:
        display_msg("Sorry, you lost the game.The word was " + word)
        break

pygame.quit()
