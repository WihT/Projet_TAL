import os
import random
import re
import argparse
import numpy as np

def ansMode1(prevChoice) :
	choice = random.randint(0, 4)
	if choice >= prevChoice :
		choice += 1
	str = {
		0 : "Interesting...",
        1 : "Hmm...",
        2 : "So that's your opinion...",
        3 : "Continue...",
		4 : "Tell me more...",
        5 : "Yes...",
    }[choice]
	print ("Bob : " + str)
	return choice


def ansMode2(answer, lexicals, currSubj, botAnswers, prevChoice) :
	ansWords = re.split("[ .,?!/()]+", answer)
	#print(ansWords)
	for wAns in ansWords :
		for iLex in range(len(lexicals)) :
			for wLex in lexicals[iLex] :
				if matchLex(wAns, wLex) :
					#print("I recognized the word " + wLex + " from lexical \"" + lexicals[iLex][0] + "\"")
					currSubj[iLex] += 1
					
	#print(currSubj)
	maxSubj = currSubj.index(np.amax(currSubj))

	choice = random.randint(0, len(botAnswers[maxSubj])-2)
	if choice >= prevChoice :
		choice += 1
	prevChoice = choice

	mode2 = False

	for i in range(0, len(currSubj)-1) :
		if currSubj[i] != 0 :
			mode2 = True
			break

	if mode2 == False :
		return -1
	else :
		print ("Bob : " + botAnswers[maxSubj][choice])
		return choice

		
def ansMode3(answer, lexicals, currSubj, botAnswers, prevChoice) :
	return -1
	

def matchLex(wAns, wLex) :
	if wAns.endswith("s") :
		if wAns.endswith("ies") :
			wAns = wAns[:-3] + "y"
		else :
			wAns = wAns[:-1]
	return wAns == wLex

	
def bot(answer, lexicals, currSubj, botAnswers, prevChoice) :
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you !")
		return -1
	choice = ansMode3(answer, lexicals, currSubj, botAnswers, prevChoice)
	if  choice == -1 :
		choice = ansMode2(answer, lexicals, currSubj, botAnswers, prevChoice)
		if choice == -1 :
			choice = ansMode1(prevChoice)
	return choice

	
#  MAIN DEFINITION
with open("lexicals2.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\t+", content)
	lexicals = []
	for lex in tmp :
		lexicals.append(re.split("\n+", lex))
		
del lexicals[len(lexicals)-1][len(lexicals[len(lexicals)-1])-1]
#print(lexicals)

with open("answers2.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\t+", content)
	botAnswers = []
	for lex in tmp :
		botAnswers.append(re.split("\n+", lex))
		del botAnswers[len(botAnswers)-1][0]
		
del botAnswers[len(botAnswers)-1][len(botAnswers[len(botAnswers)-1])-1]
#print(botAnswers)

currSubj = [0] * len(lexicals)
prevChoice = 0

print("Bob : Hello")
print("Bob : Please tell me something about you.")
while True:
	choice = bot(input("You : "), lexicals, currSubj, botAnswers, prevChoice)
	if  choice == -1 :
		break
	for iSubj in range(len(currSubj)) :
		currSubj[iSubj] /= 2;
		if (currSubj[iSubj] < 1) :
			currSubj[iSubj] = 0;
	prevChoice = choice
	#print(currSubj)