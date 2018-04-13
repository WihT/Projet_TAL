import os
import random
import re
import argparse
import numpy as np

prevChoice = 0

def ansMode1() :
	global prevChoice
	x = random.randint(0,1024)%6
	while prevChoice == x :
		x = random.randint(0,1024)%6
	prevChoice = x
	return {
		0 : "Interesting...",
        1 : "Hmm...",
        2 : "So that's your opinion...",
        3 : "Continue...",
		4 : "Tell me more...",
        5 : "Yes...",
    }[x]

def ansMode2(answer, lexicals, currSubj, botAnswers) :
	ansWords = re.split("[ .,?!/()]+", answer)
	#print(ansWords)
	for wAns in ansWords :
		for iLex in range(len(lexicals)) :
			for wLex in lexicals[iLex] :
				if matchLex(wAns, wLex) :
					#print("I recognized the word " + wLex + " from lexical \"" + lexicals[iLex][0] + "\"")
					currSubj[iLex] += 1
	maxSubj = currSubj.index(np.amax(currSubj))

	global prevChoice
	x = random.randint(0, len(botAnswers[maxSubj])-1)
	while prevChoice == x :
		x = random.randint(0, len(botAnswers[maxSubj])-1)
	prevChoice = x

	mode2 = False

	for i in range(0,len(currSubj)-1) :
		if currSubj[i] != 0 :
			mode2 = True
			break

	if mode2 == False :
		return False
	else :
		print ("Bob : " + botAnswers[maxSubj][x])
		return True

def ansMode3(answer, lexicals, currSubj, botAnswers) :

	return False
	
def matchLex(wAns, wLex) :
	if wAns.endswith("s") :
		if wAns.endswith("ies") :
			wAns = wAns[:-3] + "y"
		else :
			wAns = wAns[:-1]
	return wAns == wLex

def bot(answer, lexicals, currSubj, botAnswers) :
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you !")
		return True


	if ansMode3(answer, lexicals, currSubj, botAnswers) == False :
		if ansMode2(answer, lexicals, currSubj, botAnswers) == False :
			print("Bob : "+ansMode1())
	return True

#  MAIN DEFINITION
with open("lexicals.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\t+", content)
	lexicals = []
	for lex in tmp :
		lexicals.append(re.split("\n+", lex))
		
del lexicals[len(lexicals)-1][len(lexicals[len(lexicals)-1])-1]
#print(lexicals)

with open("answers.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\t+", content)
	botAnswers = []
	for lex in tmp :
		botAnswers.append(re.split("\n+", lex))
		del botAnswers[len(botAnswers)-1][0]
		
del botAnswers[len(botAnswers)-1][len(botAnswers[len(botAnswers)-1])-1]
#print(botAnswers)

currSubj = [0] * len(lexicals);

print("Bob : Hello")
print("Bob : Please tell me something about you.")
while True:
	if bot(input("You : "), lexicals, currSubj, botAnswers) == False :
		break
	for iSubj in range(len(currSubj)) :
		currSubj[iSubj] /= 2;
		if (currSubj[iSubj] < 1) :
			currSubj[iSubj] = 0;
	#print(currSubj)