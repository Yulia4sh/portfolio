# Task Description:
# This script generates the Dragon curve fractal using a recursive method.
# It calculates and displays the length of the Dragon curve and the number of recursive function calls.

import turtle as t

count = []  # List to count recursive function calls
len_f = []  # List to store segment lengths

# Function to draw Dragon curve recursively
def dragon_curve_segment(ln, trg):
    count.append(1)  # Increment function call count
    if trg == 0:
        t.forward(ln)
        len_f.append(ln)
    else:
        dragon_curve_segment(ln, trg - 1)
        t.left(90)
        dragon_curve_segment(ln, trg - 1)

t.penup()
t.speed(0)
t.setpos(-70, 0)
t.pendown()
dragon_curve_segment(5, 10)

print("Number of function calls:", len(count))
print("Length of the contour of the fractal:", sum(len_f))
