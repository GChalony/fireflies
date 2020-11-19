import numpy as np


class Swarm:

    def __init__(self, height, width, number, clock_speed,
                 clock_nudge, nudge_on, influence_radius, speed, leds_number=0,
                 leds_clock_speed=None, led_influence_radius=None, fps=30):
        self.height = height
        self.width = width
        self.fps = fps

        self.number = number
        self.nudge_on = nudge_on
        self.clock_speed = clock_speed
        self.clock_nudge = clock_nudge
        self.influence_radius = influence_radius
        self.speed = speed
        self.X_positions = np.full(number, width/2)  #np.random.randint(low=0, high=width, size=number)
        self.Y_positions = np.full(number, height / 2)  #np.random.randint(low=0, high=height, size=number)
        self.angle_direction = 2 * np.pi * np.random.rand(number)
        self.clocks = np.random.random(number)
        self.shining_time = 0.1

        self.leds_number = leds_number
        self.leds_clock_speed = leds_clock_speed if leds_clock_speed else clock_speed
        self.leds_influence_radius = led_influence_radius if led_influence_radius else influence_radius
        self.leds_X_positions = np.random.randint(low=0, high=width, size=leds_number)
        self.leds_Y_positions = np.random.randint(low=0, high=height, size=leds_number)
        self.leds_clocks = np.random.rand(leds_number)
        self.leds_on = np.array([1] * leds_number)

    def next_step(self):
        self.update_position()
        self.update_direction()
        self.update_clocks()
        # self.update_leds()

    def update_position(self):
        self.X_positions = (self.X_positions + self.speed * np.cos(self.angle_direction)) % self.width
        self.Y_positions = (self.Y_positions + self.speed * np.sin(self.angle_direction)) % self.height

    def update_direction(self):
        self.angle_direction = (self.angle_direction + np.random.normal(0, 2 * np.pi / 30, self.number))

    def update_clocks(self):
        if self.nudge_on:
            is_shiny = self.shinning
            not_shiny_indices = np.where(~is_shiny)[0]

            # Calculating shining fireflies neighbors
            dX = self.X_positions[is_shiny, np.newaxis] - self.X_positions[np.newaxis, ~is_shiny]
            dY = self.Y_positions[is_shiny, np.newaxis] - self.Y_positions[np.newaxis, ~is_shiny]
            distances = dX ** 2 + dY ** 2

            is_shiny_neighbors = (distances < self.influence_radius ** 2)
            has_shiny_neighbors = is_shiny_neighbors.sum(axis=0) > 0

            not_shiney_with_shiny_neighbors = not_shiny_indices[np.where(has_shiny_neighbors)[0]]

            # Calculating shining leds neighbors
            is_shiny_leds = (self.leds_clocks < self.fps * self.shining_time * self.leds_clock_speed) & (
                    self.leds_on == 1)

            dX2 = self.leds_X_positions[is_shiny_leds, np.newaxis] - self.X_positions[np.newaxis, ~is_shiny]
            dY2 = self.leds_Y_positions[is_shiny_leds, np.newaxis] - self.Y_positions[np.newaxis, ~is_shiny]
            distances2 = dX * dX + dY * dY
            shiny_led_neighbors = (distances2 < self.leds_influence_radius * self.leds_influence_radius)
            has_shiny_led_neighbors = shiny_led_neighbors.sum(axis=0) > 0

            not_shiney_with_shiny_led_neighbors = not_shiny_indices[np.where(has_shiny_led_neighbors)[0]]

            # Nudging
            fireflies_to_nudge = np.intersect1d(
                np.union1d(not_shiney_with_shiny_neighbors, not_shiney_with_shiny_led_neighbors),
                np.where(self.clocks > 0.5)[0]
            )
            print(fireflies_to_nudge)
            self.clocks[fireflies_to_nudge] = (self.clocks[fireflies_to_nudge] + self.clock_nudge) % 1

        self.clocks = self.clocks + self.clock_speed
        self.shinning = self.clocks > 1
        self.clocks[self.shinning] = 0
        print(self.clocks)

    @property
    def shinning(self):
        return self.clocks < self.shining_time


    def update_leds(self):
        self.leds_clocks = (self.leds_clocks + self.leds_on * self.leds_clock_speed) % 1
