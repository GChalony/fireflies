import tkinter as tk

import numpy as np
import pandas as pd


class MyLabel(tk.Label):
    DEFAULT_PARAMS = dict(fg="white")

    def __init__(self, master, **kwargs):
        kwargs = {**self.DEFAULT_PARAMS, **kwargs}
        tk.Label.__init__(self, master, **kwargs)


class MyScale(tk.Scale):
    DEFAULT_PARAMS = dict(orient=tk.HORIZONTAL, bg="black", fg="gray",
                          troughcolor="#ffff4d",
                          showvalue=True, borderwidth=0, highlightthickness=0)

    def __init__(self, master, **kwargs):
        kwargs = {**self.DEFAULT_PARAMS, **kwargs}
        tk.Scale.__init__(self, master, **kwargs)


class MyCheckButton(tk.Checkbutton):
    DEFAULT_PARAMS = dict(justify="left", bg="black", activebackground="black",
                          activeforeground="gray",
                          fg="gray", pady=5,
                          borderwidth=0, highlightthickness=0)

    def __init__(self, master, **kwargs):
        kwargs = {**self.DEFAULT_PARAMS, **kwargs}
        tk.Checkbutton.__init__(self, master, **kwargs)


class FireflyCanvas(tk.Canvas):
    def __init__(self, master, swarm, w=10, h=10, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.w = w
        self.h = h

        self.draw(swarm)

    def draw(self, swarm):
        self.delete("all")
        for x, y, shines in zip(swarm.X_positions, swarm.Y_positions, swarm.shinning):
            color = "yellow" if shines else "gray"
            self.create_rectangle(x, y, x + self.w, y + self.h, fill=color)


class ControlPanel(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black")

        clock_speed = MyScale(self, from_=1, to=10, label="Clock speed")
        number_flies = MyScale(self, from_=10, to=200, resolution=10, label="Number of flies")
        nudge_on = MyCheckButton(self, text="Activate nudging")
        influence_radius = MyScale(self, from_=0, to=100, label="Influence radius")
        flies_speed = MyScale(self, from_=0, to=10, label="Speed of flies")
        led_on = MyCheckButton(self, text="LED ON")
        led_clock_speed = MyScale(self, from_=0, to=10, label="LED clock speed")

        clock_speed.pack(fill=tk.X, expand=True, padx=5)
        number_flies.pack(fill=tk.X, expand=True, padx=5)
        nudge_on.pack(fill=tk.X, expand=True, padx=5)
        influence_radius.pack(fill=tk.X, expand=True, padx=5)
        flies_speed.pack(fill=tk.X, expand=True, padx=5)
        led_on.pack(fill=tk.X, expand=True, padx=5)
        led_clock_speed.pack(fill=tk.X, expand=True, padx=5)


class ControledFrame(tk.Frame):
    """A TKinter frame with a canvas in the middle and a control panel on the left."""
    FPS = 30

    def __init__(self, master, swarm, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # TODO figure out size
        self.W = 1000
        self.H = 600

        self.control = ControlPanel(self)

        # Hackish part
        self.N = 50
        self.swarm = swarm

        self.canvas = FireflyCanvas(self, self.swarm,
                                    background="black", width=1000, height=600)

        self.control.grid(column=0, row=0, sticky='nesw')
        self.canvas.grid(column=1, row=0)

    def loop(self):
        # update swarm then replot
        # self.swarm.x = ((np.random.random(self.N) - .5 ) * 4 + self.swarm.x) % self.W
        # self.swarm.y = ((np.random.random(self.N) - .5) * 4 + self.swarm.y) % self.H
        # self.swarm.clock = (0.1 + self.swarm.clock) % 1
        self.swarm.next_step()

        self.canvas.draw(self.swarm)
        self.master.after(int(1000 / self.FPS), self.loop)