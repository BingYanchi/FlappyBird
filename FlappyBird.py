# Flappy Bird
import pygame
import random
import sys
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
# 游戏开始
keep_going = True
clock = pygame.time.Clock()
# 分数设定
best = -1
score = 0

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
		global score # 声明score是全局变量
		global best
		if self.rect.left == newWall.wallUpRect.right: # 如果水管矩形右边等于小鸟左边的x坐标
			score = score + 1 # score增加1
	def birdCrush(self):
		global keep_going
		resultU = self.rect.colliderect(newWall.wallUpRect)
		resultD = self.rect.colliderect(newWall.wallDownRect)
		if resultU or resultD or newBird.rect.bottom >= ground.rect.top:
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

		self.gap = 60 # 缝隙间隔
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

class Text(): # 显示分数
	def __init__(self,connect):
		red = (100,50,50)
		self.color = red # 为文字设置一个颜色
		# SysFont(字体名, 大小) -> Font
		self.font = pygame.font.SysFont(None,52) # 设置字体与大小
		connectStr = str(connect)
		# pygame.font.render(文字内容,是否平滑,文字颜色)
		self.image = self.font.render(connectStr,True,self.color) # 设置文本内容

	def updateText(self,connect): # 更新文字
		connectStr = str(connect)
		self.image = self.font.render(connectStr,True,self.color)

	def topupdateText(self,connect):
		connectStr = str(connect)
		self.connectStr = str(connect)
		self.font = pygame.font.SysFont(None,32)
		if keep_going == False:
			self.image = self.font.render("Best play: " + connectStr,True,self.color)

class Groud():
	def __init__(self):
		self.image = pygame.image.load("assets/ground.png")
		self.rect = self.image.get_rect()
		self.rect.bottom = 560
		self.rect.left =- 30

coolText = Text(score)
newBird = Bird()
newWall = Wall()
endText = Text("END")
ground = Groud()
bestText = Text(best)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# 直接退出循环，结束所有进程
			sys.exit()
		if keep_going:
			if (event.type == pygame.MOUSEBUTTONDOWN):
				newBird.jumpSpeed = 7
				channel_2 = pygame.mixer.Channel(2)
				fly = pygame.mixer.Sound('sound/fly.WAV')
				channel_2.play(fly)
				print(best)
		else:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					# 重置游戏参数,重新开始
					keep_going = True
					score = 0
					newBird.birdX = 50
					newBird.birdY = 100
					newWall.wallx = 288
					newBird.jumpSpeed = 7

	screen.blit(background,(0,0))
	screen.blit(newBird.birdSprites[newBird.a],newBird.rect)
	screen.blit(newWall.wallUp,newWall.wallUpRect)
	screen.blit(newWall.wallDown,newWall.wallDownRect)
	screen.blit(coolText.image,(10,10))
	screen.blit(ground.image,ground.rect)

	if score > best:
		best = score + 0
		#print(best,score)
	coolText.updateText(score)
	bestText.topupdateText(best)
	# 是否绘制分数,检测小鸟撞毁
	if keep_going:
		newWall.wallUpdate()
		newBird.birdUpdate()
		newBird.birdCrush()
	else:
		screen.blit(bestText.image,(85,265))
		screen.blit(endText.image,(110,230))

	pygame.display.update()
	clock.tick(60)

pygame.quit()
