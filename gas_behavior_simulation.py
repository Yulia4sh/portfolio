"""
This script simulates the behavior of gas particles within a container. It models the movement and collisions
of gas particles using basic principles of statistical mechanics. The script includes functionality for:
1. Generating initial positions and velocities of particles.
2. Updating positions based on particle velocities and checking for collisions.
3. Animating the Maxwell-Boltzmann distribution of particle speeds.
4. Animating the Boltzmann distribution of particle heights in the presence of gravity.
5. Calculating and plotting pressure-volume dependencies at different temperatures.
6. Calculating and plotting entropy as a function of time.
7. Visualizing the positions of particles in a 3D space.
"""

import numpy as np
from numpy import cos, sin
from random import uniform, choice, random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import wx

class ModelingGasBehavior:
    """
    Class to model the behavior of gas particles in a container.
    """

    def __init__(self, base_area: [int, float], height_vessel: [int, float], number_atoms: int, mass: [int, float],
                 temperature: [int, float], g: float):
        """
        Initialize the gas behavior model.

        Parameters:
        - base_area: Base area of the container.
        - height_vessel: Height of the container.
        - number_atoms: Number of gas particles.
        - mass: Mass of each gas particle.
        - temperature: Temperature of the gas.
        - g: Acceleration due to gravity.
        """
        self.base_area = base_area
        self.width_vessel = np.sqrt(base_area)
        self.height_vessel = height_vessel
        self.number_atoms = number_atoms
        self.mass = mass
        self.temperature = temperature
        self.g = g
        self.positions = np.random.uniform(low=[0, 0, 0], high=[self.width_vessel, self.width_vessel, height_vessel],
                                           size=(number_atoms, 3))
        self.radius = 5e-4
        k_e = 3 * self.number_atoms * 1.38e-23 * self.temperature * (1 / mass)
        v_sum = k_e ** .5
        speed = [uniform(0, v_sum) for _ in range(self.number_atoms)]
        norm = (1 / k_e) * sum([i ** 2 for i in speed])
        self.speed = np.array([i / (norm ** .5) for i in speed])
        self.speeds = []
        for i in self.speed:
            v_x = i * random() * choice([-1, 1])
            v_y = ((i**2 - v_x**2) ** .5) * random() * choice([-1, 1])
            v_z = ((i**2 - v_x**2 - v_y**2)**.5) * choice([-1, 1])
            self.speeds.append(np.array([v_x, v_y, v_z]))
        self.heights = []

    def main_func(self):
        """
        Main function to simulate the gas behavior.
        - Generate initial positions and velocities of particles.
        - Update positions and check for collisions.
        """
        # Adjusting velocities to match the expected kinetic energy
        kinetic_energy = 0.5 * self.mass * sum(self.speed**2)
        required_energy = 1.5 * self.number_atoms * 1.38e-23 * self.temperature
        scaling_factor = required_energy / kinetic_energy
        self.speed *= scaling_factor
        print('Expected kinetic energy sum:', 1.5 * self.number_atoms * 1.38e-23 * self.temperature,
              '\nResulting kinetic energy sum:', 0.5 * self.mass * sum(self.speed**2))

        # Time step calculation
        num_iter = 500
        n = len(self.positions)
        for k in range(num_iter):
            dt = (self.radius / 4) / max(self.speed)

            # Update positions and check for collisions
            for i in range(n):
                for j in range(i + 1, n):
                    distance = np.linalg.norm(self.positions[i] - self.positions[j])
                    if distance <= 2 * self.radius:
                        self.compute_coll(i, j)
                if self.positions[i][0] <= 0 or self.positions[i][0] >= self.width_vessel:
                    self.speeds[i][0] *= -1
                if self.positions[i][1] <= 0 or self.positions[i][1] >= self.width_vessel:
                    self.speeds[i][1] *= -1
                if self.positions[i][2] <= 0 or self.positions[i][2] >= self.height_vessel:
                    self.speeds[i][2] *= -1
                self.positions[i] = self.positions[i] + self.speeds[i] * dt

    def compute_coll(self, num1, num2):
        """
        Compute the result of a collision between two particles.

        Parameters:
        - num1: Index of the first particle.
        - num2: Index of the second particle.
        """
        v1, v2 = self.speeds[num1], self.speeds[num2]
        v_n1, v_n2 = np.linalg.norm(v1), np.linalg.norm(v2)
        teta = uniform(-np.pi / 2, np.pi / 2)
        phi = uniform(0, 2 * np.pi)
        v = v1 + v2
        r = ((v_n1 ** 2 + v_n2 ** 2) / 2 - np.dot(v, v) / 4) ** .5
        ux = r * cos(phi) * sin(teta) + v[0] / 2
        uy = r * sin(phi) * sin(teta) + v[1] / 2
        uz = r * cos(teta) + v[2] / 2
        new_v1 = np.array([ux, uy, uz])
        new_v2 = v - new_v1
        self.speeds[num1] = new_v1
        self.speeds[num2] = new_v2
        self.speed[num1] = np.linalg.norm(new_v1)
        self.speed[num2] = np.linalg.norm(new_v2)

    def maxwell_distribution(self):
        """
        Plot the Maxwell-Boltzmann distribution of particle speeds.
        """
        k = 1.38e-23
        v = np.linalg.norm(self.speeds, axis=1)
        plt.figure(figsize=(8, 6))
        plt.hist(v, bins=50, density=False, alpha=0.6, color='b', label=f'T = {self.temperature} K')

        v_range = np.linspace(0, np.max(v), 1000)
        f_v = 4 * np.pi * (self.mass / (2 * np.pi * k * self.temperature)) ** 1.5 * v_range ** 2 * np.exp(
            -self.mass * v_range ** 2 / (2 * k * self.temperature))
        plt.plot(v_range, f_v, 'r-', lw=2, label='Maxwell Distribution Function')

        plt.xlabel('Speed (m/s)')
        plt.ylabel('Frequency')
        plt.title('Maxwell Distribution')
        plt.legend()
        plt.grid(True)
        plt.show()

    def animate_distribution(self):
        """
        Animate the Maxwell-Boltzmann distribution of particle speeds over time.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        k = 1.38e-23
        mass = self.mass
        temperature = self.temperature

        def update_hist(num):
            dt = (self.radius / 4) / max(self.speed)
            n = len(self.positions)
            for i in range(n):
                for j in range(i + 1, n):
                    distance = np.linalg.norm(self.positions[i] - self.positions[j])
                    if distance <= 2 * self.radius:
                        self.compute_coll(i, j)
                if self.positions[i][0] <= 0 or self.positions[i][0] >= self.width_vessel:
                    self.speeds[i][0] *= -1
                if self.positions[i][1] <= 0 or self.positions[i][1] >= self.width_vessel:
                    self.speeds[i][1] *= -1
                if self.positions[i][2] <= 0 or self.positions[i][2] >= self.height_vessel:
                    self.speeds[i][2] *= -1
                self.positions[i] = self.positions[i] + self.speeds[i] * dt
            ax.clear()
            ax.hist(self.speed, bins=40, density=False, alpha=0.6, color='b', label=f'T = {temperature} K')

            v_range = np.linspace(0, np.max(self.speed), 1000)
            f_v = 4 * np.pi * (mass / (2 * np.pi * k * temperature)) ** 1.5 * v_range ** 2 * np.exp(
                -mass * v_range ** 2 / (2 * k * temperature))
            ax.plot(v_range, f_v, 'r-', lw=2, label='Maxwell Distribution Function')

            ax.set_xlabel('Speed (m/s)')
            ax.set_ylabel('Frequency')
            ax.set_title('Maxwell Distribution')
            ax.legend()
            ax.grid(True)

        ani = FuncAnimation(fig, update_hist, frames=200, interval=100)
        plt.show()

# Initialize GUI application
app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, "Gas Behavior Simulation")
frame.Show()
app.MainLoop()
