def ShiftAnd (P, T):
	print('Text is :'+ T+', and pattern is :'+P)
	m = len(P)
	masks = dict () # empty dictionary
	bit = 1
	print('starting with bit = 1 and mask[....] = 0')
	for c in P:
		if c not in masks : masks [c] = 0
		masks [c] |= bit
		print('mask '+c+' :'+str(masks[c]))
		bit *= 2
		print('bit: ' + str(bit))
		
	accept_state = bit // 2
	print('accept state: '+str(accept_state))
	D = 0 # bit - mask of active states
	i = 0
	for c in T:
		D = ((D << 1) + 1) & masks [c]
		if (D & accept_state ) != 0:
			# since the ith position is the end of the matching, 
			# we subtract the length of pattern from i to get to the start
			# of the matching
			print('pattern match found from :'+str(i-(len(P)-1))+' to '+str(i))
			yield i
		i += 1


def horspool_preprocessing (sigma , P):
	shifts = dict ()
	for c in sigma :
		shifts [c] = len (P)
	for i in range (len(P) -1):
		print(i)
		shifts [P[i]] = len (P) - i - 1
	return shifts
		
		
def horspool_matching (sigma , P, T):
	shifts = horspool_preprocessing (sigma , P)
	i = len(P) - 1
	while i < len(T):
		if T[i- len(P )+1: i +1] == P:
			yield i
		i += shifts [T[i]]
		
#for f in ShiftAnd('abb', 'abbababc'):
#	f

x = ShiftAnd('abb', 'abbababc')
print(x)
#for f in horspool_matching('abc', 'abaaa', 'abaaaabaaabaaabaaa'):
#	f