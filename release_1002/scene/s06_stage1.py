from core.scene import Scene
from core.div import Div
from core.place import Place
import pygame
import math
import random
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)


class Stage1(Scene):
	def __init__(self, game):
		super().__init__(game, "Stage1")

		self.location = "Base"
		self.nStep = 0
		self.bBoss = False

		#각 장소 열림여부.
		#각 장소 최초방문 여부. 

		self.load()
		self.reset()
		return 

	def reset(self):
		self.location = "Base"
		self.nStep = 0
		self.bBoss = False

		for place in self.groupPlace :
			place.status("NONE")
			place.bVisited = False
			if( place.sName == "Base" 
				or place.sName == "Classroom1" ):
				place.status("OPEN")

		

		#장소 라인정보 lines = { "Base_Classroom1" : (place, place), ... }
		self.lines = {}
		for place1 in self.groupPlace :

			for sName in place1.map :
				for place2 in self.groupPlace :
					if place2.sName == sName :
						line = self.get_rd_line(place1.rect.center, place2.rect.center, 4, 10 )
						if place1.sName < place2.sName :
							self.lines[ place1.sName+"_"+place2.sName ] = ( place1, place2, line )
						else : self.lines[ place2.sName+"_"+place1.sName ] = ( place2 , place1, line )

		# place.status("NORMAL")
		return	


	def load(self):
		#배경
		img = pygame.image.load("img/stage1_bg_001.png")
		img = pygame.transform.scale(img, self.game.arrWindowSize)
		#상단바
		surfaceGray = pygame.Surface((self.game.arrWindowSize[0],45), pygame.SRCALPHA)
		surfaceGray.set_alpha(50)
		surfaceGray.fill((0, 0, 0))
		img.blit(surfaceGray,(0,0))
		self.imgBg = img

		div = Div(self.game)
		div.width(600)
		div.height(45)
		img = pygame.Surface((1,1), pygame.SRCALPHA)
		img.set_alpha(70)
		div.surface(img)
		div.padding_top(-5)
		div.padding_left(5)
		div.text("학교")
		self.title = div

		#카드 스페이스 
		img = pygame.image.load("img/card_space.png")
		img2 = img.copy()
		img_rect = img2.get_rect()
		pygame.draw.rect(img2, (50, 50, 255, 100), img_rect, 10)

		div = Div(self.game)
		div.width(50)
		div.height(50)
		div.surface(img)
		div.surfaceHover(img2)
		div.top(5)
		div.right(20)
		self.btCardspace = div


		#캐릭터 이미지 
		# img = pygame.image.load("img/char_01.png")
		img = pygame.Surface((800, 800), pygame.SRCALPHA)
		img = img.subsurface(pygame.Rect(80, 0, 300, 300))
		#원형 마스크 
		mask = pygame.Surface((300, 300), pygame.SRCALPHA)
		pygame.draw.circle(mask, (255, 255, 255, 255), (150, 150), 150)
		#마스크에 그리기 
		mask.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
		#마우스 호버
		mask2 = mask.copy()
		pygame.draw.circle(mask2, (50, 50, 255, 100), (150, 150), 150, 10)


		#왼쪽 이미지 
		div = Div(self.game)
		div.surface(mask)
		div.surfaceHover(mask2)
		div.width(150)
		div.height(150)
		div.bottom(20)
		div.left(20)
		self.myChar = div


		#테스트 
		# temp = pygame.Surface((1,1), pygame.SRCALPHA)
		# self.myChar.surface(temp)
		# self.myChar.surfaceHover(temp) 

		self.load_place();

		return 


	def get_stage_data(self):
		stageData = {}
		stageData["location"] = self.location
		stageData["nStep"] = self.nStep
		stageData["bBoss"] = self.bBoss

		arrStatus = {}
		arrVisited = {}
		for place in self.groupPlace :
			arrStatus[place.sName] = place.status()
			arrVisited[place.sName] = place.bVisited

		stageData["arrStatus"] = arrStatus
		stageData["arrVisited"] = arrVisited
		return stageData

	def set_stage_data(self, stageData):
		self.location = stageData["location"]
		self.nStep = stageData["nStep"]
		self.bBoss = stageData["bBoss"]

		for place in self.groupPlace :
			place.status(stageData["arrStatus"][place.sName])
			place.bVisited = stageData["arrVisited"][place.sName]
		return 

	def load_place(self):

		self.groupPlace = pygame.sprite.Group()

		place = Place(self, "Base", ["Classroom1"], 130, 335)
		place.type("BASE")
		place.status("OPEN")
		self.groupPlace.add(place)
		place = Place(self, "Classroom1", ["Base", "Stairs2", "Stairs3", "Classroom2"], 452, 335)
		place.status("OPEN")
		self.groupPlace.add(place)
		place = Place(self, "Classroom2", ["Stairs2", "Stairs3", "Classroom1"], 958, 335)
		place.status("NONE")
		self.groupPlace.add(place)

		#윗층 
		place = Place(self, "Stairs3", ["Stairs2", "Classroom1", "Classroom2", "Classroom3", "Classroom4", "Roof"], 590, 248)
		place.status("NONE")
		self.groupPlace.add(place)
		place = Place(self, "Classroom3", ["Stairs3"], 310, 248)
		place.status("NONE")
		self.groupPlace.add(place)
		place = Place(self, "Classroom4", ["Stairs3"], 817, 248)
		place.status("NONE")
		self.groupPlace.add(place)

		#옥상
		place = Place(self, "Roof", ["Stairs3"], 800, 138)
		place.status("NONE")
		self.groupPlace.add(place)

		#아랫층 
		place = Place(self, "Stairs2", ["Stairs1", "Stairs3", "Classroom1", "Classroom2", "Classroom5", "Classroom6"], 590, 420)
		place.status("NONE")
		self.groupPlace.add(place)
		place = Place(self, "Classroom5", ["Stairs2"], 410, 420)
		place.status("NONE")
		self.groupPlace.add(place)
		place = Place(self, "Classroom6", ["Stairs2"], 817, 420)
		place.status("NONE")
		self.groupPlace.add(place)

		#1층
		place = Place(self, "Stairs1", ["Stairs2", "Classroom7", "Classroom8", "Playground"], 590, 603)
		place.status("NONE")
		self.groupPlace.add(place)
		place = Place(self, "Classroom7", ["Stairs1", "Playground"], 880, 603)
		place.status("NONE")
		self.groupPlace.add(place)
		place = Place(self, "Classroom8", ["Stairs1"], 335, 603)
		place.status("NONE")
		self.groupPlace.add(place)

		#운동장 
		place = Place(self, "Playground", ["Stairs1" , "Classroom7"], 725, 650)
		place.type("WARNING")
		place.status("NONE")
		self.groupPlace.add(place)

		#장소 라인정보 lines = { "Base_Classroom1" : (place, place), ... }
		self.lines = {}
		for place1 in self.groupPlace :

			for sName in place1.map :
				for place2 in self.groupPlace :
					if place2.sName == sName :
						line = self.get_rd_line(place1.rect.center, place2.rect.center, 4, 10 )
						if place1.sName < place2.sName :
							self.lines[ place1.sName+"_"+place2.sName ] = ( place1, place2, line )
						else : self.lines[ place2.sName+"_"+place1.sName ] = ( place2 , place1, line )

		return 


	def get_rd_line(self, start, end, size, length):
		if end[0]**2+end[1]**2 < start[0]**2+start[1]**2 :
			temp = end 
			end = start 
			start = temp 

		line = {}

		x1x2 = end[0]-start[0]
		y1y2 = end[1]-start[1]

		total = x1x2**2 + y1y2**2
		total_length = math.sqrt(total)
		if total_length<1 : return

		dx = x1x2 / total_length
		dy = y1y2 / total_length

		nPadding = 50
		mX = min(start[0], end[0])
		mY = min(start[1], end[1])
		width = abs(x1x2)+nPadding*2
		height = abs(y1y2)+nPadding*2
		start = (start[0]-mX+nPadding, start[1]-mY+nPadding)
		end = (end[0]-mX+nPadding, end[1]-mY+nPadding)

		line["pos"] = (mX-nPadding,mY-nPadding)
		line["disable"] = pygame.Surface((width,height), pygame.SRCALPHA)
		line["movable"] = pygame.Surface((width,height), pygame.SRCALPHA)

		arr = [] # (startx, starty, endx, endy)

		p1 = None
		p2 = None
		while True :
			# 한축이 같은 좌표인지 확인. 같으면 그냥 그림됨.
			if p1 is None : 
				p1 = start 
			else : 
				#p2 에서 거리와 남은 
				x1x2 = end[0]-p2[0]
				y1y2 = end[1]-p2[1]

				total = x1x2**2 + y1y2**2
				total_length = math.sqrt(total)

				dx = x1x2 / total_length
				dy = y1y2 / total_length


				p1 = ( p2[0]+dx*length*0.8,p2[1]+dy*length*0.8 ) 

			if (end[0]-p1[0])**2+(end[1]-p1[1])**2 < length**2 :
				#남은 거리가 길이보다 작은상황
				arr.append( p1+end )
				break
			
			p2 = ( p1[0]+dx*length+random.randint(-3, 3), p1[1]+dy*length+random.randint(-3, 3)) 
			arr.append( p1+p2 )

			if (end[0]-p2[0])**2+(end[1]-p2[1])**2 < length**2 :
				#다음 점찍을 위치가 끝점을 지나감. 
				break

			if width < p2[0] or height < p2[1] : break



		for p in arr :
			s = (rd(p[0]), rd(p[1]))
			e = (rd(p[2]), rd(p[3]))
			pygame.draw.line(line["disable"], (0,0,0), s, e, size)
			pygame.draw.line(line["movable"], (255,255,255), s, e, size)

		return line

	
	def draw_map_line(self):
		for k in self.lines : #self.lines[k] = ( place, place, line(surf, pos))
			#일단 status가 NONE이면 넘어감. 
			place1 = self.lines[k][0]
			place2 = self.lines[k][1]
			shape = self.lines[k][2]

			if place1.status() == "NONE" or place2.status() == "NONE" :
				continue
			elif place1.sName != self.location and place2.sName != self.location : 
				self.game.screen.blit(shape["disable"], shape["pos"])
			elif place1.sName == self.location and place2.check_movable() :
				self.game.screen.blit(shape["movable"], shape["pos"])
			elif place2.sName == self.location and place1.check_movable() :
				self.game.screen.blit(shape["movable"], shape["pos"])
			else :
				self.game.screen.blit(shape["disable"], shape["pos"])

		return





	def on_mouse_button_down(self, e):
		try:
			if e.button == 1: 
				for place in self.groupPlace :
					# if place.collidepoint(e.pos) : print(place.sName)
					if place.collidepoint(e.pos) and place.check_movable() :
						self.move_place(place)
						return
				if self.btCardspace.collidepoint(e.pos) : #카드 스페이스 
					self.game.sound_play("CURSOR")
					self.game.set_stage_cardspace_scene()
					return


		except Exception as e: print(e)


	def find_place(self, sName):
		for place in self.groupPlace :
			if place.sName == sName : return place
		return None


	def cal_stage_step(self):


		if self.nStep == 0 : 
			for place in self.groupPlace :
				if place.sName=="Base" or place.sName=="Classroom1" : continue
				place.bVisited = False
				place.status("NONE")

		if 1 <= self.nStep :
			self.title.text("학교 - Step "+str(self.nStep))

		if 5 <= self.nStep : #5회 이상시 옥상 오픈
			place = self.find_place("Roof")
			place.status("NORMAL")

		if 8 <= self.nStep : #8회 이상시 보스 오픈
			place = self.find_place("Playground")
			place.status("NORMAL")


		if 15 <= self.nStep : #15회 이상이면 보스전만 가능
			for place in self.groupPlace :
				place.status("NONE")
			place1 = self.find_place(self.location)
			place1.status("CLOSE")
			place1.map = ["Playground"]
			place2 = self.find_place("Playground")
			place2.status("OPEN")
			place2.map = [self.location]

			if self.bBoss==False : 
				self.bBoss = True
				self.lines = {}
				line = self.get_rd_line(place1.rect.center, place2.rect.center, 4, 10 )
				if place1.sName < place2.sName :
					self.lines[ place1.sName+"_"+place2.sName ] = ( place1, place2, line )
				else : self.lines[ place2.sName+"_"+place1.sName ] = ( place2 , place1, line )



			


		return 

	def update(self):
		try:
			#배경
			self.game.screen.blit(self.imgBg, (0, 0))

			#타이틀
			self.title.update()
			self.title.draw()

			# 커서 변경.
			bCursor = False
			pos = pygame.mouse.get_pos()
			for place in self.groupPlace :
				if place.collidepoint(pos) and place.check_movable() :
					bCursor = True
			if self.btCardspace.collidepoint(pos) : bCursor = True
			if bCursor : pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
			else : pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

			self.cal_stage_step() #조건들 적용하기.

			self.draw_map_line()		
			#이은선 그리기 
			# self.draw_movable_line()

			self.btCardspace.update()
			self.btCardspace.draw()

			# self.myChar.update()
			# self.myChar.draw()

			self.groupPlace.update()
			self.groupPlace.draw(self.game.screen)

		except Exception as e: print(e)
	


	def move_place(self, place):
		self.game.sound_play("FOOTSTEP")
		if hasattr(self,"on_"+place.sName): 
			def fn():
				getattr(self,"on_"+place.sName)(place)
				return
			self.game.call_delay(fn, 500)
			
		else :
			print(place.sName, "함수 없음!!!")
		return 	

	def on_Classroom1(self, place):
		# 최초 고정 이벤트	SE	001
		# 	확률 50%	TE	101, 102
		# 	확률 50%	BE	101
		if place.bVisited==False : # 최초
			place.bVisited = True
			self.game.fade_scenario_scene("001")
		else :
			n = random.randint(1, 100) 
			if n<=25 : self.game.fade_text_scene("101")
			elif n<=50 : self.game.fade_text_scene("102")
			else :
				sCode = random.choice(["001","002","003","004","005","006"])
				self.game.fade_battle_scene(sCode)
		
		def fn(): #다른곳 해금 
			self.find_place("Stairs3").status("NORMAL")
			# self.find_place("Classroom2").status("NORMAL")
			self.find_place("Stairs2").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 


	def on_Stairs1(self, place):
		# 최초 고정 이벤트	SE	002	// 계단2, 계단3 상관 없이 1회만 SE002 발생 그 이후에는 모든 계단에서 케이스2로
		# 	확률 50%	TE	103	
		# 	확률 50%	BE	101	
		if place.bVisited==False : # 최초
			self.find_place("Stairs1").bVisited = True
			self.find_place("Stairs2").bVisited = True
			self.find_place("Stairs3").bVisited = True
			self.game.fade_scenario_scene("002")
		else :
			n = random.randint(1, 100) 
			if n<=50 : 
				self.game.fade_text_scene("103")
			else :
				sCode = random.choice(["001","002","003","004","005","006"])
				self.game.fade_battle_scene(sCode)
		
		def fn(): #다른곳 해금 
			self.find_place("Stairs2").status("NORMAL")
			self.find_place("Classroom7").status("NORMAL")
			self.find_place("Classroom8").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 
	
	def on_Stairs2(self, place):
		# 최초 고정 이벤트	SE	002	// 계단2, 계단3 상관 없이 1회만 SE002 발생 그 이후에는 모든 계단에서 케이스2로
		# 	확률 50%	TE	103	
		# 	확률 50%	BE	101	
		if place.bVisited==False : # 최초
			self.find_place("Stairs1").bVisited = True
			self.find_place("Stairs2").bVisited = True
			self.find_place("Stairs3").bVisited = True
			self.game.fade_scenario_scene("002")
		else :
			n = random.randint(1, 100) 
			if n<=50 : 
				self.game.fade_text_scene("103")
			else :
				sCode = random.choice(["001","002","003","004","005","006"])
				self.game.fade_battle_scene(sCode)
		
		def fn(): #다른곳 해금 
			self.find_place("Stairs3").status("NORMAL")
			self.find_place("Classroom2").status("NORMAL")
			self.find_place("Classroom6").status("NORMAL")
			self.find_place("Stairs1").status("NORMAL")
			self.find_place("Classroom5").status("NORMAL")
			self.find_place("Classroom1").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def on_Stairs3(self, place):
		# 최초 고정 이벤트	SE	002	// 계단2, 계단3 상관 없이 1회만 SE002 발생 그 이후에는 모든 계단에서 케이스2로
		# 	확률 50%	TE	103	
		# 	확률 50%	BE	101	
		if place.bVisited==False : # 최초
			self.find_place("Stairs1").bVisited = True
			self.find_place("Stairs2").bVisited = True
			self.find_place("Stairs3").bVisited = True
			self.game.fade_scenario_scene("002")
		else :
			n = random.randint(1, 100) 
			if n<=50 : 
				self.game.fade_text_scene("103")
			else :
				sCode = random.choice(["001","002","003","004","005","006"])
				self.game.fade_battle_scene(sCode)
		
		def fn(): #다른곳 해금 
			# self.find_place("Roof").status("NORMAL")
			self.find_place("Classroom4").status("NORMAL")
			self.find_place("Classroom2").status("NORMAL")
			self.find_place("Stairs2").status("NORMAL")
			self.find_place("Classroom1").status("NORMAL")
			self.find_place("Classroom3").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 


	def on_Classroom8(self, place):
		# 최초 고정 이벤트	SE	004
		# 확률 100%	TE	104
		if place.bVisited==False : # 최초
			place.bVisited = True
			self.game.fade_scenario_scene("004")
		else :
			self.game.fade_text_scene("104")
			
		def fn(): #다른곳 해금 
			self.find_place("Stairs1").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def on_Classroom3(self, place):
		# 최초 고정 이벤트	SE	005
		# 확률 100%	TE	105
		if place.bVisited==False : # 최초
			place.bVisited = True
			self.game.fade_scenario_scene("005")
		else :
			self.game.fade_text_scene("105")
			
		def fn(): #다른곳 해금 
			self.find_place("Stairs3").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def on_Classroom4(self, place):
		# 최초 고정 이벤트	SE	006
		# 확률 100%	TE	106
		if place.bVisited==False : # 최초
			place.bVisited = True
			self.game.fade_scenario_scene("006")
		else :
			self.game.fade_text_scene("106")
			
		def fn(): #다른곳 해금 
			self.find_place("Stairs3").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def on_Classroom6(self, place):
		# 최초 고정 이벤트	SE	007
		# 확률 100%	TE	107
		if place.bVisited==False : # 최초
			place.bVisited = True
			self.game.fade_scenario_scene("007")
		else :
			self.game.fade_text_scene("107")
			
		def fn(): #다른곳 해금 
			self.find_place("Stairs2").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 


	def on_Roof(self, place):
		# 최초 고정 이벤트	SE	008
		# 확률 80%	TE	108
		# 확률 20%	BE	mon013
		if place.bVisited==False : # 최초
			place.bVisited = True
			self.game.fade_scenario_scene("008")
		else :
			n = random.randint(1, 100) 
			if n<=80 : # 80%
				self.game.fade_text_scene("108")
			else : # 20%
				self.game.fade_battle_scene("013")
			
		def fn(): #다른곳 해금 
			self.find_place("Stairs3").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 


	def on_Playground(self, place):
		# 보스 조우 조건 미달성			
		# 	보스 조우 조건은 추후에 작업할 예정, 
		# 	조건 예시 턴 12턴 이후 조우 가능 
		# 	그전까지는 운동장은 갈 수 있지만 
		# 	케이스1로 처리
		# 75%	SE	010	
		# 25%	BE	101	
		# 보스 조우 조건 달성	SE	011	
		if self.nStep >= 12 : # 12턴 이후 
			place.bVisited = True
			self.game.fade_scenario_scene("011")
		else :
			n = random.randint(1, 100) 
			if n<=75 : # 75%
				self.game.fade_scenario_scene("010")
			else : # 25%
				self.game.fade_battle_scene("012")

		def fn(): #다른곳 해금 
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def classrooms(self, place):
		place.bVisited = True

		n = random.randint(1, 100) 
		if n <= 25 : self.game.fade_battle_scene("001")
		elif n <= 50 : self.game.fade_battle_scene("002")
		else :
			sCode = random.choice(["001","002","003","004","005","006"])
			self.game.fade_battle_scene(sCode)
		return

	def on_Classroom2(self, place):
		self.classrooms(place)

		def fn(): #다른곳 해금 
			self.find_place("Stairs2").status("NORMAL")
			self.find_place("Classroom1").status("NORMAL")
			self.find_place("Stairs3").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def on_Classroom5(self, place):
		self.classrooms(place)
		
		def fn(): #다른곳 해금 
			self.find_place("Stairs2").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 

	def on_Classroom7(self, place):
		self.classrooms(place)

		def fn(): #다른곳 해금 
			self.find_place("Stairs1").status("NORMAL")
			self.nStep += 1
			self.location = place.sName
			return
		self.game.call_delay(fn, 1000)
		return 




















