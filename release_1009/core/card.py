import time

class Card:
	def __init__(self, cardinfo):
		self.cardinfo = cardinfo

		for k, v in cardinfo.__dict__.items():
		    if not callable(v):
		    	setattr(self, k, v)

		self.sId = self.sCode+str(time.time())
		self.bInRaid = False
		return 

			
