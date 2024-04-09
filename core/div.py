import pygame

font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 36)

class Div(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()

		self.game = game
		self.image = pygame.Surface((0,0), pygame.SRCALPHA)	
		self.shape = None
		self.shapeRaw = None
		self.shapeHover = None
		self.shapeHoverRaw = None
		self.rect = pygame.Rect(0, 0, 100, 100)
		self._color = (255, 255, 255)

		self.bDisplay = True

		self.bHover = False
		self._font = font
		self._text = None
		self.nPaddingTop = 10
		self.nPaddingLeft = 15
		self.arrTextPos = [0,0]

		self.shapeText = None
		self.bFitText = False
		self.bCenterText = False
		self.sTextAlign = "LEFT"
		self.centerPos = [0,0]
		self.rightX = 0

		#일단 프레임별 좌표이동, 투명도 
		self.bAnim = False
		self.nFrame = 0
		self.animList = {}
		self.sAnimCode = "NORMAL"

		return

	def set_display(self, bDisplay):
		self.bDisplay = bDisplay
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

	def color(self, color=None):
		if color is not None : 
			self._color = color
			self.render_text()
		return self._color

	def surface(self, surface=None):
		if surface is not None : 
			self.shapeRaw = surface
			self.shape = pygame.transform.scale(self.shapeRaw, (self.rect.width, self.rect.height))
		return self.shape

	def surfaceHover(self, surface=None):
		if surface is not None : 
			self.shapeHoverRaw = surface
			self.shapeHover = pygame.transform.scale(self.shapeHoverRaw, (self.rect.width, self.rect.height))
		return self.shapeHover

	def resize(self):
		if self.shape is not None : 
			self.shape = pygame.transform.scale(self.shapeRaw, (self.rect.width, self.rect.height))
		if self.shapeHover is not None : 
			self.shapeHover = pygame.transform.scale(self.shapeHoverRaw, (self.rect.width, self.rect.height))
		self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)	
		self.render_text()
		return


	def text(self, s=None):
		if s is not None :
			self._text = s
			self.render_text()
		return self._text


	def font(self, f=None):
		if f is not None :
			self._font = f
			self.render_text()
		return self._font


	def font_size(self, n=None):
		if n is not None:
			self.nFontSize = n
			font = pygame.font.Font("./font/NotoSansKR-Regular.otf", self.nFontSize)
			self.font(font)
		return self.nFontSize	

	def center_text(self, bCenterText):
		if bCenterText is not None:
			self.bCenterText = bCenterText
			# self.render_text()
			self.text_align("CENTER")
		return self.bCenterText

	def text_align(self, sTextAlign=None):
		if sTextAlign is None : return self.sTextAlign
		if sTextAlign=="CENTER" : self.sTextAlign="CENTER"
		elif sTextAlign=="RIGHT" : self.sTextAlign="RIGHT"
		else : self.sTextAlign="LEFT"
		self.render_text()
		return self.sTextAlign


	def render_text(self):
		if self._text is not None : 
			self.shapeText = self._font.render(self._text, True, self._color)
			rect = self.shapeText.get_rect()
			self.centerPos = [(self.rect.width-rect.width)/2,(self.rect.height-rect.height)/2]
			self.rightX = self.rect.width - rect.width
		return
		

	def fit_text(self, b=True):
		self.bFitText = b
		return self.bFitText

	def padding(self, n=None):
		if n is not None :
			self.padding_top(n)
			self.padding_left(n)
		return self.nPaddingTop

	def padding_left(self, n=None):
		if n is not None :
			self.nPaddingLeft = n 
		return self.nPaddingLeft

	def padding_top(self, n=None):
		if n is not None :
			self.nPaddingTop = n 
		return self.nPaddingTop


	def add_anim_absolute(self, sAnimCode, pos, nFrame=10):
		shape = {}
		shape["sType"] = "ABSOLUTE"
		shape["pos"] = [pos[0], pos[1]]
		shape["nFrame"] = nFrame
		
		if sAnimCode not in self.animList:
			self.animList[sAnimCode] = {}
			self.animList[sAnimCode]["arrShape"] = []
		self.animList[sAnimCode]["arrShape"].append(shape)

		self.animList[sAnimCode]["nFrame"] = self.connect_shape(self.animList[sAnimCode]["arrShape"]) #최종 프레임 계산.
		return
	def add_anim_relative(self, sAnimCode, pos, nFrame=10):
		shape = {}
		shape["sType"] = "RELATIVE"
		shape["pos"] = [pos[0]/nFrame, pos[1]/nFrame]
		shape["nFrame"] = nFrame

		if sAnimCode not in self.animList:
			self.animList[sAnimCode] = {}
			self.animList[sAnimCode]["arrShape"] = []
		self.animList[sAnimCode]["arrShape"].append(shape)

		self.animList[sAnimCode]["nFrame"] = self.connect_shape(self.animList[sAnimCode]["arrShape"]) #최종 프레임 계산.
		return

	def add_anim_display(self, sAnimCode, bDisplay, nFrame=10):
		shape = {}
		shape["sType"] = "DISPLAY"
		shape["bDisplay"] = bDisplay
		shape["nFrame"] = nFrame

		if sAnimCode not in self.animList:
			self.animList[sAnimCode] = {}
			self.animList[sAnimCode]["arrShape"] = []
		self.animList[sAnimCode]["arrShape"].append(shape)

		self.animList[sAnimCode]["nFrame"] = self.connect_shape(self.animList[sAnimCode]["arrShape"]) #최종 프레임 계산.
		return

	def connect_shape(self, arrShape):
		nEndFrame = 0
		if len(arrShape)==0 : return nEndFrame
		for shape in arrShape :
			nEndFrame += shape["nFrame"]
			shape["nEndFrame"] = nEndFrame
		return nEndFrame

	def start_animate(self, sAnimCode):
		self.bAnim = True
		self.sAnimCode = sAnimCode
		self.nFrame = 0
		return 

	def apply_anim(self):
		anim = self.animList[self.sAnimCode]
		self.nFrame += 1
		if self.nFrame > anim["nFrame"] : 
			self.bAnim = False
			return
		
		for i in range(0, len(anim["arrShape"])) :
			if self.nFrame <= anim["arrShape"][i]["nEndFrame"] : 
				shape = anim["arrShape"][i]
				if shape["sType"]=="RELATIVE":
					self.left(self.rect.x+shape["pos"][0])
					self.top(self.rect.y+shape["pos"][1])
				elif shape["sType"]=="ABSOLUTE":
					self.left(shape["pos"][0])
					self.top(shape["pos"][1])
				elif shape["sType"]=="DISPLAY":
					self.bDisplay = shape["bDisplay"]
				break;
		return 



	def collidepoint(self, pos):
		return self.rect.collidepoint(pos)
		
	def update(self):
		self.image.fill((0,0,0,0))

		if self.bAnim : self.apply_anim()
		if not self.bDisplay : return

		self.bHover = self.rect.collidepoint(pygame.mouse.get_pos())

		if self.bHover and self.shapeHover is not None : 
			self.image.blit(self.shapeHover, (0,0))
		elif self.shape is not None : 
			self.image.blit(self.shape, (0,0)) 

		if self.shapeText is not None : 
			if self.bFitText : self.shapeText = pygame.transform.scale(
				self._font.render(self._text, True, self._color)
				, (self.rect.width-self.nPaddingLeft*2, self.rect.height-self.nPaddingTop*2))
			

			if self.sTextAlign=="CENTER" :
				self.image.blit(self.shapeText, (self.centerPos[0]+self.arrTextPos[0], self.centerPos[1]+self.arrTextPos[1]))
			elif self.sTextAlign=="RIGHT" :
				self.image.blit(self.shapeText, (self.rightX - self.nPaddingLeft - self.arrTextPos[0], self.nPaddingTop+self.arrTextPos[1]))
			else : 
				self.image.blit(self.shapeText, (self.nPaddingLeft+self.arrTextPos[0], self.nPaddingTop+self.arrTextPos[1]))



		return

	def draw(self):
		self.game.screen.blit(self.image, self.rect)
		return