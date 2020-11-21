import numpy as np


class Swarm:

    def __init__(self, height, width, number, clock_speed,
                 clock_nudge, nudge_on, influence_radius, speed, leds_number=0,
                 leds_clock_speed=None, led_influence_radius=None, sync_leds=True, fps=30):
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
        self.shinning_time = 0.1

        self.leds_number = leds_number
        self.leds_clock_speed = leds_clock_speed if leds_clock_speed is not None else clock_speed
        self.leds_influence_radius = led_influence_radius if led_influence_radius else influence_radius
        self.leds_X_positions = np.random.randint(low=0, high=width, size=leds_number)
        self.leds_Y_positions = np.random.randint(low=0, high=height, size=leds_number)
        self.sync_leds = sync_leds
        if sync_leds:
            self.leds_clocks = np.full(leds_number, np.random.random())  #np.random.rand(leds_number)
        else:
            self.leds_clocks = np.random.rand(leds_number)
        self.shinning = np.random.randint(0, 2, number)
        self.leds_on = np.full(leds_number, 1)

    def next_step(self):
        self.update_position()
        self.update_direction()
        self.update_clocks()
        self.update_leds()

    def update_position(self):
        self.X_positions = (self.X_positions + self.speed * np.cos(self.angle_direction)) % self.width
        self.Y_positions = (self.Y_positions + self.speed * np.sin(self.angle_direction)) % self.height

    def update_direction(self):
        self.angle_direction = (self.angle_direction + np.random.normal(0, 2 * np.pi / 30, self.number))

    def update_clocks(self):
        if self.nudge_on:
            is_shiny = self.shinning
            not_shiny_indices = np.where(~is_shiny)[0]

            # Calculating shinning fireflies neighbors
            dX = self.X_positions[is_shiny, np.newaxis] - self.X_positions[np.newaxis, ~is_shiny]
            dY = self.Y_positions[is_shiny, np.newaxis] - self.Y_positions[np.newaxis, ~is_shiny]
            distances = dX ** 2 + dY ** 2

            is_shiny_neighbors = (distances < self.influence_radius ** 2)
            has_shiny_neighbors = is_shiny_neighbors.sum(axis=0) > 0

            not_shiney_with_shiny_neighbors = not_shiny_indices[np.where(has_shiny_neighbors)[0]]

            # Calculating shinning leds neighbors
            is_shiny_leds = (self.leds_clocks < self.fps * self.shinning_time * self.leds_clock_speed) & (
                    self.leds_on == 1)

            dX2 = self.leds_X_positions[is_shiny_leds, np.newaxis] - self.X_positions[np.newaxis, ~is_shiny]
            dY2 = self.leds_Y_positions[is_shiny_leds, np.newaxis] - self.Y_positions[np.newaxis, ~is_shiny]
            distances2 = dX2 ** 2 + dY2 ** 2
            shiny_led_neighbors = (distances2 < self.leds_influence_radius * self.leds_influence_radius)
            has_shiny_led_neighbors = shiny_led_neighbors.sum(axis=0) > 0

            not_shiney_with_shiny_led_neighbors = not_shiny_indices[np.where(has_shiny_led_neighbors)[0]]

            # Nudging
            fireflies_to_nudge = np.union1d(not_shiney_with_shiny_neighbors, not_shiney_with_shiny_led_neighbors)
            fireflies_to_nudge_up = np.intersect1d(
                fireflies_to_nudge,
                np.where(self.clocks > 0.5)[0]
            )
            self.clocks[fireflies_to_nudge_up] = (self.clocks[fireflies_to_nudge_up] + self.clock_nudge) % 1
            fireflies_to_nudge_down = np.intersect1d(
                fireflies_to_nudge,
                np.where(self.clocks < 0.5)[0]
            )
            self.clocks[fireflies_to_nudge_down] = (self.clocks[fireflies_to_nudge_down] - self.clock_nudge) % 1

        self.clocks = self.clocks + self.clock_speed
        self.shinning = self.clocks > 1
        self.clocks[self.shinning] = 0

    @property
    def shines(self):
        return self.clocks < self.shinning_time

    def update_leds(self):
        # The 0.98 factor is an empirical value to fit the natural swarm frequency
        self.leds_clocks = (self.leds_clocks + self.leds_on * self.leds_clock_speed * 0.98) % 1

    def synchronize_leds(self):
        if not self.sync_leds:
            self.leds_clocks = np.full(self.leds_number, self.leds_clocks[0])
            self.sync_leds = True

    def desynchronize_leds(self):
        if self.sync_leds:
            self.leds_clocks = np.random.random(self.leds_number)
            self.sync_leds = False


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import pandas as pd

    res = []

    swarm = Swarm(
        height=600,
        width=1000,
        number=300,
        clock_speed=0.03,
        clock_nudge=0.01,
        nudge_on=True,
        influence_radius=100,
        speed=5,
        leds_number=2,
        leds_clock_speed=None,
        led_influence_radius=None,
        fps=30
    )
    for step in range(5000):
        print(step)
        res.append(
            dict(
                step=step,
                average_shinning=swarm.shinning.mean(),
                leds=(swarm.leds_clocks < 0.1).mean()
            )
        )
        swarm.next_step()
    df = pd.DataFrame(res)
    df.to_csv("result.csv")
    df.plot("step", ["average_shinning", "leds"])
    plt.show()
