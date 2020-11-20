import tkinter as tk


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
        super().__init__(master, **kwargs)


class MyCheckButton(tk.Checkbutton):
    DEFAULT_PARAMS = dict(justify="left", bg="black", activebackground="black",
                          activeforeground="gray",
                          fg="gray", pady=5,
                          borderwidth=0, highlightthickness=0)

    def __init__(self, master, **kwargs):
        kwargs = {**self.DEFAULT_PARAMS, **kwargs}
        super().__init__(master, **kwargs)


class FireflyCanvas(tk.Canvas):
    def __init__(self, master, swarm, w=8, h=8, **kwargs):
        super().__init__(master, **kwargs)
        self.w = w
        self.h = h
        self.swarm = swarm

        self.draw(swarm)

    def draw(self, swarm):
        self.delete("all")
        # Flies
        for x, y, shines in zip(swarm.X_positions, swarm.Y_positions, swarm.clocks):
            # color = "yellow" if shines else "#282828"
            i = max(0, 1 - 3 * shines)
            color = "#%02x%02x%02x" % (int(200 * i) + 20, int(100 * i) + 20, int(17 * i) + 20)
            self.create_oval(x - self.w / 2, y - self.h /2, x + self.w / 2, y + self.h / 2,
                                  fill=color, outline=color)

        # LEDs
        for x, y, clock in zip(swarm.leds_X_positions, swarm.leds_Y_positions, swarm.leds_clocks):
            color = "red" if clock < 0.1 else "#202020"
            self.create_rectangle(x - self.w / 2, y - self.h / 2, x + self.w / 2, y + self.h / 2,
                                  fill=color, outline="black")




class ControlPanel(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="black")

        clock_speed = MyScale(self, from_=0, to=0.1, resolution=0.001, label="Clock speed",
                              command=controller.handler("clock_speed"), variable=controller.clock_speed)
        number_flies = MyScale(self, from_=10, to=200, resolution=10, label="Number of flies",
                               command=controller.handler("number_flies"), variable=controller.number_flies)
        nudge_on = MyCheckButton(self, text="Activate nudging",
                                 command=controller.handler("nudge_on"), variable=controller.nudge_on)
        nudge_delta = MyScale(self, from_=0, to=1, resolution=0.01, label="Nudge Delta",
                              command=controller.handler("clock_nudge"), variable=controller.clock_nudge)
        influence_radius = MyScale(self, from_=0, to=500, label="Influence radius",
                                   command=controller.handler("influence_radius"), variable=controller.influence_radius)
        flies_speed = MyScale(self, from_=0, to=10, label="Speed of flies",
                              command=controller.handler("flies_speed"), variable=controller.flies_speed)
        led_on = MyCheckButton(self, text="LED ON",
                               command=controller.handler("led_on"), variable=controller.led_on)
        led_clock_speed = MyScale(self, from_=0, to=10, label="LED clock speed",
                                  command=controller.handler("led_clock_speed"), variable=controller.led_clock_speed)

        clock_speed.pack(fill=tk.X, expand=True, padx=5)
        number_flies.pack(fill=tk.X, expand=True, padx=5)
        nudge_on.pack(fill=tk.X, expand=True, padx=5)
        nudge_delta.pack(fill=tk.X, expand=True, padx=5)
        influence_radius.pack(fill=tk.X, expand=True, padx=5)
        flies_speed.pack(fill=tk.X, expand=True, padx=5)
        led_on.pack(fill=tk.X, expand=True, padx=5)
        led_clock_speed.pack(fill=tk.X, expand=True, padx=5)


class ControledFrame(tk.Frame):
    """A TKinter frame with a canvas in the middle and a control panel on the left."""
    FPS = 30

    def __init__(self, master, controller, swarm, **kwargs):
        super().__init__(master, **kwargs)

        # TODO figure out size
        self.W = 1000
        self.H = 600

        self.control = ControlPanel(self, controller)

        # Hackish part
        self.N = 50
        self.swarm = swarm

        self.canvas = FireflyCanvas(self, self.swarm,
                                    background="black", width=1000, height=600)

        self.control.grid(column=0, row=0, sticky='nesw')
        self.canvas.grid(column=1, row=0)

    def loop(self):
        self.swarm.next_step()

        self.canvas.draw()
        self.master.after(int(1000 / self.FPS), self.loop)