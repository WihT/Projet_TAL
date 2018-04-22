import re

class LexField:
	"""Representation of a lexical field"""
	
	def __init__(self, content):
		self.paragraphs = content.split("\n\n")
		self.keyWords = self.paragraphs[0].split("\n")
		self.answers = self.paragraphs[1].split("\n")
		self.parents = []
		self.pertinent = 0
		#print(str(self))
		
	def __str__(self):
		return str(self.keyWords) + "\n" + str(self.answers)
		
	def __repr__(self):
		return str('{0:.2f}'.format(self.pertinent))
		
	def decrement(self):
		self.pertinent *= 0.7
		if self.pertinent < 0.5:
			self.pertinent = 0
			
	def increment(self, value):
		self.pertinent += value
		for subj in self.parents:
			subj.increment(value/2)