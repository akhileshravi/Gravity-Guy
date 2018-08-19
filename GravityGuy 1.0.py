#Akhilesh Ravi
#16110007
#ES112 Project

'''
Gravity Guy
Gravity Guy is a game in which you are running away from your enemy
and you can change your gravity, that is, the direction towards which
gravity pulls you.
'''

#####  Importing Modules  #####

import pygame, sys, random, time

from pygame.locals import *

pygame.init()

#Pygame Window
scrWidth = 960
scrHeight = 540
scr = pygame.display.set_mode((scrWidth,scrHeight),0,32)
pygame.display.set_caption('Gravity Guy')                    

#Dimensions
skWidth = 44    # Main Character Dimensions
skHeight = 55

pwidth = 149          # Sizes of the Platform images
pheight = 39

# Fonts
font1 = pygame.font.SysFont('Algerian', 32)
font2 = pygame.font.SysFont('Algerian', 36)
font3 = pygame.font.SysFont('Monaco', 32)


# The states of the character
up, down = 'up', 'down'

# Images

gravityguyDownImg = 'skateboarder1a_down_t.png'
gravityguyUpImg = 'skateboarder1a_up_t.png'
back = 'background.png'
platimg = 'platform2t.png'

# Loading Images
ggDownImg = pygame.image.load(gravityguyDownImg).convert_alpha()
ggUpImg = pygame.image.load(gravityguyUpImg).convert_alpha()
background = pygame.image.load(back).convert()
platformImg = pygame.image.load(platimg).convert_alpha()
platformImg = { up: platformImg, down : platformImg}


#######    Class Definitions    #######

class MainChar(pygame.sprite.Sprite):
    '''
Class for the Main Character
    '''
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = ggDownImg
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = (scrHeight - skHeight)/2
        self.state = down
        self.switchState = 0

    def update(self, dgx, dy):

        self.rect.x += dgx
        self.rect.y += dy
        if True in (self.rect.y <= -skHeight, self.rect.y > scrHeight,
                    self.rect.x <= -skWidth, self.rect.x > scrWidth):
            global alive
            alive = False
        if dy < 0:
            self.image = ggUpImg
        elif dy > 0:
            self.image = ggDownImg

    def changeState(self, flag = False):
        '''
Changes state of the main character
        '''

        global dy
        if flag:
            self.switchState -= 1
        if self.state == down and dy == 0:
            self.state = up
            self.image = ggUpImg
            dy = -4
            
        elif self.state == up and dy == 0:
            self.state = down
            self.image = ggDownImg
            dy = 4

        else:
            self.switchState += 1

                    
    def checkPlatform(self,dgx,dy):
        '''
Checks whether the main character collides with a platform
        '''

        if self.state == down:
            stopFlag = False
            fall = True
            for position in Platform.plist:

                for plat in Platform.plist[position]:

                    if False not in (plat.rect.x < self.rect.x + skWidth+2,
                                     self.rect.x < plat.rect.x + pwidth+2):
                        if 0 <= plat.rect.y - self.rect.y - skHeight <= abs(dy)+2:
                            dy = 0
                            stopFlag = True
                            break
                if stopFlag:
                    break
            else:
                dy = 4
                    
        else:
            stopFlag = False
            fall = True
            for position in Platform.plist:

                for plat in Platform.plist[position]:

                    if False not in (plat.rect.x < self.rect.x + skWidth+2,
                                self.rect.x < plat.rect.x + pwidth+2):
                        if 0 <= self.rect.y - plat.rect.y - pheight <= abs(dy)+2:
                        
                            dy = 0
                            stopFlag = True
                            break

                    
                if stopFlag:
                    break
            else:
                dy = -4
            
        for position in Platform.plist:
            stopFlag = False
            for plat in Platform.plist[position]:

                if False not in (plat.rect.y < self.rect.y + skHeight+2,
                                     self.rect.y < plat.rect.y + pheight+2):
                    if 0 <= plat.rect.x - self.rect.x - skWidth <= abs(dgx)+1:
                        dgx = -5
                        stopFlag = True
                        break
                if stopFlag:
                    break
            else:
                dgx = 0           
    
        return dgx, dy


