import tkinter as tk

from source.controller import Controller
from source.swarm import Swarm
from source.widgets import ControledFrame

root = tk.Tk()
root.title("Fireflies simulation")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# Maximize window
# root.geometry("%dx%d+0+0" % (w, h))


swarm = Swarm(
    height=600,
    width=1000,
    number=300,
    clock_speed=0.03,
    clock_nudge=0.01,
    nudge_on=False,
    influence_radius=100,
    speed=0,
    leds_number=2,
    leds_clock_speed=None,
    led_influence_radius=None,
    sync_leds=False,
    fps=30
)

controller = Controller(root, swarm)
frame = ControledFrame(root, controller, swarm)
# frame = tk.Frame(root, width=1000, height=100)
frame.pack(fill=tk.BOTH, expand=True)
root.after(0, frame.loop)
root.mainloop()
