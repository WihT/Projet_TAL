import re

class LexField:
	"""Representation of a lexical field"""
	keyWords = []
	keyGroups = []
	answers = []
	parentFieldsID = []
	
	def __init__(self, content):
		self.paragraphs = content.split("\n\n")
		self.keyWords = self.paragraphs[0].split("\n")
		self.answers = self.paragraphs[1].split("\n")
		#print(str(self))
		
	def __str__(self):
		return str(self.keyWords) + "\n" + str(self.answers)