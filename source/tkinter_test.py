import numpy as np
import tkinter as tk


class FireflyCanvas(tk.Canvas):
    def __init__(self, master, fireflies, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.fireflies = fireflies
        self.draw()

    def draw(self):
        for fly in self.fireflies.T:
            p1 = fly + np.array([4, 4])
            self.create_rectangle(*fly, *p1, fill="red")


class ControlPanel(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, borderwidth=2, text="Control")

        btn1 = tk.Button(self, text="Coucou", command=lambda: print("Coucou"))
        btn2 = tk.Button(self, text="Coucou2", command=lambda: print("Coucou"))
        btn3 = tk.Button(self, text="Coucou3", command=lambda: print("Coucou"))
        btn1.pack()
        btn2.pack()
        btn3.pack()


class ControledFrame(tk.Frame):
    """A TKinter frame with a canvas in the middle and a control panel on the left."""
    def __init__(self, master=None, **kwargs):
        kwargs = {"width": 700, "height": 500, "borderwidth": 2, **kwargs}
        tk.Frame.__init__(self, master, **kwargs)
        self.control = ControlPanel(self)
        self.canvas = FireflyCanvas(self, np.random.randint(0, 500, (2, 10)),
                                    background="black", width=1000, height=600)

        self.control.grid(column=0, row=0, sticky='nesw')
        self.canvas.grid(column=1, row=0)


root = tk.Tk()
frame = ControledFrame(root, width=100, height=100)
# frame = tk.Frame(root, width=1000, height=100)
frame.pack(fill=tk.BOTH)
root.mainloop()
