# Flappy Bird by Bing_Fenghan
import pygame # pygame 需要手动安装
import random # random 为 python 安装自带
import sys # sys 用于快速结束程序
# 初始化与画布大小
pygame.init() # 完成初始设置
screen = pygame.display.set_mode([288,512]) # 创建指定大小的画布
# 加载背景与名称
background = pygame.image.load("assets/background.png") # 加载背景图片
pygame.display.set_caption("Flappy Bird") # 设置游戏名称
# 背景音乐
bgm = pygame.mixer.Sound('sound/bgm.wav') # 加载背景音乐
channel_1 = pygame.mixer.Channel(1) # 设置为第一层
channel_1.play(bgm) # 播放背景音乐
# 游戏开始
keep_going = True # 设置 keep_going 为 True
clock = pygame.time.Clock() # 调用帧数
# 分数设定
best = -1 # 最高分
score = 0 # 当前分值
# 小鸟
class Bird(pygame.sprite.Sprite): # 包含编写游戏对象时所需的很多功能
	def __init__(self): # 初始化
		pygame.sprite.Sprite.__init__(self) # 调用主 Sprite 类的初始化函数
		# 设置小鸟图像
		self.birdSprites=[pygame.image.load("assets/0.png"),pygame.image.load("assets/1.png"),pygame.image.load("assets/2.png")]
		self.a = 0 # 赋值变量
		self.birdX = 50 # 小鸟初始x坐标
		self.birdY = 100 # 小鸟初始y坐标
		self.jumpSpeed = 7 # 跳跃高度
		self.gravity = 0.4 # 跳跃重力
		self.rect = self.birdSprites[self.a].get_rect() # 小鸟状态并绘制矩形
		self.rect.center = (self.birdX,self.birdY) # 更新矩形
	def birdUpdate(self): # 小鸟更新
		self.jumpSpeed -= self.gravity # 小鸟速度
		self.birdY -= self.jumpSpeed # 小鸟高度
		self.rect.center = (self.birdX,self.birdY) # 更新矩形
		# 判断小鸟状态
		if self.jumpSpeed < 0: # 当y向值<0时，鸟下坠
			self.a = 1 # 小鸟状态为列表 1
		if self.jumpSpeed > 0: # 当y向值>0时，鸟上升
			self.a = 2 # 小鸟状态为列表 2
		global score # 声明 score 是全局变量
		if self.rect.left == newWall.wallUpRect.right: # 如果水管矩形右边等于小鸟左边的x坐标
			score = score + 1 # score增加1
	def birdCrush(self): # 小鸟撞击
		global keep_going # 声明 keep_going 是全局变量
		resultU = self.rect.colliderect(newWall.wallUpRect) # 调用上墙矩形检测
		resultD = self.rect.colliderect(newWall.wallDownRect) # 调用下墙矩形检测
		if resultU or resultD or newBird.rect.bottom >= ground.rect.top or newBird.rect.bottom < -1: # 矩形检测
			hit = pygame.mixer.Sound('sound/hit.wav') # 加载撞击声音
			channel_3 = pygame.mixer.Channel(3) # 设置为第三层
			channel_3.play(hit) # 播放撞击声音
			keep_going = False # 设置 keep_going 为 False
# 墙
class Wall(): # 加载水管
	def __init__(self): # 初始化
		self.wallUp = pygame.image.load("assets/bottom.png") # 加载上墙
		self.wallDown = pygame.image.load("assets/top.png") # 加载下墙
		self.wallUpRect = self.wallUp.get_rect() # 绘制上墙矩形
		self.wallDownRect = self.wallDown.get_rect() # 绘制下墙矩形
		self.gap = 45 # 缝隙间隔
		self.wallx = 288 # 墙的 x 坐标
		self.offset = random.randint(-50, 50) # 随机取 y 坐标
		self.wallUpY = 360 + self.gap - self.offset # 计算上墙 y 坐标
		self.wallDownY = 0 - self.gap - self.offset # 计算下墙 y 坐标
		self.wallUpRect.center = (self.wallx,self.wallUpY) # 更新上墙矩形
		self.wallDownRect.center = (self.wallx,self.wallDownY) # 更新下墙矩形
	def wallUpdate(self): # 墙更新
		self.wallx -= 3 # 速度 2
		self.wallUpRect.center = (self.wallx,self.wallUpY) # 更新上香矩形
		self.wallDownRect.center = (self.wallx,self.wallDownY) # 更新下墙矩形
		if self.wallx < -370: # 如果墙移出画面
			self.wallx = 360 # 重新设置墙的 x 坐标
			self.offset = random.randint(-50, 50) # 随机取 y 坐标
			self.wallUpY = 360 + self.gap - self.offset # 计算上墙 y 坐标
			self.wallDownY = 0 - self.gap - self.offset # 计算下墙 y 坐标
