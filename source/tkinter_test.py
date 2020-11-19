import numpy as np
import pandas as pd
import tkinter as tk


class FireflyCanvas(tk.Canvas):
    def __init__(self, master, swarm, w=4, h=4, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.w = w
        self.h = h

        self.draw(swarm)

    def draw(self, swarm):
        self.delete("all")
        for _, fly in swarm.iterrows():
            color = "yellow" if fly.shines else "red"
            self.create_rectangle(fly.x, fly.y, fly.x + self.w, fly.y + self.h, fill=color)


class ControlPanel(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, borderwidth=2, text="Control")

        clock_speed = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL, label="Clock speed")
        number_flies = tk.Scale(self, from_=10, to=200, resolution=10,
                                orient=tk.HORIZONTAL, label="Number of flies")
        nudge_on = tk.Checkbutton(self, justify="left", text="Activate nudging")
        influence_radius = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, label="Influence radius")
        flies_speed = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, label="Speed of flies")
        led_on = tk.Checkbutton(self, justify="left", text="LED ON")
        led_clock_speed = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, label="LED clock speed")

        clock_speed.pack()
        number_flies.pack()
        nudge_on.pack()
        influence_radius.pack()
        flies_speed.pack()
        led_on.pack()
        led_clock_speed.pack()


class ControledFrame(tk.Frame):
    """A TKinter frame with a canvas in the middle and a control panel on the left."""
    FPS = 30

    def __init__(self, master=None, **kwargs):
        kwargs = {"width": 1000, "height": 600, "borderwidth": 2, **kwargs}
        tk.Frame.__init__(self, master, **kwargs)

        self.W = kwargs["width"]
        self.H = kwargs["height"]

        self.control = ControlPanel(self)

        # Hackish part
        self.N = 100
        self.swarm = pd.DataFrame({"x": 700 * np.random.random(self.N),
                              "y": 400 * np.random.random(self.N),
                              "shines": np.random.random(self.N) > 0.9})

        self.canvas = FireflyCanvas(self, self.swarm,
                                    background="black", width=1000, height=600)

        self.control.grid(column=0, row=0, sticky='nesw')
        self.canvas.grid(column=1, row=0)

    def loop(self):
        # update swarm then replot
        self.swarm.x = ((np.random.random(self.N) - .5 )* 4 + self.swarm.x) % self.W
        self.swarm.y = ((np.random.random(self.N) - .5) * 4 + self.swarm.y) % self.H

        self.canvas.draw(self.swarm)
        self.master.after(int(1000 / self.FPS), self.loop)



root = tk.Tk()
frame = ControledFrame(root)
# frame = tk.Frame(root, width=1000, height=100)
frame.pack(fill=tk.BOTH)
root.after(0, frame.loop)
root.mainloop()
