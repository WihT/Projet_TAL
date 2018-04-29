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
print("Bob : Hi I'm Bob! Please tell me something about you.")

while True:
	choice = bob.respond(input("You : "), subjects)
	if  choice < 0 :
		break
	#print(subjects)
	for subj in subjects :
		subj.decrement()
	#print(subjects)