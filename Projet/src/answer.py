import re

class Answer:
	"""Representation of a possible answer from Bob"""
	subjects = []
	
	def __init__(self, content, id) :
		self.content = content
		self.id = id
		
		
	def __str__(self) :
		return self.content
		
	def __repr__(self) :
		return str(self.id)