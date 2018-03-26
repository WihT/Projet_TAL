import os
import random
import re
import argparse

prevchoice = 0

def answers(x):
    return {
        1 : "hmm",
        2 : "uh huh",
        3 : "continue",
        4 : "yes",
    }[x]

def bot(answer) :
	global prevchoice
	choice = random.randint(1,4)
	while prevchoice == choice :
		choice = random.randint(1,4)
	print("Bob : "+answers(choice))
	prevchoice = choice
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you!")
		return False
	return True

print("Bob : Hello")
while True:
    if bot(input("You : ")) == False :
        break
    