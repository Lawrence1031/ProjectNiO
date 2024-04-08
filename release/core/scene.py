
class Scene:
	def __init__(self, game, sSceneName):
		self.sSceneName = sSceneName
		self.game = game
		self.bControl = False
		return 
	
	check_name = lambda self, sSceneName: self.sSceneName == sSceneName
	load = lambda self : None
	event = lambda self, e : None
	update = lambda self : None


