from node import Node
from graph import Graph
from queue import Queue
from collections import deque
from copy import deepcopy
import heapq

# this function makes the graph
# reads: the set of reads for graph construction
# k: ksize
# includeReverse: if true, include reverse complement in the graph
def makeGraph(reads, k, includeReverse = True):
	nodes = dict()
	for read in reads:
		if includeReverse:
			reversedRead = getReverseComplement(read)
		for i in range(0,len(read)-k):
			firstNode = read[i:i+k]
			nextNode = read[i+1:i+1+k]
			addNodesToGraph(firstNode, nextNode, nodes,i)
			if includeReverse:
				firstNode = reversedRead[i:i+k]
				nextNode = reversedRead[i+1:i+1+k]
				addNodesToGraph(firstNode, nextNode, nodes,i)
	return Graph(nodes)

# returns reverse complement of the string
def getReverseComplement(str):
	rc = ''
	for i in range(len(str)-1, -1, -1):
		if str[i] == 'A':
			rc += 'T'
		elif str[i] == 'T':
			rc += 'A'
		elif str[i] == 'C':
			rc += 'G'
		else:
			rc += 'C'
	return rc


# def printNode(node):
# 	print('Node: ', node.label)
# 	print('\toutDegree: ', len(node.outNodes))
# 	print('\tinDegree: ', len(node.inNodes))
# 	print('\tCoverage: ', node.coverage)
# 	print('\tinNodes:')
# 	for inNode in node.inNodes:
# 		print('\t\t', inNode)
# 	print('\toutNodes:')
# 	for outNode in node.outNodes:
# 		print('\t\t', outNode)

# def traverseGraph(graph):
# 	print('------------------------------GRAPH TRAVERSAL------------------------')
# 	for label,node in graph.nodes.items():
# 		printNode(node)
# 	print('------------------------------GRAPH TRAVERSAL END------------------------')

# this function colapses linear stretches in a de bruijn graph
def colapseLinearStretches(graph, kSize):
	# multi is a dict which stores all non collapsable nodes
	multi = dict()
	for label, node in graph.nodes.items():
		# if its a non collapsable node, add to multi
		if len(node.inNodes) == 0 or len(node.inNodes) >1 or len(node.outNodes) > 1:
			multi[label] = node
	# for each node in multi, colapse its outNodes, if possible 
	for label, node in multi.items():
		queue = deque()
		if len(node.outNodes) == 1:
			queue.append(node)
		outNodes = deepcopy(node.outNodes)
		for outNode in outNodes:
			DFSForNodeColapse(graph,graph.nodes[outNode], queue, multi, kSize)
			if len(queue) != 0 and queue[0].label == node.label and len(queue) > 1:
				createColapsedNode(queue,graph,kSize)
			queue = deque()
	return graph

# this function helps in node collapse.
def DFSForNodeColapse(graph,node,queue,multi, kSize):
	if len(node.inNodes) == 1:
		queue.append(node)
	if node.label not in multi.keys():
		outNodes = deepcopy(node.outNodes)
		for outNode in outNodes:
			DFSForNodeColapse(graph,graph.nodes[outNode],queue,multi,kSize)
		if len(queue) > 1 and queue[0].label == node.label:
			createColapsedNode(queue,graph,kSize)
			queue = deque()

# this function collapses all nodes in queue into a single node
# and handles all outgoing/incoming edges
def createColapsedNode(queue, graph, kSize):
	firstNode = queue[0]
	newNodeInNodes = []
	newNodeOutNodes = []
	contig = queue[0].label
	coverage = queue[0].coverage
	numberOfNodes = len(queue)

	#add all first node's in node into new node's in nodes
	newNodeInNodes += queue[0].inNodes
	#add all last node's out nodes into new node's out nodes
	newNodeOutNodes += queue[len(queue)-1].outNodes

	# iterate over all nodes except the first one
	for i in range(1,len(queue)):
		# updated coverage of newNode
		coverage += queue[i].coverage
		# update label of newNode 
		contig = contig + queue[i].label[kSize-1:len(queue[i].label)]
		Node.removeNode(graph, queue[i])
	# create new node with coverage equals average of all collapsed nodes,
	# outNodes and inNodes of all collapsed nodes
	newNode = Node(contig, coverage/numberOfNodes, newNodeOutNodes, newNodeInNodes)
	# remove first Node as well
	Node.removeNode(graph, queue[0])
	# finally, merge this node in graph
	Node.mergeNodeInGraph(graph, newNode)

# this is the solution for part a
def getKmer(graph, kmer):
	print('---------- Part a ---------- ')
	print('checking for kmer ', kmer)
	if kmer not in graph.nodes.keys():
		print('kmer ', kmer, ' does not exist.')
		return 0
	node = graph.nodes[kmer]
	print('Incoming k-mers - ', ','.join(node.inNodes))
	print('Outgoing k-mers - ', ','.join(node.outNodes))

