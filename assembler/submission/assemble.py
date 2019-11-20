import sys
import debruijn as db

def main():
	# take the console input
	args = sys.argv
	# ./assemble <Input>.fasta <Output>.fasta size k-mer
	#if invalid number of params, end
	if (len(args) < 5):
		print('Invalid number of parameters.')
		return
	inputFile = args[1]
	outputFile = args[2]
	kSize = int(args[3])
	kmer = args[4]
	reads = db.readFile(inputFile)
	graph = db.makeGraph(reads, kSize, False)
	# ---------part a --------------
	db.getKmer(graph, kmer)
	# ---------part a end --------------
	graph = db.makeGraph(reads, kSize, True)	
	collapsedGraph = db.colapseLinearStretches(graph,kSize)
	errorFreeGraph = db.removeErrors(collapsedGraph, kSize)
	db.writeToOutput(errorFreeGraph,outputFile)
	

if __name__ == "__main__":
	main()