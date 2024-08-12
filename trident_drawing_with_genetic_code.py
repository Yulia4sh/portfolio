"""
Title: Drawing a Trident with Genetic Code Using Turtle Graphics

Description:
This script uses a genetic code approach to control turtle graphics for drawing a trident on a blue-yellow background. The genetic code consists of sequences of nucleotides (A, C, G, T) which are mapped to turtle operations. The script translates this genetic code into turtle commands to draw the trident.

The genetic code is divided into codons (three-nucleotide sequences), and each codon corresponds to a specific turtle operation or setting. The script executes these operations to render the trident on the turtle graphics canvas.

Functions:
1. draw_escutcheon(s): Draws a trident using turtle graphics based on the provided genetic code.

Requirements:
- Python 3.x
- turtle module

Usage:
- Define the genetic code string and call the draw_escutcheon function to draw the trident.
"""

import turtle as t

# Dictionary mapping codons to turtle operations
dict = {
    'AAA': ['hideturtle'],
    'AAC': ['tracer'],
    'AAG': ['pensize'],
    'AAT': ['bgcolor'],
    'ACA': ['penup'],
    'ACC': ['pendown'],
    'ACG': ['goto'],
    'ACT': ['color', 'yellow'],
    'AGA': ['color', 'blue'],
    'AGC': ['fillcolor'],
    'AGG': ['begin_fill'],
    'AGT': ['end_fill'],
    'ATA': ['setheading'],
    'ATC': ['mainloop'],
    'ATG': ['forward', 1000],
    'ATT': ['forward', 35],
    'CAA': ['forward', 20],
    'CAC': ['forward', 23],
    'CAG': ['forward', 49],
    'CAT': ['forward', 12],
    'CCA': ['forward', 25],
    'CCC': ['right', 90],
    'CCG': ['right', 225],
    'CCT': ['right', 191],
    'CGA': ['left', 90],
    'CGC': ['left', 80],
    'CGG': ['left', 180],
    'CGT': ['left', 76],
    'CTA': ['left', 89],
    'CTC': ['left', 93],
    'CTG': ['left', 35],
    'CTT': ['left', 4],
    'GAA': ['left', 185],
    'GAC': ['left', 110],
    'GAG': ['left', 105],
    'GAT': ['setpos', 0, 0],
    'GCA': ['setpos', -14.64, 0.36],
    'GCC': ['setpos', 16.22, -14.37],
    'GCG': ['setpos', 8.9, -33.74],
    'GCT': ['setpos', 5.36, 0.36],
    'GGA': ['setpos', -14.64, -10.36],
    'GGC': ['circle', 50, 45],
    'GGG': ['circle', 200, 12],
    'GGT': ['circle', 200, 12.3],
    'GTA': ['circle', 8, 140],
    'GTC': ['circle', 40, 30],
    'GTG': ['circle', 25, 90]
}

def draw_escutcheon(s):
    """
    Draws a trident using turtle graphics based on the provided genetic code.

    Args:
    - s (str): The genetic code sequence that dictates the turtle operations.
    """
    cut_1 = 0
    cut_2 = 3
    for _ in range(len(s)//3):
        local_s = s[cut_1:cut_2]
        if local_s in dict:
            operation = dict[local_s]
            if operation[0] == 'hideturtle':
                t.hideturtle()
            elif operation[0] == 'tracer':
                t.tracer(0)  # Disable animation to speed up drawing
            elif operation[0] == 'pensize':
                t.pensize(3)  # Set pen size
            elif operation[0] == 'bgcolor':
                t.bgcolor('blue')  # Set background color
            elif operation[0] == 'penup':
                t.penup()  # Lift the pen
            elif operation[0] == 'pendown':
                t.pendown()  # Lower the pen
            elif operation[0] == 'goto':
                t.goto(-500, 0)  # Move to position
            elif operation[0] == 'color':
                t.color(operation[1])  # Set pen color
            elif operation[0] == 'fillcolor':
                t.fillcolor('yellow')  # Set fill color
            elif operation[0] == 'begin_fill':
                t.begin_fill()  # Begin filling the shape
            elif operation[0] == 'forward':
                t.forward(operation[1])  # Move forward
            elif operation[0] == 'right':
                t.right(operation[1])  # Turn right
            elif operation[0] == 'left':
                t.left(operation[1])  # Turn left
            elif operation[0] == 'end_fill':
                t.end_fill()  # End filling the shape
            elif operation[0] == 'setheading':
                t.setheading(0)  # Set the heading
            elif operation[0] == 'mainloop':
                t.mainloop()  # Enter the main event loop
            elif operation[0] == 'setpos':
                t.setpos(operation[1], operation[2])  # Set the position
            elif operation[0] == 'circle':
                t.circle(operation[1], operation[2])  # Draw a circle
        cut_1 += 3
        cut_2 += 3

# Genetic code for drawing the trident
escutcheon = 'AAAAACAAGAATACAACGACCACTAGCAGGATGCCCATGCCCATGCCCATGCCCAGTACAGATACCCGAGGCCCGATTCGAACACAACGCACCGGGCGGGGTCGTACACAAACCCGAATTCCGGGCACAGCAACCAGACACCTACAGCTCCACCTAACAGATCTGACCGTACTTACACATACCCTTGTAACAGCCACCCGAGTCGAAGTCGACACAGCGCCTACCGTGACAGCTGAGACCGTGCGAACAGGAACCATACATACACCAACCCATACAATC'

# Draw the trident
draw_escutcheon(escutcheon)