# 文字
class Text(): # 显示分数
	def __init__(self,connect): # 初始化
		red = (100,50,50) # 红色的RGB
		self.color = red # 为文字设置一个颜色
		# SysFont(字体名, 大小) -> Font
		self.font = pygame.font.SysFont(None,52) # 设置字体与大小
		connectStr = str(connect) # 将 connect 转换为 str
		# pygame.font.render(文字内容,是否平滑,文字颜色)
		self.image = self.font.render(connectStr,True,self.color) # 设置文本内容
	def updateText(self,connect): # 更新分数与结束标语
		connectStr = str(connect) # 将 connect 转换为 str
		self.image = self.font.render(connectStr,True,self.color) # 设置文本内容
	def topupdateText(self,connect): # 更新最高分
		connectStr = str(connect) # 将 connect 转换为 str
		self.font = pygame.font.SysFont(None,32) # 设置字体与大小
		if keep_going == False: # 如果 keep_going 为 False
			self.image = self.font.render("Best play: " + connectStr,True,self.color) # 设置文本内容
# 地板
class Groud(): # 加载地板
	def __init__(self): # 初始化
		self.image = pygame.image.load("assets/ground.png") # 加载地板
		self.rect = self.image.get_rect() # 绘制矩形
		self.rect.bottom = 560 # 矩形底部坐标
		self.rect.left =- 30 # 矩形左侧坐标
# 创建
newBird = Bird() # 创建小鸟
newWall = Wall() # 创建墙
ground = Groud() # 创建地板
endText = Text("END") # 创建结束标语
coolText = Text(score) # 创建分数
bestText = Text(best) # 创建最高分
# 主程序
while True: # 循环执行
	for event in pygame.event.get(): # 侦测事件
		if event.type == pygame.QUIT: # 确定对事件的反馈
			sys.exit() # 直接退出循环，结束所有进程
		if keep_going: # 如果 keep_going 为 true 则循环执行
			if (event.type == pygame.MOUSEBUTTONDOWN): # 鼠标按下的交互
				newBird.jumpSpeed = 7 # 设定跳跃速度为 7
				channel_2 = pygame.mixer.Channel(2) # 设置为第二层
				fly = pygame.mixer.Sound('sound/fly.WAV') # 播放飞行声音
				channel_2.play(fly) # 播放飞行声音
		else: # 否则执行
			if event.type == pygame.KEYDOWN: # 如果键盘执行任意键
				# 重置游戏参数,重新开始
				keep_going = True # 设置 Keep_going 为 True
				score = 0 # 设置分数为 0
				newBird.birdX = 50 # 设置小鸟的 x 坐标
				newBird.birdY = 100 # 设置小鸟的 y 坐标
				newBird.jumpSpeed = 7 # 设置小鸟的跳跃速度
				newWall.wallx = 288 # 设置墙的 x 坐标
	# 设置位置
	screen.blit(background,(0,0)) # 设置背景位置
	screen.blit(newBird.birdSprites[newBird.a],newBird.rect) # 设置小鸟位置
	screen.blit(newWall.wallUp,newWall.wallUpRect) # 设置上墙位置
	screen.blit(newWall.wallDown,newWall.wallDownRect) # 设置下墙位置
	screen.blit(coolText.image,(10,10)) # 设置分数位置
	screen.blit(ground.image,ground.rect) # 设置地板位置
	# 当分数大于最高分时进行更新
	if score > best: # 如果当前分数大于最高分
		best = score # 最高分为当前分数
	# 分数更新
	coolText.updateText(score) # 调用分数更新
	bestText.topupdateText(best) # 调用最高分更新
	# 是否绘制分数,检测小鸟撞毁
	if keep_going: # 如果 keep_going 为 true 则执行
		newWall.wallUpdate() # 调用墙更新
		newBird.birdUpdate() # 调用小鸟更新
		newBird.birdCrush() # 调用小鸟撞击
	else: # 否则运行
		screen.blit(bestText.image,(85,235)) # 调用结束标语
		screen.blit(endText.image,(110,200)) # 调用最高分
	# 基础类设置
	pygame.display.update() # 调用游戏更新
	clock.tick(60) # 帧数设定
pygame.quit() # 撤销初始化后的设置
