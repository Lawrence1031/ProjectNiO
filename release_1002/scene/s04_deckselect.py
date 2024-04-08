from core.scene import Scene
from core.div import Div
from core.card import Card
import pygame
# from PIL import Image #pip install pillow
# import random


class Deckselect(Scene):
	def __init__(self, game):
		super().__init__(game, "Deckselect")

		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/deck_bg_001.png")
		self.imgBg = pygame.transform.scale(img, self.game.arrWindowSize)


		#캐릭터 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = img.subsurface(pygame.Rect(115, 30, 300, 300))
		#원형 마스크 
		mask = pygame.Surface((300, 300), pygame.SRCALPHA)
		pygame.draw.circle(mask, (255, 255, 255, 255), (150, 150), 150)
		#마스크에 그리기 
		mask.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
		#마우스 호버
		# mask2 = mask.copy()
		# pygame.draw.circle(mask2, (50, 50, 255, 100), (150, 150), 150, 10)

		#중앙 NPC 
		div = Div(self.game)
		div.surface(mask)
		# div.surfaceHover(mask2)
		div.width(150)
		div.height(150)
		div.top(10)
		div.left(self.game.arrWindowSize[0]/2-75)
		self.npc = div


		#덱1 
		img = pygame.image.load("img/deck_type_01.png")
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
		img = pygame.image.load("img/deck_type_02.png")
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
		img = pygame.image.load("img/deck_type_03.png")
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
		div.text("덱을 선택하지 않는다(무기를 선택하지 않는다)")
		div.fit_text()
		div.width(600)
		div.height(40)
		div.bottom(30)
		div.padding_top(0)
		div.left(self.game.arrWindowSize[0]/2-300)
		self.text = div



		return 



	def on_mouse_button_down(self, e):
		try:
			self.game.reset_scene("Stage1")
			if e.button == 1: 
				if ( self.deck1.collidepoint(e.pos) 
					or self.deck2.collidepoint(e.pos)
					or self.deck3.collidepoint(e.pos)
					or self.text.collidepoint(e.pos) ) :
					self.game.sound_play("CURSOR")

					if self.deck1.collidepoint(e.pos) : #공격 
						self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("406")))
					elif self.deck2.collidepoint(e.pos) : #수비
						self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("406")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("406")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("406")))
					elif self.deck3.collidepoint(e.pos) : #지원
						self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("406")))
						self.game.arrDeck.append(Card(self.game.cardlist.find("406")))
					elif self.text.collidepoint(e.pos) : #선택안함.
						self.game.nRemainNio += 4

					self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
					self.game.arrDeck.append(Card(self.game.cardlist.find("001")))
					self.game.arrDeck.append(Card(self.game.cardlist.find("404")))
					self.game.arrDeck.append(Card(self.game.cardlist.find("406")))

					self.game.arrDiscard = []
					self.game.fade_scene("Stage1")
					self.game.save_file()

		except Exception as e: print(e)

	def update(self):
		try:
			pos = pygame.mouse.get_pos()

			# 커서 변경.
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			if ( self.deck1.collidepoint(pos) 
				or self.deck2.collidepoint(pos) 
				or self.deck3.collidepoint(pos) 
				or self.text.collidepoint(pos)
				): pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


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
	

