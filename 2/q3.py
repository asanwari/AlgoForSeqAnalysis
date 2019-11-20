import sys

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

# This function returns the matched prefix length
def getPrefixMatchLength(suffix, pattern, mlr):
	match = 0
	for i in range(mlr,len(pattern)):
		print('in prefix, matching ',pattern[i], ' and ', suffix[i])
		if (pattern[i] == suffix[i]):
			match+=1
		else:
			break

	return match
	#return [rank for suffix, rank in sorted((pattern[i:], i) for i in range(len(pattern)))]

def binarySearch(suffixArray, text, pattern):
	# initialization of variables
	intervalStart = 1
	textLength = len(text)
	intervalEnd = textLength-1
	print(pattern)

	# first, find the intervalStart  by a binary search
	# if pattern is empty, set intervalStart to 0
	if pattern <= text[suffixArray[0]:]:
		intervalStart = 0
	#if the pattern is greater or equal to the entire text, set intervalStart to full text(last index of suffix array)
	elif pattern >= text[suffixArray[textLength-1]:]:
		intervalStart = textLength
	# else, use binary search to determine intervalStart
	else:
		#initialize start and end vars
		L = 0
		R = textLength-1
		l = r = mlr = 0
		# while R and L do not converge
		while(R-L > 1):
			M = (L+R+1)//2
			# use mlr to reduce string matching time
			l = getPrefixMatchLength(text[suffixArray[L]:], pattern, mlr)
			r = getPrefixMatchLength(text[suffixArray[R]:], pattern, mlr)
			mlr = min(l,r)
			#----------print block----------------
			print('\n\n')
			print('L is ', text[suffixArray[L]:], L)
			print('R is ', text[suffixArray[R]:], R)
			print('P is ', pattern)
			print('M is ', text[suffixArray[M]:], M)
			print('mlr is ',mlr)
			print('comparing ',pattern[mlr:],' and ', text[suffixArray[M]+mlr:])
			#----------print block----------------


			# if mlr == len(pattern) or pattern[mlr:len(pattern)] == text[suffixArray[M]+mlr:suffixArray[M]+len(pattern)]:
			# 	return M 
			# return interval somehow
			# compare M is smaller or equal modify R
			if pattern[mlr:] <= text[suffixArray[M]+mlr:]:
				print('updating R from ', R, ' to ', M-1)
				R = M-1
			# compare M is greater modify L
			else:
				print('updating L from ', L, ' to ', M+1)
				L= M+1
		#set interval start
		intervalStart = R
		print('start interval is ', intervalStart)

	# Now, find the intervalEnd  by a second binary search
	print('\n\n\t\tin second\n\n')
	# if pattern is empty, set intervalEnd to 0 
	if pattern <= text[suffixArray[0]:]:
		intervalEnd = 0
	#if the pattern is greater or equal to the entire text, set intervalEnd to full text(last index of suffix array)
	elif pattern >= text[suffixArray[textLength-1]:]:
		intervalEnd = textLength
	# else, use binary search to determine intervalStart
	else:
		#initialize start and end vars
		L = 1
		R = textLength-1
		l = r = mlr = 0

		# while R and L do not converge
		while(R-L > 1):
			M = (L+R+1)//2
			# use mlr to reduce string matching time
			l = getPrefixMatchLength(text[suffixArray[L]:], pattern,mlr)
			r = getPrefixMatchLength(text[suffixArray[R]:], pattern,mlr)
			mlr = min(l,r)

			# if mlr == len(pattern) or pattern[mlr:len(pattern)] == text[suffixArray[M]+mlr:suffixArray[M]+len(pattern)]:
			# 	return M 
			# return interval somehow
			# compare M is smaller, modify R

			#----------print block----------------
			print('\n\n')
			print('L is ', text[suffixArray[L]:], L)
			print('R is ', text[suffixArray[R]:], R)
			print('P is ', pattern)
			print('M is ', text[suffixArray[M]:], M)
			print('mlr is ',mlr)
			print('comparing ',pattern[mlr:],' and ', text[suffixArray[M]+mlr:])
			#----------print block----------------

			# if pattern[mlr:] < text[suffixArray[M]+mlr:]:
			if pattern[mlr:] < text[suffixArray[M]+mlr:]:
				print('updating R from ', R, ' to ', M-1)
				R = M-1
			# compare M is greater modify L
			else:
				print('updating L from ', L, ' to ', M+1)
				L= M+1
		#set interval start
		intervalEnd = L
		print('end interval is ', intervalEnd)

	return (intervalStart, intervalEnd)
	# then, find the upper interval limit by another binary search



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
	print('intervall=',binarySearch(suffixArray, text, pattern), sep='')
	for i in suffixArray:
		print(text[i:])

if __name__ == "__main__":
	main()