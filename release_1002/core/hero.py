import pygame

class Hero(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()

		self.game = game
		self.image = None
		self.rect = pygame.Rect(0, 0, 0, 0) #x, y만 사용하고, 그게 캐릭터 정중앙.

		self.nFrame = 0
		self.animList = {}
		self.sAnimCode = "NORMAL"
		
		self.load_anim()
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




	def load_anim(self):

		#기본 애니메이션 테스트 
		sprite = pygame.image.load("img/hero_001_001.png") #210x130
		width = 210
		height = 130
		anim = {}
		anim["arrShape"] = []

		img = sprite.subsurface(pygame.Rect(width*0, 0, width, height))
		shape = self.build_shape(img, (0,0), (width,height))
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*1, 0, width, height))
		shape = self.build_shape(img, (0,0), (width,height))
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*2, 0, width, height))
		shape = self.build_shape(img, (0,0), (width,height))
		anim["arrShape"].append(shape)

		shape = self.copy_shape(anim["arrShape"][1]) #1번 한번더 추가.
		anim["arrShape"].append(shape)

		shape = self.copy_shape(anim["arrShape"][0]) #0번 한번더 추가.
		anim["arrShape"].append(shape)

		anim["nFrame"] = self.connect_shape(anim["arrShape"]) #최종 프레임 계산.
		self.animList["NORMAL"] = anim


		#공격 애니메이션
		offset = height + 40
		anim = {}
		anim["arrShape"] = []

		img = sprite.subsurface(pygame.Rect(width*0, offset, width, height))
		shape = self.build_shape(img, (0,0), (width, height), 3)
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*1, offset, width, height))
		shape = self.build_shape(img, (0,0), (width, height), 3)
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*2, offset, width, height))
		shape = self.build_shape(img, (0,0), (width, height), 3)
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*3, offset, width, height))
		shape = self.build_shape(img, (0,0), (width, height), 3)
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*4, offset, width, height))
		shape = self.build_shape(img, (0,0), (width, height), 3)
		anim["arrShape"].append(shape)

		img = sprite.subsurface(pygame.Rect(width*5, offset, width, height))
		shape = self.build_shape(img, (0,0), (width, height), 3)
		anim["arrShape"].append(shape)

		shape = self.copy_shape(anim["arrShape"][1]) #1번 한번더 추가.
		anim["arrShape"].append(shape)
		
		shape = self.copy_shape(anim["arrShape"][0]) #1번 한번더 추가.
		anim["arrShape"].append(shape)

		anim["nFrame"] = self.connect_shape(anim["arrShape"]) #최종 프레임 계산.
		self.animList["ATTACT"] = anim


		#공격 당하는 애니메이션 
		anim = {}
		anim["arrShape"] = []

		img = sprite.subsurface(pygame.Rect(0, 0, width, height)).convert_alpha().copy()
		img2 = pygame.Surface((width,height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		shape = self.build_shape(img, (0,0), (width,height), 10) # 0번째 
		anim["arrShape"].append(shape)

		img = img.copy()
		img2 = pygame.Surface((width,height), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		shape = self.build_shape(img2, (-1,0), (width,height), 5) # 1
		anim["arrShape"].append(shape)

		shape = self.copy_shape(anim["arrShape"][0], (1,0), 3) #1번 한번더 추가.
		anim["arrShape"].append(shape)

		shape = self.copy_shape(anim["arrShape"][1], (0,0), 3) #1번 한번더 추가.
		anim["arrShape"].append(shape)

		shape = self.copy_shape(anim["arrShape"][0], nFrame=1) #1번 한번더 추가.
		anim["arrShape"].append(shape)

		anim["nFrame"] = self.connect_shape(anim["arrShape"]) #최종 프레임 계산.
		self.animList["DAMAGE"] = anim


		return 

	def build_shape(self, surface, pos=(0,0), size=(100,100), nFrame=10):
		shape = {}
		shape["img"] = pygame.transform.smoothscale(surface.convert_alpha(), size)
		shape["rect"] = pygame.Rect(pos[0],pos[1], size[0],size[1])
		shape["pos"] = [pos[0]-size[0]/2, pos[1]-size[1]/2]
		shape["nFrame"] = nFrame
		return shape

	def copy_shape(self, shape, pos=None, nFrame=None):
		sp = {}
		sp["img"] = shape["img"].copy()
		sp["rect"] = pygame.Rect(shape["rect"].x,shape["rect"].y, shape["rect"].width,shape["rect"].height)
		if pos is None :
			sp["pos"] = [ shape["pos"][0], shape["pos"][1] ]
		else :
			sp["pos"] = [pos[0]-shape["rect"].width/2, pos[1]-shape["rect"].height/2]

		if nFrame is None : sp["nFrame"] = shape["nFrame"]
		else : sp["nFrame"] = nFrame
		return sp


	def connect_shape(self, arrShape):
		nEndFrame = 0
		if len(arrShape)==0 : return nEndFrame
		for shape in arrShape :
			nEndFrame += shape["nFrame"]
			shape["nEndFrame"] = nEndFrame
		return nEndFrame


	def start_animate(self, sAnimCode):
		self.sAnimCode = sAnimCode
		self.nFrame = 0
		return 


	def update(self):
		anim = self.animList[self.sAnimCode]

		self.nFrame += 1
		if self.nFrame > anim["nFrame"] :
			self.nFrame = 0
			self.sAnimCode = "NORMAL"
			#기본 애니메이션으로 변경.
			#애니메이션 종료 이벤트 호출 

		shape = None
		for i in range(0, len(anim["arrShape"])) :
			if self.nFrame <= anim["arrShape"][i]["nEndFrame"] : 
				shape = anim["arrShape"][i]
				break;

		if shape is None : return 

		self.image = shape["img"]
		self.subPos = shape["pos"]

		return

	def draw(self):

		self.game.screen.blit(self.image, (self.rect.x + self.subPos[0], self.rect.y + self.subPos[1]))
		return