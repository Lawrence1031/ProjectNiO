from core.scene import Scene
from core.div import Div
from core.card import Card
import pygame
import random
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)


class Cardshop(Scene):
	def __init__(self, game):
		super().__init__(game, "Cardshop")

		self.nNio = 0

		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/s13_bg.png")
		img = pygame.transform.smoothscale(img, self.game.arrWindowSize)

		#전체 반투명 배경
		surf = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)
		surf.set_alpha(90)
		surf.fill((0, 0, 0))
		img.blit(surf,(0,0))

		font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 36)
		text = font.render(" 원하는 카드를 선택해봐! ", True, (255, 255, 255), (100, 100, 100))
		img.blit(text,(200,30))

		self.imgBg = img


		#재화
		surf = pygame.Surface((1,1), pygame.SRCALPHA)
		surf.set_alpha(200)
		surf.fill((150, 0, 0))

		div = Div(self.game)
		div.surface(surf)
		div.padding(0)
		div.text_align("RIGHT")
		div.width(130)
		div.height(50)
		div.top(60)
		div.right(100)
		div.font_size(35)
		div.text(str(self.nNio)+" Nio ")
		self.nio = div


		#캐릭터 이미지 
		img = pygame.image.load("img/npc_001.png") #540 400
		img = img.subsurface(pygame.Rect(65, 0, 400, 400))
		nWidth = 300
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img, (nWidth, nHeight))
		#원형 마스크 
		mask = pygame.Surface((300, 300), pygame.SRCALPHA)
		pygame.draw.circle(mask, (255, 255, 255, 255), (150, 150), 150)
		#마스크에 그리기 
		mask.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
		#마우스 호버
		pygame.draw.circle(mask, (255, 255, 255, 200), (150, 150), 150, 10)

		#중앙 NPC 
		div = Div(self.game)
		div.surface(mask)
		div.width(150)
		div.height(150)
		div.top(10)
		div.left(30)
		self.npc = div



		#카드 574, 800
		img = self.game.cardlist.render("001")
		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		#버튼 그룹 
		self.gCard = pygame.sprite.Group()
		self.gPrice = pygame.sprite.Group()

		# 1장 : (287,400) t150 / lc-287*0.5
		# 2장 : (287,400) t150 / l250, r250 
		# 3장 : (287,400) t150 / l100, lc-287*0.5, r100
		# 4장 : (230,320) t180 / l100, l380, r380, r100 
		# 5장 : (230,320) t180 / l25, l275, lc-115, r275, r25 

		#덱1 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(230)
		div.height(320)
		div.top(180)
		div.left(25)
		div.sCode = ""
		self.gCard.add(div)
		#가격
		div = Div(self.game)
		div.surface(surf)
		div.padding(0)
		div.center_text(True)
		div.width(230)
		div.height(40)
		div.top(180+320+5)
		div.left(25)
		div.font_size(25)
		div.text("1 Nio")
		self.gPrice.add(div)


		#덱2 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(230)
		div.height(320)
		div.top(180)
		div.left(275)
		div.sCode = ""
		self.gCard.add(div)
		#가격
		div = Div(self.game)
		div.surface(surf)
		div.padding(0)
		div.center_text(True)
		div.width(230)
		div.height(40)
		div.top(180+320+5)
		div.left(275)
		div.font_size(25)
		div.text("1 Nio")
		self.gPrice.add(div)

		#덱3 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(230)
		div.height(320)
		div.top(180)
		div.right(self.game.arrWindowSize[0]/2-115)
		div.sCode = ""
		self.gCard.add(div)
		#가격
		div = Div(self.game)
		div.surface(surf)
		div.padding(0)
		div.center_text(True)
		div.width(230)
		div.height(40)
		div.top(180+320+5)
		div.right(self.game.arrWindowSize[0]/2-115)
		div.font_size(25)
		div.text("1 Nio")
		self.gPrice.add(div)

		#덱4 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(230)
		div.height(320)
		div.top(180)
		div.right(275)
		div.sCode = ""
		self.gCard.add(div)
		#가격
		div = Div(self.game)
		div.surface(surf)
		div.padding(0)
		div.center_text(True)
		div.width(230)
		div.height(40)
		div.top(180+320+5)
		div.right(275)
		div.font_size(25)
		div.text("1 Nio")
		self.gPrice.add(div)

		#덱5 
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.width(230)
		div.height(320)
		div.top(180)
		div.right(25)
		div.sCode = ""
		self.gCard.add(div)
		#가격
		div = Div(self.game)
		div.surface(surf)
		div.padding(0)
		div.center_text(True)
		div.width(230)
		div.height(40)
		div.top(180+320+5)
		div.right(25)
		div.font_size(25)
		div.text("1 Nio")
		self.gPrice.add(div)

		#선택x
		img = pygame.Surface((1, 1), pygame.SRCALPHA)
		img.fill((50,50,50))
		img2 = pygame.Surface((1, 1), pygame.SRCALPHA)
		img2.fill((100,200,200))

		#선택x
		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img2)
		div.center_text(True)
		div.width(300)
		div.height(50)
		div.bottom(60)
		div.left(self.game.arrWindowSize[0]/2-150)
		div.font_size(25)
		div.text("선택하지 않는다.( 1 Nio )")
		self.text = div


		#end_cardadd
		def fn(sCode):
			print("end_cardadd",sCode)
		self.end_cardadd = fn

		
		self.set_arr_card(["001","001","001","001","001"]) #카드 그리기.
		

		return 


	def set_arr_card(self, arrCard=[]):

		nCnt = len(arrCard)
		if nCnt==0 : return 
		for div in self.gCard : 
			div.set_display(False)
			if nCnt < 4 : 
				div.width(287)
				div.height(400)
				div.top(160)
			else :
				div.width(230)
				div.height(320)
				div.top(220)

		for div in self.gPrice : 
			div.set_display(False)
			if nCnt < 4 : 
				div.width(287)
				div.top(165+400)
			else :
				div.width(230)
				div.top(225+320)

		arrDiv = self.gCard.sprites()
		arrPrice = self.gPrice.sprites()

		if nCnt==1 : # 1장 : (287,400) t150 / lc-287*0.5
			arrDiv[0].left(self.game.arrWindowSize[0]/2-287*0.5)
			arrPrice[0].left(self.game.arrWindowSize[0]/2-287*0.5)
		elif nCnt==2 : # 2장 : (287,400) t150 / l250, r250 
			arrDiv[0].left(250)
			arrDiv[1].right(250)
			arrPrice[0].left(250)
			arrPrice[1].right(250)
		elif nCnt==3 : # 3장 : (287,400) t150 / l100, lc-287*0.5, r100
			arrDiv[0].left(100)
			arrDiv[1].right(self.game.arrWindowSize[0]/2-287*0.5)
			arrDiv[2].right(100)
			arrPrice[0].left(100)
			arrPrice[1].right(self.game.arrWindowSize[0]/2-287*0.5)
			arrPrice[2].right(100)
		elif nCnt==4 : # 4장 : (230,320) t180 / l100, l380, r380, r100 
			arrDiv[0].left(100)
			arrDiv[1].left(380)
			arrDiv[2].right(380)
			arrDiv[3].right(100)
			arrPrice[0].left(100)
			arrPrice[1].left(380)
			arrPrice[2].right(380)
			arrPrice[3].right(100)
		else : # 5장 : (230,320) t180 / l25, l275, lc-115, r275, r25 
			arrDiv[0].left(25)
			arrDiv[1].left(275)
			arrDiv[2].left(self.game.arrWindowSize[0]/2-115)
			arrDiv[3].right(275)
			arrDiv[4].right(25)
			arrPrice[0].left(25)
			arrPrice[1].left(275)
			arrPrice[2].left(self.game.arrWindowSize[0]/2-115)
			arrPrice[3].right(275)
			arrPrice[4].right(25)
		
		for i in range(0,min(len(arrCard),5)) : 
			img = self.game.cardlist.render(arrCard[i])
			img2 = img.copy()
			img_rect = img2.get_rect()
			pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)
			arrDiv[i].sCode = arrCard[i]
			arrDiv[i].surface(img)
			arrDiv[i].surfaceHover(img2)
			arrDiv[i].set_display(True)
			cardInfo = self.game.cardlist.find(arrCard[i])
			nPrice = 1
			if cardInfo.sRarity=="N" : nPrice=1
			elif cardInfo.sRarity=="A" : nPrice=3
			elif cardInfo.sRarity=="S" : nPrice=10
			arrDiv[i].nPrice = nPrice
			arrPrice[i].text(str(nPrice)+" Nio")
			arrPrice[i].set_display(True)


		return



	def load_rand_card(self):
		table = [
			["001", 10]
			, ["002", 3]
			, ["003", 6]
			, ["004", 6]
			, ["005", 3]
			, ["006", 3]
			, ["007", 3]
			, ["201", 10]
			, ["401", 6]
			, ["403", 6]
			, ["404", 3]
			, ["406", 10]
		]

		nTotal = sum(data[1] for data in table)
		arrCard = []
		while len(arrCard)<5 :
			nRand = random.randint(1, nTotal)
			sCode = None
			for data in table:
				nRand -= data[1]
				if nRand <= 0 : 
					sCode = data[0]
					break

			if sCode is None or sCode in arrCard : continue
			arrCard.append(sCode)

		self.set_arr_card(arrCard) #카드 그리기.

		self.nio.text(str(self.nNio)+" Nio ")
		
		return


	def load_cardshop(self, nNio):
		print("s13_cardshop.load_cardshop()", nNio)
		self.nNio = nNio

		self.game.arrDeck = []
		self.game.arrDiscard = []
		self.game.nTotalDamage = 0

		self.game.nRemainNio = 0
		self.game.nMonsterN = 0
		self.game.nMonsterA = 0
		self.game.nMonsterS = 0
		self.game.nMonsterEx = 0

		self.load_rand_card()

		return




	def on_click(self,sCode):
		print(sCode)

		cardInfo = self.game.cardlist.find(sCode)
		nPrice = 1
		if cardInfo.sRarity=="N" : nPrice=1
		elif cardInfo.sRarity=="A" : nPrice=3
		elif cardInfo.sRarity=="S" : nPrice=10

		if self.nNio < nPrice : return 
		self.nNio -= nPrice
		self.game.arrDeck.append(Card(self.game.cardlist.find(sCode)))

		if self.nNio < 1 : 
			self.game.set_scene("Deckselect")
			return

		self.load_rand_card()
		return 

	def none_click(self):
		print("none_click")
		self.nNio -= 1
		self.game.nRemainNio += 1

		if self.nNio < 1 : 
			self.game.set_scene("Deckselect")
			return

		self.load_rand_card()
		return

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				for div in self.gCard :
					if div.bDisplay and div.collidepoint(e.pos) :
						self.game.sound_play("CURSOR")
						return self.on_click(div.sCode)
				if self.text.collidepoint(e.pos) : 
					self.game.sound_play("CURSOR")
					return self.none_click()
		except Exception as e: print(e)

	def update(self):
		try:
			pos = pygame.mouse.get_pos()

			# 커서 변경.
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

			for div in self.gCard :
				if div.bDisplay and div.collidepoint(pos) :
					pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
					break;
			if self.text.collidepoint(pos) : 
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


			self.game.screen.blit(self.imgBg, (0, 0))

			self.nio.update()
			self.nio.draw()

			self.npc.update()
			self.npc.draw()


			self.gCard.update()
			self.gCard.draw(self.game.screen)

			self.gPrice.update()
			self.gPrice.draw(self.game.screen)

			self.text.update()
			self.text.draw()

		except Exception as e: print(e)
	




















