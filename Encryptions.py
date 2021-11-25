import random
import os
import sys

############################### NOTE #####################################

# With the added end and beginning strings checked during the OTP module,
# no zeros are allowed within them. They are tested with the decryption
# methods given here. Must use the same methods for coding and decoding!

############################### Encryption 1 ###########################

def Ei(MessageLength, RandomNumbers, StartNumbers):
	# This will code our message based upon these properties.
	BaseCodedMessage = []
	i = 0 
	while i<MessageLength:
		# Use the modular addition function for python.
		# This is the (X+Y) % Z Where Z is the max number,
		# afterwhich the addition start back at 0.
		CodeVariable = (RandomNumbers[i]+StartNumbers[i]) % 27
		# Modular addition starts back at zero, we need it to be 1
		# If the variable exceeds 26, we need to manually add 1 to make
		# up for the error.
		if (RandomNumbers[i]+StartNumbers[i])>=27:
			# Add the additional 1
			CodeVariable = CodeVariable+1
		# Append the sum to the sum list
		BaseCodedMessage.append(CodeVariable)
		# Count the index
		i = i+1
	# Return the message
	return BaseCodedMessage

##### Decode Encryption 1
def Decode_Ei(x, y, LN):
	LetterSelect = 999
	# Where x is the coded message value and y is the key value
	# if int(x)>=y:
	if int(x)>y:
		# They can not be equal, that would be zero, if an error occurs
		# the encryption method need modification.
		z = int(x)-y
		for aLetter in LN:
			if aLetter[1]==z:
				LetterSelect = aLetter[0]
	if int(x)<y:
		z = (26-y)+int(x)
		for aLetter in LN:
			if aLetter[1]==z:
				LetterSelect = aLetter[0]		
	return LetterSelect

def FixZeroEi(ModKeyStart, ModKeyEnd, ModStart, ModEnd, LN):
	# Fix ZERO problem
	i = 0
	while i < len(ModStart):
		# Pull decode method
		Var = Decode_Ei(ModStart[i], ModKeyStart[i], LN)
		if Var == 999:
			P = False
			if ModKeyStart[i]==26:
				ModKeyStart[i] = 1
				P = True
			if P==False:
				if ModKeyStart[i]<26:
					ModKeyStart[i] = ModKeyStart[i]+1
		i = i+1

	i = 0
	while i < len(ModEnd):
		Var = Decode_Ei(ModEnd[i], ModKeyEnd[i], LN)
		if Var == 999:
			P = False
			if ModKeyEnd[i]==26:
				ModKeyEnd[i] = 1
				P = True
			if P==False:
				if ModKeyEnd[i]<26:
					ModKeyEnd[i] = ModKeyEnd[i]+1
		i = i+1
	return ModKeyEnd, ModKeyStart

############### Basic decode and code properties
# *Code Letter Value = (integer of Message letter number + the integer of the random key gen)
# if the sum reaches 27, addition returns to 1 and continues up.
# Thus, V + X = 22 + 24 = 46 = 20

# Decode Letter Value = There are two possible ways for this to happen. In order
# to decode, the Message Number (X) is subracted by the key number (Y), UNLESS!
# the message number (X) is less than the key number (Y).
# Thus:
# if x>y then Decode Value is = x-y
# if x<y then Decode Value is = (26-y)+x
