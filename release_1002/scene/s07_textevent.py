from core.scene import Scene
from core.dialog import Dialog
from core.div import Div
import pygame
# from PIL import Image #pip install pillow
import random


class Textevent(Scene):
	def __init__(self, game):
		super().__init__(game, "Textevent")
		self.imgBg = None
		self.imgEvent = None

		self.load()
		self.load_text("001")

		return 

	def load(self):
		self.load_bg("./img/place_classroom_01.png") #배경 이미지 

		#이벤트 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		#타이틀 
		div = Div(self.game)
		div.width(600)
		div.height(55)
		img = pygame.Surface((1,1), pygame.SRCALPHA)
		img.set_alpha(230)
		img.fill((26, 18, 11))
		div.surface(img)
		div.padding_top(0)
		# div.padding_left(5)
		div.text("title")
		div.top(10)
		div.left(20)
		self.title = div

		#텍스트 
		dialog = Dialog(self.game)
		dialog.width(700)
		dialog.height(430)
		dialog.top(100)
		dialog.left(30)
		dialog.font_size(30)
		dialog.add_typing("text")
		self.dialog = dialog


		#버튼 그룹 
		self.groupBt = pygame.sprite.Group()

		#버튼1 
		div = Div(self.game)
		div.width(500)
		div.height(55)
		img = pygame.image.load("img/bt5_off.png")
		div.surface(img)
		img = pygame.image.load("img/bt5_on.png")
		div.surfaceHover(img)
		div.padding_top(6)
		div.padding_left(30)
		div.font_size(25)
		div.text("공격한다.")
		div.top(330)
		div.left(740)
		div.bDisplay = False
		div.on_click = print
		self.groupBt.add(div)
		self.bt1 = div

		#버튼2 
		div = Div(self.game)
		div.width(500)
		div.height(55)
		img = pygame.image.load("img/bt5_off.png")
		div.surface(img)
		img = pygame.image.load("img/bt5_on.png")
		div.surfaceHover(img)
		div.padding_top(6)
		div.padding_left(30)
		div.font_size(25)
		div.text("기뉴를 공격한다.")
		div.top(400)
		div.left(740)
		div.bDisplay = False
		div.on_click = print
		self.groupBt.add(div)
		self.bt2 = div


		#버튼3 
		div = Div(self.game)
		div.width(500)
		div.height(55)
		img = pygame.image.load("img/bt5_off.png")
		div.surface(img)
		img = pygame.image.load("img/bt5_on.png")
		div.surfaceHover(img)
		div.padding_top(6)
		div.padding_left(30)
		div.font_size(25)
		div.text("고구마 폭탄을 던진다.")
		div.top(470)
		div.left(740)
		div.bDisplay = False
		div.on_click = print
		self.groupBt.add(div)
		self.bt3 = div




		#버튼 이미지 
		spriteBt = pygame.image.load("img/bt.png") #157, 120(60)
		surfaceBt = spriteBt.subsurface(pygame.Rect(0, 60, 157, 60))
		surfaceBtHover = spriteBt.subsurface(pygame.Rect(0, 0, 157, 60))

		div = Div(self.game)
		div.surface(surfaceBt)
		div.surfaceHover(surfaceBtHover)
		div.text("확인")
		div.fit_text()
		div.width(100)
		div.height(60)
		div.left( (self.game.arrWindowSize[0]-100)/2 )
		div.top( (self.game.arrWindowSize[1]+300)/2 )
		div.padding_left(20)
		div.on_click = print
		self.btOk = div

		self.alert = pygame.Surface((1,1), pygame.SRCALPHA)
		self.bAlert = False
		self.nCode = 0
		return 


	def load_bg(self, sName):
		#배경
		img = pygame.image.load(sName)
		img = pygame.transform.smoothscale(img, self.game.arrWindowSize)
		
		#전체 반투명 배경
		surf = pygame.Surface(self.game.arrWindowSize, pygame.SRCALPHA)
		surf.set_alpha(90)
		surf.fill((0, 0, 0))
		img.blit(surf,(0,0))

		#본문 배경 
		surf = pygame.Surface((self.game.arrWindowSize[0]-40,470), pygame.SRCALPHA)
		surf.set_alpha(230)
		surf.fill((26, 18, 11))
		img.blit(surf,(20,80))
		if self.imgBg is not None : del self.imgBg
		self.imgBg = img
		return 

	def set_event_img(self, surf):
		#이벤트 이미지 
		if surf.get_height()!=200 :
			surf = pygame.transform.smoothscale(surf, (200*surf.get_width()/surf.get_height(),200))
		nWidth = min(500, surf.get_width())
		self.imgEvent = surf.subsurface(pygame.Rect(0, 0, nWidth, 200))
		return

	def load_text(self, sName):
		print("s07_textevent.load_text()",sName)


		#시나리오 초기화 
		for bt in self.groupBt : bt.bDisplay = False
		self.dialog.clear_text()

		self.bAlert = False
		self.nCode = 0

		#시나리오함수 호출 
		if hasattr(self,"te_"+sName): 
			getattr(self,"te_"+sName)()
		else :
			print("함수정의 필요!!")

		return 	



	def pop_alert(self, n, s):
		self.nCode = n
		nAlertWidth = 500 #알람 너비 

		#텍스트 
		arrShapeText = []
		font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 30)

		nSize = 0
		shapeText = None
		shapeTextLast = None
		while s!="" and nSize<100 :
			shapeText = font.render(s[0:nSize], True, (255, 255, 255))
			if s==s[0:nSize] : break

			if nAlertWidth - 40 < shapeText.get_width() :
				arrShapeText.append(shapeTextLast)
				s = s[nSize-1:]
				nSize = 0
				shapeText = None
				shapeTextLast = None

			elif s[nSize]=="\n" :
				arrShapeText.append(shapeText)
				s = s[nSize+1:]
				nSize = 0
				shapeText = None
				shapeTextLast = None

			else :
				shapeTextLast = shapeText
			nSize += 1

		if shapeText is not None :
			arrShapeText.append(shapeText)


		nTextHeight = 0
		for st in arrShapeText :
			nTextHeight += st.get_height()


		#알림창 전체
		nAlertHegiht = nTextHeight + 35 + self.btOk.height()
		img = pygame.Surface((nAlertWidth,nAlertHegiht), pygame.SRCALPHA)
		img.set_alpha(250)
		img.fill((7,21,35))
		pygame.draw.rect(img, (50, 121, 165), (5, 5, 490, nAlertHegiht-10), 3)

		nAlertTop = (self.game.arrWindowSize[1]-nAlertHegiht)/2
		self.posAlert = ( (self.game.arrWindowSize[0]-nAlertWidth)/2, nAlertTop )

		#텍스트 붙이기. 
		for i in range(0, len(arrShapeText)) :
			img.blit(arrShapeText[i], (20,10+ arrShapeText[i].get_height()*i))


		#버튼 
		self.btOk.top(nAlertTop + nTextHeight + 20 )

		self.alert = img 
		self.bAlert = True
		return 	
		

	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				self.dialog.end_typing()
				for bt in self.groupBt :
					if bt.collidepoint(e.pos) and bt.bDisplay and not self.bAlert :
						self.game.sound_play("CURSOR")
						bt.on_click()
						break
				if self.btOk.collidepoint(e.pos) and self.bAlert :
					self.game.sound_play("CURSOR")
					self.btOk.on_click(self.nCode)



		except Exception as e: print(e)

	def update(self):
		try:

			# 커서 변경.
			pos = pygame.mouse.get_pos()
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			if( ( self.bt1.collidepoint(pos) and self.bt1.bDisplay and not self.bAlert )
				or ( self.bt2.collidepoint(pos) and self.bt2.bDisplay and not self.bAlert )
				or ( self.bt3.collidepoint(pos) and self.bt3.bDisplay and not self.bAlert ) 
				or ( self.btOk.collidepoint(pos) and self.bAlert ) ):
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
			

			#배경
			self.game.screen.blit(self.imgBg, (0, 0))

			#타이틀 
			self.title.update()
			self.title.draw()

			#이벤트 이미지 
			#300일때 840 이면 150 빼면 990 - 절반 이다. 

			self.game.screen.blit(self.imgEvent, (990-self.imgEvent.get_width()/2, 100))

			self.dialog.update()
			self.dialog.draw()

			self.groupBt.update()

			if self.bt1.bDisplay : self.bt1.draw()
			if self.bt2.bDisplay : self.bt2.draw()
			if self.bt3.bDisplay : self.bt3.draw()


			if self.bAlert : 
				self.game.screen.blit(self.alert, self.posAlert)

				self.btOk.update()
				self.btOk.draw()
				
		except Exception as e: print(e)
	

	def read_text(self, sName):
		arrScenario = []
		with open("./lang/"+sName+"_"+self.game.sLangCode+".txt", "r", encoding="utf8") as file:
			for sLine in file:
				arrScenario.append(sLine.strip())
		return arrScenario

	def set_scenario(self, arr):
		#텍스트 출력. 
		lastText = None
		for text in arr :
			if text.startswith("#TTL") : #타이틀 
				self.title.text(text.split(maxsplit=1)[1])
			elif text.startswith("#Q1") : #Q1 
				self.bt1.text(text.split(maxsplit=1)[1])
				self.bt1.bDisplay = True
			elif text.startswith("#Q2") : #Q1 
				self.bt2.text(text.split(maxsplit=1)[1])
				self.bt2.bDisplay = True
			elif text.startswith("#Q3") : #Q1 
				self.bt3.text(text.split(maxsplit=1)[1])
				self.bt3.bDisplay = True
			elif text.startswith("#END") : #END
				break 
			else :
				if lastText is not None : self.dialog.add_text(lastText)
				lastText = text
		self.dialog.add_typing(lastText)
		return 


	"""
	이하 텍스트 이벤트 리스트 
	"""
	def te_001(self):
		self.load_bg("img/place_classroom_01.png") #배경 이미지 
		self.set_scenario(self.read_text("te_001")) #시나리오 파일 읽기. 

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 


		def fn(): #Q1 사람의 형상으로 보인다. 말을 걸어본다.
			nCode = 1
			sText = "전투를 진행합니다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): #Q2 기뉴를 공격한다.
			
			nCode = 2
			sText = "폐기된 카드를 덱으로 가져옵니다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn

		def fn(): #Q3 고구마 폭탄을 던진다.

			nCode = 3
			sText = "적을 해치웠습니다.\n경험치 +3"
			self.pop_alert(nCode, sText)
			return
		self.bt3.on_click = fn


		def fn(nCode): #팝업창 확인.
			self.game.fade_scene_save("Stage1")

			if nCode==1 :
				self.game.fade_scene_save("Stage1")

			elif nCode==2 :
				self.game.fade_scene_save("Stage1")

			elif nCode==3 :
				self.game.fade_scene_save("Stage1")

			return
		self.btOk.on_click = fn

		return


	#테스트 씬
	def te_test(self):
		#배경 이미지 
		self.load_bg("img/intro_002.png") 

		#시나리오 파일 읽기. 파일명 
		arrScenario = self.read_text("te_test")
		self.set_scenario(arrScenario) #파일 분석.

		#시나리오 이미지 
		img = pygame.image.load("img/char_02.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 


		def fn(): #Q1 적을 공격한다.
			nRand = random.randint(1, 100)
			print(nRand)

			if nRand <=50 : 
				nCode = 10 
				sText ="10%확률로 죽었습니다."

			else : 
				nCode = 90 
				sText = "90퍼 확률로 뒈졌다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): #Q2 기뉴를 공격한다.
			
			nCode = 2
			sText = "폐기된 카드를 덱으로 가져옵니다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn


		def fn(nCode): #팝업창 확인.
			self.game.fade_scene_save("Stage1")

			if nCode==1 :
				self.game.fade_scene_save("Stage1")

			elif nCode==2 :
				self.game.fade_scene_save("Stage1")

			return
		self.btOk.on_click = fn

		return


	#교실에서 의문의 존재와 조우
	def te_101(self):
		self.load_bg("img/place_classroom_01.png") #배경 이미지 
		self.set_scenario(self.read_text("te_101")) #파일 분석.

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): #Q1 사람의 형상으로 보인다. 말을 걸어본다.
			# 50%	정체는 학교 친구였다.	새로운 동료를 얻는다
			# 50%	정체는 로봇이였다.	적과 전투

			nRand = random.randint(1, 100)
			if nRand <=50 : 
				nCode = 1 
				sText = "정체는 학교 친구였다. 새로운 동료를 얻는다"
			else : 
				nCode = 2
				sText = "정체는 로봇이였다. 적과 전투"
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): #Q2 위험한건 최대한 피하자. 돌아간다.
			self.game.fade_scene_save("Stage1")
			return
		self.bt2.on_click = fn


		def fn(nCode): #팝업창 확인.
			if nCode==1 : #동료 해금
				print("동료 해금 개발 필요.")
				self.game.fade_scene_save("Stage1")

			elif nCode==2 : #교실 몬스터와 전투
				sCode = random.choice(["001","002","003","004","005","006"])
				self.game.fade_battle_scene(sCode)

			return
		self.btOk.on_click = fn

		return



	#교실에서 아이템 획득 관련 이벤트
	def te_102(self):
		self.load_bg("img/place_classroom_01.png") #배경 이미지 
		self.set_scenario(self.read_text("te_102")) #시나리오 파일 읽기

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 물건 더미를 살펴본다.
			#50%	물건 더미에서 쓸만한 카드를 발견했다.		새로운 카드를 획득
			#25%	물건 더미에서 책을 찾아 읽었다.			경험치 X 획득
			#25%	물건 더미를 살펴보다가 상처를 입었다.		피격게이지 5~10정도 소비 -> 카드 한장 랜덤 폐기
			
			nRand = random.randint(1, 100)
			print(nRand)
			if nRand <=50 : 
				nCode = 1 
				sText = "물건 더미에서 쓸만한 카드를 발견했다."
			elif nRand <=75 : 
				nCode = 2
				sText = "물건 더미에서 책을 찾아 읽었다.(+10 Nio)"
			else :
				nCode = 3
				sText = "물건 더미를 살펴보다가 상처를 입었다.(랜덤카드 폐기)"
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q2 물건 더미를 살펴보지 않는다.
			#100%	-	이벤트 종료
			self.game.fade_scene_save("Stage1")
			return
		self.bt2.on_click = fn


		def fn(nCode): #팝업창 확인.

			if nCode==1 : #카드 획득
				#랜덤으로 카드 1장 획득 팝업
				self.game.fade_cardadd_scene("102")

			elif nCode==2 : #경험치 획득
				self.game.nRemainNio += 10
				self.game.fade_scene_save("Stage1") 

			elif nCode==3 : #피격
				self.game.discard_deck() # 카드삭제
				self.game.fade_scene_save("Stage1")

			return
		self.btOk.on_click = fn

		return



	#복도 혹은 계단에서 적과 조우
	def te_103(self):
		self.load_bg("img/place_classroom_01.png") #배경 이미지 
		self.set_scenario(self.read_text("te_103")) #시나리오 파일

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 적과 전투한다.
			#100%	-	적과 전투
			nCode = 1
			sText = "전투에 돌입한다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q2 물러난다.
			#25%	도망에 실패했다.	적과 전투한다.
			#75%	도망에 성공했다.	전투 회피
			nRand = random.randint(1, 100)
			if nRand <=25 : 
				nCode = 2 
				sText = "도망에 실패했다. 전투에 돌입한다."
			else : 
				nCode = 3
				sText = "도망에 성공했다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn


		def fn(nCode): #팝업창 확인.

			if nCode==3 : #도망에 성공
				self.game.fade_scene_save("Stage1")
			else : #전투
				sCode = random.choice(["001","002","003","004","005","006","007","008","009"])
				self.game.fade_battle_scene(sCode)

			return
		self.btOk.on_click = fn

		return



	#양호실에서 양호 선생님에게 도움을 받음
	def te_104(self):
		self.load_bg("img/bg_004.png") #배경 이미지
		self.set_scenario(self.read_text("te_104")) ##시나리오 파일 

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 양호실에서 휴식한다.
			#100%	피격 게이지 모두 회복	새로운 카드(지원 카드 중에?)를 획득

			nCode = 1
			sText = "상처를 치료하고 도움이 될 카드를 얻었다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q2 약품을 받는다.
			#100%	카드를 획득	회복카드(201) 획득

			nCode = 2
			sText = "회복에 도움이 될 카드를 얻었다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn


		def fn(nCode): #팝업창 확인.

			if nCode==1 : #회복 + 지원 카드 획득
				#피격 게이지 회복, 지원 카드(400번대) 중에서 랜덤으로 1장 획득
				self.game.nTotalDamage = 0;
				self.game.fade_cardadd_scene("400")

			elif nCode==2 : #회복 카드 획득
				#회복 카드(201) 획득.
				self.game.fade_cardadd_scene("201")
			return
		self.btOk.on_click = fn

		return



	#과학실에서 비품을 이용하는 이벤트 
	def te_105(self):
		self.load_bg("img/bg_005.png") #배경 이미지
		self.set_scenario(self.read_text("te_105")) #시나리오 파일

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 화학 약품을 제조한다.
			#50%	카드를 획득											공격 카드 랜덤으로 획득
			#50%	화학 약품은 위험하다. 정확한 지식없이 제조하다 다쳤다.	카드 한장 폐기

			nRand = random.randint(1, 100)
			if nRand <=50 : 
				nCode = 1 
				sText = "제조를 통해 쓸만한 카드를 얻었다."
			else : 
				nCode = 2
				sText = "제조에 실패했다. 카드를 한 장 폐기한다." 
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q2 소독제(혹은 약품)를 가져간다.
			#100%	카드를 획득	회복카드(201) 획득  -> 회복카드보단 전투에 도움이 되는 구급약품 쪽이 좋아보임

			nCode = 3
			sText = "과학실의 비상약품을 얻었다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn

		def fn(): 
			#Q3 소화기를 가져간다.
			#100%	카드를 획득	소화기 카드 혹은 비슷한 느낌의 1회성 사용 카드 획득 -> 이 쪽은 지원 카드쪽으로

			nCode = 4
			sText = "과학실에 비치된 소화기를 얻었다."
			self.pop_alert(nCode, sText)
			return
		self.bt3.on_click = fn


		def fn(nCode): #팝업창 확인.

			if nCode==1 : #공격 카드 획득
				#공격 카드(000번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("000")

			elif nCode==2 : #카드 한장 폐기
				#실험 실패로 대미지를 받아서 카드를 한장 폐기
				self.game.discard_deck() # 카드삭제
				self.game.fade_scene_save("Stage1")

			elif nCode==3 : #회복 카드 획득
				#회복 카드(200번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("200")

			elif nCode==4 : #지원 카드 획득
				#지원 카드(400번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("400")
			return
		self.btOk.on_click = fn

		return


	#도서실에서 필요한 책을 찾아보아 카드를 획득하거나 체력 회복 등의 이벤트 
	def te_106(self):
		self.load_bg("img/bg_006.png") #배경 이미지
		self.set_scenario(self.read_text("te_106")) #시나리오 파일

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 A 서고를 살펴본다.
			#50%	카드를 획득	공격 카드 랜덤 획득
			#25%	카드를 획득	지원 카드 랜덤 획득
			#25%	필요한 책을 찾지 못했다.	이벤트 종료

			nRand = random.randint(1, 100)
			if nRand <=50 : 
				nCode = 1 
				sText = "서고에서 공격 카드를 발견했다."
			elif nRand <=75 : 
				nCode = 2
				sText = "서고에서 지원 카드를 발견했다."
			else :
				nCode = 3
				sText = "아무것도 발견할 수 없었다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q1 B 서고를 살펴본다.
			#50%	카드를 획득	지원 카드 랜덤 획득
			#25%	카드를 획득	공격 카드 랜덤 획득
			#25%	필요한 책을 찾지 못했다.	이벤트 종료
			
			nRand = random.randint(1, 100)
			if nRand <=50 : 
				nCode = 4 
				sText = "서고에서 지원 카드를 발견했다."
			elif nRand <=75 : 
				nCode = 5
				sText = "서고에서 공격 카드를 발견했다."
			else :
				nCode = 6
				sText = "아무것도 발견할 수 없었다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn

		def fn(): 
			#Q3 휴식한다.
			#50%	피격 게이지 모두 회복
			#50%	카드를 획득	회복카드(201) 획득

			nRand = random.randint(1, 100)
			if nRand <=50 :
				nCode = 7
				sText = "휴식으로 피격 게이지를 모두 회복했다."
			else :
				nCode = 8
				sText = "멍하니 쉬고있다가 회복 카드를 발견했다."
			self.pop_alert(nCode, sText)
			return
		self.bt3.on_click = fn


		def fn(nCode): #팝업창 확인.
			if nCode==1 : #공격 카드(000번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("000")

			elif nCode==2 : #지원 카드(400번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("400")

			elif nCode==3 : #변화 없음
				self.game.fade_scene_save("Stage1")

			elif nCode==4 : #지원 카드(400번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("400")

			elif nCode==5 : #공격 카드(000번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("000")

			elif nCode==6 : #변화 없음
				self.game.fade_scene_save("Stage1")

			elif nCode==7 : #피격 게이지 모두 회복
				self.game.nTotalDamage = 0
				self.game.fade_scene_save("Stage1")

			elif nCode==8 : #회복 카드(200번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("200")
			return
		self.btOk.on_click = fn

		return




	#방송실에서 방송을 하거나 자료를 찾아보면서 친구 해금 or 전투 or 카드 획득의 이벤트
	def te_107(self):
		self.load_bg("img/bg_007.png") #배경 이미지
		self.set_scenario(self.read_text("te_107")) #시나리오 파일

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 	방송을 한다
			#70%	방송을 듣고 로봇이 방송실로 공격해왔다. 전투에 돌입한다.
			#30%	방송을 듣고 친구가 방송실로 달려왔다. 친구를 해금했다.

			nRand = random.randint(1, 100)
			if nRand <=70 : 
				nCode = 1 
				sText = "방송을 듣고 로봇이 방송실로 공격해왔다."
			else : 
				nCode = 2
				sText = "방송을 듣고 친구가 방송실로 달려왔다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q2 	방송실 내부를 살펴본다
			#50%	방송실 내부에 쓸만한 카드가 있었다.	지원 카드 랜덤 획득
			#50%	아무것도 찾지 못했다	이벤트 종료
			
			nRand = random.randint(1, 100)
			if nRand <=50 : 
				nCode = 3 
				sText = "방송실 내부에 쓸만한 카드가 있었다."
			else :
				nCode = 4
				sText = "아무것도 찾지 못했다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn

		def fn(): 
			#Q3 	아무것도 하지 않는다
			self.game.fade_scene_save("Stage1")
			return
		self.bt3.on_click = fn


		def fn(nCode): #팝업창 확인.
			if nCode==1 : # 전투에 돌입한다.
				sCode = random.choice(["001","002","003","004","005","006","007","008","009"])
				self.game.fade_battle_scene(sCode)

			elif nCode==2 : #동료 해금
				print("동료 해금 개발 필요.")
				self.game.fade_scene_save("Stage1")

			elif nCode==3 : #지원 카드(400번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("400")

			elif nCode==4 : #아무것도 찾지 못했다.
				self.game.fade_scene_save("Stage1")

			return
		self.btOk.on_click = fn

		return



	#옥상 출입 가능한 시점에서 옥상을 살펴보거나 학교 밖을 살펴보거나 하는 정찰성 이벤트
	def te_108(self):
		self.load_bg("img/bg_008.png") #배경 이미지
		self.set_scenario(self.read_text("te_108")) #시나리오 파일

		#시나리오 이미지 
		img = pygame.image.load("img/te_001_001.png")
		img = pygame.transform.smoothscale(img, (300,200))
		self.set_event_img(img) #500x200 사이즈 

		def fn(): 
			#Q1 	옥상을 조사한다.
			#50%	열어뒀던 옥상으로 로봇이 들어와 있었다. 전투에 돌입한다.	전투 발생
			#25%	옥상을 조사하다 카드를 발견했다.	공격 카드 랜덤 획득
			#25%	아무것도 찾지 못했다.	이벤트 종료

			nRand = random.randint(1, 100)
			if nRand <=50 : 
				nCode = 1 
				sText = "열어뒀던 옥상으로 로봇이 들어와 있었다."
			elif nRand <=75 :
				nCode = 2 
				sText = "옥상을 조사하다 카드를 발견했다."
			else : 
				nCode = 3
				sText = "아무것도 찾지 못했다."
			self.pop_alert(nCode, sText)
			return
		self.bt1.on_click = fn

		def fn(): 
			#Q2 	밖을 살펴본다.
			#60%	주변을 살펴봤지만 별다른 이상은 없었다.	이벤트 종료
			#30%	옥상에서 밖을 살펴보니 이전과는 다른 거리가 보였다. 멀리로는 인공적인 벽 같은게 마을을 둘러싸고 있었고, 마을도 군데군데 파괴되어 있었다.	이벤트 종료
			#10%	운동장에 이상한 로봇이 있었다. 로봇을 자세히 관찰하며 보스에게만 사용 가능한 "약점포착(공격카드 010)"카드 획득

			nRand = random.randint(1, 100)
			if nRand <=60 : 
				nCode = 4 
				sText = "주변을 살펴봤지만 별다른 이상은 없었다."
			elif nRand <=90 : 
				nCode = 5 
				sText = "옥상에서 밖을 살펴보니 이전과는 다른 거리가 보였다."
			else :
				nCode = 6
				sText = "아무것도 찾지 못했다."
			self.pop_alert(nCode, sText)
			return
		self.bt2.on_click = fn

		def fn(): 
			#Q3 	휴식한다.
			#옥상에서 하늘을 보며 휴식하며 체력을 회복했다.
			nCode = 7 
			sText = "옥상에서 하늘을 보며 휴식하며 체력을 회복했다."
			self.pop_alert(nCode, sText)
			return
		self.bt3.on_click = fn


		def fn(nCode): #팝업창 확인.
			if nCode==1 : # 전투 발생
				self.game.fade_battle_scene("013")

			elif nCode==2 : #공격 카드(000번대) 랜덤으로 1장 획득
				self.game.fade_cardadd_scene("000")

			elif nCode==3 : #아무것도 찾지 못했다.
				self.game.fade_scene_save("Stage1")

			elif nCode==4 : #주변을 살펴봤지만 별다른 이상은 없었다.
				self.game.fade_scene_save("Stage1")

			elif nCode==5 : #옥상에서 밖을 살펴보니 이전과는 다른 거리가 보였다.
				self.game.fade_scene_save("Stage1")

			elif nCode==6 : #아무것도 찾지 못했다.
				self.game.fade_scene_save("Stage1")

			elif nCode==7 : #피격 게이지 모두 회복
				self.game.nTotalDamage = 0
				self.game.fade_scene_save("Stage1")

			return
		self.btOk.on_click = fn

		return













