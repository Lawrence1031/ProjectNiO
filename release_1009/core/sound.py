import pygame
import os
import random


class Sound:
	def __init__(self, game):
		self.game = game
		self.nVolumeBgm = 0.1
		self.nVolumeSe = 0.3
		self.soundEffect = {}

		self.sSoundPath = "./sound/"
		self.sSoundEffectPath = self.sSoundPath+"se/"
		self.sSoundBgmPath = self.sSoundPath+"bgm/"

		self.load_se()

		return 


	def load_se(self):
		self.soundEffect = {}
		arrFileName = os.listdir(self.sSoundEffectPath)

		for sFileName in arrFileName:
			sCode = sFileName.split(".")[0]
			self.soundEffect[sCode] = pygame.mixer.Sound(self.sSoundEffectPath+sFileName)
		return

			
	def play(self, sSoundName):
		if hasattr(self, "play_"+sSoundName): 
			getattr(self, "play_"+sSoundName)()
		else : pygame.mixer.music.stop() 


	def play_Intro(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s03_intro_02.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Scenarioevent(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s06_scenario_01.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Stage1(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s06_stage_01.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Battleevent_1(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s08_battle_01.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Battleevent_2(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s08_battle_02.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Battleevent_3(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s08_battle_03.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Battleevent_boss(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s08_boss_01.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Battleevent_mid(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s08_mid-boss_01.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_Battleevent_victory(self):
		pygame.mixer.music.load(self.sSoundBgmPath+"s08_victory.ogg")
		pygame.mixer.music.set_volume(self.nVolumeBgm) #크기 
		pygame.mixer.music.play(-1)  # 반복재생
		return

	def play_VICTORY(self):
		sFileName = "s08_victory"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		def fn():
			self.soundEffect[sFileName].stop()
			return
		self.game.call_delay(fn, 2000)
		return
	
	def play_CANCEL(self):
		sFileName = "cancel"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_CURSOR(self):
		arrFileName = ["cursor1","cursor2"]
		sFileName = random.choice(arrFileName)
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_FOOTSTEP(self):
		arrFileName = ["s06_footstep-fast", "s06_footstep-middle (1)", "s06_footstep-middle (2)"]
		sFileName = random.choice(arrFileName)
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()

		def fn():
			self.soundEffect[sFileName].stop()
			return
		self.game.call_delay(fn, 2000)
		return

	def play_DAMAGE(self):
		sFileName = "s08_Damage"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_ENEMY_DESTROYED(self):
		arrFileName = ["s08_enemy_destroyed1","s08_enemy_destroyed2"]
		sFileName = random.choice(arrFileName)
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_GUNSHOT_01(self):
		sFileName = "s08_gunshot1"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_GUNSHOT_02(self):
		sFileName = "s08_gunshot2"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return


	def play_GUNSHOT_03(self):
		sFileName = "s08_gunshot3"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_GUNSHOT_04(self):
		sFileName = "s08_gunshot4"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_GUNSHOT_05(self):
		sFileName = "s08_gunshot5"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_GUNSHOT_06(self):
		sFileName = "s08_gunshot6"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_MACHINEGUN_01(self):
		sFileName = "s08_machinegun1"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_MACHINEGUN_02(self):
		sFileName = "s08_machinegun2"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_POWERUP(self):
		sFileName = "s08_powerup"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return

	def play_RELOAD(self):
		sFileName = "s08_reload"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return


	def play_SHIELD(self):
		sFileName = "s08_shield"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return




	def play_SHIELD_DESTROYED(self):
		sFileName = "s08_shield_destroyed"
		self.soundEffect[sFileName].set_volume(self.nVolumeSe)
		self.soundEffect[sFileName].play()
		return














