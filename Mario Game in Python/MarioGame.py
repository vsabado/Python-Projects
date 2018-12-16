import random
import pygame
import time

from pygame.locals import *
from time import sleep


class Model():
    def __init__(self):
        self.groundOffset = 8  # To make Mario's feet on the line
        self.ground = 614
        self.marioHeight = 95
        self.goombaHeight = 60
        self.sprites = []
        self.mario = Mario(150, self.ground - self.marioHeight - self.groundOffset)
        self.sprites.append(self.mario)
        self.PokemonHeight = 83

        tubeWidth = 55
        spritecount = 0
        tubeX = 0
        prevX = 0
        goombaTossUp = 0
        while spritecount <= 10:
            tubeX += random.randint(300, 600)  # Randomized placement of the tubes
            prevX = tubeX
            self.sprites.append(Tube(tubeX, self.ground - random.randint(50, 250)))  # Randomized length of the tubes

            goombaTossUp = random.randint(1, 2)
            if goombaTossUp != 1:
                self.sprites.append(
                    Goomba(random.randint(prevX + tubeWidth, tubeX + tubeWidth), self.ground - self.goombaHeight))
            else:
                self.sprites.append(
                    Pokemon(random.randint(prevX + tubeWidth, tubeX + tubeWidth), self.ground - self.PokemonHeight))
            spritecount += 1

    def update(self):
        for spr in self.sprites:
            spr.update()

        for spr in self.sprites:
            if isinstance(spr, Tube):
                t = spr
                self.goombaCollide(t)
                self.fireballCollide(t)
                self.pokeCollide(t)
                if self.doescollide(self.mario.x, self.mario.y, self.mario.w, self.mario.h, t.x, t.y, t.w, t.h):
                    self.mario.getOut(t)

            if isinstance(spr, Goomba):
                self.goombaFire(spr)
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, self.mario.x, self.mario.y, self.mario.w, self.mario.h):
                    self.mario.health -= 5
                    self.mario.image = pygame.image.load("resources/images/turtle.png")
                if spr.defaultHP == 0:
                    self.sprites.remove(spr)
            if isinstance(spr, Pokemon):
                self.pokeFire(spr)
                if spr.defaultHP == 0:
                    self.sprites.remove(spr)
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, self.mario.x, self.mario.y, self.mario.w, self.mario.h):
                    self.mario.teleportMario()

    def pokeCollide(self, t):
        for spr in self.sprites:
            if isinstance(spr, Pokemon):
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, t.x, t.y, t.w, t.h):
                    spr.pokeGetOut()

    def goombaFire(self, g):
        for spr in self.sprites:
            if isinstance(spr, Fireball):
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, g.x, g.y, g.w, g.h):
                    g.onfire()

    def pokeFire(self, p):
        for spr in self.sprites:
            if isinstance(spr, Fireball):
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, p.x, p.y, p.w, p.h):
                    p.onhit()

    def goombaCollide(self, t):
        for spr in self.sprites:
            if isinstance(spr, Goomba):
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, t.x, t.y, t.w, t.h):
                    spr.goombaGetOut()

    def move(self, dx):
        self.mario.move(dx)

    def doescollide(self, x1, y1, w1, h1, x2, y2, w2, h2):
        if (x1 + w1) < x2:
            return False
        if x1 > (x2 + w2):
            return False
        if (y1 + h1) < y2:
            return False
        if y1 > (y2 + h2):
            return False
        return True

    def addFireball(self):
        if self.mario.isFacingRight:
            f = Fireball(self.mario.x, self.mario.y)
            self.sprites.append(f)
        else:
            f = Fireball(self.mario.x - self.mario.w, self.mario.y)
            self.sprites.append(f)

        if self.mario.leftFrameCounter >= 1:
            f.changeDir()

    def fireballCollide(self, t):
        for spr in self.sprites:
            if isinstance(spr, Fireball):
                if self.doescollide(spr.x, spr.y, spr.w, spr.h, t.x, t.y, t.w, t.h):
                    self.sprites.remove(spr)


class View():
    def __init__(self, model):
        self.screen_size = (1440, 900)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        self.model = model
        self.background = pygame.image.load("resources/images/bg1.jpg")
        self.gameOver = pygame.image.load("resources/images/youlost2.png")
        self.model.rect = self.background.get_rect()
        self.viewOffset = 200

    def update(self):
        self.screen.fill([0, 200, 100])
        self.screen.blit(self.background, self.model.rect)
        if self.model.mario.health == 0:
            pygame.mixer.music.stop()
            self.model.sprites = []
            self.screen.blit(self.gameOver, self.model.rect)

        for spr in self.model.sprites:
            if isinstance(spr, Mario):
                self.screen.blit(spr.marioHPBarR, (5, 5))
                for health1 in range(self.model.mario.health):
                    self.screen.blit(self.model.mario.marioHPBarG, (health1 + 8, 8))
                if self.model.mario.health < 0:
                    self.model.mario.health = 0
            self.screen.blit(spr.image, (spr.x - self.model.mario.x + self.viewOffset, spr.y))
        pygame.display.flip()


