from core.scene import Scene
from core.div import Div
from core.card import Card
import pygame
import random


class Cardadd(Scene):
	def __init__(self, game):
		super().__init__(game, "Cardadd")
		self.arrCard = []
		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/deck_bg_001.png")
		self.imgBg = pygame.transform.scale(img, self.game.arrWindowSize)

		#카드 574, 800
		img = self.game.cardlist.render("001")
		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		#버튼 그룹 
		self.gCard = pygame.sprite.Group()

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

		#선택x
		img = pygame.Surface((1, 1), pygame.SRCALPHA)
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
		div.text("선택하지 않는다")
		self.text = div


		#end_cardadd
		def fn(sCode):
			print("end_cardadd",sCode)
		self.end_cardadd = fn


		return 


	def set_arr_card(self, arrCard=[]):
		self.arrCard = arrCard
		nCnt = len(arrCard)
		if nCnt==0 : return 
		for div in self.gCard : 
			div.set_display(False)
			if nCnt < 4 : 
				div.width(287)
				div.height(400)
				div.top(150)
			else :
				div.width(230)
				div.height(320)
				div.top(180)

		arrDiv = self.gCard.sprites()

		if nCnt==1 : # 1장 : (287,400) t150 / lc-287*0.5
			arrDiv[0].left(self.game.arrWindowSize[0]/2-287*0.5)
		elif nCnt==2 : # 2장 : (287,400) t150 / l250, r250 
			arrDiv[0].left(250)
			arrDiv[1].right(250)
		elif nCnt==3 : # 3장 : (287,400) t150 / l100, lc-287*0.5, r100
			arrDiv[0].left(100)
			arrDiv[1].right(self.game.arrWindowSize[0]/2-287*0.5)
			arrDiv[2].right(100)
		elif nCnt==4 : # 4장 : (230,320) t180 / l100, l380, r380, r100 
			arrDiv[0].left(100)
			arrDiv[1].left(380)
			arrDiv[2].right(380)
			arrDiv[3].right(100)
		else : # 5장 : (230,320) t180 / l25, l275, lc-115, r275, r25 
			arrDiv[0].left(25)
			arrDiv[1].left(275)
			arrDiv[2].left(self.game.arrWindowSize[0]/2-115)
			arrDiv[3].right(275)
			arrDiv[4].right(25)
		

		nMaxNio = 0
		for i in range(0,min(len(arrCard),5)) : 
			img = self.game.cardlist.render(arrCard[i])
			img2 = img.copy()
			img_rect = img2.get_rect()
			pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)
			arrDiv[i].sCode = arrCard[i]
			arrDiv[i].surface(img)
			arrDiv[i].surfaceHover(img2)
			arrDiv[i].set_display(True)

			cardInfo = self.game.cardlist.find("002")
			nNio = 1
			if cardInfo.sRarity == "A" : nNio = 3
			elif cardInfo.sRarity == "S" : nNio = 10
			if nMaxNio < nNio : nMaxNio = nNio

		self.nMaxNio = nMaxNio
		return


	def on_click(self,sCode):
		print(sCode)
		self.end_cardadd(sCode)
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
					return self.on_click(None)
				return

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

			self.gCard.update()
			self.gCard.draw(self.game.screen)
			self.text.update()
			self.text.draw()

		except Exception as e: print(e)
	

	def load_cardadd(self, sName):
		print("s10_cardadd.load_cardadd()",sName)

		#카드 추가 함수 호출 
		if hasattr(self,"ca_"+sName): 
			getattr(self,"ca_"+sName)()

		return 	


	def shuffle_and_draw(self, table, nCnt):
		nTotal = sum(data[1] for data in table)
		arrCard = []
		while len(arrCard)<nCnt :
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
		return 


	"""
	이하 텍스트 이벤트 리스트 
	"""
	def ca_test(self):
		table = [
			["001", 100]
			, ["002", 3]
			, ["003", 60]
			, ["004", 60]
			, ["005", 3]
			, ["006", 3]
			, ["007", 3]
			, ["201", 100]
			, ["401", 60]
			, ["403", 60]
			, ["404", 3]
			, ["406", 100]
		]
		self.shuffle_and_draw(table, 3)

		#카드 선택 후
		def fn(sCode):
			print(sCode)
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_cardadd_scene("test")
		self.end_cardadd = fn
		return 




	def ca_001(self): # 3장 
		table = [
			["001", 100]
			, ["002", 3]
			, ["003", 60]
			, ["004", 60]
			, ["005", 3]
			, ["006", 3]
			, ["007", 3]
			, ["201", 100]
			, ["401", 60]
			, ["403", 60]
			, ["404", 3]
			, ["406", 100]
		]
		self.shuffle_and_draw(table, 3)

		#카드 선택 후
		def fn(sCode):
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_scene_save("Stage1")
		self.end_cardadd = fn
		return 



	def ca_102(self): #동일 확률 3개
		table = [
			["001", 10]
			, ["002", 10]
			, ["003", 10]
			, ["004", 10]
			, ["005", 10]
			, ["006", 10]
			, ["007", 10]
			, ["201", 10]
			, ["401", 10]
			, ["403", 10]
			, ["404", 10]
			, ["406", 10]
		]
		self.shuffle_and_draw(table, 3)

		#카드 선택 후
		def fn(sCode):
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_scene_save("Stage1")
		self.end_cardadd = fn
		return 



	def ca_400(self): #400번대 1장 
		table = [
			["401", 10]
			, ["403", 10]
			, ["404", 10]
			, ["406", 10]
		]
		self.shuffle_and_draw(table, 1)

		#카드 선택 후
		def fn(sCode):
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_scene_save("Stage1")
		self.end_cardadd = fn
		return 




	def ca_201(self): #201번 1장 
		table = [
			["201", 10]
		]
		self.shuffle_and_draw(table, 1)

		#카드 선택 후
		def fn(sCode):
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_scene_save("Stage1")
		self.end_cardadd = fn
		return 




	def ca_000(self): #000번대 1장 
		table = [
			["001", 10]
			, ["002", 10]
			, ["003", 10]
			, ["004", 10]
			, ["005", 10]
			, ["006", 10]
			, ["007", 10]
		]
		self.shuffle_and_draw(table, 1)

		#카드 선택 후
		def fn(sCode):
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_scene_save("Stage1")
		self.end_cardadd = fn
		return 

	def ca_200(self): #200번대 1장 
		table = [
			["201", 10]
		]
		self.shuffle_and_draw(table, 1)

		#카드 선택 후
		def fn(sCode):
			if sCode is None : 
				self.game.nRemainNio += self.nMaxNio
			else : 
				card = Card(self.game.cardlist.find(sCode))
				self.game.arrDeck.append(card)
			self.game.fade_scene_save("Stage1")
		self.end_cardadd = fn
		return 























