# Task Description:
# This script generates the Dragon curve fractal using an iterative method.
# It calculates and displays the length of the Dragon curve after drawing it.

import turtle as t

# Variables and constants
f_len = 5
angle = 90
axiom = "FX"
state = axiom

# Function to generate the path of the fractal
def generate_path(n_iter):
    local_state = state
    for n in range(n_iter):
        new_state = local_state.replace("X", "x")
        new_state = new_state.replace("Y", "y")
        local_state = new_state.replace("y", "-FX-Y").replace("x", "X+YF+")
    return local_state

# Function to draw the fractal and calculate its length
def draw_fractal(start_pos, start_angle):
    count = 0
    t.penup()
    t.speed(0)
    t.setpos(start_pos)
    t.seth(start_angle)
    t.down()
    for move in state:
        if move == "F":
            t.forward(f_len)
            count += f_len
        elif move == "+":
            t.right(angle)
        elif move == "-":
            t.left(angle)
    return count

# Generate and draw the Dragon curve fractal
state = generate_path(10)
print("Length =", draw_fractal((50, 150), 0))
