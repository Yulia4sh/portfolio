# Task Description:
# This script generates the Sierpinski triangle fractal using an iterative method.
# It calculates and displays the length of the Sierpinski triangle's perimeter and its area.

import turtle as t

# Variables and constants
f_len = 25
angle = 120
axiom = "F+G+G"
state = axiom
rules = {}
n_iter = 2

# Function to add rules for L-System
def add_rules(*rul):
    for key, value in rul:
        rules[key] = value

# Function to generate the path of the fractal
def generate_path(n_iter):
    local_state = state
    for n in range(n_iter):
        for key, value in rules.items():
            local_state = local_state.replace(key, value)
    return local_state

# Function to draw the fractal and calculate its length
def draw_fractal(start_pos, start_angle):
    count = 0
    t.penup()
    t.setpos(start_pos)
    t.seth(start_angle)
    t.down()
    for move in state:
        if move == "F" or move == "G":
            t.forward(f_len)
            count += f_len
        elif move == "+":
            t.left(angle)
        elif move == "-":
            t.right(angle)
    return count

# Function to calculate the area of the Sierpinski triangle
def area(ln):
    return (ln**2) * (3**0.5) / 4

# Define rules for Sierpinski triangle
add_rules(("G", "GG"))
add_rules(("F", "F+G-F-G+F"))
state = generate_path(n_iter)
print("Length =", draw_fractal((-150, 0), 0))
print("Area =", area(f_len * (2**n_iter)))
