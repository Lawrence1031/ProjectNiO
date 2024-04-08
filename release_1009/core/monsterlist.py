import pygame
import random
from core.card import Card
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)

class Monsterinfo:
	def __init__(self,sCode):
		self.sCode = sCode

		self.sType = "SMALL" #SMALL, MEDIUM, LARGE, BOSS
		self.sRarity = "N"
		self.nAD = 1
		self.nAP = 0
		self.nHp = 20
		self.nShield = 0
		self.animList = {}
		self.arrMessage = [ 
			"몬스터 대사1"
			, "몬스터 대사2"
		]
		return 


class Monsterlist:
	def __init__(self, game):
		self.game = game
		self.monsterList = {}
		#추가 방법
		monsterinfo = Monsterinfo("000")
		monsterinfo.sType = "SMALL" 
		monsterinfo.sRarity = "N"
		monsterinfo.nAD = 1
		monsterinfo.nAP = 0
		monsterinfo.nHp = 20
		monsterinfo.animList = {}
		self.add(monsterinfo)

		#각 분류별 카드로드
		self.small_monster()
		self.medium_monster()
		self.large_monster()
		self.boss_monster()

		#카드 언어팩 적용. 
		self.set_lang()
		return 

	def add(self, monsterinfo):
		self.monsterList["m"+monsterinfo.sCode] = monsterinfo
		return	

	def find(self, sCode):
		return self.monsterList.get("m"+sCode)

	def set_lang(self):

		arrText = []
		with open("./lang/monster_info_"+self.game.sLangCode+".txt", "r", encoding="utf8") as file:
			for sLine in file:
				arrText.append(sLine.strip())

		langList = {}
		lang = None
		for text in arrText :
			try:

				if text.startswith("#CODE") :
					if lang is not None : 
						langList[lang["sCode"]] = lang
					lang = {}
					lang["sCode"] = text.split(maxsplit=1)[1]
					lang["arrMessage"] = []

				elif lang is not None and text.startswith("#MSG") :
					sMessage = text.split(maxsplit=1)[1]
					lang["arrMessage"].append(sMessage)

			except Exception as e: print(e)

		if lang is not None : 
			langList[lang["sCode"]] = lang

		for k in self.monsterList :
			sCode = self.monsterList[k].sCode
			lang = langList.get(sCode)
			if lang is None : continue
			self.monsterList[k].arrMessage = lang.get("arrMessage", [])

		return 

	def add_shape(self, anim, surface, pos=(0,0), nFrame=10, offset=(0,0)):
		if "arrShape" not in anim : anim["arrShape"] = []
		shape = {}
		shape["img"] = surface
		anim[len(anim["arrShape"])] = shape["img"]
		rect = surface.get_rect()
		shape["rect"] = pygame.Rect(offset[0],offset[1], rect.width,rect.height)
		shape["offset"] = offset
		shape["pos"] = pos
		shape["nFrame"] = nFrame
		anim["arrShape"].append(shape)

		nEndFrame = 0
		for shape in anim["arrShape"] :
			nEndFrame += shape["nFrame"]
			shape["nEndFrame"] = nEndFrame
		anim["nFrame"] = nEndFrame
		return

	##################################
	# 소형 몬스터 001 ~
	##################################
	def small_monster(self):
		print("소형 몬스터(001~) 로드")


		##############
		# 001 청소로봇
		##############
		monsterinfo = Monsterinfo("001")
		monsterinfo.sType = "SMALL" 
		monsterinfo.sRarity = "N"
		monsterinfo.nAD = 2
		monsterinfo.nAP = 5
		monsterinfo.nHp = 30

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_001_01.png") #431 339
		nWidth = 80
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10)
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3)
		self.add_shape(anim, img, (-10,0), 3)
		self.add_shape(anim, img, (-20,0), 3)
		self.add_shape(anim, img, (-10,0), 3)
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8)

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4)
		self.add_shape(anim, anim[0], (2,0), 4)
		self.add_shape(anim, anim[1], (-1,0), 2)
		self.add_shape(anim, anim[0], (1,0), 2)
		self.add_shape(anim, anim[1], (0,0), 2)
		self.add_shape(anim, anim[0], (0,0), 1)
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			#청소로봇
			# 턴1	공격 	1 * 5(5(1d)) 공격 (총 타수 5타)
			# 턴2 	방어 	방어도 5(0.7~0.8a)를 얻는다
			# 턴1, 턴2 반복

			monster.nShield = 0 #실드 초기화 

			monster.nStep += 1
			monster.nSubStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep%2==1 : #공격 
				monster.start_animate("ATTACT") #몬스터 애니메이션 
				
				for i in range(0,5):
					def fn():
						nDamage = nAD*1
						scene.add_hero_damage(nDamage) #영웅 데미지 적용
					self.game.call_delay(fn, 100*i)
			else :
				monster.start_animate("DAMAGE") #몬스터 애니메이션 
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				monster.nShield += rd(nAP*0.8)

			
			self.game.call_delay(next, 1000)

		monsterinfo.on_use = fn

		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		



		##############
		# 002 운반용 드론
		##############
		monsterinfo = Monsterinfo("002")
		monsterinfo.sType = "SMALL" 
		monsterinfo.sRarity = "N"
		monsterinfo.nAD = 7
		monsterinfo.nAP = 1
		monsterinfo.nHp = 40

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_002_01.png") # 292 394
		nWidth = 80
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10)
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3)
		self.add_shape(anim, img, (-10,0), 3)
		self.add_shape(anim, img, (-20,0), 3)
		self.add_shape(anim, img, (-10,0), 3)
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8)

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4)
		self.add_shape(anim, anim[0], (2,0), 4)
		self.add_shape(anim, anim[1], (-1,0), 2)
		self.add_shape(anim, anim[0], (1,0), 2)
		self.add_shape(anim, anim[1], (0,0), 2)
		self.add_shape(anim, anim[0], (0,0), 1)
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 운반용 드론
			# 첫턴		공격 5(1AD)
			# Case 1 	준비단계 nSubStep 이 0이면 1을 모운다.
			# Case 2 	공격단계 nSubStep 이 1이상이면 공격 15(3AD)

			monster.nStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep==1 : #첫공격 
				scene.add_hero_damage(nAD) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nSubStep%2==0 : #준비단계 nSubStep 이 0이면 1을 모운다.
				monster.nSubStep += 1
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT") #물건찾기
			elif monster.nSubStep%2==1 : #공격단계 nSubStep 이 1이상이면 공격 15(3AD)
				monster.nSubStep -= 1
				scene.add_hero_damage(nAD*3) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT") #물건 던지기 

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn

		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		




		##############
		# 003 운반 로봇
		##############
		monsterinfo = Monsterinfo("003")
		monsterinfo.sType = "SMALL" 
		monsterinfo.sRarity = "N"
		monsterinfo.nAD = 10
		monsterinfo.nAP = 7
		monsterinfo.nHp = 40

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_003_01.png") #303 353
		nWidth = 80
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10)
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3)
		self.add_shape(anim, img, (-10,0), 3)
		self.add_shape(anim, img, (-20,0), 3)
		self.add_shape(anim, img, (-10,0), 3)
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8)

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4)
		self.add_shape(anim, anim[0], (2,0), 4)
		self.add_shape(anim, anim[1], (-1,0), 2)
		self.add_shape(anim, anim[0], (1,0), 2)
		self.add_shape(anim, anim[1], (0,0), 2)
		self.add_shape(anim, anim[0], (0,0), 1)
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 운반 로봇
			# Case 1(33.3%)	공격 5(1AD) + 방해 카드 덱에 1장넣기
			# Case 2(33.3%) 방어도 7(1a)을 얻는다 
			# Case 3(33.3%) 공격 5(1AD) 

			monster.nShield = 0 #실드 초기화 
			
			monster.nStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			nCase = random.randint(1, 3)

			if nCase==1 : #공격 5(1AD) + 방해 카드 덱에 1장넣기
				scene.add_hero_damage(nAD) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				scene.arrGrave.append(Card(self.game.cardlist.find("601"))) # 어지러움카드 추가 
			elif nCase==2 : #방어도 7(1a)을 얻는다 
				monster.start_animate("DAMAGE") #몬스터 애니메이션 
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				monster.nShield += rd(nAP)
			else : #공격 5(1AD) 
				scene.add_hero_damage(nAD) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn

		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		


		return

	##################################
	# 중형 몬스터 301 ~
	##################################
	def medium_monster(self):
		print("중형 몬스터(301~) 로드")


		##############
		# 301 소방 로봇
		##############
		monsterinfo = Monsterinfo("301")
		monsterinfo.sType = "MEDIUM" 
		monsterinfo.sRarity = "A"
		monsterinfo.nAD = 8
		monsterinfo.nAP = 10
		monsterinfo.nHp = 60

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_301_01.png") #260 339
		nWidth = 120
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 소방 로봇
			# Case 1 	순찰중입니다.(방어) : 방어도 5~7(0.7~1a)를 얻는다
			# Case 2 	위험 발견!(공격 준비 + 방해) : 다음턴 드로우하는 카드수 -1
			# Case 3 	위험을 제거합니다.(강공격) : 15~20(3~4d) 공격	

			monster.nShield = 0 #실드 초기화 
			
			monster.nStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep%3==1 : #case1 방어도 5~7(0.7~1a)를 얻는다
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				monster.nShield += rd(nAP)
			elif monster.nStep%3==2 : #case2 다음턴 드로우하는 카드수 -1
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				monster.start_animate("ATTACT") #몬스터 애니메이션 
				print("다음턴 드로우하는 카드수 -1 구현필요")
			elif monster.nStep%3==0 : #case3 15~20(3~4d) 공격	
				self.game.pop_text(monster.posHead, monster.arrMessage[2], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*3) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		


		##############
		# 302 운반 로봇
		##############
		monsterinfo = Monsterinfo("302")
		monsterinfo.sType = "MEDIUM" 
		monsterinfo.sRarity = "A"
		monsterinfo.nAD = 8
		monsterinfo.nAP = 1
		monsterinfo.nHp = 120

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_302_01.png") #251 368
		nWidth = 120
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 과학 용품 관리 로봇
			# 첫턴	이곳은 과학실입니다. 실험 도구에 주의하십시오(행동 x) 그냥 넘어가는 턴
			# Case 1 	다음턴 드로우 1장 감소 
			# Case 2 	10(2d) 공격 
			# Case 3 	5~35(1~7d) 랜덤 공격 

			monster.nShield = 0 #실드 초기화 
			
			monster.nStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep==1 : #첫턴 대화 
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
			elif monster.nStep%3==2 : #case1 
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				def fn():
					self.game.pop_text(monster.posHead, monster.arrMessage[2], "UP_MONSTER_TEXT")
				self.game.call_delay(fn, 1500)
				print("드로우 1장 감소 구현 필요 ")
			elif monster.nStep%3==0 : #case2
				self.game.pop_text(monster.posHead, monster.arrMessage[3], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep%3==1 : #case3 
				nRand = random.randint(1, 7)
				self.game.pop_text(monster.posHead, monster.arrMessage[4], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*nRand) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			self.game.call_delay(next, 600)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		




		##############
		# 303 도서실 관리 로봇
		##############
		monsterinfo = Monsterinfo("303")
		monsterinfo.sType = "MEDIUM" 
		monsterinfo.sRarity = "A"
		monsterinfo.nAD = 5
		monsterinfo.nAP = 15
		monsterinfo.nHp = 60

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_303_01.png") #251 368
		nWidth = 120
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 도서실 관리 로봇
			# Case 1 	도서실에 어서오십시오(환영) 플레이어 체력 회복
			# Case 2 	도서실에서는 정숙하십시오(약공격) 5(1d) 공격 + 방어도 5(0.7a)를 얻는다
			# Case 3 	공격 10(2d) 공격

			monster.nShield = 0 #실드 초기화 
			
			monster.nStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep%3==1 : #case1 체력 회복
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				scene.nTotalDamage = 0
			elif monster.nStep%3==2 : #case2 5(1d) 공격 + 방어도 5(0.7a)
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD) #영웅 데미지 적용
				monster.nShield += rd(nAP)
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep%3==0 : #case3 공격 10(2d) 공격
				scene.add_hero_damage(nAD*2) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		







		##############
		# 502 강의 로봇(약화)
		##############
		monsterinfo = Monsterinfo("502")
		monsterinfo.sType = "MEDIUM" 
		monsterinfo.sRarity = "N"
		monsterinfo.nAD = 5
		monsterinfo.nAP = 7
		monsterinfo.nHp = 40

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_502_01.png") #251 368
		nWidth = 120
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 강의 로봇(약화)
			# Case 1 	강의 중에 소란은 안됩니다. (강공격) 10(2d) 공격
			# Case 2 	정숙 하세요(공격 + 방해) 5(1d) 공격 + 플레이어에게 탈진을 1 부여 약공격 + 플레이어 방해요소
			# Case 3 	방어 방어도 5(0.7a)를 얻는다.

			monster.nShield = 0 #실드 초기화 
			
			monster.nStep += 1

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep%3==1 : #case1 체력 회복
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep%3==2 : #case2 5(1d) 공격 + 방어도 5(0.7a)
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD) #영웅 데미지 적용
				print("플레이어 탈진 구현 필요.")
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep%3==0 : #case3 공격 10(2d) 공격
				monster.nShield += rd(nAP*0.7)

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		






		return


	##################################
	# 대형 몬스터 501 ~ 
	##################################
	def large_monster(self):
		print("대형 몬스터(501~) 로드")




		##############
		# 501 강의 로봇
		##############
		monsterinfo = Monsterinfo("501")
		monsterinfo.sType = "LARGE" 
		monsterinfo.sRarity = "A"
		monsterinfo.nAD = 5
		monsterinfo.nAP = 7
		monsterinfo.nHp = 120

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_501_01.png") #251 368
		nWidth = 180
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 강의 로봇
			# 영웅 움직이면 스탭 증가 시작. 
			# Case 1 	강의 중에 소란은 안됩니다. (강공격) 20(4d) 공격
			# Case 2 	정숙 하세요(공격 + 방해) 10(2d) 공격 + 플레이어 1턴 공격카드 사용 불가.
			# Case 3 	방어 방어도 14(2a)를 얻는다.

			monster.nShield = 0 #실드 초기화 
			
			if True : #영웅 움직이면 증가하도록 
				monster.nStep += 1 

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep==0 : 
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
			elif monster.nStep%3==1 : #case1 강의 중에 소란은 안됩니다. (강공격) 20(4d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*4) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep%3==2 : #case2 10(1d) 공격. 플레이어 공격 카드 봉쇄 1턴
				self.game.pop_text(monster.posHead, monster.arrMessage[2], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) #영웅 데미지 적용
				print("플레이어 공격 봉쇄 구현필요 ")
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep%3==0 : #case3 방어 방어도 14(2a)를 얻는다.
				monster.nShield += rd(nAP*2)

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		








		##############
		# 503 선도 로봇
		##############
		monsterinfo = Monsterinfo("503")
		monsterinfo.sType = "LARGE" 
		monsterinfo.sRarity = "A"
		monsterinfo.nAD = 10
		monsterinfo.nAP = 7
		monsterinfo.nHp = 120

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_503_01.png") #330 386
		nWidth = 210
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 선도 로봇 
			# Case 1 	선도 로봇입니다. 교칙을 준수하십시오. / (방해) 다음턴 수비카드 못쓰게 
			# Case 2 	삐빅. 교칙 위반. 교칙 위반 (약공격) / 10(2d) 공격
			# Case 3 	얌전히 선도부의 지도를 따르십시오(강공격) / 20(4d) 공격
			# Case 4 	저항하지 마십시오. 선도부의 지도를 따르십시오.(강공격+) / 25(5d) 공격
			# Case 5 	저항하지 마십시오. 선도부의 지도를 따르십시오.(강공격+) / 30(6d) 공격

			monster.nShield = 0 #실드 초기화 
			
			if True : #영웅 움직이면 증가하도록 
				monster.nStep += 1 

			nAD = monster.get_ad()
			nAP = monster.get_ap()


			if monster.nStep==1 : #case1 선도 로봇입니다. 교칙을 준수하십시오. / (방해) 다음턴 수비카드 못쓰게 
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				print("수비카드 못쓰게 구현")
			elif monster.nStep==2 : #case2 삐빅. 교칙 위반. 교칙 위반 (약공격) / 10(2d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) 
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep==3 : #case3 얌전히 선도부의 지도를 따르십시오(강공격) / 20(4d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[2], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*4) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			elif monster.nStep==4 : #case4 저항하지 마십시오. 선도부의 지도를 따르십시오.(강공격+) / 25(5d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[3], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*5) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 
			else : #case5 저항하지 마십시오. 선도부의 지도를 따르십시오.(강공격+) / 30(6d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[3], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*6) #영웅 데미지 적용
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			self.game.call_delay(next, 300)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		










		return


	##################################
	# 보스 몬스터 801 ~ 
	##################################
	def boss_monster(self):
		print("보스 몬스터(801~) 로드")



		##############
		# 801 경비 로봇
		##############
		monsterinfo = Monsterinfo("801")
		monsterinfo.sType = "BOSS" 
		monsterinfo.sRarity = "S"
		monsterinfo.nAD = 10
		monsterinfo.nAP = 7
		monsterinfo.nHp = 250

		#기본 애니메이션 NORMAL
		monsterinfo.animList = {}	
		img = pygame.image.load("img/monster_801_01.png") #295 277
		nWidth = 300
		nHeight = rd(nWidth * img.get_rect().height / img.get_rect().width) 
		img = pygame.transform.smoothscale(img.convert_alpha(), (nWidth,nHeight))

		anim = {}
		self.add_shape(anim, img, (0,0), 10, (0,-30))
		monsterinfo.animList["NORMAL"] = anim

		#공격 애니메이션 ATTACT
		anim = {}
		self.add_shape(anim, img, (-5,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		self.add_shape(anim, img, (-20,0), 3, (0,-30))
		self.add_shape(anim, img, (-10,0), 3, (0,-30))
		monsterinfo.animList["ATTACT"] = anim

		#공격 당하는 애니메이션 DAMAGE
		img = img.copy()
		rect = img.get_rect()
		img2 = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
		img2.fill((0,0,0))
		img.blit(img2, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

		anim = {}
		self.add_shape(anim, img, (0,0), 8, (0,-30))

		img = img.copy()
		img2 = pygame.Surface((48,48), pygame.SRCALPHA)
		img2.fill((255,255,255,0))
		img2.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

		self.add_shape(anim, img, (-2,0), 4, (0,-30))
		self.add_shape(anim, anim[0], (2,0), 4, (0,-30))
		self.add_shape(anim, anim[1], (-1,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (1,0), 2, (0,-30))
		self.add_shape(anim, anim[1], (0,0), 2, (0,-30))
		self.add_shape(anim, anim[0], (0,0), 1, (0,-30))
		monsterinfo.animList["DAMAGE"] = anim

		def fn(scene, monster, next):
			# 경비 로봇 
			# 첫턴 		아직 하교 시간이 아닙니다 교내로 돌아가십시오. (견제, 약공격) / 10(2d) 공격
			# Case 1 	지시에 따르십시오(약공격) / 10(2d) * 2 공격 (타수 2타)
			# Case 2 	상황 확인중(관측) / 방어도 7~10(1a~1.5a)를 얻는다
			# Case 3 	변수 발생 변수 발생(강공격) / 30(6d) 공격
			# Case 4 	지시에 따르십시오(약공격) / 10(2d) * 2 공격 (타수 2타)
			# Case 5 	포박을 시도합니다(방해) / 탈진 1부여 + 동료카드 못쓰게 1턴 봉인
			# Case 6 	변수 발생 변수 발생(강공격) / 20(4d) 공격

			monster.nShield = 0 #실드 초기화 
			
			monster.nStep += 1 

			nAD = monster.get_ad()
			nAP = monster.get_ap()

			if monster.nStep==1 : # 아직 하교 시간이 아닙니다 교내로 돌아가십시오. (견제, 약공격) / 10(2d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[0], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) 
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			elif monster.nStep%6==2 : # Case 1 	지시에 따르십시오(약공격) / 10(2d) * 2 공격 (타수 2타)
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) 
				monster.start_animate("ATTACT") #몬스터 애니메이션 

				def fn():
					scene.add_hero_damage(nAD*2) #영웅 데미지 적용
				self.game.call_delay(fn, 200)

			elif monster.nStep%6==3 : # Case 2 	상황 확인중(관측) / 방어도 7~10(1a~1.5a)를 얻는다
				self.game.pop_text(monster.posHead, monster.arrMessage[2], "UP_MONSTER_TEXT")
				monster.nShield += rd(nAP*1.5)

			elif monster.nStep%6==4 : # Case 3 	변수 발생 변수 발생(강공격) / 30(6d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[3], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*6) 
				monster.start_animate("ATTACT") #몬스터 애니메이션 

			elif monster.nStep%6==5 : # Case 4 	지시에 따르십시오(약공격) / 10(2d) * 2 공격 (타수 2타)
				self.game.pop_text(monster.posHead, monster.arrMessage[1], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*2) 
				monster.start_animate("ATTACT") #몬스터 애니메이션 

				def fn():
					scene.add_hero_damage(nAD*2) #영웅 데미지 적용
				self.game.call_delay(fn, 100)

			elif monster.nStep%6==0 : # Case 5 	포박을 시도합니다(방해) / 탈진 1부여 + 동료카드 못쓰게 1턴 봉인
				self.game.pop_text(monster.posHead, monster.arrMessage[4], "UP_MONSTER_TEXT")
				scene.hero.add_buff("004")
				print("동료카드 봉쇄 구현필요")

			elif monster.nStep%6==1 : # Case 6 	변수 발생 변수 발생(강공격) / 20(4d) 공격
				self.game.pop_text(monster.posHead, monster.arrMessage[3], "UP_MONSTER_TEXT")
				scene.add_hero_damage(nAD*4) 
				monster.start_animate("ATTACT") #몬스터 애니메이션 


			self.game.call_delay(next, 400)

		monsterinfo.on_use = fn
		self.add(monsterinfo) # 몬스터 리스트에 몬스터 정보 추가 
		




		return







