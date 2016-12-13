import pygame
import sys
import random
from pygame import gfxdraw

pygame.init()

height = 550
width = 350
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pipeCounterEnd = 1
pipeCounterStart = 0
pipeRate = 50
myfont = pygame.font.SysFont("monospace", 15)
scorePoints = 0
gameLost = False

class bird:
    def __init__(self):
        self.y = height/2
        self.x = 64

        self.gravity = 0.8
        self.lift = -12
        self.velocity = 0

    def show(self):
      pygame.draw.circle(screen,(255,255,255),(int(self.x),int(self.y)),10,0)

    def up(self):
        self.velocity += self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > height:
            self.y = height
            self.velocity = 0

    def hitDetection(self):
        for i in range(pipeCounterStart,pipeCounterEnd):
            global gameLost
            # bird must be on same x (-15/+15 bc. width of pipe and radius of ball)
            if (self.x > (pipes[i].giveX()-15) and self.x < (pipes[i].giveX()+15)):
                #bot rec
                if self.y>(height-pipes[i].giveBottom()-10) and self.y<(height+100):
                    pipes[i].hitAlert()
                    gameLost = True
                #top rec
                if self.y>-100 and self.y<(pipes[i].giveTop()):
                    pipes[i].hitAlert()
                    gameLost = True

class pipe():
    def __init__(self):
        self.top = height/2 - random.randint(0,100)
        self.bottom = height/2 - random.randint(0,110)
        self.x = width
        self.w = 20
        self.speed = 4
        self.colour = (255,255,255)

    def giveX(self):
        return self.x
    def giveBottom(self):
        return self.bottom
    def giveTop(self):
        return self.top
    def hitAlert(self):
        self.colour = (255,0,0)

    def show(self):
        pygame.draw.rect(screen,self.colour,(self.x,0,self.w,self.top))
        pygame.draw.rect(screen,self.colour,(self.x,height-self.bottom,self.w,self.bottom))


    def update(self):
        self.x -= self.speed

    def createPipe(self):
        if self.x == (width-self.speed*pipeRate):
            global pipeCounterEnd
            pipeCounterEnd +=1

    def deletePipe(self):
        if self.x == 0:
            global pipeCounterStart
            pipeCounterStart +=1

    def givePoint(self):
        global scorePoints
        if self.x == 62 and gameLost == False:
            scorePoints +=1


pipes = [pipe() for _ in range(100)]

flappy = bird()

while gameLost == False:
    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flappy.up()

    #erase screen
    screen.fill((0,0,0))

    flappy.show()
    flappy.update()
    flappy.hitDetection()

    scoreLabel = myfont.render(str(scorePoints), 1, (255,255,0))
    screen.blit(scoreLabel, (10, 10))

    #create pipes
    for i in range(pipeCounterStart,pipeCounterEnd):
        pipes[i].show()
        pipes[i].update()
        pipes[i].createPipe()
        pipes[i].deletePipe()
        pipes[i].givePoint()

    #update screen
    clock.tick(30)
    pygame.display.update()
