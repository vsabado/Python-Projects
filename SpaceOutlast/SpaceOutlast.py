# Assignment 5
# August 5, 2017
# Vladimir Sabado

# Inspired by:
# https://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python

# Game Synopsis
##Objective of the game:
##Collect 10 fuel to win

##Fuel gives 25 hp back to player
##Every fuel gathered decreases movement speed by 1.5 (It gets really hard because of this)
##Missiles seek the player
##Fuel spawns at random locations
##Missile speed are randomized
##6 missile spawn
##Each missile does damage to the player
##About 15% of the entire project is borrowed codes (player movement, player healthbar, angled missile). The rest is original.
##Sprites and images are from google.
##Music is from google
##Difficulty modifiers: missile frequency, missile speed, movement speed reduction, missle dmg, healing from fuel increased/decreased


# Libraries used in this project

import math
import pygame
import random
import time
from pygame.locals import *

# Defining game speed in frames per second
clock = pygame.time.Clock()
clock.tick(60)

# Initilizing the game
pygame.init()  # This initializes pygame
pygame.display.set_caption("Space Outlast")  # Game Title
pygame.mixer.init()  # Music initilization
width, height = 1280, 720  # Code resolution
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)  # Defining screen using integers for width and height
keys = [False, False, False, False]  # Default key presses (not moving)
playerpos = [300, 300]  # Player starting position
projectiles = []  # Array that we'll use to store our projectiles
maxFuel = 10  # Not going to spawn over 10 fuel so this is our limit used for the for loop.
fuels = []  # Array that we'll use to store fuels
scoreCounter = 0  # This will iterate when the player picks up fuel
fuelPosition = [100, 100]  # Defining fuel position
currentFuel = 0  # Keeps count of how many fuel has spawned
movementSpeed = 20  # Defining default movement speed
playerHealth = 200  # Player starting health

# Creating graphics
player = pygame.image.load("resources/images/PlayerSprite4.png")  # Loads the skin for our sprite
space = pygame.image.load("resources/images/background2.png")  # Background image
space = pygame.transform.scale(space, (width, height))  # Manipulates background image
missiles = pygame.image.load("resources/images/missile.png")  # Loads the skin for our missiles
enemySprite = pygame.image.load("resources/images/EnemyShip.png")  # Used this to create enemy visual
fuelImg = pygame.image.load("resources/images/fuel.png")  # Loads the skin for our fuel
youWon = pygame.image.load("resources/images/wellplayed.png")  # Load the image for our victory screen
youLost = pygame.image.load("resources/images/youlost2.png")  # Load the image for our loss screen
healthbar = pygame.image.load("resources/images/healthbar.png")  # Load the image for the healthbar
health = pygame.image.load("resources/images/health.png")  # Load the image for health

# Enemy Parameters
enemy1 = [1000, 50]  # Location from where missile #1 is shot
enemy2 = [1000, 200]  # Location from where missile #2 is shot
enemy3 = [1000, 300]  # Location from where missile #3 is shot
enemy4 = [1000, 500]  # Location from where missile #4 is shot
enemy5 = [1000, 600]  # Location from where missile #5 is shot
enemy6 = [900, 650]  # Location from where missile #6 is shot
enemyTimer1 = 60  # Frames until next projectile
enemyTimer2 = 50  # Frames until next projectile
enemyTimer3 = 50  # Frames until next projectile
enemyTimer4 = 50  # Frames until next projectile
enemyTimer5 = 35  # Frames until next projectile
enemyTimer6 = 50  # Frames until next projectile

# Fuel Parameter
fuelTimer = 400  # Frames until first fuel spawn

# Game audio
pygame.mixer.music.load('resources/audio/battle.ogg')  # Load audio
pygame.mixer.music.play(-1, 0.0)  # Play audio
pygame.mixer.music.set_volume(0.25)  # Audio volume

# Game loop
running = 1

