# Fireflies

This project aims to simulate fireflies blinking synchronization.  
It was done during the two project days of Telecom Paris's Athens Week : Emergence of Complex Systems.

Authors: Adrien Monteiro and Gregoire Chalony.

The idea is shamelessly taken from [Nicky Case's blog](ncase.me/fireflies), and rewritten in Python. On addentum that we made was to be able to add LEDs to the simulation, to see if the fireflies would sync with the LEDs.

## Modelisation

Each firefly moves randomly, and has an internal clock, with a given period (the same for all). Every time its clocks finishes one period, it blinks.

The only interaction is that if a firefly sees a nearby firefly blinking, _and that its clock was past half period_, then it nudges its internal clock forward by a small value. This very simple phenomenon leads to synchronisation if the right parameters are used.

## The app

A small Tkinter app lets you play with the simulation and some parameters (speed of flies, influence radius, leds...). For more control, dig in the code :wink:.


## Example

![demo.gif](data/fireflies_app_demo.gif)
