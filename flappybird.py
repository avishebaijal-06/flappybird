import pygame, random, pyautogui, time, math
pygame.init()
W,H=pyautogui.size()
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("Flappybird")
gamestate="start"

bg=pygame.image.load("bg3.png")
ground=pygame.image.load("ground.png")
bg=pygame.transform.scale(bg,(W,H))
ground=pygame.transform.scale(ground,(W*2,H//4))
pipegap=200
clock=pygame.time.Clock()
pipefrequency=500
lastpipe=pygame.time.get_ticks()

class Bird (pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        self.velocity=0
        for i in range(3):
            img=pygame.image.load(f"bird{i+1}.png")
            self.images.append(img)
        self.image=self.images[0]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
    def update(self):
        if gamestate=="play":

            self.velocity+=0.5
            if self.velocity>8:
                self.velocity=8
            if self.rect.bottom<H-H//4:
                self.rect.y+=self.velocity
            if pygame.mouse.get_pressed()[0]==1:
                self.velocity=-10
            self.index+=1
            if self.index>2:
                self.index=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index],self.velocity*-2)
        if gamestate=="end":
            self.image=pygame.transform.rotate(self.images[self.index],-90)

class Pipe (pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pipe.png")
        self.rect=self.image.get_rect()
        if pos=="top":
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-pipegap//2]
        if pos=="bottom":
            self.rect.topleft=[x,y+pipegap//2]
    def update(self):
        self.rect.x-=10
        if self.rect.right<0:
            self.kill()
birdgroup=pygame.sprite.Group()
flappy=Bird(100,H/2)
birdgroup.add(flappy)
pipegroup=pygame.sprite.Group()

groundscroll=0
run=True
while run:
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundscroll,H-H//4))
    if gamestate=="play":
        groundscroll-=10
        if flappy.rect.bottom>H-H//4:
            gamestate="end"
        if groundscroll<-W:
            groundscroll=0  
        currenttime=pygame.time.get_ticks()
        if currenttime-lastpipe>pipefrequency:
            pipeheight=random.randint(-100,100)
            bottompipe=Pipe(W,H//2+pipeheight,"bottom")
            toppipe=Pipe(W,H//2+pipeheight,"top")
            pipegroup.add(bottompipe)
            pipegroup.add(toppipe)
            lastpipe=currenttime
        pipegroup.update()
        if pygame.sprite.groupcollide(birdgroup,pipegroup,False,False) and flappy.rect.top<0:
            gamestate="end"
    birdgroup.draw(screen)
    birdgroup.update()
    pipegroup.draw(screen)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
        if e.type==pygame.MOUSEBUTTONDOWN and gamestate=="start":
            gamestate="play"
    pygame.display.update()

