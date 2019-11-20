import sys

# This function takes the text as input and outputs the sufix array
def makeSuffixArray(text):
	suffixTable = []
	# make a suffix table
	for i in range(len(text)):
		suffixTable.append(text[i:])
	# sort the resulting suffix table
	# enumerate used to keep the original index value while sorting by the string
	sortedArray = sorted(enumerate(suffixTable), key=lambda suffix: suffix[1])
	# return the original indices of the sorted list, and not the string themselves
	# which is a suffix array
	return [suffix[0] for suffix in sortedArray]



# This function returns the matched prefix length or -1 if fully matched
def getPrefixMatchLength(suffix, pattern, mlr):
	match = mlr
	for i in range(mlr,len(pattern)):
		if (pattern[i] == suffix[i]):
			match+=1
		else:
			break
	#if its a complete match, return a sentinal val, here -1
	# meaning its a complete match
	if (len(pattern) == match):
		return -1
	return match

# This function returns the interval start for the pattern in the text
def binarySearchForIntervalStart(suffixArray, text, pattern):
	#initialize vars
	L = 0
	R = len(text)-1
	M = (L+R)//2
	l = r = mlr = 0
	matchFound = False
	# while R and L do not converge
	while(R-L > 0):
		# get how much characters does suffix and M and pattern match 
		currentMatch = getPrefixMatchLength(text[suffixArray[M]:], pattern, mlr)
		# since currentMatch is -1 for a full match, set mlr to pattern length, meaning a full match occured 
		mlr =  len(pattern) if currentMatch ==  -1 else currentMatch
		# check if its a complete match update R and r.
		# Since here we are setting intervalStart, we want to set R = M, so that in the next iteration
		# We look for the matches in the upward direction from the current match
		if(currentMatch < 0):
			matchFound = True
			R = M
			r = mlr
		# compare if suffix at M is smaller update R and r
		elif pattern[mlr:] < text[suffixArray[M]+mlr:]:
			R = M-1
			r = mlr
		# compare if suffix at M is greater update L and l
		else:
			L= M+1
			l = mlr
		# calculate and set new M and mlr
		M = (R+L)//2
		mlr = min(l,r)

	# the binray search never compares when L == R, so we manually do it
	if L == R:
		if pattern[mlr:] == text[suffixArray[R]+mlr:]:
			matchFound = True

	#if we find a match, we return R, else we return -1 as not found
	if matchFound:
		return R
	return -1

def binarySearchForIntervalEnd(suffixArray, text, pattern):
	#initialize vars
	L = 0
	R = len(text)-1
	M = (L+R)//2

	l = r = mlr = 0
	matchFound = False
	# while R and L do not converge
	while(R-L > 0):
		# get how much characters does suffix and M and pattern match 
		currentMatch = getPrefixMatchLength(text[suffixArray[M]:], pattern, mlr)
		# since currentMatch is -1 for a full match, set mlr to pattern length, meaning a full match occured 
		mlr =  len(pattern) if currentMatch ==  -1 else currentMatch
		# check if its a complete match modify L and l
		if(currentMatch < 0):
			matchFound = True
			L = M
			l = mlr
		# compare if suffix at M is smaller or equal modify R and r
		elif pattern[mlr:] < text[suffixArray[M]+mlr:]:
			R = M-1
			r = mlr
		# compare if suffix at M is greater modify L and l
		else:
			L= M+1
			l = mlr
		# calculate and set new M and mlr
		M = (R+L+1)//2
		mlr = min(l,r)

	# the binray search never compares when L == R, so we manually do it
	if L == R:
		if pattern[mlr:] == text[suffixArray[R]+mlr:]:
			matchFound = True
	#if we find a match, we return R, else we return -1 as not found
	if matchFound:
		return R
	return -1


def binarySearchWithMlr(suffixArray, text, pattern):
	# First, find the intervalStart  by a binary search
	intervalStart = binarySearchForIntervalStart(suffixArray, text, pattern)
	# Now, find the intervalEnd  by a second binary search
	intervalEnd = binarySearchForIntervalEnd(suffixArray, text, pattern)
	#return the intervals
	return (intervalStart, intervalEnd)


def main():
	args = sys.argv
	if (len(args) < 3):
		print('Invalid number of parameters.')
		return
	pattern = args[1]
	textFile = open(args[2], "r")
	text = textFile.readline()+'$'
	
	suffixArray = makeSuffixArray(text)
	print('pos=',suffixArray, sep='')	
	print('text=',text, sep='')
	print('pattern=',pattern, sep='')
	
	interval = binarySearchWithMlr(suffixArray, text, pattern)
	if interval[0] == -1 or interval[1] == -1:
		print('intervall = NotFound')
	else:
		print('intervall = [',interval[0],',', interval[1],']', sep='')
	
if __name__ == "__main__":
	main()