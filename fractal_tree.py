"""
Task:
1. Generate and display a tree with random elements, varying branch thicknesses, and color variations using the code provided in the lecture. Implement the following functions:

a) A function that returns a list of tuples, where each tuple consists of 4 parameters: the first two parameters are the x and y coordinates of each branching point, 'root', and 'leaves' of the tree, and the 3rd and 4th parameters are the thickness and color of the elemental part of the tree (edge or 'branch') which ends at the point (x, y).

b) A function that writes to a file the list of tuples returned by the function in part a).

c) A function that loads tree data from a file and reconstructs the tree image using turtle.

d) A function that returns the width and height of the tree.

e) A function that returns the length of all branches and the 'area' of the tree ('area' of the tree is the sum of the areas of the tree's edges; the area of one edge is equal to the product of its thickness and the length of the edge).
"""

import turtle as t
import random
import pickle
import math

# Function to generate tree data
def generate_tree_data(axiom, rules, itr, angle, dl):
    state = ""
    stc = []
    result = []

    for _ in range(itr):
        for ch in axiom:
            if ch in rules:
                state += rules[ch]
            else:
                state += ch
        axiom = state
        state = " "

    t.penup()
    t.setpos(0, -150)
    t.left(90)
    t.pendown()
    t.pencolor('#462b00')
    thick = 6
    t.pensize(thick)
    t.tracer(0)

    for ch in axiom:
        if ch == "+":
            t.right(angle - random.randint(-20, 20))
        elif ch == "-":
            t.left(angle - random.randint(-20, 20))
        elif ch == "2":
            if random.randint(0, 10) > 4:
                t.penup()
                t.forward(dl)
                result.append((t.xcor(), t.ycor(), t.pensize(), t.pencolor()))
        elif ch == "1":
            if random.randint(0, 10) > 5:
                t.penup()
                t.forward(dl)
                result.append((t.xcor(), t.ycor(), t.pensize(), t.pencolor()))
        elif ch == "0":
            stc.append(t.pensize())
            t.pensize(3)
            r = random.randint(0, 11)
            if r < 3:
                t.pencolor('#00cc66')
            elif r > 6:
                t.pencolor('#66cc66')
            elif 3 < r < 6:
                t.pencolor('#298700')
            t.penup()
            t.forward(dl - 5)
            result.append((False, False, False, False))
            result.append((t.xcor(), t.ycor(), t.pensize(), t.pencolor()))
            t.pensize(stc.pop())
            t.pencolor('#462b00')
        elif ch == "[":
            thick = thick * 0.75
            t.pensize(round(thick))
            stc.append(thick)
            stc.append(t.xcor())
            stc.append(t.ycor())
            stc.append(t.heading())
            result.append((t.xcor(), t.ycor(), t.pensize(), t.pencolor()))
        elif ch == "]":
            t.penup()
            t.setheading(stc.pop())
            t.sety(stc.pop())
            t.setx(stc.pop())
            thick = stc.pop()
            t.pensize(thick)
            t.pendown()
            result.append((t.xcor(), t.ycor(), t.pensize(), t.pencolor()))

    return result

# Function to save tree data to a file
def save_tree_data(filename, data):
    with open(filename, "wb") as file:
        pickle.dump(data, file)

# Function to draw the tree from saved data
def draw_tree(filename):
    with open(filename, "rb") as file:
        now_result_here = pickle.load(file)

    t.penup()
    t.speed(0)

    for i in range(len(now_result_here)):
        try:
            if not now_result_here[i][0]:
                pass
            elif not now_result_here[i + 1][0]:
                t.penup()
                t.pensize(now_result_here[i][2])
                t.pencolor(now_result_here[i][3])
                t.setpos(now_result_here[i][0], now_result_here[i][1])
                t.pendown()
                t.goto(now_result_here[i + 2][0], now_result_here[i + 2][1])
            elif not now_result_here[i - 1][0]:
                r2 = random.randint(0, 100)
                if r2 == 11:
                    t.pencolor('#db0000')
                    t.penup()
                    t.dot(15)
                t.penup()
                t.pensize(now_result_here[i][2])
                t.pencolor(now_result_here[i][3])
                t.setpos(now_result_here[i][0], now_result_here[i][1])
                t.pendown()
                t.right(angle - random.randint(-11, 11))
                t.forward(random.randint(5, 10))
            else:
                t.penup()
                t.pensize(now_result_here[i][2])
                t.pencolor(now_result_here[i][3])
                t.setpos(now_result_here[i][0], now_result_here[i][1])
                t.pendown()
                t.goto(now_result_here[i + 1][0], now_result_here[i + 1][1])
        except IndexError:
            pass

    t.done()

# Function to calculate the width and height of the tree
def calculate_width_height(data):
    list_height = [i[1] for i in data if i[0] is not False]
    list_width = [i[0] for i in data if i[0] is not False]

    height = max(list_height) - min(list_height)
    width = max(list_width) - min(list_width)

    return width, height

# Function to calculate the length and area of all branches
def calculate_length_area(data):
    length = 0
    area = 0

    for i in range(len(data)):
        try:
            if (data[i + 1][1] < data[i][1] and data[i + 1][0] > data[i][0]) or (data[i + 1][1] < data[i][1] and data[i + 1][0] < data[i][0]):
                pass
            else:
                length_local = math.sqrt((data[i + 1][0] - data[i][0])**2 + (data[i + 1][1] - data[i][1])**2)
                area_local = length_local * data[i][2]
                length += length_local
                area += area_local
        except IndexError:
            pass

    return length, area

# Usage of functions
axiom = "0"
rules = {"1": "21", "0": "1[-0]+0"}
itr = 11
angle = 10
dl = 5
filename = "tree_data.pkl"

# Generate and save tree data
tree_data = generate_tree_data(axiom, rules, itr, angle, dl)
save_tree_data(filename, tree_data)

# Draw the tree from saved data
draw_tree(filename)

# Calculate and print tree dimensions
width, height = calculate_width_height(tree_data)
print("Width:", width)
print("Height:", height)

# Calculate and print length and area of the tree
length, area = calculate_length_area(tree_data)
print("Length:", length)
print("Area:", area)
