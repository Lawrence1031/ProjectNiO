import pygame
from core.scene import Scene

font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 15)
MAP_PLACE_NAME = None

class Place(pygame.sprite.Sprite):
	def __init__(self, scene, sName, map, x, y):
		super().__init__()
		self.scene = scene
		self.game = scene.game

		self.sName = sName
		self.map = map
		self.sType = "NORMAL" #NORMAL, BASE, WARNING, EVENT1, EVENT2
		self.sStatus = "NORMAL" #NORMAL, OPEN, CLOSE, NONE
		self.bVisited = False

		self.image = None
		self.rect = pygame.Rect(x, y, 50, 50)
		self.bHover = False

		if MAP_PLACE_NAME is None : 
			self.load_name_file()

		#장소는 원으로 그릴듯. 

		#모양 종류
		# 0. 내 위치 녹색 
		# 1. base 하늘색 
		# 2. 갈수있음. 흰색
		# 3. 갈수 없음 회색
		# 4. 보스 : 빨간색
		# 마우스 호버 테두리가 연파랑 
		#총 10개 

		#폰트 및 글자
		sLabel = MAP_PLACE_NAME.get(self.sName,self.sName)
		def add_text_shape(shape):
			shapeText = font.render(f" {sLabel} ", True, (255, 255, 255), ((51, 51, 51)))
			shape.blit(shapeText, (5, 53))
			return shape

		self.shapes = {}
		shape = pygame.Surface((200, 80), pygame.SRCALPHA)
		
		#안보임.
		pygame.draw.circle(shape, (0, 0, 0, 0), (0, 0), 0)
		self.shapes["NONE"] = shape.copy()

		#내위치 녹색
		pygame.draw.circle(shape, (191, 253, 159, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["STAYING"] = shape.copy()
		pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["STAYING_HOVER"] = add_text_shape(shape.copy())

		#base위치 하늘색
		pygame.draw.circle(shape, (153, 222, 230, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["BASE"] = shape.copy()
		pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["BASE_HOVER"] = add_text_shape(shape.copy())

		#이동가능 흰색
		pygame.draw.circle(shape, (255, 255, 255, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["MOVABLE"] = shape.copy()
		pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["MOVABLE_HOVER"] = add_text_shape(shape.copy())

		#이동불가 회색
		pygame.draw.circle(shape, (120, 122, 145, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["DISABLE"] = shape.copy()
		# pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["DISABLE_HOVER"] = add_text_shape(shape.copy())

		#보스 빨강 
		pygame.draw.circle(shape, (128, 0, 0, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["WARNING"] = shape.copy()
		pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["WARNING_HOVER"] = add_text_shape(shape.copy())

		#이벤트 금색 
		pygame.draw.circle(shape, (128,128,0, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["EVENT1"] = shape.copy()
		pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["EVENT1_HOVER"] = add_text_shape(shape.copy())

		#이벤트2 청록색 
		pygame.draw.circle(shape, (0,255,255, 255), (25, 25), 25)
		pygame.draw.circle(shape, (0, 0, 0, 255), (25, 25), 25, 4)
		self.shapes["EVENT2"] = shape.copy()
		pygame.draw.circle(shape, (50, 50, 255, 100), (25, 25), 25, 4) #호버 
		self.shapes["EVENT2_HOVER"] = add_text_shape(shape.copy())

		self.left(x)
		self.top(y)
		return


	def cal(self): 
		self.cal_x()
		self.cal_y()
		return

	def cal_x(self):
		self.nRight = self.game.arrWindowSize[0] - self.rect.x - self.rect.width 
		self.nX = self.rect.x + self.rect.width/2
		return

	def cal_y(self):
		self.nBottom = self.game.arrWindowSize[1] - self.rect.y - self.rect.height
		self.nY = self.rect.y + self.rect.height/2
		return

	def left(self, n=None):
		if n is not None : 
			self.rect.x = n
			self.nRight = self.game.arrWindowSize[0] - self.rect.x - self.rect.width 
			self.nX = self.rect.x + self.rect.width/2
		return self.rect.x

	def right(self, n=None):
		if n is not None : 
			self.nRight = n 
			self.rect.x = self.game.arrWindowSize[0] - self.nRight - self.rect.width
			self.nX = self.rect.x + self.rect.width/2
		return self.nRight

	def x(self, n=None):
		if n is not None : 
			self.nX = n 
			self.rect.x = self.nX - self.rect.width/2 
			self.nRight = self.game.arrWindowSize[0] - self.rect.x - self.rect.width 
		return self.nX

	def top(self, n=None):
		if n is not None :
			self.rect.y = n 
			self.nBottom = self.game.arrWindowSize[1] - self.rect.y - self.rect.height
			self.nY = self.rect.y + self.rect.height/2
		return self.rect.y

	def bottom(self, n=None):
		if n is not None :
			self.nBottom = n 
			self.rect.y = self.game.arrWindowSize[1] - self.nBottom - self.rect.height
			self.nY = self.rect.y + self.rect.height/2
		return self.nBottom

	def y(self, n=None):
		if n is not None : 
			self.nY = n 
			self.rect.y = self.nY - self.rect.height/2
			self.nBottom = self.game.arrWindowSize[1] - self.rect.y - self.rect.height
		return self.nY 


	def width(self, n=None):
		if n is not None :
			self.rect.width = n 
			self.resize()
			self.cal_x()
		return self.rect.width

	def height(self, n=None):
		if n is not None :
			self.rect.height = n 
			self.resize()
			self.cal_y()
		return self.rect.height

	def resize(self):
		for k in self.shapes:
			try:
				self.shapes[k] = pygame.transform.scale(self.shapes[k], (self.rect.width, self.rect.height))
			except Exception as e: print(e)

		return


	def collidepoint(self, pos):
		return ( (self.rect.center[0] - pos[0])**2 + (self.rect.center[1] - pos[1])**2 <= (self.rect.width/2)**2 )


	def load_name_file(self):
		global MAP_PLACE_NAME
		MAP_PLACE_NAME = {}
		with open("./lang/place_"+self.game.sLangCode+".txt", "r", encoding="utf8") as file:
			for sLine in file:
				kv = sLine.strip().split(maxsplit=1)
				if len(kv)>1 :
					MAP_PLACE_NAME[kv[0]] = kv[1]
		return 

	def type(self, s=None):
		if s is not None : 
			self.sType = s 
		return self.sType

	def status(self, s=None):
		if s is not None : 
			self.sStatus = s 
		return self.sStatus

	def check_movable(self):
		bMoving = True
		if self.sStatus == "NONE" or self.sStatus == "CLOSE" :
			bMoving = False
		return (self.scene.location==self.sName or self.scene.location in self.map) and bMoving

		
	def update(self):
		self.bHover = self.collidepoint(pygame.mouse.get_pos())

		bMoving = False
		#현재 위치인가. 
		if self.scene.location == self.sName : 
			self.image = self.shapes["STAYING"]
			if self.bHover  : self.image = self.shapes["STAYING_HOVER"]
			return
		
		#이어진 위치인가. 
		bMoving = self.check_movable()

		#상태 NORMAL, OPEN, CLOSE, NONE
		if self.sStatus == "NONE" : #안보임.
			self.image = self.shapes["NONE"]
			bMoving = False
			return
		elif self.sStatus == "OPEN" : #갈수있음.
			bMoving = True
		elif self.sStatus == "CLOSE" : #못감.
			bMoving = False

		#특수장소 먼저 체크하고, 아니면 갈수있는지 체크.
		if self.sType == "BASE" : 
			if self.bHover and bMoving : self.image = self.shapes["BASE_HOVER"]
			else : self.image = self.shapes["BASE"]
		elif self.sType == "WARNING" : 
			if self.bHover and bMoving : self.image = self.shapes["WARNING_HOVER"]
			else : self.image = self.shapes["WARNING"]
		elif self.sType == "EVENT1" : 
			if self.bHover and bMoving : self.image = self.shapes["EVENT1_HOVER"]
			else : self.image = self.shapes["EVENT1"]
		elif self.sType == "EVENT2" : 
			if self.bHover and bMoving : self.image = self.shapes["EVENT2_HOVER"]
			else : self.image = self.shapes["EVENT2"]
		elif bMoving : 
			if self.bHover : self.image = self.shapes["MOVABLE_HOVER"]
			else : self.image = self.shapes["MOVABLE"]
		else : 
			if self.bHover : self.image = self.shapes["DISABLE_HOVER"]
			else : self.image = self.shapes["DISABLE"]
		


		return

	def draw(self):
		self.game.screen.blit(self.image, self.rect)
		return



