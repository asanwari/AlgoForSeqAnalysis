class Node:
	def __init__(self, label, coverage, outNodes = [], inNodes = []):
		self.label = label
		self.coverage = coverage
		self.outNodes = outNodes
		self.inNodes = inNodes
	
	# this function safely removes a node from the graph (catering for all in/out nodes)
	def removeNode(graph, node):
		# remove all first node inEdges
		for inNode in node.inNodes:
			if node.label in graph.nodes[inNode].outNodes:
				graph.nodes[inNode].outNodes.remove(node.label)
		# remove all first node outEdges
		# print(node.outNodes)
		# print(node.label)
		for outNode in node.outNodes:
			if node.label in graph.nodes[outNode].inNodes: 
				graph.nodes[outNode].inNodes.remove(node.label)
		# remvove the node
		del graph.nodes[node.label]
		
	# this function merges a new node in a graph safely
	def mergeNodeInGraph(graph, node):
		for inNode in node.inNodes:
			graph.nodes[inNode].outNodes.append(node.label)
		for outNode in node.outNodes:
			graph.nodes[outNode].inNodes.append(node.label)

		graph.nodes[node.label] = node
