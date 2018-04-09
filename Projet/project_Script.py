import os
import random
import re
import argparse

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

def ansMode2(answer, lexicals) :
	ansWords = re.split("[ .,?!/()]+", answer)
	print(ansWords)
	for wAns in ansWords :
		for lex in lexicals :
			for wLex in lex :
				if matchLex(wAns, wLex) :
					print("I recognized the word " + wLex + " from lexical \"" + lex[0] + "\"")
	return
	
def matchLex(wAns, wLex) :
	if wAns.endswith("s") :
		if wAns.endswith("ies") :
			wAns = wAns[:-3] + "y"
		else :
			wAns = wAns[:-1]
	return wAns == wLex

def bot(answer, lexicals) : 
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you !")
		return False
	#print("Bob : "+ansMode1())
	ansMode2(answer, lexicals)
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

print("Bob : Hello")
while True:
    if bot(input("You : "), lexicals) == False :
        break
    