class Platform(pygame.sprite.Sprite):
    '''
Class for making Platform objects
    '''
    plist = {up : [], down : []}

    def __init__(self, px, py, position):
        pygame.sprite.Sprite.__init__(self) 
        self.image = platformImg[position]
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        Platform.plist[position] += [self]

    def update(self, dpx, dpy):
        '''
Updates the position of a Platform object
        '''
        self.rect.x += dpx
        self.rect.y += dpy
        
        for position in Platform.plist:

            if self in Platform.plist[position] and self.rect.x < -(pwidth):

                Platform.plist[position].remove(self)
                splist.remove(self)
                del self
                break
            

    @staticmethod
    def updateAll(dx, dy):
        '''
Updates the positions of all Platform objects
        '''
        
        for position in Platform.plist:
            for i in Platform.plist[position]:
                i.update(dx, dy)
    
    def __del__(self):
        pass


#######    Function Definitions    #######


def loading():
    '''
Function for the loading bar
    '''
    frequencies = {1:4,2:10,3:8,4:4,5:3,6:2,7:2,8:1,9:1,10:1}
    l = []
    for i in frequencies:
        l += [i]*frequencies[i]
    width, height = 400, 30
    rect1 = ((scrWidth-400)/2, (scrHeight-30)/2, width, height)
    colour = (200,0,0)
    parts = width/100
    time.sleep(0.255)
    logo = font2.render('GRAVITY GUY', True, (120, 150, 200))
    logoWidth, logoHeight = logo.get_width(), logo.get_height()
    scr.blit(logo,((scrWidth - logoWidth)/2, scrHeight/2 - 80))
    for i in range(1,51):
        pygame.draw.rect(scr, (255,255,255), rect1, 5)
        pygame.draw.rect(scr, (0,0,0), rect1, 0)
        rect2 = (rect1[0], rect1[1], parts * i, height)
        pygame.draw.rect(scr,colour,rect2,0)
        txt = font1.render('LOADING '+str(i-1)+'%', True, (255, 255, 255))
        txtWidth, txtHeight = txt.get_width(), txt.get_height()
        scr.blit(txt,((scrWidth - txtWidth)/2, (scrHeight - txtHeight)/2))
        period = frequencies[random.choice(l)]
        time.sleep(0.02*period)
        colour = (colour[0]-4,colour[1]+4,0)
        pygame.display.update()
        for event in pygame.event.get():    # Loop to check the events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    for i in range(1,51):
        pygame.draw.rect(scr, (255,255,255), rect1, 5)
        pygame.draw.rect(scr, (0,0,0), rect1, 0)
        
        rect2 = (rect1[0], rect1[1], width/2 + parts * i, height)
        pygame.draw.rect(scr,colour,rect2,0)
        txt = font1.render('LOADING '+str(i+49)+'%', True, (255, 255, 255))
        txtWidth, txtHeight = txt.get_width(), txt.get_height()
        scr.blit(txt,((scrWidth - txtWidth)/2, (scrHeight - txtHeight)/2))
        period = frequencies[random.choice(l)]
        time.sleep(0.02*period)
        colour = (0,colour[1]-4,colour[2]+4)
        pygame.display.update()
        for event in pygame.event.get():    # Loop to check the events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def menu():
    '''
Function for the menu screen
    '''
    scr.blit(background, (0,0))
    logo = font2.render('GRAVITY GUY', True, (120, 150, 200))
    logoWidth, logoHeight = logo.get_width(), logo.get_height()
    scr.blit(logo,((scrWidth - logoWidth)/2, scrHeight/2 - 80))
    txt = font3.render('Press Space To Start', True, (50, 150, 100))
    txtWidth, txtHeight = txt.get_width(), txt.get_height()
    scr.blit(txt,((scrWidth - txtWidth)/2, scrHeight/2 + 100))
    pygame.display.update()
    no_space = True
    fps = 60
    clock = pygame.time.Clock()
    while no_space:
        for event in pygame.event.get():    # Loop to check the events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                key = event.key

                if key == K_SPACE:
                    no_space = False
        clock.tick(fps)

