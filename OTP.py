import random
import os
import sys
# Import our encryption methods
import Encryptions
from Encryptions import*

# Define the base numbers and letter
LN = [['A', 1], ['B', 2], ['C', 3], ['D', 4], ['E', 5], ['F', 6], ['G', 7], 
	['H', 8], ['I', 9], ['J', 10], ['K', 11], ['L', 12], ['M', 13], ['N', 14],
	['O', 15], ['P', 16], ['Q', 17], ['R', 18], ['S', 19], ['T', 20], ['U', 21],
	['V', 22], ['W', 23], ['X', 24], ['Y', 25], ['Z', 26]]

######################### MESSAGE INPUT AND PREP #############################

# Define a message
# End will be XX
# Message = 'Hello'
Message = 'XX Tear down the bridges X drain all the rivers X burn down the town hall X there are no winners XX'

# All letters will be converted to caps
MAC = Message.upper()

######################## DETERMINE CODED MESSAGE ###########################

# Convert this to numbers
StartNumbers = []

for aCharacter in MAC:
	# Skipp spaces
	if aCharacter !=' ':
		# Compare to LN to get base numbers
		for anItem in LN:
			if aCharacter==anItem[0]:
				# If it matches a character, then suppliment this with a 
				# number. This number is the character's place in the
				# alphabet
				StartNumbers.append(anItem[1])

######################## DETERMINE BASE KEY ###########################

MessageLength = len(StartNumbers)

# Write random numbers for coded message
# These random numbers are the equivalent to the key
RandomNumbers = []
for x in range(MessageLength):
	RandomNumbers.append(random.randint(1,26))

######################## CODE MESSAGE FROM KEY ###########################

BaseCodedMessage = Ei(MessageLength, RandomNumbers, StartNumbers)

# NOTE
# RandomNumbers = Key
# StartNumbers = Original message
# BaseCodedMessage = Coded message
# print RandomNumbers
# print StartNumbers
# print BaseCodedMessage
# sys.exit()

######################## EXTEND CODED MESSAGE LENGTH ###########################

# Here we increase the len of the coded message to make it more
# difficult to decipher. Furthermore, the message has to be even
# and divisible by five to match the OTP transmission format.

# Counting index
CI = 0
DIV = False
# If the number has no remainderm DIV will be true
while DIV == False:
	DIV = ((CI+MessageLength) % 5==0 & 2==0)
	# If it has just switched to true, don't add to CI
	if DIV==False:
		CI = CI+1

# CI is now our modifier on code length
# We must add additional random variables to the end
# of the coded message. The number of additional variables
# to add is equal to CI.

# Add a random number of random vars to further expand the
# coded message length. This will still enable division by 5 and 2.
CIMOD = 0
DIV = False
# If the number has no remainderm DIV will be true
while DIV == False:
	CIMOD = random.randint(2, 6)
	DIV = ((CIMOD) % 2==0)

# The CIMOD must be in segs of 5, so we multiply CIMOD by 5
CImult = CIMOD*5

AddedVars = []
for x in range(CI+CImult):
	AddedVars.append(random.randint(1,26))

# Now add the additional variables to the start and end of the message at random

ModEnd = []
ModStart = []

for anItem in AddedVars:
	# Pick a random number
	z = random.randint(1,100)
	# If th number is greater than or equal to 50, number will go to the end
	if z>=51:
		ModEnd.append(anItem)
	# If th number is less than 50, number will go to the end
	if z < 51:
		ModStart.append(anItem)

# Add these to the coded list now

for anItem in ModEnd:
	BaseCodedMessage.append(anItem)

# Reverse so the order of this list matches that of the tested one
# below. This is done to remove the possibility of a zero being present
# during the decode process. Only happens in the randomized sections.
ModStart.reverse()
for anItem in ModStart:
	BaseCodedMessage.insert(0, anItem)

# Switch it back!
ModStart.reverse()
# BaseCodedMessage is now complete.

######################## EXTEND KEY MESSAGE LENGTH ###########################
ModKeyStart = []
ModKeyEnd = []

# Random generate start key vars
i = 0
while i < len(ModEnd):
	ModKeyEnd.append(random.randint(1,26))
	i = i+1
# Random generate end key vars
i = 0
while i < len(ModStart):
	ModKeyStart.insert(0, random.randint(1,26))
	i = i+1

# Fix zeros based on Ei
ModKeyEnd, ModKeyStart = FixZeroEi(ModKeyStart, ModKeyEnd, ModStart, ModEnd, LN)

# Start and end vars generated
# Add them to the key list

for anItem in ModKeyEnd:
	RandomNumbers.append(anItem)

# Reverse this list to ensure it is appended in a specific order.
# With the check on zeros above, the order of these values must
# match with the check.
ModKeyStart.reverse()
for anItem in ModKeyStart:
	RandomNumbers.insert(0, anItem)

# Write a text key

TextKey = []
String = ''
for anItem in RandomNumbers:
	for aLetter in LN:
		if anItem==aLetter[1]:
			String = String+aLetter[0]

# Parse the string every 5 characters
n = 5
# Define the key
CompletedKey = [String[i:i+n] for i in range(0, len(String), n)]

###################### ADD LEADING ZEROS AND PARSE DATA ######################

# Add the leading zeros and write single string
String = ''
for aVal in BaseCodedMessage:
	String = String+'%02d' % aVal

# Parse the string every 5 characters
n = 5
# [line[i:i+n] for i in range(0, len(line), n)]
CompletedEncryption = [String[i:i+n] for i in range(0, len(String), n)]

with open("MyFile.txt","w") as Doc:
	Doc.write('_________________MESSAGE KEY_________________\n')
	i = 0
	for anItem in CompletedKey:
		P = True
		if i == 4:
			Doc.write('\n')
			Doc.write(anItem)
			Doc.write('     ')
			i = 1
			P = False
		if i < 4:
			if P == True:
				Doc.write(anItem)
				Doc.write('     ')
				i = i+1
	Doc.write('\n')
	Doc.write('________________CODED MESSAGE________________\n')
	i = 0
	for anItem in CompletedEncryption:
		P = True
		if i == 4:
			Doc.write('\n')
			Doc.write(anItem)
			Doc.write('     ')
			i = 1
			P = False
		if i < 4:
			if P == True:
				Doc.write(anItem)
				Doc.write('     ')
				i = i+1
Doc.close()