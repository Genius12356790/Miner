import time
import pygame
import sys
import os
import random

FRAMETIME = 1/60

def opencell(xx, yy):
    global gameover
    if field[xx][yy] == 10:
        field[xx][yy] = -10
        gameover = 1
    elif field[xx][yy] < 0 and field[xx][yy] > -10:
        field[xx][yy] += 9
        if field[xx][yy] == 0:
            for z in cir:
                xd = xx + z[0]
                yd = yy + z[1]
                if xd > -1 and xd < x and yd > -1 and yd < y:
                    if field[xd][yd] < 0:
                        opencell(xd, yd)

def textout(text, pos, size=30, font='Comic Sans MS', color=(255, 255, 255), sur=0):
    myfont = pygame.font.SysFont(font, size)
    textsurface = myfont.render(str(text), False, color)
    sur.blit(textsurface,(pos))
    
def terminate():
    pygame.quit()
    sys.exit()   
    
class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(cell)
        self.image = pygame.Surface((20, 20))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 19, 19))
        pygame.draw.line(self.image, (100, 100, 100), (0, 18), (19, 18), 2)
        pygame.draw.line(self.image, (100, 100, 100), (18, 0), (18, 19), 2)
        self.rect = self.image.get_rect()
        self.rect.x = x * 21
        self.rect.y = y * 21
        self.x = x
        self.y = y
        self.pr = field[x][y]
        
    def update(self):
        if field[self.x][self.y] != self.pr:
            self.pr = field[self.x][self.y]
            if self.pr == -10:
                self.image = pygame.Surface((20, 20))
                pygame.draw.rect(self.image, (150, 150, 150), (0, 0, 19, 19))
                pygame.draw.line(self.image, (70, 70, 70), (0, 0), (19, 0), 2)
                pygame.draw.line(self.image, (70, 70, 70), (0, 0), (0, 19), 2)  
                textout('M', (3, -2), sur=self.image, color=(255, 0, 0), size=18)
            elif self.pr > -1 and self.pr < 9:
                self.image = pygame.Surface((20, 20))
                pygame.draw.rect(self.image, (150, 150, 150), (0, 0, 19, 19))
                pygame.draw.line(self.image, (70, 70, 70), (0, 0), (20, 0), 2)
                pygame.draw.line(self.image, (70, 70, 70), (0, 0), (0, 20), 2)                    
                if self.pr != 0:
                    textout(str(self.pr), (3, -2), sur=self.image, color=(0, 255, 0), size=18)
            elif self.pr < -10:
                pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 19, 19))
                pygame.draw.line(self.image, (100, 100, 100), (0, 18), (19, 18), 2)
                pygame.draw.line(self.image, (100, 100, 100), (18, 0), (18, 19), 2)
                textout(str('P'), (3, -2), sur=self.image, color=(0, 0, 255), size=18)
            else:
                pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 19, 19))
                pygame.draw.line(self.image, (100, 100, 100), (0, 18), (19, 18), 2)
                pygame.draw.line(self.image, (100, 100, 100), (18, 0), (18, 19), 2)                
                
# input settigs
x, y = [int(a) for a in input('size\n > ').split()]
mines = int(input('mines\n > '))
gameover = 0

# init field
if x < 5 or y < 5 or mines < x * y * 0.1 or mines > x * y * 0.5 or x > 31 or y > 31:
    x = 10
    y = 10
    mines = 10
field = [[-9] * y for a in range(x)] # 0..8 = minedata -9..-1 = cell 10 = mine -109..-90 = flag
m = 0
while m != mines:
    xx = random.randint(0, x - 1)
    yy = random.randint(0, y - 1)
    if field[xx][yy] == -9:
        m += 1
        field[xx][yy] = 10
cir = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
for xx in range(x):
    for yy in range(y):
        for z in cir:
            xd = xx + z[0]
            yd = yy + z[1]
            if xd > -1 and xd < x and yd > -1 and yd < y and field[xx][yy] == 10 and field[xd][yd] < 0:
                field[xd][yd] += 1

# init pg
pygame.init()
size = width, height = x * 21, y * 21 + 50
screen = pygame.display.set_mode(size)
cell = pygame.sprite.Group()
for xx in range(x):
    for yy in range(y):
        Cell(xx, yy)
lastframe = time.process_time()
gtime = lastframe
while True:
    
    # mousepos or exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()   
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            if event.button == 1:
                posx = min(event.pos[0] // 21, x)
                posy = min(event.pos[1] // 21, y)        
                opencell(posx, posy)
            if event.button == 3:
                posx = event.pos[0] // 21
                posy = event.pos[1] // 21  
                if field[posx][posy] < -10:
                    field[posx][posy] += 100
                elif field[posx][posy] < 0 or field[posx][posy] == 10:
                    field[posx][posy] -= 100
            s = sum(sum(b < -1 and b != -90 for b in a) for a in field)
            if not s:
                gameover = -1                        
    # update graphics
    cell.update()
    cell.draw(screen)
    if gameover == 1:
        textout('Game Over', ((x * 21) // 2 - 75, (y * 21) // 2 - 20), color=(255, 0, 0), sur=screen)
    if gameover == -1:
        textout('Road Cleared!', ((x * 21) // 2 - 95, (y * 21) // 2 - 20), color=(60, 255, 60), sur=screen)
    pygame.display.flip()
    pygame.draw.rect(screen, (0, 0, 0), (0, height - 50, width, height),)
    textout(str(int(gtime)), (0, height - 55), color=(255, 255, 255), sur=screen, size=24)
    textout(str(int(mines - sum(sum(b < -89 for b in a) for a in field))), (0, height - 30), color=(255, 0, 0), sur=screen, size=24)
    # wait until next frame
    while time.process_time() < lastframe + FRAMETIME:
        pass
    lastframe += FRAMETIME
    prtime = time.process_time()
    if lastframe + 0.1 < prtime:
        lastframe = prtime 
    if not gameover:
        gtime = prtime