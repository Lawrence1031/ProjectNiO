import pygame
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)

# hp바 
img = pygame.image.load("img/s08_bar_gy.png") 
IMG_HP_GRAY = pygame.transform.smoothscale(img, (150, 15))
img = pygame.image.load("img/s08_bar_gn.png") 
IMG_HP_GREEN = pygame.transform.smoothscale(img, (150, 15))
img = pygame.Surface((1,1), pygame.SRCALPHA)
img.fill((30,30,30,130))
IMG_HP_TEXT = img
FONT_HP = pygame.font.Font("./font/NotoSansKR-Regular.otf", 15)
FONT_HP.set_bold(True)

# 실드
img = pygame.image.load("img/s08_shield_1.png")
IMG_SHIELD = pygame.transform.smoothscale(img, (56, 87))
FONT_SHIELD = pygame.font.Font("./font/NotoSansKR-Regular.otf", 36)

# 텍스트
FONT_TEXT = pygame.font.Font("./font/NotoSansKR-Regular.otf", 20)

class Monster(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.nPadding = 200
		self.image = pygame.Surface((100+self.nPadding*2, 100+self.nPadding*2), pygame.SRCALPHA)
		self.rect = pygame.Rect(0, 0, 0, 0) #x, y만 사용하고, 그게 캐릭터 정중앙.
		self.bDisplay = False

		self.nFrame = 9999
		self.sAnimCode = "NORMAL"
		self.subPos = [0,0]	
		self.shapeText = None

		# monsterinfo
		self.monsterinfo = None
		self.sType = None
		self.sRarity = None
		self.nAD = 0
		self.nAP = 0
		self.nHpMax = 10
		self.nHp = 10
		self.nShield = 0
		self.animList = {}
		self.arrMessage = []
		self.nStep = 0
		self.nSubStep = 0

		# hp바 
		self.imgHp = pygame.Surface((150, 15), pygame.SRCALPHA)

		# 쉴드 
		self.imgShield = pygame.Surface((56, 87), pygame.SRCALPHA)
		self.bShield = True

		# 텍스트 
		self.imgText = pygame.Surface((300, 30), pygame.SRCALPHA)
		self.nFrameText = 9999

		#머리좌표
		self.posHead = (0,0)
		return

	def left(self, n=None):
		if n is not None : 
			self.rect.x = n
			self.nRight = self.game.arrWindowSize[0] - self.rect.x
		return self.rect.x

	def right(self, n=None):
		if n is not None : 
			self.nRight = n 
			self.rect.x = self.game.arrWindowSize[0] - self.nRight
		return self.nRight

	def top(self, n=None):
		if n is not None :
			self.rect.y = n 
			self.nBottom = self.game.arrWindowSize[1] - self.rect.y
		return self.rect.y

	def bottom(self, n=None):
		if n is not None :
			self.nBottom = n 
			self.rect.y = self.game.arrWindowSize[1] - self.nBottom
		return self.nBottom

	def set_monster_info(self, monsterinfo):
		self.monsterinfo = monsterinfo 
		self.sType = monsterinfo.sType
		self.sRarity = monsterinfo.sRarity
		self.nAD = monsterinfo.nAD
		self.nAP = monsterinfo.nAP
		self.nHpMax = monsterinfo.nHp
		self.nHp = monsterinfo.nHp
		self.animList = monsterinfo.animList
		self.arrMessage = monsterinfo.arrMessage

		self.nShield = 0
		self.nStep = 0
		self.nSubStep = 0

		self.nFrame = 9999
		self.nFrameText = 9999
		self.bDisplay = True
		self.update_status_img()
		return

	def start_animate(self, sAnimCode):
		self.sAnimCode = sAnimCode
		self.nFrame = 0
		return 

	def add_damage(self, nDamage):
		if self.nShield >= nDamage :
			self.nShield -= nDamage
		else :
			nDamage -= self.nShield 
			self.nShield = 0
			self.game.sound_play("SHIELD_DESTROYED")

		self.nHp = max(0, self.nHp-nDamage)
		if self.nHp <= 0 : self.game.sound_play("ENEMY_DESTROYED")

		if nDamage!=0 : self.set_text(str(-nDamage))
		self.update_status_img()
		return

	def update_status_img(self):
		self.update_hp()
		self.update_shield()
		return 

	def update_hp(self):
		self.imgHp.fill((0,0,0,0))
		self.imgHp.blit(IMG_HP_GRAY,(0,0))

		nWidth = 5+max(rd(145*self.nHp/self.nHpMax),0)
		bar = pygame.transform.smoothscale(IMG_HP_GREEN.copy(), (nWidth, 15))
		self.imgHp.blit(bar,(0,0))

		shapeText = FONT_HP.render(f" {self.nHp}/{self.nHpMax} ", True, (255, 255, 255))
		rect = shapeText.get_rect()
		img = pygame.transform.smoothscale(IMG_HP_TEXT.copy(), (rect.width, rect.height))
		self.imgHp.blit(img,(75-rect.width/2,-5))
		self.imgHp.blit(shapeText,(75-rect.width/2,-5))
		return 

	def update_shield(self):
		self.bShield = False
		if self.nShield > 0 : self.bShield = True

		self.imgShield.fill((0,0,0,0))
		self.imgShield.blit(IMG_SHIELD, (0,0))

		shapeText = FONT_SHIELD.render(f" {self.nShield} ", True, (255, 255, 255))
		rect = shapeText.get_rect()

		self.imgShield.blit(shapeText, (27-rect.width/2, 38-rect.height/2))
		return 

	def set_text(self, s):
		self.imgText.fill((0,0,0,0))
		shapeText = FONT_TEXT.render(s, True, (255,46,99))
		rect = shapeText.get_rect()

		self.imgText.blit(shapeText, (50-rect.width/2,15-rect.height/2))
		self.nFrameText = 0
		return	
	
	def update(self):
		self.image.fill((0,0,0,0))

		if self.sAnimCode not in self.animList: return

		anim = self.animList[self.sAnimCode]

		self.nFrame += 1
		if self.nFrame > anim["nFrame"] :
			self.nFrame = 0
			self.sAnimCode = "NORMAL"

		if not self.bDisplay : return 

		shape = None
		for i in range(0, len(anim["arrShape"])) :
			if self.nFrame <= anim["arrShape"][i]["nEndFrame"] : 
				shape = anim["arrShape"][i]
				break;

		if shape is None : return 

		self.image.blit(shape["img"], (self.nPadding+shape["offset"][0], self.nPadding+shape["offset"][1]))
		self.subPos = shape["pos"]
		self.posHead = (self.rect.x + self.subPos[0] + self.nPadding+shape["offset"][0]+shape["rect"].width/2
			, self.rect.y + self.subPos[1]+self.nPadding+shape["offset"][1]-60)

		#hp
		self.update_hp()
		self.image.blit(self.imgHp, (self.nPadding+shape["offset"][0]-75+shape["rect"].width/2, self.nPadding+shape["offset"][1]-25))

		#실드
		self.update_shield()
		if self.bShield : 
			self.image.blit(self.imgShield, (self.nPadding+shape["offset"][0]-70, self.nPadding+shape["offset"][1]-44+shape["rect"].height/2))

		#텍스트
		self.nFrameText = min(self.nFrameText+1, 60)
		if self.nFrameText < 30 :
			self.image.blit(self.imgText, (self.nPadding+shape["offset"][0]-50+shape["rect"].width/2, self.nPadding+shape["offset"][1]-60))
		elif self.nFrameText < 60 :
			self.image.blit(self.imgText, (self.nPadding+shape["offset"][0]-50+shape["rect"].width/2, self.nPadding+shape["offset"][1]-30-self.nFrameText))

		return

	def draw(self):
		self.game.screen.blit(self.image, (self.rect.x + self.subPos[0], self.rect.y + self.subPos[1]))
		return