class Controller():
    def __init__(self, model):
        self.model = model
        self.running = True
        self.destX = 0
        self.space = 0
        self.shootCounter = 10

    def update(self):
        self.shootCounter -= 1
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # pygame.mixer.pause()
                    boing = pygame.mixer.Sound('resources/audio/boing.wav')
                    pygame.mixer.Sound.play(boing)  # Play audio
                    pygame.mixer.Sound.set_volume(boing, 0.10)  # Audio volume

                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    pygame.mixer.unpause()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.destX -= 1
            self.model.mario.leftFrameCounter += 1
            self.model.mario.facingRight = False
        if keys[K_RIGHT]:
            self.destX += 1
            self.model.mario.rightFrameCounter += 1
            self.model.mario.facingRight = True
        if keys[K_SPACE]:
            self.space -= 48
        if keys[K_LCTRL] and self.shootCounter <= 0:
            self.shootCounter = 10
            self.model.addFireball()

        self.model.move(self.destX)
        self.destX = 0
        self.model.mario.jump(self.space)
        self.space = 0


class Mario():
    def __init__(self, x, y):
        self.jumpCounter = 0
        self.health = 200
        self.destX = 0
        self.h = 95
        self.w = 60
        self.x = x
        self.y = y
        self.vertVel = -11
        self.rightFrameCounter = 0
        self.leftFrameCounter = 0
        self.image = pygame.image.load("resources/images/mario1.png")
        self.marioHPBarR = pygame.image.load("resources/images/healthbar.png")
        self.marioHPBarG = pygame.image.load("resources/images/health.png")
        self.isFacingRight = False
        self.offGroundCount = 0
        self.prevX = 0
        self.prevY = 0

    def rememberState(self):
        self.prevX = self.x
        self.prevY = self.y

    def update(self):
        self.rememberState()
        self.y -= self.vertVel
        if self.y < 519:
            self.vertVel = -11
        else:
            self.jumpCounter = 0
            self.vertVel = 0

        # self.rightFrameCounter += 1

        if self.rightFrameCounter == 1:
            self.isFacingRight = True
            self.leftFrameCounter = 0
            self.image = pygame.image.load("resources/images/mario1.png")
        elif self.rightFrameCounter == 2:
            self.image = pygame.image.load("resources/images/mario2.png")
        elif self.rightFrameCounter == 3:
            self.image = pygame.image.load("resources/images/mario3.png")
        elif self.rightFrameCounter == 4:
            self.image = pygame.image.load("resources/images/mario4.png")
        elif self.rightFrameCounter == 5:
            self.image = pygame.image.load("resources/images/mario5.png")
            self.rightFrameCounter = 0

        if self.leftFrameCounter == 1:
            self.rightFrameCounter = 0
            self.image = pygame.image.load("resources/images/Lmario1.png")
        elif self.leftFrameCounter == 2:
            self.image = pygame.image.load("resources/images/Lmario2.png")
        elif self.leftFrameCounter == 3:
            self.image = pygame.image.load("resources/images/Lmario3.png")
        elif self.leftFrameCounter == 4:
            self.image = pygame.image.load("resources/images/Lmario4.png")
        elif self.leftFrameCounter == 5:
            self.image = pygame.image.load("resources/images/Lmario5.png")
            self.leftFrameCounter = 0

    def move(self, dx):
        self.destX = self.x + dx
        if self.x < self.destX:
            self.x += 5
        elif self.x > self.destX:
            self.x -= 5

    def jump(self, dy):
        if self.jumpCounter <= 3:
            self.y += dy
        self.jumpCounter += 1

    def teleportMario(self):
        self.health -= 50
        self.x -= 300
        self.y = 200

    def getOut(self, t):
        if (t.x - self.x) > 10 and (self.y + self.w) > t.y:
            self.x = t.x - self.w - 4
        elif (self.y + self.h) >= t.y and self.prevY < (t.y - self.h):
            self.y = t.y - self.h - 4
            self.offGroundCount = 0
            self.vertVel = 0
        elif self.y <= (t.y + t.h) < self.prevY:
            self.y = t.y + t.h + 4
        elif self.x < (t.x + t.w) and (self.y + self.w) > t.y:
            self.x = t.x + self.w + 4


class Tube():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 400
        self.w = 55
        self.image = pygame.image.load("resources/images/tube.png")

    def update(self):
        pass


