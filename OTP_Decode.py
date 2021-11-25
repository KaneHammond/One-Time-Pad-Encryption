import random
import os
import sys
import itertools
from itertools import izip_longest
# Import our encryption methods
from Encryptions import*
# Define the base numbers and letter
LN = [['A', 1], ['B', 2], ['C', 3], ['D', 4], ['E', 5], ['F', 6], ['G', 7], 
	['H', 8], ['I', 9], ['J', 10], ['K', 11], ['L', 12], ['M', 13], ['N', 14],
	['O', 15], ['P', 16], ['Q', 17], ['R', 18], ['S', 19], ['T', 20], ['U', 21],
	['V', 22], ['W', 23], ['X', 24], ['Y', 25], ['Z', 26]]

################################# Pull Data ###############################
# Pull in our text file.
RawData = []

with open('MyFile.txt') as Doc:
	for anItem in Doc:
		RawData.append(anItem)
Doc.close()

################################# List Data ###############################

# Define the message key versus the coded message
Key = []
CodedMessage = []

InKey = False
InMessage = False

for anItem in RawData:
	# Check for message key
	if anItem == '_________________MESSAGE KEY_________________\n':
		InKey = True
	# Check for message alone
	if anItem == '________________CODED MESSAGE________________\n':
		InKey = False
		InMessage = True
	if InKey == True:
		# We are in the key
		Key.append(anItem)
	if InMessage == True:
		# We are in the message
		CodedMessage.append(anItem)

# Drop first item
CodedMessage = CodedMessage[1::]
Key = Key[1::]

################################# Key numerical conversion ####################
# Convert these items to the correct format
KeyString = ''
# Write a continuous string
for anItem in Key:
	# Remove the new line deliminator
	Mod1 = anItem.replace('\n', '')
	# Remove the spacing
	Mod2 = Mod1.replace(' ', '')
	# Add to overall string
	KeyString = KeyString+Mod2

# Convert key to numerical form
KeyNumbers = []

for aLetter in KeyString:
	for aVal in LN:
		if aLetter == aVal[0]:
			# The letter matches, pull the integer
			KeyNumbers.append(aVal[1])

######################### Message numerical conversion ####################	

CodedMessageString = ''		
# Write a continuous string
for anItem in CodedMessage:
	# Remove the new line deliminator
	Mod1 = anItem.replace('\n', '')
	# Remove the spacing
	Mod2 = Mod1.replace(' ', '')
	# Add to overall string
	CodedMessageString = CodedMessageString+Mod2

# Parse this into integer pairs using itertools

MessageNString = [''.join(e) for e in list(izip_longest(*[iter(CodedMessageString)] * 2,fillvalue=''))]

######################### Decode The Message ##########################
DecodedMessage = []

i = 0
while i < len(MessageNString):
	# Call the decode method
	Letter = Decode_Ei(MessageNString[i], KeyNumbers[i], LN)
	if Letter == 999:
		print MessageNString[i], KeyNumbers[i]
		sys.exit()
	DecodedMessage.append(Letter)
	i = i+1

print DecodedMessage




