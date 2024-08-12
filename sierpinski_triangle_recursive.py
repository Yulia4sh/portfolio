# Task Description:
# This script generates the Sierpinski triangle fractal using a recursive method.
# It calculates and displays the length of the Sierpinski triangle's perimeter,
# and the area of the Sierpinski triangle.

import turtle as t

count = []  # List to count recursive function calls
len_f = []  # List to store segment lengths
trg = 2     # Number of iterations

# Function to draw Sierpinski triangle recursively
def sierpinski_triangle(ln, trg):
    count.append(1)  # Increment function call count
    if trg == 0:
        len_f.append(ln)
        t.forward(ln)
        t.left(120)
        len_f.append(ln)
        t.forward(ln)
        t.left(120)
        len_f.append(ln)
        t.forward(ln)
        t.left(120)
    else:
        ln //= 2
        sierpinski_triangle(ln, trg - 1)
        t.forward(ln)
        sierpinski_triangle(ln, trg - 1)
        t.back(ln)
        t.left(60)
        t.forward(ln)
        t.right(60)
        sierpinski_triangle(ln, trg - 1)
        t.left(60)
        t.back(ln)
        t.right(60)

t.penup()
t.speed(0)
t.setpos(-180, 0)
t.pendown()
sierpinski_triangle(100, trg)

def area(ln):
    return (ln**2) * (3**0.5) / 4

print("Number of function calls:", len(count))
print("Length of the contour of the fractal:", sum(len_f))
print("Area =", area(len_f[0] * (2**trg)))
