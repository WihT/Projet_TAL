class Bob:
	"""Representation of a lexical field"""
	subjects = []
	
	def __init__(self):
		self.sympathy = 0
		self.stress = 0
		self.interest = 0
		#print(str(self))
		
	def __str__(self):
		return str(self.keyWords) + "\n" + str(self.answers)
		
	def __repr__(self):
		return str('{0:.2f}'.format(self.pertinent))