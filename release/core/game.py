import sys
import pygame
import json
import hashlib
from core.cardlist import Cardlist
from core.card import Card
from core.monsterlist import Monsterlist
from core.poptext import Poptext
from core.sound import Sound
from PIL import Image #pip install pillow
import random
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)

class Game:
	def __init__(self):
		self.bRunning = True
		self.bPopSetting = False
		self.bToggleScreen = False
		self.nFps = 30
		self.arrWindowSize = (1280, 720)

		self.arrScene = []
		self.scNow = None
		self.sBgmName = ""
		self.nFrame = 0

		self.sLangCode = "kr"

		self.arrDelayRequest = []
		self.fade = pygame.Surface(self.arrWindowSize, pygame.SRCALPHA)
		self.fade.fill((0,0,0))

		self.arrDeck = []
		self.arrDiscard = []
		self.nTotalDamage = 0

		self.nRemainNio = 0
		self.nMonsterN = 0
		self.nMonsterA = 0
		self.nMonsterS = 0
		self.nMonsterEx = 0



		return
		


	def load(self):
		pygame.init()
		self.setting()
		self.cardlist = Cardlist(self)
		self.monsterlist = Monsterlist(self)
		self.poptext = Poptext(self)
		self.sound = Sound(self)

		#세팅 팝업.
		from scene.s00_setting import Setting
		self.scSetting = Setting(self)

		if len(sys.argv) > 1 and sys.argv[1]=="test" : 
			#""" 테스트 
			# self.nFps = 1
			# from scene.s03_intro import Intro
			# self.arrScene.append(Intro(self))
			# from scene.s04_deckselect import Deckselect
			# self.arrScene.append(Deckselect(self))
			from scene.s06_stage1 import Stage1
			self.arrScene.append(Stage1(self))
			# from scene.s07_textevent import Textevent
			# self.arrScene.append(Textevent(self))
			from scene.s08_battleevent import Battleevent
			self.arrScene.append(Battleevent(self))
			# from scene.s09_scenarioevent import Scenarioevent
			# self.arrScene.append(Scenarioevent(self))
			# from scene.s10_cardadd import Cardadd
			# self.arrScene.append(Cardadd(self))
			# from scene.s11_cardspace import Cardspace
			# self.arrScene.append(Cardspace(self))
			# from scene.s12_result import Result
			# self.arrScene.append(Result(self))
			# from scene.s13_cardshop import Cardshop
			# self.arrScene.append(Cardshop(self))

			arrDeck = []
			arrDeck.append(Card(self.cardlist.find("002")))
			arrDeck.append(Card(self.cardlist.find("002")))
			arrDeck.append(Card(self.cardlist.find("002")))
			arrDeck.append(Card(self.cardlist.find("003")))
			arrDeck.append(Card(self.cardlist.find("003")))
			arrDeck.append(Card(self.cardlist.find("406")))
			arrDeck.append(Card(self.cardlist.find("406")))
			arrDeck.append(Card(self.cardlist.find("406")))
			arrDeck.append(Card(self.cardlist.find("001")))
			arrDeck.append(Card(self.cardlist.find("001")))
			self.arrDeck = arrDeck
			# self.set_text_scene("102")
			self.set_battle_scene("test")
			# self.set_scenario_scene("002")
			# self.set_cardadd_scene("test")
			# self.set_stage_cardspace_scene()
			# self.set_battle_cardspace_scene(arrDeck, arrDeck, arrDeck)
			# self.set_result_scene()
			# self.set_cardshop_scene(10)
			# self.set_scene("Stage1")
			# self.pop_setting()

			# self.save_file()
			# self.load_file()

			return
			#"""

		#로딩 화면
		from scene.s01_loading import Loading
		scloading = Loading(self)
		self.arrScene.append(scloading)
		pygame.init()
		self.setting()
		scloading.update()
		scloading.update_loading_bar(10)

		#씬
		from scene.s02_lobby import Lobby
		self.arrScene.append(Lobby(self))
		scloading.update_loading_bar(15)
		from scene.s03_intro import Intro
		self.arrScene.append(Intro(self))
		scloading.update_loading_bar(20)
		from scene.s04_deckselect import Deckselect
		self.arrScene.append(Deckselect(self))
		scloading.update_loading_bar(28)
		from scene.s05_teambuild import Teambuild
		self.arrScene.append(Teambuild(self))
		scloading.update_loading_bar(36)
		from scene.s06_stage1 import Stage1
		self.arrScene.append(Stage1(self))
		scloading.update_loading_bar(44)
		from scene.s07_textevent import Textevent
		self.arrScene.append(Textevent(self))
		scloading.update_loading_bar(52)
		from scene.s08_battleevent import Battleevent
		self.arrScene.append(Battleevent(self))
		scloading.update_loading_bar(60)
		from scene.s09_scenarioevent import Scenarioevent
		self.arrScene.append(Scenarioevent(self))
		scloading.update_loading_bar(68)
		from scene.s10_cardadd import Cardadd
		self.arrScene.append(Cardadd(self))
		scloading.update_loading_bar(76)
		from scene.s11_cardspace import Cardspace
		self.arrScene.append(Cardspace(self))
		scloading.update_loading_bar(84)
		from scene.s12_result import Result
		self.arrScene.append(Result(self))
		scloading.update_loading_bar(92)
		from scene.s13_cardshop import Cardshop
		self.arrScene.append(Cardshop(self))
		scloading.update_loading_bar(100)
		pygame.time.delay(100)

		#로딩 완료시.
		self.set_scene("Lobby")
		self.get_scene("Loading").unload()
		return


	def setting(self): #기본 설정 
		pygame.display.set_caption("Nio")
		
		# 아이콘 설정
		pygame.display.set_icon(pygame.image.load("./img/icon.png"))

		# self.screen = pygame.display.set_mode(self.arrWindowSize, pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode(self.arrWindowSize)
		self.fps = pygame.time.Clock()
		return  

	def call_delay(self, fn, nTime): #시간 이벤트 
		if not callable(fn) : return
		request = {}
		request["fn"] = fn 
		request["nFrame"] = rd((nTime*self.nFps)/1000)
		if request["nFrame"] < 2 : request["nFrame"] = 1
		self.arrDelayRequest.append(request)
		return 

	def check_request(self): #시간 이벤트 체크 함수 
		nCnt = len(self.arrDelayRequest)
		if nCnt <= 0: return

		for i in range(nCnt-1, -1, -1):
			self.arrDelayRequest[i]["nFrame"] -= 1
			if self.arrDelayRequest[i]["nFrame"] <= 0:
				fn = self.arrDelayRequest[i]["fn"]
				self.arrDelayRequest.pop(i)
				fn()
		return 


	def discard_deck(self):
		nIndex = random.randint(1, len(self.arrDeck))-1
		if nIndex<0 : 
			print("폐기할 카드 없음!!!")
			self.set_scene("Lobby")
			return
		card = self.arrDeck.pop(nIndex-1)
		self.arrDiscard.append(card)
		return	

	def get_scene(self, sSceneName): #씬 이름으로가져오기 
		for sc in self.arrScene :
			if sc.check_name(sSceneName) : return sc
		return None

	def reset_scene(self, sSceneName): #씬 초기화 호출 
		sc = self.get_scene(sSceneName)
		if sc is not None and hasattr(sc,"reset"):
			getattr(sc,"reset")()
		return

	def set_scene(self, sSceneName): #씬 변경 
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene(sSceneName)
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
		return

	def fade_scene(self, sSceneName): #씬 호출 
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = 1.5*self.nFps
		def fn():
			self.set_scene(sSceneName)
			return 
		self.call_delay(fn, 500)
		return 

	def fade_scene_save(self, sSceneName): #씬 호출 그리고 저장 
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = 1.5*self.nFps
		def fn():
			self.set_scene(sSceneName)
			self.save_file()
			return 
		self.call_delay(fn, 500)
		return 

	def set_text_scene(self, sName): #텍스트 이벤트씬 변경.
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Textevent")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_text(sName)
		return 

	def fade_text_scene(self, sName): #텍스트 이벤트씬 호출.
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = 1.5*self.nFps
		def fn():
			self.set_text_scene(sName)
			return 
		self.call_delay(fn, 500)
		return 

	def set_battle_scene(self, sName): #배틀 이벤트씬 변경.
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Battleevent")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_battle(sName)
		return 

	def fade_battle_scene(self, sName): #배틀 이벤트씬 호출.
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = 1.5*self.nFps
		def fn():
			self.set_battle_scene(sName)
			return 
		self.call_delay(fn, 500)
		return 

	def set_scenario_scene(self, sName): #시나리오 이벤트씬 변경.
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Scenarioevent")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_scenario(sName)
		return 

	def fade_scenario_scene(self, sName): #시나리오 이벤트씬 호출.
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = 1.5*self.nFps
		def fn():
			self.set_scenario_scene(sName)
			return 
		self.call_delay(fn, 500)
		return 


	def set_cardadd_scene(self, sName): #카드추가 씬 변경.
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Cardadd")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_cardadd(sName)
		return 

	def fade_cardadd_scene(self, sName): #카드추가 씬 호출.
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = 1.5*self.nFps
		def fn():
			self.set_cardadd_scene(sName)
			return 
		self.call_delay(fn, 500)
		return 

	def set_stage_cardspace_scene(self): #스테이지 카드공간 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Cardspace")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_stage_cardspace()
		return 

	def fade_stage_cardspace_scene(self): #스테이지 카드공간 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = self.nFps
		def fn():
			self.set_stage_cardspace_scene()
			return 
		self.call_delay(fn, 300)
		return 

	def set_battle_cardspace_scene(self, arrDeck, arrGrave, arrDiscard): #베틀 카드공간 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Cardspace")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_battle_cardspace(arrDeck, arrGrave, arrDiscard)
		return 

	def fade_battle_cardspace_scene(self, arrDeck, arrGrave, arrDiscard): #베틀 카드공간 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = self.nFps
		def fn():
			self.set_battle_cardspace_scene(arrDeck, arrGrave, arrDiscard)
			return 
		self.call_delay(fn, 300)
		return 

	def set_result_scene(self): #결과 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Result")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.cal_result()
		return 

	def fade_result_scene(self): #결과 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = self.nFps
		def fn():
			self.set_result_scene()
			return 
		self.call_delay(fn, 300)
		return 

	def fade_result_scene_save(self): #결과 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = self.nFps
		def fn():
			self.set_result_scene()
			self.save_file()
			return 
		self.call_delay(fn, 300)
		return 

	def set_cardshop_scene(self, nNio): #카드샵 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		sc = self.get_scene("Cardshop")
		if sc is not None : 
			self.scNow = sc
			self.scNow.bControl = True
			self.scNow.load_cardshop(nNio)
		return 

	def fade_cardshop_scene(self, nNio): #카드샵 씬
		if self.scNow is not None : 
			self.scNow.bControl = False
		self.nFrame = self.nFps
		def fn():
			self.set_cardshop_scene(nNio)
			return 
		self.call_delay(fn, 300)
		return 


	def check_fade(self):
		if self.nFrame==0 : return 
		self.nFrame -= 1

		nTime = self.nFrame/self.nFps

		if nTime > 1 :
			self.fade.set_alpha(255*max(3-2*nTime,0))
		elif nTime > 0.5 :
			self.fade.set_alpha(255)
		else :
			self.fade.set_alpha(255*min(2*nTime,1))

		self.screen.blit(self.fade,(0,0))
		return 

	def check_bgm(self):
		if self.sBgmName!=self.scNow.sSceneName : 
			self.sBgmName = self.scNow.sSceneName
			self.sound.play(self.scNow.sSceneName)
		return 

	def sound_play(self, sCode):
		self.sound.play(sCode)	
		return

	def sound_size(self, sType="BG", nUpSize=0):
		if sType.upper()=="BG" :
			self.sound.nVolumeBgm = min(1,max(0,round(self.sound.nVolumeBgm+nUpSize, 2)))
			if self.scNow is not None : 
				print(self.scNow.sSceneName)
				self.sound.play(self.scNow.sSceneName)
			return self.sound.nVolumeBgm
		self.sound.nVolumeSe = min(1,max(0,round(self.sound.nVolumeSe+nUpSize, 2)))
		return self.sound.nVolumeSe

	def get_stage_name(self):
		for sc in self.arrScene :
			if sc.check_name("Stage1") : 
				self.scNow = sc
				return self.scNow.location
		return ""


	def pop_text(self, pos, sText, sType="UP_TEXT", sTextAlign="CENTER"):
		self.poptext.add_text(pos, sText, sType, sTextAlign)
		return



	def save_file(self):
		sSceneName = "Result" # 스테이지, 결과 씬만 저장.
		sSceneData = {}
		if( self.scNow.sSceneName=="Stage1" 
			or self.scNow.sSceneName=="Stage2" 
			or self.scNow.sSceneName=="Stage3" ): 
			sSceneName = self.scNow.sSceneName
			sSceneData = self.scNow.get_stage_data()

		arrDeck = []
		for card in self.arrDeck:
			arrDeck.append(card.sCode)
		arrDiscard = []
		for card in self.arrDiscard:
			arrDiscard.append(card.sCode)

		data = {
			"sSceneName" : sSceneName
			, "sSceneData" : sSceneData
			, "arrDeck" : arrDeck
			, "arrDiscard" : arrDiscard
			, "nTotalDamage" : self.nTotalDamage
			, "nRemainNio" : self.nRemainNio
			, "nMonsterN" : self.nMonsterN
			, "nMonsterA" : self.nMonsterA
			, "nMonsterS" : self.nMonsterS
			, "nMonsterEx" : self.nMonsterEx
		}

		sJson = json.dumps(data)
		eData = (sJson+"bkchoi1018").encode()
		sHash = hashlib.sha256(eData).hexdigest()
		sFile = sHash+"#"+sJson
		with open("save.txt", "w") as file:
			file.write(sFile)
		return 

	def load_file(self):
		try:
			sFile = ""
			with open("save.txt", "r") as file:
				sFile = file.read()

			arr = sFile.split("#",maxsplit=1)
			sHash = arr[0]
			sJson = arr[1]
			eData = (sJson+"bkchoi1018").encode()
			sHash2 = hashlib.sha256(eData).hexdigest()
			bSave = (sHash==sHash2)
		except: 
			bSave = False

		sSceneName = "Deckselect"
		if not bSave : #비정상 세이브 파일
			print("세이브 파일 비정상")
			#초기화 
			self.nTotalDamage = 0
			self.nRemainNio = 0
			self.nMonsterN = 0
			self.nMonsterA = 0
			self.nMonsterS = 0
			self.nMonsterEx = 0
		else :
			data = json.loads(sJson)
			sSceneName = data["sSceneName"]
			
			arrDeck = []
			for i in range(0, len(data["arrDeck"])):
				arrDeck.append(Card(self.cardlist.find(data["arrDeck"][i])))
			self.arrDeck = arrDeck

			arrDiscard = []
			for i in range(0, len(data["arrDiscard"])):
				arrDiscard.append(Card(self.cardlist.find(data["arrDiscard"][i])))
			self.arrDiscard = arrDiscard
			
			self.nTotalDamage = data["nTotalDamage"]
			self.nRemainNio = data["nRemainNio"]
			self.nMonsterN = data["nMonsterN"]
			self.nMonsterA = data["nMonsterA"]
			self.nMonsterS = data["nMonsterS"]
			self.nMonsterEx = data["nMonsterEx"]

		#씬 변경.
		if( sSceneName=="Stage1" 
			or sSceneName=="Stage2" 
			or sSceneName=="Stage3" ): 
			sc = self.get_scene(sSceneName)
			sc.set_stage_data(data["sSceneData"])
			self.fade_scene(sSceneName)
		elif sSceneName=="Result" :
			self.fade_result_scene()
		return 


	def pop_setting(self):
		self.sound_play("CURSOR")
		self.bPopSetting = not self.bPopSetting 
		self.scSetting.bControl = self.bPopSetting 
		self.scNow.bControl = not self.bPopSetting
		return 	


	def check_event(self, e):
		if e.type == pygame.QUIT:
			self.bRunning = False 
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: #esc키
			self.pop_setting()
		elif self.bPopSetting and self.scSetting.bControl:
			if( ( e.type == pygame.MOUSEBUTTONDOWN or ( self.bToggleScreen and e.type == pygame.MOUSEBUTTONUP ))
				and hasattr(self.scSetting, "on_mouse_button_down" ) ):
				self.scSetting.on_mouse_button_down(e)
			else : self.scSetting.event(e)
		elif self.scNow is not None and self.scNow.bControl : 
			if( ( e.type == pygame.MOUSEBUTTONDOWN or ( self.bToggleScreen and e.type == pygame.MOUSEBUTTONUP ))
				and hasattr(self.scNow, "on_mouse_button_down" ) ):
				self.scNow.on_mouse_button_down(e)
			else : self.scNow.event(e)

		return 


	def run(self):
		while self.bRunning:
			deltaTime = self.fps.tick(self.nFps)

			for e in pygame.event.get() : self.check_event(e)

			self.check_request()

			if self.scNow is not None : self.scNow.update()

			if self.bPopSetting : self.scSetting.update()
			
			self.check_fade()

			self.poptext.update()
			self.poptext.draw()

			pygame.display.update()

			self.check_bgm()


		pygame.quit()







