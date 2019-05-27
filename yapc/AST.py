import pydot

class Node(object):
	def __init__(self, t, *args):
		self.type = t
		self.args = args
		
	def __str__(self):
		s = "type: " + str(self.type) + "\n"
		s += "".join( ["i: " + str(i) + "\n" for i in self.args])
		return s

def graph(node,filename):
	edges = descend(node)
	g = pydot.graph_from_edges(edges) 
	if filename:
		f = filename + ".png"
	else:
		f = "graph.png"
	g.write_png(f, prog='dot') 
	

def descend(node):	
	edges = []
	if node.__class__ != Node:
		return []
	
	for i in node.args:
		edges.append((s(node),s(i)))
		edges += descend(i)
	return edges

def s(node):
	if node.__class__ != Node:
		return "%s (%s)" % (node,id(node))
	return "%s (%s)" % (node.type,id(node))
