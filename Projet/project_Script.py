import os
import random
import re
import argparse

prevchoice = 0

def answersmode1(x):
    return {
        1 : "hmm",
        2 : "uh huh",
        3 : "continue",
        4 : "yes",
    }[x]

def mode1(answer) :
	global prevchoice
	choice = random.randint(1,4)
	while prevchoice == choice :
		choice = random.randint(1,4)
	if (answer == "Bye") or (answer == "bye") :
		print("Bob : See you!")
		return False
	print("Bob : "+answersmode1(choice))
	prevchoice = choice
	return True

print("Bob : Hello")
while True:
    if mode1(input("You : ")) == False :
        break
    