class Goomba():
    def __init__(self, x, y):
        self.frameCounter = 0
        self.x = x
        self.y = y
        self.h = 60
        self.w = 50
        self.defaultHP = 20
        self.isDead = False
        self.onFire = False
        self.image = pygame.image.load("resources/images/goomba1.png")
        self.horizVel = 5

    def onfire(self):
        self.onFire = True

    def goombaLife(self):
        if self.onFire:
            self.defaultHP -= 1

    def update(self):
        self.x += self.horizVel
        self.frameCounter += 1
        self.goombaLife()

        if self.frameCounter == 1 and self.onFire == False:
            self.image = pygame.image.load("resources/images/goomba1.png")
        elif self.frameCounter == 2 and self.onFire == False:
            self.image = pygame.image.load("resources/images/goomba2.png")
        elif self.frameCounter == 3 and self.onFire == False:
            self.image = pygame.image.load("resources/images/goomba3.png")
        elif self.frameCounter == 4 and self.onFire == False:
            self.image = pygame.image.load("resources/images/goomba4.png")
        elif self.frameCounter == 5 and self.onFire == False:
            self.image = pygame.image.load("resources/images/goomba5.png")
            self.frameCounter = 0

        if self.frameCounter == 1 and self.onFire == True:
            self.image = pygame.image.load("resources/images/GoombaFire1.png")
        elif self.frameCounter == 2 and self.onFire == True:
            self.image = pygame.image.load("resources/images/GoombaFire2.png")
        elif self.frameCounter == 3 and self.onFire == True:
            self.image = pygame.image.load("resources/images/GoombaFire3.png")
        elif self.frameCounter == 4 and self.onFire == True:
            self.image = pygame.image.load("resources/images/GoombaFire4.png")
        elif self.frameCounter == 5 and self.onFire == True:
            self.image = pygame.image.load("resources/images/GoombaFire5.png")
            self.frameCounter = 0

    def goombaGetOut(self):
        self.horizVel *= -1


class Fireball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 47
        self.w = 47
        self.vertVel = 5
        self.horizVel = 10
        self.image = pygame.image.load("resources/images/fireball.png")

    def update(self):
        self.x += self.horizVel
        self.y += self.vertVel
        ground = 614
        maxHeight = 500

        if ((self.y + self.h) > ground and self.vertVel > 0) or (self.y <= maxHeight and self.vertVel < 0):
            self.vertVel *= -1

    def changeDir(self):
        self.horizVel *= -1


class Pokemon():
    def __init__(self, x, y):
        self.frameCounter = 0
        self.x = x
        self.y = y
        self.h = 83
        self.w = 117
        self.image = pygame.image.load("resources/images/Dragon1.png")
        self.horizVel = 5
        self.isHit = False
        self.defaultHP = 50

    def onhit(self):
        self.isHit = True
        self.horizVel = 0
        self.w = 56
        self.h = 86
        self.image = pygame.image.load("resources/images/DragStill.png")

    def update(self):
        if self.isHit:
            self.defaultHP -= 1
        self.x += self.horizVel
        self.frameCounter += 1

        if self.horizVel > 0:
            if self.frameCounter == 0 and self.isHit == False:
                self.image = pygame.image.load("resources/images/Dragon4.png")
            elif self.frameCounter == 1 and self.isHit == False:
                self.image = pygame.image.load("resources/images/Dragon5.png")
            elif self.frameCounter == 2 and self.isHit == False:
                self.image = pygame.image.load("resources/images/Dragon6.png")
                self.frameCounter = 0
        else:
            if self.frameCounter == 0 and self.isHit == False:
                self.image = pygame.image.load("resources/images/Dragon1.png")
            elif self.frameCounter == 1 and self.isHit == False:
                self.image = pygame.image.load("resources/images/Dragon2.png")
            elif self.frameCounter == 2 and self.isHit == False:
                self.image = pygame.image.load("resources/images/Dragon3.png")
                self.frameCounter = 0

    def pokeGetOut(self):
        self.horizVel *= -1


# Driver
pygame.init()
pygame.display.set_caption("Mario Game")
pygame.mixer.init()  # Initializing music
pygame.mixer.music.load('resources/audio/SuperMarioBros.ogg')  # Load audio
pygame.mixer.music.play(-1, 0.0)  # Play audio
pygame.mixer.music.set_volume(0.20)  # Audio volume

gameOverCount = 0

m = Model()
v = View(m)
c = Controller(m)


def gameCondition(model):
    if model.mario.health == 0:
        return True


while c.running:
    c.update()
    m.update()
    v.update()
    sleep(0.04)

    if gameCondition(m):
        gameOver = pygame.mixer.Sound('resources/audio/gameOver.wav')
        pygame.mixer.Sound.play(gameOver)  # Play audio
        pygame.mixer.Sound.set_volume(gameOver, 0.50)  # Audio volume
        time.sleep(gameOver.get_length() + 0.2)
        pygame.quit()
        exit()
