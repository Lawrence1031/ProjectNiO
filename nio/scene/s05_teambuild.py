from core.scene import Scene
from core.div import Div
import pygame
# from PIL import Image #pip install pillow
# import random


class Teambuild(Scene):
	def __init__(self, game):
		super().__init__(game, "Teambuild")

		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/team_bg_001.png")
		self.imgBg = pygame.transform.scale(img, self.game.arrWindowSize)


		#캐릭터 이미지 
		# img = pygame.image.load("img/ingo2.jpg")
		img = pygame.Surface((800, 800), pygame.SRCALPHA)
		img = img.subsurface(pygame.Rect(80, 0, 300, 300))
		#원형 마스크 
		mask = pygame.Surface((300, 300), pygame.SRCALPHA)
		pygame.draw.circle(mask, (255, 255, 255, 255), (150, 150), 150)
		#마스크에 그리기 
		mask.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
		#마우스 호버
		mask2 = mask.copy()
		pygame.draw.circle(mask2, (50, 50, 255, 100), (150, 150), 150, 10)

		#중앙 NPC 
		div = Div(self.game)
		div.surface(mask)
		div.surfaceHover(mask2)
		div.width(150)
		div.height(150)
		div.top(10)
		div.left(self.game.arrWindowSize[0]/2-75)
		self.npc = div



		#동료1 
		# img = pygame.image.load("img/ingo2.jpg")
		img = pygame.Surface((800, 800), pygame.SRCALPHA)
		img = img.subsurface(pygame.Rect(50, 0, 512-50, (512-50)*40/25))
		img = pygame.transform.scale(img, (250,400))

		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		#덱1 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(250)
		div.height(400)
		div.top(200)
		div.left(200)
		self.deck1 = div





		#덱2 
		# img = pygame.image.load("img/ingo2.jpg")
		img = pygame.Surface((800, 800), pygame.SRCALPHA)
		img = pygame.transform.scale(img, (250,400))
		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		#덱2 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(250)
		div.height(400)
		div.top(200)
		div.left(self.game.arrWindowSize[0]/2-125)
		self.deck2 = div





		#덱3 
		# img = pygame.image.load("img/ingo2.jpg")
		img = pygame.Surface((800, 800), pygame.SRCALPHA)
		img = img.subsurface(pygame.Rect(130, 0, 250, 400))
		img = pygame.transform.scale(img, (250,400))
		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		#덱3 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(250)
		div.height(400)
		div.top(200)
		div.right(200)
		self.deck3 = div


		#선택x
		img = pygame.Surface((1, 1), pygame.SRCALPHA)
		img2 = pygame.Surface((1, 1), pygame.SRCALPHA)
		img2.fill((100,200,200))

		#선택x
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.text("친구들과 함께하지 않는다(혼자 간다)")
		div.fit_text()
		div.width(400)
		div.height(40)
		div.bottom(30)
		div.padding_top(0)
		div.left(self.game.arrWindowSize[0]/2-200)
		self.text = div




		return 
		

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				self.game.set_scene("Stage1")

		except Exception as e: print(e)

	def update(self):
		try:
			self.game.screen.blit(self.imgBg, (0, 0))

			self.npc.update()
			self.npc.draw()
			self.deck1.update()
			self.deck1.draw()
			self.deck2.update()
			self.deck2.draw()
			self.deck3.update()
			self.deck3.draw()
			self.text.update()
			self.text.draw()

			
		except Exception as e: print(e)
	

