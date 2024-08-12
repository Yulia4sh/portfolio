# Task Description:
# This script generates the Koch curve fractal using an iterative method.
# It calculates and displays the length of the Koch curve after drawing it.

import turtle as t

# Variables and constants
pen_width = 2
f_len = 33
angle = 60
axiom = "F--F--F"
state = axiom
rules = {}

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
    t.tracer(1, 0)
    t.penup()
    t.setpos(start_pos)
    t.seth(start_angle)
    t.down()
    for move in state:
        if move == "F":
            t.forward(f_len)
            count += f_len
        elif move == "+":
            t.left(angle)
        elif move == "-":
            t.right(angle)
    return count

# Define rules for Koch curve
add_rules(("F", "F+F--F+F"))
state = generate_path(2)
print("Length =", draw_fractal((-150, 0), 0))
