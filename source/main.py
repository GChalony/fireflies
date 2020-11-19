import tkinter as tk

from source.controller import Controller
from source.swarm import Swarm
from source.widgets import ControledFrame

swarm = Swarm(height=600, width=1000, number=100, clock_speed=0.01,
                 clock_nudge = 0.1, nudge_on=True, influence_radius=30, speed=3, leds_number=0,
                 leds_clock_speed=None, led_influence_radius=None, fps=30)


root = tk.Tk()
root.title("Fireflies simulation")
controller = Controller(root, swarm)
frame = ControledFrame(root, controller, swarm)
# frame = tk.Frame(root, width=1000, height=100)
frame.pack(fill=tk.BOTH, expand=True)
root.after(0, frame.loop)
root.mainloop()
