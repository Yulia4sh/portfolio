#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime
import json
from tabulate import tabulate
from random import choice
from colorama import Fore, Style
import doctest
import turtle as t

# Function to load data from a file
def load_txt(name):
    with open(name, 'r') as file:
        return [eval(line) for line in file]

# Function to draw the game board
def draw_board():
    t.color('black')
    t.setheading(0)
    t.clear()
    t.penup()
    t.setpos(-30, 10)
    t.pendown()
    t.forward(60)
    t.penup()
    t.setpos(-30, -10)
    t.pendown()
    t.forward(60)
    t.right(90)
    t.penup()
    t.setpos(-10, 30)
    t.pendown()
    t.forward(60)
    t.penup()
    t.setpos(10, 30)
    t.pendown()
    t.forward(60)

# Function to draw X or O
def draw_x_or_o(x_or_o, row, column):
    if x_or_o == f'{Fore.RED}x{Style.RESET_ALL}':
        t.color('red')
        coords = [
            (-30, 30, -10, 10), (-10, 30, 10, 10), (10, 30, 30, 10),
            (-30, 10, -10, -10), (-10, 10, 10, -10), (10, 10, 30, -10),
            (-30, -10, -10, -30), (-10, -10, 10, -30), (10, -10, 30, -30)
        ]
        x1, y1, x2, y2 = coords[row * 3 + column]
        t.penup()
        t.setpos(x1, y1)
        t.pendown()
        t.goto(x2, y2)
        t.penup()
        t.setpos(x2, y1)
        t.pendown()
        t.goto(x1, y2)
    elif x_or_o == f'{Fore.BLUE}o{Style.RESET_ALL}':
        t.color('blue')
        coords = [
            (-20, 20), (0, 20), (20, 20),
            (-20, 0), (0, 0), (20, 0),
            (-20, -20), (0, -20), (20, -20)
        ]
        x, y = coords[row * 3 + column]
        t.penup()
        t.setpos(x, y - 10)
        t.pendown()
        t.circle(10)

# Function to print the board
def print_board(lst):
    return tabulate(lst, tablefmt="grid")

# Function to handle player move
def input_move(lst: list, str_x_or_o: str) -> list:
    row, column = int(input('Enter row number: ')), int(input('Enter column number: '))
    while lst[row][column] != '*':
        print('The cell is already occupied, enter another cell')
        row, column = int(input('Enter row number: ')), int(input('Enter column number: '))
    lst[row][column] = str_x_or_o
    draw_x_or_o(str_x_or_o, row, column)
    return lst

# Function to handle computer move
def make_move(lst: list, x: str) -> list:
    """
    >>> make_move([['x', '*', '*'], ['x', '*', '*'], ['*', '*', '*']], 'x')
    Genius move:
    [['x', '*', '*'], ['x', 'x', '*'], ['*', '*', '*']]
    """
    if '*' not in [j for i in lst for j in i]:
        return lst
    print('Genius move:')
    if lst[1][1] == '*':
        lst[1][1] = x
        draw_x_or_o(x, 1, 1)
        return lst
    count = 0
    check = 1
    while count < 10:
        count += 1
        row = choice(lst)
        column, row_index = choice(row), lst.index(row)
        column_index = row.index(column)
        while lst[row_index][column_index] != '*':
            row = choice(lst)
            column, row_index = choice(row), lst.index(row)
            column_index = row.index(column)
        lst[row_index][column_index] = x
        if check_board(lst) == 2:
            check *= 0
            break
        else:
            lst[row_index][column_index] = '*'
    if check == 1:
        row = choice(lst)
        column, row_index = choice(row), lst.index(row)
        column_index = row.index(column)
        while lst[row_index][column_index] != '*':
            row = choice(lst)
            column, row_index = choice(row), lst.index(row)
            column_index = row.index(column)
        lst[row_index][column_index] = x
    draw_x_or_o(x, row_index, column_index)
    return lst

