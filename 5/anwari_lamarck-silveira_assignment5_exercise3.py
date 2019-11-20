import sys

def semiglobal_alignment (s, t, maxdist ):
	m, n = len (s), len (t)
	T = [] # create empty matrix
	T.append([0] * (m +1)) # empty 0th row
	for i in range (1, n +1):
		T.append([None] * (m +1)) # add empty row i
		T[i][0] = i # init 0th column of row i
		for j in range (1,m +1):
			T[i][j] = min(T[i-1][j-1] + (0 if s[j-1]== t[i-1] else 1), T[i-1][j] + 1, T[i][j-1] + 1)
	p = [i for i in range (m) if T[n][i] <= maxdist]
	return p

def main():
	# take the console input
	args = sys.argv
	if (len(args) != 4):
		print('Invalid number of parameters.')
		return
	pattern = args[1]
	inputFile = args[2]
	maxDist = int(args[3])
	inputFile = open(inputFile, "r")
	text = inputFile.readline()
	result = semiglobal_alignment(text, pattern, maxDist)
	print(text)
	for x in result:
		print('(',x-len(pattern),',', x-1,')')
	print((len(text))*(len(pattern)+1))

if __name__ == "__main__":
	main()