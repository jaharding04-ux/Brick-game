# ============================================================
# Author: Jordan Harding
# Course: CST 269
# Date: 11-14
# Title: Brick Breaker Game
#
# ----------------------------
# References:
# ----------------------------
#
# Sprite / Art Creation:
#   - Microsoft Paint / Paint App
#       Used to design simple graphics such as the paddle, ball,
#       and brick placeholders.
#
# ChatGPT:
#   - Used for generating background ideas and help writing code.
#
# Map Loading Logic Reference:
#   - W3Schools File Reading Tutorial
#       https://www.w3schools.com/python/python_file_handling.asp
#
# Sounds:
#   - Pixabay Free Sound Effects
#       https://pixabay.com/sound-effects/
#
# Splash Screen:
#   - Based on Python 1 splash screen example.
#
# Game Over Screen:
#   - Adapted from pygame example in Python 1.
#
# Pygame Documentation:
#   - https://www.pygame.org/docs/
#
# ============================================================


import pygame, os, sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

fpsClock = pygame.time.Clock()
mainSurface = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Brick Breaker")

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

font = pygame.font.SysFont(None, 36)
bigFont = pygame.font.SysFont(None, 64)

# ============================
# SAFE IMAGE & SOUND LOADERS
# ============================

def safe_load_image(name, fallback_color, size):
    if os.path.exists(name):
        return pygame.image.load(name)
    surf = pygame.Surface(size)
    surf.fill(fallback_color)
    return surf

def safe_sound(name):
    if os.path.exists(name):
        return pygame.mixer.Sound(name)
    return None

# ============================
# LOAD IMAGES & SOUNDS
# ============================

background = safe_load_image("bbf.png", (0,0,0), (800,600))
splash = safe_load_image("splash.png", (30,30,30), (800,600))

bat = safe_load_image("bat.png", (200,200,200), (100,20))
ball = safe_load_image("ball.png", (255,255,255), (16,16))
brick = safe_load_image("brick.png", (255,0,0), (30,16))

hitSound = safe_sound("hit.mp3")
gameOverSound = safe_sound("gameover.mp3")
levelPassSound = safe_sound("levelpass.mp3")

musicLoaded = False
if os.path.exists("bgm.mp3"):
    pygame.mixer.music.load("bgm.mp3")
    musicLoaded = True

# ============================
# GAME VARIABLES
# ============================

score = 0
finalScore = 0
lives = 3

splashActive = True
gameOverActive = False
levelPassedActive = False

mapFiles = ["Level_1.txt", "Level_2.txt", "level_3.txt"]
selectedMap = 0
bricks = []

playerY = 540
batRect = bat.get_rect()
batRect.topleft = (350, playerY)

ballRect = ball.get_rect()
ballStartY = 300
ballServed = False
lvlSpeed = [4, 5, 7]
ballSpeed = lvlSpeed[selectedMap]

bx, by = (400, ballStartY)
sx, sy = (ballSpeed, ballSpeed)
ballRect.topleft = (bx, by)

# ============================
# SPLASH SCREEN WITH RULES
# ============================

while splashActive:
    mainSurface.blit(pygame.transform.scale(splash, (800,600)), (0,0))

    title = bigFont.render("BRICK BREAKER", True, white)
    startText = font.render("Press any key to continue", True, white)

    rules1 = font.render("Rules:", True, white)
    rules2 = font.render("- Move the paddle with your mouse", True, white)
    rules3 = font.render("- Click to launch the ball", True, white)
    rules4 = font.render("- Break all the bricks to beat the level", True, white)
    rules5 = font.render("- Don’t let the ball fall below the paddle", True, white)

    mainSurface.blit(title, (250, 100))
    mainSurface.blit(rules1, (300, 200))
    mainSurface.blit(rules2, (200, 240))
    mainSurface.blit(rules3, (200, 280))
    mainSurface.blit(rules4, (200, 320))
    mainSurface.blit(rules5, (200, 360))
    mainSurface.blit(startText, (240, 460))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            splashActive = False

# ============================
# MAP LOADER
# ============================

def loadMap(fileName):
    global bricks, bx, by, sx, sy, ballServed, ballSpeed

    bricks = []

    if not os.path.exists(fileName):
        return

    with open(fileName, "r") as f:
        rows = [line.strip() for line in f.readlines() if line.strip()]

    w = brick.get_width()
    h = brick.get_height()

    totalWidth = len(rows[0]) * (w + 2)
    xOffset = (800 - totalWidth) // 2
    yOffset = 80

    for rowIndex, line in enumerate(rows):
        for col, char in enumerate(line):
            if char == "#":
                rect = Rect(
                    xOffset + col * (w + 2),
                    yOffset + rowIndex * (h + 4),
                    w, h
                )
                bricks.append(rect)

    ballSpeed = lvlSpeed[selectedMap]
    ballServed = False
    bx, by = (400, ballStartY)
    sx, sy = (ballSpeed, ballSpeed)
    ballRect.topleft = (bx, by)

# ============================
# MAIN MENU & MAP MENU
# ============================

menuOptions = ["Start Game", "Select Level", "Quit"]
menuIndex = 0

def drawMainMenu():
    mainSurface.fill((0, 0, 0))
    title = bigFont.render("MAIN MENU", True, white)
    mainSurface.blit(title, (280, 140))

    for i, opt in enumerate(menuOptions):
        color = (255, 255, 0) if i == menuIndex else white
        text = font.render(opt, True, color)
        mainSurface.blit(text, (330, 250 + i * 50))

    pygame.display.update()

