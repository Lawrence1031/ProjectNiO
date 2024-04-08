import pygame
from core.card import Card


class Cardinfo:
	def __init__(self,sCode):
		self.sCode = sCode

		self.sType = "ATTACK" 
		self.sRarity = "N"
		self.nCost = 1
		self.sImgIllu = "card_001.png"
		self.sImgBase = "NORMAL"
		self.bBattleMelted = False
		self.bHandMelted = False
		self.bGraveMelted = False
		self.bUnusable = False

		self.sTitle = "카드명"
		self.arrBody = [ 
			"카드설명"
			, "카드설명 다음줄"
		]
		return 


class Cardlist:
	def __init__(self, game):
		self.game = game
		self.cardList = {}
		#추가 방법
		cardinfo = Cardinfo("000")
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "N"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_001.png"
		cardinfo.sImgBase = "NORMAL"
		self.add(cardinfo)

		#각 분류별 카드로드
		self.attack_card()
		self.heal_card()
		self.support_card()
		self.obstruction_card()
		self.melt_card()

		#카드 언어팩 적용. 
		self.set_lang()

		#렌더값들 로드 
		self.load_render()
		return 

	def add(self, cardinfo):
		self.cardList["c"+cardinfo.sCode] = cardinfo
		return	

	def find(self, sCode):
		return self.cardList.get("c"+sCode)

	def set_lang(self):

		arrText = []
		with open("./lang/card_info_"+self.game.sLangCode+".txt", "r", encoding="utf8") as file:
			for sLine in file:
				arrText.append(sLine.strip())

		langList = {}
		sCode = ""
		lang = None
		bBody = False
		for text in arrText :
			try:
				if text.startswith("#CODE") :
					lang = {}
					sCode = text.split(maxsplit=1)[1]
					lang["sCode"] = sCode
					lang["sTitle"] = ""
					lang["arrBody"] = []

				elif lang is not None :

					if text.startswith("#TIT") :
						lang["sTitle"] = text.split(maxsplit=1)[1]
					elif text.startswith("#BODY") :
						bBody = True
					elif text.startswith("#END") :
						langList[sCode] = lang
						lang = None
						bBody = False
					elif bBody :
						lang["arrBody"].append(text)

				else :
					bBody = False

			except Exception as e: print(e)

		sCode = ""
		for k in self.cardList :
			sCode = self.cardList[k].sCode
			lang = langList.get(sCode)
			if lang is None : continue
			self.cardList[k].sTitle = lang.get("sTitle", "")
			self.cardList[k].arrBody = lang.get("arrBody", [])

		return 

	def load_render(self):
		self.cardRender = {}

		self.nCardWidth = 574
		self.nCardHeight = 800

		self.nTitleLeft = 272
		self.nTitleTop = 13

		self.nIlluWidth = 553
		self.nIlluHeight = 412
		self.nIlluLeft = 10
		self.nIlluTop = 78
		
		self.nBodyLeft = 20
		self.nBodyTop = 495
		self.nBodyWidth = 530
		self.nBodyLineHeight = 50

		self.fTitle = pygame.font.Font("./font/NotoSansKR-Regular.otf", 40)
		self.fBody = pygame.font.Font("./font/NotoSansKR-Regular.otf", 40)

		self.arrBaseImage = {} #카드 기본틀들. 
		self.arrBaseImage["NORMAL"] = pygame.image.load("img/card_base_001.png").convert_alpha()
		self.arrBaseImage["ATTACK"] = pygame.image.load("img/card_base_001.png").convert_alpha()
		self.arrBaseImage["HEAL"] = pygame.image.load("img/card_base_002.png").convert_alpha()
		self.arrBaseImage["SUPPORT"] = pygame.image.load("img/card_base_003.png").convert_alpha()
		self.arrBaseImage["OBSTRUCTION"] = pygame.image.load("img/card_base_004.png").convert_alpha()

		self.imgCost = pygame.image.load("img/card_sp.png").convert()
		return 

	def render(self, sCode):
		if sCode not in self.cardRender : #없으면 그리기.
			cardInfo = self.find(sCode)
			if cardInfo is None : return pygame.Surface((1,1), pygame.SRCALPHA)

			#일러
			imgIllu = pygame.image.load("img/"+cardInfo.sImgIllu).convert()
			#베이스
			imgBase = self.arrBaseImage[cardInfo.sImgBase]
			#타이틀 
			sTitle = cardInfo.sTitle
			#본문 
			arrBody = cardInfo.arrBody
			#카드 코스트 
			nCost = cardInfo.nCost

			#이미지 만들기 시작 
			img = pygame.Surface((self.nCardWidth,self.nCardHeight), pygame.SRCALPHA)
			#일러 투명 막기.
			pygame.draw.rect(img, (0,0,0), (self.nIlluLeft,self.nIlluTop,self.nIlluWidth,self.nIlluHeight))
			#일러 합치기 
			imgIllu = pygame.transform.smoothscale(imgIllu, (self.nIlluWidth,self.nIlluHeight))
			img.blit(imgIllu, (self.nIlluLeft,self.nIlluTop), special_flags=pygame.BLEND_RGBA_MAX)
			#베이스 합치기 
			img.blit(imgBase,(0,0))
			#카드 타이틀 
			shapeText = self.fTitle.render(sTitle, True, (0, 0, 0))
			rect = shapeText.get_rect()

			img.blit(shapeText,(self.nTitleLeft-rect.width/2,self.nTitleTop))
			#카드 본문
			shape = None
			shapeLast = None
			nLine = 0
			for s in arrBody :
				shape = self.fBody.render(s, True, (0, 0, 0))
				if self.nBodyWidth < shape.get_rect().width :
					shape = None
					shapeLast = None

					i = 0
					while len(s)!=0 :
						shape = self.fBody.render(s[0:i], True, (0, 0, 0))
						if self.nBodyWidth < shape.get_rect().width :
							img.blit(shapeLast,(self.nBodyLeft,self.nBodyTop+nLine*self.nBodyLineHeight))
							nLine += 1
							s = s[i-1:]
							i = 0
						else : 
							shapeLast = shape
							i += 1
						
						if len(s) <= i : 
							img.blit(shape,(self.nBodyLeft,self.nBodyTop+nLine*self.nBodyLineHeight))
							nLine += 1
							break
				else :
					img.blit(shape,(self.nBodyLeft,self.nBodyTop+nLine*self.nBodyLineHeight))
					nLine += 1

			#카드 코스트
			if nCost > 0 : img.blit(self.imgCost,(20,20+0*55))
			if nCost > 1 : img.blit(self.imgCost,(20,20+1*55))
			if nCost > 2 : img.blit(self.imgCost,(20,20+2*55))
			if nCost > 3 : img.blit(self.imgCost,(20,20+3*55))

			self.cardRender[sCode] = img

		return self.cardRender[sCode].copy()



	##################################
	# 공격카드 001 ~
	##################################
	def attack_card(self):
		print("공격카드(001~) 로드")

		#001 사격
		cardinfo = Cardinfo("001")
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "N"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_001.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 적에게 피해(7)를 준다.
			scene.add_monster_damage(7)
			self.game.sound_play("GUNSHOT_01")
		cardinfo.on_use = fn
		self.add(cardinfo)

		#002 무모한 돌진 
		cardinfo = Cardinfo("002")
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "S"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_002.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 적에게 피해(10)를 준다. 
			# 그 후에 "어지러움"카드를 1장 묘지에 추가한다.
			scene.add_monster_damage(10) # 10떼미지!
			self.game.sound_play("GUNSHOT_02")
			scene.arrGrave.append(Card(self.find("601"))) # 어지러움카드 추가 
		cardinfo.on_use = fn
		self.add(cardinfo)

		#003
		cardinfo = Cardinfo("003") #무작위 사격
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "A"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_003.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 무작위 적에게 피해(7)를 준다.
			scene.add_monster_damage(7) # 7데미지 
			self.game.sound_play("GUNSHOT_03")
		cardinfo.on_use = fn
		self.add(cardinfo)


		cardinfo = Cardinfo("004") #견제 사격
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "A"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_004.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 적에게 피해(4)를 준다.
			scene.add_monster_damage(4) # 4데미지
			self.game.sound_play("GUNSHOT_04")
		cardinfo.on_use = fn
		self.add(cardinfo)


		cardinfo = Cardinfo("005") #퀵 샷
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "S"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_005.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 적에게 피해(3)를 준다.
			# 그 후에 "퀵 샷"카드를 1장 묘지에 추가한다.
			# 적에게 피격당해 복사된 "퀵 샷"카드가 폐기되는 경우, 복사된 "퀵 샷" 카드와 이 카드를 전부 폐기한다. 
			scene.add_monster_damage(3)
			self.game.sound_play("GUNSHOT_05")
			newCard = Card(self.find("901")) # 퀵 샷
			newCard.sId = card.sId #아이디는 동일하게.
			scene.arrGrave.append(newCard) #무덤에 추가
		cardinfo.on_use = fn
		self.add(cardinfo)

		cardinfo = Cardinfo("006") #제압 사격
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "S"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_006.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 적 전체에게 피해(5)를 준다.
			scene.add_monster_damage_all(5)# 적 전체 피해
			self.game.sound_play("GUNSHOT_06")
		cardinfo.on_use = fn
		self.add(cardinfo)

		cardinfo = Cardinfo("007") #조준 사격
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "S"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_007.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 적 전체에게 피해(4)를 준다.
			# 그 후에 해당 적의 공격력을 2턴동안 (5) 감소시킨다.
			scene.add_monster_damage(4) # 피격 당한 적 공격력을 2턴동안 5 감소 부탁드립니다.(부관에게)
			self.game.sound_play("MACHINEGUN_01")
			# nDamage = nDamage -5 (15)
			# count = 0
			# if 너 턴종료 click -> count = count + 1
			# if count >= 2 :
				# nDamage = nDamage +5 (20)

		cardinfo.on_use = fn
		self.add(cardinfo)


		cardinfo = Cardinfo("010") #약점 포착
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "-"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_007.png"
		cardinfo.sImgBase = "ATTACK"
		def fn(scene, card):
			# 보스에게만 사용 가능하다. 보스의 현재 체력의 25의 대미지를 준다.
			# 그 후 이 카드를 삭제한다.
			scene.add_monster_damage(25)
			self.game.sound_play("MACHINEGUN_02")
			# 이 카드 사용 시에 삭제되게(폐기 말고 아예 없어지게) 부탁드립니다 (부관에게)
			# if use this card, this card will removed.


		cardinfo.on_use = fn
		self.add(cardinfo)


		return

	##################################
	# 회복카드  201 ~
	##################################
	def heal_card(self):
		print("회복카드(201~) 로드")

		cardinfo = Cardinfo("201") #게이지 회복 카드 1
		cardinfo.sType = "HEAL" 
		cardinfo.sRarity = "N"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_201.png"
		cardinfo.sImgBase = "HEAL"
		def fn(scene, card):
			# 게이지를 회복한다.
			#self.nTotalDamage = 0 대충 이런식으로 하면 될까요?(부관에게)
			scene.nTotalDamage = max(scene.nTotalDamage-15,0)
			self.game.sound_play("SHIELD")
		cardinfo.on_use = fn
		self.add(cardinfo)

		return


	##################################
	# 지원카드  401 ~ 
	##################################
	def support_card(self):
		print("지원카드(401~) 로드")

		cardinfo = Cardinfo("401") #격려 
		cardinfo.sType = "SUPPORT" 
		cardinfo.sRarity = "A"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_401.png"
		cardinfo.sImgBase = "SUPPORT"
		def fn(scene, card):
			# 이번 전투 종료 시까지 공격력 +1
			# 기본 공격력이라는 스텟이 없는듯? 기본 공격력 없이 가려면 카드마다 공격력 +1 효과를 줘야되는데
			# 기본 공격력 스텟을 만들어서 0으로 쓰다가 이 카드 사용 시 1 추가되게 해주셔야될듯(부관에게)

			# 기본 공격력 = 기본 공격력 +1
			# if progress victory step, 기본 공격력 = 0
			print(cardinfo.sCode)
			self.game.sound_play("POWERUP")
		cardinfo.on_use = fn
		self.add(cardinfo)

		cardinfo = Cardinfo("403") #몸풀기
		cardinfo.sType = "SUPPORT" 
		cardinfo.sRarity = "A"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_403.png"
		cardinfo.sImgBase = "SUPPORT"
		def fn(scene, card):
			# 이번 턴 종료 시까지 공격력 +1
			# 위에꺼와 연관되게 기본 공격력 플리즈

			# 기본 공격력 = 기본 공격력 +1
			# if you click turn end btn, 기본 공격력 = 기본 공격력 -1
			print(cardinfo.sCode)
			self.game.sound_play("POWERUP")
		cardinfo.on_use = fn
		self.add(cardinfo)

		cardinfo = Cardinfo("404") #보급
		cardinfo.sType = "SUPPORT" 
		cardinfo.sRarity = "S"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_404.png"
		cardinfo.sImgBase = "SUPPORT"
		def fn(scene, card):
			# 카드 1장을 드로우한다. 스태미나(1)을 회복한다.
			scene.deck_draw()
			scene.nSP += 1
			self.game.sound_play("RELOAD")
		cardinfo.on_use = fn
		self.add(cardinfo)

		cardinfo = Cardinfo("406") #방어 지원 
		cardinfo.sType = "SUPPORT" 
		cardinfo.sRarity = "N"
		cardinfo.nCost = 1
		cardinfo.sImgIllu = "card_406.png"
		cardinfo.sImgBase = "SUPPORT"
		def fn(scene, card):
			# 아군에게 방어도(5)를 부여한다.
			scene.nShield += 5
			self.game.sound_play("SHIELD")
		cardinfo.on_use = fn
		self.add(cardinfo)

		return


	##################################
	# 방해카드  601 ~ 
	##################################
	def obstruction_card(self):
		print("방해카드(601~) 로드")

		cardinfo = Cardinfo("601") #어지러움
		cardinfo.sType = "OBSTRUCTION" 
		cardinfo.sRarity = "-"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_601.png"
		cardinfo.sImgBase = "OBSTRUCTION"
		cardinfo.bBattleMelted = True
		cardinfo.bHandMelted = True
		cardinfo.bUnusable = True
		def fn(scene, card):
			print("어지러움카드 사용불가")
		cardinfo.on_use = fn
		self.add(cardinfo)

		return



	##################################
	# 임시카드  901 ~ 
	##################################
	def melt_card(self):
		print("임시카드(901~) 로드")

		#901 퀵샷 복사
		cardinfo = Cardinfo("901") #퀵 샷
		cardinfo.sType = "ATTACK" 
		cardinfo.sRarity = "-"
		cardinfo.nCost = 0
		cardinfo.sImgIllu = "card_005.png"
		cardinfo.sImgBase = "ATTACK"
		cardinfo.bBattleMelted = True
		def fn(scene, card):
			# 적에게 피해(3)를 준다.
			# 그 후에 "퀵 샷"카드를 1장 묘지에 추가한다.
			# 적에게 피격당해 복사된 "퀵 샷"카드가 폐기되는 경우, 복사된 "퀵 샷" 카드와 이 카드를 전부 폐기한다. 
			scene.add_monster_damage(3)
			newCard = Card(self.find("901")) # 퀵 샷
			newCard.sId = card.sId #아이디는 동일하게.
			scene.arrGrave.append(newCard) #무덤에 추가
			self.game.sound_play("GUNSHOT_05")
		cardinfo.on_use = fn
		self.add(cardinfo)

		return















