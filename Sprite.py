# ============================================================
# Author: Jordan Harding
# Course: CST 269
# Date: 11-14
#
# Title: Brick Breaker Game
#
# References:
# - Base Brick Breaker logic inspired by classic "Breakout" arcade game.
# - Pygame official documentation: https://www.pygame.org/docs/
# - Splash screen structure adapted from Python 1 example code.
# - Image loading fallback method adapted from Pygame community examples.
# - Mouse-based paddle movement inspired by Sloan Kelly’s game tutorials.
# - Brick layout loading expanded from file-reading examples (Python docs).
# - Audio usage based on pygame.mixer official examples.
# ============================================================

import pygame, os, sys
from pygame.locals import *

# Game Title
title = "brick breaker"
print(title.title().center(80, "="))  # Title centered

# ========== Begin Pygame Game ==========
pygame.init()
fpsClock = pygame.time.Clock()
mainSurface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Bricks')

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Font for splash screen and score
font = pygame.font.SysFont(None, 36)
bigFont = pygame.font.SysFont(None, 64)

# Score
score = 0

# Splash screen flag
gameStarted = False
menuActive = True

# -----------------------------
# AUDIO LOADING
# -----------------------------
pygame.mixer.init()

def safe_sound(name):
    if os.path.exists(name):
        return pygame.mixer.Sound(name)
    else:
        return None

# sound effects
hitSound = safe_sound("hit.wav")
gameOverSound = safe_sound("gameover.wav")

# bgm should LOOP
if os.path.exists("bgm.mp3"):
    pygame.mixer.music.load("bgm.mp3")

# -----------------------------
# IMAGE LOADER
# -----------------------------
def safe_load_image(name, fallback_color, size):
    if os.path.exists(name):
        return pygame.image.load(name)
    else:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

# === Load images ===
background = safe_load_image('bbf.jpg', (0, 0, 0), (800, 600))
splash_bg = safe_load_image('splash.png', (20, 20, 40), (800, 600))
bat = safe_load_image('bat.png', (200, 200, 200), (100, 20))
ball = safe_load_image('ball.png', (255, 255, 255), (16, 16))
brick = safe_load_image('brick.png', (255, 0, 0), (30, 16))

# ============================================================
# MAP LOADING
# ============================================================
mapFiles = ["map1.txt", "map2.txt", "map_hard.txt"]
selectedMap = 0
bricks = []

def loadMap(fileName):
    global bricks
    bricks = []
    if not os.path.exists(fileName):
        print("Missing map:", fileName)
        return

    f = open(fileName, "r")
    rows = f.readlines()
    f.close()

    yOffset = 100
    xOffset = 245
    w = brick.get_width()
    h = brick.get_height()

    rowIndex = 0
    for line in rows:
        col = 0
        for char in line.strip():
            if char == "#":
                rect = Rect(xOffset + (col * (w+1)), yOffset + (rowIndex * (h+2)), w, h)
                bricks.append(rect)
            col += 1
        rowIndex += 1

# ============================================================
# GAME OBJECTS
# ============================================================
playerY = 540
batRect = bat.get_rect()
mousex, mousey = (0, playerY)
batRect.topleft = (mousex, playerY)

ballRect = ball.get_rect()
ballStartY = 200
ballSpeed = 3
ballServed = False
bx, by = (24, ballStartY)
sx, sy = (ballSpeed, ballSpeed)
ballRect.topleft = (bx, by)

# ============================================================
# ===================== MENU SCREEN ==========================
# ============================================================

def drawMenu():
    mainSurface.fill((0,0,0))
    titleText = bigFont.render("Select Map (UP/DOWN)", True, white)
    mainSurface.blit(titleText, (180, 200))

    for i, m in enumerate(mapFiles):
        color = (255,255,0) if i == selectedMap else (255,255,255)
        line = font.render(m, True, color)
        mainSurface.blit(line, (300, 280 + i*40))

    startText = font.render("Press ENTER to Start", True, white)
    mainSurface.blit(startText, (280, 450))
    pygame.display.update()

# ============================================================
# ===================== SPLASH SCREEN ========================
# ============================================================

while menuActive:
    drawMenu()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                selectedMap = (selectedMap - 1) % len(mapFiles)
            if event.key == K_DOWN:
                selectedMap = (selectedMap + 1) % len(mapFiles)
            if event.key == K_RETURN:
                loadMap(mapFiles[selectedMap])
                menuActive = False
                gameStarted = True
                score = 0
                pygame.mixer.music.play(-1)   # LOOP

# ============================================================
# ====================== GAME LOOP ===========================
# ============================================================
while True:
    # Draw background
    mainSurface.blit(pygame.transform.scale(background, (800, 600)), (0, 0))

    # Draw bricks
    for b in bricks:
        mainSu
