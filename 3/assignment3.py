# Submission by:

#Ahmed Sohail Anwari - 2571606
#Gabriele Lamarck Silveira - 2571612

import sys
import collections
from copy import deepcopy

# this function makes type array for a given string
def makeTypeArray(text):
	# if empty string, simply return an S for $
	textLength = len(text)
	if textLength == 1:
		return ['S']
	#type array has the same length as text
	# -1 just means unassigned
	typeArray = [-1] * textLength 
	#last char ($) will always be type S
	typeArray[-1] = 'S'
	# 2nd last char will always be an L since all chars are greater than $
	typeArray[-2] = 'L'

	# iterate in reverse and assign type
	for i in range(len(text)-2, -1, -1):
		if text[i] > text[i+1]:
			typeArray[i] = 'L'
		elif text[i] == text[i+1]:
			typeArray[i] = typeArray[i+1]
		else:
			typeArray[i] = 'S'
	return typeArray

# this function returns the LMS Array 
def findLMSArray(typeArray):
	LMSArray = []
	for i in range(len(typeArray)-1, 0,-1):
		if typeArray[i] =='S' and typeArray[i-1] == 'L':
			LMSArray.append(i)
	return LMSArray

# this function generates buckets for insertion
def makeBuckets(text):
	bucket = dict()
	# calculate size for each character and store in bucket
	for i in range(0,len(text)):
		if text[i] in bucket:
			bucket[text[i]]['size']  += 1
		else:
		    bucket[text[i]]  = {'size': 1}
	#sort the buckets
	bucket = collections.OrderedDict(sorted(bucket.items()))
	count = 0
	for key,value in bucket.items():
		# add head of each alphabet
		bucket[key]['head'] = count
		count += bucket[key]['size']
		#add tail for each bucket
		bucket[key]['tail'] = count-1
	return bucket

# This function inserts the LMS positions in the suffixArray
def firstMLSSort(text, buckets, LMSArray):
	suffixArray = [-1] * len(text)
	# insert all LMS position in the correct bucket's tail
	for i in LMSArray:
		suffixArray[buckets[text[i]]['tail']] = i
		# update tail
		buckets[text[i]]['tail'] -= 1

	return suffixArray

# This function takes the LMS inserted suffixArray 
# and inserts the L positions in the suffixArray
# it also removes all LMS positions for next step
def sortLPositions(suffixArray, buckets, text, typeArray):
	#declare a new suffixArray. this is done because we want to remove
	# lms positions from suffix array at the end
	# its much more convenient to just make a new array
	newSuffixArray = [-1] * len(text)
	for i in suffixArray:
		# if unassigned, do nothing
		if i == -1:
			continue

		# if i-1 type is "L" insert it in the correct bucket's head
		if typeArray[i-1] == 'L':
			newSuffixArray[buckets[text[i-1]]['head']] = i-1
			suffixArray[buckets[text[i-1]]['head']] = i-1
			# update head
			buckets[text[i-1]]['head'] += 1

	return newSuffixArray

# This function takes the L sorted suffixArray 
# and inserts the S positions in the suffixArray
def sortSPositions(suffixArray, buckets, text, typeArray):
	# $ is always on position 0 of suffix array
	suffixArray[0] = len(suffixArray)-1 
	for i in range(len(suffixArray)-1, 0, -1):
		# if it is unassigned or 0, do nothing
		if suffixArray[i] == -1 or suffixArray[i] == 0:
			continue
		toCheck = suffixArray[i]-1
		# if i-1 type is "S" insert it in the correct bucket's tail
		if typeArray[toCheck] == 'S':
			suffixArray[buckets[text[toCheck]]['tail']] = toCheck
			# update the tail
			buckets[text[toCheck]]['tail'] -= 1

	return suffixArray

# this function generates LMS substrings
def generateLMSSubstrings(LMSArray, text):
	LMSSubstrings = []
	for i in range(len(LMSArray)-1, 0,-1): 
		LMSSubstrings.append(text[LMSArray[i]:LMSArray[i-1]])
	return LMSSubstrings

# This function checks if our LMS substrings are unique
def hasUniqueLMSSubstrings(LMSSubstrings):
	if len(LMSSubstrings) > len(set(LMSSubstrings)):
		return False
	return True


def main():
	# take the console input
	args = sys.argv
	#if invalid number of params, end
	if (len(args) < 2):
		print('Invalid number of parameters.')
		return
	text = args[1]
	# appending '$' if not already done
	if text[-1] != '$':
		text+= '$'
	print(text)
	print('type array:')
	# make type array
	typeArray = makeTypeArray(text)
	print(''.join(typeArray))
	print('suffix array of sorted LMS positions:')
	# make LMS array
	LMSArray = findLMSArray(typeArray)
	print(LMSArray)
	# Check if LMS substrings are unique
	if not hasUniqueLMSSubstrings(generateLMSSubstrings(LMSArray, text)):
		print('LMS substrings not unique!')
		return 0
	# make buckets 
	buckets = makeBuckets(text)
	# first MLS Sort
	firstMLSSortArray = firstMLSSort(text, deepcopy(buckets), LMSArray)
	# L position sort
	LSortedSuffixArray = sortLPositions(firstMLSSortArray, deepcopy(buckets), text, typeArray)
	print('pos after sorting of L-positions:')
	print(LSortedSuffixArray)
	# final S position sort
	SsortedSuffixArray = sortSPositions(LSortedSuffixArray, buckets, text, typeArray)
	print('final pos:')
	print(SsortedSuffixArray)


if __name__ == "__main__":
	main()