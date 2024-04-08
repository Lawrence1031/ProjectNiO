from core.scene import Scene
import pygame

class Loading(Scene):
	def __init__(self, game):
		super().__init__(game, "Loading")

		self.load()
		return 

	def load(self):
		img = pygame.image.load("img/s01_bg.png")
		img2 = pygame.image.load("img/s01_loadingbar.png")
		self.imgBg = img
		self.imgLoadingbarFull = pygame.image.load("img/s01_loadingbar_full.png")
		return 

	def update_loading_bar(self, nPer):
		ract = self.imgLoadingbarFull.get_rect()
		width = ract.width * nPer / 100 
		img = pygame.transform.scale(self.imgLoadingbarFull, (width,ract.height))

		self.game.screen.blit(img, (72, 646))
		pygame.display.update()
		return
		
	def unload(self):
		del self.imgBg
		del self.imgLoadingbarFull
		return 		

	def update(self):
		try:
			self.game.screen.blit(self.imgBg, (0, 0))
		except Exception as e: print(e)
	

