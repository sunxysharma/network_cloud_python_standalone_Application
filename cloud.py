import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import Tkinter as Tk
import networkx as nx
from tkMessageBox import showinfo

root = Tk.Tk()
root.geometry("1500x1640")
root.wm_title("Optimum Clouds Network")
root.wm_protocol('WM_DELETE_WINDOW', root.quit())




frame= Tk.Frame()
frame.place(height=50,width=50)
frame.pack(side=Tk.LEFT, anchor=Tk.NW)

frame1= Tk.Frame()
frame1.place(height=100,width=100)
frame1.pack(side=Tk.RIGHT, anchor=Tk.NE)

# Nodes label 
nodes_label = Tk.Label(frame, text = "Network Node")
nodes_label.place(x=10)
nodes_label.pack(side=Tk.TOP, anchor=Tk.N)


f = plt.figure(figsize=(5,4))
a = f.add_subplot(111)
plt.axis('off')

# the networkx part dummy
G=nx.complete_graph(5)
pos=nx.circular_layout(G)
nx.draw_networkx(G,pos=pos,ax=a)
xlim=a.get_xlim()
ylim=a.get_ylim()


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=frame)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

'''test '''

# Nodes label 
Result_label = Tk.Label(frame1, text = "Resulting Graphs")
Result_label.place()
Result_label.pack(side=Tk.TOP, anchor=Tk.N)

g = plt.figure(figsize=(10,9))
d = g.add_subplot(111)
plt.axis('off')

# the networkx part Dummy
G=nx.complete_graph(9)
pos=nx.circular_layout(G)
nx.draw_networkx(G,pos=pos,ax=d)
xlim=d.get_xlim()
ylim=d.get_ylim()


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(g, master=frame1)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)


'''ends '''

# label 
algo_label = Tk.Label(frame, text = "Choose your algorithm")
algo_label.pack(padx=10)

#dropdown to select algorithm
variable = Tk.StringVar(frame)
variable.set("Shortest Path") # default value
w = Tk.OptionMenu(frame, variable, "Shortest Path", "Critical Path", "Maximum Flow")
w.pack()

#Calculate button
cal_button=Tk.Button(frame, text="Calculate")
cal_button.pack()

#Quit button
quit_button=Tk.Button(frame, text="Quit", command=root.quit)
quit_button.pack()

Tk.mainloop()