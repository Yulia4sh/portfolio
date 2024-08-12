"""
Title: Taper Formula Visualization

Description:
This script uses the Taper formula to graphically represent both the Taper formula itself and a given name. 
It consists of the following functionalities:

1. find_k(name): Determines the constant 'k' based on a binary image. It converts a binary image (106 × 17) to a binary string, calculates its decimal equivalent, and multiplies by 17.
2. black_square(x, y): Draws a black square at the specified (x, y) coordinates using the turtle library.
3. tapper(x, y): Calculates the value of the Taper function at a given (x, y) position.
4. f(k): Uses the Taper formula to form an image based on the constant 'k' by drawing squares on the turtle canvas.

Requirements:
- Pillow (PIL) library for image processing.
- Turtle graphics library for drawing.

Usage:
- Provide binary images named "0.png" and "0(0).png" to visualize their representations using the Taper formula.
"""

from PIL import Image
import turtle

def find_k(name):
    """
    Finds the constant 'k' from a binary image.

    Args:
    - name (str): The filename of the binary image.

    Returns:
    - int: The computed constant 'k' after multiplying by 17.
    """
    # Open the image file
    image = Image.open(name)
    width, height = image.size
    result = ''

    # Process image from bottom-left to top-right
    for x in range(width-1, -1, -1):
        for y in range(height):
            pixel_color = image.getpixel((x, y))
            if pixel_color == (0, 0, 0, 255):  # Check if pixel is black
                result += '1'
            else:
                result += '0'

    # Convert binary string to decimal and multiply by 17
    return int(result, 2) * 17

def black_square(x, y):
    """
    Draws a black square at the specified coordinates using the turtle library.

    Args:
    - x (int): The x-coordinate for the square.
    - y (int): The y-coordinate for the square.
    """
    turtle.penup()
    turtle.setpos(x, y)
    turtle.pendown()
    for _ in range(4):
        turtle.forward(1)
        turtle.right(90)
    turtle.penup()

def tapper(x, y):
    """
    Computes the value of the Taper function at given coordinates.

    Args:
    - x (int): The x-coordinate.
    - y (int): The y-coordinate.

    Returns:
    - int: 1 or 0 based on the Taper formula.
    """
    result = ((y//17)//(2**(17*x+(y%17)))) % 2
    return 1 if result > 0.5 else 0

def f(k):
    """
    Draws the image based on the Taper formula and constant 'k'.

    Args:
    - k (int): The constant derived from the binary image.
    """
    turtle.tracer(2)
    x_r = -100
    y_r = 0

    for x in range(106):
        x_r += 2
        y_r = -2
        for y in range(k, k + 17):
            y_r += 2
            if tapper(x, y) == 1:
                black_square(x_r, y_r)

# Main execution
if __name__ == '__main__':
    k1 = find_k("0.png")      # Compute k from image "0.png"
    k2 = find_k("0(0).png")   # Compute k from image "0(0).png"

    print(f'Computed k for 0.png: {k1}')
    f(k1)  # Draw image for the first computed k

    turtle.reset()  # Reset turtle to clear previous drawings

    print(f'Computed k for 0(0).png: {k2}')
    f(k2)  # Draw image for the second computed k

turtle.mainloop()  # Keep the turtle graphics window open
