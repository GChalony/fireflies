import tkinter as tk

from source.swarm import Swarm


class Controller:
    def __init__(self, master, swarm: Swarm):
        self.swarm = swarm

        self.clock_speed = tk.IntVar(master)
        self.number_flies = tk.IntVar(master)
        self.nudge_on = tk.IntVar(master)
        self.influence_radius = tk.IntVar(master)
        self.flies_speed = tk.IntVar(master)
        self.led_on = tk.IntVar(master)
        self.led_clock_speed = tk.IntVar(master)
        self.clock_nudge = tk.IntVar(master)

    def handle(self, event, *args):
        if event == "clock_speed":
            # print("Changed clock speed", self.clock_speed.get())
            self.swarm.clock_speed = self.clock_speed.get()
        elif event == "number_flies":
            # self.swarm.change_number_flies(self.number_flies.get())
            raise NotImplementedError("Can't change number flies")
        elif event == "nudge_on":
            self.swarm.nudge_on = self.nudge_on.get()
        elif event == "clock_nudge":
            self.swarm.clock_nudge = self.clock_nudge.get()
        elif event == "influence_radius":
            self.swarm.influence_radius = self.influence_radius.get()
        elif event == "flies_speed":
            self.swarm.speed = self.flies_speed.get()
        elif event == "led_on":
            self.swarm.leds_on = self.led_on.get()
        elif event == "sync_leds":
            if self.sync_leds.get():
                self.swarm.synchronize_leds()
            else:
                self.swarm.desynchronize_leds()
        elif event == "led_clock_speed":
            self.swarm.leds_clock_speed = self.led_clock_speed.get()

    def handler(self, event):
        def raise_event(*args):
            self.handle(event, *args)
        return raise_event
