import re
import random
import math
from lexicalField import LexField
from answer import Answer

class Bob:
	"""Representation of Bob"""
	
	
	def __init__(self, modeChoice):
		self.interest = 0
		self.stress = 0
		self.sympathy = 0
		self.prevChoices = []
		self.choiceMode1 = 0
		self.maxMode = modeChoice
		
	def __str__(self):
		return "interest = " + str(self.interest) + " ;  stress = " + str(self.stress) + " ;  sympathy = " + str(self.sympathy)


	def respond(self, answer, subjects) :
		if (answer.lower() == "bye") or (answer.lower() == "goodbye") or (answer.lower() == "see you"):
			return Answer("See you !", -1)
		
		if self.maxMode > 1 :
			ansWords = re.split("[ .,'?!/()]+", answer)
			influence = LexField.updateSubjects(ansWords, subjects)
			self.stress += influence[0]
			self.sympathy += influence[1]
		
		if self.maxMode == 3 :
			ansBob = self.ansMode3(ansWords, subjects)
		else :
			ansBob = Answer("Error : shouldn't be displayed", -1)
		
		if  ansBob.id == -1 :
			if self.maxMode > 1 :
				ansBob = self.ansMode2(subjects)
				if ansBob.id != -1 :
					self.interest = 0
			else :
				ansBob = Answer("Error : shouldn't be displayed", -1)
			if ansBob.id == -1 :
				ansBob = self.ansMode1()
				self.interest -= 1
		else : 
			self.interest = 0
		
		if ansBob.id > 9 : #that means it's a mode2 or mode3 answer
			self.prevChoices.append(ansBob.id)
			if len(self.prevChoices) > 20 :
				del self.prevChoices[0]
		
		if self.maxMode == 3 :
			if self.interest <= -5 :
				return Answer("Hm, it's getting late, I should leave.\n * Bob left the conversation because he got bored *", -2)
			if self.stress >= 5 :
				return Answer("Yeah hm... I think it's time for me to go to... the swimming pool... in order to... walk my pony or something like that...\n * Bob ran away from you, convinced you are from the NSA *", -3)
			if self.sympathy <= -5 :
				return Answer("Well this conversation was... interesting, but maybe you're too young to plainly understand these subjects.\n * Bob left the conversation because you have been too annoying to him *", -4)
				
		return ansBob
	
	def ansMode1(self) :
		choice = random.randint(0, 4)
		if choice >= self.choiceMode1 :
			choice += 1
		str = {
			0 : "Interesting...",
			1 : "Hmm...",
			2 : "Continue.",
			3 : "Tell me more.",
			4 : "I see...",
			5 : "Oh really?"
		}[choice]
		self.choiceMode1 = choice
		return Answer(str, choice)


	def ansMode2(self, subjects) :
		
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
		if len(maxSubjs) > 0 :
			ansList = [] #flattened list of the answers
			for iSubj in maxSubjs :
				for ans in subjects[iSubj].answers :
					ansList.append(ans)
			#Removing the previous answers in order to avoid repetition
			ansList = [ans for ans in ansList if ans.id not in self.prevChoices]
			if len(ansList) == 0 :
				return Answer("Error : shouldn't be displayed", -1)
			return ansList[random.randint(0, len(ansList)-1)]
		else :
			return Answer("Error : shouldn't be displayed", -1)


	def ansMode3(self, ansWords, subjects) :
		
		
		ansBob = Answer("Error : shouldn't be displayed", -1)
		
		if self.prevChoices != [] :
			
			lastChoice = self.prevChoices[len(self.prevChoices)-1]
			if math.floor(lastChoice/10)==100 :
				lastChoice = self.prevChoices[len(self.prevChoices)-2]
				
			if lastChoice == 41 :
				ansBob = self.miniMode2(ansWords, "worstInvention.txt")
			elif lastChoice == 93 :
				ansBob =  self.miniMode2(ansWords, "purposeMoney.txt")
			elif lastChoice == 190 :
				ansBob =  self.miniMode2(ansWords, "respoTerror.txt")
			elif lastChoice == 200 :
				ansBob =  self.miniMode2(ansWords, "purposeEdu.txt")
			elif lastChoice == 24 or lastChoice == 520 :
				ansBob = self.miniMode2(ansWords, "purposeGov.txt")
			elif lastChoice == 231 :
				if self.checkYesNo(ansWords) > 1 :
					self.sympathy -= 1
					ansBob = Answer("Well then, try to prove me Earth is round!", 233)
				elif self.checkYesNo(ansWords) < -1 :
					ansBob = self.approve()
				else :
					ansBob = self.askYesOrNo()
			elif lastChoice == 233 :
				ansBob = self.miniMode2(ansWords, "proveRoundEarth.txt")
			elif lastChoice == 90 and self.checkStunned(ansWords) > 1 :
				ansBob = Answer("Well, it's quite obvious to me. In your mind, what is the purpose of money?", 93)
			elif lastChoice == 193 and self.checkStunned(ansWords) > 1 :
				ansBob = Answer("Let's put it that way : who do you think is the real responsible for terrorism?", 190)
			elif lastChoice == 22 or lastChoice == 30 or lastChoice == 51 or lastChoice == 62 or lastChoice == 630 or lastChoice == 620 or lastChoice == 83 or lastChoice == 90 or lastChoice == 91 or lastChoice == 112 or lastChoice == 114 or lastChoice == 193 or lastChoice == 223 :
				if self.checkYesNo(ansWords) > 1 :
					ansBob = self.approve()
				elif self.checkYesNo(ansWords) < -1 :
					ansBob = self.disapprove()
				elif math.floor(self.prevChoices[len(self.prevChoices)-1]/10)!=100 :
					ansBob = self.askYesOrNo()
			elif lastChoice == 20 or lastChoice == 23 or lastChoice == 32 or lastChoice == 40 or lastChoice == 42 or lastChoice == 46 or lastChoice == 50 or lastChoice == 51 or lastChoice == 80 or lastChoice == 191 or lastChoice == 201 or lastChoice == 221 :
				if self.checkYesNo(ansWords) > 1 :
					ansBob = self.disapprove()
				elif self.checkYesNo(ansWords) < -1 :
					ansBob = self.approve()
				elif math.floor(self.prevChoices[len(self.prevChoices)-1]/10)!=100 :
					ansBob = self.askYesOrNo()
			
		return ansBob
		
			
	def miniMode2(self, ansWords, srcFile) :
		
		with open(srcFile,"r") as filepointer :
			content = filepointer.read()
			tmp = re.split("\n\n\n", content)
			currentSubjects = []
			for lex in tmp :
				currentSubjects.append(LexField(lex))
				
		influence = LexField.updateSubjects(ansWords, currentSubjects)
		self.stress += influence[0]
		self.sympathy += influence[1]
		
		ansBob = self.ansMode2(currentSubjects)
		
		# When the response of the user isn't clear enough to Bob,
		# He asks for precisions once, and then abandons if it's still not clear enough.
		if ansBob.id==-1 and math.floor(self.prevChoices[len(self.prevChoices)-1]/10)!=100 :
			return self.askPrecision()
			
		return ansBob
		

	def askYesOrNo(self) :
		choice = random.randint(0, 2)
		str = {
			0 : "So... is that a yes or a no?",
			1 : "You seem to hesitate...",
			2 : "So what would you say in conclusion?"
		}[choice]
		return Answer(str, choice+1000)
		
	def askPrecision(self) :
		choice = random.randint(0, 2)
		str = {
			0 : "So what's your point?",
			1 : "Okay, continue...",
			2 : "And what does it mean according to you?"
		}[choice]
		return Answer(str, choice+1000)
		
	def approve(self) :
		choice = random.randint(0, 3)
		str = {
			0 : "I'm glad to see I'm not the only one thinking that way!",
			1 : "I think you're right on that point.",
			2 : "At least one thing we agree on!",
			3 : "That's also what I think."
		}[choice]
		self.sympathy += 1
		return Answer(str, choice+1010)
		
	def disapprove(self) :
		choice = random.randint(0, 4)
		str = {
			0 : "I hope one day you will understand.",
			1 : "Oh god, no offense but you've been completely brainwashed.",
			2 : "Have you ever really thought about it? Or are you just repeating what you've learned?",
			3 : "Maybe you should think again about that.",
			4 : "I'm sad to hear that. Sad for you."
		}[choice]
		self.sympathy -= 1
		return Answer(str, choice+1015)
				
	#This method try to find out whether the user is stunned or not.
	def checkStunned(self, ansWords) :
		score = 0
		for iWord in range(len(ansWords)) :
			if ansWords[iWord] == "why" or ansWords[iWord] == "what" :
				score += 8 #Magic numbers :D
			elif ansWords[iWord] == "how" :
				score += 6
			elif ansWords[iWord] == "mean" or ansWords[iWord] == "meaning":
				score += 4
			elif ansWords[iWord] == "stunned" :
				score += 4
			elif ansWords[iWord] == "sorry" :
				score += 4
			elif ansWords[iWord] == "understand" :
				score += 4
			elif iWord + 2 <= len(ansWords) :
				if ansWords[iWord] == "not" and ansWords[iWord+1] == "sure" :
					score += 6
				if ansWords[iWord] == "nt" and ansWords[iWord+1] == "know" :
					score += 6
				elif ansWords[iWord] == "get" and (ansWords[iWord+1] == "it" or ansWords[iWord+1] == "that")  :
					score += 6
		return score/len(ansWords)
		
	# Returns a positive number if it thinks it's a yes, returns a negative if it thinks it's a no.
	def checkYesNo(self, ansWords) :
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
				if ansWords[iWord] == "i" :
					if ansWords[iWord+1] == "think" or ansWords[iWord+1] == "guess" or ansWords[iWord+1] == "do" or ansWords[iWord+1] == "am" :
						if iWord + 3 <= len(ansWords) and ansWords[iWord+2] == "not" :
							score -= 7
						else :
							score += 5
					elif iWord + 3 <= len(ansWords) and ansWords[iWord+1] == "don" and ansWords[iWord+2] == "t" :
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