# this function adds the nodes read from the reads into the graph
def addNodesToGraph(firstNode, nextNode, nodes, i):
	#first, make the two nodes (if they dont exist)
	#check if firstNode is new
	if firstNode not in nodes:
		nodes[firstNode] = Node(firstNode,1,[],[])
	#if not, increase its out degree
	elif i == 0:
		nodes[firstNode].coverage += 1

	#check if nextNode is new
	if nextNode not in nodes:
		nodes[nextNode] = Node(nextNode,1,[],[])
	#if not, increase its coverage
	else:
		nodes[nextNode].coverage += 1
	# next, set an edge between the two nodes
	if nextNode not in nodes[firstNode].outNodes:
		nodes[firstNode].outNodes.append(nextNode)
	if firstNode not in nodes[nextNode].inNodes:
		nodes[nextNode].inNodes.append(firstNode)

# this function removes error
def removeErrors(graph, kSize):
	# first, get all tips and bubbles
	tips = getAllTips(graph,kSize)
	bubbles = getAllBubbles(graph)
	# repeat until tips and bubbles don't exist
	while not (len(tips) == 0 and len(bubbles) == 0):
		# =======================tips removal=======================
		#for each tip(ordered by lowest coverage first), remove it from the graph
		# and then collapse it again
		while tips:
			tip = heapq.heappop(tips)[1]
			if tip in graph.nodes:
				removeTip(graph, tip)
				colapseLinearStretches(graph, kSize)
		# for each bubble, remove it from the graph and collapse it again


		# =======================bubble removal=======================
		for bubble in bubbles:
			if bubble in graph.nodes:
				removeBubble(graph, bubble)
				colapseLinearStretches(graph, kSize)


		# =======================cutoff nodes removal=======================
		# remove all nodes whose coverage is less than 10% of the average coverage of the graphs
		# get cutoffNodes
		cutoffNodes = getCutoffNodes(graph, getCutoff(graph))
		#remove cutoff Nodes
		for cutoffNode in cutoffNodes:
			removeCutoffNode(graph, cutoffNode)
		
		# finally do a nodeCollapse
		colapseLinearStretches(graph, kSize)
		# get all remaining tips and bubbles
		tips = getAllTips(graph,kSize)
		bubbles = getAllBubbles(graph)
	return graph

# returns tips if they exist
def getAllTips(graph, kSize):
	tipLength = 2*kSize
	tips = []
	# a node is a tip if:
	# it has either in or out degree of 0
	# its length is < 2k
	for label, node in graph.nodes.items():
		if len(node.outNodes) <= 1  and len(node.inNodes) <= 1 and ((len(node.inNodes) == 0 or len(node.outNodes) == 0) and len(label) < tipLength):
			heapq.heappush(tips, (node.coverage, label))
	return tips

#removes tip Node from the graph
def removeTip(graph, tip):
	Node.removeNode(graph, graph.nodes[tip])

# returns bubbles if they exist
def getAllBubbles(graph):
	bubbles = []
	# a bubble is :
	# a node with 2 children
	# both of its children having just 1 outNode
	# both outNodes of the children pointing at the same node 
	for label, node in graph.nodes.items():
		# this means its a possible bubble start
		if len(node.outNodes) == 2:
			# check if all children have 1 outgoing edges
			if len(graph.nodes[node.outNodes[0]].outNodes) == 1 and len(graph.nodes[node.outNodes[1]].outNodes) == 1:
				# check if both outgoing point to the same node
				if graph.nodes[node.outNodes[0]].outNodes[0] == graph.nodes[node.outNodes[1]].outNodes[0]:
					# we have found a bubble
					# compare coverage and remove lower one
					if graph.nodes[node.outNodes[0]].coverage <= graph.nodes[node.outNodes[1]].coverage:
						bubbles.append(graph.nodes[node.outNodes[0]].label)
					else:
						bubbles.append(graph.nodes[node.outNodes[1]].label)
	return bubbles

#removes bubble from the graph
def removeBubble(graph, bubble):
	Node.removeNode(graph, graph.nodes[bubble])

#removes cutoffNodes from the graph
def removeCutoffNode(graph, cutoffNode):
	Node.removeNode(graph, graph.nodes[cutoffNode])

#get the cutoff from the graph (10% of the average coverage)
def getCutoff(graph):
	totalCoverage = 0
	for label, node in graph.nodes.items():
		totalCoverage += node.coverage
	# average the coverage of all nodes in graph
	avgCoverage = totalCoverage/len(graph.nodes)
	# setting our cutoff as the 10% of the average coverage
	return avgCoverage/10 
# geta all Nodes having coverage lower than cutoff
def getCutoffNodes(graph, cutoff):
	cutoffNodes = []
	for label, node in graph.nodes.items():
		if node.coverage < cutoff:
			cutoffNodes.append(node)
	return cutoffNodes

# this function writes output to the file
def writeToOutput(graph,outputFile):
	f = open(outputFile, 'w')
	i = 1
	for label, node in graph.nodes.items():
		f.write('>'+ str(i)+ '\n')
		f.write(node.label+ '\n')
		i+=1
	print('\n\noutput written to file ',outputFile)
	f.close()

# this function reads the reads from the file
def readFile(fileName):
	f = open(fileName, 'r')
	inputLines = f.readlines()
	f.close()
	reads = []

	for line in inputLines:
		if line[0] != '>':
			reads = reads + [line.rstrip()]
	return reads
