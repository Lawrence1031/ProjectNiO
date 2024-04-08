import pygame

class Dialog(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()

		self.game = game
		self.image = None
		self.shape = None
		self.shapeRaw = None
		self.rectOneChar = None
		self.shapeLast = None
		self.shapeLastDot = None
		self.nDotTime = 0

		self.arrText = []
		self.arrTyping = []

		self.nPaddingTop = 10
		self.nPaddingLeft = 15
		self._color = (255, 255, 255)

		self.rect = pygame.Rect(0, 0, 100, 100)

		self._font = None
		self.nFontSize = 50
		self.sFontPath = "./font/NotoSansKR-Regular.otf"

		#반투명 배경
		surfaceGray = pygame.Surface((1,1), pygame.SRCALPHA)
		surfaceGray.set_alpha(150)
		surfaceGray.fill((0, 0, 0))
		self.surface(surfaceGray)

		font = pygame.font.Font(self.sFontPath, self.nFontSize)
		self.font(font)
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
		return self._color

	def surface(self, surface=None):
		if surface is not None : 
			self.shapeRaw = surface
			self.shape = pygame.transform.scale(self.shapeRaw, (self.rect.width, self.rect.height))
		return self.shape

	def resize(self):
		if self.shape is not None : 
			self.shape = pygame.transform.scale(self.shapeRaw, (self.rect.width, self.rect.height))
		return

	def font(self, f=None):
		if f is not None :
			self._font = f

		self.rectOneChar = self._font.render("  ", True, (255, 255, 255)).get_rect()
		return self._font

	def font_size(self, n=None):
		if n is not None:
			self.nFontSize = n
			font = pygame.font.Font(self.sFontPath, self.nFontSize)
			self.font(font)
		return self.nFontSize			

	def add_text(self, s):
		self.image = None
		while len(self.arrTyping)!=0 :
			self.text_typing()
		self.arrText.append(s)
		return

	def add_typing(self, s):
		self.image = None
		if len(self.arrTyping)==0 :
			self.arrTyping.append("")
		self.arrTyping.append(s)
		return

	def end_typing(self):
		self.image = None
		while len(self.arrTyping)!=0 :
			self.text_typing()
		return

	def clear_text(self):
		self.image = None
		self.arrText = []
		self.arrTyping = []
		return

	def text_typing(self):
		if len(self.arrTyping)==0 : return False
		if self.arrTyping[0]=="" : 
			self.arrTyping.pop(0)
			if 1<=len(self.arrTyping) :
				self.arrText.append("")
				return self.text_typing()
		else :
			if len(self.arrText)==0 : self.arrText.append("")
			self.arrText[-1] += self.arrTyping[0][0]
			self.arrTyping[0] = self.arrTyping[0][1:]
		return True

	def padding_left(self, n=None):
		if n is not None :
			self.nPaddingLeft = n 
		return self.nPaddingLeft

	def padding_top(self, n=None):
		if n is not None :
			self.nPaddingTop = n 
		return self.nPaddingTop

	def update(self):
		if self.shapeLast is None and len(self.arrText)==0:
			self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
			self.shapeLast = self.image
			self.shapeLastDot = self.image

		bTyping = self.text_typing()
		
		if bTyping==False and self.image is not None : 
			self.nDotTime += 1 # 0~10 dot, 11~20 no dot 
			if self.nDotTime < self.game.nFps :
				self.image = self.shapeLastDot
			elif self.nDotTime < self.game.nFps*2 :
				self.image = self.shapeLast
			else : self.nDotTime = 0
			return

		self.shapeLast = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
		self.shapeLast.blit(self.shape, (0,0))

		shapeText = None
		nTextWidth = self.rect.width-self.nPaddingLeft*2
		nTextHeight = self.rect.height-self.nPaddingTop*2

		arrShape = []
		text = None
		shape = None
		for i in range(len(self.arrText)):
			text = self.arrText[i]
			shape = self._font.render(text, True, self._color)
			if nTextWidth < shape.get_rect().width :
				shape = None
				shapeLast = None

				j = 0
				while len(text)!=0 :
					shape = self._font.render(text[0:j], True, self._color)
					if nTextWidth < shape.get_rect().width :
						arrShape.append(shapeLast)
						text = text[j-1:]
						j = 0
					elif j >= len(text) : 
						arrShape.append(shape)
						break
					else :
						shapeLast = shape
						j+=1

			else :
				arrShape.append(shape)
		
		nLine = len(arrShape)
		if nLine > 0 :
			nLineHeight = arrShape[0].get_rect().height
			base = pygame.Surface((nTextWidth, nLine*nLineHeight), pygame.SRCALPHA)
			for i in range(len(arrShape)):
				base.blit(arrShape[i], (0, i*nLineHeight))

			nY = max(0,nLine*nLineHeight-nTextHeight)
			nHeight = min(nLine*nLineHeight,nTextHeight)
			shapeText = base.subsurface(pygame.Rect(0, nY, nTextWidth, nHeight))	
			self.shapeLast.blit(shapeText, (self.nPaddingLeft, self.nPaddingTop))

			self.shapeLastDot = self.shapeLast.copy()

			shapeDot = pygame.Surface((nLineHeight/4, nLineHeight/2))
			shapeDot.fill(self._color)

			nDotX = self.nPaddingLeft + arrShape[-1].get_rect().width + 5
			nDotY = nHeight - nLineHeight/2
			self.shapeLastDot.blit(shapeDot, (nDotX, nDotY))

		self.image = self.shapeLastDot

	def draw(self):
		self.game.screen.blit(self.image, self.rect)
		return