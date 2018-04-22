import re

class LexField:
	"""Representation of a lexical field"""
	subjects = []
	
	def __init__(self, content):
		self.paragraphs = content.split("\n\n")
		self.keyWords = self.paragraphs[0].split("\n")
		self.answers = self.paragraphs[1].split("\n")
		self.keyGroups = []
		self.parents = []
		self.pertinent = 0
		i = 0
		while i < len(self.keyWords):
			if self.keyWords[i].startswith(">"):
				self.parents.append(self.keyWords[i])
				del self.keyWords[i]
			elif " " in self.keyWords[i]:
				self.keyGroups.append(self.keyWords[i].split(" "))
				del self.keyWords[i]
			else:
				i += 1
		
		LexField.subjects.append(self)
		
	def __str__(self):
		return str(self.keyWords) + "\n" + str(self.keyGroups) + "\n" + str(self.parents) + "\n" + str(self.answers) + "\n"
		
	def __repr__(self):
		return str('{0:.2f}'.format(self.pertinent))
	
	# Bob quickly forgets about a subject when you stop talking about it
	def decrement(self):
		self.pertinent *= 0.6
		if self.pertinent < 0.4:
			self.pertinent = 0
	
	# Some subjects are linked to each other :
	# when you talk about reptiles, Bob also think about reptilians
	# so "reptilian" lexField is a parent of "reptile" lexField
	def increment(self, value):
		self.pertinent += value
		for subj in self.parents:
			LexField.subjects[subj].increment(value*0.6)
	
	# We replace all of the parents names by their IDs, in order to save time later
	@staticmethod
	def linkParents():
		subjs = LexField.subjects
		for iChild in range(len(subjs)):
			idList = []
			for iParent in range(len(subjs[iChild].parents)):
				for iSubj in range(len(subjs)):
					if subjs[iChild].parents[iParent][1:] == subjs[iSubj].keyWords[0]:
						idList.append(iSubj)
			subjs[iChild].parents = idList
			#print(subjs[iChild])
			