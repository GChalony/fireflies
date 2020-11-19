import tkinter as tk

from source.swarm import Swarm
from source.widgets import ControledFrame

swarm = Swarm(600, 1000, 100, 0.01, 0.01, True, 30, 2)


root = tk.Tk()
frame = ControledFrame(root, swarm)
# frame = tk.Frame(root, width=1000, height=100)
frame.pack(fill=tk.BOTH, expand=True)
root.after(0, frame.loop)
root.mainloop()
