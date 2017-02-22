import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import Tkinter as Tk
import networkx as nx
import numpy as np
from tkMessageBox import showinfo
import tkMessageBox
import operator



class tkinterWindow:
	def __init__(self):
		self.root = Tk.Tk()
		# self.root.geometry("1500x1640")
		self.root.update()
		self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
		self.root.wm_title("Optimum Clouds Network")
		self.root.wm_protocol('WM_DELETE_WINDOW',self.root.quit())
		
		self.G = None  # nodes 
		self.startnodevalue = None
		self.endnodevalue = None 
		self.Algorithmname = None

		self.ResultchildFrame = None
		

		self.MainFrame = Tk.Frame(relief=Tk.RAISED, borderwidth=1)
		self.MainFrame.columnconfigure(0,pad=20)
		self.MainFrame.columnconfigure(1,pad=20)	
		self.MainFrame.rowconfigure(0,pad=20)
		self.MainFrame.rowconfigure(1,pad=20)
		
		self.leftframe = Tk.Frame(self.MainFrame)
		self.leftframe.grid(row=0, column=0)

		self.rightframe = Tk.Frame(self.MainFrame)
		self.rightframe.grid(row=0, column=1)

		self.resultframe = Tk.Frame(self.MainFrame)
		self.resultframe.grid(row=1, column=0)

		self.showResultframe = Tk.Frame(self.MainFrame)
		self.showResultframe.grid(row=1,column=1)

		self.MainFrame.pack()

		self.figure = plt.figure(figsize=(5,4))
		self.subplot = self.figure.add_subplot(111)
		self.subplot.axis('off')
		self.xlim=self.subplot.get_xlim()
		self.ylim=self.subplot.get_ylim()

		self.ResultFigure = plt.figure(figsize=(5,4))
		self.ResultSubplot = self.ResultFigure.add_subplot(111)
		self.ResultSubplot.axis('off')
		self.Resultxlim=self.ResultSubplot.get_xlim()
		self.Resultylim=self.ResultSubplot.get_ylim()


	# Node colour change method 
	def node_colors(self, G, path):
		colors = []
		for node in G.nodes():
			if node in path:
				colors.append('g')
			else:
				colors.append('r')
		return colors

	# Start node label method
	def startNodeEntry(self,val):
		self.startnodevalue = val
		self.checkValidation()

	# End node label method
	def endnodeEntry(self,val):
		self.endnodevalue = val
		self.checkValidation()

	# Select Option Algorithm method
	def selectAlgorithm(self,val):
		self.Algorithmname = val
		self.checkValidation()

	# Calculate butoon method
	def CalculateAlgorithm(self):
		self.ResultSubplot.clear()
		self.ResultSubplot.axis('off')
		self.ResultCanvas.draw()
		if self.Algorithmname == 'Shortest Path':
			self.draw_shortest_path(self.G,self.pos,self.startnodevalue,self.endnodevalue)
		elif self.Algorithmname == 'Critical Path':
			self.draw_critical_path(self.G,self.pos,self.startnodevalue,self.endnodevalue)
		elif self.Algorithmname == 'Maximum Flow':
			print self.Algorithmname
			self.maximum_flow_path(self.G,self.pos,self.startnodevalue,self.endnodevalue)

	# Shortest Path Algorithm method
	def draw_shortest_path(self,G,pos,start,end):
		try:
			self.ResultSubplot.clear()
			self.ResultSubplot.axis('off')
			path = nx.shortest_path(G, start, end, weight='weight')
			self.resultLength = nx.shortest_path_length(G, start, end, weight='weight')
			node_colors = self.node_colors(G, path)
			# edges_colors = self.edges_colors(G, path)
			path_edges = zip(path,path[1:])
			nx.draw_networkx(G, pos=pos, node_color=node_colors,ax=self.ResultSubplot)
			nx.draw_networkx_edges(G,pos=pos,edgelist=path_edges,edge_color='g',width=3,ax=self.ResultSubplot)
			nx.draw_networkx_edge_labels(G,pos=pos, edge_labels=self.edge_labels,ax=self.ResultSubplot,font_color='r')
			self.ResultSubplot.plot(0,0,'-g', label='Path')
			self.ResultSubplot.legend(loc='upper right')
			self.ResultCanvas.draw()
			self.resultPath = ', '.join(str(x) for x in path) 
			if self.ResultchildFrame != None:
				self.ResultchildFrame.destroy()
			self.SelectResultFrame()

		except nx.NetworkXNoPath:
			if self.ResultchildFrame != None:
				self.ResultchildFrame.destroy()
			self.ResultSubplot.clear()
			self.ResultSubplot.axis('off')
			# self.ResultSubplot.text(0.3,0.5,'No Path is Connected', ha='center', va='center', fontsize=20, fontweight='bold')
			self.ResultCanvas.draw()
			tkMessageBox.showerror("Path", "No Path is Connected")
	
	# Critical Path Algorithm method 
	def draw_critical_path(self,G,pos,start,end,weight='weight'):
		try:
			path_length = []
			paths = nx.all_simple_paths(G, start,end)
			if not list(paths):
				if self.ResultchildFrame != None:
					self.ResultchildFrame.destroy()
				self.ResultSubplot.clear()
				self.ResultSubplot.axis('off')
				self.ResultCanvas.draw()
				tkMessageBox.showerror("Path", "No Path is Connected")
			else:
				paths = nx.all_simple_paths(G, start,end)
				for path in paths:
					total_length = 0
					for i in range(len(path)-1):
						d={}
						source, target = path[i], path[i+1]
						edge = G[source][target]
						length = edge['weight']
						total_length += length
					d['path']=path
					d['total_length']=total_length
					path_length.append(d)
				data = max(path_length, key=lambda pl: pl['total_length'])
				path = data['path']
				length = data['total_length']

				node_colors = self.node_colors(G,path)
				# edges_colors = self.edges_colors(G, path)
				path_edges = zip(path,path[1:])
				nx.draw_networkx(G, pos=pos, node_color=node_colors,ax=self.ResultSubplot)
				nx.draw_networkx_edges(G,pos=pos,edgelist=path_edges,edge_color='g',width=3,ax=self.ResultSubplot)
				nx.draw_networkx_edge_labels(G,pos=pos, edge_labels=self.edge_labels,ax=self.ResultSubplot,font_color='r')
				self.ResultSubplot.plot(0,0,'-g', label='Path')
				self.ResultSubplot.legend(loc='upper right')
				self.ResultCanvas.draw()
				self.resultPath = ', '.join(str(x) for x in path) 
				self.resultLength = length
				if self.ResultchildFrame != None:
					self.ResultchildFrame.destroy()
				self.SelectResultFrame()

				
		except nx.NetworkXNoPath:
			tkMessageBox.showerror("Path", "No Path is Connected")


	def maximum_flow_path(self):
		print 'hello'



	# calculate button validation method
	def checkValidation(self):
		if None in (self.startnodevalue, self.endnodevalue, self.Algorithmname):
			self.calculatebutton.config(state=Tk.DISABLED)
		else:
			self.calculatebutton.config(state=Tk.NORMAL)
	
	# Random traffic matrix using numpy method
	def RandomMatrix(self):
		matrix = np.random.binomial(4, 0.1, (6, 6))
		return matrix

	#  Random graph gentrate using networkx method
	def RandomGraph(self):
		matrix = self.RandomMatrix()
		self.G = nx.DiGraph(matrix)
		
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
		

	# Refresh networkx graph method	
	def refreshFigure(self):
		self.subplot.clear()
		self.subplot.axis('off')
		self.ResultSubplot.clear()
		self.ResultSubplot.axis('off')
		self.ResultCanvas.draw()
		self.RandomGraph()
		self.canvas.draw()
		if self.ResultchildFrame != None:
				self.ResultchildFrame.destroy()
		

	# Left networkx random frame graph 
	def LeftFrame(self):
		nodes_label = Tk.Label(self.leftframe, text = "Network Node")
		nodes_label.place(x=10)
		nodes_label.pack(side=Tk.TOP, anchor=Tk.N)
		self.RandomGraph()
		self.canvas = FigureCanvasTkAgg(self.figure, master=self.leftframe)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

		
	# left networkx reult frame graph
	def RightFrame(self):

		Result_label = Tk.Label(self.rightframe, text = "Resulting Graphs")
		Result_label.place()
		Result_label.pack(side=Tk.TOP, anchor=Tk.N)

		
		self.ResultCanvas = FigureCanvasTkAgg(self.ResultFigure, master=self.rightframe)
		self.ResultCanvas.show()
		self.ResultCanvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


	# left frame form
	def ResultFrame(self):

		childFrame = Tk.Frame(self.resultframe)
		childFrame.columnconfigure(0)
		childFrame.columnconfigure(1)
		childFrame.columnconfigure(2)

		childFrame.rowconfigure(0,weight=1)
		childFrame.rowconfigure(1,weight=1)
		childFrame.rowconfigure(2,weight=1)
		childFrame.rowconfigure(3,pad=5)

		startnode = Tk.Label(childFrame, text="Start Node")
		startnode.grid(row=0, column=0,padx=5,pady=5)

		startvariable = Tk.StringVar(childFrame)
		startvariable.set("--Select--")
		
		entry1 = Tk.OptionMenu(childFrame,startvariable,*self.G.nodes(),command=self.startNodeEntry)
		entry1.grid(row=0, column=1,columnspan=2, padx=5,pady=5) 

		endnode = Tk.Label(childFrame, text="End Node")
		endnode.grid(row=1,column=0,padx=5, pady=5)

		endvariable = Tk.StringVar(childFrame)
		endvariable.set("--Select--")

		entry2 = Tk.OptionMenu(childFrame,endvariable,*self.G.nodes(),command=self.endnodeEntry)
		entry2.grid(row=1,column=1,columnspan=2,padx=5,pady=5)

		
		selectAlgo = Tk.Label(childFrame, text="Select Algorithm")
		selectAlgo.grid(row=2,column=0,padx=5, pady=5)

		variable = Tk.StringVar(childFrame)
		variable.set("--Select--")
		OptionAlgo = Tk.OptionMenu(childFrame,variable,"Shortest Path", "Critical Path", "Maximum Flow", command=self.selectAlgorithm)
		OptionAlgo.grid(row=2,column=1,columnspan=2,padx=5, pady=5)


		quit_button=Tk.Button(childFrame, text="Quit" , command=self.root.destroy,bg="red",fg="white")
		quit_button.grid(row=3,column=0,padx=5, pady=5)

		RefreshButton = Tk.Button(childFrame,text="Refresh",command=self.refreshFigure,bg="blue",fg="white")
		RefreshButton.grid(row=3,column=1,padx=5, pady=5)

		self.calculatebutton=Tk.Button(childFrame, text="Calculate",bg="green",fg="white",command=self.CalculateAlgorithm,state=Tk.DISABLED) 
		self.calculatebutton.grid(row=3,column=2,padx=5, pady=5)


		childFrame.pack()


	# result right frame 
	def SelectResultFrame(self):
		self.ResultchildFrame = Tk.Frame(self.showResultframe)
		self.ResultchildFrame.columnconfigure(0)
		self.ResultchildFrame.columnconfigure(1)
	
		self.ResultchildFrame.rowconfigure(0,weight=1)
		self.ResultchildFrame.rowconfigure(1,weight=1)
		self.ResultchildFrame.rowconfigure(2,weight=1)


		LabelAlgo = Tk.Label(self.ResultchildFrame, text=self.Algorithmname)
		LabelAlgo.grid(row=0, columnspan=2,padx=5,pady=5)

		pathLabel = Tk.Label(self.ResultchildFrame, text='Path')
		pathLabel.grid(row=1, column=0,padx=5,pady=5)

		pathResult = Tk.Label(self.ResultchildFrame, text=self.resultPath,bg="green",fg="white")
		pathResult.grid(row=1, column=1,padx=5,pady=5)


		lengthLabel = Tk.Label(self.ResultchildFrame, text='Length')
		lengthLabel.grid(row=2, column=0,padx=5,pady=5)

		lengthResult = Tk.Label(self.ResultchildFrame, text=self.resultLength,bg="green",fg="white")
		lengthResult.grid(row=2, column=1,padx=5,pady=5)

		self.ResultchildFrame.pack()



App = tkinterWindow()
App.LeftFrame()
App.RightFrame()
App.ResultFrame()
Tk.mainloop()





















