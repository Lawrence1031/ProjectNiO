import pygame


def load_icon(sPath, sColor):
	color = pygame.Surface((30, 30), pygame.SRCALPHA)		
	if sColor == "RED" : color.fill((204, 0, 0))
	else : color.fill((0, 102, 204))

	img = pygame.image.load(sPath) #512 512
	img = pygame.transform.smoothscale(img, (30, 30 ))
	img.blit(color, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

	back = pygame.Surface((30, 30), pygame.SRCALPHA)
	back.fill((0,0,0,200))
	back.blit(img, (0, 0))
	return back

ICON_BACK_PAIN 		= load_icon("icons/lorc/back-pain.png","RED")
ICON_CONDOR_EMBLEM 	= load_icon("icons/lorc/condor-emblem.png","BLUE")
ICON_SPRINT 		= load_icon("icons/lorc/sprint.png","BLUE")
ICON_SLAVERY_WHIP 	= load_icon("icons/lorc/slavery-whip.png","RED")

class Buff:
	def __init__(self, sCode, nStart):
		self.sCode = sCode
		self.nStart = nStart #시작조건

		self.buff_default()
		if hasattr(self, "buff_"+sCode): 
			getattr(self, "buff_"+sCode)()
		self.nEnd = self.nStart + self.nTurn
		return 


	def load_icon(self, sPath, sColor):
		color = pygame.Surface((30, 30), pygame.SRCALPHA)		
		if sColor == "RED" : color.fill((204, 0, 0))
		else : color.fill((0, 102, 204))

		img = pygame.image.load(sPath) #512 512
		img = pygame.transform.smoothscale(img, (30, 30 ))
		img.blit(color, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

		back = pygame.Surface((30, 30), pygame.SRCALPHA)
		back.fill((0,0,0,200))
		back.blit(img, (0, 0))
		return back

	def buff_default(self):
		self.nAD = 0
		self.nAP = 0
		self.icon = None
		self.nTurn = 0
		return

	def buff_001(self):
		# 카드 007 조준사격 : 적의 공격력을 2턴동안 (5) 감소시킨다.
		self.nAD = -5
		self.nTurn = 2
		self.icon = ICON_BACK_PAIN
		return 


	def buff_002(self):
		# 카드 401 격려 : 이번 전투 종료 시까지 공격력을 (1)올린다.
		self.nAD = 1
		self.nTurn = 999
		self.icon = ICON_CONDOR_EMBLEM
		return 

	def buff_003(self):
		# 카드 403 몸풀기 : 이번 턴 종료 시까지 공격력을 (1)올린다.
		self.nAD = 1
		self.nTurn = 1
		self.icon = ICON_SPRINT
		return 

	def buff_004(self):
		# 801 경비로봇이 거는 탈진
		self.nAD = -5
		self.nTurn = 1
		self.icon = ICON_SLAVERY_WHIP
		return 