while running:
    # This will clear the screen
    screen.fill(0)
    # This block of code will obtain the width and height. It will also draw the background and sprites.
    for x in range(width // space.get_width()):
        for y in range(height // space.get_height()):
            screen.blit(space, (x * 1, y * 1))
            screen.blit(enemySprite, (800, 25))
            screen.blit(player, playerpos)

    # This block of code creates a boundary so that player position cannot exceed width and height.
    if playerpos[0] > width - player.get_width() - 300:
        playerpos[0] = width - player.get_width() - 300
    if playerpos[0] < 0:
        playerpos[0] = 0
    if playerpos[1] > height - player.get_height():
        playerpos[1] = height - player.get_height()
    if playerpos[1] < 0:
        playerpos[1] = 0

    # These blocks of codes dictate player movement and speed.
    # These blocks of codes were borrowed.
    for event in pygame.event.get():
        # Key presses are boolean, true is pressed and false if not
        if event.type == KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False

        if event.type == QUIT:
            # This block of code allows the coder to quit (CAN'T EVEN EXIT OUT WITHOUT THIS!!)
            pygame.quit()
            exit(0)

    # Change in position when keys are TRUE. Refer to default movement speed defined up there.
    # This block of code was borrowed, but modified.
    if keys[0]:
        playerpos[1] -= movementSpeed
    elif keys[2]:
        playerpos[1] += movementSpeed
    if keys[1]:
        playerpos[0] -= movementSpeed
    elif keys[3]:
        playerpos[0] += movementSpeed

    # Enemy Weapons Timer Deployment
    # The missiles are designed to launch from the specified X and Y
    # They go to player position
    # Some parts of this code was borrowed but has been modified extensively
    if enemyTimer1 == 0:
        position = playerpos
        startPos = enemy1
        projectiles.append(
            [math.atan2(position[1] - (startPos[1] + 32), position[0] - (startPos[0] + 26)), startPos[0] + 32,
             startPos[1] + 32])
        if enemyTimer1 <= 0:
            enemyTimer1 = random.randint(15, 60)  # Firing frequency randomized

    if enemyTimer2 == 0:
        position = playerpos
        startPos = enemy2
        projectiles.append(
            [math.atan2(position[1] - (startPos[1] + 32), position[0] - (startPos[0] + 26)), startPos[0] + 32,
             startPos[1] + 32])
        if enemyTimer2 <= 0:
            enemyTimer2 = random.randint(15, 60)  # Firing frequency randomized

    if enemyTimer3 == 0:
        position = playerpos
        startPos = enemy3
        projectiles.append(
            [math.atan2(position[1] - (startPos[1] + 32), position[0] - (startPos[0] + 26)), startPos[0] + 32,
             startPos[1] + 32])
        if enemyTimer3 <= 0:
            enemyTimer3 = random.randint(15, 60)  # Firing frequency randomized

    if enemyTimer4 == 0:
        position = playerpos
        startPos = enemy4
        projectiles.append(
            [math.atan2(position[1] - (startPos[1] + 32), position[0] - (startPos[0] + 26)), startPos[0] + 32,
             startPos[1] + 32])
        if enemyTimer4 <= 0:
            enemyTimer4 = random.randint(15, 60)  # Firing frequency randomized

    if enemyTimer5 == 0:
        position = playerpos
        startPos = enemy5
        projectiles.append(
            [math.atan2(position[1] - (startPos[1] + 32), position[0] - (startPos[0] + 26)), startPos[0] + 32,
             startPos[1] + 32])
        if enemyTimer5 <= 0:
            enemyTimer5 = random.randint(15, 60)  # Firing frequency randomized

    if enemyTimer6 == 0:
        position = playerpos
        startPos = enemy6
        projectiles.append(
            [math.atan2(position[1] - (startPos[1] + 32), position[0] - (startPos[0] + 26)), startPos[0] + 32,
             startPos[1] + 32])
        if enemyTimer6 <= 0:
            enemyTimer6 = random.randint(15, 25)  # Firing frequency randomized

    # Countdown until next shot in frames per second
    enemyTimer1 -= 1
    enemyTimer2 -= 1
    enemyTimer3 -= 1
    enemyTimer4 -= 1
    enemyTimer5 -= 1
    enemyTimer6 -= 1

    # Fuel Spawn by time (Frames per second)
    # Spawn randomized to make it more interesting
    if fuelTimer == 0:
        fuelX = random.randint(50, width - 400)
        fuelY = random.randint(70, height - 100)
        fuelPosition = [fuelX, fuelY]
        if currentFuel <= maxFuel:
            fuels.append(fuelPosition)
            currentFuel += 1

    # Countdown until next fuel is spawned
    fuelTimer -= 1

    # Using rect for collision
    for fuel in fuels:
        screen.blit(fuelImg, fuel)
        fuelRect = pygame.Rect(fuelImg.get_rect())
        fuelRect.left = fuelX
        fuelRect.top = fuelY
        playerRect = pygame.Rect(player.get_rect())
        playerRect.left = playerpos[0]
        playerRect.top = playerpos[1]
        if fuelRect.colliderect(playerRect):
            fuels.pop()  # Removes the fuel when collision occurs
            fuelTimer = 250  # Resets fuelTimer when fuel is picked up
            movementSpeed -= 1.5  # Player loses movement speed everytime they pick up fuel to simulate cargo
            scoreCounter += 1  # Player gains a score
            playerHealth += 50  # Player gains health when they pick up fuel

    # Drawing the Projectiles. Projectiles are set to disappear at the edge of the screen.
    for bullet in projectiles:
        velx = math.cos(bullet[0]) * random.randint(10, 15)  # Randomized missile speed
        vely = math.sin(bullet[0]) * random.randint(10, 15)  # Randomized missile speed
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < 0 or bullet[1] > width or bullet[2] < 0 or bullet[2] > width:
            projectiles.pop(index)

    # Setting missile collision with player
    index = 0
    for projectile in projectiles:
        arrow1 = pygame.transform.rotate(missiles, 360 - projectile[0] * 57.29)

        projectileRect = pygame.Rect(missiles.get_rect())
        projectileRect.left = projectile[1]
        projectileRect.top = projectile[2]

        playerRect = pygame.Rect(player.get_rect())
        playerRect.left = playerpos[0]
        playerRect.top = playerpos[1]
        if projectileRect.colliderect(playerRect):
            projectiles.pop(index)
            index += 1
            playerHealth -= 5  # Player loses 5 hp when colliding with a missile
            # print (playerHealth)
        screen.blit(arrow1, (projectile[1], projectile[2]))

    # Player Healthbar
    # This block of code is borrowed
    screen.blit(healthbar, (5, 5))
    for health1 in range(playerHealth):
        screen.blit(health, (health1 + 8, 8))
    if playerHealth < 0:
        playerHealth = 0

    # Check player HP and objective counter
    # Ends the loop and set value to exitcode depending on which if statement is true
    if playerHealth <= 0:
        running = 0
        exitcode = 1
    if scoreCounter == 10:
        running = 0
        exitcode = 2

    # This line of code updates the screen! VERY IMPORTANT!
    pygame.display.flip()

# Checking for win or loss
if exitcode == 2:
    for x in range(width // youWon.get_width()):
        for y in range(height // youWon.get_height()):
            screen.blit(youWon, (x * 1, y * 1))
    pygame.display.flip()
    k = input("Press enter to quit")
    pygame.quit()

if exitcode == 1:
    for x in range(width // youLost.get_width()):
        for y in range(height // youLost.get_height()):
            screen.blit(youLost, (x * 1, y * 1))
    pygame.display.flip()
    pygame.quit()
