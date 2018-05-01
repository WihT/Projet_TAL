import os
import re
import argparse
import sys
from bob import Bob
from lexicalField import LexField
    
#  MAIN DEFINITION

with open("lexFields.txt","r") as filepointer :
	# lecture du fichier de champs lexicaux
	content = filepointer.read()
	tmp = re.split("\n\n\n", content)
	subjects = []
	for lex in tmp :
		subjects.append(LexField(lex))
		
LexField.linkParents(subjects)
		
bob = Bob()
print("Bob : Hi I'm Bob! What could we talk about?")

while True:
	answer = bob.respond(input("You : "), subjects)
	#print(subjects)
	print(bob)
	print("Bob : " + str(answer))
	if  answer.id < 0 :
		break
	for subj in subjects :
		subj.decrement()