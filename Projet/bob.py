import re
import random
from lexicalField import LexField

class Bob:
	"""Representation of a lexical field"""
	
	
	def __init__(self, subjs):
		self.sympathy = 0
		self.stress = 0
		self.interest = 0
		#print(str(self))
		
	def __str__(self):
		return str(self.sympathy) + "\n" + str(self.stress) + "\n" + str(self.interest)


	def respond(self, answer, subjects, prevChoice) :
		if (answer == "Bye") or (answer == "bye") :
			print("Bob : See you !")
			return -1
			
		#print("I recognized the word " + wLex + " from lexical \"" + lexicals[iLex][0] + "\"")
		
		ansWords = re.split("[ .,'?!/()]+", answer)
		for iWord in range(len(ansWords)):
			ansWords[iWord] = ansWords[iWord].lower()
			for iLex in range(len(subjects)) :
				for wLex in subjects[iLex].keyWords :
					if matchLex(ansWords[iWord], wLex) :
						subjects[iLex].increment(1)
				for gLex in subjects[iLex].keyGroups :
					if iWord + len(gLex) <= len(ansWords) :
						i = 0
						while i < len(gLex) and matchLex(ansWords[iWord+i], gLex[i]) :
							i += 1
						if i == len(gLex) :
							subjects[iLex].increment(1)
		
		choice = self.ansMode3(ansWords, subjects, prevChoice)
		if  choice == -1 :
			choice = self.ansMode2(subjects, prevChoice)
			if choice == -1 :
				choice = self.ansMode1(prevChoice)
		return choice


	def ansMode1(self, prevChoice) :
		choice = random.randint(0, 4)
		if choice >= prevChoice :
			choice += 1
		str = {
			0 : "Interesting...",
			1 : "Hmm...",
			2 : "Continue.",
			3 : "Tell me more.",
			4 : "I see...",
			5 : "Oh really?"
		}[choice]
		print ("Bob : " + str)
		return choice


	def ansMode2(self, subjects, prevChoice) :
		
		maxSubjs = []
		maxPertinence = 0
		for iSubj in range(len(subjects)):
			if subjects[iSubj].pertinent > maxPertinence:
				maxPertinence = subjects[iSubj].pertinent
				maxSubjs = []
				maxSubjs.append(iSubj)
			elif subjects[iSubj].pertinent == maxPertinence and maxPertinence > 0:
				maxSubjs.append(iSubj)
		
		# if there are several equally pertinent subjects, Bob chooses one randomly
		if (len(maxSubjs) > 0):
			maxSubj = maxSubjs[random.randint(0, len(maxSubjs)-1)]
			choice = random.randint(0, len(subjects[maxSubj].answers)-2)
			if choice >= prevChoice :
				choice += 1
			prevChoice = choice
			print ("Bob : " + subjects[maxSubj].answers[choice])
			return choice
		else:
			return -1


	def ansMode3(self, ansWords, subjects, prevChoice) :
		yesNo = checkYesNo(ansWords)
		if yesNo >  1:
			print("*Bob thinks you said yes.* ( yesNo = " + str(yesNo) + " )")
			self.sympathy += 1
		elif yesNo < -1 :
			print("*Bob thinks you said no* ( yesNo = " + str(yesNo) + " )")
			self.sympathy -= 1
		else :
			print("*Bob thinks you hesitate.* ( yesNo = " + str(yesNo) + " )")
		
		if checkStunned(ansWords) > 0 :
			print("*Bob notices you are stunned*")
	   
		return -1
			

				
#This type of method returns a positive number if it thinks the idea is present in the sentence.
def checkStunned(ansWords) :
	score = 0
	for iWord in range(len(ansWords)):
		if ansWords[iWord] == "why" :
			score += 7 #Magic numbers :D
		elif ansWords[iWord] == "what" :
			score += 7
		elif ansWords[iWord] == "mean" :
			score += 3
		elif ansWords[iWord] == "stunned" :
			score += 3
		elif ansWords[iWord] == "you" :
			score += 3
		elif iWord + 2 <= len(ansWords) :
			if ansWords[iWord] == "not" and ansWords[iWord+1] == "sure" :
				score += 5
		else :
			score -= 1
	return score/len(ansWords)
	
# Returns a positive number if it thinks it's a yes, returns a negative if it thinks it's a no.
def checkYesNo(ansWords) :
	score = 0
	for iWord in range(len(ansWords)):
		if ansWords[iWord] == "yes" or ansWords[iWord] == "yep" or ansWords[iWord] == "yeah" :
			score += 10
		elif ansWords[iWord] == "no" or ansWords[iWord] == "nope":
			score -= 10
		elif ansWords[iWord] == "affirmative" :
			score += 7
		elif ansWords[iWord] == "negative" :
			score -= 7
		elif ansWords[iWord] == "not" :
			score -= 3
			if iWord + 2 <= len(ansWords) and ansWords[iWord+1] == "sure" :
				return 0
		elif iWord + 2 <= len(ansWords) :
			if ansWords[iWord] == "i":
				if ansWords[iWord+1] == "think" or ansWords[iWord+1] == "guess" or ansWords[iWord+1] == "do" :
					if iWord + 3 <= len(ansWords) and ansWords[iWord+2] == "not" :
						score -= 7
					else :
						score += 5
				elif iWord + 3 <= len(ansWords) and ansWords[iWord+1] == "don" and ansWords[iWord+2] == "t":
					score -= 7
					if iWord + 4 <= len(ansWords) and ansWords[iWord+3] == "know" :
						return 0
			elif ansWords[iWord] == "of" and ansWords[iWord+1] == "course" :
				if iWord + 3 <= len(ansWords) and ansWords[iWord+2] == "not" :
					score -= 10
				else :
					score += 2
					score *= 2
		if ansWords[iWord] == "if" or ansWords[iWord] == "normally" or ansWords[iWord] == "maybe" :
			score /= 4
	return score/len(ansWords)

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