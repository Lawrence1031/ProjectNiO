from core.scene import Scene
from core.div import Div
import pygame
from PIL import Image #pip install pillow
# import random


class Lobby(Scene):
	def __init__(self, game):
		super().__init__(game, "Lobby")

		self.arrObject = []

		self.load()
		return 

	def load(self):
		self.img2 = pygame.image.load("img/s01_test_logo.png")
		self.imgBg = pygame.image.load("img/s02_bg.png")
		self.arrBgImg = self.load_gif("img/s02_bg.gif")
		self.load_bt()
		return 

	def load_gif(self, sFile, arrSize=None):
		frames = []
		gif_image = Image.open(sFile)
		try:
			while True:
				gif_image.seek(len(frames))
				img = gif_image.convert('RGBA')
				
				if arrSize is None : 
					frames.append(pygame.image.fromstring(
					img.tobytes(), img.size, 'RGBA'))
				else :
					frames.append(pygame.transform.scale(
					pygame.image.fromstring(
						img.tobytes(), img.size, 'RGBA'
						), arrSize))
		except EOFError:
			pass
		return frames	


	def load_bt(self):

		#반투명 배경
		# surfaceGray = pygame.Surface((1,1), pygame.SRCALPHA)
		# surfaceGray.set_alpha(70)
		# surfaceGray.fill((255, 255, 255))

		#현재 진행창
		imgprogress = pygame.image.load("img/s02_progress.png")
		div = Div(self.game)
		div.surface(imgprogress)
		rect = imgprogress.get_rect()
		div.width(rect.width)
		div.height(rect.height)
		div.bottom(150)
		div.left(0)
		self.progress = div

		#오른쪽 밑바탕 
		imgbtback = pygame.image.load("img/s01_btback.png")
		div = Div(self.game)
		div.surface(imgbtback)
		div.width(325)
		div.height(440)
		div.bottom(50)
		div.right(20)
		self.baseRight = div

		#버튼 그룹 
		self.groupBt = pygame.sprite.Group()

		#버튼 이미지 
		spriteBt = pygame.image.load("img/bt.png") #157, 120(60)
		surfaceBt = spriteBt.subsurface(pygame.Rect(0, 60, 157, 60))
		surfaceBtHover = spriteBt.subsurface(pygame.Rect(0, 0, 157, 60))

		#새로하기 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("새로하기")
		div.fit_text()
		div.width(240)
		div.height(60)
		div.top(self.baseRight.top()+50)
		div.right(60)
		div.padding_left(20)
		self.groupBt.add(div)
		self.btNewGame = div

		#이어하기 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("이어하기")
		div.fit_text()
		div.width(240)
		div.height(60)
		div.top(self.btNewGame.top()+self.btNewGame.height()+30)
		div.right(60)
		div.padding_left(20)
		self.groupBt.add(div)
		self.btContinue = div

		#설정 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("설정")
		div.fit_text()
		div.width(240)
		div.height(60)
		div.top(self.btContinue.top()+self.btContinue.height()+30)
		div.right(60)
		div.padding_left(80)
		self.groupBt.add(div)
		self.btSetting = div

		#종료 버튼 
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("종료")
		div.fit_text()
		div.width(240)
		div.height(60)
		div.top(self.btSetting.top()+self.btSetting.height()+30)
		div.right(60)
		div.padding_left(80)
		self.groupBt.add(div)
		self.btExit = div

		return

	def reset(self):
		self.game.reset_scene("Stage1")


	def get_transform_bg(self):
		nIndex = int(pygame.time.get_ticks() / (self.game.nFps*5)) % len(self.arrBgImg)

		if not hasattr(self, "_gtb_index"):
			self._gtb_index = None
			self._gtb_img = None

		if self._gtb_index!=nIndex : 
			self._gtb_index = nIndex
			self._gtb_img = pygame.transform.scale(
				self.arrBgImg[nIndex],self.game.arrWindowSize)

		return self._gtb_img

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1:
				if self.btNewGame.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					self.game.set_scene("Intro")

				elif self.btContinue.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					self.game.load_file()

				elif self.btSetting.collidepoint(e.pos):
					self.game.pop_setting()

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
			#배경 움직이는 이미지 그리기 
			self.game.screen.blit(self.get_transform_bg(), (0, 0))
			self.game.screen.blit(self.img2, (326,88))

			#오른쪽 하단 배경 
			self.baseRight.update()
			self.baseRight.draw()

			#버튼 
			self.groupBt.update()
			self.groupBt.draw(self.game.screen)

			#상황판
			self.progress.update()
			self.progress.draw()

		except Exception as e: print(e)
	

