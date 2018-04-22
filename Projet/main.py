import os
import random
import re
import argparse
import sys
import numpy as np
from lexicalField import LexField
from bob import Bob
    
def ansMode1(prevChoice) :
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


def ansMode2(answer, subjects, prevChoice) :
	
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
		

def checkYes(answer) :
    for word in answer :
        if word.lower().startswith("ye") :
            return True
        else :
            if word.lower() == "affirmative" :
                return True
            else : 
                return False

def checkNo(answer) :
    for word in answer :
        if word.lower().startswith("no") :
            return True
        else :
            if word.lower() == "negative" :
                return True
            else : 
                return False
def ansMode3(answer, subjects, prevChoice, sympathy) :
   if checkYes(answer) :
       print("*Bob writes it in his notebook.*")
       sympathy += 1
   if checkNo(answer) :
       print("*Bob writes it in his notebook.*")
       sympathy -= 1
   
   return -1, sympathy

def matchLex(wAns, wLex) :
	wAns = wAns.lower()
	if wLex.endswith("_") : # That means the words must be compared as they are
		return wAns == wLex[:-1]
	if wAns.endswith("s") :
		if wAns.endswith("ies") :
			wAns = wAns[:-3] + "y"
		else :
			wAns = wAns[:-1]
	return wAns == wLex

	
def bot(answer, subjects, prevChoice, sympathy) :
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you !")
		return -1, sympathy
		
	#print("I recognized the word " + wLex + " from lexical \"" + lexicals[iLex][0] + "\"")
	
	ansWords = re.split("[ .,?!/()]+", answer)
	for iWord in range(len(ansWords)):
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
    
	choice, sympathy = ansMode3(ansWords, subjects, prevChoice, sympathy)
	if sympathy <= -5 :
		return choice, sympathy
	if  choice == -1 :
		choice = ansMode2(ansWords, subjects, prevChoice)
		if choice == -1 :
			choice = ansMode1(prevChoice)
	return choice, sympathy

	
#  MAIN DEFINITION

with open("lexFields.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\t", content)
	subjects = []
	for lex in tmp :
		subjects.append(LexField(lex))
		
LexField.linkParents()
subjects = LexField.subjects
		
sympathy = 0
prevChoice = 0

print("Bob : Hello")
print("Bob : Please tell me something about you.")
while True:
	choice, sympathy = bot(input("You : "), subjects, prevChoice, sympathy)
	if sympathy <= -5 :
		print("You monster !")
		print("*Bob run away from you*")
		break
	if  choice == -1 :
		break
	print(subjects)
	for subj in subjects :
		subj.decrement()
	prevChoice = choice
	print(subjects)