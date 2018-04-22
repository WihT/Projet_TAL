import os
import random
import re
import argparse
import sys
import numpy as np
from lexicalField import LexField
    
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


def ansMode2(answer, lexFields, prevChoice) :
	for wAns in answer :
		for iLex in range(len(lexFields)) :
			for wLex in lexFields[iLex].keyWords :
				if matchLex(wAns, wLex) :
					#print("I recognized the word " + wLex + " from lexical \"" + lexicals[iLex][0] + "\"")
					lexFields[iLex].increment(1)
					
	maxSubjs = []
	maxPertinence = 0
	for iSubj in range(len(lexFields)):
		if lexFields[iSubj].pertinent > maxPertinence:
			maxPertinence = lexFields[iSubj].pertinent
			maxSubjs = []
			maxSubjs.append(iSubj)
		elif lexFields[iSubj].pertinent == maxPertinence and maxPertinence > 0:
			maxSubjs.append(iSubj)
	
	# if there are several equally pertinent subjects, Bob chooses one randomly
	if (len(maxSubjs) > 0):
		maxSubj = maxSubjs[random.randint(0, len(maxSubjs)-1)]
		choice = random.randint(0, len(lexFields[maxSubj].answers)-2)
		if choice >= prevChoice :
			choice += 1
		prevChoice = choice
		print ("Bob : " + lexFields[maxSubj].answers[choice])
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
def ansMode3(answer, lexFields, prevChoice, sympathy) :
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

	
def bot(answer, lexFields, prevChoice, sympathy) :
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you !")
		return -1
	
	ansWords = re.split("[ .,?!/()]+", answer)
    
	choice, sympathy = ansMode3(ansWords, lexFields, prevChoice, sympathy)
	if sympathy <= -5 :
		return choice, sympathy
	if  choice == -1 :
		choice = ansMode2(ansWords, lexFields, prevChoice)
		if choice == -1 :
			choice = ansMode1(prevChoice)
	return choice, sympathy

	
#  MAIN DEFINITION

with open("lexFields.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\t", content)
	lexFields = []
	for lex in tmp :
		lexFields.append(LexField(lex))
		
sympathy = 0
prevChoice = 0

print("Bob : Hello")
print("Bob : Please tell me something about you.")
while True:
	choice, sympathy = bot(input("You : "), lexFields, prevChoice, sympathy)
	if sympathy <= -5 :
		print("You monster !")
		print("*Bob run away from you*")
		break
	if  choice == -1 :
		break
	#print(lexFields)
	for subj in lexFields :
		subj.decrement()
	prevChoice = choice
	#print(lexFields)