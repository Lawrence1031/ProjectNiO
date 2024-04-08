import pygame


class Ptt():
	def __init__(self):
		self.shape = None
		self.nFrame = 0
		self.pos = [0,0] #x,y
		self.sType = "UP_TEXT"
		self.bEnd = False

		return 

class Poptext():
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.arrPtt = []
		return


	def add_text(self, pos, sText, sType="UP_TEXT", sTextAlign="CENTER"):
		ptt = Ptt()
		ptt.sType = sType

		if sType=="UP_TEXT" :
			font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 20)
			ptt.shape = font.render(sText, True, (255,46,99))
			rect = ptt.shape.get_rect()

			nX = pos[0]
			nY = pos[1]-rect.height/2
			if sTextAlign=="CENTER" : 
				nX = pos[0]-rect.width/2
			elif sTextAlign=="RIGHT" : 
				nX = pos[0]-rect.width

			ptt.pos = [nX, nY]
			ptt.nFrame = 60

		elif sType=="UP_MONSTER_TEXT" :
			font = pygame.font.Font("./font/NotoSansKR-Regular.otf", 25)
			ptt.shape = font.render("  "+sText+"  ", True, (91, 109, 91), (246, 230, 228))
			rect = ptt.shape.get_rect()

			nX = pos[0]
			nY = pos[1]-rect.height/2
			if sTextAlign=="CENTER" : 
				nX = pos[0]-rect.width/2
			elif sTextAlign=="RIGHT" : 
				nX = pos[0]-rect.width

			ptt.pos = [nX, nY]
			ptt.nFrame = 40


		self.arrPtt.append(ptt)

		return 


	def update(self):
		
		for ptt in self.arrPtt : 
			ptt.nFrame -= 1
			if ptt.nFrame < 0 :
				ptt.bEnd = True
				continue

			if ptt.sType=="UP_TEXT" : 
				if ptt.nFrame <= 30 : ptt.pos[1] -= 1

			elif ptt.sType=="UP_MONSTER_TEXT" : 
				if ptt.nFrame <= 20 : ptt.pos[1] -= 2	

		for i in range(len(self.arrPtt)-1, -1, -1):
			if self.arrPtt[i].bEnd : self.arrPtt.pop(i)

		return


	def draw(self):
		for ptt in self.arrPtt : 
			self.game.screen.blit(ptt.shape, ptt.pos)

		return
