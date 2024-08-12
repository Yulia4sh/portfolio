# Task Description:
# This script generates the Koch curve fractal using a recursive method.
# It calculates and displays the length of the Koch curve and the number of recursive function calls.

import turtle as t

count = []  # List to count recursive function calls
len_f = []  # List to store segment lengths

# Function to draw Koch curve segment recursively
def koch_segment(ln):
    count.append(1)  # Increment function call count
    if ln > 50:
        new_ln = ln // 3
        koch_segment(new_ln)
        t.left(60)
        koch_segment(new_ln)
        t.right(120)
        koch_segment(new_ln)
        t.left(60)
        koch_segment(new_ln)
    else:
        t.forward(ln)
        len_f.append(ln)
        t.left(60)
        t.forward(ln)
        len_f.append(ln)
        t.right(120)
        t.forward(ln)
        len_f.append(ln)
        t.left(60)
        t.forward(ln)
        len_f.append(ln)

t.penup()
t.speed(0)
t.setpos(-180, 0)
t.pendown()
koch_segment(100)
t.right(120)
koch_segment(100)
t.right(120)
koch_segment(100)

print("Number of function calls:", len(count))
print("Length of the contour of the fractal:", sum(len_f))
