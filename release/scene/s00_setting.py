from core.scene import Scene
from core.div import Div
import pygame
from PIL import Image #pip install pillow
# import random


class Setting(Scene):
	def __init__(self, game):
		super().__init__(game, "Setting")

		self.imgBg = None
		self.groupBt = None
		self.btClose = None # 닫기 버튼 
		self.btScreen = None # 전체/창모드 버튼 
		self.btLobby = None # 로비로 이동 버튼 
		self.btExit = None # 게임 종료 버튼 
		self.btBgLeft = None # 배경음 줄이기 버튼 
		self.btBgRight = None # 배경음 키우기 버튼 
		self.btBgText = None # 배경음 수치
		self.btSeLeft = None # 효과음 줄이기 버튼 
		self.btSeRight = None # 효과음 키우기 버튼
		self.btSeText = None # 효과음 수치

		self.load()
		return 

	def load(self):
		# 배경이미지 
		self.imgBg = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)

		# 반투명 배경
		img = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)
		img.fill((0,0,0,150))
		self.imgBg.blit(img,(0,0))

		# 중앙틀 
		img = pygame.image.load("img/s01_btback.png")
		rect = img.get_rect()
		width = 400
		height = 400*rect.height/rect.width
		left = (self.game.arrWindowSize[0]-width)/2
		top = (self.game.arrWindowSize[1]-height)/2
		img = pygame.transform.smoothscale(img, (width, height))
		self.imgBg.blit(img,(left,top))

		font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 25)

		#설정 텍스트 
		img = font.render("설정", True, (255,255,255))
		rect = img.get_rect()
		self.imgBg.blit(img,( (self.game.arrWindowSize[0]-rect.width)/2, top+10))

		#배경음 텍스트
		img = font.render("배경음", True, (255,255,255))
		rect = img.get_rect()
		self.imgBg.blit(img,( left+25, top+60))

		#효과음 텍스트
		img = font.render("효과음", True, (255,255,255))
		rect = img.get_rect()
		self.imgBg.blit(img,( left+25, top+120))

		#이하 버튼
		self.groupBt = pygame.sprite.Group()
		spriteBt = pygame.image.load("img/bt.png") #157, 120(60)
		surfaceBt = spriteBt.subsurface(pygame.Rect(0, 60, 157, 60))
		surfaceBtHover = spriteBt.subsurface(pygame.Rect(0, 0, 157, 60))

		# 닫기 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(20)
		div.text("닫기")
		div.center_text(True)
		div.width(60)
		div.height(40)
		div.left(left+width-70)
		div.top(top+10)
		self.groupBt.add(div)
		self.btClose = div

		# '전체 화면으/창 모드'로 변경 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(25)
		div.text("전체 화면으로 변경")
		div.center_text(True)
		div.width(300)
		div.height(60)
		div.left(left+width/2-150)
		div.top(top+190)
		self.groupBt.add(div)
		self.btScreen = div

		# 로비로 이동 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(25)
		div.text("로비로 이동")
		div.center_text(True)
		div.width(300)
		div.height(60)
		div.left(left+width/2-150)
		div.top(top+270)
		self.groupBt.add(div)
		self.btLobby = div

		# 게임 종료 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(25)
		div.text("게임 종료")
		div.center_text(True)
		div.width(300)
		div.height(60)
		div.left(left+width/2-150)
		div.top(top+350)
		self.groupBt.add(div)
		self.btExit = div

		# 배경음 < 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(20)
		div.text("<")
		div.center_text(True)
		div.width(30)
		div.height(40)
		div.left(left+180)
		div.top(top+60)
		self.groupBt.add(div)
		self.btBgLeft = div

		# 배경음 >
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(20)
		div.text(">")
		div.center_text(True)
		div.width(30)
		div.height(40)
		div.left(left+310)
		div.top(top+60)
		self.groupBt.add(div)
		self.btBgRight = div

		# 배경음 값
		div = Div(self.game)
		div.center_text(True)
		sSize = str(int(self.game.sound_size("BG")*100))
		div.text(sSize)
		div.width(60)
		div.height(40)
		div.left(left+230)
		div.top(top+60)
		self.btBgText = div

		
		# 효과음 < 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(20)
		div.text("<")
		div.center_text(True)
		div.width(30)
		div.height(40)
		div.left(left+180)
		div.top(top+120)
		self.groupBt.add(div)
		self.btSeLeft = div

		# 효과음 >
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.font_size(20)
		div.text(">")
		div.center_text(True)
		div.width(30)
		div.height(40)
		div.left(left+310)
		div.top(top+120)
		self.groupBt.add(div)
		self.btSeRight = div

		# 효과음 값
		div = Div(self.game)
		div.center_text(True)
		sSize = str(int(self.game.sound_size("SE")*100))
		div.text(sSize)
		div.width(60)
		div.height(40)
		div.left(left+230)
		div.top(top+120)
		self.btSeText = div

		return 

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1:
				if self.btClose.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					self.game.pop_setting()

				elif self.btScreen.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					value = pygame.display.toggle_fullscreen() # -1 full, 0 window
					self.game.bToggleScreen = True
					if value==-1 : self.btScreen.text("창 모드로 변경")
					else : self.btScreen.text("전체 화면으로 변경")
					# pygame.display.set_mode((0,0), pygame.FULLSCREEN)

				elif self.btLobby.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					self.game.pop_setting()
					self.game.fade_scene("Lobby")

				elif self.btBgLeft.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					nSize = self.game.sound_size("BG",-0.05)
					self.btBgText.text(str(int(nSize*100)))

				elif self.btBgRight.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					nSize = self.game.sound_size("BG",0.05)
					self.btBgText.text(str(int(nSize*100)))

				elif self.btSeLeft.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					nSize = self.game.sound_size("SE",-0.05)
					self.btSeText.text(str(int(nSize*100)))

				elif self.btSeRight.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					nSize = self.game.sound_size("SE",0.05)
					self.btSeText.text(str(int(nSize*100)))

				elif self.btExit.collidepoint(e.pos):
					self.game.sound_play("CANCEL")
					self.game.bRunning = False 

		except Exception as e: print(e)

	def update(self):
		try:
			# 커서 변경.
			bCursor = False
			pos = pygame.mouse.get_pos()
			for div in self.groupBt :
				if div.collidepoint(pos): bCursor = True
				
			if bCursor : pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
			else : pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

			self.game.screen.blit(self.imgBg, (0, 0))

			#버튼 
			self.groupBt.update()
			self.groupBt.draw(self.game.screen)

			#기타 텍스트  
			self.btBgText.update()
			self.btBgText.draw()
			self.btSeText.update()
			self.btSeText.draw()


		except Exception as e: print(e)
	

