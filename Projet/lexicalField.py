import re
from answer import Answer

class LexField:
	"""Representation of a lexical field"""
	subjects = []
	
	def __init__(self, content):
		paragraphs = content.split("\n\n")
		if "|" in paragraphs[0] :
			numbers = paragraphs[0].split("|")
			id = int(int(numbers[0]))
			self.influence = [int(numbers[1]), int(numbers[2])]
		else :
			self.influence = []
			id = int(paragraphs[0])
		self.keyWords = paragraphs[1].split("\n")
		tempAnswers = paragraphs[2].split("\n")
		self.answers = []
		for iAns in range(len(tempAnswers)) :
			self.answers.append(Answer(tempAnswers[iAns], id*10+iAns))
		self.keyGroups = []
		self.parents = []
		self.pertinent = 0
		i = 0
		while i < len(self.keyWords) :
			if self.keyWords[i].startswith(">") :
				self.parents.append(self.keyWords[i])
				del self.keyWords[i]
			elif " " in self.keyWords[i]:
				self.keyGroups.append(self.keyWords[i].split(" "))
				del self.keyWords[i]
			else:
				i += 1
		
		
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
	def increment(self, value, container):
		self.pertinent += value
		if value > 0.1 :
			for subj in self.parents:
				container[subj].increment(value*0.6, container)
	
	# We replace all of the parents names by their IDs, in order to save time later
	@staticmethod
	def linkParents(subjs):
		for iChild in range(len(subjs)):
			idList = []
			for iParent in range(len(subjs[iChild].parents)):
				for iSubj in range(len(subjs)):
					if subjs[iChild].parents[iParent][1:] == subjs[iSubj].keyWords[0]:
						idList.append(iSubj)
			subjs[iChild].parents = idList
			
	@staticmethod
	def updateSubjects(ansWords, subjects) :
	
		incrInfl = [0, 0]
		
		for iWord in range(len(ansWords)) :
			ansWords[iWord] = ansWords[iWord].lower()
			for iLex in range(len(subjects)) :
				for wLex in subjects[iLex].keyWords :
					if LexField.matchLex(ansWords[iWord], wLex) :
						subjects[iLex].increment(1, subjects)
				for gLex in subjects[iLex].keyGroups :
					if iWord + len(gLex) <= len(ansWords) :
						i = 0
						while i < len(gLex) and LexField.matchLex(ansWords[iWord+i], gLex[i]) :
							i += 1
						if i == len(gLex) :
							subjects[iLex].increment(1, subjects)
							if subjects[iLex].influence != [] :
								incrInfl[0] += subjects[iLex].influence[0]
								incrInfl[1] += subjects[iLex].influence[1]
								
		return incrInfl
								

	@staticmethod
	def matchLex(wAns, wLex) :
		if wLex.endswith("_") : # That means the words must be compared as they are
			return wAns == wLex[:-1]
		if wAns.endswith("al") :
			wAns = wAns[:-2]
		elif wAns.endswith("ly") :
			if wAns.endswith("ally") :
				wAns = wAns[:-4]
			else :
				wAns = wAns[:-2]
		elif wAns.endswith("s") :
			if wAns.endswith("ies") :
				wAns = wAns[:-3] + "y"
			else :
				wAns = wAns[:-1]
		if wAns.endswith("st") :
			wAns = wAns[:-1] + "m"
		return wAns == wLex
	
			