import os
import random
import re
import argparse

prevChoice = 0

def ansMode1():
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

def bot(answer) :
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you !")
		return False
	print("Bob : "+ansMode1())
	return True

#main
print("Bob : Hello")
while True:
    if bot(input("You : ")) == False :
        break
    