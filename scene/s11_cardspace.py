from core.scene import Scene
from core.div import Div
from core.card import Card
import pygame
import random


class Cardspace(Scene):
	def __init__(self, game):
		super().__init__(game, "Cardspace")

		self.sLoadType = "STAGE" # STAGE, BATTLE
		self.nCntDraw = 18

		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/s11_bg.png")
		img = pygame.transform.smoothscale(img, self.game.arrWindowSize)

		#전체 반투명 배경
		surf = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)
		surf.set_alpha(90)
		surf.fill((0, 0, 0))
		img.blit(surf,(0,0))

		#왼쪽 파트
		img2 = pygame.image.load("img/s11_brown.png")
		img2 = pygame.transform.smoothscale(img2, (800,580))
		img2.set_alpha(180)
		img.blit(img2,(35,100))

		img2 = pygame.Surface((780,525), pygame.SRCALPHA)
		img2.set_alpha(120)
		img2.fill((0, 0, 0))
		img.blit(img2,(45,150))


		#오른쪽 파트 
		img2 = pygame.image.load("img/s11_brown_d.png")
		img2 = pygame.transform.smoothscale(img2, (400,580))
		img2.set_alpha(180)
		img.blit(img2,(835,100))

		self.imgBg = img


		#상단 버튼 3개

		#로드할때 스테이지 모드, 배틀 모드 2개로
		#스테이지 모드에서는 덱, 폐기 2종으로
		#배틀 모드에서는 덱, 묘지, 폐기 3종으로 



		#버튼 그룹 
		self.gBt = pygame.sprite.Group()

		#버튼 이미지 
		spriteBt = pygame.image.load("img/bt.png") #157, 120(60)
		surfaceBt = spriteBt.subsurface(pygame.Rect(0, 60, 157, 60))
		surfaceBtHover = spriteBt.subsurface(pygame.Rect(0, 0, 157, 60))

		#덱 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("덱")
		div.fit_text()
		div.width(50)
		div.height(50)
		div.top(50)
		div.left(35)
		div.padding_top(5)
		div.padding_left(10)
		self.gBt.add(div)
		self.btDeck = div

		#묘지 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("묘지")
		div.fit_text()
		div.width(80)
		div.height(50)
		div.top(50)
		div.left(87)
		div.padding_top(5)
		div.padding_left(10)
		self.gBt.add(div)
		self.btGrave = div
		
		#폐기 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("폐기")
		div.fit_text()
		div.width(80)
		div.height(50)
		div.top(50)
		div.left(169)
		div.padding_top(5)
		div.padding_left(10)
		self.gBt.add(div)
		self.btDiscard = div

		#폐기, 회수 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("폐기")
		div.fit_text()
		div.width(140)
		div.height(50)
		div.top(615)
		div.left(955)
		div.padding_top(5)
		div.padding_left(40)
		div.bDisplay = False
		self.gBt.add(div)
		self.btUse = div




		#리스트 이동 

		#버튼 이미지 
		btArrowB = pygame.image.load("img/s11_arrow_b.png") #778, 669
		btArrowW = pygame.image.load("img/s11_arrow_w.png") #778, 669

		#위 버튼
		div = Div(self.game)
		div.surface(btArrowB)
		div.surfaceHover(btArrowW)
		div.width(50)
		div.height(35)
		div.top(110)
		div.left(715)
		self.gBt.add(div)
		self.btArrowUp = div

		
		#회전 
		btArrowB = pygame.transform.rotate(btArrowB, 180)	
		btArrowW = pygame.transform.rotate(btArrowW, 180)

		#아래 버튼
		div = Div(self.game)
		div.surface(btArrowB)
		div.surfaceHover(btArrowW)
		div.width(50)
		div.height(35)
		div.top(110)
		div.left(775)
		self.gBt.add(div)
		self.btArrowDown = div

		#닫기 버튼
		img = pygame.image.load("img/star_07_b.png") #512, 512
		img_hover = pygame.image.load("img/star_07_w.png")
		# img = pygame.transform.smoothscale(img, (235, 118))
		rect = img.get_rect()

		btCloseB = pygame.Surface((rect.width/2,rect.height/2), pygame.SRCALPHA)
		btCloseB.fill((0, 0, 0))
		btCloseB.blit(img,(-rect.width/4,-rect.height/4))

		btCloseW = pygame.Surface((rect.width/2,rect.height/2), pygame.SRCALPHA)
		btCloseW.fill((150, 150, 150))
		btCloseW.blit(img,(-rect.width/4,-rect.height/4))

		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img_hover)
		div.width(64)
		div.height(64)
		div.top(10)
		div.right(10)
		self.gBt.add(div)
		self.btClose = div




		#카드 리스트들
		self.gCard = pygame.sprite.Group()

		cardImg = self.game.cardlist.render("001") #574 800

		nWidth = 574*0.2
		nHeight = 800*0.2
		nStartTop = 160
		nStartLeft = 60
		nDiffY = 170
		nDiffX = 125

		for i in range(0, 3):
			for j in range(0, 6):
				div = Div(self.game)
				div.sCardCode = "001"
				div.surface(cardImg)
				# div.surfaceHover(btArrowW)
				div.width(nWidth)
				div.height(nHeight)
				div.top(nStartTop+nDiffY*i)
				div.left(nStartLeft+nDiffX*j)
				div.bDisplay = False
				self.gCard.add(div)


		#확대 카드 

		cardImg = self.game.cardlist.render("001") #574 800

		div = Div(self.game)
		div.surface(cardImg)
		# div.surfaceHover(btArrowW)
		div.width(574*0.6)
		div.height(800*0.6)
		div.top(120)
		div.left(860)
		self.imgSelCard = div


		self.nTab = 0 # 0:덱, 1:묘지, 2:폐기 
		self.nPage = 0
		self.arrDeck = []
		self.arrGrave = []
		self.arrDiscard = []

		return 



	def draw_card(self, nPageUp):

		arrDiv = self.gCard.sprites()
		for div in arrDiv: div.bDisplay=False

		nIndex = 0
		arrCard = []
		if self.nTab == 0 :
			arrCard = self.arrDeck
		elif self.nTab == 1 :
			arrCard = self.arrGrave 
		elif self.nTab == 2 :
			arrCard = self.arrDiscard

		if nPageUp < 0 : 
			self.nPage = max(0, self.nPage+nPageUp)
		else :
			self.nPage = min(len(arrCard)//self.nCntDraw, self.nPage+nPageUp)

		nStart = self.nPage*self.nCntDraw
		for i in range(nStart, len(arrCard)) : 
			div = arrDiv[nIndex]
			cardImg = self.game.cardlist.render(arrCard[i]) 
			div.sCardCode = arrCard[i]
			div.surface(cardImg)
			div.bDisplay = True
			nIndex+=1
			if nIndex >= self.nCntDraw : break




		return 

	def card_click(self, sCardCode):

		cardImg = self.game.cardlist.render(sCardCode) #574 800
		self.imgSelCard.surface(cardImg)


		return 

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				if self.btDeck.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					self.nTab = 0
					self.reset_draw()
					return
				elif self.btGrave.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					self.nTab = 1
					self.reset_draw()
					return
				elif self.btDiscard.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					self.nTab = 2
					self.reset_draw()
					return
				elif self.btArrowUp.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					self.draw_card(-1)
					return
				elif self.btArrowDown.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					self.draw_card(1)
					return
				elif self.btClose.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					if self.sLoadType=="STAGE" : 
						self.game.set_scene("Stage1")
					elif self.sLoadType == "BATTLE" :
						self.game.set_scene("Battleevent")
					return
				elif self.btUse.collidepoint(e.pos) :
					self.game.sound_play("CURSOR")
					print("카드사용.")

				for div in self.gCard :
					if div.bDisplay and div.collidepoint(e.pos) :
						self.game.sound_play("CURSOR")
						self.card_click(div.sCardCode)
						return

		except Exception as e: print(e)

	def update(self):
		try:

			# 커서 변경.
			pos = pygame.mouse.get_pos()
			for div in self.gBt :
				if div.bDisplay and div.collidepoint(pos) :
					self.game.bCursorHand = True
					break
			for div in self.gCard :
				if div.bDisplay and div.collidepoint(pos) :
					self.game.bCursorHand = True
					break

			self.game.screen.blit(self.imgBg, (0, 0))

			# self.gCard.update()
			# self.gCard.draw(self.game.screen)

			#카드 
			self.gCard.update()
			self.gCard.draw(self.game.screen)

			#확대 카드 
			self.imgSelCard.update()
			self.imgSelCard.draw()

			#버튼 
			self.gBt.update()
			self.gBt.draw(self.game.screen)



		except Exception as e: print(e)
	


	def load_cardspace(self, sName):
		if sName == "stage" :
			self.load_stage_cardspace()
		elif sName == "battle" :
			self.load_battle_cardspace()
		else :
			self.load_stage_cardspace()

		return 

	def reset_data(self):
		self.nTab = 0 # 0:덱, 1:묘지, 2:폐기 
		self.nPage = 0
		self.arrDeck = []
		self.arrGrave = []
		self.arrDiscard = []
		return 

	def reset_draw(self):
		self.draw_card(-9999)
		arrCard = []
		if self.nTab == 0 :
			arrCard = self.arrDeck
		elif self.nTab == 1 :
			arrCard = self.arrGrave 
		elif self.nTab == 2 :
			arrCard = self.arrDiscard

		if len(arrCard)>0 :
			cardImg = self.game.cardlist.render(arrCard[0]) #574 800
			self.imgSelCard.surface(cardImg)
		else : self.imgSelCard.surface(None)
		return 

	def load_stage_cardspace(self):
		self.reset_data() #데이터 초기화 
		self.sLoadType = "STAGE"

		#덱 불러오기
		for card in self.game.arrDeck :
			self.arrDeck.append(card.sCode)
		self.arrDeck.sort()

		#묘지 
		self.arrGrave = []

		#폐기
		for card in self.game.arrDiscard :
			self.arrDiscard.append(card.sCode)
		self.arrDiscard.sort()

		self.reset_draw() #화면 그리기 
		return 


	def load_battle_cardspace(self, arrDeck, arrGrave, arrDiscard):
		self.reset_data() #데이터 초기화 
		self.sLoadType = "BATTLE"

		#덱 불러오기
		for card in arrDeck :
			self.arrDeck.append(card.sCode)
		self.arrDeck.sort()

		#묘지 
		for card in arrGrave :
			self.arrGrave.append(card.sCode)
		self.arrGrave.sort()

		#폐기
		for card in arrDiscard :
			self.arrDiscard.append(card.sCode)
		self.arrDiscard.sort()

		self.reset_draw() #화면 그리기 
		return 