def dispscore(score):
    '''
Displays the score of the player
    '''
    scr.blit(background, (0,0))
    txt = font3.render('Press Space To Continue', True, (50, 150, 100))
    txtWidth, txtHeight = txt.get_width(), txt.get_height()
    scr.blit(txt,((scrWidth - txtWidth)/2, scrHeight/2 + 100))
    txt = font2.render('SCORE: '+str(score), True, (200, 150, 100))
    txtWidth, txtHeight = txt.get_width(), txt.get_height()
    scr.blit(txt,((scrWidth - txtWidth)/2, scrHeight/2))
    pygame.display.update()
    no_space = True
    fps = 60
    clock = pygame.time.Clock()
    while no_space:
        for event in pygame.event.get():    # Loop to check the events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                key = event.key

                if key == K_SPACE:
                    no_space = False
        clock.tick(fps)
ingame = True

#####  Variable Definition /Initiation  ######

fps = 60
clock = pygame.time.Clock()

upStd = (scrHeight*1)/3 - pheight/2
downStd = (scrHeight*2)/3 - pheight/2
begin = pwidth * 7
platformList = [[],
                [(begin, downStd+50, down)],
                [(begin, upStd+50, up)],
                [(begin, upStd, up), (begin, downStd, down)],
                [(begin, upStd, up), (begin, downStd, down)]
                ]

    
loading()

#######    Main Game Loop    #######

while ingame:

    menu()
    dx = -5
    dy = 4
    dgx = 0
    gravityguy = MainChar()
    splist = pygame.sprite.Group()
    splist.add(gravityguy)

    # Creating the initial platforms    
    px = 0
    score = 0

    for i in range(7):
        plat1 = Platform(px, downStd, down)
        plat2 = Platform(px, upStd, up)
        splist.add(plat1)
        splist.add(plat2)
        px += pwidth
    index = 0

    # Creating the successive platforms
    for i in range(7):
        for i in range(4):
            plat1 = Platform(px+pwidth, downStd+50, down)
            plat2 = Platform(px+pwidth, upStd-50, up)
            plat3 = Platform(px+pwidth*2, downStd, down)
            plat4 = Platform(px+pwidth*2, upStd, up)
            splist.add(plat1)
            splist.add(plat2)
            splist.add(plat3)
            splist.add(plat4)
            px+= 3*pwidth
        for i in range(4):
            plat1 = Platform(px, downStd+50, down)
            plat2 = Platform(px+pwidth, downStd+75, down)
            plat3 = Platform(px+pwidth*3, upStd-15, down)
            splist.add(plat1)
            splist.add(plat2)
            splist.add(plat3)
            px += pwidth*4
    
    alive = True
    while alive:
        score += 5
        scr.blit(background, (0,0))
        splist.draw(scr)
        
        pygame.display.update()

        res = gravityguy.update(dgx, dy)
        if res != None:
            print 'GAME OVER'
            pygame.quit()
            break

        #Updating all platforms
        Platform.updateAll(dx,0)
        
        dgx, dy = gravityguy.checkPlatform(dgx, dy)
        
        if dy == 0 and gravityguy.switchState > 0:
            gravityguy.changeState(True)

        for event in pygame.event.get():    # Loop to check the events
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    key = event.key

                    if key == K_SPACE:
                        gravityguy.changeState()
                        pass
                            
        clock.tick(fps)

    dispscore(score)
    
    
