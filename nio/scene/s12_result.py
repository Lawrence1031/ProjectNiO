from core.scene import Scene
from core.div import Div
import pygame
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)

class Result(Scene):
	def __init__(self, game):
		super().__init__(game, "Result")

		self.nResult = 0
		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/s12_bg.png")
		img = pygame.transform.smoothscale(img, self.game.arrWindowSize)

		#전체 반투명 배경
		#surf = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)
		#surf.set_alpha(90)
		#surf.fill((0, 0, 0))
		#img.blit(surf,(0,0))


		#전체 반투명 배경
		#line = pygame.Surface((900,5), pygame.SRCALPHA)
		#line.fill((255, 255, 255))
		#img.blit(line,(200,500))
		
		self.imgBg = img

		#텍스트 카드
		self.gText = pygame.sprite.Group()

		#글자 
		div = Div(self.game)
		# div.surface(surf)
		div.text("잔여 포인트")
		div.width(350)
		div.height(70)
		div.top(150+80*0)
		div.left(200)
		self.gText.add(div)
		self.textRemain = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("0")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*0)
		div.left(500)
		self.gText.add(div)
		self.textRemain2 = div

		#글자 
		div = Div(self.game)
		# div.surface(surf)
		div.text("N등급 카드 X 10")
		div.width(350)
		div.height(70)
		div.top(150+80*1)
		div.left(200)
		self.gText.add(div)
		self.textCardN = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("5")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*1)
		div.left(500)
		self.gText.add(div)
		self.textCardN2 = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("A등급 카드 X 2")
		div.width(350)
		div.height(70)
		div.top(150+80*2)
		div.left(200)
		self.gText.add(div)
		self.textCardA = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("8")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*2)
		div.left(500)
		self.gText.add(div)
		self.textCardA2 = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("S등급 카드 X 0")
		div.width(350)
		div.height(70)
		div.top(150+80*3)
		div.left(200)
		self.gText.add(div)
		self.textCardS = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("0")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*3)
		div.left(500)
		self.gText.add(div)
		self.textCardS2 = div


		div = Div(self.game)
		# div.surface(surf)
		div.text("몬스터(N) 처치 X 1")
		div.width(350)
		div.height(70)
		div.top(150+80*0)
		div.left(680)
		self.gText.add(div)
		self.textMonsterN = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("0")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*0)
		div.left(980)
		self.gText.add(div)
		self.textMonsterN2 = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("몬스터(A) 처치 X 1")
		div.width(350)
		div.height(70)
		div.top(150+80*1)
		div.left(680)
		self.gText.add(div)
		self.textMonsterA = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("0")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*1)
		div.left(980)
		self.gText.add(div)
		self.textMonsterA2 = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("보스 처치 X 1")
		div.width(350)
		div.height(70)
		div.top(150+80*2)
		div.left(680)
		self.gText.add(div)
		self.textMonsterS = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("0")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*2)
		div.left(980)
		self.gText.add(div)
		self.textMonsterS2 = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("??? 처치 X 1")
		div.width(350)
		div.height(70)
		div.top(150+80*3)
		div.left(680)
		self.gText.add(div)
		self.textMonsterEx = div

		div = Div(self.game)
		# div.surface(surf)
		div.text("0")
		div.text_align("RIGHT")
		div.width(120)
		div.height(70)
		div.top(150+80*3)
		div.left(980)
		self.gText.add(div)
		self.textMonsterEx2 = div


		div = Div(self.game)
		# div.surface(surf)
		div.font_size(50)
		div.text("35")
		div.text_align("RIGHT")
		div.width(120)
		div.height(90)
		div.top(500)
		div.left(950)
		self.gText.add(div)
		self.textResult = div

		#버튼 이미지 
		spriteBt = pygame.image.load("img/bt.png") #157, 120(60)
		surfaceBt = spriteBt.subsurface(pygame.Rect(0, 60, 157, 60))
		surfaceBtHover = spriteBt.subsurface(pygame.Rect(0, 0, 157, 60))

		#다음 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("다음")
		div.fit_text()
		div.width(100)
		div.height(60)
		div.top(595)
		div.right(90)
		self.btNext = div


		return 


	def cal_result(self):
		self.game.reset_scene("Stage1")
		
		nCardN = 0
		nCardA = 0
		nCardS = 0

		for card in self.game.arrDeck :
			if not card.bInRaid : continue
			elif card.sRarity=="N" : nCardN+=1
			elif card.sRarity=="A" : nCardA+=1
			elif card.sRarity=="S" : nCardS+=1

		for card in self.game.arrDiscard :
			if not card.bInRaid : continue
			elif card.sRarity=="N" : nCardN+=1
			elif card.sRarity=="A" : nCardA+=1
			elif card.sRarity=="S" : nCardS+=1

		self.textRemain.text("계승 포인트")
		self.textRemain2.text(str(self.game.nRemainNio))
		self.textCardN.text("N등급 카드 X "+str(nCardN))
		self.textCardN2.text(str(rd(nCardN*1)))
		self.textCardA.text("A등급 카드 X "+str(nCardA))
		self.textCardA2.text(str(rd(nCardA*3)))
		self.textCardS.text("S등급 카드 X "+str(nCardS))
		self.textCardS2.text(str(rd(nCardS*10)))
		self.textMonsterN.text("몬스터(N) 처치 X "+str(self.game.nMonsterN))
		self.textMonsterN2.text(str(rd(self.game.nMonsterN)))
		self.textMonsterA.text("몬스터(A) 처치 X "+str(self.game.nMonsterA))
		self.textMonsterA2.text(str(rd(self.game.nMonsterA*5)))
		self.textMonsterS.text("보스 처치 X "+str(self.game.nMonsterS))
		self.textMonsterS2.text(str(rd(self.game.nMonsterS*20)))
		self.textMonsterEx.text("??? 처치 X "+str(self.game.nMonsterEx))
		self.textMonsterEx2.text(str(rd(self.game.nMonsterEx*100)))
		
		nResult = self.game.nRemainNio
		nResult += rd(nCardN*1)
		nResult += rd(nCardA*3)
		nResult += rd(nCardS*10)
		nResult += rd(self.game.nMonsterN)
		nResult += rd(self.game.nMonsterA*5)
		nResult += rd(self.game.nMonsterS*20)
		nResult += rd(self.game.nMonsterEx*100)
		self.nResult = nResult
		self.textResult.text(str(nResult))

		#위치를 순차적으로 왼쪽
		nIndex = 0

		#잔여포인트
		self.textRemain.top(150+80*nIndex)
		self.textRemain.bDisplay = True
		self.textRemain2.top(150+80*nIndex)
		self.textRemain2.bDisplay = True
		nIndex += 1

		#N 카드 
		if nCardN > 0 :
			self.textCardN.top(150+80*nIndex)
			self.textCardN.bDisplay = True
			self.textCardN2.top(150+80*nIndex)
			self.textCardN2.bDisplay = True
			nIndex += 1
		else : 
			self.textCardN.bDisplay = False
			self.textCardN2.bDisplay = False

		#A 카드 
		if nCardA > 0 :
			self.textCardA.top(150+80*nIndex)
			self.textCardA.bDisplay = True
			self.textCardA2.top(150+80*nIndex)
			self.textCardA2.bDisplay = True
			nIndex += 1
		else : 
			self.textCardA.bDisplay = False
			self.textCardA2.bDisplay = False

		#S 카드 
		if nCardS > 0 :
			self.textCardS.top(150+80*nIndex)
			self.textCardS.bDisplay = True
			self.textCardS2.top(150+80*nIndex)
			self.textCardS2.bDisplay = True
			nIndex += 1
		else : 
			self.textCardS.bDisplay = False
			self.textCardS2.bDisplay = False


		#오른쪽 
		nIndex = 0

		#N 몬스터 
		if self.game.nMonsterN > 0 :
			self.textMonsterN.top(150+80*nIndex)
			self.textMonsterN.bDisplay = True
			self.textMonsterN2.top(150+80*nIndex)
			self.textMonsterN2.bDisplay = True
			nIndex += 1
		else : 
			self.textMonsterN.bDisplay = False
			self.textMonsterN2.bDisplay = False

		#A 몬스터 
		if self.game.nMonsterA > 0 :
			self.textMonsterA.top(150+80*nIndex)
			self.textMonsterA.bDisplay = True
			self.textMonsterA2.top(150+80*nIndex)
			self.textMonsterA2.bDisplay = True
			nIndex += 1
		else : 
			self.textMonsterA.bDisplay = False
			self.textMonsterA2.bDisplay = False

		#S 몬스터 
		if self.game.nMonsterS > 0 :
			self.textMonsterS.top(150+80*nIndex)
			self.textMonsterS.bDisplay = True
			self.textMonsterS2.top(150+80*nIndex)
			self.textMonsterS2.bDisplay = True
			nIndex += 1
		else : 
			self.textMonsterS.bDisplay = False
			self.textMonsterS2.bDisplay = False

		#EX 몬스터 
		if self.game.nMonsterEx > 0 :
			self.textMonsterEx.top(150+80*nIndex)
			self.textMonsterEx.bDisplay = True
			self.textMonsterEx2.top(150+80*nIndex)
			self.textMonsterEx2.bDisplay = True
			nIndex += 1
		else : 
			self.textMonsterEx.bDisplay = False
			self.textMonsterEx2.bDisplay = False


		return 

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				if self.btNext.collidepoint(e.pos) : #다음 
					self.game.sound_play("CURSOR")
					self.game.nRemainNio = self.nResult
					self.game.fade_cardshop_scene(self.nResult)
					return
		except Exception as e: print(e)

	def update(self):
		try:
			# 커서 변경.
			pos = pygame.mouse.get_pos()
			if self.btNext.collidepoint(pos) : self.game.bCursorHand = True

			self.game.screen.blit(self.imgBg, (0, 0))

			self.gText.update()
			self.gText.draw(self.game.screen)

			self.btNext.update()
			self.btNext.draw()


		except Exception as e: print(e)
	









