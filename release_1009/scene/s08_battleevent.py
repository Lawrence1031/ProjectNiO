from core.scene import Scene
from core.div import Div
from core.dualdisc import Dualdisc
from core.hero import Hero
from core.monster import Monster
import pygame
import math
import random
import copy
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)


class Battleevent(Scene):
	def __init__(self, game):
		super().__init__(game, "Battleevent")

		self.bCardUselock = False
		self.bMonsterlock = False
		self.bVictory = False
		def fn():
			print("end_battle")
			self.game.fade_scene("Stage1")
		self.end_battle = fn

		self.arrDeck = []
		self.arrHand = []
		self.arrGrave = []
		self.arrDiscard = []
		self.nTotalDamage = 0
		self.nMaxDamage = 0
		self.nSP = 0
		self.nMaxSP = 0
		self.nShield = 0

		self.load()

		# self.load_battle("test")
		return 

	def load(self):
		#배경
		self.imgBg = pygame.Surface((1,1), pygame.SRCALPHA)
		#오른쪽 상단 무덤 백그라운드.
		img = pygame.image.load("img/s08_grave_bg.png")
		self.imgBgLeftTop = pygame.transform.smoothscale(img, (235, 118))
		#오른쪽 하단 데미지바 회색 
		img = pygame.image.load("img/s08_bar_gy.png")
		self.imgBgDamage = pygame.transform.smoothscale(img, (150,15))

		#캐릭터 이미지 
		img = pygame.image.load("img/hero_face_001.png")
		img = img.subsurface(pygame.Rect(0, 0, 130, 130))
		#원형 마스크 
		mask = pygame.Surface((130, 130), pygame.SRCALPHA)
		pygame.draw.circle(mask, (255, 255, 255, 255), (65, 65), 65)
		#마스크에 그리기 
		mask.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN) 
		self.imgHero = img


		#카드 스페이스 
		img = pygame.Surface((200,200), pygame.SRCALPHA)
		img.fill((200,200,200))
		img.blit(pygame.image.load("img/card_space.png"),(0,0))
		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		div = Div(self.game)
		div.width(50)
		div.height(50)
		div.surface(img)
		div.surfaceHover(img2)
		div.top(20)
		div.right(80)
		self.btCardspace = div


		#버튼 이미지 
		spriteBt = pygame.image.load("img/bt.png") #157, 120(60)
		surfaceBt = spriteBt.subsurface(pygame.Rect(0, 60, 157, 60))
		surfaceBtHover = spriteBt.subsurface(pygame.Rect(0, 0, 157, 60))

		#턴종료 버튼
		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("턴종료")
		div.fit_text()
		div.width(100)
		div.height(40)
		div.top(650)
		div.left(867)
		div.padding_top(5)
		div.padding_left(10)
		self.btEnd = div

		self.hero = None #캐릭터
		self.arrMonster = []
		monster = Monster(self.game) #적 
		monster.left(480)
		monster.top(70)
		monster.nIndex = 0
		self.arrMonster.append(monster)
		monster = Monster(self.game) #적 
		monster.left(620)
		monster.top(150)
		monster.nIndex = 1
		self.arrMonster.append(monster)
		monster = Monster(self.game) #적 
		monster.left(760)
		monster.top(70)
		monster.nIndex = 2
		self.arrMonster.append(monster)
		monster = Monster(self.game) #적 
		monster.left(900)
		monster.top(150)
		monster.nIndex = 3
		self.arrMonster.append(monster)

		#MyInfo 누적피해, 덱, 무덤, 폐기
		img = pygame.Surface((150,100), pygame.SRCALPHA)
		self.fMyInfo = pygame.font.Font("./font/NotoSansKR-Regular.otf", 15)
		self.myInfo = img


		#남은 카드
		img = pygame.Surface((150,100), pygame.SRCALPHA)
		self.imgRemain = img

		#덱
		img = pygame.image.load("img/deck.png")
		img = pygame.transform.smoothscale(img, (50,50))
		self.deckBase = img.copy()

		self.fDeck = pygame.font.Font("./font/NotoSansKR-Regular.otf", 20)
		shapeText = self.fDeck.render("30", True, (255, 255, 255))
		img.blit(shapeText, (15,7))
		self.deck = img

		#오른쪽 상단 무덤 아이콘
		img = pygame.image.load("img/s08_grave_icon.png")

		div = Div(self.game)
		div.surface(img)
		div.surfaceHover(img)
		div.width(47)
		div.height(65)
		div.top(9)
		div.left(1069)
		self.btGrave = div

		self.fGrave = pygame.font.Font("./font/NotoSansKR-Regular.otf", 30)
		self.textGrave = self.fGrave.render(str(len(self.arrGrave)), True, (255,255,255))

		#실드 방패 아이콘
		img = pygame.image.load("img/s08_shield_1.png")

		div = Div(self.game)
		div.surface(img)
		div.width(372*0.15)
		div.height(581*0.15)
		div.top(268)
		div.left(400)
		div.text("100")
		# div.fit_text()
		div.padding_top(10)
		div.padding_left(-3)
		div.bVisible = False
		# div.arrTextPos = [-1,-10]
		self.shield = div

		#스태미나 포인트
		img = pygame.image.load("img/s08_sp_bg.png")

		div = Div(self.game)
		div.surface(img)
		div.width(80)
		div.height(77)
		div.top(547)
		div.left(878)
		div.color((0,0,0,))
		font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 36)
		font.set_bold(True)
		div.font(font)
		div.text("3/3")
		div.padding_top(8)
		div.padding_left(10)
		self.imgSp = div

		#피해 바 
		img = pygame.image.load("img/s08_bar_rd.png")
		img = pygame.transform.smoothscale(img, (150,15))

		#(150,15)
		div = Div(self.game)
		div.surface(img)
		div.width(100)
		div.height(15)
		div.top(540)
		div.left(36)
		self.imgDamage = div

		#타격시 숫자
		div = Div(self.game)
		div.width(100)
		div.height(50)
		div.left(276)
		div.top(170)
		div.text("-1")
		div.color((255,46,99))
		div.center_text(True)
		div.set_display(False)
		#애니메이션 
		div.add_anim_display("UP", True, 20)
		div.add_anim_relative("UP", (0,-30), 15)
		div.add_anim_display("UP", False, 1)
		div.add_anim_absolute("UP", (276,170), 1)
		self.textDamage = div

		#타격시 숫자 
		self.groupTextDamage = pygame.sprite.Group()
		for i in range(0,10):
			div = Div(self.game)
			div.width(100)
			div.height(50)
			div.left(276)
			div.top(170)
			div.text("-1")
			div.color((255,46,99))
			div.center_text(True)
			div.set_display(False)
			#애니메이션 
			div.add_anim_display("UP", True, 20)
			div.add_anim_relative("UP", (0,-30), 15)
			div.add_anim_display("UP", False, 1)
			div.add_anim_absolute("UP", (276,170), 1)
			self.groupTextDamage.add(div)

		#오른쪽 하단 해골 
		img = pygame.image.load("img/s08_discard_icon.png")
		img = pygame.transform.smoothscale(img, (50,50))

		div = Div(self.game)
		div.surface(img)
		div.width(50)
		div.height(50)
		div.left(202)
		div.top(522)
		#애니메이션 
		div.add_anim_relative("SHAKE", (15,0), 5)
		div.add_anim_relative("SHAKE", (-30,0), 5)
		div.add_anim_relative("SHAKE", (30,0), 3)
		div.add_anim_relative("SHAKE", (-30,0), 3)
		div.add_anim_relative("SHAKE", (30,0), 3)
		div.add_anim_relative("SHAKE", (-30,0), 3)
		div.add_anim_relative("SHAKE", (30,0), 3)
		div.add_anim_absolute("SHAKE", (202,522), 1)
		self.imgDiscard = div

		#폐기 숫자
		div = Div(self.game)
		div.width(100)
		div.height(50)
		div.left(178)
		div.top(480)
		div.text("-1")
		div.color((255,46,99))
		div.center_text(True)
		div.set_display(False)
		#애니메이션 
		div.add_anim_display("UP", True, 20)
		div.add_anim_relative("UP", (0,-30), 15)
		div.add_anim_display("UP", False, 1)
		div.add_anim_absolute("UP", (178,480), 1)
		self.textDiscard = div


		
		#몬스터 텍스트 
		img = pygame.Surface((1,1),pygame.SRCALPHA)
		img.fill((61,60,66,200))
		div = Div(self.game)
		div.surface(img)
		div.width(600)
		div.height(60)
		div.left(600)
		div.top(160)
		div.text("다음 공격을 준비하는 것 같다.")
		div.color((244,203,255))
		div.center_text(True)
		div.set_display(False)
		#애니메이션 
		div.add_anim_display("UP", True, 20)
		div.add_anim_relative("UP", (0,-30), 30)
		div.add_anim_display("UP", True, 30)
		div.add_anim_display("UP", False, 1)
		div.add_anim_absolute("UP", (600,160), 1)
		self.monsterText = div
		# self.monsterText.text("몬스터 텍스트")
		# self.monsterText.start_animate("UP")

		#손패 
		dualdisc = Dualdisc(self.game)
		dualdisc.width(800)
		dualdisc.height(500)
		dualdisc.left(200)
		dualdisc.bottom(0)

		self.dualdisc = dualdisc

		return 


	def load_bg(self, sName):
		#배경
		img = pygame.image.load(sName)
		img = pygame.transform.smoothscale(img, self.game.arrWindowSize)

		mask = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)
		mask.set_alpha(130)
		mask.fill((0, 0, 0))
		pygame.draw.ellipse(mask, (255, 255, 255, 0), (-200, -20, self.game.arrWindowSize[0]+400,self.game.arrWindowSize[1]+40))
		img.blit(mask, (0, 0))

		#오른쪽 상단 무덤 백그라운드.
		img.blit(self.imgBgLeftTop, (self.game.arrWindowSize[0]-235, 0))

		#오른쪽 하단 데미지바 회색 
		img.blit(self.imgBgDamage, (36, 540))

		#오른쪽 하단 주인공 얼굴
		img.blit(self.imgHero,(40,self.game.arrWindowSize[1]-150))
		
		if self.imgBg is not None : del self.imgBg
		self.imgBg = img
		return 

	def load_bgm(self, sCode):
		def fn():
			self.game.sound_play(sCode)
			return
		self.game.call_delay(fn, 500)
		return


	def deck_draw(self):
		if len(self.arrDeck)==0 :
			self.arrDeck = self.arrGrave
			self.arrGrave = []
			if len(self.arrDeck)==0 :
				print("덱&묘지 카드가 없습니다!")
				return ""
		nIndex = random.randint(0, len(self.arrDeck)-1)
		card = self.arrDeck.pop(nIndex)
		self.arrHand.append(card)
		self.dualdisc.add_card(card.sCode)

		#덱 숫자변경 
		del self.deck
		img = self.deckBase.copy()
		shapeText = self.fDeck.render(str(len(self.arrDeck)), True, (255, 255, 255))
		img.blit(shapeText, (15,7))
		self.deck = img
		return card


	def turn_end(self):
		if self.bMonsterlock : return 
		self.bMonsterlock = True

		#손패 휘발카드 빼기 
		for i in range(len(self.arrHand)-1, -1, -1):
			if self.arrHand[i].bHandMelted : #휘발성 방해카드 삭제 
				self.arrHand.pop(i)

		#손패를 묘지로 버리기
		while len(self.arrHand)>0 :
			sCode = self.arrHand.pop(0)
			if sCode=="601" : continue
			self.arrGrave.append(sCode)

		#손패 이미지 비우기 	
		self.dualdisc.remove_card_all()

		#몬스터 액션
		for monster in self.arrMonster:
			if not monster.bDisplay : continue 
			monster.bUseAction = False

		#몬스터 액션 실행.
		self.use_monster_action() 
		return 


	def use_monster_action(self):
		monster = None
		for i in range(0,len(self.arrMonster)):
			if( self.arrMonster[i].bUseAction or self.arrMonster[i].nHp<=0 ): continue
			monster = self.arrMonster[i]
			break

		if monster is not None : #몬스터 액션 
			monster.bUseAction = True
			monsterinfo = monster.monsterinfo 
			if hasattr(monsterinfo, "on_use") and callable(monsterinfo.on_use): 
				monsterinfo.on_use(self, monster, self.end_monster_action)
			monster.cal_buff()

		else : self.start_turn() #턴시작.

		return 

	def start_turn(self):
		self.hero.nStep += 1
		self.hero.nSubStep += 1
		
		#버프 업데이트
		self.hero.cal_buff()

		self.nSP = min(self.nSP+3, self.nMaxSP)
		self.nShield = 0

		#다시 드로우 
		for i in range(0, 5): self.deck_draw()

		self.update_my_info()

		self.bCardUselock = False
		self.bMonsterlock = False

		return 

	def end_monster_action(self):

		#토탈 데미지 체크 
		self.check_total_damage()
		#내정보 업데이트
		self.update_my_info()

		#종료 체크 
		if self.check_defeat() : return

		#다음 토탈 
		self.use_monster_action();

		return
	
	def check_total_damage(self):
		nDiscard = 0
		while self.nTotalDamage >= self.nMaxDamage :
			card = None
			nDiscard += 1

			if len(self.arrDeck)>0 : 
				card = self.arrDeck.pop(0)
			elif len(self.arrGrave)>0 :
				card = self.arrGrave.pop(0)
			else : return 	

			self.nTotalDamage -= self.nMaxDamage 

			if card is not None :
				self.arrDiscard.append(card)

				#같은 카드 아이디 다 폐기.
				sId = card.sId
				nCnt = len(self.arrDeck)
				if nCnt > 0:
					for i in range(nCnt-1, -1, -1):
						if self.arrDeck[i].sId == sId : 
							self.arrDiscard.append(self.arrDeck.pop(i))
				nCnt = len(self.arrGrave)
				if nCnt > 0:
					for i in range(nCnt-1, -1, -1):
						if self.arrGrave[i].sId == sId : 
							self.arrDiscard.append(self.arrGrave.pop(i))

		if nDiscard>0 :
			self.textDiscard.text(f"-{nDiscard}")
			def fn():
				self.textDiscard.start_animate("UP")
				self.imgDiscard.start_animate("SHAKE")
				return
			self.game.call_delay(fn, 500)

		return 	

	def check_defeat(self):
		if len(self.arrDeck)==0 and len(self.arrGrave)==0 :
			self.game.fade_result_scene_save()

			for monster in self.arrMonster: 
				monster.bDisplay = False
				monster.bUseAction = True
			return True
		return False	

	def use_hand_card(self, nIndex):
		if nIndex == -1 : return

		card = self.arrHand[nIndex]
		nCost = card.nCost

		if self.nSP < nCost or card.bUnusable : 
			print("스태미나 부족 / 사용불가")
			return

		if self.bCardUselock : return
		self.bCardUselock = True
		bLocalLock = False

		self.nSP -= nCost #스태미나 차감.

		if card.sType == "ATTACK" : #공격 카드 애니메이션 
			self.hero.start_animate("ATTACT")
			bLocalLock = True
			def fn():
				self.bCardUselock = False
				self.check_victory()
			self.game.call_delay(fn, 300)


		#카드 효과 사용 
		cardinfo = card.cardinfo
		if hasattr(cardinfo,"on_use") and callable(cardinfo.on_use): 
			cardinfo.on_use(self, card)

		self.arrHand.pop(nIndex) #핸드에서 제거
		self.dualdisc.remove_card(nIndex) #핸드모양에서 제거
		self.arrGrave.append(card) #무덤에 추가.

		self.update_my_info()
		if not bLocalLock : self.bCardUselock = False
		return 

	def add_monster_damage(self, nDamage):
		nAD = self.hero.get_ad()

		for monster in self.arrMonster:
			if not monster.bDisplay : continue 
			if monster.nHp > 0 : 
				monster.add_damage(nDamage+nAD)
				def fn():
					monster.start_animate("DAMAGE")
					self.check_victory()
					return
				self.game.call_delay(fn, 300)
				return 

		return 	

	def add_monster_damage_all(self, nDamage):
		nAD = self.hero.get_ad()

		for monster in self.arrMonster :
			if monster.bDisplay : 
				monster.add_damage(nDamage+nAD)
				def fn():
					monster.start_animate("DAMAGE")
					self.check_victory()
					return
				self.game.call_delay(fn, 300)

		return	


	def add_monster_damage_rand(self, nDamage):
		nAD = self.hero.get_ad()

		arr = []
		for monster in self.arrMonster:
			if not monster.bDisplay : continue 
			if monster.nHp > 0 : 
				arr.append(monster)
		
		if len(arr)<1 : return
		monster = random.choice(arr)
		monster.add_damage(nDamage+nAD)
		def fn():
			monster.start_animate("DAMAGE")
			self.check_victory()
			return
		self.game.call_delay(fn, 300)
		return 	


	def add_monster_buff(self, sCode):
		for monster in self.arrMonster:
			if not monster.bDisplay : continue 
			if monster.nHp > 0 : 
				monster.add_buff(sCode)
				return 
		return 	

	def add_monster_buff_all(self, sCode):
		for monster in self.arrMonster :
			if monster.bDisplay : 
				monster.add_buff(sCode)
		return	

	def add_hero_damage(self, nDamage):
		bDamage = False

		if nDamage == 0 :
			for textDamage in self.groupTextDamage:
				if not textDamage.bAnim : 
					self.game.sound_play("DAMAGE")
					textDamage.text("0")
					textDamage.start_animate("UP")
					break

		elif self.nShield >= nDamage : 
			self.nShield -= nDamage
		else : 
			nDamage -= self.nShield

			for textDamage in self.groupTextDamage:
				if not textDamage.bAnim : 
					self.game.sound_play("DAMAGE")
					textDamage.text(f"{-nDamage}")
					textDamage.start_animate("UP")
					break

			self.nTotalDamage += nDamage
			self.nShield = 0
			bDamage = True

		if bDamage : self.hero.start_animate("DAMAGE")
		return 	

	def check_victory(self):
		if self.bVictory : return 

		for monster in self.arrMonster:
			if not monster.bDisplay : continue 
			if monster.nHp > 0 : return 

		#몬스터 처치 카운터 올리기 
		for monster in self.arrMonster:
			if not monster.bDisplay : continue 
			if monster.monsterinfo.sRarity=="N" :
				self.game.nMonsterN += 1
			elif monster.monsterinfo.sRarity=="A" :
				self.game.nMonsterA += 1
			elif monster.monsterinfo.sRarity=="S" :
				self.game.nMonsterS += 1
		
		#승리! 
		self.game.nTotalDamage = self.nTotalDamage #누적데미지 동기화 
		self.game.arrDiscard = copy.deepcopy(self.arrDiscard) #폐기 동기화

		arrCard = copy.deepcopy(self.arrHand)
		arrCard += copy.deepcopy(self.arrDeck)
		arrCard += copy.deepcopy(self.arrGrave)
		for i in range(len(arrCard)-1, -1, -1):
			if arrCard[i].bBattleMelted or arrCard[i].bHandMelted : #휘발성 방해카드 삭제 
				arrCard.pop(i)
		
		self.arrHand = []
		self.arrDeck = []
		self.arrGrave = []

		self.game.arrDeck = arrCard

		self.hero.arrBuff = []

		self.bVictory = True


		#배틀 이벤트 종료 
		self.load_bgm("VICTORY")
		self.bControl = False
		self.end_battle()
		self.game.save_file() #자동 저장 
		


		return


	def update_my_info(self):


		#MyInfo 누적피해, 덱, 무덤, 폐기
		img = pygame.Surface((150,100), pygame.SRCALPHA)
		shapeText = self.fMyInfo.render(f" 스태미나:{self.nSP} ", True, (255, 255, 255),(0,0,0))
		img.blit(shapeText, (0,0))
		shapeText = self.fMyInfo.render(f" 실드:{self.nShield} ", True, (255, 255, 255),(0,0,0))
		img.blit(shapeText, (80,0))
		shapeText = self.fMyInfo.render(f" 누적피해:{self.nTotalDamage}/{self.nMaxDamage} ", True, (255, 255, 255),(0,0,0))
		img.blit(shapeText, (0,20))
		shapeText = self.fMyInfo.render(f" 덱:{len(self.arrDeck)} ", True, (255, 255, 255),(0,0,0))
		img.blit(shapeText, (0,50))
		shapeText = self.fMyInfo.render(f" 무덤:{len(self.arrGrave)} ", True, (255, 255, 255),(0,0,0))
		img.blit(shapeText, (50,50))
		shapeText = self.fMyInfo.render(f" 폐기:{len(self.arrDiscard)} ", True, (255, 255, 255),(0,0,0))
		img.blit(shapeText, (0,70))
		self.myInfo = img

		nNowCard = 0
		for card in self.arrHand:
			if not card.bHandMelted : nNowCard += 1
		for card in self.arrDeck:
			if not card.bHandMelted : nNowCard += 1
		for card in self.arrGrave:
			if not card.bHandMelted : nNowCard += 1

		nTotalCard = nNowCard+len(self.arrDiscard)
		self.imgRemain = self.fMyInfo.render(f" {nNowCard}/{nTotalCard} ", True, (255, 255, 255),(0,0,0)) 

		self.textGrave = self.fGrave.render(str(len(self.arrGrave)), True, (255,255,255))

		self.shield.bVisible = False
		if self.nShield >= 100 :
			# 3자리 
			self.shield.text(str(self.nShield))
			self.shield.bVisible = True 
			self.shield.padding_left(-3)
		if self.nShield >= 10 :
			# 2자리
			self.shield.text(str(self.nShield))
			self.shield.bVisible = True 
			self.shield.padding_left(7)
		elif self.nShield > 0 :
			# 1자리 
			self.shield.text(str(self.nShield))
			self.shield.bVisible = True 
			self.shield.padding_left(17)

		self.imgSp.text(f"{self.nSP}/{self.nMaxSP}")
		nWidth = min(rd(145*self.nTotalDamage/self.nMaxDamage),145)
		self.imgDamage.width(5+nWidth) # 5 ~ 150

		return 

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				if self.bVictory : return 
				nIndex = self.dualdisc.get_select_index()
				if nIndex > -1 :
					self.use_hand_card(nIndex)
				elif self.btEnd.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					self.turn_end()
				elif self.btCardspace.collidepoint(e.pos):
					self.game.sound_play("CURSOR")
					self.game.set_battle_cardspace_scene(self.arrDeck, self.arrGrave, self.arrDiscard)
				return


		except Exception as e: print(e)
		return 

	def update(self):
		try:
			#배경
			self.game.screen.blit(self.imgBg, (0, 0))

			self.game.screen.blit(self.deck, (200, 600))

			self.hero.update()


			for monster in self.arrMonster: monster.update()
			self.dualdisc.update()
			self.btEnd.update()
			self.btGrave.update()
			self.btCardspace.update()
			self.shield.update()
			self.imgSp.update()
			self.imgDamage.update()
			self.imgDiscard.update()
			self.textDamage.update()
			self.groupTextDamage.update()
			self.textDiscard.update()
			self.monsterText.update()

			# 커서 변경.
			pos = pygame.mouse.get_pos()
			nIndex = self.dualdisc.get_select_index()
			if nIndex > -1 : 
				self.game.bCursorHand = True
			elif self.btEnd.collidepoint(pygame.mouse.get_pos()) :
				self.game.bCursorHand = True
			elif self.btCardspace.collidepoint(pos) : 
				self.game.bCursorHand = True
			

			if self.shield.bVisible : self.shield.draw()
			self.hero.draw()
			for monster in self.arrMonster: monster.draw()
			self.dualdisc.draw()
			self.btEnd.draw()
			self.btGrave.draw()
			self.btCardspace.draw()
			self.imgSp.draw()
			self.imgDamage.draw()
			self.imgDiscard.draw()
			self.textDamage.draw()
			self.groupTextDamage.draw(self.game.screen)
			self.textDiscard.draw()
			self.monsterText.draw()

			self.game.screen.blit(self.textGrave, (1090,70))

			# self.game.screen.blit(self.myInfo, (20, 600))
			self.game.screen.blit(self.imgRemain, (260, 550))


		except Exception as e: print(e)


	def load_my_deck(self):
		self.bCardUselock = False
		self.bMonsterlock = False
		self.bVictory = False
		self.arrDeck = copy.deepcopy(self.game.arrDeck)
		self.arrDiscard = copy.deepcopy(self.game.arrDiscard)
		self.arrHand = []
		self.arrGrave = []

		self.nTotalDamage = self.game.nTotalDamage
		self.nMaxDamage = 15
		self.nSP = 3
		self.nMaxSP = 3
		self.nShield = 0

		if self.hero is not None : del self.hero
		hero = Hero(self.game)
		hero.left(400)
		hero.top(300)
		self.hero = hero
		
		#손패 이미지 비우기 	
		self.dualdisc.remove_card_all()

		for i in range(0, 5): self.deck_draw()

		self.update_my_info()
		return 
	

	def load_battle(self, sName):
		print("s08_battleevent.load_battle()",sName)
		self.load_my_deck()

		for monster in self.arrMonster: 
			monster.reset()

		#몬스터 정보 로드  
		if hasattr(self,"be_"+sName): 
			getattr(self,"be_"+sName)()
		return 


	"""
	이하 텍스트 이벤트 리스트 
	"""

	def be_test(self):
		#배경 이미지 
		self.load_bg("img/team_bg_001.png") 
		#배경 음악
		self.load_bgm("Battleevent_1")

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("001")
		self.arrMonster[0].set_monster_info(monsterinfo)

		# monsterinfo = self.game.monsterlist.find("501")
		# self.arrMonster[1].set_monster_info(monsterinfo)

		# monsterinfo = self.game.monsterlist.find("502")
		# self.arrMonster[2].set_monster_info(monsterinfo)

		# monsterinfo = self.game.monsterlist.find("502")
		# self.arrMonster[3].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_scene_save("Stage1")
		self.end_battle = fn
		return 

	def be_000(self):
		self.load_bg("img/bg_001.png") # 배경 이미지(교실)
		self.load_bgm("Battleevent_1") #배경 음악

		#몬스터 로드
		monsterinfo = self.game.monsterlist.find("502")
		self.arrMonster[0].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return


	def set_classroom_stairs(self):
		if self.game.get_stage_name().startswith("Classroom"): 
			#Classroom으로 시작하면. 
			self.load_bg("img/bg_001.png") # 교실
			self.load_bgm("Battleevent_1") #배경 음악
		else : #그외 
			self.load_bg("img/bg_003.png") # 계단
			self.load_bgm("Battleevent_3") #배경 음악
		return 

	def be_001(self):
		self.set_classroom_stairs() #배경, 음악 

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("001")
		self.arrMonster[0].set_monster_info(monsterinfo)
		self.arrMonster[1].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_002(self):
		self.set_classroom_stairs() #배경, 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("001")
		self.arrMonster[0].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("002")
		self.arrMonster[1].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_003(self):
		self.set_classroom_stairs() #배경, 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("001")
		self.arrMonster[0].set_monster_info(monsterinfo)
		self.arrMonster[1].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("002")
		self.arrMonster[2].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_004(self):
		self.set_classroom_stairs() #배경, 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("001")
		self.arrMonster[0].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("002")
		self.arrMonster[1].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("003")
		self.arrMonster[2].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_005(self):
		self.set_classroom_stairs() #배경, 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("002")
		self.arrMonster[0].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("003")
		self.arrMonster[1].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_006(self):
		self.set_classroom_stairs() #배경, 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("002")
		self.arrMonster[0].set_monster_info(monsterinfo)
		self.arrMonster[1].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("003")
		self.arrMonster[2].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_007(self):
		self.load_bg("img/bg_003.png") #배경 이미지(계단)
		self.load_bgm("Battleevent_3") #배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("301")
		self.arrMonster[0].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("002")
		self.arrMonster[1].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_008(self):
		self.load_bg("img/bg_003.png") # 배경 이미지(계단)
		self.load_bgm("Battleevent_3") # 배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("301")
		self.arrMonster[0].set_monster_info(monsterinfo)
		monsterinfo = self.game.monsterlist.find("003")
		self.arrMonster[1].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_009(self):
		self.load_bg("img/bg_003.png") # 배경 이미지(계단)
		self.load_bgm("Battleevent_3") # 배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("301")
		self.arrMonster[0].set_monster_info(monsterinfo)
		self.arrMonster[2].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("001")
		self.end_battle = fn
		return

	def be_010(self):
		self.load_bg("img/bg_005.png") # 배경 이미지(과학실-Classroom3)
		self.load_bgm("Battleevent_2") # 배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("302")
		self.arrMonster[0].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("002")
		self.end_battle = fn
		return

	def be_011(self):
		self.load_bg("img/bg_006.png") # 배경 이미지(도서실-Classroom4)
		self.load_bgm("Battleevent_2") # 배경 음악 

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("303")
		self.arrMonster[0].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("002")
		self.end_battle = fn
		return

	def be_012(self):
		self.load_bg("img/bg_002.png") # 배경 이미지(교실)
		self.load_bgm("Battleevent_2") # 배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("501")
		self.arrMonster[0].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("002")
		self.end_battle = fn
		return


	def be_013(self):
		sStageName = self.game.get_stage_name()
		if sStageName.startswith("Classroom") : #Classroom으로 시작하면. 
			self.load_bg("img/bg_001.png") # 교실
			self.load_bgm("Battleevent_1") # 배경 음악
		elif sStageName.startswith("Stairs") : #Stairs으로 시작하면. 
			self.load_bg("img/bg_003.png") # 계단
			self.load_bgm("Battleevent_3") # 배경 음악
		else : #그외 
			self.load_bg("img/bg_008.png") # 옥상
			self.load_bgm("Battleevent_2") # 배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("503")
		self.arrMonster[0].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.fade_cardadd_scene("003")
		self.end_battle = fn
		return


	def be_014(self): #보스
		self.load_bg("img/bg_002.png") #배경 이미지(운동장-Playground)
		self.load_bgm("Battleevent_2") #배경 음악

		#몬스터 로드 
		monsterinfo = self.game.monsterlist.find("801")
		self.arrMonster[0].set_monster_info(monsterinfo)

		#배틀 종료 이벤트 
		def fn():
			self.game.nLevel += 1
			self.game.fade_result_scene_save()
		self.end_battle = fn
		return







