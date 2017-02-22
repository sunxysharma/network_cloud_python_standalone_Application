''' code that creates a random traffic matrix withh capacity on each link'''


# Random traffic matrix using numpy
def RandomMatrix(self):
	matrix = np.random.binomial(4, 0.1, (5, 5))
	return matrix

#  Random graph gentrate using networkx
def RandomGraph(self):
	matrix = self.RandomMatrix()
	self.G = nx.Graph(matrix)
	# capacity generation for traffic matrix 
	weights = np.random.random_integers(low=10, high=30, size=len(self.G.edges()))
	
	for i, (n1, n2) in enumerate(self.G.edges()):
		self.G[n1][n2]['weight'] = weights[i]

	# genrate circular network using networkx
	self.pos=nx.circular_layout(self.G)
	
	# assign edges capacity label in networkx graph
	self.edge_labels = {(n1,n2): self.G[n1][n2]['weight'] for (n1,n2) in self.G.edges()}
	
	# Draw networkx graph on matplotlib 
	nx.draw_networkx(self.G,pos=self.pos,ax=self.subplot)

	# assign label in networkx graph
	nx.draw_networkx_edge_labels(self.G,self.pos,ax=self.subplot,edge_labels=self.edge_labels,font_color='r')
		