# Function to check the board for a win or draw
def check_board(lst: list, o: str = f'{Fore.BLUE}o{Style.RESET_ALL}', x: str = f'{Fore.RED}x{Style.RESET_ALL}') -> int:
    """
    >>> check_board([['x', '*', '*'], ['x', 'x', '*'], ['x', '*', '*']], 'o', 'x')
    2
    >>> check_board([['o', 'o', 'x'], ['x', 'x', 'o'], ['o', 'x', 'o']], 'o', 'x')
    3
    """
    t.color('blue')
    if [o] * 3 in lst or [o] * 3 in [list(row) for row in zip(*lst)]:
        winning_lines = {
            0: (-30, 20, 60, 0), 1: (-30, 0, 60, 0), 2: (-30, -20, 60, 0),
            3: (-20, 30, 60, 90), 4: (0, 30, 60, 90), 5: (20, 30, 60, 90)
        }
        t.penup()
        if lst[0] == [o] * 3:
            t.setpos(*winning_lines[0][:2])
            t.pendown()
            t.forward(winning_lines[0][2])
        elif lst[1] == [o] * 3:
            t.setpos(*winning_lines[1][:2])
            t.pendown()
            t.forward(winning_lines[1][2])
        elif lst[2] == [o] * 3:
            t.setpos(*winning_lines[2][:2])
            t.pendown()
            t.forward(winning_lines[2][2])
        elif [lst[0][0], lst[1][0], lst[2][0]] == [o] * 3:
            t.setpos(*winning_lines[3][:2])
            t.pendown()
            t.forward(winning_lines[3][2])
        elif [lst[0][1], lst[1][1], lst[2][1]] == [o] * 3:
            t.setpos(*winning_lines[4][:2])
            t.pendown()
            t.forward(winning_lines[4][2])
        elif [lst[0][2], lst[1][2], lst[2][2]] == [o] * 3:
            t.setpos(*winning_lines[5][:2])
            t.pendown()
            t.forward(winning_lines[5][2])
        if [lst[0][0], lst[1][1], lst[2][2]] == [o] * 3:
            t.setpos(-30, 30)
            t.pendown()
            t.goto(30, -30)
        elif [lst[0][2], lst[1][1], lst[2][0]] == [o] * 3:
            t.setpos(30, 30)
            t.pendown()
            t.goto(-30, -30)
        t.penup()
        t.setpos(0, -80)
        t.pendown()
        t.write('YOU WON!', align="center", font=("Arial", 24, "normal"))
        return 1
    t.color('red')
    if [x] * 3 in lst or [x] * 3 in [list(row) for row in zip(*lst)]:
        winning_lines = {
            0: (-30, 20, 60, 0), 1: (-30, 0, 60, 0), 2: (-30, -20, 60, 0),
            3: (-20, 30, 60, 90), 4: (0, 30, 60, 90), 5: (20, 30, 60, 90)
        }
        t.penup()
        if lst[0] == [x] * 3:
            t.setpos(*winning_lines[0][:2])
            t.pendown()
            t.forward(winning_lines[0][2])
        elif lst[1] == [x] * 3:
            t.setpos(*winning_lines[1][:2])
            t.pendown()
            t.forward(winning_lines[1][2])
        elif lst[2] == [x] * 3:
            t.setpos(*winning_lines[2][:2])
            t.pendown()
            t.forward(winning_lines[2][2])
        elif [lst[0][0], lst[1][0], lst[2][0]] == [x] * 3:
            t.setpos(*winning_lines[3][:2])
            t.pendown()
            t.forward(winning_lines[3][2])
        elif [lst[0][1], lst[1][1], lst[2][1]] == [x] * 3:
            t.setpos(*winning_lines[4][:2])
            t.pendown()
            t.forward(winning_lines[4][2])
        elif [lst[0][2], lst[1][2], lst[2][2]] == [x] * 3:
            t.setpos(*winning_lines[5][:2])
            t.pendown()
            t.forward(winning_lines[5][2])
        if [lst[0][0], lst[1][1], lst[2][2]] == [x] * 3:
            t.setpos(-30, 30)
            t.pendown()
            t.goto(30, -30)
        elif [lst[0][2], lst[1][1], lst[2][0]] == [x] * 3:
            t.setpos(30, 30)
            t.pendown()
            t.goto(-30, -30)
        t.penup()
        t.setpos(0, -80)
        t.pendown()
        t.write('YOU LOST!', align="center", font=("Arial", 24, "normal"))
        return 2
    if '*' not in [j for i in lst for j in i]:
        t.penup()
        t.setpos(0, -80)
        t.pendown()
        t.write('DRAW!', align="center", font=("Arial", 24, "normal"))
        return 3
    return 0

# Function to save the game data
def save_game_to_json(file_name: str, data: list) -> None:
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Function to load the game data from JSON file
def load_game_from_json(file_name: str) -> list:
    with open(file_name, 'r') as file:
        return json.load(file)

# Main function to handle the game logic
def main():
    """
    Main function to handle the game logic and play the game of Tic-Tac-Toe.
    """
    data = load_txt('players.txt')
    t.setup(400, 400)
    t.speed(0)
    t.hideturtle()
    draw_board()
    t.title("Tic-Tac-Toe")

    lst = [['*'] * 3 for _ in range(3)]
    turn = 1

    while True:
        if turn % 2 == 1:
            lst = input_move(lst, f'{Fore.RED}x{Style.RESET_ALL}')
        else:
            lst = make_move(lst, f'{Fore.BLUE}o{Style.RESET_ALL}')
        print(print_board(lst))
        if check_board(lst) == 1:
            print('Congratulations! You have won.')
            break
        elif check_board(lst) == 2:
            print('Sorry, you have lost.')
            break
        elif check_board(lst) == 3:
            print('The game is a draw.')
            break
        turn += 1
        t.clear()

    save_game_to_json('game_result.json', lst)

if __name__ == "__main__":
    doctest.testmod()
    main()


# In[ ]:





# In[ ]:





# In[ ]:




