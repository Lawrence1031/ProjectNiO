import pygame
import math
import time
rd = lambda n,d=None:round(n+10**(-len(str(n))-1),d)

class Dualdisc(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()

		self.game = game
		self.image = None
		self.rect = pygame.Rect(0, 0, 100, 100)
		self._font = None

		self.lastState = str(time.time())
		self.arrCard = [] # [ {sCode :"001", image:IMG, ... } ]

		self.arrBaseImage = {} #카드 기본틀들. 
		self.arrBaseImage["NORMAL"] = pygame.image.load("img/card_base_001.png").convert_alpha()
		self.arrBaseImage["ATTACK"] = pygame.image.load("img/card_base_001.png").convert_alpha()
		self.arrBaseImage["HEAL"] = pygame.image.load("img/card_base_002.png").convert_alpha()
		self.arrBaseImage["SUPPORT"] = pygame.image.load("img/card_base_003.png").convert_alpha()
		self.arrBaseImage["OBSTRUCTION"] = pygame.image.load("img/card_base_004.png").convert_alpha()
		# self.arrBaseImage["___"] = pygame.image.load("img/card_base_003.png").convert_alpha()
		rect = self.arrBaseImage["NORMAL"].get_rect()
		self.nCardWidth = rect.width
		self.nCardHeight = rect.height

		self.nIlluWidth = 553
		self.nIlluHeight = 412
		self.nIlluLeft = 10
		self.nIlluTop = 78

		self.fTitle = pygame.font.Font("./font/NotoSansKR-Regular.otf", 40)
		self.fTitle.set_bold(True)
		self.nTitleLeft = 287-15
		self.nTitleTop = 13

		self.fBody = pygame.font.Font("./font/NotoSansKR-Regular.otf", 40)
		self.nBodyLeft = 20
		self.nBodyTop = 495
		self.nBodyWidth = 530
		self.nBodyLineHeight = 50


		self.nFullCardX = 574*0.4
		self.nFullCardY = 800*0.4
		self.nHandCardX = 574*0.2
		self.nHandCardY = 800*0.2
		self.mapCardPos = {}
		self.nSelectIndex = -1
		self.nLastFullIndex = -1
		self.arrNowPos = []

		self.nIndex = 0
		return


	def add_card(self, sCode):
		card = {}
		card["bFull"] = False
		card["nX"] = -300
		card["nY"] = 140
		card["nA"] = 0
		card["bAnim"] = False
		card["nAnimX"] = 0
		card["nAnimY"] = 0
		card["nSpeedX"] = 0
		card["nSpeedY"] = 0

		#sCode 추가 
		card["sCode"] = sCode

		cardInfo = self.game.cardlist.find(sCode)

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
		imgCost = pygame.image.load("img/card_sp.png").convert()

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
		if nCost > 0 : img.blit(imgCost,(20,20+0*55))
		if nCost > 1 : img.blit(imgCost,(20,20+1*55))
		if nCost > 2 : img.blit(imgCost,(20,20+2*55))
		if nCost > 3 : img.blit(imgCost,(20,20+3*55))


		#이미지 저장.
		card["fullImage"] = pygame.transform.smoothscale(img, (self.nFullCardX,self.nFullCardY)) #229
		card["handImage"] = pygame.transform.smoothscale(img, (self.nHandCardX,self.nHandCardY)) #114.5
		card["image"] = card["handImage"]
		card["rect"] = card["image"].get_rect()


		#저장.
		self.arrCard.append(card)
		return 


	def remove_card(self, n):
		self.arrCard.pop(n)
		self.lastState = str(time.time())
		self.nLastFullIndex = -1
		return 

	def remove_card_all(self):
		self.arrCard = []
		self.lastState = str(time.time())
		self.nLastFullIndex = -1
		return

	def cal(self): 
		self.cal_x()
		self.cal_y()
		return

	def cal_x(self):
		self.nRight = self.game.arrWindowSize[0] - self.rect.x - self.rect.width 
		return

	def cal_y(self):
		self.nBottom = self.game.arrWindowSize[1] - self.rect.y - self.rect.height
		return

	def left(self, n=None):
		if n is not None : 
			self.rect.x = n
			self.nRight = self.game.arrWindowSize[0] - self.rect.x - self.rect.width 
		return self.rect.x

	def right(self, n=None):
		if n is not None : 
			self.nRight = n 
			self.rect.x = self.game.arrWindowSize[0] - self.nRight - self.rect.width
		return self.nRight

	def top(self, n=None):
		if n is not None :
			self.rect.y = n 
			self.nBottom = self.game.arrWindowSize[1] - self.rect.y - self.rect.height
		return self.rect.y

	def bottom(self, n=None):
		if n is not None :
			self.nBottom = n 
			self.rect.y = self.game.arrWindowSize[1] - self.nBottom - self.rect.height
		return self.nBottom

	def width(self, n=None):
		if n is not None :
			self.rect.width = n 
			self.cal_x()
		return self.rect.width

	def height(self, n=None):
		if n is not None :
			self.rect.height = n 
			self.cal_y()
		return self.rect.height


	def map_card_pos(self, n, i=-1):

		key = "n"+str(n)+"i"+str(i) 

		if key not in self.mapCardPos :
			r = 1000 #기준 반지름 
			self.mapCardPos[key] = []

			if 0 <= i : #마우스 호버(확대)
				if 4 < n : 
					nStartAngle = 8.5
					nDiffAngle = 17/(n-1)
					nPadding = -163
				else : 
					nStartAngle = 2.5*(n-1)
					nDiffAngle = 5
					nPadding = -163
			else :
				if 4 < n : 
					nStartAngle = 11
					nDiffAngle = 22/(n-1)
					nPadding = -100
				else : 
					nStartAngle = 2.5*(n-1)
					nDiffAngle = 5
					nPadding = -100
			
			bFull = False
			nLastX = 0
			for j in range(0, n) :
				nAngle = nStartAngle-nDiffAngle*j
				dX = r*math.sin(math.radians(nAngle))
				dY = r*(1-math.cos(math.radians(nAngle)))/3
				if i==j : #확대
					self.mapCardPos[key].append( [rd(-dX+nPadding),rd(-dY),nAngle] )
					bFull = True
					#이하 확대후 패딩 
					if n > 4 : #카드 많을때 
						if nAngle > 0 :#왼쪽편
							l = self.nFullCardX*math.cos(math.radians(nAngle))+self.nFullCardY*math.sin(math.radians(abs(nAngle)))
							nPadding = nPadding+self.nFullCardX+(l-self.nFullCardX)/2-3
						else : #오른쪽편 
							nNextAngle = nStartAngle-nDiffAngle*(j+1)
							l = self.nHandCardX*math.cos(math.radians(nNextAngle))+self.nHandCardY*math.sin(math.radians(abs(nNextAngle)))
							nPadding = nPadding+self.nFullCardX-(l-self.nHandCardX)/2-3
					elif n==4 :
						if j==0 : nPadding = nPadding+self.nFullCardX+17
						elif j==1 : nPadding = nPadding+self.nFullCardX
						elif j==2 : nPadding = nPadding+self.nFullCardX-14
					elif n==3 :
						if j==0 : nPadding = nPadding+self.nFullCardX+12
						elif j==1 : nPadding = nPadding+self.nFullCardX-14
					else : #카드 적을때 
						nPadding = nPadding+self.nFullCardX
					
				elif bFull :
					self.mapCardPos[key].append( [rd(-nLastX+nPadding),rd(160+dY),nAngle] )
				else :
					self.mapCardPos[key].append( [rd(-dX+nPadding),rd(160+dY),nAngle] )

				nLastX = dX

			#보정
			if n==3 :
				self.mapCardPos[key][1][1] += 2
			elif n==5 :
				self.mapCardPos[key][1][1] -= 4
				self.mapCardPos[key][3][1] -= 4
			elif n==6 :
				self.mapCardPos[key][1][1] -= 2
				self.mapCardPos[key][5][1] += 6
			elif n==7 :
				self.mapCardPos[key][1][1] -= 1
				self.mapCardPos[key][3][1] += 3
				self.mapCardPos[key][6][1] += 4
			elif n>7 :
				self.mapCardPos[key][-1][1] += 4


		return self.mapCardPos[key] # [ (x,y,a), (-10,20,4), ... ]


	def collidepoint(self, pos):
		for i in range(0, len(self.arrCard)) :
			if self.arrCard[i]["bFull"] and self.arrCard[i]["rect"].collidepoint(pos):
				pos2 = (pos[0]-self.arrCard[i]["rect"].x,pos[1]-self.arrCard[i]["rect"].y)
				if self.arrCard[i]["image"].get_at(pos2)[3]!=0 : return i
		for i in range(len(self.arrCard)-1, -1, -1) :
			if not self.arrCard[i]["bFull"] and self.arrCard[i]["rect"].collidepoint(pos):
				pos2 = (pos[0]-self.arrCard[i]["rect"].x,pos[1]-self.arrCard[i]["rect"].y)
				if self.arrCard[i]["image"].get_at(pos2)[3]!=0 : return i
		return -1


	def check_change(self):

		nCnt = len(self.arrCard)

		#마우스 호버 체크
		pos = pygame.mouse.get_pos()
		nIndex = self.collidepoint(pos)
		self.nSelectIndex = nIndex

		sState = str(nCnt)+"#"+str(nIndex) # "장수#인덱스"
		if sState==self.lastState : return False #변화 없음.
		self.lastState = sState

		#해당 상태의 카드 좌표들 가져오기 
		arrPos = self.map_card_pos(nCnt, nIndex)
		self.arrNowPos = arrPos

		#확대 플래그 초기화 
		for card in self.arrCard : card["bFull"] = False

		if len(self.arrCard) <= self.nLastFullIndex : self.nLastFullIndex = -1

		#확대 축소에따른 즉각 적용.
		if self.nLastFullIndex!=-1 and nIndex < self.nLastFullIndex: #인덱스가 작아지면 이전것이 오른쪽으로 이동해야함.
			self.arrCard[self.nLastFullIndex]["nX"] = self.arrCard[self.nLastFullIndex]["nX"] + self.nFullCardX/2

		if nIndex!=-1 and nIndex > self.nLastFullIndex: #인덱스가 커지면 현재것이 왼쪽으로 이동해야함
			self.arrCard[nIndex]["nX"] = self.arrCard[nIndex]["nX"] - 3*self.nFullCardX/4

		if self.nLastFullIndex!=-1 and self.nLastFullIndex!=nIndex : #이전 큰 카드 y축 변경
			self.arrCard[self.nLastFullIndex]["nY"] = self.arrCard[self.nLastFullIndex]["nY"] + (self.nFullCardY - self.nHandCardY)

		if nIndex!=-1 and self.nLastFullIndex!=nIndex : #확대할 카드 y축 변경 
			self.arrCard[nIndex]["nY"] = self.arrCard[nIndex]["nY"] - (self.nFullCardY - self.nHandCardY)
			self.arrCard[nIndex]["bFull"] = True

		#마지막 인덱스로 저장.
		self.nLastFullIndex = nIndex

		#이하 각 카드들 애니메이션 걸기.
		for i in range(0,nCnt):
			#애니메이션 플래그 및 목표치 적용.
			self.arrCard[i]["bAnim"] = True
			self.arrCard[i]["nAnimX"] = arrPos[i][0]
			self.arrCard[i]["nAnimY"] = arrPos[i][1]

			#x축 속도 설정.
			self.arrCard[i]["nSpeedX"] = (arrPos[i][0]-self.arrCard[i]["nX"])/3
			if self.arrCard[i]["nSpeedX"] > 0 : #오른쪽으로 이동시 
				self.arrCard[i]["nSpeedX"] = max(self.arrCard[i]["nSpeedX"], 10)
			else :
				self.arrCard[i]["nSpeedX"] = min(self.arrCard[i]["nSpeedX"], -10)

			#y축 속도 설정.
			self.arrCard[i]["nSpeedY"] = (arrPos[i][1]-self.arrCard[i]["nY"])/3
			if self.arrCard[i]["nSpeedY"] > 0 : #아래쪽으로 이동시 
				self.arrCard[i]["nSpeedY"] = max(self.arrCard[i]["nSpeedY"], 10)
			else :
				self.arrCard[i]["nSpeedY"] = min(self.arrCard[i]["nSpeedY"], -10)

			#회전각도 설정 
			self.arrCard[i]["nA"] = arrPos[i][2]


			# self.arrCard[i]["nX"] = arrPos[i][0]
			# self.arrCard[i]["nY"] = arrPos[i][1]

			if self.arrCard[i]["bFull"] : img = self.arrCard[i]["fullImage"]
			else : img = self.arrCard[i]["handImage"]
			# self.arrCard[i]["image"] = pygame.transform.rotate(img, arrPos[i][2])
			self.arrCard[i]["image"] = pygame.transform.rotozoom(img, arrPos[i][2], 1)
			self.arrCard[i]["rect"] = self.arrCard[i]["image"].get_rect()
			# self.arrCard[i]["rect"].x = self.rect.x+arrPos[i][0]+400
			# self.arrCard[i]["rect"].y = self.rect.y+arrPos[i][1]+140

			if i==nIndex :
				self.arrCard[i]["nX"] = arrPos[i][0]
				self.arrCard[i]["nY"] = arrPos[i][1]
				# self.arrCard[i]["bAnim"] = False

			self.arrCard[i]["rect"].x = self.rect.x+self.arrCard[i]["nX"]+400
			self.arrCard[i]["rect"].y = self.rect.y+self.arrCard[i]["nY"]+140

		return True

	def get_select_index(self):
		return self.nSelectIndex


	def animate_card(self) : 
		#애니메이션이 켜졌는지 체크 
		#애니메이션 켜졌으면 속도만큼 한번이동하고, 도착했는지 체크하고, 다되면 애니메이션 끄기.

		bAnim = any(card["bAnim"] for card in self.arrCard)
		if not bAnim : return

		for card in self.arrCard:
			if not card["bAnim"] : continue
			#속도를 체크해서 음수면 목표지점보다 작으면 완료 양수면 목표지점보다 크면 완료. 
			card["nX"] = card["nX"] + card["nSpeedX"]
			if card["nSpeedX"] > 0 and card["nX"] > card["nAnimX"] : card["nX"] = card["nAnimX"]
			elif card["nSpeedX"] < 0 and card["nX"] < card["nAnimX"] : card["nX"] = card["nAnimX"]

			card["nY"] = card["nY"] + card["nSpeedY"]
			if card["nSpeedY"] > 0 and card["nY"] > card["nAnimY"] : card["nY"] = card["nAnimY"]
			elif card["nSpeedY"] < 0 and card["nY"] < card["nAnimY"] : card["nY"] = card["nAnimY"]
			#축변경에 따른 판정위치 변경도 해줘야함.
			card["rect"].x = self.rect.x+card["nX"]+400
			card["rect"].y = self.rect.y+card["nY"]+140		

			#도착하면 애니메이션 종료 
			card["bAnim"] = not( card["nX"]==card["nAnimX"] and card["nY"]==card["nAnimY"] )
		
		#모든 애니메이션이 종료되면 강제로 좌표 고정해줌.
		bAnim = any(card["bAnim"] for card in self.arrCard)
		if not bAnim :
			for i in range(0,len(self.arrCard)) :
				self.arrCard[i]["nX"] = self.arrNowPos[i][0]
				self.arrCard[i]["nY"] = self.arrNowPos[i][1]
				self.arrCard[i]["rect"].x = self.rect.x+self.arrCard[i]["nX"]+400 
				self.arrCard[i]["rect"].y = self.rect.y+self.arrCard[i]["nY"]+140 

		return
	


	def update(self):
		bChange = self.check_change() #카드수 변화 호버 등 계산및 체크
		bAnim = any(card["bAnim"] for card in self.arrCard)
		if not bChange and not bAnim : return 
		self.animate_card() #애니메이션 있는지 체크

		#그리기 
		img = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
		# img.set_alpha(150)
		# img.fill((100,100,100))

		fullCard = None
		for i in range(0,len(self.arrCard)):
			if self.arrCard[i]["bFull"] : 
				fullCard = self.arrCard[i]
			else : 
				img.blit(self.arrCard[i]["image"],(400+self.arrCard[i]["nX"],140+self.arrCard[i]["nY"]))

		if fullCard is not None : #확대카드는 가장 마지막에 그림.
			img.blit(fullCard["image"],(400+fullCard["nX"],140+fullCard["nY"]))				

		self.image = img

		return

	def draw(self):
		if self.image is not None : self.game.screen.blit(self.image, self.rect)
		return


