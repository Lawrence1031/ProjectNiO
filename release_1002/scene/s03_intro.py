from core.scene import Scene
from core.dialog import Dialog
# from core.div import Div
import pygame
# from PIL import Image #pip install pillow
# import random


class Intro(Scene):
	def __init__(self, game):
		super().__init__(game, "Intro")

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
		self.next_scenario()
		return 
		

	def next_scenario(self):
		if len(self.dialog.arrTyping)>0 :
			self.dialog.end_typing()
			return

		self.nIndex += 1
		if len(self.arrScenario) <= self.nIndex :
			self.game.set_scene("Deckselect")
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
			if e.button == 1: 
				self.game.sound_play("CURSOR")
				self.next_scenario()

		except Exception as e: print(e)

	def update(self):
		try:


			self.game.screen.blit(self.img, (0, 0))
			# self.game.screen.blit(self.surfaceGray, (0, 0))
			# self.game.screen.blit(self.text_surface, (0, -60))

			self.dialog.update()
			self.dialog.draw()
			
		except Exception as e: print(e)
	

