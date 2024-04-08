from core.scene import Scene
from core.dialog import Dialog
import pygame

class Scenarioevent(Scene):
	def __init__(self, game):
		super().__init__(game, "Scenarioevent")
		self.img = pygame.Surface((0,0), pygame.SRCALPHA)
		self.bEnd = True

		self.load()
		return 

	def load(self):
		self.arrScenario = []
		with open("./lang/intro_"+self.game.sLangCode+".txt", "r", encoding="utf8") as file:
			for sLine in file:
				self.arrScenario.append(sLine.strip())

		dialog = Dialog(self.game)
		dialog.width(self.game.arrWindowSize[0])
		dialog.height(self.game.arrWindowSize[1])
		self.dialog = dialog

		self.nIndex = -1

		def fn():
			print("end_scenario")
		self.end_scenario = fn

		return 

	def next_scenario(self):
		if len(self.dialog.arrTyping)>0 :
			self.dialog.end_typing()
			return

		self.nIndex += 1
		if len(self.arrScenario) <= self.nIndex :
			self.bEnd = True
			self.end_scenario()
			return

		text = self.arrScenario[self.nIndex]
		if text.startswith("#CRL") : #글자 지우기 
			self.dialog.clear_text()
			self.next_scenario()
		elif text.startswith("#IMG") : #배경 
			sImg = text.split(maxsplit=1)[1]
			self.img = pygame.image.load("img/"+sImg)
			self.img = pygame.transform.scale(self.img, self.game.arrWindowSize)	
			self.next_scenario()
		else :
			self.dialog.add_typing(self.arrScenario[self.nIndex])

		return 

	def event(self, e):
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_LCTRL : #왼쪽 컨트롤키 눌렀을때 
				# self.nIndex
				self.dialog.end_typing()
				self.next_scenario()
				for i in range(self.nIndex+1, len(self.arrScenario)) :
					if self.arrScenario[i].startswith("#CRL") :
						break
					self.dialog.end_typing()
					self.next_scenario()
					self.dialog.end_typing()

		return

	def on_mouse_button_down(self, e):
		try:
			if self.bEnd : return
			if e.button == 1: 
				self.game.sound_play("CURSOR")
				self.next_scenario()

		except Exception as e: print(e)


	def update(self):
		try:
			self.game.bCursorHand = True
			self.game.screen.blit(self.img, (0, 0))
			self.dialog.update()
			self.dialog.draw()
				
		except Exception as e: print(e)
	
	def load_scenario(self, sName):
		print("s09_scenarioevent.load_scenario()",sName)

		#시나리오 초기화
		self.arrScenario = []
		self.nIndex = -1
		self.dialog.clear_text()
		self.bEnd = False
		
		#시나리오함수 호출 
		if hasattr(self,"se_"+sName): 
			getattr(self,"se_"+sName)()

		return 	

	def read_scenario(self, sName):
		with open("./lang/se_"+sName+"_"+self.game.sLangCode+".txt", "r", encoding="utf8") as file:
			for sLine in file:
				self.arrScenario.append(sLine.strip())
		return 


	"""
	이하 텍스트 이벤트 리스트 
	"""
	def se_test(self):
		#시나리오 파일 읽기
		self.read_scenario("test")

		#시나리오 종료 이벤트 
		def fn():
			self.game.fade_scene_save("Stage1")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		return

	def se_001(self):
		"""
			- 교실에서 친구와 만남	
			교실(교실1)로 진입하자 구석에 숨어서 농성중인 친구를 발견했다. 
			친구를 설득하여 함께 동행하기로 했다.	
			=> 동료를 해금	동료들은 랜덤으로 결정(희귀도가 있다면 그 희귀도를 따라 확률 조정).  모든 동료를 해금한 경우, 이 이벤트가 발생하지 않음. 혹은 발생하더라도 동료를 얻지 않게
		"""

		#시나리오 파일 읽기
		self.read_scenario("001")

		#시나리오 종료 이벤트 
		def fn():
			# self.game.fade_scene_save("Stage1")
			self.game.fade_cardadd_scene("001") #동료추가 대신.
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.

		#남은 동료 랜덤 해금 
		return



	def se_002(self):
		"""
			- 계단(계단2, 계단3)으로 처음 진입 시, 전투 발생(튜토리얼 전투 느낌)	
			친구와 합류한 나는 다른 곳을 살펴보기위해 계단으로 향했다. 
			그곳에는 Ges가 말했던 것으로 추측되는 로봇 하나가 있었다. 
			이쪽을 눈치챈 로봇과 전투가 불가피할 것으로 보인다.	 
			=> 전투 발생	팝업으로 "전투를 준비한다"라는거 뜨고 누르면 전투로 넘어가면 느낌이 좋을듯
		"""

		#시나리오 파일 읽기
		self.read_scenario("002")

		#시나리오 종료 이벤트 
		def fn():
			#게스와 전투 발생 
			self.game.fade_battle_scene("000")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		
		return



	def se_003(self):
		"""
			- 교실에서 카드 획득 
			로봇과의 전투가 끝나고 친구들이 피신해 있을지도 모르는 교실(교실2)로 향했다. 
			아쉽게도 그곳에 사람은 없었다. 교실을 살펴보자 쓸만한 물건(카드)을 얻을 수 있었다. 
			=> 카드를 얻음	랜덤으로 1개
		"""

		#시나리오 파일 읽기
		self.read_scenario("003")

		#시나리오 종료 이벤트 
		def fn():
			self.game.fade_scene_save("Stage1")
			#카드 1장 랜덤 획득 카드 추가 씬으로 이동.
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.

		return




	def se_004(self):
		"""
			- 양호실에 처음 가는 경우, 양호 선생님과 만남
			양호실로 향했다. 양호실은 다행이도 로봇들이 점령하지 못했고, 
			양호 선생님이 계셨다. 양호 선생님께서 반갑게 맞이해주시며, 
			상처를 치료해주시면서 언제라도 괜찮으니 휴식이 필요하면 양호실로 오라고 하셨다.
			=> 체력 회복(피격 게이지 회복?),
			양호실이 안전구역으로 변경(안전구역을 색상 바꿔서 표시할거면 그 색상으로, 
			색상 바꿔서 표시 안할거면 그냥 냅둬도 됨), 
			이후 양호실 입장시 텍스트 이벤트 104 발생
		"""

		#시나리오 파일 읽기
		self.read_scenario("004")

		#시나리오 종료 이벤트 
		def fn():
			self.game.fade_scene_save("Stage1")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.

		#체력 회복(피격 게이지 회복)
		#양호실이 안전구역으로 변경. 이후 양호실에는 텍스트이벤트104가 발생.
		return


	def se_005(self):
		"""
			- 과학실에 처음 진입하는 경우, 과학실에서 과학 용품 관리 로봇과 전투
			과학실로 향했다. 과학실은 과학용품을 관리하는 로봇이 있었다. 
			과학실을 이용하기 위해서는 이 로봇을 물리쳐야될 것 같다. 
			전투를 준비한다.
			=> "과학용품 관리 로봇(302)과 전투.
			전투 승리로 과학실 이용 가능. (과학실 진입 시, 텍스트 이벤트 105 발생)"
		"""

		#시나리오 파일 읽기
		self.read_scenario("005")

		#시나리오 종료 이벤트 
		def fn():
			#과학용품 관리 로봇(302)와 전투 scc
			self.game.fade_battle_scene("010")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		return



	def se_006(self):
		"""
			- 도서실로 처음 입장 시, 도서실을 관리하는 로봇과 전투	
			도서실로 향했다. 도서실을 관리하는 로봇이 있었다. 
			도서실을 이용하기 위해서는 이 로봇을 물리쳐야될 것 같다. 
			전투를 준비한다.	
			=> 도서실 관리 로봇(사서 로봇(303))과 전투.
			전투 승리로 도서실 이용 가능. (도서실 진입 시, 텍스트 이벤트 106 발생)"
		"""

		#시나리오 파일 읽기
		self.read_scenario("006")

		#시나리오 종료 이벤트 
		def fn():
			#도서실 관리 로봇(사서 로봇(303))과 전투.
			self.game.fade_battle_scene("011")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		return



	def se_007(self):
		"""
			- 방송실로 처음 입장 시, 일어나는 이벤트
			방송실로 향했다. 방송실은 방송부원들만 출입했었던 곳으로 
			로봇들의 출입도 금지되어 있었던 것 같다. 
			혹시나 하고 향했던 방송실에서 농성중인 학생을 
			발견해 방송실에 들어갈 수 있었다.
			=> 방송실에 있던 친구 해금.
			이후 방송실 이용 가능. (방송실 진입 시, 텍스트 이벤트 107 발생)
		"""

		#시나리오 파일 읽기
		self.read_scenario("007")

		#시나리오 종료 이벤트 
		def fn():
			# self.game.fade_scene_save("Stage1")
			self.game.fade_cardadd_scene("001") #동료추가 대신.
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		#방송실에 있던 친구 해금.
		#이후 방송실 이용 가능. (방송실 진입 시, 텍스트 이벤트 107 발생)
		return


	def se_008(self):
		"""
			- 옥상으로 진입 시 일어나는 이벤트
			옥상으로 가려면 카드키가 필요한 것 같다. 
			내가 가지고 있는 카드들로 시도해보면 어떨까 / 
			(선택한 후에) 카드를 한 장 사용하여 옥상으로 
			가는 문을 열었다. 문이 닫히지 않게 고정해뒀으니 
			다음부턴 카드 소모 없이 옥상을 출입할 수 있다.
			카드 한장 사용(삭제), 옥상으로 진입할 수 있게됨.
			=> "선택지가 있는 시나리오 이벤트(1회성 텍스트 이벤트라고 해도 될듯)
			선택지는 내 카드 풀을 보여주고 사용할 카드를 선택하는 선택지 -> 카드리스트 씬에 선택지를 추가하는 방식으로?
			위의 선택지 만드는게 시간이 걸리면 단순하게 시도하는거 Yes or No 선택지 주고 Yes 선택 시 랜덤으로 카드 한 장 삭제되게
			이 이벤트는 두 페이지로 만들어야됨(첫 페이지는 선택 전의 이야기, 두번째 페이지는 선택 후에 결과)"

			텍스트 이벤트로 만들어야할듯.
		"""

		#시나리오 파일 읽기
		self.read_scenario("008")

		#시나리오 종료 이벤트 
		def fn():
			self.game.fade_scene_save("Stage1")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		return





	def se_010(self):
		"""
			- 보스 전투가 가능하지 않은 시점에 운동장으로 가는 경우(운동장에 도착 못하고 현관쪽에서 이벤트가 발생하는 것)
			운동장으로 가려 했으나, 출입문이 열리지 않았다. 문 밖의 상황은 별다른 이상은 없어 보인다.
			=> 행동 소모만 있고 아무일도 일어나지 않음.
		"""

		#시나리오 파일 읽기
		self.read_scenario("010")

		#시나리오 종료 이벤트 
		def fn():
			self.game.fade_scene_save("Stage1")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		return




	def se_011(self):
		"""
			- 보스 전투가 가능한 시점에 운동장으로 가는 경우
			이전과는 달리 출입문이 열렸다. 아까 들렸던 큰 소리가 발생했던 
			운동장쪽으로 향하자 여태까지 싸워왔던 적과는 전혀 
			다른 형태의 로봇이 있었다. 이게 Ges가 말했던 다른 
			타입의 적인 것 같다. 이녀석이 학교의 로봇들이 
			이상행동을 하게 만든 녀석인 것 같다. 이녀석을 물리치면 
			학교는 평화를 되찾을 것으로 보인다.
			=> 스테이지 1 보스전 돌입
			"스테이지 1의 보스로 이 보스를 제외한 적들은 학교에서 원래 있던 로봇들.
			이 보스는 그런 로봇과는 형태가 좀 다른 녀석으로 강해보이면 좋을 것같음."

		"""

		#시나리오 파일 읽기
		self.read_scenario("011")

		#시나리오 종료 이벤트 
		def fn():
			self.game.fade_battle_scene("014")
		self.end_scenario = fn

		self.next_scenario() #시나리오 시작.
		return