def drawMapMenu():
    mainSurface.fill((0,0,0))
    titleText = bigFont.render("Select Level", True, white)
    mainSurface.blit(titleText, (300, 150))

    for i, m in enumerate(mapFiles):
        color = (255,255,0) if i == selectedMap else white
        line = font.render(m, True, color)
        mainSurface.blit(line, (340, 260 + i*40))

    backText = font.render("Press ESC to return", True, white)
    mainSurface.blit(backText, (280, 500))

    pygame.display.update()

inMainMenu = True
inMapMenu = False

# ============================
# MAIN MENU LOOP
# ============================

while inMainMenu:

    if inMapMenu:
        drawMapMenu()
    else:
        drawMainMenu()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_RETURN:

                if not inMapMenu:
                    if menuIndex == 0:  # Start Game
                        inMainMenu = False
                        loadMap(mapFiles[selectedMap])
                        if musicLoaded:
                            pygame.mixer.music.play(-1)

                    elif menuIndex == 1:  # Select map submenu
                        inMapMenu = True

                    elif menuIndex == 2:  # Quit
                        pygame.quit()
                        sys.exit()

                else:
                    inMapMenu = False

            if event.key == K_ESCAPE and inMapMenu:
                inMapMenu = False

            if event.key == K_UP:
                if inMapMenu:
                    selectedMap = (selectedMap - 1) % len(mapFiles)
                else:
                    menuIndex = (menuIndex - 1) % len(menuOptions)

            if event.key == K_DOWN:
                if inMapMenu:
                    selectedMap = (selectedMap + 1) % len(mapFiles)
                else:
                    menuIndex = (menuIndex + 1) % len(menuOptions)

# ============================
# GAME OVER SCREEN
# ============================

def gameOverScreen():
    global gameOverActive, inMainMenu, score
    mainSurface.fill((0,0,0))

    overText = bigFont.render("GAME OVER", True, (255, 0, 0))
    scoreText = font.render(f"Final Score: {finalScore}", True, white)
    restartText = font.render("Press ENTER to Restart", True, white)

    mainSurface.blit(overText, (270, 220))
    mainSurface.blit(scoreText, (310, 300))
    mainSurface.blit(restartText, (270, 350))
    pygame.display.update()

    while gameOverActive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    score = 0
                    gameOverActive = False
                    inMainMenu = True
                    # Return to main menu loop
                    break

# ============================
# LEVEL PASSED SCREEN
# ============================

def levelPassedScreen():
    global levelPassedActive

    mainSurface.fill((0,0,0))
    winText = bigFont.render("LEVEL PASSED!", True, (0, 255, 0))
    scoreText = font.render(f"Score: {score}", True, white)
    contText = font.render("Press ENTER for Next Level", True, white)

    mainSurface.blit(winText, (250, 220))
    mainSurface.blit(scoreText, (350, 300))
    mainSurface.blit(contText, (230, 360))
    pygame.display.update()

    while levelPassedActive:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    levelPassedActive = False

# ============================
# MAIN GAME LOOP
# ============================

while True:
    if gameOverActive:
        gameOverScreen()

    if levelPassedActive:
        levelPassedScreen()

    mainSurface.blit(pygame.transform.scale(background, (800,600)), (0,0))

    for b in bricks:
        mainSurface.blit(brick, b)

    mainSurface.blit(ball, ballRect)
    mainSurface.blit(bat, batRect)

    scoreText = font.render(f"Score: {score}", True, white)
    livesText = font.render(f"Lives: {lives}", True, white)
    levelText = font.render(f"Level: {selectedMap + 1}", True, white)

    mainSurface.blit(scoreText, (10,10))
    mainSurface.blit(livesText, (10, 40))
    mainSurface.blit(levelText, (10, 70))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEMOTION:
            mousex, _ = event.pos
            batRect.x = max(0, min(mousex, 800 - batRect.width))

        elif event.type == MOUSEBUTTONUP and not ballServed:
            ballServed = True

    if ballServed:
        bx += sx
        by += sy
        ballRect.topleft = (bx, by)

    # Wall bounce
    if by <= 0:
        sy = -sy

    if bx <= 0 or bx >= 800 - ballRect.width:
        sx = -sx

    # Paddle bounce
    if ballRect.colliderect(batRect) and sy > 0:
        by = batRect.top - ballRect.height
        sy = -sy
        if hitSound:
            hitSound.play()

    # Brick collision
    hitIndex = ballRect.collidelist(bricks)
    if hitIndex >= 0:
        del bricks[hitIndex]
        sy = -sy
        score += 10

    # Ball falls off screen
    if by >= 600:
        lives -= 1
        ballServed = False
        bx, by = (400, ballStartY)
        sx, sy = (ballSpeed, ballSpeed)
        ballRect.topleft = (bx, by)

        if lives <= 0:
            finalScore = score
            if gameOverSound:
                gameOverSound.play()
            gameOverActive = True
            lives = 3
            loadMap(mapFiles[selectedMap])

    # Level Passed
    if len(bricks) == 0 and not levelPassedActive:
        if levelPassSound:
            levelPassSound.play()

        if selectedMap < len(mapFiles) - 1:
            selectedMap += 1
        loadMap(mapFiles[selectedMap])
        levelPassedActive = True

    pygame.display.update()
    fpsClock.tick(60)
