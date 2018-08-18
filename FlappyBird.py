# Flappy Bird
import pygame
import random
# 初始化与画布大小
pygame.init()
screen = pygame.display.set_mode([288,512])
# 加载背景与名称
background = pygame.image.load("assets/background.png")
pygame.display.set_caption("Flappy Bird")
# 背景音乐
bgm = pygame.mixer.Sound('sound/bgm.wav')
channel_1 = pygame.mixer.Channel(1)
channel_1.play(bgm)

keep_going = True
clock = pygame.time.Clock()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.birdSprites = [pygame.image.load("assets/0.png"), pygame.image.load("assets/1.png"), pygame.image.load("assets/2.png")]
        self.a = 0
        self.birdX = 50 # 初始x坐标
        self.birdY = 100 # 初始y坐标
        self.jumpSpeed = 7 # 跳跃高度
        self.gravity = 0.4 # 跳跃重力

        self.rect = self.birdSprites[self.a].get_rect()
        self.rect.center = (self.birdX,self.birdY)

    def birdUpdate(self):
    	self.jumpSpeed -= self.gravity
    	self.birdY -= self.jumpSpeed
    	self.rect.center = (self.birdX,self.birdY)

    	if self.jumpSpeed < 0: # 当y向值<0时，鸟下坠
    		self.a = 1
    	if self.jumpSpeed > 0: # 当y向值>0时，鸟上升
    		self.a = 2

    def birdCrush(self):
    	global keep_going
    	resultU = self.rect.colliderect(newWall.wallUpRect)
    	resultD = self.rect.colliderect(newWall.wallDownRect)

    	if resultU or resultD or newBird.rect.top > 512:
    		hit = pygame.mixer.Sound('sound/hit.wav')
    		channel_3 = pygame.mixer.Channel(3)
    		channel_3.play(hit)
    		keep_going = False

class Wall():
	def __init__(self):
		self.wallUp = pygame.image.load("assets/bottom.png")
		self.wallDown = pygame.image.load("assets/top.png")
		self.wallUpRect = self.wallUp.get_rect()
		self.wallDownRect = self.wallDown.get_rect()

		self.gap = 50 # 缝隙间隔
		self.wallx = 288
		self.offset = random.randint(-50, 50)

		self.wallUpY = 360 + self.gap - self.offset
		self.wallDownY = 0 - self.gap - self.offset

		self.wallUpRect.center = (self.wallx,self.wallUpY)
		self.wallDownRect.center = (self.wallx,self.wallDownY)

	def wallUpdate(self):
		self.wallx -= 2 # 速度 2
		self.wallUpRect.center = (self.wallx,self.wallUpY)
		self.wallDownRect.center = (self.wallx,self.wallDownY)

		if self.wallx < -370:
			self.wallx = 360
			self.offset = random.randint(-50, 50)
			self.wallUpY = 360 + self.gap - self.offset
			self.wallDownY = 0 - self.gap - self.offset

newBird = Bird()
newWall = Wall()

while keep_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
        	newBird.jumpSpeed = 7

        	channel_2 = pygame.mixer.Channel(2)
        	fly = pygame.mixer.Sound('sound/fly.WAV')
        	channel_2.play(fly)

    screen.blit(background,(0,0))
    screen.blit(newBird.birdSprites[newBird.a],newBird.rect)
    screen.blit(newWall.wallUp,newWall.wallUpRect)
    screen.blit(newWall.wallDown,newWall.wallDownRect)

    newWall.wallUpdate()
    newBird.birdUpdate()
    newBird.birdCrush()
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
