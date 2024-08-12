# Task Description:
# This script generates the Sierpinski triangle fractal using a stochastic method.
# Instead of classical randomness, it uses a quantum computer to select the vertices
# of the triangle. The points are drawn iteratively based on the quantum-generated choices.

import turtle as t
import random as r
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Set up the turtle graphics
t.tracer(10000)  # Adjust the tracer for faster drawing
t.penup()

# Define the vertices of the triangle
A = (-60, -50)
B = (60, -50)
C = (0, 50)

# Draw the triangle vertices and labels
t.setpos(*A)
t.dot(5)
t.setpos(A[0], A[1] - 10)
t.write("A")

t.setpos(*B)
t.dot(5)
t.setpos(B[0], B[1] - 10)
t.write("B")

t.setpos(*C)
t.dot(5)
t.setpos(C[0], C[1] + 10)
t.write("C")

# Quantum circuit setup
simulator = AerSimulator()
circuit = QuantumCircuit(4, 4)
circuit.h([0, 1])
circuit.ccx(0, 1, 2)
circuit.cx(2, 1)
circuit.reset(2)
circuit.measure([0, 1, 2, 3], [0, 1, 2, 3])

# Function to get a quantum-generated random value
def quantum_random():
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    return list(counts.keys())[0]

# Function to determine if a point is inside the triangle using barycentric coordinates
def barycentric_coordinates(x, y, x1=-60, x2=60, x3=0, y1=-50, y2=-50, y3=50):
    lambda1 = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
    lambda2 = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
    lambda3 = 1 - lambda1 - lambda2
    return 0 <= lambda1 <= 1 and 0 <= lambda2 <= 1 and 0 <= lambda3 <= 1

# Function to generate points within the triangle based on quantum randomness
def random_dot(x, y, x1=-60, x2=60, x3=0, y1=-50, y2=-50, y3=50, n=1000):
    for _ in range(n):
        to_dot = quantum_random()
        if to_dot == "0000":
            to_x, to_y = x1, y1
        elif to_dot == "0001":
            to_x, to_y = x2, y2
        elif to_dot == "0010":
            to_x, to_y = x3, y3
        else:
            continue  # Skip if the quantum result is not in the expected format

        # Compute the midpoint
        new_x = (x + to_x) / 2
        new_y = (y + to_y) / 2
        x, y = new_x, new_y

        t.setpos(x, y)
        t.dot(2)

# Randomly select a starting point within the triangle
x = r.randint(-60, 60)
y = r.randint(-50, 50)
while not barycentric_coordinates(x, y):
    x = r.randint(-60, 60)
    y = r.randint(-50, 50)

# Generate points and draw the fractal
random_dot(x, y)
t.done()
